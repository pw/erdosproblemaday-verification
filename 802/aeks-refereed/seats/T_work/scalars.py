"""All scalar inequalities used in Lemma 4.1 / Lemma 5.3 / Prop 5.4 / proof of Thm 3.1, checked on a grid
x in [32, 1e12] (log-spaced, plus dense near 32) and C in {1, 2, 10, 256, 1e4}. Prints any failure."""
import numpy as np
from mpmath import mp, mpf, log, exp, sqrt, ceil
mp.dps = 50
xs = sorted(set([mpf(32) + mpf(k) / 100 for k in range(0, 2000)] + [mpf(10) ** (mpf(k) / 20) for k in range(31, 241)]))
Cs = [mpf(1), mpf(2), mpf(10), mpf(256), mpf(10) ** 4]
fails = []
def chk(name, cond, x, C=None):
    if not cond: fails.append((name, float(x), None if C is None else float(C)))
for x in xs:
    R = ceil(x)
    chk('6logx<=x', 6 * log(x) <= x, x)
    chk('log(1+e^2x x^6)<=4x', log(1 + exp(2 * x) * x ** 6) <= 4 * x, x)
    chk('R<=2x', R <= 2 * x, x)
    chk('x+R log(1+e^2x x^6)<=20x^2', x + R * log(1 + exp(2 * x) * x ** 6) <= 20 * x ** 2, x)
    chk('20x^2+log x <= 21 x^2', 20 * x ** 2 + log(x) <= 21 * x ** 2, x)
    chk('e^-x<=x^-7', exp(-x) <= x ** -7, x)
    chk('R x^-4 < 1', R * x ** -4 < 1, x)
    chk('sqrt(log x)<=log x', sqrt(log(x)) <= log(x), x)
    chk('f decreasing (x>=e^2)', x >= exp(2), x)
    for C in Cs:
        EC = 42 * C ** 2 + 2 * C; AC = 10 + EC; BC = 2 * sqrt(AC + 1); aC = 6 * (BC + AC + 1)
        chk('42C^2x^-4+2Cx^3e^-x<=E_C x^-4', 42 * C ** 2 * x ** -4 + 2 * C * x ** 3 * exp(-x) <= EC * x ** -4, x, C)
        chk('H_R final', log(2) + 8 * log(x) + R * x ** -3 + EC * x ** -3 <= AC * log(x), x, C)
        chk('2sqrt((A+1)logx/R)... B_C', 2 * sqrt((AC + 1) * log(x) / R) <= BC * sqrt(log(x) / x), x, C)
        dx = (AC + 1) * log(x) / (sqrt(x) + log(x))
        chk('6B sqrt(logx/x)+6dx<=aC logx/sqrtx', 6 * BC * sqrt(log(x) / x) + 6 * dx <= aC * log(x) / sqrt(x), x, C)
print('grid points', len(xs), 'failures', len(fails))
for f in fails[:20]: print(f)
# X(C) magnitude for r=4 (C=16 r^2=256) -- informational
for C in [mpf(1), mpf(256)]:
    EC = 42 * C ** 2 + 2 * C; AC = 10 + EC; BC = 2 * sqrt(AC + 1); aC = 6 * (BC + AC + 1)
    lo, hi = mpf(32), mpf(10) ** 40
    for _ in range(400):
        mid = sqrt(lo * hi)
        if 2 * aC * log(mid) / sqrt(mid) <= mpf(1) / 2: hi = mid
        else: lo = mid
    print('C', float(C), 'a_C', float(aC), 'minimal X(C) ~', float(hi))
