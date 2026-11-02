#!/usr/bin/env python3
"""Referee A: numerical check of Theorem 1.2 / Proposition 7.1 and of the quoted R1-R5.

Lambda(x) = sum_{p < P(x)} log((p-1)!),  P(x) = largest prime with P(P+3) <= x  (x >= 40).
Claim: Lambda(x) >= x/2 - 3x/log x for every real x >= 40.
"""
import sys, math
import numpy as np

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10**8
BRUTE = int(sys.argv[2]) if len(sys.argv) > 2 else 10**7

sieve = np.ones(PMAX + 1, dtype=bool); sieve[:2] = False
for p in range(2, math.isqrt(PMAX) + 1):
    if sieve[p]:
        sieve[p * p::p] = False
primes = np.nonzero(sieve)[0].astype(np.int64)
print(f"primes up to {PMAX}: {len(primes)}")

lg = np.array([math.lgamma(float(p)) for p in primes])     # log((p-1)!)
# Lam_before[i] = sum_{k<i} log((p_k - 1)!)  = Lambda when P = primes[i]
Lam_before = np.concatenate(([0.0], np.cumsum(lg)))[:-1]

# ---- interval check: on [P(P+3), P'(P'+3)) Lambda = Lam_before[idx(P)], RHS increasing for x>=e^6
i0 = int(np.searchsorted(primes, 5))
P = primes[i0:-1]; Pn = primes[i0 + 1:]
Lam = Lam_before[i0:-1]
X = (Pn * (Pn + 3)).astype(np.float64)       # right endpoint (sup of interval)
Xl = (P * (P + 3)).astype(np.float64)
rhs = X / 2 - 3 * X / np.log(X)
viol = np.nonzero(Lam < rhs)[0]
print(f"interval check, P from 5 to {int(P[-1])} (X up to {X[-1]:.3e}): violations = {len(viol)}")
if len(viol):
    for k in viol[:10]:
        print("   VIOLATION", int(P[k]), int(Pn[k]), Lam[k], rhs[k])
# normalised gap (X/2 - Lam) log X / X, which must stay <= 3; paper says max 2.587 at X=928
g = (X / 2 - Lam) * np.log(X) / X
sel = X >= math.exp(6)
k = int(np.argmax(np.where(sel, g, -1e9)))
print(f"max (X/2-Lambda) logX/X over intervals with X>=e^6: {g[k]:.4f} at X={int(X[k])} (P={int(P[k])}, P'={int(Pn[k])})")
for lo in (1e4, 1e6, 1e8, 1e10, 1e12):
    s2 = X >= lo
    if s2.any():
        kk = int(np.argmax(np.where(s2, g, -1e9)))
        print(f"   over X>={lo:.0e}: max {g[kk]:.4f} at X={int(X[kk])}")
# small-x region: e^6 is about 403.4; RHS<0 there
print(f"RHS at x=403: {403/2-3*403/math.log(403):.3f}, at x=404: {404/2-3*404/math.log(404):.3f}")

# ---- brute force over every integer 40 <= x <= BRUTE, P(x) computed independently
def P_of(x):
    y = (math.isqrt(4 * x + 9) - 3) // 2 + 2
    while y * (y + 3) > x:
        y -= 1
    # largest prime <= y
    i = int(np.searchsorted(primes, y, side="right")) - 1
    return i
worst = (-1e9, None)
viol_b = 0
i = int(np.searchsorted(primes, 5))
pl = [int(v) for v in primes[: int(np.searchsorted(primes, math.isqrt(BRUTE) + 10)) + 2]]
for x in range(40, BRUTE + 1):
    while pl[i + 1] * (pl[i + 1] + 3) <= x:
        i += 1
    assert pl[i] * (pl[i] + 3) <= x < pl[i + 1] * (pl[i + 1] + 3)
    lam = Lam_before[i]
    r = x / 2 - 3 * x / math.log(x)
    if lam < r:
        viol_b += 1
    if x >= 404:
        v = (x / 2 - lam) * math.log(x) / x
        if v > worst[0]:
            worst = (v, x)
print(f"brute force every integer 40..{BRUTE}: violations={viol_b}; worst normalised gap {worst[0]:.4f} at x={worst[1]}")

