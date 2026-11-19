"""Continuous search: minimise Q over x in [-1,1]^N, Q = x^T S2 x / (8 N^2), S2 = K + K^T exact integer grid matrix."""
import sys, json, time, os
import numpy as np
from multiprocessing import Pool
from fractions import Fraction as F
from common import grid_S2, phistar_grid, blocks_of, BLOCKS
import qlib

N = int(sys.argv[1]); SCALE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
TAG = sys.argv[3] if len(sys.argv) > 3 else "true"     # 'true' or a control name
CS = float(os.environ.get("CS", SCALE)); NW = int(os.environ.get("NW", 4))
OUT = f"csearch_N{N}_{TAG}{os.environ.get('SUFFIX', '')}.jsonl"
QSTAR = -5 / 137

def build_M(tag):
    S2 = grid_S2(N).astype(np.float64)
    if tag in ("true", "smoke"):
        return S2, None
    return np.ascontiguousarray(np.load(f"M_{tag}_N{N}.npy")), None

PH = phistar_grid(N).astype(np.float64)

def family_start(fam, k, rng):
    if fam == "rand_pm1": return rng.choice([-1.0, 1.0], N)
    if fam == "rand_unif": return rng.uniform(-1, 1, N)
    if fam == "smooth":
        w = [N / 200, N / 50, N / 20, N / 8][k % 4]
        z = rng.normal(size=N + 8 * int(w) + 8)
        ker = np.exp(-0.5 * (np.arange(-4 * int(w) - 4, 4 * int(w) + 5) / w) ** 2)
        y = np.convolve(z, ker, mode="valid")[:N]
        y = y / (np.std(y) + 1e-12)
        return np.tanh(2 * y) if k % 2 else np.sign(y)
    if fam in ("blocks", "anti_blocks"):
        nb = 2 + k % 29          # 2..30 blocks
        if fam == "blocks":
            cuts = np.sort(rng.choice(np.arange(1, N), nb - 1, replace=False))
            sg = rng.choice([-1, 1]); x = np.empty(N)
            edges = np.concatenate([[0], cuts, [N]])
            for b in range(nb): x[edges[b]:edges[b + 1]] = sg * (-1) ** b
            return x
        half = N // 2
        nh = max(1, nb // 2)
        cuts = np.sort(rng.choice(np.arange(1, half), nh - 1, replace=False)) if nh > 1 else np.array([], int)
        edges = np.concatenate([[0], cuts, [half]])
        sg = rng.choice([-1, 1]); y = np.empty(half)
        for b in range(nh): y[edges[b]:edges[b + 1]] = sg * (-1) ** b
        return np.concatenate([y, -y[::-1]])
    if fam == "phistar_pert":
        x = PH.copy() * rng.choice([-1, 1]); r = N // 548
        edges = np.cumsum([0] + [L * r for L in BLOCKS])
        mode = k % 5
        if mode == 0:   # flip one block
            b = rng.integers(12); x[edges[b]:edges[b + 1]] *= -1
        elif mode == 1:  # shift every edge randomly
            sh = int(rng.integers(3, 25)) * r
            e2 = edges.copy(); e2[1:-1] = np.clip(edges[1:-1] + rng.integers(-sh, sh + 1, 11), 1, N - 1); e2 = np.sort(e2)
            sg = x[0]
            for b in range(12): x[e2[b]:e2[b + 1]] = sg * (-1) ** b
        elif mode == 2:  # noise flips
            p = rng.uniform(0.02, 0.3); m = rng.random(N) < p; x[m] *= -1
        elif mode == 3:  # flip a few small intervals
            for _ in range(rng.integers(1, 8)):
                L = int(rng.integers(2, N // 20)); l = int(rng.integers(0, N - L)); x[l:l + L] *= -1
        else:  # continuous noise
            x = np.clip(x + rng.normal(0, rng.uniform(0.3, 1.5), N), -1, 1)
        return x
    raise ValueError(fam)

def classify(M, x, method, fam, k, seed, extra=None):
    q = qlib.qv(M, x) / (8 * N * N)
    xr = np.where(x > 1 - 1e-9, 1, np.where(x < -1 + 1e-9, -1, 0))
    nfrac = int(np.sum(xr == 0))
    ham = int(min(np.sum(xr != PH), np.sum(xr != -PH)))
    bl = blocks_of(x)
    rec = dict(N=N, tag=TAG, method=method, fam=fam, k=int(k), seed=int(seed), Q=q, gap=q - QSTAR,
               nfrac=nfrac, ham=ham, nblocks=len(bl), mean=float(x.mean()),
               blocks=[(int(s), round(L * 548 / N, 3)) for s, L in bl] if len(bl) <= 40 else None)
    if extra: rec.update(extra)
    return rec, x

M = None
def init(tag):
    global M
    M, _ = build_M(tag)

def job(args):
    method, fam, k, seed, T0, T1 = args
    rng = np.random.default_rng(seed)
    x0 = family_start(fam, k, rng)
    t = time.time()
    if method == "cd":
        x, sw = qlib.cd(M, x0, seed)
        ext = {"sweeps": sw}
    elif method == "sa":
        steps = int(SCALE * 1500 * N)
        x, f = qlib.sa(M, x0, seed, steps, T0, T1)
        x, sw = qlib.cd(M, x, seed)
        ext = {"steps": steps}
    elif method == "tabu":
        it = int(SCALE * 200 * N)
        x, f = qlib.tabu(M, x0, seed, it, max(5, N // 60), max(5, N // 60))
        x, sw = qlib.cd(M, x, seed)
        ext = {"iters": it}
    elif method == "pg":
        # projected gradient with heavy-ball momentum, then CD polish
        L = T0  # pass spectral norm in T0 slot
        x = x0.copy(); v = np.zeros(N); eta = 1.0 / (2 * L)
        for it in range(int(SCALE * 3000)):
            g = 2 * (M @ x)
            xn = np.clip(x - eta * g + 0.8 * v, -1, 1); v = xn - x; x = xn
        qpg = qlib.qv(M, x) / (8 * N * N)
        x, sw = qlib.cd(M, x, seed)
        ext = {"Q_pg_before_cd": qpg}
    ext["Q_raw"] = qlib.qv(M, x) / (8 * N * N)
    xp, _ = qlib.tabu(M, x, seed + 1, 3 * N, 0, 1)      # snap to +-1 + steepest single-flip descent
    if qlib.qv(M, xp) <= qlib.qv(M, x): x = xp
    ext["secs"] = round(time.time() - t, 2)
    rec, x = classify(M, x, method, fam, k, seed, ext)
    if rec["gap"] < -1e-10 and TAG == "true":
        np.save(f"candidate_N{N}_{TAG}_{method}_{seed}.npy", x)
    return rec

if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    M0, _ = build_M(TAG)
    # temperature scale from single-flip deltas at phi*
    g = M0 @ PH
    d = -4 * PH * (g - np.diag(M0) * PH)
    med = float(np.median(np.abs(d)))
    L = float(np.max(np.abs(np.linalg.eigvalsh(M0)))) if N <= 2192 else None
    print(f"N={N} tag={TAG} Q(phi*)={qlib.qv(M0, PH)/(8*N*N):.15f} median|flip delta| at phi* = {med:.1f}, min flip delta = {d.min():.1f}, ||S||={L:.1f}", flush=True)
    jobs = []
    sd = 1000 * N + (0 if TAG == "true" else 7_000_000)
    fams_cd = [("rand_pm1", 800), ("rand_unif", 800), ("smooth", 800), ("blocks", 1160), ("anti_blocks", 1160), ("phistar_pert", 1000)]
    for fam, cnt in (fams_cd if not os.environ.get('SKIPCD') else []):
        for k in range(int(cnt * CS)):
            sd += 1; jobs.append(("cd", fam, k, sd, 0, 0))
    for fam, cnt in [("rand_pm1", 40), ("blocks", 40), ("anti_blocks", 30), ("smooth", 20), ("phistar_pert", 30)]:
        for k in range(int(cnt * CS)):
            sd += 1; jobs.append(("sa", fam, k, sd, 3 * med, 0.003 * med))
    for fam, cnt in [("rand_pm1", 40), ("blocks", 40), ("anti_blocks", 20), ("phistar_pert", 20)]:
        for k in range(int(cnt * CS)):
            sd += 1; jobs.append(("tabu", fam, k, sd, 0, 0))
    for fam, cnt in [("rand_unif", 24), ("smooth", 24), ("rand_pm1", 12)]:
        for k in range(int(cnt * CS)):
            sd += 1; jobs.append(("pg", fam, k, sd, L, 0))
    rng = np.random.default_rng(0); order = rng.permutation(len(jobs))
    jobs = [jobs[i] for i in order]
    print(f"{len(jobs)} jobs", flush=True)
    t0 = time.time(); best = 1.0
    with Pool(NW, initializer=init, initargs=(TAG,)) as pool, open(OUT, "w") as fo:
        for i, rec in enumerate(pool.imap_unordered(job, jobs, chunksize=1)):
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            if rec["Q"] < best:
                best = rec["Q"]
                print(f"[{i+1}/{len(jobs)} {time.time()-t0:.0f}s] new best {best:.12f} gap {rec['gap']:.3e} by {rec['method']}/{rec['fam']} ham={rec['ham']} nblocks={rec['nblocks']} nfrac={rec['nfrac']}", flush=True)
            if (i + 1) % 200 == 0:
                print(f"[{i+1}/{len(jobs)} {time.time()-t0:.0f}s]", flush=True)
    print("done", time.time() - t0)
