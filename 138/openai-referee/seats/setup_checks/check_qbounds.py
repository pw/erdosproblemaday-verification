# (setup:q-bounds) 02-setup.tex l.84-92 and (setup:orders) l.97-101.
# q = least power of P >= k^{ck/D}, c = 1/100000, D = ceil(k^{1/10}).
# EXACT integer form (no floating point):  q >= k^{ck/D}  <=>  q^(10^5 D) >= k^k ;
#                                          q <= 2k^2 k^{ck/D} <=> q^(10^5 D) <= (2k^2)^(10^5 D) * k^k.
# Checked for EVERY prime P in (k, 2k^2] for k = 3..30 (uniformity over the choice in Lemma setup:prime),
# and for the least prime P>k at several larger k. Then log-scale (mpmath, 60 digits) for k up to 10^40.
# CONTROL (must FAIL): a prime P' > 2k^2 (outside Lemma setup:prime's range) -- the upper bound breaks.
import math, mpmath
from sympy import primerange, nextprime
mpmath.mp.dps = 60
C_DEN = 10**5

def iroot_ceil(k, r):
    D = max(1, int(round(k ** (1.0/r)))) if k < 10**300 else int(mpmath.ceil(mpmath.mpf(k)**(mpmath.mpf(1)/r)))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def least_q(P, k, D):            # least P^e (e>=0) with (P^e)^(C_DEN*D) >= k^k ; uses logs to guess e then exact fix-up
    E = C_DEN * D
    target = k**k
    e = max(0, int(mpmath.floor(mpmath.mpf(k)*mpmath.log(k)/(E*mpmath.log(P)))) - 1)
    while (P**e)**E < target: e += 1
    while e > 0 and (P**(e-1))**E >= target: e -= 1
    return e

def exact_bounds(P, k, D):
    e = least_q(P, k, D); q = P**e; E = C_DEN*D
    lower = q**E >= k**k
    upper = q**E <= (2*k*k)**E * k**k
    return e, lower, upper

def log_bounds(P, k, D):          # same inequalities in log form, 60-digit mpmath, returning margins
    c = mpmath.mpf(1)/C_DEN; lk = mpmath.log(k); lP = mpmath.log(P)
    e = max(1, int(mpmath.ceil(c*k*lk/(D*lP))))
    # minimality fix-up
    while e > 1 and (e-1)*lP*D >= c*k*lk: e -= 1
    while e*lP*D < c*k*lk: e += 1
    m_lo = D*e*lP - c*k*lk
    m_up = c*k*lk + D*mpmath.log(2*k*k) - D*e*lP
    return e, m_lo, m_up

viol = 0; cnt = 0; e_hist = {}; min_lo = None; min_up = None
for k in range(3, 61):
    D = iroot_ceil(k, 10)
    for P in primerange(k+1, 2*k*k+1):
        e, mlo, mup = log_bounds(P, k, D)
        cnt += 1; e_hist[e] = e_hist.get(e, 0) + 1
        if not (mlo >= 0 and mup >= 0 and e >= 1): viol += 1
        min_lo = mlo if min_lo is None else min(min_lo, mlo); min_up = mup if min_up is None else min(min_up, mup)
print("log-form q-bounds, k=3..60, EVERY prime P in (k,2k^2]: %d (k,P) pairs, violations=%d, exponent histogram=%s, min lower margin=%s, min upper margin=%s"
      % (cnt, viol, e_hist, mpmath.nstr(min_lo, 5), mpmath.nstr(min_up, 5)))

for k in [3, 10, 30, 100, 400]:
    D = iroot_ceil(k, 10); P = nextprime(k)
    e, lo, up = exact_bounds(P, k, D)
    print("EXACT integer form k=%d D=%d P=%d e=%d  q^(1e5 D) >= k^k: %s   q^(1e5 D) <= (2k^2)^(1e5 D) k^k: %s" % (k, D, P, e, lo, up))

print("\nlog-scale (mpmath 60 digits): ck log k <= D log q <= ck log k + D log(2k^2); orders of magnitude")
c = mpmath.mpf(1)/C_DEN
for k in [10**4, 10**6, 10**9, 10**12, 10**20, 10**40]:
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); h0 = D*D
    P = nextprime(k)
    lk, lP = mpmath.log(k), mpmath.log(P)
    e = int(mpmath.ceil(c*k*lk/(D*lP)))
    if e < 1: e = 1
    logq = e*lP
    lo = c*k*lk <= D*logq; up = D*logq <= c*k*lk + D*mpmath.log(2*mpmath.mpf(k)**2)
    # log lambda exactly as sum a*log l for k <= 10^12 (h0 small enough)
    if h0 <= 10**5:
        loglam = mpmath.fsum(mpmath.mpf(int(mpmath.floor(mpmath.log(2*M)/mpmath.log(l))))*mpmath.log(l) for l in primerange(2, h0+1))
        lam_ratio = mpmath.nstr(loglam/(mpmath.mpf(k)**(mpmath.mpf(1)/5)*lk), 4)
    else:
        lam_ratio = "skip"
    alpha_log = -(D+1)*logq
    R = mpmath.log1p(mpmath.exp(-alpha_log)/2)
    m = mpmath.ceil(mpmath.mpf(k)**2*R)
    print("k=1e%-3d D=%-5d e=%-14d lower=%s upper=%s | logq/(k^.9 logk)=%s  loglam/(k^.2 logk)=%s  D/k^.1=%s  M/k^.5=%s  |V|/(k^3 log k)=%s"
          % (round(math.log10(k)), D, e, lo, up, mpmath.nstr(logq/(mpmath.mpf(k)**0.9*lk), 4), lam_ratio,
             mpmath.nstr(D/mpmath.mpf(k)**0.1, 4), mpmath.nstr(M/mpmath.mpf(k)**0.5, 4), mpmath.nstr(2*m/(mpmath.mpf(k)**3*lk), 4)))

print("\nCONTROL: prime P' > 2k^2 (outside Lemma setup:prime)")
for k in [10, 20, 30]:
    D = iroot_ceil(k, 10); Pbad = nextprime(k**3)
    e, lo, up = exact_bounds(Pbad, k, D)
    print("k=%d P'=%d e=%d lower=%s upper=%s  -> %s" % (k, Pbad, e, lo, up, "upper bound FAILS (expected)" if not up else "control did not fail"))
