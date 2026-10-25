#!/usr/bin/env python3
"""Prop 7.6 check (exact Fractions, no sympy): rows p(T_i)_alpha p(U_i)_beta, p(t) = (1,(1-t^2)/(1+t^2),2t/(1+t^2)).
(a) at the paper's grid {0,1,-1}^2 (ordered 0,1,-1 in both coordinates) det must be 64 = 2^6;
(b) at random rational (T_i,U_i) det != 0 (another witness that det D is a nonzero rational function);
(c) control: on the diagonal T_i = U_i det must be 0 (the ordinary circle equation is a kernel vector)."""
from fractions import Fraction as Fr
import random, itertools
def p(t): return (Fr(1), (1 - t*t)/(1 + t*t), 2*t/(1 + t*t))
def det(M):
    M = [r[:] for r in M]; n = len(M); s = Fr(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c: M[c], M[piv] = M[piv], M[c]; s = -s
        s *= M[c][c]
        for i in range(c+1, n):
            f = M[i][c]/M[c][c]; M[i] = [a - f*b for a, b in zip(M[i], M[c])]
    return s
def D(pairs): return [[p(T)[a]*p(U)[b] for a in range(3) for b in range(3)] for T, U in pairs]
grid = [(Fr(a), Fr(b)) for a in (0, 1, -1) for b in (0, 1, -1)]
print('grid det =', det(D(grid)))
random.seed(7)
for _ in range(3):
    pr = [(Fr(random.randint(-30, 30), random.randint(1, 30)), Fr(random.randint(-30, 30), random.randint(1, 30))) for _ in range(9)]
    print('random det != 0:', det(D(pr)) != 0)
pr = [(t, t) for t in (Fr(random.randint(-30, 30), random.randint(1, 30)) for _ in range(9))]
print('diagonal control det =', det(D(pr)))
