import math
from fractions import Fraction as Fr
def b(r, eps): return Fr(2)**(r*(r-2)) * (1/eps)**(r-2)
ok = True
for r in range(3, 25):
    for eps in [Fr(1,2), Fr(1,3), Fr(1,1000), Fr(1, 10**9)]:
        if (8/eps) * b(r-1, eps/4) != b(r, eps): ok = False; print('recursion fail', r, eps)
        if b(r, eps) < 2: ok = False
for r in range(2, 200):
    A = 4 + 8*(r-2) + (1 + r*(r-2))*math.log(2)
    if not (A + 3 <= r*r + 6*r - 8 <= 4*r*r): ok = False; print('Ar fail', r)
    for x in [1, 1.0001, 1.5, 2, 5, 10, 50, 700]:
        # log(1 + k b_r(e^{-8x})) in log space: log(k b) = 4x + r(r-2)log2 + 8x(r-2)
        lkb = 4*x + r*(r-2)*math.log(2) + 8*x*(r-2)
        lhs = lkb + math.log1p(math.exp(-lkb))
        if lhs > A*x + 1e-12: ok = False; print('log bound fail', r, x, lhs, A*x)
print('constants OK:', ok)
