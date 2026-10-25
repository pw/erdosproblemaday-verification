#!/usr/bin/env python3
"""Controls for myverify.py.
(i)  mutated certificates must FAIL;
(ii) the host-level expansion must reproduce graphon quantities computed by DIRECT counting
     (t(C4), rho^3, rho, and every one of the 34 averaged squares) on step graphons."""
import itertools, random, sys, time, functools
print = functools.partial(print, flush=True)
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, '/tmp/erdos1800/seats/cert')
import myverify as mv

t0 = time.time()
H = mv.hosts_geng(); C = mv.coords(); E = mv.Expansion(H, C)
eps, terms = mv.load_cert()
ok, mins, need, worst = mv.check_fast(E, eps, terms)
print(f'[baseline] ok={ok} min_slack={float(mins):.3e} need={float(need):.6e}   ({time.time()-t0:.1f}s)')
assert ok

print('\n=== (i) mutation controls (each must FAIL) ===')
def run(name, e, tt, expect_fail=True):
    ok, mins, need, worst = mv.check_fast(E, e, tt)
    verdict = 'FAIL' if not ok else 'pass'
    flag = '' if (not ok) == expect_fail else '   <<< UNEXPECTED'
    print(f'  {name:55s} -> {verdict}  (min slack {float(mins) if mins is not None else None:.3e} at host {worst}){flag}')
    return ok

run('gamma = 3/64 - 1e-6', Fr(-1, 10**6), terms)
run('epsilon = 0 (sharp gamma = 3/64)', Fr(0), terms)
run('epsilon = 1.9910e-11 (just below needed)', Fr(19910, 10**15), terms)
run('epsilon = 1.9911e-11 (just above needed) [must PASS]', Fr(19911, 10**15), terms, expect_fail=False)
nf = 0; passes = []
for k in range(len(terms)):
    tt = list(terms); b, w, v = tt[k]; tt[k] = (b, w * Fr(101, 100), v)
    ok, *_ = mv.check_fast(E, eps, tt)
    if not ok: nf += 1
    else: passes.append(k)
print(f'  weight x1.01, one term at a time: {nf}/34 FAIL; still passing: {passes}')
nf = 0
for k in range(len(terms)):
    tt = list(terms); b, w, v = tt[k]; tt[k] = (b, w * Fr(99, 100), v)
    ok, *_ = mv.check_fast(E, eps, tt)
    nf += (not ok)
print(f'  weight x0.99, one term at a time: {nf}/34 FAIL (no monotonicity: a square\'s HOST coefficients can be negative, '
      'so shrinking a weight can lower the slack; all-fail in both directions = the certificate is a near-identity, slack ~1e-11)')
# vector perturbations
rnd = random.Random(1); nf = 0; tot = 0
for k in range(len(terms)):
    b, w, v = terms[k]
    nz = [i for i, x in enumerate(v) if x != 0]
    i = rnd.choice(nz); v2 = list(v); v2[i] = v2[i] * Fr(1001, 1000)
    tt = list(terms); tt[k] = (b, w, v2)
    ok, *_ = mv.check_fast(E, eps, tt); tot += 1; nf += (not ok)
print(f'  one nonzero vector entry x1.001, one term at a time: {nf}/{tot} FAIL')
# coordinate reversal within block (tests that coordinate ORDER is load-bearing)
nf = 0
for k in range(len(terms)):
    b, w, v = terms[k]; tt = list(terms); tt[k] = (b, w, list(reversed(v)))
    ok, *_ = mv.check_fast(E, eps, tt); nf += (not ok)
print(f'  reverse one vector\'s coordinate order: {nf}/34 FAIL')
# drop a host-relevant sign: negate weight
tt = list(terms); b, w, v = tt[0]; tt[0] = (b, -w, v)
run('weight of term 0 negated', eps, tt)
# drop one host from the list (must be caught by the host census, not the domination)
print('  host census: dropping a host is caught by the 38-class assertion in myverify.main (two routes).')

