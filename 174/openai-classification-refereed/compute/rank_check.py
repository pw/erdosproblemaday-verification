#!/usr/bin/env python3
"""Second instrument (no sympy): exact Fraction arithmetic. Specialise (tau_left, tau_right) = (x0, y0) rational with
1 + x0^2, 1 + y0^2 != 0, build the 12 x 9 matrix with rows p(x0)_alpha * p(y0)_beta for the three-squares set, and
compute its rank by fraction-exact Gaussian elimination. Rank 9 at ONE rational point proves rank 9 over Q(x,y)
(a nonzero 9x9 minor is a nonzero rational function). Controls: two squares (8 rows) must give rank <= 8 everywhere;
the diagonal x0 = y0 must give rank < 9 for the three squares (the ordinary sphere matrix is in the kernel there)."""
from fractions import Fraction as Fr
import random, itertools
def rot(t):
    u = (1 - t*t) / (1 + t*t); v = 2*t / (1 + t*t); return u, v
Q0 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
def pts(t, which):
    u, v = rot(t); out = []
    if 'p' in which: out += [(u*a - v*b, v*a + u*b) for a, b in Q0]
    if 'm' in which: out += [(u*a + v*b, -v*a + u*b) for a, b in Q0]
    if '0' in which: out += [(Fr(a), Fr(b)) for a, b in Q0]
    return out
def rank(M):
    M = [r[:] for r in M]; rk = 0; ncol = len(M[0])
    for c in range(ncol):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def mat(x0, y0, which):
    L, R = pts(x0, which), pts(y0, which)
    out = []
    for l, r in zip(L, R):
        pl = (Fr(1),) + tuple(l); pr = (Fr(1),) + tuple(r)
        out.append([pl[al] * pr[be] for al in range(3) for be in range(3)])
    return out
random.seed(20261021)
for trial in range(5):
    x0 = Fr(random.randint(-50, 50), random.randint(1, 50)); y0 = Fr(random.randint(-50, 50), random.randint(1, 50))
    if x0 == y0: continue
    print(f"x0={x0} y0={y0}: three squares rank {rank(mat(x0, y0, 'pm0'))}/9 ; two squares rank {rank(mat(x0, y0, 'p0'))} ; diagonal (x0,x0) three squares rank {rank(mat(x0, x0, 'pm0'))}")
# which 9-row subsets are already full rank at a random point (each such subset = a 9-point non-Ramsey set, by Thm 1.1)
x0, y0 = Fr(3, 7), Fr(-11, 5)
M = mat(x0, y0, 'pm0'); full9 = sum(1 for S in itertools.combinations(range(12), 9) if rank([M[i] for i in S]) == 9)
print('9-point subsets of the 12 with full rank 9 at (3/7,-11/5):', full9, 'of', 220)
