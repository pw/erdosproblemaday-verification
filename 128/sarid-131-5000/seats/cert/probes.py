#!/usr/bin/env python3
"""Numeric necessary-condition probes for Prop 3.1:  g(W) = t(C4,W) - rho^3 + gamma*rho >= 0.
(a) every triangle-free graph on <= 10 vertices (geng -t), exact rationals;
(b) the seven known triangle-free SRGs, exact;
(c) weighted blow-ups: connected triangle-free graphs on <= 8 vertices, multistart SLSQP on the simplex,
    minimising both g and the normalised h = t4/rho - rho^2 (claim: h >= -gamma);
(d) local weighted probes around the SRGs and a few named triangle-free graphs."""
import itertools, subprocess, sys, time, functools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import minimize
print = functools.partial(print, flush=True)
sys.path.insert(0, '/tmp/erdos1800/seats/cert')
import myverify as mv

GAMMA = Fr(3, 64) + Fr(1, 50_000_000_000); GF = float(GAMMA)

def geng(n, conn=False):
    args = ['/usr/bin/nauty-geng', '-tq' + ('c' if conn else ''), str(n)]
    return [mv.parse_g6(s)[1] for s in subprocess.run(args, capture_output=True, text=True, check=True).stdout.split()]

def g_exact(A):
    n = len(A); M = np.array(A, dtype=np.int64)
    t4 = int(np.trace(np.linalg.matrix_power(M, 4)))
    e2 = int(M.sum())                          # = 2e
    rho = Fr(e2, n * n)
    return Fr(t4, n ** 4) - rho ** 3 + GAMMA * rho, rho, Fr(t4, n ** 4)

t0 = time.time()
print('=== (a) all triangle-free graphs on n <= 10 vertices, uniform weights, exact ===')
glob = None
for n in range(1, 11):
    Gs = geng(n); best = None; besth = None
    for A in Gs:
        g, rho, t4 = g_exact(A)
        if best is None or g < best[0]: best = (g, A)
        if rho > 0:
            h = t4 / rho - rho ** 2
            if besth is None or h < besth[0]: besth = (h, A)
    neg = sum(1 for A in Gs if g_exact(A)[0] < 0)
    hs = f'{float(besth[0]):.6f} at {mv.g6_of(besth[1])}' if besth else 'n/a (no edges)'
    print(f'  n={n:2d}: {len(Gs):6d} graphs; negatives={neg}; min g={float(best[0]):.6e} ({mv.g6_of(best[1])});'
          f' min h=t4/rho-rho^2={hs} (claim: >= -{GF:.6f})')
    assert neg == 0

print('\n=== (b) the seven triangle-free strongly regular graphs, exact ===')
def check_srg(A, v, k, lam, mu):
    M = np.array(A, dtype=np.int64); n = len(M)
    assert n == v and (M == M.T).all() and (np.diag(M) == 0).all() and set(M.sum(1)) == {k}
    M2 = M @ M
    for i in range(n):
        for j in range(n):
            if i != j: assert M2[i, j] == (lam if M[i, j] else mu)
def cycle(n): return [[1 if (i - j) % n in (1, n - 1) else 0 for j in range(n)] for i in range(n)]
def kneser(n, k):
    vs = list(itertools.combinations(range(n), k))
    return [[1 if not set(a) & set(b) else 0 for b in vs] for a in vs]
def clebsch():
    return [[1 if bin(x ^ y).count('1') == 1 or (x ^ y) == 15 else 0 for y in range(16)] for x in range(16)]
def hoffman_singleton():
    # Robertson pentagons/pentagrams (own transcription): P_h j ~ P_h j+-1, Q_i j ~ Q_i j+-2, P_h j ~ Q_i (h*i+j)
    idx = {}
    for t in 'PQ':
        for a in range(5):
            for j in range(5): idx[(t, a, j)] = len(idx)
    A = [[0]*50 for _ in range(50)]
    def add(u, v): A[idx[u]][idx[v]] = A[idx[v]][idx[u]] = 1
    for h in range(5):
        for j in range(5):
            add(('P', h, j), ('P', h, (j + 1) % 5)); add(('Q', h, j), ('Q', h, (j + 2) % 5))
            for i in range(5): add(('P', h, j), ('Q', i, (h * i + j) % 5))
    return A
