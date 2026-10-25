#!/usr/bin/env python3
"""NOTE: the DOWN block below is SUPERSEDED by down2.py -- its binomial lower bound
(n-k)^k/k! degenerates at small n and produced spurious passes at n~4. Use the UP block only.

One-parameter family of the Didin-Pimenov argument.

Target density t, P_U = lam^{tH - x_U} mu^{f_U}.  Bella edge in U: x1/mu =: u.
Chingiz edge in U: x 1/(lam*mu) =: r (or -> 0 at threshold).  Exact Lemma-1 accounting
(Bella's increase = 2 x Chingiz's guaranteed decrease, danger weight (1-r) on P_U):
     u - 1 = 2 (1 - r).
theta = lam^t mu = u^{t-1} r^{-t};  minimised over u at u = 3(1-t), r = 3t/2, giving
     -ln theta = D(t || 2/3)   (KL divergence, Chernoff exponent).
Lemma 2 generalises: m_{i+1} + c >= t (m_i + c) with c = t/(1-t);
     R_t(n) = 1 + floor(log_{1/t}((n+c)/(l+c))).
Q-part unchanged: Q_A = 3^{-f_A}, a = least integer with the Q-sum small.

Two computations:
 (UP)   sufficient conditions (method provably works at n): SQ <= 1/2, SP <= 1/2 with
        binom(n,k) <= n^k/k!, opening-edge factors 3 and u, win iff R_t + slack >= a.
        Report last failing ln n for each t (slack 0 = faithful; slack 1 = the free extra
        vertex w in V_R, which the paper does not count).
 (DOWN) necessary conditions (generous): initial sums >= binom(n,k) * base^{-binom(k,2)},
        binom(n,k) >= (n-k)^k/k!, a = least a with ln binom(n,a) - binom(a,2) ln 3 < 0,
        l = least l with ln binom(n,l) - eta(t) binom(l,2) < 0, slack up to 3.
        Report the smallest ln n at which ANY t passes.
"""
import math, sys
import numpy as np
from scipy.special import gammaln, digamma

LN3 = math.log(3)

def D(t, p=2/3):
    return t*math.log(t/p) + (1-t)*math.log((1-t)/(1-p))

def least_beyond_hump(f, fprime, x, target, lo_init=1.0, hi_init=1e9):
    """least integer k >= argmax with f(k) < target (f concave in k); vectorised over x."""
    # argmax via bisection on fprime
    lo = np.full_like(x, lo_init); hi = np.full_like(x, hi_init)
    for _ in range(64):
        mid = (lo+hi)/2
        pos = fprime(mid, x) > 0
        lo = np.where(pos, mid, lo); hi = np.where(pos, hi, mid)
    peak = lo
    lo = np.floor(peak); hi = np.full_like(x, hi_init)
    for _ in range(64):
        mid = np.floor((lo+hi)/2)
        ok = f(mid, x) < target
        hi = np.where(ok, mid, hi); lo = np.where(ok, lo, mid)
    return hi

def up_last_failure(t, xs, slack=0):
    eta = D(t); u = 3*(1-t); c = t/(1-t)
    # Q: ln(3) + a x - lnfact(a) - ln3 a(a-1)/2 <= ln 1/2
    fQ = lambda a, x: LN3 + a*x - gammaln(a+1) - LN3*a*(a-1)/2
    fQp = lambda a, x: x - digamma(a+1) - LN3*(a-0.5)
    a = least_beyond_hump(fQ, fQp, xs, math.log(0.5))
    fP = lambda l, x: math.log(u) + l*x - gammaln(l+1) - eta*l*(l-1)/2
    fPp = lambda l, x: x - digamma(l+1) - eta*(l-0.5)
    l = least_beyond_hump(fP, fPp, xs, math.log(0.5))
    R = 1 + np.floor((xs - np.log(l + c)) / math.log(1/t))   # n+c ~ n
    ok = (R + slack >= a) & (l < np.exp(xs))
    bad = np.where(~ok)[0]
    return (xs[bad[-1]] if len(bad) else None), a, l, R

