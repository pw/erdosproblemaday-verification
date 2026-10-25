# Least preimage ell(d) = min{n : phi(n) = d} by the classical divisor recursion (route C, independent of both sieves):
# every preimage is a product of prime powers p^k with (p-1)p^(k-1) | d; recurse over primes p with p-1 | d in DECREASING order.
from sympy import divisors, isprime
from functools import lru_cache
def ell(d):
    if d == 1: return 1
    ps = sorted([q+1 for q in divisors(d) if isprime(q+1)], reverse=True)
    best = [None]
    def rec(rem, idx, n):
        if rem == 1:
            if best[0] is None or n < best[0]: best[0] = n
            return
        for i in range(idx, len(ps)):
            p = ps[i]
            if rem % (p-1): continue
            r = rem // (p-1); pk = p
            while True:
                rec(r, i+1, n*pk)
                if r % p: break
                r //= p; pk *= p
    rec(d, 0, 1)
    # n odd preimage m has phi(2m)=phi(m): the recursion includes p=2 (p-1=1 divides everything), so 2*m is covered.
    return best[0]
if __name__ == '__main__':
    import sys
    for d in [2, 8, 128, 5888, 2037248, 2**18*257]:
        print(d, ell(d), ell(d)/d)
