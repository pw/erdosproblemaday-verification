# u_r(n) = #{exponents attained by exactly r primes} at n = 10^8, 10^9 — compare with the Cramér limit
# c_r = (sqrt2/2) Gamma(r-1/2)/r! and Owmire's sqrt(2pi)(-1)^{r+1} C(2-sqrt2, r); show the pi(sqrt n) share of u_1.
import math, numpy as np
from math import gamma, sqrt, pi
def binom(a, r):
    out = 1.0
    for j in range(r): out *= (a - j) / (j + 1)
    return out
for e in (8, 9):
    n = 10**e; s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, math.isqrt(n) + 1):
        if s[i]: s[i*i::i] = False
    P = np.nonzero(s)[0]; del s
    k = n // P
    c = np.bincount(k)            # multiplicity of each floor value (== exponent multiplicity, by the isolation lemma)
    ur = np.bincount(c[c > 0])
    sc = sqrt(n / math.log(n)); pis = int((P <= math.isqrt(n)).sum())
    print(f"n=1e{e} scale={sc:.1f} h={int((c>0).sum())} pi(sqrt n)/scale={pis/sc:.4f}  (2/sqrt(log n)={2/sqrt(math.log(n)):.4f})")
    for r in range(1, 6):
        cr = sqrt(2)/2*gamma(r-0.5)/math.factorial(r); co = sqrt(2*pi)*(-1)**(r+1)*binom(2-sqrt(2), r)
        extra = f"  (u_1 - pi(sqrt n))/scale={(ur[1]-pis)/sc:.4f}" if r == 1 else ""
        print(f"  r={r}: u_r/scale={ur[r]/sc:.4f}   Cramér limit {cr:.4f}   Owmire {co:.4f}{extra}")
    del P, k, c
