
## 9. Finite checks (scripts VERBATIM, outputs, failing controls)

All under `/tmp/oaimath/160/seats/whole_checks/`. Run with `python3 -I`. Each takes under 7 s and under 100 MB.

### 9.1 thresholds.py — every large-k inequality with the paper's explicit constants (feeds §4)

```python
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
```

Output:
```
inequality                                             last failing k on grid (k=3..2e4 exact, then 10^4.3..10^300 step 10^0.01)
S1 h0<2M<k (sec2 l.21)                                 6
S2 prime: k^2 log4 - log(2k^2+1) > k log(2k^2)         never fails (k>=3)
S3 h0<k (gcd(lambda,q)=1)                              4
S4 alpha<=1/4, R>=1, H<=1 (mesh:width)                 never fails (k>=3)
S6 H<=1/8 and 3w<=6H<1 (mesh:neighbors)                never fails (k>=3)
C2 6H<1, 4H<1 (count:local ranges)                     never fails (k>=3)
O1+O4 incident weight <= 1/500                         ~10^44.65
O1 first-family total kTglob e^{-(dM-1)/32} <= 1/1000  ~10^22.70
O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})     ~10^44.65
O4 sum_{h>D^2} e^{-h/128} <= 1/1000                    ~10^15.78
O5 l(E)>=100: dM-1>=100 and (D^2+1)/2>=100             ~10^11.46
O2 log(CDh)/h decreasing for h>=D^2 (CD^3>e)           never fails (k>=3)
D1 2kH<1 (affinity)                                    never fails (k>=3)
D2 m*-1>=k/(2M) (needs k>=2M)                          5
D3 6MH/k<1 (v=lambda u)                                never fails (k>=3)
D4 4MH<1 ((1-2MH)/2M > H)                              never fails (k>=3)
D5 2H+4MH<1 (heavy-width)                              3
D7 4MH < 1/2 (short-motion, h>=1)                      4
D8 2H(k+1)<1 (short width)                             never fails (k>=3)
D10 4MH/k < eta (long, drift<eta)                      38
D11 D(4eta+1/h0)<1/2                                   1024
D12 2M<=k and 4M<=k (|u|<=Hx,|v|<=H)                   19
D13 2M/k<=1/16                                         1055
D14 k-h-dk>=4k/5 (h<=2M<=k/10)                         419
P1 p<1/2 (k^{1/20}>2)                                  1047128
P2r rich: log R_k < log(1/2)                           154881
P2a affine: log A_k < log(1/2)                         7238
O3 threshold: k ~ 10^44.655, D = 29210, C = 1321.0
```

Control: `cap_check.py` (§9.4) is the failing control for this machinery. With c = 7×10⁻⁵ the rich inequality P3 fails at every k. Within this run, S1/S3/D2/D5/D7/D10–D14/P1–P4 visibly FAIL below their thresholds, so the predicates can fail.

### 9.2 digit_product_check.py — Prop transfer:product (7.1) by brute force

