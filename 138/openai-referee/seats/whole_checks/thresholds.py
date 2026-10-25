#!/usr/bin/env python3
"""Every 'for sufficiently large k' inequality of the paper, evaluated with the
paper's own explicit bounds (log lambda <= h0 log 2M; q <= 2k^2 k^{ck/D};
R <= (D+1) log q; T_glob <= [9(3k^2F+1)^2]^{2D}; C_0 = 9*16005^2, C = C_0^{1/3};
arrangement constant in dim 3: 16(s+1)^3 <= 128 s^3).
Reports, for each inequality, the last k (on a grid) at which it FAILS and
checks it holds on the whole grid beyond that, up to k = 10^300.
No quantity depends on r or on the progression: r never appears below."""
import math, sys

def iroot_floor(n, e):
    # integer Newton: largest x with x**e <= n
    if n < 2: return n
    x = 1 << ((n.bit_length() + e - 1) // e)
    while True:
        y = ((e - 1) * x + n // x ** (e - 1)) // e
        if y >= x: break
        x = y
    while x ** e > n: x -= 1
    while (x + 1) ** e <= n: x += 1
    return x

def iroot_ceil(n, e):
    # smallest x with x**e >= n
    x = iroot_floor(n, e)
    return x if x ** e == n else x + 1

c, delta, gamma = 1e-5, 0.1, 0.01
C0 = 9 * 16005 ** 2
Ccl = C0 ** (1 / 3)          # count:local constant
LN2 = math.log(2)

def logaddexp(a, b):
    m = max(a, b); return m + math.log(math.exp(a - m) + math.exp(b - m))

def params(k):
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); h0 = D * D
    lk = math.log(k)
    loglam = h0 * math.log(2 * M)                    # setup:dilation bound
    logq = (c * k / D) * lk + math.log(2 * k * k)    # setup:q-bounds upper
    R = (D + 1) * logq                               # mesh:width
    logm = logaddexp(2 * lk + math.log(R), 0.0)      # m <= k^2 R + 1
    logF = logaddexp(2 * lk + loglam, math.log(2) + logm)
    log3k2F1 = logaddexp(math.log(3) + 2 * lk + logF, 0.0)
    logTglob = 2 * D * (math.log(9) + 2 * log3k2F1)  # count:global
    return D, M, h0, lk, loglam, logq, logTglob

def ineqs(k):
    D, M, h0, lk, loglam, logq, logTglob = params(k)
    H = 1.0 / k ** 2 if k < 10 ** 150 else 0.0
    eta = 1 / (1000 * D)
    out = {}
    out['S1 h0<2M<k (sec2 l.21)'] = h0 < 2 * M < k
    out['S2 prime: k^2 log4 - log(2k^2+1) > k log(2k^2)'] = (k * k * math.log(4) - math.log(2 * k * k + 1) > k * math.log(2 * k * k)) if k < 10**100 else (math.exp(lk) * math.log(4) - (math.log(3) + 2 * lk) / math.exp(lk) > LN2 + 2 * lk)
    out['S3 h0<k (gcd(lambda,q)=1)'] = h0 < k
    out['S4 alpha<=1/4, R>=1, H<=1 (mesh:width)'] = (logq > 0) and k >= 1
    out['S6 H<=1/8 and 3w<=6H<1 (mesh:neighbors)'] = k * k >= 8
    out['C2 6H<1, 4H<1 (count:local ranges)'] = k * k > 6
    out['O1+O4 incident weight <= 1/500'] = None   # filled below
    first_log = lk + logTglob - (delta * float(M) - 1) / 32
    out['O1 first-family total kTglob e^{-(dM-1)/32} <= 1/1000'] = first_log < math.log(1 / 1000)
    out['O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})'] = 6 * math.log(Ccl * D ** 3) / D <= 1 / 128
    sec_log = -(h0 + 1) / 128 - math.log(1 - math.exp(-1 / 128))
    out['O4 sum_{h>D^2} e^{-h/128} <= 1/1000'] = sec_log < math.log(1 / 1000)
    out['O1+O4 incident weight <= 1/500'] = out['O1 first-family total kTglob e^{-(dM-1)/32} <= 1/1000'] and out['O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})'] and out['O4 sum_{h>D^2} e^{-h/128} <= 1/1000']
    out['O5 l(E)>=100: dM-1>=100 and (D^2+1)/2>=100'] = (delta * M - 1 >= 100) and ((h0 + 1) / 2 >= 100)
    out['O2 log(CDh)/h decreasing for h>=D^2 (CD^3>e)'] = Ccl * D ** 3 > math.e
    out['D1 2kH<1 (affinity)'] = 2 * k < k * k
    out['D2 m*-1>=k/(2M) (needs k>=2M)'] = k >= 2 * M
    out['D3 6MH/k<1 (v=lambda u)'] = 6 * M < k ** 3
    out['D4 4MH<1 ((1-2MH)/2M > H)'] = 4 * M < k * k
    out['D5 2H+4MH<1 (heavy-width)'] = 2 + 4 * M < k * k
    out['D7 4MH < 1/2 (short-motion, h>=1)'] = 8 * M < k * k
    out['D8 2H(k+1)<1 (short width)'] = 2 * (k + 1) < k * k
    out['D10 4MH/k < eta (long, drift<eta)'] = 4 * M * 1000 * D < k ** 3
    out['D11 D(4eta+1/h0)<1/2'] = 4 / 1000 + 1 / D < 0.5
    out['D12 2M<=k and 4M<=k (|u|<=Hx,|v|<=H)'] = 4 * M <= k
    out['D13 2M/k<=1/16'] = 32 * M <= k
    out['D14 k-h-dk>=4k/5 (h<=2M<=k/10)'] = 20 * M <= k
    out['P1 p<1/2 (k^{1/20}>2)'] = k > 2 ** 20
    logR = LN2 + 2 * D * logq - (gamma / 80) * math.exp(lk) * lk
    logA = LN2 + math.log(128) + logTglob + 3 * (lk + math.log(3 * D) + 2 * logq) - math.exp(0.95 * lk) / 4
    out['P2r rich: log R_k < log(1/2)'] = logR < -LN2
    out['P2a affine: log A_k < log(1/2)'] = logA < -LN2
    return out

# exact scan for small k, grid scan beyond
names = list(ineqs(10 ** 7).keys())
last_fail = {n: None for n in names}
for k in range(3, 20001):
    for n, v in ineqs(k).items():
        if not v: last_fail[n] = k
x = 4.30
while x <= 300:
    k = int(10 ** x) if x < 15 else int(round(10 ** (x - 15))) * 10 ** 15
    for n, v in ineqs(k).items():
        if not v: last_fail[n] = k
    x += 0.01
w = max(len(n) for n in names)
print(f"{'inequality':<{w}}  last failing k on grid (k=3..2e4 exact, then 10^4.3..10^300 step 10^0.01)")
for n in names:
    lf = last_fail[n]
    s = 'never fails (k>=3)' if lf is None else (f'{lf}' if lf < 10 ** 7 else f'~10^{math.log10(lf):.2f}')
    print(f"{n:<{w}}  {s}")
# the binding constraint, located more finely
lo, hi = 40.0, 46.0
for _ in range(60):
    mid = (lo + hi) / 2
    k = int(round(10 ** (mid - 15))) * 10 ** 15
    if ineqs(k)['O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})']: hi = mid
    else: lo = mid
k = int(round(10 ** (hi - 15))) * 10 ** 15
print(f"O3 threshold: k ~ 10^{hi:.3f}, D = {params(k)[0]}, C = {Ccl:.1f}")
