# exact-integer check of sqrt2 r B^beta < a_r <= 2^15 sqrt3 r B^beta (divide by r), squared:
# 2 B^(2beta) < N^3/tau <= 2^30*3 B^(2beta), with 2beta = 3029k+1 integer.
import random
from fractions import Fraction
random.seed(3)
bad = 0; n = 0
for kk in [2, 3, 4]:
    for _ in range(60):
        B = random.choice([3, 5, 7, 11, 101, 1009, 10007])
        h = B**kk
        H100 = h**100
        for q in [H100 + 1, 2*H100, H100 + random.randrange(1, H100)]:
            N = (h*q)**10
            tau = B**(kk-1) // 2
            lhs = 2 * B**(3029*kk+1)
            rhs = 2**30 * 3 * B**(3029*kk+1)
            val = Fraction(N**3, tau)
            n += 1
            if not (lhs < val <= rhs): bad += 1
        # tau >= B^(k-1)/3 and h/tau <= 3B
        assert 3*tau >= B**(kk-1) and h <= 3*B*tau
print("a_r/r two-sided bound checks:", n, "failures:", bad)
