#!/usr/bin/env python3
"""Referee A: numerical check of Theorem 1.5 / Proposition 7.2.

Upsilon(x) = sum_{n in S_x} log(n+1),  S_x = {2<=n<=x : P^+(n) <= sqrt(x)}.
Claim: Upsilon(x) <= (1-log 2) x log x + 1.5 x for all x >= 2.
Upsilon depends only on floor(x) and the RHS increases, so integers suffice.

n is in S_x iff x >= t(n) := max(n, P^+(n)^2).  So Upsilon(x) = sum_{t(n)<=x} log(n+1),
computed by bucketing on t(n) and a cumulative sum.  Independent of the paper's formula (7),
which we then check against a direct count as a cross-check.
"""
import sys, math
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**7

# largest prime factor sieve
lpf = np.zeros(N + 1, dtype=np.int64)
is_comp = np.zeros(N + 1, dtype=bool)
for p in range(2, N + 1):
    if p * p > N:
        break
    if not is_comp[p]:
        is_comp[p * p::p] = True
primes = np.nonzero(~is_comp[2:])[0] + 2
for p in primes:            # ascending: last write = largest prime factor
    lpf[p::p] = p
n = np.arange(N + 1, dtype=np.int64)
t = np.maximum(n, lpf * lpf)
mask = (n >= 2) & (t <= N)
tb = t[mask]
w = np.log(n[mask].astype(np.float64) + 1.0)
cnt = np.cumsum(np.bincount(tb, minlength=N + 1)).astype(np.int64)      # |S_x|
ups = np.cumsum(np.bincount(tb, weights=w, minlength=N + 1))              # Upsilon(x)

x = np.arange(N + 1, dtype=np.float64)
c = 1.0 - math.log(2.0)
xs = x[2:]
ratio = (ups[2:] - c * xs * np.log(xs)) / xs
i = int(np.argmax(ratio))
print(f"N={N}")
print(f"max (Ups - (1-log2) x log x)/x over 2<=x<=N: {ratio[i]:.6f} at x={i+2}  (claim <= 1.5; paper says 0.542 at x=50)")
print(f"any violation of <=1.5: {bool((ratio > 1.5).any())}")
# where is the ratio largest beyond small x
for lo in (1000, 10**4, 10**5, 10**6, 81796):
    if lo < N:
        j = int(np.argmax(ratio[lo - 2:])) + lo
        print(f"  max ratio over x>={lo}: {ratio[j-2]:.6f} at x={j}")

# cross-check |S_x| against formula (7) at a few points, using exact integer arithmetic
def S_formula(X):
    r = math.isqrt(X)
    s = X - 1
    for p in primes:
        if p > X:
            break
        if p > r or (p * p > X):
            s -= X // int(p)
    return s
for X in [2, 3, 10, 24, 25, 50, 100, 1000, 12345, 81796, min(N, 10**6), N]:
    if X <= N:
        print(f"  |S_{X}| bucket={cnt[X]} formula(7)={S_formula(X)}")

# Table 2 cross-check
for X in [10**3, 10**4, 10**5, 10**6, 10**7, 10**8]:
    if X <= N:
        print(f"  Table2 x={X}: |S_x|/x={cnt[X]/X:.4f}  Ups/(x log x)={ups[X]/(X*math.log(X)):.4f}")

# intermediate inequalities of the analytic proof for x >= 286^2 (sanity, not proof)
lo = 81796
if N > lo:
    X = x[lo:]
    L = np.log(X)
    rhs_S = c * X + 1.25506 * X / L + 2.5 * X / L**2 - 1
    bad_S = np.nonzero(cnt[lo:] >= rhs_S)[0]
    rhs_U = c * X * L + 1.477 * X
    bad_U = np.nonzero(ups[lo:] >= rhs_U)[0]
    gapS = (rhs_S - cnt[lo:]) / X
    print(f"  |S_x| < (1-log2)x+1.25506x/L+2.5x/L^2-1 on [{lo},{N}]: violations={len(bad_S)}, min slack/x={gapS.min():.5f}")
    print(f"  Ups < (1-log2)xL+1.477x on [{lo},{N}]: violations={len(bad_U)}, min slack/x={((rhs_U-ups[lo:])/X).min():.5f}")
