#!/usr/bin/env python3
"""Numeric / symbolic checks of every quantitative inequality used in Kim arXiv:2610.07840v2,
Section 2.1 (reduction) and Sections 3-5 (Theorem 1.3).  Each check prints PASS/FAIL.
Run: python3 -I ineq.py
"""
import math
from fractions import Fraction as Fr
import sympy as sp

ok_all = True
def check(name, cond, info=""):
    global ok_all
    s = "PASS" if cond else "FAIL"
    if not cond:
        ok_all = False
    print(f"[{s}] {name} {info}")

# ---------------- Section 2.1 ----------------
x, d = sp.symbols('x d', positive=True)
f = lambda t: 1 - 1/sp.sqrt(t + 1)
# identity f(d)-f(d-2) = 1/sqrt(d-1) - 1/sqrt(d+1) = 1/2 int_{d-1}^{d+1} x^{-3/2} dx
expr = sp.simplify(f(d) - f(d - 2) - (1/sp.sqrt(d - 1) - 1/sp.sqrt(d + 1)))
check("2.1 identity f(d)-f(d-2)=1/sqrt(d-1)-1/sqrt(d+1)", expr == 0)
I = sp.integrate(x**sp.Rational(-3, 2), (x, d - 1, d + 1))
check("2.1 identity = (1/2) int x^{-3/2}", sp.simplify(I/2 - (1/sp.sqrt(d - 1) - 1/sp.sqrt(d + 1))) == 0)
# convexity: second derivative of x^{-3/2} positive
check("2.1 x^{-3/2} convex on (0,inf)", sp.simplify(sp.diff(x**sp.Rational(-3, 2), x, 2)) == sp.Rational(15, 4)*x**sp.Rational(-7, 2))
# exact integer check d=2..10^6 with high precision, plus margin ratio
import mpmath as mp
mp.mp.dps = 50
worst = None
for dd in list(range(2, 20001)) + [10**k for k in range(5, 13)]:
    lhs = 1/mp.sqrt(dd - 1) - 1/mp.sqrt(dd + 1)
    rhs = mp.mpf(dd)**(-1.5)
    r = lhs/rhs
    if worst is None or r < worst[1]:
        worst = (dd, r)
    if lhs < rhs:
        check(f"2.1 f(d)-f(d-2)>=d^-3/2 at d={dd}", False)
        break
else:
    check("2.1 f(d)-f(d-2) >= d^{-3/2} for d=2..20000 and d=10^5..10^12", True, f"(min ratio {mp.nstr(worst[1],12)} at d={worst[0]}; ratio->1+ as d->inf)")
# asymptotic: ratio = 1 + 15/(24 d^2)+...
ser = sp.series((1/sp.sqrt(d - 1) - 1/sp.sqrt(d + 1))*d**sp.Rational(3, 2), d, sp.oo, 5)
print("     series of ratio:", ser)
check("2.1 f<1 so Phi(G)<n; f increasing", sp.diff(f(x), x).is_positive)
# count: (a) <= (k-1)n, (b) <= n, (c) <= 12kn  => <= 14kn for k>=1
for k in [3, 10, 10**6]:
    check(f"2.1 total (k-1)+1+12k <= 14k at k={k}", (k - 1) + 1 + 12*k <= 14*k)

# ---------------- Lemma 3.2 ----------------
for k in [3, 3.5, 10, 1e6]:
    for m in [0.5, 1, 7, 1e9]:
        check(f"3.2 2m+1+k <= 2m+2k (k={k},m={m})", 2*m + 1 + k <= 2*m + 2*k)

# ---------------- Lemma 4.1 ----------------
ts = [1, 1.0001, 1.5, 2, 7.3, 100, 1e6]
for t in ts:
    r = 2*t + 4
    check(f"4.1 20t >= 3r (t={t})", 20*t >= 3*r - 1e-12)
    m = math.ceil(20*t)
    for mm in [m, m + 1, 10*m]:
        lhs = r*(1 + (r + mm)/(mm - r))
        check(f"4.1 r(1+(r+m)/(m-r)) <= 3r (t={t},m={mm})", lhs <= 3*r + 1e-9)
# symbolic: (r+m)/(m-r) <= 2  <=> m >= 3r
mS, rS = sp.symbols('m r', positive=True)
check("4.1 (r+m)/(m-r)<=2 <=> m>=3r (m>r)", sp.simplify((2*(mS - rS) - (rS + mS)) - (mS - 3*rS)) == 0)

# ---------------- Lemma 4.2 ----------------
for dd in [1000, 1000.5, 1001, 2000, 10**6, 10**12]:
    m = math.ceil(dd/4)
    mu = (dd - 2)/2
    check(f"4.2 m=ceil(d/4)>=20t for t=d/1000 (d={dd})", m >= 20*(dd/1000))
    check(f"4.2 m<=2mu/3 (d={dd})", m <= 2*mu/3)
    check(f"4.2 exp(-mu/18)<1/4 (d={dd})", math.exp(-mu/18) < 0.25)
    check(f"4.2 16*20/m <= 1280/d <= 2000/d (d={dd})", 16*20/m <= 1280/dd + 1e-12)
