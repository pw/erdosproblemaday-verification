#!/usr/bin/env python3
# SUPERSEDED by down2.py: real-valued n below 8 produced spurious passes; restrict to integer n >= 8.
"""NECESSARY conditions for ANY member of the one-parameter family to certify a Chingiz win at n.
(Replaces the DOWN block of family.py, whose binomial lower bound (n-k)^k/k! degenerated at small n.)
Exact log-binomials via betaln.  For each n (log grid) and t in a grid:
  a  = least a >= 2 with ln C(n,a) - C(a,2) ln 3 < 0    (initial sum Q >= C(n,a) 3^{-C(a,2)} must be < 1)
       -> Bella certified bound omega_B <= a-1
  l  = least l in [2,n] with ln C(n,l) - D(t||2/3) C(l,2) < 0   (any legal multipliers have eta <= D)
  R  = 1 + floor(log_{1/t}((n+c)/(l+c))),  c = t/(1-t)
  s  = generous extra vertices from V_R: +1 always (V_R nonempty), +1 more if t(l-1) >= a, +S_extra
  need R + s >= a.
Reports the smallest ln n at which some t passes, for S_extra = 0, 1, 3, 10."""
import math, numpy as np
from scipy.special import betaln

LN3 = math.log(3)
def lnC(n, k):
    return -np.log1p(n) - betaln(n - k + 1, k + 1)
def D(t, p=2/3):
    return t*math.log(t/p) + (1-t)*math.log((1-t)/(1-p))

def least_pass(f, n, lo_val=2.0):
    """least integer k in [2, n] with f(k) < 0, f concave, f(2) > 0 assumed; returns inf if none."""
    # find argmax by ternary-ish bisection on discrete slope
    lo = np.full_like(n, lo_val); hi = n.copy()
    for _ in range(90):
        mid = np.floor((lo + hi)/2)
        up = f(mid + 1) > f(mid)
        lo = np.where(up, mid + 1, lo); hi = np.where(up, hi, mid)
    peak = lo
    ok_end = f(n) < 0
    lo = peak.copy(); hi = n.copy()
    for _ in range(90):
        mid = np.floor((lo + hi)/2)
        ok = f(mid) < 0
        hi = np.where(ok, mid, hi); lo = np.where(ok, lo, mid + 0)
        lo = np.where(ok, lo, np.minimum(mid + 1, hi))
    return np.where(ok_end, hi, np.inf)

xs = np.arange(math.log(4), 60.0, 0.005)
n = np.exp(xs)
fa = lambda a: lnC(n, a) - LN3*a*(a-1)/2
a = least_pass(fa, n)
ts = np.round(np.arange(0.40, 0.6665, 0.0025), 4)
for S in [0, 1, 3, 10]:
    first = None
    for t in ts:
        eta = D(t); c = t/(1-t)
        fl = lambda l: lnC(n, l) - eta*l*(l-1)/2
        l = least_pass(fl, n)
        R = 1 + np.floor((np.log(n + c) - np.log(l + c)) / math.log(1/t))
        s = 1 + (t*(l-1) >= a) + S
        ok = np.isfinite(l) & (R + s >= a)
        idx = np.where(ok)[0]
        if len(idx) and (first is None or xs[idx[0]] < first[1]):
            i = idx[0]; first = (t, xs[i], int(a[i]), int(l[i]), int(R[i]))
    t, x, ai, li, Ri = first
    print(f"S_extra={S:2d}: first ln n = {x:6.2f} (n ~ 10^{x/math.log(10):5.2f}) at t={t}: a={ai}, l={li}, R={Ri}")
# sanity: small n table at t=0.6
for nn in [8, 20, 100, 10**4]:
    N = np.array([float(nn)])
    aa = least_pass(lambda k: lnC(N, k) - LN3*k*(k-1)/2, N)
    ll = least_pass(lambda k: lnC(N, k) - D(0.6)*k*(k-1)/2, N)
    print(f"n={nn}: least a={aa[0]}, least l (t=0.6) = {ll[0]}")