def steiner_3_6_22():
    # PG(2,4) + infinity; blocks = lines+inf and one class of 56 hyperovals (even pairwise meets). Own code.
    F_add = lambda a, b: a ^ b
    log = {1: 0, 2: 1, 3: 2}; exp = {0: 1, 1: 2, 2: 3}
    F_mul = lambda a, b: 0 if a == 0 or b == 0 else exp[(log[a] + log[b]) % 3]
    pts = [(1, x, y) for x in range(4) for y in range(4)] + [(0, 1, y) for y in range(4)] + [(0, 0, 1)]
    def dot(u, v):
        s = 0
        for a, b in zip(u, v): s = F_add(s, F_mul(a, b))
        return s
    lines = sorted({frozenset(i for i, p in enumerate(pts) if dot(l, p) == 0) for l in pts}, key=sorted)
    assert len(lines) == 21 and all(len(l) == 5 for l in lines)
    col = set()
    for l in lines:
        for t in itertools.combinations(sorted(l), 3): col.add(t)
    ovals = []
    def ext(arc, s):
        if len(arc) == 6: ovals.append(frozenset(arc)); return
        for p in range(s, 21):
            if all(tuple(sorted((a, b, p))) not in col for a, b in itertools.combinations(arc, 2)): ext(arc + [p], p + 1)
    ext([], 0); assert len(ovals) == 168
    orbit = [o for o in ovals if len(o & ovals[0]) % 2 == 0]; assert len(orbit) == 56
    blocks = [l | {21} for l in lines] + orbit
    cover = set()
    for b in blocks:
        for t in itertools.combinations(sorted(b), 3):
            assert t not in cover; cover.add(t)
    assert len(cover) == 1540
    return blocks
def disj_graph(bl): return [[1 if not (a & b) else 0 for b in bl] for a in bl]
def higman_sims(bl):
    A = [[0]*100 for _ in range(100)]
    def add(u, v): A[u][v] = A[v][u] = 1
    for p in range(22): add(0, 1 + p)
    for i, b in enumerate(bl):
        for p in b: add(1 + p, 23 + i)
    for i, j in itertools.combinations(range(77), 2):
        if not (bl[i] & bl[j]): add(23 + i, 23 + j)
    return A
BL = steiner_3_6_22()
SRG = [('C5', cycle(5), (5, 2, 0, 1)), ('Petersen', kneser(5, 2), (10, 3, 0, 1)), ('Clebsch', clebsch(), (16, 5, 0, 2)),
       ('Hoffman-Singleton', hoffman_singleton(), (50, 7, 0, 1)),
       ('Gewirtz', disj_graph([b for b in BL if 21 not in b]), (56, 10, 0, 2)),
       ('M22', disj_graph(BL), (77, 16, 0, 4)), ('Higman-Sims', higman_sims(BL), (100, 22, 0, 6))]
for name, A, par in SRG:
    check_srg(A, *par)
    g, rho, t4 = g_exact(A)
    print(f'  {name:18s} srg{par} verified;  rho={rho}  t(C4)={t4}  g={g} = {float(g):.6e}   h={float(t4/rho - rho**2):.6f}')
    assert g >= 0

print('\n=== (c) weighted blow-ups: connected triangle-free graphs on <= 8 vertices, multistart SLSQP ===')
def make_funcs(A):
    A = np.array(A, dtype=float)
    def parts(w):
        AD = A * w[None, :]
        P2 = AD @ AD; P3 = P2 @ AD
        t4 = np.trace(P2 @ P2); rho = w @ A @ w
        gt4 = 4 * np.diag(P3 @ A)               # d tr((AD)^4) / dw_a = 4 [(AD)^3 A]_aa
        grho = 2 * A @ w
        return t4, rho, gt4, grho
    def g(w):
        t4, rho, gt4, grho = parts(w)
        return t4 - rho ** 3 + GF * rho, gt4 - 3 * rho ** 2 * grho + GF * grho
    def h(w):
        t4, rho, gt4, grho = parts(w)
        rho = max(rho, 1e-12)
        return t4 / rho - rho ** 2, gt4 / rho - t4 * grho / rho ** 2 - 2 * rho * grho
    return g, h, parts
