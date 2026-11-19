"""Discrete search: minimise # monochromatic 3-APs over 2-colourings of [n] (exact counts)."""
import sys, json, time, os
import numpy as np
from multiprocessing import Pool
from fractions import Fraction as F
from common import ap_W, count_mono_brute, BLOCKS, blocks_of
import qlib

n = int(sys.argv[1]); NSA = int(sys.argv[2]); NTB = int(sys.argv[3])
OUT = f"dsearch_n{n}.jsonl"

def twelve_rounded(n):
    # largest-remainder rounding of the 12 block lengths to sum n
    raw = np.array(BLOCKS, float) * n / 548
    L = np.floor(raw).astype(int); rem = n - L.sum()
    L[np.argsort(-(raw - L))[:rem]] += 1
    x = np.concatenate([[(-1) ** b] * L[b] for b in range(12)]).astype(float)
    return x

W = T = None
def init():
    global W, T, M
    W, T = ap_W(n); M = np.ascontiguousarray(W.astype(np.float64))

def V_of(x):
    return (T + qlib.qv(M, x) / 2) / 4

def start(fam, k, rng):
    if fam == "rand": return rng.choice([-1.0, 1.0], n)
    if fam == "blocks":
        nb = 2 + k % 29
        cuts = np.sort(rng.choice(np.arange(1, n), nb - 1, replace=False))
        e = np.concatenate([[0], cuts, [n]]); x = np.empty(n); sg = rng.choice([-1, 1])
        for b in range(nb): x[e[b]:e[b + 1]] = sg * (-1) ** b
        return x
    if fam == "twelve": return twelve_rounded(n)
    raise ValueError

def job(a):
    method, fam, k, seed, T0, T1 = a
    rng = np.random.default_rng(seed)
    x0 = start(fam, k, rng); t = time.time()
    if method == "sa":
        steps = 3000 * n if fam != "twelve" else 1000 * n
        if fam == "twelve": T0 = T0 / 30          # low-temperature polish of the rounded 12-block colouring
        x, f = qlib.sa(M, x0, seed, steps, T0, T1, 0.1, 40)
    else:
        x, f = qlib.tabu(M, x0, seed, 300 * n, max(5, n // 40), max(5, n // 40))
    v = V_of(x)
    col = [int(c) for c in x]
    vb = count_mono_brute(col)                       # independent recount
    bl = blocks_of(x)
    return dict(n=n, method=method, fam=fam, k=k, seed=seed, V=vb, V_qf=v, Vn2=vb / n / n,
                secs=round(time.time() - t, 2), nruns=len(bl),
                runs=[(s, L) for s, L in bl] if len(bl) <= 60 else None, col="".join("+" if c > 0 else "-" for c in col))

if __name__ == "__main__":
    init()
    x12 = twelve_rounded(n)
    g = M @ x12; d = -4 * x12 * g; med = float(np.median(np.abs(d)))
    v12 = count_mono_brute([int(c) for c in x12])
    print(f"n={n}: T={T}, twelve-block rounded colouring V={v12} (V/n^2={v12/n/n:.6f}); 117/2192={117/2192:.6f}; 117n^2/2192-n/2={117*n*n/2192-n/2:.1f}; med|flip|={med}", flush=True)
    jobs = []; sd = 50000 * n
    for k in range(NSA):
        sd += 1; jobs.append(("sa", "rand" if k % 2 == 0 else "blocks", k, sd, 3 * med, 0.003 * med))
    for k in range(max(2, NSA // 10)):
        sd += 1; jobs.append(("sa", "twelve", k, sd, 3 * med, 0.003 * med))
    for k in range(NTB):
        sd += 1; jobs.append(("tabu", "rand" if k % 2 == 0 else "blocks", k, sd, 0, 0))
    best = None; t0 = time.time()
    with Pool(int(os.environ.get("NW", 3)), initializer=init) as pool, open(OUT, "w") as fo:
        for i, r in enumerate(pool.imap_unordered(job, jobs)):
            fo.write(json.dumps(r) + "\n"); fo.flush()
            assert r["V"] == round(r["V_qf"]), (r["V"], r["V_qf"])
            if best is None or r["V"] < best:
                best = r["V"]
                print(f"[{i+1}/{len(jobs)} {time.time()-t0:.0f}s] best V={best} V/n^2={best/n/n:.6f} by {r['method']}/{r['fam']} runs={r['nruns']}", flush=True)
    print("done", time.time() - t0)
