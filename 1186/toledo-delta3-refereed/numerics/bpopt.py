"""Off-grid search: step functions with k blocks, breakpoints real. Exact Q (float, closed-form areas),
exact gradient dQ/dt_k = (s_k - s_{k+1}) G(t_k). Projected gradient descent with block collapse."""
import sys, json, time
import numpy as np
from fractions import Fraction as F
from common import BLOCKS, Q_step, phistar_breaks
QSTAR = -5 / 137

def areas(e):
    """matrix of area(R ∩ [e_i,e_{i+1}] x [e_j,e_{j+1}]), vectorised exact piecewise-linear integration."""
    a0 = e[:-1][:, None]; a1 = e[1:][:, None]
    b0 = e[:-1][None, :]; b1 = e[1:][None, :]
    k = len(e) - 1
    A0 = np.broadcast_to(a0, (k, k)); A1 = np.broadcast_to(a1, (k, k))
    P = np.stack([A0, A1, np.clip(2 * b0 - 1, A0, A1), np.clip(2 * b1 - 1, A0, A1),
                  np.clip(2 * b0 + 0 * A0, A0, A1), np.clip(2 * b1 + 0 * A0, A0, A1)], -1)
    P = np.sort(P, -1)
    B0 = b0[..., None]; B1 = b1[..., None]
    L = np.maximum(0, np.minimum(B1, (1 + P) / 2) - np.maximum(B0, P / 2))
    return np.sum((P[..., 1:] - P[..., :-1]) * (L[..., 1:] + L[..., :-1]) / 2, -1)

def Qf(t, s0):
    e = np.concatenate([[0.0], t, [1.0]]); k = len(e) - 1
    s = s0 * (-1.0) ** np.arange(k)
    return float(s @ areas(e) @ s)

def Gf(a, t, s0):
    e = np.concatenate([[0.0], t, [1.0]]); k = len(e) - 1
    s = s0 * (-1.0) ** np.arange(k)
    cum = np.concatenate([[0.0], np.cumsum(s * np.diff(e))])
    def Phi(x):
        j = np.clip(np.searchsorted(e, x, side="right") - 1, 0, k - 1)
        return cum[j] + s[j] * (x - e[j])
    a = np.asarray(a)
    return Phi((1 + a) / 2) - Phi(a / 2) + Phi(np.minimum(1, 2 * a)) - Phi(np.maximum(0, 2 * a - 1))

def grad(t, s0):
    k = len(t) + 1
    s = s0 * (-1.0) ** np.arange(k)
    return (s[:-1] - s[1:]) * Gf(t, t, s0)

def collapse(t, s0, eps=1e-11):
    e = list(np.concatenate([[0.0], t, [1.0]]))
    changed = True
    while changed and len(e) > 2:
        changed = False
        for i in range(len(e) - 1):
            if e[i + 1] - e[i] < eps:
                if i == 0:            # first block vanishes: drop breakpoint e[1], sign flips
                    del e[1]; s0 = -s0
                elif i == len(e) - 2:  # last block vanishes
                    del e[-2]
                else:                  # interior block vanishes: neighbours merge
                    del e[i:i + 2]
                changed = True; break
    return np.array(e[1:-1]), s0

def descend(t, s0, iters=700):
    t = np.array(sorted(t), float); q = Qf(t, s0); eta = 0.5
    for it in range(iters):
        if len(t) == 0: break
        g = grad(t, s0)
        if np.max(np.abs(g)) < 1e-13: break
        # max step keeping order
        e = np.concatenate([[0.0], t, [1.0]])
        de = np.concatenate([[0.0], -g, [0.0]])
        rate = de[:-1] - de[1:]            # d(length)/d(eta) = -(de_{i+1}-de_i)
        lens = np.diff(e)
        with np.errstate(divide="ignore", invalid="ignore"):
            lim = np.where(rate > 0, lens / rate, np.inf)
        emax = float(np.min(lim))
        step = min(eta, emax)
        while True:
            tn = t - step * g
            if step >= emax - 1e-15:
                tn = np.clip(tn, 0, 1); tn, s0n = collapse(np.sort(tn), s0)
            else:
                s0n = s0
            qn = Qf(tn, s0n)
            if qn <= q - 1e-4 * step * float(g @ g) * (1 if len(tn) == len(t) else 0) or step < 1e-14:
                break
            step *= 0.5
        if qn > q + 1e-15:
            break
        if len(tn) == len(t) and abs(q - qn) < 1e-16 and step < 1e-12:
            break
        t, s0, q = tn, s0n, qn
        eta = min(1.0, step * 2.5)
    return t, s0, q