```python
#!/usr/bin/env python3
"""Brute-force check of Prop transfer:product (07-transfers.tex) on tiny cyclic colourings.
(1) find 2-colourings C of Z/NZ with no monochromatic a, a+d, ..., a+(k-1)d (d != 0 mod N,
    wrap-around allowed, repeated terms allowed) -- the hypothesis of the proposition;
(2) build the digit-product colouring n -> (C(floor(n/N^i) mod N))_{i<m} of [0, N^m) and
    brute-force every progression a, a+d, ..., a+(k-1)d with d >= 1 inside [0, N^m);
CONTROL A (must FAIL): a colouring of Z/NZ that avoids every NON-wrapping k-AP in {0..N-1}
    but has a wrapping cyclic mono k-AP; its digit product must contain a mono k-AP.
CONTROL B (must FAIL): identity (transfer:division) with N^i NOT dividing d.
EXTERNAL CONTROL: W_2(3) = 9, so no cyclic 3-AP-free 2-colouring of Z/9Z ... Z/12Z may exist."""
import itertools, random, sys

def cyclic_avoids(C, N, k):
    for a in range(N):
        for d in range(1, N):
            c0 = C[a]
            if all(C[(a + j * d) % N] == c0 for j in range(1, k)):
                return False
    return True

def interval_avoids(col, L, k):
    for a in range(L):
        for d in range(1, (L - 1 - a) // (k - 1) + 1 if k > 1 else 1):
            c0 = col[a]
            if all(col[a + j * d] == c0 for j in range(1, k)):
                return (a, d)
    return None

def digit_colour(C, N, m):
    out = []
    for n in range(N ** m):
        out.append(tuple(C[(n // N ** i) % N] for i in range(m)))
    return out

def search(N, k, limit=4):
    found = []
    for bits in range(1 << (N - 1)):          # fix C[0]=0 (colour swap symmetry)
        C = [0] + [(bits >> i) & 1 for i in range(N - 1)]
        if cyclic_avoids(C, N, k):
            found.append(C)
            if len(found) >= limit: break
    return found

print("EXTERNAL CONTROL (W_2(3)=9): cyclic 3-AP-free 2-colourings of Z/NZ, N=3..12:")
for N in range(3, 13):
    print(f"  N={N}: {'some' if search(N, 3, 1) else 'none'}")

for (N, k, ms) in [(3, 3, (1, 2, 3, 4, 5)), (4, 3, (1, 2, 3, 4)), (11, 4, (1, 2, 3))]:
    cols = search(N, k, 2)
    if not cols:
        print(f"N={N},k={k}: no cyclic avoiding colouring found"); continue
    C = cols[0]
    for m in ms:
        bad = interval_avoids(digit_colour(C, N, m), N ** m, k)
        print(f"N={N},k={k},C={''.join(map(str,C))},m={m}: interval [0,{N**m}) with 2^{m} colours: "
              f"{'NO mono k-AP (W_{2^m}(k) > N^m)' if bad is None else 'MONO AP FOUND ' + str(bad)}")

print("\nCONTROL A: colourings avoiding all NON-wrapping k-APs on {0..N-1} but not cyclically:")
for (N, k) in [(8, 3), (16, 4)]:
    ctrl = None
    for bits in range(1 << (N - 1)):
        C = [0] + [(bits >> i) & 1 for i in range(N - 1)]
        if interval_avoids(C, N, k) is None and not cyclic_avoids(C, N, k):
            ctrl = C; break
    if ctrl is None:
        print(f"  N={N},k={k}: none found"); continue
    for m in (2,):
        bad = interval_avoids(digit_colour(ctrl, N, m), N ** m, k)
        print(f"  N={N},k={k},C={''.join(map(str,ctrl))},m={m}: digit product "
              f"{'has NO mono AP (control did not fail!)' if bad is None else 'has mono k-AP (a,d)=' + str(bad) + '  [control FAILS as it must]'}")

print("\nIdentity (transfer:division): floor((a+jd)/N^i) == floor(a/N^i) + j*d/N^i")
random.seed(1)
ok = bad = 0
for _ in range(20000):
    N = random.randint(2, 12); i = random.randint(0, 3); e = random.randint(1, 50)
    d = N ** i * e; a = random.randint(0, 10 ** 6); j = random.randint(0, 40)
    ok += ((a + j * d) // N ** i == a // N ** i + j * e)
print(f"  N^i | d: {ok}/20000 hold")
fails = 0
for _ in range(20000):
    N = random.randint(2, 12); i = random.randint(1, 3); d = random.randint(1, 10 ** 4)
    if d % N ** i == 0: continue
    a = random.randint(0, 10 ** 6); j = random.randint(1, 40)
    # with N^i not dividing d, j*d/N^i is not an integer for j=1: the identity cannot hold
    if (a + j * d) // N ** i * N ** i != (a // N ** i) * N ** i + j * d: fails += 1
print(f"  CONTROL B (N^i does not divide d): identity fails in {fails} random cases [must be > 0]")
```

