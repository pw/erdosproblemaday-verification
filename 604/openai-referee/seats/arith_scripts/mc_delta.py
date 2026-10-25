# Monte Carlo of Lemma 3.1 (paper p.9-10): law of Delta = d - i for the random nested grids of Sec 3.2.
# Faithful construction: uniform orientation theta, xi ~ U[0,log2), l_m = e^xi 2^m, shift s0 uniform mod l0 per axis,
# s_{m+1} = s_m + B_m l_m (B_m fair bit, per axis) for m>=0, s_m = s0 mod l_m for m<0. d = -log(smallest sharing side),
# i = -log R, Delta = d - i = log(R / l*).
# Controls (each removes one randomisation; the law should then DEPEND on the pair):
#   'fixed'   : theta=0, xi=0, shift=0 (deterministic grid)
#   'noxi'    : xi=0 (no log-uniform scale), rest random
#   'norot'   : theta=0 (no random orientation), rest random
import numpy as np, sys
from scipy.stats import ks_2samp
LOG2 = np.log(2.0)

def sample_delta(p, q, N, rng, mode='paper'):
    p = np.asarray(p, float); q = np.asarray(q, float)
    R = np.hypot(*(q - p))
    th = rng.uniform(0, 2*np.pi, N) if mode in ('paper', 'noxi', 'sameshift') else np.zeros(N)
    xi = rng.uniform(0, LOG2, N) if mode in ('paper', 'norot', 'sameshift') else np.zeros(N)
    c, s = np.cos(th), np.sin(th)
    # coordinates along the oriented axes (axis1 = (c,s), axis2 = (-s,c))
    P1 = p[0]*c + p[1]*s; P2 = -p[0]*s + p[1]*c
    Q1 = q[0]*c + q[1]*s; Q2 = -q[0]*s + q[1]*c
    l0 = np.exp(xi)
    if mode == 'fixed':
        s0 = np.zeros((N, 2))
    elif mode == 'sameshift':        # control: ONE shift used for both axes (not uniform on the torus)
        s0 = np.repeat(rng.uniform(0, 1, (N, 1)), 2, axis=1) * l0[:, None]
    else:
        s0 = rng.uniform(0, 1, (N, 2)) * l0[:, None]
    mlo = int(np.floor(np.log2(R/np.sqrt(2)))) - 2
    mhi = mlo + 60
    first = np.full(N, np.nan)
    # shifts for m>0 built incrementally from s0 with fresh fair bits
    sm_pos = s0.copy()          # s_0
    for m in range(mlo, mhi):
        l = l0 * 2.0**m
        if m <= 0:
            sm = np.mod(s0, l[:, None])
        else:
            if mode == 'fixed':
                bits = np.zeros((N, 2))
            else:
                bits = rng.integers(0, 2, (N, 2)).astype(float)
                if mode == 'sameshift': bits[:, 1] = bits[:, 0]
            sm_pos = sm_pos + bits * (l0 * 2.0**(m-1))[:, None]   # s_m = s_{m-1} + B l_{m-1}
            sm = sm_pos
        a1 = np.floor((P1 - sm[:, 0]) / l); b1 = np.floor((Q1 - sm[:, 0]) / l)
        a2 = np.floor((P2 - sm[:, 1]) / l); b2 = np.floor((Q2 - sm[:, 1]) / l)
        share = (a1 == b1) & (a2 == b2) & np.isnan(first)
        first[share] = np.log(l[share])
    if np.isnan(first).any():
        print(f"    [{mode}] {np.isnan(first).mean():.3f} of samples NEVER share a cell up to side 2^{mhi} (Delta=-inf)")
        first[np.isnan(first)] = np.inf
    return np.log(R) - first      # Delta = log(R/l*)

