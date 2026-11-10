#!/usr/bin/env python3
"""Independent route for h(n) (Erdős #912): h(n) = #{floor(n/p) : p prime <= n}  (Heyman–Miraj).
No pi(sqrt n) split, no isolation lemma: the set from small primes and the set of hit k's are UNIONED.
A = {n//p : p prime <= L}, L = isqrt(n)  (numpy sieve)
B = {k <= n//(L+1) : gmpy2.next_prime(max(n//(k+1), L)) <= n//k}   (GMP primality)
"""
import sys, math, numpy as np, gmpy2

def primes_upto(L):
    s = np.ones(L + 1, dtype=bool); s[:2] = False
    for i in range(2, math.isqrt(L) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def h(n):
    L = math.isqrt(n)
    A = set(int(n // int(p)) for p in primes_upto(L))
    B = set()
    for k in range(1, n // (L + 1) + 1):
        lo = max(n // (k + 1), L)
        if int(gmpy2.next_prime(lo)) <= n // k:
            B.add(k)
    return len(A | B), len(A), len(B), len(A & B)

if __name__ == '__main__':
    for a in sys.argv[1:]:
        n = int(a)
        hv, a_, b_, ab = h(n)
        print(f"n={n} h={hv} |A|={a_} |B|={b_} |A&B|={ab}", flush=True)