Output:
```
EXTERNAL CONTROL (W_2(3)=9): cyclic 3-AP-free 2-colourings of Z/NZ, N=3..12:
  N=3: some
  N=4: some
  N=5: none
  N=6: none
  N=7: none
  N=8: none
  N=9: none
  N=10: none
  N=11: none
  N=12: none
N=3,k=3,C=010,m=1: interval [0,3) with 2^1 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=2: interval [0,9) with 2^2 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=3: interval [0,27) with 2^3 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=4: interval [0,81) with 2^4 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=5: interval [0,243) with 2^5 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=1: interval [0,4) with 2^1 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=2: interval [0,16) with 2^2 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=3: interval [0,64) with 2^3 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=4: interval [0,256) with 2^4 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=11,k=4,C=01110100100,m=1: interval [0,11) with 2^1 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=11,k=4,C=01110100100,m=2: interval [0,121) with 2^2 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=11,k=4,C=01110100100,m=3: interval [0,1331) with 2^3 colours: NO mono k-AP (W_{2^m}(k) > N^m)

CONTROL A: colourings avoiding all NON-wrapping k-APs on {0..N-1} but not cyclically:
  N=8,k=3,C=01011010,m=2: digit product has mono k-AP (a,d)=(0, 21)  [control FAILS as it must]
  N=16,k=4,C=0010110101001000,m=2: digit product has mono k-AP (a,d)=(0, 8)  [control FAILS as it must]

Identity (transfer:division): floor((a+jd)/N^i) == floor(a/N^i) + j*d/N^i
  N^i | d: 20000/20000 hold
  CONTROL B (N^i does not divide d): identity fails in 16340 random cases [must be > 0]
```

Controls: (A) colourings avoiding every NON-wrapping k-AP in {0..N−1} but not cyclically produce a monochromatic k-AP in the digit product. For example, N = 16, k = 4: (a,d) = (0,8), whose lowest digits 0,8,0,8 form a wrapping, repeated-term cyclic progression with step 8. This shows the cyclic hypothesis must cover every d ≠ 0, which Theorem 6.3 provides. (B) Identity (7.1) fails whenever N^i ∤ d. External control: W_2(3) = 9 forbids cyclic 3-AP-free 2-colourings of Z/NZ for N ≥ 9, and the search finds none.

### 9.3 behrend_check.py — Thm transfer:large-r (7.2) by brute force + exact sweep

