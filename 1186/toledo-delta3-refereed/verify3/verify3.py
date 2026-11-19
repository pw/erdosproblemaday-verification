#!/usr/bin/env python3
"""Third, independent verifier for Toledo's delta_3 certificates (erdosproblemaday.com, 2026-11-19).

Written from the paper (draft v0.2, sections 2-5) and CERT-FORMAT.md only. It does not read or import
the claimant's generators, the claimant's verifier, or cert-machine's verify.js.

Different methods from verify.js where it matters:
  * cell areas: exact integration of the section length in a, cross-checked by integration in b;
  * positive definiteness: fraction-free (Bareiss) elimination on the integer matrix D*(S + eps*I),
    all leading principal minors > 0 (Sylvester), no floating point anywhere.

Usage: verify3.py CERT.json [--mutate NAME]   exit 0 = accepted, 1 = refused, 2 = could not run.
"""
import json, sys, math
from fractions import Fraction as F

U = 1096
BLOCKS = [28, 6, 28, 37, 59, 116, 116, 59, 37, 28, 6, 28]          # out of 548
EDGES = []                                                           # in units of 1/1096
acc = 0
for L in BLOCKS:
    acc += 2 * L
    EDGES.append(acc)
assert EDGES[-1] == U
SIGN = [1 if k % 2 == 0 else -1 for k in range(len(BLOCKS))]

def block_of_unit(k):                       # unit interval [k, k+1] (units of 1/1096)
    for b, e in enumerate(EDGES):
        if k < e:
            return b
    raise ValueError(k)

UNIT_SIGN = [SIGN[block_of_unit(k)] for k in range(U)]

def phi_int(lo, hi):
    """exact integral of phi* over [lo, hi] (Fractions in [0,1])"""
    lo, hi = max(lo, F(0)), min(hi, F(1))
    if hi <= lo:
        return F(0)
    tot, start = F(0), F(0)
    for b, e in enumerate(EDGES):
        end = F(e, U)
        ov = min(hi, end) - max(lo, start)
        if ov > 0:
            tot += SIGN[b] * ov
        start = end
    return tot

def g(a):
    return (phi_int(a / 2, (1 + a) / 2) + phi_int(2 * a - 1, 2 * a)) / 2

def area_in(c1, d1, c2, d2):
    """area of R ∩ [c1,d1]x[c2,d2], R = {a/2 <= b <= (1+a)/2}; integrate in a"""
    pts = {c1, d1}
    for t in (2 * c2, 2 * d2, 2 * c2 - 1, 2 * d2 - 1):
        if c1 < t < d1:
            pts.add(t)
    pts = sorted(pts)
    def ln(a):
        return max(F(0), min(d2, (1 + a) / 2) - max(c2, a / 2))
    return sum((ln(l) + ln(r)) / 2 * (r - l) for l, r in zip(pts, pts[1:]))

def area_in_b(c1, d1, c2, d2):
    """same area, integrating in b: for fixed b, a in [max(c1, 2b-1), min(d1, 2b)]"""
    pts = {c2, d2}
    for t in ((c1 + 1) / 2, (d1 + 1) / 2, c1 / 2, d1 / 2):
        if c2 < t < d2:
            pts.add(t)
    pts = sorted(pts)
    def ln(b):
        return max(F(0), min(d1, 2 * b) - max(c1, 2 * b - 1))
    return sum((ln(l) + ln(r)) / 2 * (r - l) for l, r in zip(pts, pts[1:]))

# ---------- h on the unit grid ----------
GN = [g(F(k, U)) for k in range(U + 1)]
# h on unit interval k is linear from hL[k] to hR[k] (checked below)
HL = [-UNIT_SIGN[k] * GN[k] for k in range(U)]
HR = [-UNIT_SIGN[k] * GN[k + 1] for k in range(U)]

