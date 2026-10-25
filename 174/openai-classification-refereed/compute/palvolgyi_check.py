#!/usr/bin/env python3
"""Recompute Palvolgyi's identities (2) and (3) (arXiv 2609.23327 v1, proof of Theorem 1) symbolically.
Points: (0,0) weight 2; (j, +-y_j), y_j^2 = j(2r-j), weights -2, 2, -1 for j = 1, 3, 4. D(r) = 1 => D(p) = (0, j/y_j)."""
import sympy as sp
r = sp.symbols('r', positive=True)
pts = [(sp.Integer(0), sp.Integer(0), sp.Integer(2), (0, 0))]
for j, w in ((1, -2), (3, 2), (4, -1)):
    y = sp.sqrt(j*(2*r - j))
    for sgn in (1, -1):
        pts.append((sp.Integer(j), sgn*y, sp.Integer(w), (0, sp.Integer(j)/(sgn*y))))
P = [sp.Matrix([1, x, y]) for x, y, w, d in pts]; W = [w for *_, w, d in pts]; Dp = [sp.Matrix([0, d[0], d[1]]) for *_, d in pts]
on_circle = all(sp.simplify((x - r)**2 + y**2 - r**2) == 0 for x, y, w, d in pts)
M0 = sp.simplify(sum((W[i]*P[i]*P[i].T for i in range(7)), sp.zeros(3)))
M1 = sp.simplify(sum((W[i]*Dp[i]*P[i].T for i in range(7)), sp.zeros(3)))
E = sp.simplify(sum(W[i]*(Dp[i].T*Dp[i])[0] for i in range(7)))
R = (2*r - 1)*(2*r - 3)*(2*r - 4)
print('on circle (x-r)^2+y^2=r^2:', on_circle)
print('sum w p p^T == 0:', M0 == sp.zeros(3))
print('sum w D(p) p^T == 0:', M1 == sp.zeros(3))
print('sum w |D(p)|^2 =', E, '; times R =', sp.simplify(E*R), '(paper: -24)')