```python
#!/usr/bin/env python3
"""Brute-force + exact checks of Theorem transfer:large-r (07-transfers.tex, printed Thm 7.2).
(1) For r in a list: b = floor(r^{1/4}), s = floor(log r / (4 log 2)); colour n in [0, b^s) by
    (h(x_0),...,h(x_{s-1}), sum x_i^2); check #colours used <= 2^s(1+s(b-1)^2) <= r and that NO
    colour class contains a 3-AP n, n+d, n+2d (d >= 1).
CONTROL 1 (must FAIL): halves H_0 = {0..ceil(b/2)} (diameter one larger) -> mono 3-AP expected.
CONTROL 2 (must FAIL): drop the squared-norm entry -> mono 3-AP expected.
(2) Exact arithmetic of (transfer:color-count), s >= L/(8 log 2), log b >= L/8 and
    b^s > exp(L^2/(64 log 2)) for EVERY integer r in [256, 2*10^6] and for r = 2^j, 2^j - 1,
    j <= 400 (where floors jump)."""
import math

def iroot_floor(n, e):
    if n < 2: return n
    x = 1 << ((n.bit_length() + e - 1) // e)
    while True:
        y = ((e - 1) * x + n // x ** (e - 1)) // e
        if y >= x: break
        x = y
    while x ** e > n: x -= 1
    while (x + 1) ** e <= n: x += 1
    return x

def params(r):
    b = iroot_floor(r, 4)
    s = (r.bit_length() - 1) // 4          # floor(floor(log2 r)/4) = floor(log r/(4 log 2))
    return b, s

def colouring(b, s, half_cut, with_norm=True):
    cols = []
    for n in range(b ** s):
        x, t = [], n
        for _ in range(s):
            x.append(t % b); t //= b
        hv = tuple(int(xi >= half_cut) for xi in x)
        cols.append(hv + ((sum(xi * xi for xi in x),) if with_norm else ()))
    return cols

def mono_3ap(cols):
    classes = {}
    for n, c in enumerate(cols): classes.setdefault(c, []).append(n)
    for c, mem in classes.items():
        S = set(mem)
        for i in range(len(mem)):
            for j in range(i + 1, len(mem)):
                a, z = mem[i], mem[j]
                if (a + z) % 2 == 0 and (a + z) // 2 in S:
                    return (a, (a + z) // 2, z), len(classes)
    return None, len(classes)

for r in [256, 400, 625, 1296, 2401, 4096, 6561, 10000, 65536, 100000]:
    b, s = params(r)
    hc = (b + 1) // 2                      # ceil(b/2): H_0 = {0..ceil(b/2)-1}
    bound = 2 ** s * (1 + s * (b - 1) ** 2)
    if b ** s > 300000:
        print(f"r={r}: b={b}, s={s}, b^s={b**s} too large to brute force here"); continue
    w, ncol = mono_3ap(colouring(b, s, hc))
    w1, _ = mono_3ap(colouring(b, s, hc + 1))
    w2, _ = mono_3ap(colouring(b, s, hc, with_norm=False))
    lb = math.exp(math.log(r) ** 2 / (64 * math.log(2)))
    print(f"r={r}: b={b}, s={s}, interval [0,{b**s}), colours used {ncol} <= {bound} <= r: {ncol <= bound <= r}; "
          f"mono 3-AP: {w}; claimed bound exp(L^2/64log2)={lb:.3f} < b^s: {lb < b**s} | "
          f"CONTROL1 wide halves -> {w1} | CONTROL2 no norm -> {w2}")

# (2) exact arithmetic over all r in a range and at the jump points
bad = []
def check(r):
    b, s = params(r)
    L = math.log(r)
    ok = (2 ** s * (1 + s * b * b) <= r and s >= L / (8 * math.log(2)) - 1e-12
          and math.log(b) >= L / 8 - 1e-12 and s * math.log(b) >= L * L / (64 * math.log(2)) - 1e-9
          and b >= 2 and s >= 1)
    if not ok: bad.append(r)
for r in range(256, 2_000_001):
    check(r)
for j in range(8, 401):
    for r in (2 ** j - 1, 2 ** j, 2 ** j + 1):
        if r >= 256: check(r)
for t in range(4, 10 ** 4):
    for r in (t ** 4 - 1, t ** 4):
        if r >= 256: check(r)
print(f"\nexact-arithmetic sweep r in [256, 2e6] plus jump points: failures = {bad[:10]} (count {len(bad)})")
# CONTROL 3a (must FAIL): claim the stronger constant 16 log 2 instead of 64 log 2
f3a = [r for r in range(256, 200001) if params(r)[1] * math.log(params(r)[0]) < math.log(r) ** 2 / (16 * math.log(2))]
print(f"CONTROL3a (b^s >= exp(L^2/(16 log 2)) claimed): fails at {len(f3a)} r in [256,2e5], first {f3a[:3]}")
# CONTROL 3b (must FAIL): b = floor(r^{1/3}) instead of r^{1/4} breaks (transfer:color-count)
f3b = [r for r in range(256, 200001) if 2 ** ((r.bit_length()-1)//4) * (1 + ((r.bit_length()-1)//4) * iroot_floor(r, 3) ** 2) > r]
print(f"CONTROL3b (b = floor(r^(1/3))): colour count exceeds r at {len(f3b)} r in [256,2e5], first {f3b[:3]}")
```

Output:
```
r=256: b=4, s=2, interval [0,16), colours used 14 <= 76 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=2.000 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> None
r=400: b=4, s=2, interval [0,16), colours used 14 <= 76 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=2.246 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> None
r=625: b=5, s=2, interval [0,25), colours used 21 <= 132 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=2.545 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=1296: b=6, s=2, interval [0,36), colours used 30 <= 204 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=3.183 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=2401: b=7, s=2, interval [0,49), colours used 38 <= 292 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=3.919 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=4096: b=8, s=3, interval [0,512), colours used 243 <= 1184 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=4.757 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=6561: b=9, s=3, interval [0,729), colours used 322 <= 1544 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=5.705 < b^s: True | CONTROL1 wide halves -> (46, 86, 126) | CONTROL2 no norm -> (0, 1, 2)
r=10000: b=10, s=3, interval [0,1000), colours used 435 <= 1952 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=6.768 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=65536: b=16, s=4, interval [0,65536), colours used 5124 <= 14416 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=16.000 < b^s: True | CONTROL1 wide halves -> (24, 2064, 4104) | CONTROL2 no norm -> (0, 1, 2)
r=100000: b=17, s=4, interval [0,83521), colours used 5853 <= 16400 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=19.844 < b^s: True | CONTROL1 wide halves -> (154, 298, 442) | CONTROL2 no norm -> (0, 1, 2)

exact-arithmetic sweep r in [256, 2e6] plus jump points: failures = [] (count 0)
CONTROL3a (b^s >= exp(L^2/(16 log 2)) claimed): fails at 199742 r in [256,2e5], first [257, 258, 259]
CONTROL3b (b = floor(r^(1/3))): colour count exceeds r at 142575 r in [256,2e5], first [256, 257, 258]
```

