"""Seat C: recompute Table 2 (Lambda(x)/x, |S_x|/x, Upsilon(x)/(x log x)) and Table 3 (|U_x| etc.)
Definitions (paper Sections 1, 2, 3, 5, 6):
  S_x = {n : 2<=n<=x, P+(n) <= sqrt(x)};  Upsilon(x) = sum_{n in S_x} log(n+1)
  Lambda(x) = sum_{p < P(x)} log((p-1)!), P(x) = largest prime with P(P+3) <= x
  top(n) = largest prime-power component; n balanced iff top(n)^2 <= n (top <= sqrt n); U_x = unbalanced elements of S_x
"""
import numpy as np, math, sys
N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
NU = int(float(sys.argv[2])) if len(sys.argv) > 2 else 10**7
# greatest prime factor sieve up to N
gpf = np.zeros(N + 1, dtype=np.int32)
is_comp = np.zeros(N + 1, dtype=bool)
r = math.isqrt(N)
for p in range(2, r + 1):
    if not is_comp[p]:
        is_comp[p*p::p] = True
primes = np.nonzero(~is_comp[2:])[0] + 2
for p in primes:   # ascending: last write = largest prime factor
    gpf[p::p] = p
print('sieve done, primes up to N:', len(primes), flush=True)
def lgfact(m):  # log(m!)
    return math.lgamma(m + 1)
plist = primes.tolist()
print('Table 2 (left): x, P(x), Lambda(x)/x')
for e in (4, 6, 8, 10, 12):
    x = 10**e
    y = (math.isqrt(4*x + 9) - 3) // 2 + 2
    # largest prime P with P(P+3) <= x (P <= y ~ 1e6, within sieve)
    P = max(p for p in plist if p <= y + 5 and p*(p+3) <= x)
    Lam = sum(lgfact(p - 1) for p in plist if p < P)
    print('  1e%d  P=%d  Lambda/x=%.4f' % (e, P, Lam / x))
print('Table 2 (right): x, |S_x|/x, Upsilon/(x log x)')
for e in (3, 4, 5, 6, 8):
    x = 10**e
    if x > N: continue
    s = math.isqrt(x)
    mask = gpf[2:x+1] <= s
    cnt = int(np.count_nonzero(mask))
    ns = np.nonzero(mask)[0] + 2
    Ups = float(np.sum(np.log1p(ns.astype(np.float64))))
    print('  1e%d  |S_x|=%d  |S_x|/x=%.4f  Upsilon/(x log x)=%.4f' % (e, cnt, cnt / x, Ups / (x * math.log(x))))
# Table 3: top(n) up to NU
top = np.ones(NU + 1, dtype=np.int64)
for p in plist:
    if p > NU: break
    q = p
    while q <= NU:
        top[q::q] = np.maximum(top[q::q], q)
        q *= p
print('Table 3: x, |U_x|, |U_x| log x/x, sum_{U_x} log(n+1)/x')
for e in (3, 4, 5, 6, 7):
    x = 10**e
    if x > NU: continue
    s = math.isqrt(x)
    n = np.arange(2, x + 1, dtype=np.int64)
    inS = gpf[2:x+1] <= s
    unb = top[2:x+1] * top[2:x+1] > n
    U = n[inS & unb]
    print('  1e%d  |U_x|=%d  %.4f  %.4f' % (e, len(U), len(U) * math.log(x) / x, float(np.sum(np.log1p(U.astype(np.float64)))) / x))
# smallest balanced integer
nb = [m for m in range(2, 1000) if top[m] * top[m] <= m]
print('smallest balanced integers:', nb[:10])
