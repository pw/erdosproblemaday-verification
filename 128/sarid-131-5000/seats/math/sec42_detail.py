import numpy as np, sys
sys.path.insert(0,'/tmp/erdos1800/seats/math')
exec(open('sections234.py').read().split('# ---------- Corollary 4.2')[0])
src = open('sections234.py').read()
exec(src[src.index('def L(al):'):src.index('worst = np.inf; nt = 0')])
rng = np.random.default_rng(7)
ws = []; zero_a = 0
for _ in range(500):
    kind = rng.integers(0,3)
    if kind == 0: A = random_tf(rng, int(rng.integers(5,15)), rng.uniform(0.3,1))
    elif kind == 1:
        B0 = [cycle(5), petersen()][int(rng.integers(0,2))]; sizes = rng.integers(1,3,size=len(B0))
        if sizes.sum() > 15: continue
        A = blowup(B0, sizes, rng, rng.uniform(0,0.3))
    else: A = random_bipartite(rng, int(rng.integers(5,15)))
    n = len(A)
    if A.sum()==0: continue
    M = all_bipartitions(n); vals, Xs = internal(A, M)
    choice = int(np.argmin(vals)) if rng.random()<0.6 else int(rng.integers(0,len(M)))
    r, info = sec42(A, Xs[choice].astype(bool))
    if isinstance(r, list) or r == 'INFEASIBLE': continue
    if info[0] == 0: zero_a += 1; continue
    ws.append((r, info))
ws.sort(key=lambda u: u[0])
print("pairs with a>0 and mu>0:", len(ws), " (a=0 cases:", zero_a, ")")
print("smallest slacks (slack, (a, mu, rho, I)):")
for r, info in ws[:5]: print("  %.3e" % r, tuple(round(v,5) for v in info))
