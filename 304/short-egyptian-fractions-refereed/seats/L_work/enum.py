from fractions import Fraction as Fr
import sys
from math import ceil
def expansions(rem, k, lo):
    # all strictly increasing tuples (n1<...<nk), n1>=lo, sum 1/ni = rem
    if k == 0:
        if rem == 0: yield ()
        return
    if rem <= 0: return
    if k == 1:
        if rem.numerator == 1 and rem.denominator >= lo: yield (rem.denominator,)
        return
    # 1/n1 < rem  unless... n1 >= ceil(1/rem); and k/n1 > rem strictly (distinct, decreasing) => n1 < k/rem
    start = max(lo, ceil(1/rem))
    n = start
    while Fr(k, n) > rem:   # need 1/n + ... (k terms, decreasing strictly) >= rem; upper bound k/n
        for t in expansions(rem - Fr(1,n), k-1, n+1):
            yield (n,)+t
        n += 1
for k in range(1, 7):
    sols = list(expansions(Fr(1), k, 1))
    F = len(sols)
    ok1 = all(s[i] <= k**(2**i) for s in sols for i in range(k))
    D = set(x for s in sols for x in s if x >= 2)
    v = 2
    while v in D: v += 1
    print(k, "F=",F, "F<=k^(2^k-1):", F <= k**(2**k-1), "ni<=k^(2^i):", ok1, "v=",v, "v<=1+k^(2^(k-1)):", v <= 1+k**(2**(k-1)), "max den", max((max(s) for s in sols), default=None))