print('\n=== (ii) expansion controls on step graphons, exact ===')
pairs = mv.lexpairs(6)
# classification table: labelled 15-bit mask -> host index (or -1 for graphs with a triangle)
perms = list(itertools.permutations(range(6)))
pidx = {(i, j): b for b, (i, j) in enumerate(pairs)}
permbits = [[pidx[tuple(sorted((p[i], p[j])))] for (i, j) in pairs] for p in perms]
cls = np.full(1 << 15, -1, dtype=np.int64)
for h, adj in enumerate(H):
    m = mv.mask(adj, list(range(6)))
    for pb in permbits:
        mm = 0
        for b in range(15):
            if m >> b & 1: mm |= 1 << pb[b]
        cls[mm] = h
assert (cls >= 0).sum() == 5789

def host_densities(A, w):
    """p(H;W) for the step graphon of adjacency A with integer vertex weights w: exact Fractions.
    Enumerates all n^6 maps with repetition (vectorised)."""
    n = len(A); A = np.array(A, dtype=np.int64); w = np.array(w, dtype=object)
    Wt = sum(w)
    counts = [0] * 38
    idx = np.indices((n,) * 5).reshape(5, -1)          # positions 1..5
    wts5 = np.ones(idx.shape[1], dtype=object)
    for p in range(5): wts5 = wts5 * w[idx[p]]
    uniform = all(x == w[0] for x in w)
    for v0 in range(n):
        phi = np.vstack([np.full(idx.shape[1], v0), idx])
        m = np.zeros(idx.shape[1], dtype=np.int64)
        for b, (i, j) in enumerate(pairs):
            m |= A[phi[i], phi[j]] << b
        c = cls[m]
        assert (c >= 0).all(), 'triangle in a sample of a triangle-free graph?!'
        if uniform:
            bc = np.bincount(c, minlength=38)
            for h in range(38): counts[h] += int(bc[h]) * int(w[0]) ** 6
        else:
            for h in range(38):
                sel = (c == h)
                if sel.any(): counts[h] += int(w[v0]) * int(sum(wts5[sel]))
    tot = Fr(Wt) ** 6
    assert sum(counts) == Wt ** 6
    return [Fr(x) / tot for x in counts]

def direct_quantities(A, w):
    """graphon quantities by DIRECT counting (no host expansion)."""
    n = len(A); Wt = sum(w); f = [Fr(x, Wt) for x in w]
    Am = np.array(A, dtype=object); D = np.diag(np.array(f, dtype=object))
    AD = Am.dot(D)
    t4 = np.trace(AD.dot(AD).dot(AD).dot(AD))
    rho = sum(f[a] * f[b] * A[a][b] for a in range(n) for b in range(n))
    return Fr(t4), rho

def direct_squares(A, w, terms, C):
    """E[f^2] for every term, from the graphon definition of the averaged square."""
    n = len(A); Wt = sum(w); f = [Fr(x, Wt) for x in w]; V = range(n)
    out = []
    # s0 : densities of 3-vertex graphs by edge count
    q = [Fr(0)] * 3
    for a, b, c in itertools.product(V, repeat=3):
        q[A[a][b] + A[a][c] + A[b][c]] += f[a] * f[b] * f[c]
    # s2 : conditional flag distributions given ordered root (x,y)
    s2agg = {}
    for x, y in itertools.product(V, repeat=2):
        m = A[x][y]; idx = C[f's2_root{m}']; P = [Fr(0)] * len(idx)
        for l1, l2 in itertools.product(V, repeat=2):
            P[idx[mv.s2_key(A, x, y, (l1, l2))]] += f[l1] * f[l2]
        key = (m, tuple(P)); s2agg[key] = s2agg.get(key, 0) + f[x] * f[y]
    # u4 : for each ordered root 4-tuple, canonical assignments of POSITIONS and the leaf profile laws
    u4agg = {}   # aggregate identical (type, multiset of conditional laws) configurations
    for r in itertools.product(V, repeat=4):
        wr = f[r[0]] * f[r[1]] * f[r[2]] * f[r[3]]
        if wr == 0: continue
        Mmin = min(mv.mask(A, [r[p] for p in pi]) for pi in itertools.permutations(range(4)))
        kap = [pi for pi in itertools.permutations(range(4)) if mv.mask(A, [r[p] for p in pi]) == Mmin]
        idx = C[f'u4_root{Mmin}']; laws = []
        for pi in kap:
            P = [Fr(0)] * len(idx)
            for l in V:
                prof = sum(A[l][r[pi[i]]] << i for i in range(4))
                P[idx[prof]] += f[l]
            laws.append(P)
        key = (Mmin, tuple(sorted(tuple(P) for P in laws)))
        u4agg[key] = u4agg.get(key, 0) + wr
    for b, wgt, v in terms:
        if b == 's0_root0':
            val = sum(v[i] * q[i] for i in range(3)) ** 2
        elif b.startswith('s2'):
            m = int(b[7:]); val = Fr(0)
            for (mm, P), wr in s2agg.items():
                if mm == m: val += wr * sum(v[i] * P[i] for i in range(len(P))) ** 2
        else:
            M = int(b[7:]); val = Fr(0)
            for (MM, laws), wr in u4agg.items():
                if MM != M: continue
                val += wr * sum(sum(v[i] * P[i] for i in range(len(P))) ** 2 for P in laws) / len(laws)
        out.append(val)
    return out