def lemma1_report():
    out = []
    # linearity of g on every unit interval: interior points at 1/3, 1/2, 2/3
    for k in range(U):
        for t in (F(1, 3), F(1, 2), F(2, 3)):
            a = F(k, U) + t / U
            assert g(a) == GN[k] + t * (GN[k + 1] - GN[k]), ('g not linear', k, t)
    # continuity of h at every node (g = 0 where phi* changes sign)
    for k in range(1, U):
        assert HR[k - 1] == HL[k], ('h discontinuous', k)
    assert all(v >= 0 for v in HL + HR), 'h negative somewhere'
    zeros = [k for k in range(U + 1) if (HL[k] if k < U else HR[U - 1]) == 0]
    integral = sum((HL[k] + HR[k]) / 2 for k in range(U)) / U
    # Q(phi*) from block-rectangle areas
    starts = [0] + EDGES[:-1]
    Q = F(0)
    for i in range(12):
        for j in range(12):
            A = area_in(F(starts[i], U), F(EDGES[i], U), F(starts[j], U), F(EDGES[j], U))
            Q += SIGN[i] * SIGN[j] * A
    slopes = set()
    for k in zeros:
        if 0 < k < U:
            slopes.add((HR[k] - HL[k]) * U if False else (HL[k] - HR[k - 1]) * 0 + (HR[k] - HL[k]) * U)
            slopes.add((HR[k - 1] - HL[k - 1]) * U)
    out.append(f"Q(phi*) = {Q}   int h = {integral}   h >= 0, linear on every 1/1096 interval, continuous")
    out.append(f"zeros of h (units of 1/1096): {zeros}   edges: {EDGES[:-1]}")
    out.append(f"one-sided slopes at the zeros: {sorted(slopes)}")
    return Q, integral, zeros, out

# ---------- bathtub minorant per cell ----------
def bathtub(p, q, reading='summed'):
    w = F(q - p, U)
    pieces = [(HL[k], HR[k]) for k in range(p, q)]
    a = w * min(min(x, y) for x, y in pieces)
    if any(x == y for x, y in pieces):
        return a, F(0)
    vals = sorted(set(v for pc in pieces for v in pc))
    best = F(0)
    for lo, hi in zip(vals, vals[1:]):
        v = (lo + hi) / 2
        contrib = [F(1, U) / abs(y - x) for x, y in pieces if min(x, y) < v < max(x, y)]   # 1/|slope|
        s = sum(contrib) if reading == 'summed' else (max(contrib) if contrib else F(0))
        best = max(best, s)
    return a, w * w / 2 / best

def beta_exact(p, q, y):
    """exact bathtub value min ∫_cell h sigma, 0<=sigma<=1, ∫sigma = y*w: fill lowest levels"""
    mass = F(q - p, U) * y
    # each unit piece is linear; the sublevel set {h < v} has measure m(v); find v with m(v)=mass
    pieces = [(HL[k], HR[k]) for k in range(p, q)]
    def m_of(v):
        tot = F(0)
        for x, z in pieces:
            lo, hi = min(x, z), max(x, z)
            if v >= hi:
                tot += F(1, U)
            elif v > lo:
                tot += F(1, U) * (v - lo) / (hi - lo)
        return tot
    def int_below(v):          # ∫ min(h, v) over {h < v}  ->  ∫_{h<v} h
        tot = F(0)
        for x, z in pieces:
            lo, hi = min(x, z), max(x, z)
            if hi == lo:
                if v > lo:
                    tot += F(1, U) * lo
                continue
            if v >= hi:
                tot += F(1, U) * (lo + hi) / 2
            elif v > lo:
                frac = (v - lo) / (hi - lo)
                tot += F(1, U) * frac * (lo + v) / 2
        return tot
    vals = sorted(set(v for pc in pieces for v in pc))
    # m is piecewise linear in v between consecutive vals; find the segment
    prev = vals[0]
    if mass == 0:
        return F(0)
    for v in vals:
        if m_of(v) >= mass:
            break
        prev = v
    lo_v, hi_v = prev, v
    m_lo, m_hi = m_of(lo_v), m_of(hi_v)
    if m_hi == m_lo:
        vstar = hi_v
    else:
        vstar = lo_v + (hi_v - lo_v) * (mass - m_lo) / (m_hi - m_lo)
    # plateau pieces (constant h) may need a partial fill at level vstar
    return int_below(vstar) + (mass - m_of(vstar)) * vstar

# ---------- polynomial bookkeeping ----------
class Poly:
    def __init__(self, n):
        self.n, self.c, self.lin, self.q = n, F(0), [F(0)] * n, {}
    def addq(self, i, j, v):
        if i > j:
            i, j = j, i
        self.q[(i, j)] = self.q.get((i, j), F(0)) + v

MIRROR = False