def descend_fast(t, s0, iters=6000, eta=0.1):
    t = np.array(sorted(t), float); ql = Qf(t, s0); tl, sl = t.copy(), s0
    for it in range(iters):
        if len(t) == 0: break
        g = grad(t, s0)
        if np.max(np.abs(g)) < 1e-13: break
        tn = t - eta * g; sn = s0
        e = np.concatenate([[0.0], tn, [1.0]])
        if np.any(np.diff(e) < 1e-10):
            tn, sn = collapse(np.sort(np.clip(tn, 0, 1)), s0, eps=1e-10)
            if Qf(tn, sn) > Qf(t, s0) + 1e-15:
                eta /= 2
                if eta < 1e-9: break
                continue
        t, s0 = tn, sn
        if it % 50 == 49:
            q = Qf(t, s0)
            if q > ql + 1e-15:
                t, s0, eta = tl.copy(), sl, eta / 2
            else:
                tl, sl, ql = t.copy(), s0, q; eta = min(eta * 1.2, 0.5)
    return t, s0, Qf(t, s0)

if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    per_k = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    out = open("bpopt.jsonl", "w")
    ts, ss = phistar_breaks()
    tstar = np.array([float(x) for x in ts[1:-1]])
    # sanity: closed-form float Q matches exact at phi*, and gradient ~0
    print("Qf(phi*) =", Qf(tstar, 1.0), " exact -5/137 =", QSTAR, " max|grad| =", np.max(np.abs(grad(tstar, 1.0))), flush=True)
    # control: Qf vs exact Fractions at a random 9-block function
    tr = np.sort(rng.random(8)); fr = [F(0)] + [F(x) for x in tr] + [F(1)]
    print("Qf vs exact Fraction on random 9-block:", Qf(tr, 1.0), float(Q_step(fr, [(-1) ** i for i in range(9)])), flush=True)
    best = (1, None); t0 = time.time(); cnt = 0
    # (a) from perturbations of phi* (off-grid moves)
    for r in range(30):
        t = np.clip(tstar + rng.normal(0, [0.002, 0.01, 0.03][r % 3], 11), 1e-6, 1 - 1e-6)
        t, s0, q = descend(np.sort(t), 1.0, iters=1500)
        out.flush(); out.write(json.dumps(dict(start="phistar_jitter", k=12, q=q, gap=q - QSTAR, nb=len(t) + 1, t=list(t), s0=s0)) + "\n"); cnt += 1
        if q < best[0]: best = (q, ("phistar_jitter", list(t), s0))
    print(f"after phi* jitters: best {best[0]:.15f} gap {best[0]-QSTAR:.3e} ({time.time()-t0:.0f}s)", flush=True)
    # (b) random k-block starts, k = 2..40, plus antisymmetric ones
    for k in range(2, 31):
        for r in range(per_k):
            if r % 2 == 0:
                t = np.sort(rng.random(k - 1))
            else:
                h = np.sort(rng.random((k - 1) // 2) * 0.5)
                t = np.sort(np.concatenate([h, 1 - h] + ([[0.5]] if (k - 1) % 2 else [])))
            s0 = float(rng.choice([-1, 1]))
            t, s0, q = descend(t, s0, iters=1500)
            out.write(json.dumps(dict(start="rand_anti" if r % 2 else "rand", k=k, q=q, gap=q - QSTAR, nb=len(t) + 1, t=list(t), s0=s0)) + "\n"); out.flush(); cnt += 1
            if q < best[0]: best = (q, (k, list(t), s0))
        print(f"k={k}: best so far {best[0]:.15f} gap {best[0]-QSTAR:.3e} ({time.time()-t0:.0f}s, {cnt} runs)", flush=True)
    print("BEST", best)
