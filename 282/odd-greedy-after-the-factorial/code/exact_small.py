"""Fully exact odd greedy (distinct odd denominators) with true big denominators (gmpy2).
Third instrument: no modular reasoning at all."""
import sys, math, gmpy2
from gmpy2 import mpz
def expand(a, b, cap=200):
    a, b = mpz(a), mpz(b); prev = mpz(1); nums = []
    while a:
        g = gmpy2.gcd(a, b); a //= g; b //= g
        nums.append(int(a))
        n = (b + a - 1) // a
        if n % 2 == 0: n += 1
        if n <= prev: n = prev + 2
        a, b = a*n - b, b*n; prev = n
        assert a >= 0
        if len(nums) > cap: return None
    return nums
if __name__ == "__main__":
    for N in range(3, int(sys.argv[1])+1):
        for mult in (1, 2):
            nums = expand(3, mult*math.factorial(N) - 1)
            print(N, mult, len(nums), ",".join(map(str, nums)))
