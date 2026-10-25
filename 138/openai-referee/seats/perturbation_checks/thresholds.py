#!/usr/bin/env python3
"""Arithmetic of Theorem perturb:cyclic and the 'sufficiently large k'
inequalities of Section 6, evaluated with the paper's literal parameters.

(1) exact: 2c - gamma/80 with c = 1e-5, gamma = 1/100  (perturb:negative-coefficient)
(2) p = k^(-1/20) < 1/2                       iff k > 2^20
(3) R_k bound  log R_k <= (2c-g/80) k log k + 2D log(2k^2) + log 2   (perturb:rich-bound)
(4) A_k bound  log A_k <= log 2 + log C_arr + log T_glob + 3 log(k(Dq^2+2)) - pk/4
    with C_arr = 128 (count:arrangement, e=3: 16(s+1)^3 <= 128 s^3),
    T_glob <= [9(3k^2F+1)^2]^{2D}, F = k^2 lambda + 2m (count:global),
    m = ceil(k^2 R), R = log(1 + q^{D+1}/2), and the WORST admissible q,
    log q <= (ck/D) log k + log(2k^2)        (setup:q-bounds)
All logs natural; lambda computed exactly (as a log).
Usage: thresholds.py [control]   ('control' sets c = 1/10000 > gamma/160: rich bound must fail)"""
import sys, math
from fractions import Fraction as Fr
c = Fr(1, 100000); g = Fr(1, 100)
if len(sys.argv) > 1 and sys.argv[1] == "control": c = Fr(1, 10000)
coef = 2 * c - g / 80
print("2c - gamma/80 =", coef, "  (1/50000 - 1/8000 =", Fr(1, 50000) - Fr(1, 8000), ")")
def iroot_ceil(k, r):
    x = max(1, int(round(k ** (1.0 / r))) - 2)
    while x ** r < k: x += 1
    while x > 1 and (x - 1) ** r >= k: x -= 1
    return x
def primes_upto(n):
    return [l for l in range(2, n + 1) if all(l % r for r in range(2, int(l ** 0.5) + 1))]
def params(k):
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); h0 = D * D
    loglam = 0.0
    for l in primes_upto(h0):
        a = 0
        while l ** (a + 1) <= 2 * M: a += 1
        loglam += a * math.log(l)
    return D, M, h0, loglam
def logR(k):
    D, M, h0, _ = params(k); L = math.log(k)
    return float(coef) * k * L + 2 * D * math.log(2 * k * k) + math.log(2)
def logA(k):
    D, M, h0, loglam = params(k); L = math.log(k)
    logq = float(c) * k / D * L + math.log(2 * k * k)          # worst admissible q
    R = (D + 1) * logq                                         # log(1+q^{D+1}/2) <= (D+1) log q
    logm = 2 * L + math.log(R + 1)                              # m <= k^2 R + 1
    logF = max(2 * L + loglam, logm + math.log(2)) + math.log(2)  # F <= 2 max(k^2 lambda, 2m)
    logTg = 2 * D * (math.log(9) + 2 * (math.log(3) + 2 * L + logF + 1e-9) + math.log(2))
    p = k ** (-1 / 20)
    return math.log(2) + math.log(128) + logTg + 3 * (L + math.log(3) + math.log(D) + 2 * logq) - p * k / 4
print("p < 1/2 iff k > 2^20 =", 2 ** 20, "; check p(2^20) =", (2 ** 20) ** (-1 / 20))
# scan: every D-jump point j^10+1 and a geometric grid, from 2^20 to 1e18
pts = set()
for j in range(4, 64):
    for kk in (j ** 10, j ** 10 + 1, j ** 10 + 2):
        if 2 ** 20 <= kk <= 10 ** 18: pts.add(kk)
x = 2.0 ** 20
while x <= 1e18: pts.add(int(x)); x *= 1.05
pts = sorted(pts)
worstR = max(logR(k) for k in pts); worstA = max(logA(k) for k in pts)
print(f"scanned {len(pts)} values of k in [2^20, 1e18]: max log R_k bound = {worstR:.1f}, max log A_k bound = {worstA:.1f} "
      f"(need both < log(1/2) = {math.log(0.5):.3f})")
for k in (2 ** 20, 10 ** 7, 10 ** 9, 10 ** 12):
    print(f"  k={k:>14}: D,M,h0={params(k)[:3]}, log lambda={params(k)[3]:.1f}, logR<={logR(k):.4g}, logA<={logA(k):.4g}")
# where does the rich bound first go below log(1/2)? (smallest k on a fine scan)
k = 2
while logR(k) >= math.log(0.5) and k < 10 ** 12: k = int(k * 1.01) + 1
print("rich bound < 1/2 from about k =", k if k < 10 ** 12 else "never below 1e12")
ok = worstR < math.log(0.5) and worstA < math.log(0.5)
print("Section-6 union bounds R_k + A_k < 1 on the whole scanned range:", "YES" if ok else "NO")
sys.exit(0 if ok else 1)