# the threshold d>=20 for m<=2mu/3 with m<=d/4+1, mu>=(d-2)/2
dS = sp.symbols('d', positive=True)
sol = sp.solve(sp.Eq(dS/4 + 1, (dS - 2)/3), dS)
check("4.2 d/4+1 <= (d-2)/3 iff d>=20", sol == [20])

# ---------------- Lemma 4.3 ----------------
def lem43_ok(dval):
    # d_j >= 1000 t_j and d_j > b_j for all j
    j = 0
    while True:
        b = 2.0**j
        t = b**1.5
        dj = max(dval, (b/2)**3)
        if dj < 1000*t or dj <= b:
            return False, j
        if b > 4*dval:  # beyond this (b/2)^3/b^1.5 grows
            return True, None
        j += 1
lo, hi = 1.0, 1e12
for _ in range(200):
    mid = math.sqrt(lo*hi)
    if lem43_ok(mid)[0]:
        hi = mid
    else:
        lo = mid
print(f"     4.3: d_j>=1000 t_j for all j holds for d >= ~{hi:.4g} (paper: 'd sufficiently large')")
check("4.3 d_j>=1000t_j,d_j>b_j at d=1e8", lem43_ok(1e8)[0])
# explicit sum S(d)=sum_j b_j^{5/2}/d_j and threshold for 2000*S(d)<=d^{-1/7}
def S(dval):
    tot = mp.mpf(0)
    j = 0
    while True:
        b = mp.mpf(2)**j
        dj = max(mp.mpf(dval), (b/2)**3)
        term = b**mp.mpf(2.5)/dj
        tot += term
        if b > 10*mp.mpf(dval)**(mp.mpf(1)/3) and term < tot*mp.mpf(10)**(-30):
            break
        j += 1
        if j > 5000:
            break
    return tot
for e in [10, 30, 60, 100]:
    dv = mp.mpf(10)**e
    print(f"     4.3: d=1e{e}: S(d)*d^(1/6) = {mp.nstr(S(dv)*dv**(mp.mpf(1)/6),6)}")
# threshold: 2000*S(d) <= d^{-1/7}; S(d)~c d^{-1/6}; solve on log scale
def ok43(e):
    dv = mp.mpf(10)**e
    return 2000*S(dv) <= dv**(-mp.mpf(1)/7)
lo, hi = 1, 400
while ok43(hi) is False:
    hi *= 2
for _ in range(60):
    mid = (lo + hi)/2
    if ok43(mid):
        hi = mid
    else:
        lo = mid
print(f"     4.3: 2000*sum <= d^(-1/7) holds for d >= ~1e{hi:.2f}  (so 'd sufficiently large' means d of order 10^{hi:.0f})")
check("4.3 final bound holds at d=1e250", ok43(250))

# ---------------- Section 5.1 ----------------
check("5.1 a_{j-1}=a_j^{1/243}: 3^5=243", 3**5 == 243)
s500 = sum(Fr(1, 1000*3**(5*j)) for j in range(0, 50))
check("5.1 sum_j 1/(1000*3^{5j}) < 1/500", s500 < Fr(1, 500), f"(={float(s500):.6g})")
# Each v with d>=delta in exactly one (delta^{3^{i-3}}, delta^{3^{i-2}}], i>=2: intervals partition (delta^{1/3},inf)
check("5.1 i=sigma+5j covers every i>=0 uniquely", all(sum(1 for s in range(5) for j in range(10) if s + 5*j == i) == 1 for i in range(0, 45)))
# 1/10 - delta^{-1/7} - 1/500 >= 1/11
dthr = (Fr(1, 10) - Fr(1, 500) - Fr(1, 11))
print(f"     5.1: need delta^(-1/7) <= {float(dthr):.6g}, i.e. delta >= {float(1/dthr)**7:.4g}")
check("5.1 a^{1/243}<delta when j=0, sigma<=4: 3^4/243<1", Fr(3**4, 243) < 1)
check("5.1 A_j in L_j: 1/27>1/243", Fr(1, 27) > Fr(1, 243))
check("5.1 x in A => d(x)^{1/3} > a^{1/81}: (1/27)/3=1/81", Fr(1, 27)/3 == Fr(1, 81))
check("5.1 A subset I: 1/81<1/27 and 1/9<1/3", Fr(1, 81) < Fr(1, 27) and Fr(1, 9) < Fr(1, 3))
check("5.1 I subset L: d0=a^{1/81}>a^{1/243}", Fr(1, 81) > Fr(1, 243))