def classify(grid):
    n = len(grid) - 1
    if MIRROR:
        cells = [(F(grid[i], U), F(grid[i + 1], U)) for i in range(n)]
        pairs = []
        for i in range(n):
            for j in range(n):
                A = area_in(*cells[j], *cells[i])
                ww = (cells[i][1] - cells[i][0]) * (cells[j][1] - cells[j][0])
                pairs.append((i, j, 'absent' if A == 0 else ('full' if A == ww else 'cut'), A, ww))
        return cells, pairs
    cells = [(F(grid[i], U), F(grid[i + 1], U)) for i in range(n)]
    pairs = []
    for i in range(n):
        for j in range(n):
            A = area_in(*cells[i], *cells[j])
            assert A == area_in_b(*cells[i], *cells[j]), ('area routes disagree', i, j)
            ww = (cells[i][1] - cells[i][0]) * (cells[j][1] - cells[j][0])
            kind = 'absent' if A == 0 else ('full' if A == ww else 'cut')
            pairs.append((i, j, kind, A, ww))
    return cells, pairs

def check_grid(grid):
    assert grid[0] == 0 and grid[-1] == U, 'grid ends'
    assert all(x < y for x, y in zip(grid, grid[1:])), 'grid not increasing'
    missing = [e for e in EDGES if e not in grid]
    assert not missing, f'grid misses edges {missing}'

def cell_signs(grid):
    s = []
    for i in range(len(grid) - 1):
        ss = set(UNIT_SIGN[k] for k in range(grid[i], grid[i + 1]))
        assert len(ss) == 1, 'phi* not constant on a cell'
        s.append(ss.pop())
    return s

def int_matrix_pd(M):
    """Bareiss on an integer symmetric matrix: True iff every leading principal minor > 0."""
    n = len(M)
    A = [row[:] for row in M]
    prev = 1
    for k in range(n):
        if A[k][k] <= 0:
            return False, k, A[k][k]
        akk = A[k][k]
        for i in range(k + 1, n):
            aik = A[i][k]
            row_i, row_k = A[i], A[k]
            for j in range(k + 1, n):
                row_i[j] = (row_i[j] * akk - aik * row_k[j]) // prev
        prev = akk
    return True, n, prev

def to_int_matrix(S):
    den = 1
    for row in S:
        for v in row:
            den = den * v.denominator // math.gcd(den, v.denominator)
    return [[int(v * den) for v in row] for row in S], den

def assemble_L_base(grid, pairs, s, ab, theta=None, inner=False):
    n = len(grid) - 1
    P = Poly(n)
    for i, (a, b) in enumerate(ab):
        P.lin[i] += a
        P.addq(i, i, b)
    cut_idx = 0
    for (i, j, kind, A, ww) in pairs:
        ss = s[i] * s[j]
        if kind == 'full':
            P.addq(i, j, ss * ww)
        elif kind == 'cut':
            Aout = ww - A
            if inner:
                if ss == -1:
                    P.addq(i, j, -ww)
            else:
                th = theta[cut_idx]
                if ss == 1:          # th*0 + (1-th)*(ww*yi*yj - Aout)
                    P.addq(i, j, (1 - th) * ww)
                    P.c -= (1 - th) * Aout
                else:                # th*(-Ain) + (1-th)*(-ww*yi*yj)
                    P.c -= th * A
                    P.addq(i, j, -(1 - th) * ww)
            cut_idx += 1
    return P, cut_idx

def m_terms(w):            # m = sum w_k y_k
    return w

