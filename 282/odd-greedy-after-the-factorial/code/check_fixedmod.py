"""Independent second instrument for the odd greedy expansion of x = a/b (x < 1/3, so the
distinct-denominator rule never binds: first n >= 5).  Different strategy from og.c:
ONE fixed modulus M0 = (2*lcm(1..H))**(2*K+2), carried forward and divided down by a_j*g_j
each step (no replay).  If a numerator ever exceeds H/2, or K steps pass, it reports CANNOT
DECIDE (exit 2) instead of guessing.  Every divisibility it relies on is asserted."""
import sys, gmpy2
from gmpy2 import mpz
from math import gcd

def lcm_upto(H):
    L = mpz(1)
    for p in range(2, H+1):
        if gmpy2.is_prime(p):
            q = p
            while q*p <= H: q *= p
            L *= q
    return L

def expand(a, b, H, K):
    assert 0 < 3*a < b and b % 2 == 1 and gcd(a, b) == 1
    L2 = 2*lcm_upto(H)
    M = L2 ** (2*K+2)
    bm = mpz(b) % M
    nums = [a]
    for k in range(K):
        if a == 1:
            return nums                      # final term 1/b_k
        assert 2*a <= H, "numerator exceeds H/2: CANNOT DECIDE"
        assert M % (2*a) == 0
        r = (-bm) % a
        assert r != 0
        q_par = ((bm + r) % (2*a)) // a      # q mod 2
        s = r if q_par == 1 else r + a
        assert M % (a*s) == 0
        t = (bm + s) % M
        assert t % a == 0
        n = t // a; M //= a                  # n_k mod M/a
        bm = (bm % M) * (n % M) % M          # b_k n_k mod M/a
        g = gcd(s, int(bm % s))
        assert bm % g == 0 and M % g == 0
        bm //= g; M //= g
        a = s // g
        nums.append(a)
    raise SystemExit(2)

if __name__ == "__main__":
    import math
    mode = sys.argv[1]
    if mode == "fact":
        N, mult, H, K = map(int, sys.argv[2:6])
        b = mult*math.factorial(N) - 1
        nums = expand(3, b, H, K)
    else:
        a, b, H, K = map(int, sys.argv[2:6]); nums = expand(a, b, H, K)
    print(f"length={len(nums)} maxnum={max(nums)}")
    print(",".join(map(str, nums)))
