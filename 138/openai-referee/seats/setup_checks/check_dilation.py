# Lemma setup:dilation (02-setup.tex l.24-52) + standing threshold h0 < 2M < k (l.21) + gcd(lambda,q)=1 (l.90-92).
# Literal parameters: D = ceil(k^{1/10}), M = ceil(k^{1/2}), h0 = D^2,
#   lambda = prod_{l <= h0 prime} l^{floor(log(2M)/log l)}   (exponent computed EXACTLY as the largest a with l^a <= 2M).
# Checks for each k: (1) log lambda <= h0 log(2M); (2) every prime-power divisor l^a || h (l<=h0) divides lambda, 1<=h<=2M;
#   (3) h | lambda for 1<=h<=h0; (4) s = h/gcd(h, lambda t) is 1 or > h0 for all 1<=h<=2M and ALL residues t mod h
#   (s depends on t only mod h; t=0 included); (5) gcd(lambda, P) = 1 for the least prime P > k.
# CONTROL (must FAIL): lambda_bad = lcm(1..h0) (= exponents floor(log h0/log l), i.e. NOT the full primary part up to 2M).
import math
from sympy import primerange, nextprime

def iroot_ceil(k, r):           # least D with D^r >= k
    D = max(1, int(round(k ** (1.0/r))))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def params(k):
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); return D, M, D*D

def lam_paper(h0, M):            # floor(log(2M)/log l) = largest a with l^a <= 2M
    lam = 1
    for l in primerange(2, h0+1):
        a = 0
        while l**(a+1) <= 2*M: a += 1
        lam *= l**a
    return lam

def lam_bad(h0):                 # lcm(1..h0)
    return math.lcm(*range(1, h0+1))

def check(k, lam, verbose=True):
    D, M, h0 = params(k)
    ok1 = math.log(lam) <= h0 * math.log(2*M) + 1e-9
    bad2 = bad3 = bad4 = 0; ex4 = None
    for h in range(1, 2*M+1):
        # prime-power parts
        x = h
        for l in primerange(2, min(h0, h)+1):
            if x % l == 0:
                pp = 1
                while x % l == 0: x //= l; pp *= l
                if lam % pp: bad2 += 1
        if h <= h0 and lam % h: bad3 += 1
        for t in range(h):
            s = h // math.gcd(h, lam*t)
            if not (s == 1 or s > h0):
                bad4 += 1
                if ex4 is None: ex4 = (h, t, s)
    P = nextprime(k)
    ok5 = math.gcd(lam, P) == 1
    if verbose:
        print("k=%-8d D=%d M=%d h0=%d 2M=%d lambda=%d log(lambda)=%.2f <= h0*log(2M)=%.2f: %s | primary-part viol=%d  h|lam viol(h<=h0)=%d  s-viol=%d %s | gcd(lambda,P=%d)=1: %s"
              % (k, D, M, h0, 2*M, lam, math.log(lam), h0*math.log(2*M), ok1, bad2, bad3, bad4, ("first "+str(ex4)) if ex4 else "", P, ok5))
    return ok1 and bad2 == 0 and bad3 == 0 and bad4 == 0 and ok5

ks = [7, 100, 1024, 1025, 10**4, 59049, 59050, 10**5, 10**6]
allok = True
for k in ks:
    D, M, h0 = params(k)
    allok &= check(k, lam_paper(h0, M))
print("PAPER lambda: all checks pass for k in", ks, ":", allok)

print("\nCONTROL lambda_bad = lcm(1..h0):")
for k in [100, 10**4, 10**6]:
    D, M, h0 = params(k)
    check(k, lam_bad(h0))

# standing threshold h0 < 2M < k, exact integer arithmetic, k = 1..10^6
fails = [k for k in range(1, 10**6+1) if not (params(k)[2] < 2*params(k)[1] < k)]
print("\nh0 < 2M < k fails for k in", fails[:20], "... (max failing k =", max(fails), ") over 1..10^6")
# for k >= 10^6: h0 <= (k^{0.1}+1)^2 <= 4 k^{0.2} < 2 k^{0.5} <= 2M and 2M <= 2k^{0.5}+2 < k  (both hold once k >= 16)
print("tail: 4*k**0.2 < 2*k**0.5 and 2*k**0.5+2 < k at k=1e6:", 4*1e6**0.2 < 2*1e6**0.5, 2*1e6**0.5 + 2 < 1e6)