Controls: CONTROL1 (halves widened by one digit) produces a monochromatic 3-AP at r = 6561, 65536 and 100000. CONTROL2 (norm entry dropped) produces one at every tested r with b ≥ 5; at b = 4 the halves {0,1} and {2,3} happen to be 3-AP-free. CONTROL3a (claiming exp(L²/(16 log 2))) fails at 199,742 values of r. CONTROL3b (b = ⌊r^{1/3}⌋) breaks (7.3) at 142,575 values of r. The true chain has 0 failures over r ∈ [256, 2×10⁶] plus all jump points.

### 9.4 cap_check.py — which inequality caps c (brief item j)

```python
#!/usr/bin/env python3
"""Which inequality caps c (brief item j)?  Rich case: log R_k <= log2 + 2D log q - (gamma/80) k log k
with D log q <= c k log k + D log(2k^2)  =>  needs 2c < gamma/80, i.e. c < gamma/160 = 6.25e-5.
Affine case: log T_aff ~ 6 log q ~ 6 (c k/D) log k = o(p k) for EVERY fixed c (D ~ k^{1/10} > k^{1/20}).
CONTROL (must FAIL): c = 7e-5 > gamma/160 -> rich bound positive at every large k."""
import math
gamma = 0.01
def logR(k_log10, c):
    lk = k_log10 * math.log(10); k = math.exp(lk)
    D = math.ceil(math.exp(lk / 10))
    logq = (c * k / D) * lk + math.log(2) + 2 * lk
    return math.log(2) + 2 * D * logq - (gamma / 80) * k * lk
def logAff_main(k_log10, c):   # 6 log q - pk/4 (dominant c-dependent part of log A_k)
    lk = k_log10 * math.log(10); k = math.exp(lk)
    D = math.ceil(math.exp(lk / 10))
    logq = (c * k / D) * lk + math.log(2) + 2 * lk
    return 6 * logq - math.exp(0.95 * lk) / 4
for c in (1e-5, 6e-5, 6.2e-5, 7e-5, 1e-3):
    row = [f"{logR(x, c):+.3e}" for x in (6, 10, 50, 100, 300)]
    aff = [f"{logAff_main(x, c):+.3e}" for x in (6, 10, 50, 100, 300)]
    print(f"c={c:g}: 2c-gamma/80={2*c-gamma/80:+.3e}; log R_k at k=10^6,10^10,10^50,10^100,10^300: {row}")
    print(f"        affine main term 6log q - pk/4 at same k: {aff}")
```

Output:
```
c=1e-05: 2c-gamma/80=-1.050e-04; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['-1.223e+03', '-2.418e+07', '-1.209e+48', '-2.418e+98', '-7.253e+298']
        affine main term 6log q - pk/4 at same k: ['-1.249e+05', '-7.893e+08', '-7.905e+46', '-2.500e+94', '-2.500e+284']
c=6e-05: 2c-gamma/80=-5.000e-06; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+1.582e+02', '-1.150e+06', '-5.756e+46', '-1.151e+97', '-3.454e+297']
        affine main term 6log q - pk/4 at same k: ['-1.239e+05', '-7.830e+08', '-7.902e+46', '-2.500e+94', '-2.500e+284']
c=6.2e-05: 2c-gamma/80=-1.000e-06; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+2.135e+02', '-2.292e+05', '-1.151e+46', '-2.303e+96', '-6.908e+296']
        affine main term 6log q - pk/4 at same k: ['-1.238e+05', '-7.828e+08', '-7.901e+46', '-2.500e+94', '-2.500e+284']
c=7e-05: 2c-gamma/80=+1.500e-05; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+4.345e+02', '+3.455e+06', '+1.727e+47', '+3.454e+97', '+1.036e+298']
        affine main term 6log q - pk/4 at same k: ['-1.237e+05', '-7.818e+08', '-7.901e+46', '-2.500e+94', '-2.500e+284']
c=0.001: 2c-gamma/80=+1.875e-03; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+2.613e+04', '+4.317e+08', '+2.159e+49', '+4.317e+99', '+1.295e+300']
        affine main term 6log q - pk/4 at same k: ['-1.044e+05', '-6.650e+08', '-7.837e+46', '-2.500e+94', '-2.500e+284']
```

