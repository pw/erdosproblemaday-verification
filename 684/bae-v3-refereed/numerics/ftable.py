# Independent f(n) for small n: brute force from the integer C(n,k) itself (trial division),
# a different route from the Kummer/Legendre carry formula and from Lean's Nat.factorization.
import sys
from math import comb
def small_part(m, k):
    u, p = 1, 2
    while p <= k:
        while m % p == 0:
            m //= p; u *= p
        p += 1          # trial division by every integer ≤ k: composites never divide what's left
    return u
def f(n):
    for k in range(1, n + 1):
        if small_part(comb(n, k), k) > n * n:
            return k
    return None
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
print([(n, f(n)) for n in range(N + 1)])
