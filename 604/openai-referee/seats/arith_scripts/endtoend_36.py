# End-to-end check of (3.2)+(3.5)+Lemma 3.1 => (3.6) on an explicit configuration in K = Q(i), [K:Q]=2.
# Points with integer coordinates (u,b); Z1 = u+ib, Z2 = u-ib in Z[i].  Places of K: one complex place (sigma=2/[K:Q]=1,
# ordinary modulus) and the Gaussian primes P over p (|.|_P extends |p|_p=1/p, sigma_P=[K_P:Q_p]/[K:Q]=ef/2).
# (3.6) predicts D(x,y) := L*(x,y) - S*(x) - S*(y) is the SAME number b* = 2kappa - <M1+M2> for every distinct pair.
# Also verifies pathwise (3.5) on every realized complex-place grid hierarchy (exact integers) and that grid cells nest.
# Controls (should make D(x,y) pair-DEPENDENT): drop finite places; Milne-normalized |.|_P (log||z|| = -v log NP) with the
# paper's weights (double conversion); complex weight 1/[K:Q] (forgetting the factor 2); grid without random orientation/scale
# is NOT used here (that is mc_delta.py's job).
import numpy as np, itertools, math, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_35 import hier_quantities, check
from fractions import Fraction as F

PTS = [(0, 0), (1, 0), (0, 1), (2, 1), (3, 3), (5, 2), (1, 4)]
n = len(PTS)
PAIRS = list(itertools.combinations(range(n), 2))
Z = {1: [complex(u, b) for u, b in PTS], 2: [complex(u, -b) for u, b in PTS]}
KAPPA = -1.4571842286601309   # from kappa_quad.py