# ---- Table 2 cross-check (Lambda/x)
for xx in [10**4, 10**6, 10**8, 10**10, 10**12]:
    i = P_of(xx) if xx <= PMAX * PMAX else None
    if i is not None and primes[i] < primes[-1]:
        print(f"  Table2 x={xx}: P(x)={int(primes[i])}  Lambda/x={Lam_before[i]/xx:.4f}")

# ---- intermediate inequality of the analytic proof at right endpoints with y > 563
s3 = (Pn > 563)
yv = Pn[s3].astype(np.float64); Lv = Lam[s3]; Xv = X[s3]
ly = np.log(yv)
mid = yv**2 / 2 - 5 * yv**2 / (4 * ly) - 2 * yv**2 / ly**2 - yv * (1.377 + ly) - 50
print(f"Lambda > y^2/2 - 5y^2/(4log y) - 2y^2/log^2 y - y(1.377+log y) - 50 at y=P' in (563,{int(Pn[-1])}]: violations={int((Lv <= mid).sum())}")
LL = np.log(Xv)
fin = Xv / 2 - Xv / LL * (2.5 + 8 / LL + LL / np.sqrt(Xv) * (2.877 + LL / 2) + 50 * LL / Xv)
print(f"Lambda > x/2 - (x/L)(2.5+8/L+L/sqrt x(2.877+L/2)+50L/x): violations={int((Lv <= fin).sum())}")

# ---- quoted Rosser-Schoenfeld inequalities, checked at the extremal points (just below / at primes)
pf = primes.astype(np.float64)
pi_at = np.arange(1, len(primes) + 1, dtype=np.float64)          # pi(p)
theta_at = np.cumsum(np.log(pf))                                    # theta(p)
recip_at = np.cumsum(1.0 / pf)                                      # sum_{q<=p} 1/q
B = 0.2614972128476428
eps = 1e-9
tm = pf - eps                                                       # just below p
pi_m = pi_at - 1; th_m = theta_at - np.log(pf); rc_m = recip_at - 1 / pf
# R1: pi(t) > t/log t for t>=17 ; worst just below primes
s = tm >= 17
print("R1 violations:", int((pi_m[s] <= tm[s] / np.log(tm[s])).sum()))
# R2: pi(t) < t/log t (1+3/(2log t)) and < 1.25506 t/log t, t>1 ; worst at primes
s = pf > 1
lt = np.log(pf)
print("R2a violations:", int((pi_at >= pf / lt * (1 + 1.5 / lt)).sum()), " R2b violations:", int((pi_at >= 1.25506 * pf / lt).sum()))
# R3: theta(t) > t(1-1/(2log t)) for t>=563 ; worst just below primes
s = tm >= 563
print("R3 violations:", int((th_m[s] <= tm[s] * (1 - 1 / (2 * np.log(tm[s])))).sum()))
# R4: theta(t) < t(1+1/(2log t)) t>1 and theta < 1.01624 t ; worst at primes
print("R4a violations:", int((theta_at >= pf * (1 + 1 / (2 * lt))).sum()), " R4b violations:", int((theta_at >= 1.01624 * pf).sum()))
# R5: lower for t>1 (worst just below primes), upper for t>=286 (worst at primes)
s = tm > 1.5
lo5 = np.log(np.log(tm[s])) + B - 1 / (2 * np.log(tm[s])**2)
print("R5 lower violations:", int((rc_m[s] <= lo5).sum()))
s = pf >= 286
up5 = np.log(np.log(pf[s])) + B + 1 / (2 * np.log(pf[s])**2)
print("R5 upper violations:", int((recip_at[s] >= up5).sum()))
# negative control on the R-checker: a deliberately wrong constant must produce violations
print("NEG CONTROL R2b with 1.2 instead of 1.25506 (expect >0):", int((pi_at >= 1.2 * pf / lt).sum()))
s5 = pf >= 2
up5n = np.log(np.log(pf[s5])) + B + 1 / (2 * np.log(pf[s5])**2)
print("NEG CONTROL R5 upper with threshold 2 instead of 286 (expect >0):", int((recip_at[s5] >= up5n).sum()))
print("NEG CONTROL R3 with threshold 2 instead of 563 (expect >0):", int((th_m[tm >= 2] <= tm[tm >= 2] * (1 - 1 / (2 * np.log(tm[tm >= 2])))).sum()))
