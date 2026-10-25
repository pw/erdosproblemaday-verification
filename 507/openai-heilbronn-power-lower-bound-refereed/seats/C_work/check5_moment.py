#!/usr/bin/env python3
"""Check 5: Lemma 7.3 (eq. 7.4): for R >= h,
     sum_{x primitive, R <= |x| < 2R} g(x)^3  <<  R^3 I,
g(x) = positive generator of x . Lambda_C = gcd(entries of C~ x, h), I = [Z^3 : Lambda_C] = DE.
Exact computation for h = B^k in {4,8,16,32, 3,9,27, 5,25}, random C with a unit entry plus a representative
P diag(1,B^b,B^e) Q of every class (b <= e <= k), R in {h, 2h}.  I from determinantal divisors (independent).
Also checked pointwise: g(x) | E (eq. 7.2), and 'B^j | g(x) iff C x == 0 mod B^j', and the residue-class
density B^(-j-max(j-b,0)) for j <= e (exact over Z/B^j).
Mutations (must be REJECTED): (i) drop the hypothesis R >= h (take R = 1,2,4 < h): ratio blows up;
(ii) drop the factor I (claim sum << R^3): ratio grows like I across classes.
"""
import itertools, math, random, time
import numpy as np

# --- local instruments (written independently of check2_orbits.py, per the brief) ---
def det3(M):
    M = np.asarray(M, dtype=np.int64)
    return int(M[0, 0] * (M[1, 1] * M[2, 2] - M[1, 2] * M[2, 1]) - M[0, 1] * (M[1, 0] * M[2, 2] - M[1, 2] * M[2, 0])
               + M[0, 2] * (M[1, 0] * M[2, 1] - M[1, 1] * M[2, 0]))

def random_gl(h, rng):
    while True:
        M = np.array([[rng.randrange(h) for _ in range(3)] for _ in range(3)], dtype=np.int64)
        if math.gcd(det3(M) % h, h) == 1: return M

_SPAN_X = {}
def local_DE(C, h):
    """I = [Z^3 : Lambda_C] = h^3 / |{x.C mod h}| by enumeration; D = gcd(2x2 minors, h) (the lemma's own
    characterisation of b); E = I / D."""
    if h not in _SPAN_X:
        ax = np.arange(h, dtype=np.int64)
        _SPAN_X[h] = np.array(np.meshgrid(ax, ax, ax, indexing='ij')).reshape(3, -1).T
    X = _SPAN_X[h]
    rows = (X @ C) % h
    span = len(np.unique(rows[:, 0] * h * h + rows[:, 1] * h + rows[:, 2]))
    I = h ** 3 // span
    D = h
    for (i1, i2) in ((0, 1), (0, 2), (1, 2)):
        for (j1, j2) in ((0, 1), (0, 2), (1, 2)):
            D = math.gcd(D, int(C[i1, j1] * C[i2, j2] - C[i1, j2] * C[i2, j1]))
    assert I % D == 0
    return D, I // D

def det_divisors(Ms, h):
    """compatibility wrapper returning arrays (D, E, unit) using local_DE"""
    Ds, Es = zip(*[local_DE(np.asarray(C, dtype=np.int64), h) for C in Ms])
    return np.array(Ds), np.array(Es), None

def shell(R):
    m = 2 * R
    ax = np.arange(-m, m + 1, dtype=np.int64)
    X = np.array(np.meshgrid(ax, ax, ax, indexing='ij')).reshape(3, -1).T
    n2 = (X * X).sum(axis=1)
    X = X[(n2 >= R * R) & (n2 < 4 * R * R)]
    g = np.gcd(np.gcd(X[:, 0], X[:, 1]), X[:, 2])
    return X[g == 1]

def random_unit_entry(h, rng):
    while True:
        C = np.array([[rng.randrange(h) for _ in range(3)] for _ in range(3)], dtype=np.int64)
        if any(math.gcd(int(x), h) == 1 for x in C.ravel()): return C

def class_reps(h, B, k, rng):
    out = []
    for b in range(k + 1):
        for e in range(b, k + 1):
            P = random_gl(h, rng); Q = random_gl(h, rng)
            Dg = np.diag([1, B ** b % h, B ** e % h]).astype(np.int64)
            out.append(((P @ Dg @ Q) % h, (b, e)))
    return out

def gvals(C, X, h):
    Y = X @ C.T          # rows: C x
    return np.gcd(np.gcd(np.gcd(Y[:, 0], Y[:, 1]), Y[:, 2]), h)

