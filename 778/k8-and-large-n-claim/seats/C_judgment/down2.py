#!/usr/bin/env python3
"""Necessary-condition search restricted to INTEGER n >= 8 (exact betaln log-binomials).
Same conditions as down.py; bonus s = 1 (V_R nonempty) + 1 if t(l-1) >= a (V_R has an a-set, so a Chingiz edge).
Integers 8..2e4 exhaustively, then log grid to e^60."""
import math, numpy as np
from scipy.special import betaln
LN3 = math.log(3)
lnC = lambda n, k: -np.log1p(n) - betaln(n - k + 1, k + 1)
D = lambda t, p=2/3: t*math.log(t/p) + (1-t)*math.log((1-t)/(1-p))
def least_pass(f, n):
    lo = np.full_like(n, 2.0); hi = n.copy()
    for _ in range(80):
        mid = np.floor((lo + hi)/2); up = f(mid + 1) > f(mid)
        lo = np.where(up, mid + 1, lo); hi = np.where(up, hi, mid)
    ok_end = f(n) < 0
    lo = lo.copy(); hi = n.copy()
    for _ in range(80):
        mid = np.floor((lo + hi)/2); ok = f(mid) < 0
        hi = np.where(ok, mid, hi); lo = np.where(ok, lo, np.minimum(mid + 1, hi))
    return np.where(ok_end, hi, np.inf)
def run(n, S):
    a = least_pass(lambda k: lnC(n, k) - LN3*k*(k-1)/2, n)
    anyok = np.zeros_like(n, dtype=bool); tbest = np.full_like(n, np.nan)
    for t in np.round(np.arange(0.30, 0.6665, 0.005), 4):
        eta = D(t); c = t/(1-t)
        l = least_pass(lambda k: lnC(n, k) - eta*k*(k-1)/2, n)
        R = 1 + np.floor((np.log(n + c) - np.log(l + c)) / math.log(1/t))
        s = 1 + (t*(l-1) >= a) + S
        ok = np.isfinite(l) & (R + s >= a)
        tbest = np.where(ok & ~anyok, t, tbest); anyok |= ok
    return anyok, a, tbest
n1 = np.arange(8, 20_001, dtype=float)
x2 = np.arange(math.log(20_001), 60.0, 0.005); n2 = np.exp(x2)
for S in [0, 1, 3]:
    ok1, a1, _ = run(n1, S)
    ok2, a2, tb2 = run(n2, S)
    print(f"S_extra={S}: integers 8..2e4 passing: {int(ok1.sum())}" + (f" (first {int(n1[ok1][0])})" if ok1.any() else ""))
    if ok2.any():
        i = np.where(ok2)[0][0]
        print(f"   log grid: first pass ln n = {x2[i]:.2f} (n ~ 10^{x2[i]/math.log(10):.2f}), t={tb2[i]}, a={int(a2[i])}")