def report(tag, D):
    D = D[np.isfinite(D)] if np.isfinite(D).any() else D
    print(f"  {tag}: mean={D.mean():+.4f} sd={D.std():.4f} max={D.max():.4f} (log sqrt2={0.5*np.log(2):.4f}) "
          f"P(D<-1)={np.mean(D<-1):.4f} P(D<-2)={np.mean(D<-2):.5f} P(D<-3)={np.mean(D<-3):.5f}")

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    rng = np.random.default_rng(20261014)
    pairs = {
        'A: R=1, angle 0, at origin':       ((0.0, 0.0), (1.0, 0.0)),
        'B: R=317.3, angle 1.1, off-origin': ((123.4, -56.7), (123.4 + 317.3*np.cos(1.1), -56.7 + 317.3*np.sin(1.1))),
        'C: R=0.0037, angle pi/4':           ((-7.25, 3.5), (-7.25 + 0.0037*np.cos(np.pi/4), 3.5 + 0.0037*np.sin(np.pi/4))),
        'D: R=sqrt2 (=1.4142), angle 0':     ((0.0, 0.0), (np.sqrt(2), 0.0)),
    }
    print("PAPER CONSTRUCTION")
    S = {}
    for k, (p, q) in pairs.items():
        S[k] = sample_delta(p, q, N, rng, 'paper'); report(k, S[k])
    A2 = sample_delta(*pairs['A: R=1, angle 0, at origin'], N, rng, 'paper')
    ks = lambda x, y: ks_2samp(x, y)
    keys = list(pairs)
    print("  KS A vs A' (independent rerun, calibration):", ks(S[keys[0]], A2))
    for k in keys[1:]:
        print(f"  KS A vs {k[:1]}:", ks(S[keys[0]], S[k]))
    allD = np.concatenate(list(S.values()))
    print("TAILS (pooled, n=%d): empirical P(Delta<-u) vs paper bound 2*sqrt2*e^-u" % allD.size)
    for u in [0, 0.5, 1, 2, 3, 4, 5, 6]:
        print(f"  u={u}: emp={np.mean(allD < -u):.6f}  bound={2*np.sqrt(2)*np.exp(-u):.6f}  emp*e^u={np.mean(allD < -u)*np.exp(u):.4f}")
    print("CONTROLS (law SHOULD depend on pair)")
    print("  fixed grid, pair B (straddles the grid line u=0 forever):")
    sample_delta(*pairs[keys[1]], 1000, rng, "fixed")
    for mode, (k1, k2) in [('fixed', (keys[0], keys[2])), ('noxi', (keys[0], keys[3])), ('norot', (keys[0], keys[2]))]:
        x = sample_delta(*pairs[k1], N, rng, mode); y = sample_delta(*pairs[k2], N, rng, mode)
        report(f"{mode} {k1[:1]}", x); report(f"{mode} {k2[:1]}", y)
        print(f"  KS {mode}: {k1[:1]} vs {k2[:1]}:", ks(x, y))
    # extra norot control on direction only: same R, angles 0 and pi/4
    x = sample_delta((0, 0), (1, 0), N, rng, 'norot'); y = sample_delta((0, 0), (np.cos(np.pi/4), np.sin(np.pi/4)), N, rng, 'norot')
    print("  KS norot: R=1 angle 0 vs R=1 angle pi/4:", ks(x, y), " means", x.mean(), y.mean())
    # sameshift control: identical displacement (R=1, angle 0), two different base points
    x = sample_delta((0, 0), (1, 0), N, rng, 'sameshift'); y = sample_delta((0.5, -0.5), (1.5, -0.5), N, rng, 'sameshift')
    print("  KS sameshift: same displacement, base (0,0) vs (0.5,-0.5):", ks(x, y), " means", x.mean(), y.mean())
    x2 = sample_delta((0.5, -0.5), (1.5, -0.5), N, rng, 'paper')
    print("  KS paper    : same pair (0.5,-0.5)->(1.5,-0.5) vs pair A:", ks(S[keys[0]], x2))