Control: c = 7e-5 and c = 1e-3 give log R_k > 0 at every k shown (the rich bound FAILS as it must). The affine term stays negative for every c, so the cap 2c < γ/80 is the only one.

### 9.5 upper_check.py — Thm A.1 boundary values and W ≤ F

```python
#!/usr/bin/env python3
"""Theorem upper:finite (printed Thm A.1): compute F(r,k) from (A.1) literally and compare with
brute-force W_r(k) on tiny cases; check the boundary values W_r(1)=1, W_r(2)=r+1, W_1(k)=k.
W uses the paper's 1-based definition: least N such that every map [N]->[r] is constant on
some a, a+d, ..., a+(k-1)d with a,d >= 1, a+(k-1)d <= N.
CONTROL (must FAIL): the claim W_r(2) = r is rejected by the same brute force."""
import itertools
from functools import lru_cache

@lru_cache(None)
def F(r, k):
    if k == 1: return 1
    if k == 2: return r + 1
    m = 1
    for _ in range(r):
        m = 2 * m * F(r ** m, k - 1)
    return m

def has_mono(col, k):            # col: tuple indexed 1..N via col[n-1]
    N = len(col)
    for a in range(1, N + 1):
        for d in range(1, N + 1):
            if a + (k - 1) * d > N: break
            if all(col[a + j * d - 1] == col[a - 1] for j in range(k)): return True
    return False

def ramsey(N, r, k):
    return all(has_mono(col, k) for col in itertools.product(range(r), repeat=N))

def W(r, k, cap=12):
    for N in range(1, cap + 1):
        if ramsey(N, r, k): return N
    return None

print("F(r,k) small values:", {(r, k): F(r, k) for r in (1, 2) for k in (1, 2, 3)}, " F(1,4) =", F(1, 4))
res = []
for r in (1, 2, 3, 4):
    res.append((f"W_{r}(1)", W(r, 1), 1)); res.append((f"W_{r}(2)", W(r, 2), r + 1))
for k in (1, 2, 3, 4, 5):
    res.append((f"W_1({k})", W(1, k), k))
res.append(("W_2(3)", W(2, 3), 9))
for name, got, claim in res:
    print(f"{name}: brute force {got}, paper {claim}, {'OK' if got == claim else 'MISMATCH'}")
print("W_r(k) <= F(r,k):", all(W(r, k) <= F(r, k) for r, k in [(1, 3), (1, 4), (2, 3), (3, 2), (4, 2)]),
      "(W_2(3)=9 <= F(2,3)=%d)" % F(2, 3))
print("CONTROL claim W_r(2)=r:", ["rejected" if W(r, 2) != r else "ACCEPTED (bad)" for r in (1, 2, 3, 4)])
```

Output:
```
F(r,k) small values: {(1, 1): 1, (1, 2): 2, (1, 3): 4, (2, 1): 1, (2, 2): 3, (2, 3): 780}  F(1,4) = 8
W_1(1): brute force 1, paper 1, OK
W_1(2): brute force 2, paper 2, OK
W_2(1): brute force 1, paper 1, OK
W_2(2): brute force 3, paper 3, OK
W_3(1): brute force 1, paper 1, OK
W_3(2): brute force 4, paper 4, OK
W_4(1): brute force 1, paper 1, OK
W_4(2): brute force 5, paper 5, OK
W_1(1): brute force 1, paper 1, OK
W_1(2): brute force 2, paper 2, OK
W_1(3): brute force 3, paper 3, OK
W_1(4): brute force 4, paper 4, OK
W_1(5): brute force 5, paper 5, OK
W_2(3): brute force 9, paper 9, OK
W_r(k) <= F(r,k): True (W_2(3)=9 <= F(2,3)=780)
CONTROL claim W_r(2)=r: ['rejected', 'rejected', 'rejected', 'rejected']
```

Control: the false claim W_r(2) = r is rejected for r = 1..4.

