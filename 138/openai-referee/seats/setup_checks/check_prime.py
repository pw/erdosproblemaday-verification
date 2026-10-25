# Lemma setup:prime (02-setup.tex l.54-82), checked exactly with integers.
# Claim A (l.64-69): v_l(C(2n,n)) = sum_a (floor(2n/l^a) - 2 floor(n/l^a)) <= floor(log_l(2n)).
# Claim B (l.72-75): C(2n,n) >= 4^n/(2n+1).
# Claim C (l.77-79): with n=k^2, k^2 log4 - log(2k^2+1) > k log(2k^2) "for all sufficiently large k";
#   checked EXACTLY as the integer inequality 4^(k^2) > (2k^2+1)*(2k^2)^k, and the first k where it holds.
# Claim D: hence C(2k^2,k^2) has a prime factor P with k < P <= 2k^2 (checked by direct factor search, small k).
# CONTROL (must FAIL): same comparison with n = k instead of n = k^2: 4^k > (2k+1)(2k)^k is false for every k>=1.
import math, sys
from sympy import primerange, factorint

def vl_binom(n, l):           # exact valuation via Legendre
    def vf(x):
        s, p = 0, l
        while p <= x:
            s += x // p; p *= l
        return s
    return vf(2*n) - 2*vf(n)

def floor_log(l, x):          # largest a with l^a <= x
    a, p = 0, l
    while p <= x:
        a += 1; p *= l
    return a

# Claim A, all n <= 300, all primes l <= 2n
bad = 0
for n in range(1, 301):
    for l in primerange(2, 2*n+1):
        v = vl_binom(n, l)
        s = sum((2*n)//l**a - 2*(n//l**a) for a in range(1, floor_log(l, 2*n)+3))
        if v != s or v > floor_log(l, 2*n): bad += 1
print("Claim A (Kummer/Legendre bound), n<=300, all primes l<=2n: violations =", bad)

# Claim B
badB = sum(1 for n in range(1, 401) if math.comb(2*n, n)*(2*n+1) < 4**n)
print("Claim B (C(2n,n)(2n+1) >= 4^n), n<=400: violations =", badB)

# Claim C exact
first = None; fails = []
for k in range(1, 401):
    n = k*k
    holds = 4**n > (2*n+1)*(2*n)**k
    if not holds: fails.append(k)
print("Claim C exact 4^(k^2) > (2k^2+1)(2k^2)^k, k=1..400: fails at k =", fails)
print("  -> holds for every k in [%d, 400]" % (max(fails)+1))
# float version as printed in the paper, for the record
for k in (1, 2, 3, 4, 5):
    L = k*k*math.log(4) - math.log(2*k*k+1); Rr = k*math.log(2*k*k)
    print("  k=%d  k^2log4-log(2k^2+1)=%.4f   k log(2k^2)=%.4f   %s" % (k, L, Rr, L > Rr))
# analytic tail for k >= 400 (exact check covers 3..400):
#  log(2k^2+1) + k log(2k^2) <= (k+1) log(3k^2) = (k+1)(log3 + 2 log k) <= (k+1)(log3 + 2 sqrt k)   [log x <= sqrt x for x>0]
#  for k>=400: k+1 <= 1.0025k and log3 <= 0.055 sqrt k, so RHS <= 1.0025*2.055 k^{3/2} < 2.07 k^{3/2} <= (log 4) k^2  iff sqrt k >= 1.494.
print("  tail: max_x>0 (log x - sqrt x) =", max(math.log(x/100) - math.sqrt(x/100) for x in range(1, 10**6)), "(<0, so log x <= sqrt x)")
print("  tail: 1.0025*(math.log(3)/20 + 2) =", 1.0025*(math.log(3)/20 + 2), " and 2.07/log4 =", 2.07/math.log(4), "<= sqrt(400)=20")
# Claim D: prime factor of C(2k^2,k^2) in (k, 2k^2], k=3..12 (direct)
for k in range(3, 13):
    n = k*k
    fs = factorint(math.comb(2*n, n))
    big = [p for p in fs if p > k]
    assert big and max(big) <= 2*n
print("Claim D: C(2k^2,k^2) has a prime factor in (k,2k^2] for k=3..12: OK")

# CONTROL: n = k instead of n = k^2
ctl = [k for k in range(1, 401) if 4**k > (2*k+1)*(2*k)**k]
print("CONTROL (n=k): k in 1..400 where 4^k > (2k+1)(2k)^k:", ctl, "-> control FAILS for all k (expected)")