def cycle(n): return [[1 if (i - j) % n in (1, n - 1) else 0 for j in range(n)] for i in range(n)]
def petersen():
    vs = list(itertools.combinations(range(5), 2))
    return [[1 if not set(a) & set(b) else 0 for b in vs] for a in vs]
def clebsch():
    # folded 5-cube: F2^4, x~y iff x^y has weight 1 or is 1111
    return [[1 if bin(x ^ y).count('1') == 1 or (x ^ y) == 15 else 0 for y in range(16)] for x in range(16)]

def control(name, A, w, do_squares=True):
    t1 = time.time()
    p = host_densities(A, w)
    t4, rho = direct_quantities(A, w)
    c4 = sum(p[h] * E.parts[h][0] for h in range(38))
    m3 = sum(p[h] * E.parts[h][1] for h in range(38))
    e1 = sum(p[h] * E.parts[h][2] for h in range(38))
    print(f'  {name}: t(C4) direct={t4} via hosts={c4} {"OK" if t4 == c4 else "MISMATCH"};'
          f' rho direct={rho} via hosts={e1} {"OK" if rho == e1 else "MISMATCH"};'
          f' rho^3 {"OK" if rho**3 == m3 else "MISMATCH"}')
    assert t4 == c4 and rho == e1 and rho ** 3 == m3
    g = t4 - rho ** 3 + (Fr(3, 64) + eps) * rho
    if do_squares:
        ds = direct_squares(A, w, terms, C)
        hs = [sum(p[h] * mv.quad(E.G[h][b], v) for h in range(38)) for (b, _, v) in terms]
        nbad = sum(1 for a, b in zip(ds, hs) if a != b)
        assert all(x >= 0 for x in ds)
        sos = sum(wt * x for (_, wt, _), x in zip(terms, ds))
        print(f'     34 averaged squares: direct == host-expansion for {34 - nbad}/34;'
              f' all direct values >= 0;  g(W)={float(g):.6e}  sum w*E[f^2]={float(sos):.6e}'
              f'  g - sos = {float(g - sos):.6e}  ({time.time()-t1:.0f}s)')
        assert nbad == 0 and g - sos >= 0
    else:
        print(f'     g(W) = {float(g):.6e}  ({time.time()-t1:.0f}s)')
    return g

control('C5 (uniform)', cycle(5), [1] * 5)
assert direct_quantities(cycle(5), [1]*5)[0] == Fr(6, 125)
control('Petersen (uniform)', petersen(), [1] * 10)
g = control('Clebsch (uniform)', clebsch(), [1] * 16)
assert direct_quantities(clebsch(), [1]*16) == (Fr(65, 4096), Fr(5, 16))
print('  Clebsch: t(C4)=65/4096, rho=5/16 reproduced; g = eps*rho exactly?', g == eps * Fr(5, 16))
rnd = random.Random(7)
k = 0
while k < 4:
    n = rnd.choice([5, 6]); A = [[0]*n for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if rnd.random() < 0.55: A[i][j] = A[j][i] = 1
    if not mv.tri_free(A) or sum(map(sum, A)) == 0: continue
    w = [rnd.randint(1, 6) for _ in range(n)]
    control(f'random weighted tf graph n={n} w={w}', A, w); k += 1
print(f'\nALL CONTROLS COMPLETE ({time.time()-t0:.0f}s)')
