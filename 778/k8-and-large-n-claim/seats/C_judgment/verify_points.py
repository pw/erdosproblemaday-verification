#!/usr/bin/env python3
"""Independent exact-integer cross-check of the paper-constant threshold (mpmath, 60 digits).
For integer n, C = 206 (C*eta > 2): a = ceil(2 log_3 n)+2, l = ceil(C ln n),
SQ = 3^(1-a/2), SP = (6/5)(n theta^((l-1)/2))^l, R = 1 + floor(log_{5/3}((n+3/2)/(l+3/2))).
Worst points of each a-block: n just above 3^(k/2) (a has just stepped up)."""
from mpmath import mp, mpf, log, ceil, floor, exp, power
mp.dps = 60
theta = power(mpf(4)/3, mpf(3)/5) * mpf(5)/6
eta = -log(theta)
def check(n, C=mpf(206)):
    n = mpf(n)
    a = int(ceil(2*log(n)/log(3))) + 2
    l = int(ceil(C*log(n)))
    SQ = power(3, 1 - mpf(a)/2)
    lnSP = log(mpf(6)/5) + l*(log(n) - eta*(l-1)/2)
    R = 1 + int(floor(log((n+mpf(3)/2)/(l+mpf(3)/2))/log(mpf(5)/3)))
    return a, l, R, float(SQ), float(lnSP), (SQ + exp(lnSP) < 1) and (R >= a)
print("C*eta =", 206*eta)
# worst point of block k: n = ceil(3^(k/2)) + 1  (a = k + 3 just after the step)
lastbad = None
for k in range(250, 360):
    n = int(ceil(power(3, mpf(k)/2))) + 1
    a, l, R, SQ, lnSP, ok = check(n)
    if not ok: lastbad = (k, a, l, R)
print("last failing half-integer block start: k =", lastbad, " -> n ~ 3^(k/2) =", f"3^{lastbad[0]/2}")
for k in [lastbad[0], lastbad[0]+1, lastbad[0]+2]:
    n = int(ceil(power(3, mpf(k)/2))) + 1
    print(k, check(n))
