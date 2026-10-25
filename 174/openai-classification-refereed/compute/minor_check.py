#!/usr/bin/env python3
"""Second instrument for one-parameter configurations whose tensor matrix D (rows p_i(x) (x) p_i(y), 9 columns) has
rank 8 over Q(x,y), i.e. a 1-dim kernel.  Exact Fractions only (no sympy).  The kernel is spanned by the cofactor
vector c(x,y) (signed 8x8 minors).  Fix x = x0 rational, put y = x0 + h; each row times (1+y^2) is polynomial in h of
degree <= 2, so every minor is a polynomial in h of degree <= 16: recover it exactly by Lagrange interpolation at 17
rational h.  Let m be the least order at which some minor has a nonzero h^m coefficient; the vector of h^m
coefficients is the reduction of the saturated kernel generator (up to a unit), i.e. spans m_F(K) at tau = x0.
Criterion holds at x0 iff its spatial 2x2 block is a NONZERO multiple of I.  Exact for generic x0 (we use 3 values).
Rows that are scaled by a nonzero function of x0 alone do not change the span."""
from fractions import Fraction as Fr
import sys, itertools
Q0 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def point(lab, t):
    s, j = divmod(lab, 4); a, b = Q0[j]
    if s == 2: return (Fr(a), Fr(b))
    u = (1 - t*t)/(1 + t*t); v = 2*t/(1 + t*t)
    return (u*a - v*b, v*a + u*b) if s == 0 else (u*a + v*b, -v*a + u*b)
def det(M):
    M = [r[:] for r in M]; n = len(M); s = Fr(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c: M[c], M[piv] = M[piv], M[c]; s = -s
        s *= M[c][c]
        for i in range(c+1, n):
            f = M[i][c]/M[c][c]
            if f: M[i] = [a - f*b for a, b in zip(M[i], M[c])]
    return s
def rows(labels, x0, y0):
    out = []
    for lab in labels:
        pl = (Fr(1),) + point(lab, x0); pr = (Fr(1),) + point(lab, y0)
        out.append([pl[a]*pr[b]*(1 + y0*y0) for a in range(3) for b in range(3)])
    return out
def cofactors(M):   # M: 8 x 9 -> signed minors c_k with sum_k M[i][k] c_k = 0
    return [(-1)**k * det([r[:k] + r[k+1:] for r in M]) for k in range(9)]
def interp_coeffs(xs, ys):   # exact polynomial coefficients from samples (Newton -> monomial)
    n = len(xs); coef = list(ys)
    for j in range(1, n):
        for i in range(n-1, j-1, -1): coef[i] = (coef[i] - coef[i-1])/(xs[i] - xs[i-j])
    poly = [Fr(0)]*n
    for i in range(n-1, -1, -1):           # Horner on Newton form
        poly = [Fr(0)] + poly[:-1]          # multiply by h
        poly = [poly[k] - xs[i]*(poly[k+1] if k+1 < n else 0) if False else poly[k] for k in range(n)]
    # simpler: rebuild via Vandermonde solve
    V = [[x**k for k in range(n)] for x in xs]
    A = [V[i] + [ys[i]] for i in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if A[i][c] != 0); A[c], A[piv] = A[piv], A[c]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]/A[c][c]; A[i] = [a - f*b for a, b in zip(A[i], A[c])]
    return [A[i][n]/A[i][i] for i in range(n)]
def limit_vector(labels, x0, deg=17):
    hs = [Fr(k, 97) for k in range(1, deg+2)]
    samples = [cofactors(rows(labels, x0, x0 + h)) for h in hs]
    polys = [interp_coeffs(hs, [s[k] for s in samples]) for k in range(9)]
    for m in range(deg+1):
        vec = [polys[k][m] for k in range(9)]
        if any(vec): return m, vec
    return None, None
def verdict(labels, name):
    out = []
    for x0 in (Fr(2, 7), Fr(-5, 3), Fr(11, 13)):
        M = rows(labels, x0, x0 + Fr(1, 3))
        m, L = limit_vector(labels, x0)
        if L is None: out.append('ZERO-COFACTORS(rank<8?)'); continue
        a11, a12, a21, a22 = L[4], L[5], L[7], L[8]
        ok = a12 == 0 and a21 == 0 and a11 == a22 and a11 != 0
        out.append(f"m={m} spatial=[[{a11},{a12}],[{a21},{a22}]] -> {'HOLDS' if ok else 'FAILS'}")
    print(name); [print('   ', o) for o in out]
if __name__ == '__main__':
    verdict((0, 1, 2, 4, 5, 6, 9, 11), 'census k=8 failing set (0,1,2,4,5,6,9,11)')
    verdict((0, 1, 2, 3, 8, 9, 10, 11), 'two squares R+Q0 u Q0 (transitive control, expect HOLDS)')
    verdict((0, 1, 2, 3, 4, 5, 6, 8), 'census k=8 first orbit (0,1,2,3,4,5,6,8) (expect HOLDS per census)')
