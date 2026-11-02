#!/usr/bin/env python3
"""Replicate Table 4 (the two sums in (4) for the Section 4.1 parameters) and Lambda(x)/(x log x),
plus the capacity condition sum_c f_{p,c} <= p-1 for every p in G."""
import sys, math
import numpy as np
from scipy.special import gammaln

def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0]

def iroot_gt(x, k, c):  # c^k > x  (exact integer test)
    return c ** k > x

for ex in [int(a) for a in sys.argv[1:]]:
    x = 10 ** ex
    P = math.isqrt(x // 2)
    while True:  # largest prime <= sqrt(x/2)
        if P > 1 and all(P % d for d in range(2, math.isqrt(P) + 1)): break
        P -= 1
    pr = sieve(P)
    I = np.array([c for c in sieve(int(round(x ** 0.25)) + 2) if c ** 5 > x and c ** 4 <= x], dtype=np.int64)
    # G: primes p with 2 x^{2/5} < p < P  <=> p^5 > 32 x^2
    G = np.array([p for p in pr if p < P and int(p) ** 5 > 32 * x * x], dtype=np.int64)
    Ymax = x // (int(G.min()) * int(I.min()))
    free = np.ones(Ymax + 1, dtype=bool); free[0] = False
    for c in I: free[c::c] = False
    cnt = np.cumsum(free)                      # cnt[Y] = # I-free integers in [1, Y]
    ksum = 0; logsum = 0.0; fsum = np.zeros(len(G), dtype=np.int64)
    for c in I:
        Y = x // (G * c)
        assert (Y < G).all(), "a padding would not be < p"
        pool = cnt[Y]
        f = pool // c; fsum += f
        N = c * f
        ksum += int(N.sum()); logsum += float(gammaln(N + 1).sum())
    cap = bool((fsum <= G - 1).all())
    # Lambda(x) = sum_{p < P'} log((p-1)!), P' largest prime with P'(P'+3) <= x
    y = (math.isqrt(4 * x + 9) - 3) // 2
    while y * (y + 3) > x: y -= 1
    pp = sieve(y + 5); Pp = int(pp[pp * (pp + 3) <= x].max())
    Lam = float(gammaln(pp[pp < Pp].astype(float)).sum())   # log((p-1)!) = gammaln(p)
    L = math.log(x)
    print(f"x=1e{ex}: |I|={len(I)} |G|={len(G)}  sum N/x={ksum/x:.4f}  sum log N!/(x log x)={logsum/(x*L):.4f}  "
          f"Lambda/(x log x)={Lam/(x*L):.4f}  capacity ok={cap}", flush=True)
print("paper Table 4: 1e8: 13 458 0.0141 0.0035 0.0239 | 1e10: 40 4741 0.0190 0.0050 0.0197 | "
      "1e12: 114 45247 0.0217 0.0060 0.0167 | 1e14: 332 417491 0.0244 0.0069 0.0145 | 1e16: 979 3807376 0.0263 0.0076 0.0128")