def sub_form(P, kind, idx, mu, w, lo, hi):
    n = P.n
    if mu < 0:
        raise AssertionError(f'negative multiplier {kind} {idx}')
    def lin(i, v): P.lin[i] -= mu * v
    def q(i, j, v): P.addq(i, j, -mu * v)
    def const(v): P.c -= mu * v
    def times_m(coef_const, coef_lin_j=None, j=None, sign=1):
        pass
    if kind == 'yy':
        i, j = idx; q(i, j, 1)
    elif kind == '11':
        i, j = idx; const(1); lin(i, -1); lin(j, -1); q(i, j, 1)
    elif kind == 'y1':
        i, j = idx; lin(i, 1); q(i, j, -1)
    elif kind == 'yd':
        i = idx; lin(i, 1); q(i, i, -1)
    elif kind == '11d':
        i = idx; const(1); lin(i, -2); q(i, i, 1)
    elif kind == 'y':
        lin(idx, 1)
    elif kind == '1':
        const(1); lin(idx, -1)
    elif kind == 'mlo':                       # m - lo
        const(-lo); [lin(k, w[k]) for k in range(n)]
    elif kind == 'mhi':                       # hi - m
        const(hi); [lin(k, -w[k]) for k in range(n)]
    elif kind == 'mm':                        # (m-lo)(hi-m) = -m^2 + (lo+hi) m - lo*hi
        const(-lo * hi)
        for k in range(n):
            lin(k, (lo + hi) * w[k])
            for l in range(k, n):
                q(k, l, -(w[k] * w[l] if k == l else 2 * w[k] * w[l]))
    elif kind in ('mlo_y', 'mlo_1', 'mhi_y', 'mhi_1'):
        j = idx
        # (m - lo) or (hi - m) as  sgn*m + c0
        sgn, c0 = (1, -lo) if kind.startswith('mlo') else (-1, hi)
        if kind.endswith('_y'):               # (sgn m + c0) y_j
            lin(j, c0)
            for k in range(n):
                q(k, j, sgn * w[k])
        else:                                 # (sgn m + c0)(1 - y_j)
            const(c0); lin(j, -c0)
            for k in range(n):
                lin(k, sgn * w[k]); q(k, j, -sgn * w[k])
    elif kind == 'tri':
        i, j, k, sg = idx
        s1, s2, s3 = sg
        assert len({i, j, k}) == 3, 'triangle with repeated index'
        assert {s1, s2, s3} <= {1, -1} and s1 * s2 * s3 == 1, 'triangle signs not valid'
        const(1)
        for (sv, x, y) in ((s1, i, j), (s2, j, k), (s3, i, k)):   # z_x z_y = 1 - 2y_x - 2y_y + 4 y_x y_y
            const(sv); lin(x, -2 * sv); lin(y, -2 * sv); q(x, y, 4 * sv)
    else:
        raise AssertionError(f'unknown form {kind}')

def S_matrix(P):
    n = P.n
    S = [[F(0)] * (n + 1) for _ in range(n + 1)]
    S[0][0] = P.c
    for i in range(n):
        S[0][i + 1] = S[i + 1][0] = P.lin[i] / 2
    for (i, j), v in P.q.items():
        if i == j:
            S[i + 1][i + 1] += v
        else:
            S[i + 1][j + 1] += v / 2
            S[j + 1][i + 1] += v / 2
    return S

def apply_common(grid, mutate):
    if mutate == 'dropedge':
        grid = [x for x in grid if x != EDGES[0]]
    return grid

def verify_slab(d, mutate=None):
    grid = apply_common(d['grid'], mutate)
    check_grid(grid)
    s = cell_signs(grid)
    n = len(grid) - 1
    cells, pairs = classify(grid)
    w = [c[1] - c[0] for c in cells]
    ab = [bathtub(grid[i], grid[i + 1]) for i in range(n)]
    if mutate == 'aplus':
        ab[1] = (ab[1][0] + F(1, 10**9), ab[1][1])
    lo, hi, B, eps, claim = (F(d[k]) for k in ('lo', 'hi', 'B', 'eps', 'claim'))
    theta = [F(t) for t in d['theta']]
    forms = d['forms']
    if mutate == 'B+1e-6':
        B += F(1, 10**6); claim += F(1, 10**6)
    if mutate == 'eps0':
        eps = F(0); claim = B
    if mutate == 'theta1':
        theta = [F(1)] * len(theta)
    if mutate == 'notri':
        forms = [f for f in forms if f[0] != 'tri']
    if mutate == 'negmu':
        forms = [list(f) for f in forms]; forms[0][2] = '-' + forms[0][2]
    if mutate == 'badtri':
        forms = [list(f) for f in forms]
        for f in forms:
            if f[0] == 'tri':
                f[1] = [f[1][0], f[1][1], f[1][2], [-f[1][3][0], f[1][3][1], f[1][3][2]]]; break
    if mutate == 'widen':
        hi += F(1, 100)
    assert all(0 <= t <= 1 for t in theta), 'theta outside [0,1]'
    P, ncut = assemble_L_base(grid, pairs, s, ab, theta)
    assert ncut == len(theta), f'theta count {len(theta)} != cut pairs {ncut}'
    P.c -= B
    for kind, idx, mu in forms:
        sub_form(P, kind, idx, F(mu), w, lo, hi)
    assert eps >= 0
    assert claim == B - eps * (1 + n), 'claim != B - eps(1+n)'
    assert claim > 0, 'claim not positive'
    S = S_matrix(P)
    for i in range(n + 1):
        S[i][i] += eps
    M, den = to_int_matrix(S)
    ok, k, last = int_matrix_pd(M)
    assert ok, f'S + eps I not positive definite (leading minor {k} = {last if abs(last) < 10**30 else "..."})'
    return dict(n=n, lo=lo, hi=hi, claim=claim, cut=ncut, forms=len(forms), den_bits=den.bit_length())