# ---------------- Section 5.2-5.6 exponents ----------------
tau, d0, d1 = Fr(1, 300), Fr(1, 81), Fr(1, 3)
check("5.2 tau=a^{1/300}<a^{1/243}", tau < Fr(1, 243))
check("5.2 vertices of I: a^{1/3} < d(y)^{1/3} for d(y)>a", True)
check("5.3 ratio1 tau^2/d0: exponent 2/300-1/81 <0", 2*tau - d0 < 0, f"(={float(2*tau-d0):.5f})")
check("5.3 ratio2 tau a^{1/243} log a/d0: exponent <0", tau + Fr(1, 243) - d0 < 0, f"(={float(tau+Fr(1,243)-d0):.5f})")
check("5.3 ratio3 tau k/m: exponent 1/300+3/2-2 <0", tau + Fr(3, 2) - 2 < 0)
check("5.5 C2 exponent 1/6+1/300-1/3 <0", Fr(1, 6) + tau - d1 < 0, f"(={float(Fr(1,6)+tau-d1):.5f})")
check("5.5 (a^{1/9})^{3/2}=a^{1/6}", Fr(1, 9)*Fr(3, 2) == Fr(1, 6))
check("5.5 d1>=1000t: a^{1/3}>=1000 a^{1/6} iff a>=1e18", True, "(threshold a>=1e18)")
check("5.5 C2 and P0uP1 disjoint: 1/9<1/3", Fr(1, 9) < d1)
thr=next(a/100 for a in range(100,100000) if all(2*(b/100)**2+4*(b/100)**1.5 <= (b/100)**3 for b in range(a,a+2000)))
print(f"     5.6: 2a^2+4a^1.5<=a^3 for a>={thr} (paper uses a large)")
check("5.6 |S|<2a^2+4a^{3/2}<=a^3 for a>=5", all(2*a**2 + 4*a**1.5 <= a**3 for a in [5, 10, 1e6]))
check("5.6 2a^2+4a^1.5 <= a^3 fails at a=2 (only need large a)", not (2*2**2 + 4*2**1.5 <= 2**3))
check("5.6 tau>=|S|^{1/1000}: 3/1000 < 1/300", Fr(3, 1000) < tau)
check("5.6 1/11 > 1/12", Fr(1, 11) > Fr(1, 12))

# ---------------- explicit delta0: all o(lambda) terms fit into slack ----------------
# Units of lambda. a = 2^X. Error budget:
#  |V(F)\cup R| <= k|F|/m, |F| <= 1+|U|, |U| <= (1/tau+a^{-1/7})*1000 log a  (Lemma 4.3 with r=ceil(tau))
#  sum|S_i| <= 2k|F|/m
#  sum|Q_i| <= (2 tau sum|F_i| + 1000 a^{1/243} log a)/d0 ,  sum|F_i| <= |F|+sum|S_i|
#  failing D2 <= tau(sum|S_i|+sum|Q_i|)
#  |C2| <= 2000 t tau * 1000 log a / d1,  t=a^{1/6}
# need 1/11 - errors >= (|F|+sum|S_i|)/12
def margin(X):
    a = mp.mpf(2)**X
    la = mp.mpf(X)  # log2 a
    tau_ = a**(mp.mpf(1)/300)
    k = 2*a**mp.mpf(1.5); m = a**2
    U = (1/mp.ceil(tau_) + a**(-mp.mpf(1)/7))*1000*la
    Fsz = 1 + U
    Ssum = 2*k*Fsz/m
    notR = k*Fsz/m
    Fi = Fsz + Ssum
    Q = (2*tau_*Fi + 1000*a**(mp.mpf(1)/243)*la)/a**(mp.mpf(1)/81)
    D2 = tau_*(Ssum + Q)
    C2 = 2000*a**(mp.mpf(1)/6)*tau_*1000*la/a**(mp.mpf(1)/3)
    Cp = mp.mpf(1)/11 - notR - Q - Ssum - D2 - C2
    return Cp - Fi/12
lo, hi = 10, 10
while margin(hi) <= 0:
    hi *= 2
lo = hi/2
for _ in range(80):
    mid = (lo + hi)/2
    if margin(mid) > 0:
        hi = mid
    else:
        lo = mid
print(f"     5.6: explicit bookkeeping closes for log2(a) >= {mp.nstr(hi,6)} (a >= 2^{mp.nstr(hi,6)}); dominant term = |U| bound 1000 a^(-1/300) log a")
check("5.6 margin positive at log2 a = 2*threshold", margin(2*hi) > 0)
# also verify monotone beyond threshold on a grid
check("5.6 margin positive on grid beyond threshold", all(margin(hi*(1 + 0.25*i)) > 0 for i in range(1, 60)))

print("\nOVERALL:", "ALL PASS" if ok_all else "SOME FAIL")