def down_first_success(t, xs, slack=3):
    eta = D(t); c = t/(1-t)
    n = np.exp(xs)
    lnb = lambda k, x: k*np.log(np.maximum(np.exp(x)-k, 1e-300)) - gammaln(k+1)  # lower bound
    fQ = lambda a, x: lnb(a, x) - LN3*a*(a-1)/2
    fQp = lambda a, x: x - digamma(a+1) - LN3*(a-0.5)
    a = least_beyond_hump(fQ, fQp, xs, 0.0)
    fP = lambda l, x: lnb(l, x) - eta*l*(l-1)/2
    fPp = lambda l, x: x - digamma(l+1) - eta*(l-0.5)
    l = least_beyond_hump(fP, fPp, xs, 0.0)
    l = np.minimum(l, n)
    R = 1 + np.floor((np.log(n + c) - np.log(l + c)) / math.log(1/t))
    ok = (R + slack >= a)
    good = np.where(ok)[0]
    return (xs[good[0]] if len(good) else None)

if __name__ == "__main__":
    print("t       u=3(1-t) r=3t/2  eta=D(t||2/3)  2/eta     1/ln(1/t)  (2/ln3=%.4f)  kappa=log3(3t^2)" % (2/LN3))
    for t in [0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.645, 0.65, 0.655, 0.66, 0.665]:
        print(f"{t:.3f}   {3*(1-t):.4f}  {1.5*t:.4f}  {D(t):.6f}   {2/D(t):9.1f}  {1/math.log(1/t):.4f}   {math.log(3*t*t)/LN3:.4f}")
    print(f"check t=3/5: D = {D(0.6):.10f}, -ln theta_paper = {-math.log((4/3)**0.6*(5/6)):.10f}")
    print(f"t=1/sqrt3 = {1/math.sqrt(3):.5f}: D = {D(1/math.sqrt(3)):.6f} (largest eta among t with kappa>0)")
    print()
    xs = np.arange(2.0, 260.0, 0.01)
    print("UP (sufficient; method provably works for all n >= e^x*):")
    rows = []
    for t in np.round(np.arange(0.585, 0.6665, 0.0025), 4):
        r0 = up_last_failure(t, xs, 0)[0]; r1 = up_last_failure(t, xs, 1)[0]
        rows.append((t, r0, r1))
        f = lambda v: f"ln n0={v:7.2f} (10^{v/math.log(10):5.1f})" if v is not None else "none"
        print(f"  t={t:.4f}  slack0: {f(r0)}   slack1: {f(r1)}")
    b0 = min(rows, key=lambda r: r[1]); b1 = min(rows, key=lambda r: r[2])
    print(f"  best slack0: t={b0[0]}  ln n0={b0[1]:.2f}  n0~10^{b0[1]/math.log(10):.1f}")
    print(f"  best slack1: t={b1[0]}  ln n0={b1[2]:.2f}  n0~10^{b1[2]/math.log(10):.1f}")
    t06 = [r for r in rows if abs(r[0]-0.6) < 1e-9][0]
    print(f"  t=0.6 in this (n^k/k!, 1/2+1/2 split, least a) setup: slack0 ln n0={t06[1]:.2f}")
    print()
    print("DOWN (necessary, generous; slack 3): smallest ln n where ANY t could work:")
    xs2 = np.arange(1.4, 120.0, 0.005)
    best = None
    for t in np.round(np.arange(0.40, 0.6665, 0.0025), 4):
        v = down_first_success(t, xs2, 3)
        if v is not None and (best is None or v < best[1]): best = (t, v)
    print(f"  first possible success: t={best[0]}, ln n={best[1]:.2f}, n~10^{best[1]/math.log(10):.1f}")
    for s in [0, 1, 2, 5, 10]:
        bb = None
        for t in np.round(np.arange(0.40, 0.6665, 0.0025), 4):
            v = down_first_success(t, xs2, s)
            if v is not None and (bb is None or v < bb[1]): bb = (t, v)
        print(f"  slack {s:2d}: first possible ln n = {bb[1]:.2f} (n~10^{bb[1]/math.log(10):.1f}) at t={bb[0]}")