def multistart(A, starts, rng, extra=()):
    n = len(A); g, h, parts = make_funcs(A)
    cons = [{'type': 'eq', 'fun': lambda w: w.sum() - 1, 'jac': lambda w: np.ones_like(w)}]
    consh = cons + [{'type': 'ineq', 'fun': lambda w: parts(w)[1] - 1e-6}]
    bnds = [(0, 1)] * n
    best_g = (np.inf, None); best_h = (np.inf, None)
    x0s = [np.full(n, 1 / n)] + list(extra) + [rng.dirichlet(np.ones(n) * rng.choice([0.3, 1, 3])) for _ in range(starts)]
    for x0 in x0s:
        r = minimize(g, x0, jac=True, method='SLSQP', bounds=bnds, constraints=cons, options={'maxiter': 500, 'ftol': 1e-15})
        w = np.clip(r.x, 0, None); w /= w.sum(); val = g(w)[0]
        if val < best_g[0]: best_g = (val, w)
        if parts(x0)[1] > 1e-6:
            r = minimize(h, x0, jac=True, method='SLSQP', bounds=bnds, constraints=consh, options={'maxiter': 500, 'ftol': 1e-15})
            w = np.clip(r.x, 0, None); w /= w.sum()
            if parts(w)[1] > 1e-7:
                val = h(w)[0]
                if val < best_h[0]: best_h = (val, w)
    return best_g, best_h
rng = np.random.default_rng(2026)
overall_g = (np.inf, None, None); overall_h = (np.inf, None, None)
for n in range(2, 9):
    Gs = geng(n, conn=True); starts = 60 if n <= 7 else 15
    bg = (np.inf, None, None); bh = (np.inf, None, None)
    for A in Gs:
        (vg, wg), (vh, wh) = multistart(A, starts, rng)
        if vg < bg[0]: bg = (vg, A, wg)
        if vh < bh[0]: bh = (vh, A, wh)
    print(f'  n={n}: {len(Gs):3d} connected graphs x {starts+1} starts:  min g = {bg[0]: .3e} ({mv.g6_of(bg[1])});'
          f'  min h = {bh[0]:.9f} at {mv.g6_of(bh[1])} w={np.round(bh[2], 4).tolist()}   [{time.time()-t0:.0f}s]')
    if bg[0] < overall_g[0]: overall_g = bg
    if bh[0] < overall_h[0]: overall_h = bh
print(f'  OVERALL (c): min g = {overall_g[0]:.3e};  min h = {overall_h[0]:.9f} vs claim -gamma = {-GF:.9f}; margin = {overall_h[0] + GF:.3e}')

print('\n=== (d) local weighted probes: SRGs and named graphs, starts = uniform + perturbations + random ===')
def andrasfai(k):
    n = 3 * k - 1
    return [[1 if (i - j) % n % 3 == 1 else 0 for j in range(n)] for i in range(n)]
def mycielski(A):
    n = len(A); B = [[0]*(2*n+1) for _ in range(2*n+1)]
    for i in range(n):
        for j in range(n):
            if A[i][j]: B[i][j] = 1; B[i][n+j] = B[n+j][i] = 1
        B[n+i][2*n] = B[2*n][n+i] = 1
    return B
named = SRG + [('Grotzsch', mycielski(cycle(5)), None), ('Andrasfai(3)', andrasfai(3), None), ('Andrasfai(4)', andrasfai(4), None),
               ('Andrasfai(5)', andrasfai(5), None), ('Kneser(7,3)', kneser(7, 3), None), ('Kneser(8,3)', kneser(8, 3), None),
               ('Mobius-Kantor GP(8,3)', None, None), ('C5 x Clebsch?', None, None)]
def gp(n, k):
    A = [[0]*(2*n) for _ in range(2*n)]
    def add(u, v): A[u][v] = A[v][u] = 1
    for i in range(n): add(i, (i+1) % n); add(i, n+i); add(n+i, n+(i+k) % n)
    return A
named[-2] = ('Mobius-Kantor GP(8,3)', gp(8, 3), None)
named = named[:-1]
for name, A, _ in named:
    assert mv.tri_free(A) if len(A) <= 20 else True
    n = len(A); u = np.full(n, 1 / n)
    extra = [np.clip(u * (1 + rng.normal(0, s, n)), 1e-9, None) for s in (0.01, 0.05, 0.2) for _ in range(4)]
    extra = [x / x.sum() for x in extra]
    starts = 20 if n <= 20 else 4
    (vg, wg), (vh, wh) = multistart(A, starts, rng, extra=extra)
    gu, hu, parts = make_funcs(A)
    print(f'  {name:22s} n={n:3d}: uniform h={hu(u)[0]: .9f};  min g found={vg: .3e};  min h found={vh: .9f}'
          f'  (margin to -gamma {vh + GF: .3e}); max|w - uniform| at min h = {np.abs(wh - u).max():.2e}  [{time.time()-t0:.0f}s]')
print(f'\nPROBES COMPLETE ({time.time()-t0:.0f}s)')