def verify_inner(d, mutate=None):
    grid = apply_common(d['grid'], mutate)
    check_grid(grid)
    s = cell_signs(grid)
    n = len(grid) - 1
    cells, pairs = classify(grid)
    w = [c[1] - c[0] for c in cells]
    ab = [bathtub(grid[i], grid[i + 1]) for i in range(n)]
    if mutate == 'aplus':
        ab[1] = (ab[1][0] + F(1, 10**9), ab[1][1])
    rin = F(d['rin'])
    lam = {tuple(map(int, k.split(','))): F(v) for k, v in d['lam'].items()}
    nu = [F(v) for v in d['nu']]
    kap = F(d['kap'])
    N = {tuple(map(int, k.split(','))): F(v) for k, v in d['N'].items()}
    c = [F(v) for v in d['c']]
    if mutate == 'rin2':
        rin = 2 * rin
    if mutate == 'negmu':
        k0 = next(iter(lam)); lam[k0] = -lam[k0]
    if mutate == 'droplam':
        lam = dict(list(lam.items())[: len(lam) // 2])
    assert rin == F(1, 5), 'inner radius is not 1/5'
    assert all(v >= 0 for v in lam.values()) and all(v >= 0 for v in nu) and kap >= 0 and all(v >= 0 for v in c), 'negative multiplier'
    assert all(v >= 0 for v in N.values()), 'N not entrywise nonnegative'
    assert all(i <= j for (i, j) in N), 'N key not upper triangular'
    P0, _ = assemble_L_base(grid, pairs, s, ab, inner=True)
    assert P0.c == 0
    # linear identity: a_i = sum_j lam_ij + nu_i rin + kap rin w_i + c_i
    rhs = [c[i] + nu[i] * rin + kap * rin * w[i] for i in range(n)]
    for (i, j), v in lam.items():
        rhs[i] += v
    bad = [i for i in range(n) if rhs[i] != P0.lin[i]]
    assert not bad, f'linear identity fails at {len(bad)} cells (first {bad[:5]})'
    # quadratic: P = Quad(L0) + sum lam_ij y_i y_j + sum_j nu_j y_j m + kap m^2 - N
    Pq = Poly(n)
    for k, v in P0.q.items():
        Pq.addq(*k, v)
    for (i, j), v in lam.items():
        Pq.addq(i, j, v)
    for j in range(n):
        if nu[j]:
            for k in range(n):
                Pq.addq(k, j, nu[j] * w[k])
    if kap:
        for k in range(n):
            for l in range(k, n):
                Pq.addq(k, l, kap * (w[k] * w[l] if k == l else 2 * w[k] * w[l]))
    for (i, j), v in N.items():
        Pq.addq(i, j, -(v if i == j else 2 * v))
    S = S_matrix(Pq)
    S = [row[1:] for row in S[1:]]
    M, den = to_int_matrix(S)
    ok, k, last = int_matrix_pd(M)
    assert ok, f'P not positive definite (leading minor {k})'
    return dict(n=n, rin=rin, lam=len(lam), N=len(N), den_bits=den.bit_length())

if __name__ == '__main__':
    path = sys.argv[1]
    mutate = sys.argv[sys.argv.index('--mutate') + 1] if '--mutate' in sys.argv else None
    if mutate == 'mirror':
        MIRROR = True
    if path == '--lemma1':
        Q, I, z, out = lemma1_report()
        print('\n'.join(out))
        sys.exit(0 if (Q == F(-5, 137) and I == F(5, 137)) else 1)
    try:
        d = json.load(open(path))
    except Exception as e:
        print('CANNOT RUN', e); sys.exit(2)
    import time
    t0 = time.time()
    try:
        r = verify_inner(d, mutate) if 'rin' in d else verify_slab(d, mutate)
    except AssertionError as e:
        print(f'REFUSED {path} mutate={mutate}: {e}  ({time.time()-t0:.1f}s)'); sys.exit(1)
    r = {k: (str(v) if isinstance(v, F) else v) for k, v in r.items()}
    print(f'ACCEPTED {path} mutate={mutate}: {r}  ({time.time()-t0:.1f}s)')
    sys.exit(0)
