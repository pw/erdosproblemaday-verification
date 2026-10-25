# Lemma 7.2 / 7.3 numerical checks.
import random, math, itertools
import numpy as np
from math import gcd

def hnf_rows(gens):
    """Row-style HNF basis (list of 3 int rows) of the Z-span of gens (full rank in Z^3)."""
    A = [list(r) for r in gens]
    basis = []
    for c in range(3):
        rows = [r for r in A if any(r[j] != 0 for j in range(c, 3))]
        # gcd-reduce column c among rows
        while True:
            nz = [r for r in rows if r[c] != 0]
            if len(nz) <= 1: break
            nz.sort(key=lambda r: abs(r[c]))
            p = nz[0]
            for r in nz[1:]:
                f = r[c] // p[c]
                for j in range(3): r[j] -= f * p[j]
        nz = [r for r in rows if r[c] != 0]
        assert len(nz) == 1, "not full rank"
        p = nz[0]
        if p[c] < 0: p[:] = [-v for v in p]
        basis.append(p[:])
        A = [r for r in rows if r is not p]
    return basis

def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

def val(n, B, cap):
    if n == 0: return cap
    v = 0
    while n % B == 0 and v < cap: n //= B; v += 1
    return v

def random_C(B, k, b=None, e=None, rng=random):
    h = B**k
    if b is None:
        while True:
            C = [[rng.randrange(h) for _ in range(3)] for _ in range(3)]
            if any(C[i][j] % B for i in range(3) for j in range(3)): return C
    # C = P diag(1,B^b,B^e) Q with random invertible P,Q mod h
    def rand_inv():
        while True:
            M = [[rng.randrange(h) for _ in range(3)] for _ in range(3)]
            if det3(M) % B: return M
    P, Q = rand_inv(), rand_inv()
    Dg = [1, B**b % h, B**e % h]
    return [[sum(P[i][l]*Dg[l]*Q[l][j] for l in range(3)) % h for j in range(3)] for i in range(3)]

def analyse(C, B, k):
    h = B**k
    minors = [C[i1][j1]*C[i2][j2]-C[i1][j2]*C[i2][j1] for i1, i2 in itertools.combinations(range(3), 2) for j1, j2 in itertools.combinations(range(3), 2)]
    b = min(val(m % h, B, k) for m in minors)
    gens = [list(C[i]) for i in range(3)] + [[h if j == i else 0 for j in range(3)] for i in range(3)]
    basis = hnf_rows(gens)
    I = abs(det3(basis))
    t = val(I, B, 10**9); assert B**t == I
    e = t - b
    return b, e, I, basis

rng = random.Random(7)
print("== Lemma 7.3 equivalence, density, moment ==")
configs = []
for B, k in [(2, 3), (3, 2), (2, 4), (5, 2)]:
    for _ in range(4): configs.append((B, k, None, None))
    for b in range(k+1):
        for e in range(b, k+1): configs.append((B, k, b, e))
worst_ratio = 0; equiv_fail = 0; dens_fail = 0; gdivE_fail = 0; ncases = 0
for B, k, b0, e0 in configs:
    h = B**k
    C = random_C(B, k, b0, e0, rng)
    if not any(C[i][j] % B for i in range(3) for j in range(3)): continue
    b, e, I, basis = analyse(C, B, k)
    assert 0 <= b <= e <= k, (b, e)
    if b0 is not None: assert (b, e) == (b0, e0), (b, e, b0, e0)
    E = B**e
    ncases += 1
    # density of Cx = 0 mod B^j for j<=e (exact count over residues)
    for j in range(0, e+1):
        Mj = B**j
        cnt = sum(1 for x in itertools.product(range(Mj), repeat=3)
                  if all(sum(C[i][l]*x[l] for l in range(3)) % Mj == 0 for i in range(3)))
        pred = Mj**3 * B**(-j - max(j-b, 0))
        if abs(cnt - pred) > 1e-9: dens_fail += 1
    # vectorised g(x) over a box, check equivalence and g | E, and moment ratios
    for R in [h, 2*h, 3*h]:
        L = 2*R
        if (2*L+1)**3 > 9_000_000: continue
        ax = np.arange(-L, L+1, dtype=np.int64)
        X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
        X, Y, Z = X.ravel(), Y.ravel(), Z.ravel()
        n2 = X*X + Y*Y + Z*Z
        g = np.zeros_like(X)
        for row in basis:
            g = np.gcd(g, row[0]*X + row[1]*Y + row[2]*Z)
        prim = np.gcd(np.gcd(np.abs(X), np.abs(Y)), np.abs(Z)) == 1
        sel = prim & (n2 >= R*R) & (n2 < 4*R*R)
        mom = float(np.sum(g[sel].astype(np.float64)**3))
        ratio = mom / (R**3 * I)
        worst_ratio = max(worst_ratio, ratio)
        if R == h:
            nzero = (n2 > 0) & prim
            if np.any((E % g[nzero]) != 0): gdivE_fail += 1
            Cx = [C[i][0]*X + C[i][1]*Y + C[i][2]*Z for i in range(3)]
            for j in range(0, k+1):
                lhs = (g % (B**j)) == 0
                rhs = (Cx[0] % B**j == 0) & (Cx[1] % B**j == 0) & (Cx[2] % B**j == 0)
                if np.any(lhs != rhs): equiv_fail += 1
        print(f"B={B} k={k} (b,e)=({b},{e}) I={I} R={R}: sum_g^3/(R^3 I) = {ratio:.3f}")
print(f"cases={ncases} density mismatches={dens_fail} equivalence mismatches={equiv_fail} g|E failures={gdivE_fail} worst ratio={worst_ratio:.3f}")
