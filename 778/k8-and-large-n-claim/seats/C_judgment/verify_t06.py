#!/usr/bin/env python3
"""Spot-check family.py UP result at t=3/5 (faithful Lemma 2, slack 0): claimed last failure ln n = 91.99.
Exact mpmath: least a with 3*C(n,a)*3^{-C(a,2)} <= 1/2 and least l with (6/5)*C(n,l)*theta^{C(l,2)} <= 1/2
(these are valid since the true initial sums are <= these), R = 1+floor(log_{5/3}((n+3/2)/(l+3/2)))."""
from mpmath import mp, mpf, log, binomial, floor, power, exp, ceil
mp.dps = 80
theta = power(mpf(4)/3, mpf(3)/5)*mpf(5)/6; eta = -log(theta)
def least(f, lo, hi):
    while f(lo) >= 0: lo += 1
    return lo
def check(x):
    n = floor(exp(mpf(x)))
    fa = lambda a: log(3) + log(binomial(n, a)) - mpf(a)*(a-1)/2*log(3) - log(mpf(1)/2)
    a = int(2*x/1.0986) - 30
    while fa(a) >= 0: a += 1
    fl = lambda l: log(mpf(6)/5) + log(binomial(n, l)) - mpf(l)*(l-1)/2*eta - log(mpf(1)/2)
    l = int(2*x/float(eta)) - 2000
    while fl(l) < 0: l -= 50
    while fl(l) >= 0: l += 1
    R = 1 + int(floor(log((n + mpf(3)/2)/(l + mpf(3)/2))/log(mpf(5)/3)))
    pa = int(ceil(2*log(n)/log(3))) + 2
    return dict(x=x, a_least=a, a_paper=pa, l=l, R=R, ok=R >= a)
for x in [91.90, 91.97, 92.01, 92.3, 95.0]:
    print(check(x))