def density_check(C, h, B, k, b, e):
    bad = 0
    for j in range(1, e + 1):
        if j > k: break
        mod = B ** j
        ax = np.arange(mod, dtype=np.int64)
        X = np.array(np.meshgrid(ax, ax, ax, indexing='ij')).reshape(3, -1).T
        Y = (X @ C.T) % mod
        frac = (Y == 0).all(axis=1).mean()
        want = B ** (-j - max(j - b, 0))
        if abs(frac - want) > 1e-12: bad += 1
    return bad

def main():
    rng = random.Random(7377)
    t0 = time.time()
    shells = {}
    worst_overall = 0.0
    mutI = []   # (I, max sum/R^3)
    for B, k in ((2, 2), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 3), (5, 1), (5, 2)):
        h = B ** k
        mats = [(random_unit_entry(h, rng), None) for _ in range(6)] + class_reps(h, B, k, rng)
        Ms = np.array([m for m, _ in mats])
        Dv, Ev, unit = det_divisors(Ms, h)
        worst = 0.0; pw_bad = 0; dens_bad = 0
        for R in (h, 2 * h):
            if R not in shells: shells[R] = shell(R)
            X = shells[R]
            for t, (C, be) in enumerate(mats):
                D_, E_ = int(Dv[t]), int(Ev[t]); I = D_ * E_
                g = gvals(C, X, h)
                if (E_ % g != 0).any(): pw_bad += 1
                # B^j | g iff Cx == 0 mod B^j
                for j in range(1, k + 1):
                    Y = (X @ C.T) % (B ** j)
                    if ((g % B ** j == 0) != (Y == 0).all(axis=1)).any(): pw_bad += 1
                s = float((g.astype(np.float64) ** 3).sum())
                ratio = s / (R ** 3 * I)
                worst = max(worst, ratio)
                mutI.append((I, s / R ** 3, h, R))
                if R == h:
                    b = round(math.log(D_, B)); e = round(math.log(E_, B))
                    if h <= 32: dens_bad += density_check(C, h, B, k, b, e)
        worst_overall = max(worst_overall, worst)
        print(f"h={h} (B={B},k={k}): {len(mats)} matrices x R in {{h,2h}}: max sum g^3/(R^3 I) = {worst:.3f}; "
              f"pointwise failures (g|E, B^j|g <=> Cx=0 mod B^j): {pw_bad}; density-formula failures: {dens_bad}  "
              f"[{time.time()-t0:.0f}s]", flush=True)
    print(f"\nPOSITIVE: overall max ratio sum g^3/(R^3 I) over all h, C, R>=h: {worst_overall:.3f} "
          f"(bounded; for comparison #primitive x in shell / R^3 ~ {len(shells[16])/16**3:.2f} at R=16)")
    # mutation (ii): drop I
    byI = {}
    for I, v, h, R in mutI:
        byI[I] = max(byI.get(I, 0), v)
    print("MUTATION drop I (claim sum << R^3): max sum/R^3 by I:", {I: round(v, 1) for I, v in sorted(byI.items())})
    # mutation (i): R < h
    h, B, k = 32, 2, 5
    C, _ = class_reps(h, B, k, rng)[-1]   # b = e = k : C == rank one mod 2
    Dv, Ev, _ = det_divisors(C[None], h); I = int(Dv[0] * Ev[0])
    for R in (1, 2, 4, 8, 16, 32):
        X = shell(R); g = gvals(C, X, h)
        print(f"MUTATION R<h: h=32, C in class b=e=k (I={I}), R={R}: sum g^3/(R^3 I) = {float((g.astype(np.float64)**3).sum())/(R**3*I):.3f}")
    for (b, e) in ((0, 5), (2, 5), (5, 5)):
        P = random_gl(h, rng); Q = random_gl(h, rng)
        C = (P @ np.diag([1, B ** b % h, B ** e % h]) @ Q) % h
        Dv, Ev, _ = det_divisors(C[None], h); I = int(Dv[0] * Ev[0])
        vals = []
        for R in (1, 2, 4, 32):
            X = shell(R); g = gvals(C, X, h)
            vals.append(round(float((g.astype(np.float64)**3).sum())/(R**3*I), 2))
        print(f"MUTATION R<h: h=32, class (b,e)=({b},{e}) I={I}: ratio at R=1,2,4,32: {vals}")

if __name__ == "__main__":
    main()