Exact arithmetic (Fraction): 2c − γ/80 = −21/200000; 100·(1/8 − 1/32 − 2/500) = 100·359/4000 = 8.975 > log 2 = 0.693; γ/160 = 1/16000.

## 10. Citation table (my scope)

| Cited result | What the paper says it says | What the source says (quote) | Verdict |
|---|---|---|---|
| Fox–Hunter arXiv 2606.02541v1, Thm 1 | "$W_3(k)>2^{k\log^*k/4}$ for all sufficiently large $k$, where $\log^*k$ counts the iterations of the natural logarithm" | "Theorem 1. For k sufficiently large, w(k; 3) > 2^{k(log∗ k)/4}." log∗ = "the number of times the logarithm function must be iteratively applied to k before the result is at most 1" | MATCH ("natural" is the paper's gloss) |
| Fox–Hunter Thm 2 | "$W_r(k)\ge r^{(1-\varepsilon)k\log k}$ when $k$ is sufficiently large in terms of $\varepsilon$ and $r\ge(\log k)^{3/\varepsilon}$" | "Theorem 2. For each ε ∈ (0, 1) there exists k0(ε) so that the following holds. Suppose k ≥ k0(ε) and r ≥ (log k)^{3/ε}, then w(k; r) ≥ r^{(1−ε)k(log k)}." | MATCH |
| Fox–Hunter pp.2–3 | "covering an interval by translates of such sets already gives superpolynomial growth in the number of colors" | "if there is a set S ⊂ [N] with |S| ≥ εN with no k-term arithmetic progression, then we can use r = (3/ε) log2 N random translates of S to cover [N] … that there is c_k > 0 such that w(k; r) ≥ 2^{c_k (log r)^{⌈log k⌉}}" | MATCH |
| Fox–Hunter Section 2 (Erdős–Turán via least nonzero digit) | 07 l.7–9: "recalled, with the least-nonzero-digit argument, by Fox and Hunter [Section 2]" | "Erdős and Turán [16] gave the following simple construction … consider the position i of the least nonzero digit in base p of the common difference d." | MATCH |
| Fox–Hunter lcm dilations | "Least-common-multiple dilations in cyclic groups appear in Fox and Hunter" | Proof of Lemma 2.10: "Let ℓ = lcm(1, 2, …, ⌈1/ε⌉) … ℓ is invertible in Z_N … ℓ · I be the dilation of I by ℓ" | MATCH |
| Campos–Fox–Schildkraut arXiv 2608.20824v1, Thm 1 | "$W_2(k)\ge(1-o(1))k2^{k-1}$. They credit ChatGPT 5.6 Sol Pro with the coloring and an initial proof." | "Theorem 1. For every positive integer k we have w(k) ≥ (1 − o(1))k2^{k−1}." "The coloring used to prove Theorem 1, as well as a proof of Theorem 1, were generated by a query to ChatGPT 5.6 Sol Pro. The proof we present, while drawing somewhat on the proof given by ChatGPT, was produced by the authors." | MATCH |
| CFS settles W_2(k)/2^k | "Their result settles the question about $W_2(k)/2^k$" | "This verifies a conjecture of Erdős" (lim w(k)/2^k = ∞) | MATCH |
| Companion "Quasipolynomial Bounds for Arithmetic Progressions", Eq. (1.3) (fetched from github.com/openai/math main, sha256 481eaf7730dc…) | upper half of the intro display, r ≥ 256, A_k ≥ 1 | "Wr (k) ≤ ⌈exp(Ak (2 + log r)^{Ak})⌉ (r ≥ 1), (1.3) after increasing Ak … The companion paper [37, Theorem 7.2] gives the complementary lower bound Wr (k) > exp((log r)²/(64 log 2)) for all integers r ≥ 256 and k ≥ 3." | MATCH as a citation; content unrefereed (Obj. 3) |
| Erdős 1980 survey, p.90 (2) | "Erdős explicitly asked for this full limit in the two-color case" | "I offer 500 dollars for the proof or disproof of lim f(n)^{1/n} = ∞ (2)", with f(n) defined for "divide the integers 1 ≤ t ≤ f(n) into two classes" | MATCH |

(The remaining bib entries — Berlekamp, Szabó, Kozik–Shabanov, Hunter, Kelley–Meka, Leng–Sah–Sawhney, Stanley, Behrend, Rankin, Green–Wolf, Green, Shi–Dong, Shelah, Gowers, van der Waerden 1998 — belong to the `sources` seat. I did not check them.)

## 11. Status per lemma / proposition / equation

| Item | Status |
|---|---|
| 01-introduction.tex (all claims) | VERIFIED LINE BY LINE against the body and cited sources (§6, §10) |
| (setup:parameters), (setup:dilation-definition), Lemma 2.1 setup:dilation | VERIFIED LINE BY LINE |
| Lemma 2.2 setup:prime | VERIFIED LINE BY LINE (holds from k = 3; §4 S2) |
| (setup:q-bounds), gcd(λ,q)=1, (setup:orders), (setup:coordinates), U-partition, (mesh:definition), (mesh:intervals) | VERIFIED LINE BY LINE |
| Lemma 2.3 mesh:width, Lemma 2.4 mesh:neighbors, (mesh:truncation-definition), Lemma 2.5 mesh:truncated | VERIFIED LINE BY LINE (no numeric mesh build: that is the `setup` seat's job) |
| Lemma 3.1 count:arrangement | zero-sign reduction and final simplification VERIFIED; strict-region bound SKIMMED (classical, cited to Stanley, sketched) |
| Lemma 3.2 count:global | VERIFIED LINE BY LINE |
| Def 3.3 count:eligible, Lemma 3.4 count:local | VERIFIED LINE BY LINE (three cases, lift uniqueness, arithmetic h^{D+1}[C_0(Dh)²]^{2D} ≤ (CDh)^{6D} with C = C_0^{1/3}) |
| Lemma 4.1 outer:lll | VERIFIED LINE BY LINE |
| Prop 4.2 outer:coloring, (outer:row-size), (outer:tail), (outer:first-weight), (outer:second-weight), (outer:incident-weight), (outer:criterion) | VERIFIED LINE BY LINE (thresholds in §4) |
| Lemmas 5.1–5.4, Thm 5.5 (short and long cases) | VERIFIED LINE BY LINE (no small-model simulation: that is the `dichotomy` seat's job) |
| Lemma 6.1 perturb:multiplicity, (perturb:signature), Lemma 6.2 perturb:signatures, Thm 6.3 perturb:cyclic, (perturb:rich-bound), (perturb:negative-coefficient), (perturb:affine-bound) | VERIFIED LINE BY LINE (−21/200000 exact) |
| Prop 7.1 transfer:product, (7.1), proof of Thm 1.1 | VERIFIED LINE BY LINE + brute force with failing controls |
| Thm 7.2 transfer:large-r, (7.2)–(7.4) | VERIFIED LINE BY LINE + brute force + exact sweep with failing controls |
| Cor 7.3 transfer:limits | VERIFIED LINE BY LINE |
| Thm A.1 upper:finite, (A.1)–(A.3) | VERIFIED LINE BY LINE + brute force of boundary values |
| figures/norm-band.tex | NOT READ (illustration only) |
| Lean: Model, Main, UniformTransfer, CyclicWitness, LargeColorConsequences, CyclicBasic, DigitProduct, DigitProductBounds, Basic, UpperBound (F, finite_ramsey, W_two), comparator | statements READ and compared (§8); proofs not kernel-checked by me (replay running elsewhere; never ran lean/lake) |
| Lean: the remaining ~100 ProgressionColoring files | NOT READ |

## 12. Verdict for my scope

**HOLDS AS READ.**
- Theorem 1.1 follows from §2–§6 and Prop 7.1 through a dependency graph whose interfaces all match (§3).
- Every "sufficiently large k" inequality holds for all large k, and none is reversed (§4). K_0 is absolute and uniform in r, P and the progression. Under the paper's own constants K_0 ≈ 10^{44.7}, set by the outer:second-weight sup bound.
- The constant is capped only by 2c < γ/80 (§5). Nothing proves too much.
- §7 and the Appendix are correct.
- The Lean statement `uniform_lower_bound` is exactly Theorem 1.1, with no vacuity and no weakening.
- `kthRoot_tendsto` at r = 2 is exactly erdosproblems.com/138.
- The remaining issues are expository:
  - finiteness and monotonicity are unstated in §7;
  - 34 mislabelled "Theorem" cross-references;
  - the intro's "at most quasipolynomial" for k ≥ 4 rests on the unrefereed companion paper.