def gdiv(z, pi):   # exact division in Z[i] if possible, else None
    a, b = int(z.real), int(z.imag); c, d = int(pi.real), int(pi.imag)
    N = c*c + d*d
    re, im = a*c + b*d, b*c - a*d          # z * conj(pi)
    if re % N or im % N: return None
    return complex(re // N, im // N)
def val(z, pi):
    v = 0
    while True:
        w = gdiv(z, pi)
        if w is None: return v
        z = w; v += 1
def gaussian_primes_over(p):
    if p == 2: return [(complex(1, 1), 2, 1)]          # (pi, e, f)
    if p % 4 == 3: return [(complex(p, 0), 1, 2)]
    for a in range(1, int(p**0.5) + 1):
        b2 = p - a*a; b = int(round(b2**0.5))
        if b*b == b2: return [(complex(a, b), 1, 1), (complex(a, -b), 1, 1)]
def rational_primes(m):
    ps, q = set(), 2
    while m > 1:
        while m % q == 0: ps.add(q); m //= q
        q += 1
    return ps

# ---- finite places (exact) ----
diffs = {j: {pr: Z[j][pr[1]] - Z[j][pr[0]] for pr in PAIRS} for j in (1, 2)}
primes = set()
for j in (1, 2):
    for z in diffs[j].values(): primes |= rational_primes(int(round(abs(z)**2)))
places = [pl for p in sorted(primes) for pl in gaussian_primes_over(p)]
print("finite places with a nonunit difference:", [(p_, int(round(abs(pi)**2)) , e, f) for p_ in sorted(primes) for (pi, e, f) in gaussian_primes_over(p_)])

def finite_contrib(weight_mode):
    # returns per-j dicts: Mfin, Sfin[x], Lfin[pair], ifin[pair]  (already multiplied by sigma_v and scaled to i-units)
    out = {}
    for j in (1, 2):
        Mf = 0.0; Sf = np.zeros(n); Lf = {pr: 0.0 for pr in PAIRS}; If = {pr: 0.0 for pr in PAIRS}
        for (pi, e, f) in places:
            p = int(round(abs(pi)**2)) if f == 1 and e == 1 else (2 if e == 2 else int(round(abs(pi))))
            dv = {frozenset(pr): F(val(diffs[j][pr], pi)) for pr in PAIRS}
            M, S, L, ray = hier_quantities(list(range(n)), dv); assert ray
            assert not check(list(range(n)), dv)[0]
            if weight_mode == 'paper':      # sigma = ef/2, |z|_P = p^{-v/e}  -> sigma * (v log p / e) = v f log p / 2
                scale = (e * f / 2) * (math.log(p) / e)
            elif weight_mode == 'milne_double':   # Milne-normalized: -log||z|| = v f log p, times sigma=ef/2 (double conversion)
                scale = (e * f / 2) * (f * math.log(p))
            elif weight_mode == 'none':
                scale = 0.0
            Mf += scale * float(M)
            for x in range(n): Sf[x] += scale * float(S[x])
            for pr in PAIRS:
                Lf[pr] += scale * float(L[frozenset(pr)]); If[pr] += scale * float(dv[frozenset(pr)])
        out[j] = (Mf, Sf, Lf, If)
    return out

# ---- complex place (Monte Carlo over the paper's random nested grids, common random numbers across pairs) ----
LOG2 = math.log(2)
def grid_first_share(points, rng):
    th = rng.uniform(0, 2*math.pi); xi = rng.uniform(0, LOG2); l0 = math.exp(xi)
    c, s = math.cos(th), math.sin(th)
    X = np.array([[z.real*c + z.imag*s, -z.real*s + z.imag*c] for z in points])
    s0 = rng.uniform(0, 1, 2) * l0
    first = {}
    sm = s0.copy(); prev_cells = None
    for m in range(-6, 40):
        l = l0 * 2.0**m
        if m <= 0: sh = np.mod(s0, l)
        else:
            sm = sm + rng.integers(0, 2, 2) * (l0 * 2.0**(m-1)); sh = sm
        cells = [tuple(np.floor((X[k] - sh) / l).astype(np.int64)) for k in range(n)]
        if prev_cells is not None:     # nesting: same finer cell => same coarser cell
            for a_, b_ in PAIRS:
                if prev_cells[a_] == prev_cells[b_]: assert cells[a_] == cells[b_], "grids not nested"
        for pr in PAIRS:
            if pr not in first and cells[pr[0]] == cells[pr[1]]: first[pr] = m
        prev_cells = cells
        if len(first) == len(PAIRS): break
    assert len(first) == len(PAIRS)
    return xi, first

def complex_contrib(NG, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for j in (1, 2):
        Msum = 0.0; Ssum = np.zeros(n); Lsum = {pr: 0.0 for pr in PAIRS}; Dsum = {pr: 0.0 for pr in PAIRS}
        for g in range(NG):
            xi, first = grid_first_share(Z[j], rng)
            dint = {frozenset(pr): F(-first[pr]) for pr in PAIRS}      # d = -xi + log2 * (-a): affine image
            M, S, L, ray = hier_quantities(list(range(n)), dint); assert ray
            for pr in PAIRS:     # pathwise (3.5), exact in integer units
                a_, b_ = pr
                assert dint[frozenset(pr)] == M + L[frozenset(pr)] - S[a_] - S[b_]
            Msum += -xi + LOG2 * float(M)
            for x in range(n): Ssum[x] += LOG2 * float(S[x])
            for pr in PAIRS:
                Lsum[pr] += LOG2 * float(L[frozenset(pr)]); Dsum[pr] += -xi - LOG2 * first[pr]
        out[j] = (Msum/NG, Ssum/NG, {k: v/NG for k, v in Lsum.items()}, {k: v/NG for k, v in Dsum.items()})
    return out

if __name__ == '__main__':
    NG = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    cx = complex_contrib(NG, 1014)
    # sanity: E d_j(x,y) at the complex place = -log|z| + kappa
    errs = [cx[j][3][pr] - (-math.log(abs(diffs[j][pr])) + KAPPA) for j in (1, 2) for pr in PAIRS]
    print(f"complex place, {NG} grids/coordinate: E d - (-log|z| + kappa): mean {np.mean(errs):+.4f}, max|.| {np.max(np.abs(errs)):.4f}")
    for mode, cw in [('paper', 1.0), ('none', 1.0), ('milne_double', 1.0), ('paper', 0.5)]:
        fin = finite_contrib(mode)
        D = {}; Mtot = 0.0
        for pr in PAIRS:
            x, y = pr; val_ = 0.0
            for j in (1, 2):
                Mf, Sf, Lf, If = fin[j]; Mc, Sc, Lc, Dc = cx[j]
                val_ += (Lf[pr] + cw * Lc[pr]) - (Sf[x] + cw * Sc[x]) - (Sf[y] + cw * Sc[y])
            D[pr] = val_
        Mtot = sum(fin[j][0] + cw * cx[j][0] for j in (1, 2))
        Dv = np.array(list(D.values()))
        label = f"{mode}, complex sigma={cw}"
        print(f"[{label:32s}] D(x,y)=L*-S*(x)-S*(y) over 21 pairs: min {Dv.min():+.4f} max {Dv.max():+.4f} spread {Dv.max()-Dv.min():.4f};"
              f"  2*kappa*{cw} - <M1+M2> = {2*KAPPA*cw - Mtot:+.4f}")
