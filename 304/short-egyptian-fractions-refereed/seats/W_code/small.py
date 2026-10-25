# Cross-check OEIS A006585 (F(k)), A400352 (v(k)), A097849 (N(b)) on small cases. Exact arithmetic.
from fractions import Fraction as Fr
from math import gcd
import sys

def sols(num, den, k, lo):
    """yield increasing tuples (n1<...<nk), n1>lo, with sum 1/ni = num/den"""
    if k == 0:
        if num == 0: yield ()
        return
    if num <= 0: return
    if k == 1:
        if den % num == 0 and den // num > lo: yield (den // num,)
        return
    start = max(lo + 1, -(-den // num))      # 1/n <= num/den
    end = (k * den) // num                   # num/den <= k/n  (strict increase gives < but use <=)
    for n in range(start, end + 1):
        nn, nd = num * n - den, den * n
        if nn < 0: continue
        g = gcd(nn, nd) or 1
        for t in sols(nn // g, nd // g, k - 1, n):
            yield (n,) + t

Fk = {}; Dk = {}
for k in range(1, 7):
    S = list(sols(1, 1, k, 0)); Fk[k] = len(S)
    D = set(x for s in S for x in s); m = 2
    while m in D: m += 1
    Dk[k] = m
print("F(k) k=1..6:", [Fk[k] for k in range(1, 7)], "(A006585: 1,0,1,6,72,2320)")
print("v(k) k=1..6:", [Dk[k] for k in range(1, 7)], "(A400352 from k=3: 4,11,17,103)")

def minterms(a, b, cap=8):
    for k in range(1, cap + 1):
        g = gcd(a, b)
        for _ in sols(a // g, b // g, k, 1):   # denominators >= 2
            return k
    return None
Nb = []
for b in range(2, 41):
    Nb.append(max(minterms(a, b) for a in range(1, b)))
print("N(b) b=2..40:", Nb)
