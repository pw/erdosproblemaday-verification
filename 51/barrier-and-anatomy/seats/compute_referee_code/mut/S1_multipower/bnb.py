#!/usr/bin/env python3
"""Second instrument: exact least preimage of phi for a given a (factorization known), by depth-first search over prime
powers q^f with q^(f-1)(q-1) | a, primes in DECREASING order, exact integers, branch-and-bound
(prune when n*(rem+1) >= best: any preimage of rem > 1 exceeds rem). Independent of smoothdp.py (no lattice, no floats,
no group/0-1 knapsack split). Primality: sympy.isprime (BPSW never rejects a prime).
Returns (ell, list of (q,f))."""
import sys
from sympy import isprime, divisors, factorint
from math import prod
def ell(a, fac=None):
    if a == 1: return 1, []
    if fac is None: fac = factorint(a)
    divs = divisors(a) if a < 10**12 else _divs(fac)
    cand = sorted((d+1 for d in divs if (d % 2 == 0 or d == 1) and isprime(d+1)), reverse=True)
    best = [None, None]
    def rec(rem, idx, n, used):
        if rem == 1:
            if best[0] is None or n < best[0]: best[0] = n; best[1] = list(used)
            return
        if best[0] is not None and n*(rem+1) >= best[0]: return
        for i in range(idx, len(cand)):
            q = cand[i]
            if rem % (q-1): continue
            r = rem // (q-1); qf = q; f = 1
            while True:
                if q == 2 and f == 1:
                    pass  # phi(2)=1: 2*m never least; skip but allow higher powers
                else:
                    used.append((q, f)); rec(r, i+1, n*qf, used); used.pop()
                if r % q: break
                r //= q; qf *= q; f += 1
    rec(a, 0, 1, [])
    return best[0], best[1]
def _divs(fac):
    ds = [1]
    for p, e in fac.items():
        ds = [d * p**k for d in ds for k in range(e+1)]
    return ds
if __name__ == '__main__':
    for a in [2, 8, 128, 5888, 2037248, 387383296, 4212, 116964]:
        n, cov = ell(a); print(a, n, n/a, cov)
