# Brute-force checks of the numerical inequalities used in Sections 5-6 over generous ranges.
from math import sqrt, floor
def T(n):
    if n <= 2: return 1
    if n <= 6: return n
    if n <= 8: return 10
    return 1 + 2 ** ((n - 1) // 2)
B = lambda N: 2 ** ((N - 1) // 2)
bad = []
# T nondecreasing; B(N) >= 2^(N/2-1); T(k) <= 2^((k+1)/2) for k>=3
for n in range(1, 400):
    if T(n + 1) < T(n): bad.append(('T monotone', n))
for N in range(9, 400):
    if B(N) < 2 ** (N / 2 - 1): bad.append(('B lower', N))
for k in range(3, 400):
    if T(k) > 2 ** ((k + 1) / 2): bad.append(('T(k)<=2^((k+1)/2)', k))
# 5.1: h>=3, kappa>=2h-1: 2^(h-1)(kappa+2)-1 < 2^kappa ; (2^d-1)/(d+1) <= 2^(d-2) for even d>=2
for h in range(3, 60):
    for kap in range(2 * h - 1, 2 * h + 80):
        if not 2 ** (h - 1) * (kap + 2) - 1 < 2 ** kap: bad.append(('5.1', h, kap))
for d in range(2, 200, 2):
    if (2 ** d - 1) / (d + 1) > 2 ** (d - 2): bad.append(('5.1 frac', d))
# 5.1 directly: all d>=2 (even), m>=2, s>=1, N in [nu+dm+2, 2nu] (N>=9): a-bound < B(N)
for d in range(2, 30, 2):
    for m in range(2, 30):
        for s in range(0, 30):
            nu = d + m + s
            lo = nu + d * m + 2 if s > 0 else (d + 1) * (m + 1)
            for N in range(lo, 2 * nu + 1):
                bound = 2 ** m - 1 + 2 ** (m - 1) * (2 ** d - 1) * N / (d + 1)
                if not bound < B(N): bad.append(('5.1 direct', d, m, s, N))
# 5.2 fibre average: d>=4 even, N>=2d+5 : 1 + (2^d-1) N/(d+1) < B(N)
for d in range(4, 60, 2):
    for N in range(2 * d + 5, 2 * d + 200):
        if not 1 + (2 ** d - 1) * N / (d + 1) < B(N): bad.append(('5.2 avg', d, N))
# 5.2 separate fibres: N>=2d+3 -> 2^(d+1)-1 < B(N)
for d in (4, 6):
    for N in range(2 * d + 3, 2 * d + 5):
        if not 2 ** (d + 1) - 1 < B(N): bad.append(('5.2 sep', d, N))
# 5.3 / Lemma 5.4
for nu in range(10, 200, 2):
    if 3 * (nu - 3) < 2 * nu + 1: bad.append(('(6)', nu))
for N in (15, 16):
    if not (N + (255 - 2 * N) // 2) < B(N): bad.append(('5.4 step5', N))
if not 27 < B(11): bad.append('5.4 step3')
# 5.4 products
for i in range(3, 40):
    for j in range(3, 40):
        if i == 3 and j == 3:
            if not 9 < T(9): bad.append('5.4 33')
            continue
        if not 2 * (T(i) * T(j)) ** 2 <= B(i * j) ** 2: bad.append(('5.4 prod', i, j))
# 6.1 descent: N>=45: T(floor(N/4)) * (1 + (N(N-1)-1)(N-1)) < B(N)
for N in range(45, 2000):
    if not T(N // 4) * (1 + (N * (N - 1) - 1) * (N - 1)) < B(N): bad.append(('6.1', N))
# 6.1 small: does the descent bound already fail below 45? (informational)
# 6.2: 21<=N<=44: 31N < B(N)
for N in range(21, 45):
    if not 31 * N < B(N): bad.append(('6.2', N))
# 6.4: s=1 and s>=2 bounds
for N in range(9, 300):
    kap = (N - 1) // 2
    if not kap * kap <= B(N): bad.append(('kappa^2', N))
    if not N + 3 <= kap * kap: bad.append(('N+3<=kap^2', N))
for N in range(12, 300):
    for k in range(9, N - 2):
        if not N - k + T(k) <= B(N): bad.append(('6.4 k>=9', N, k))
# 6.4 s>=2 exact optimisation over m, u, s with c,l maxima
for m in [p ** d for p in (2, 3, 5, 7, 11, 13) for d in range(1, 8) if 3 <= p ** d <= 400]:
    p = next(q for q in (2, 3, 5, 7, 11, 13) if m % q == 0)
    c = (m - 1) // (p - 1)
    for e in [e for e in range(2, m) if (m - 1) % e == 0]:
        tau = sum(1 for t in range(1, e + 1) if e % t == 0)
        l = tau - 1
        for N in range(2 * m + 1, 2 * m + 120):
            best = max(1 + c * u + l * m * s for s in range(2, N) for u in range(1, N - m * s + 1)) if N - 2 * m >= 1 else 0
            if N >= 9 and not best < B(N): bad.append(('6.4 s>=2', m, e, N, best))
            if N in (7, 8) and not best < 10: bad.append(('6.4 s>=2 small', m, e, N, best))
# 6.5 Lemma 6.3 r>=5 and final bound
for r in range(5, 200):
    if r * (r - 1) * 2.0 ** (-r - 2) > 5 / 32 + 1e-12: bad.append(('6.3', r))
    if (r - 1) * (T(r) - 1) > 2 ** r: bad.append(('6.3 I', r))
for m in range(3, 200):
    M = (m * m + 1) / 2
    for r in range(3, 60):
        if (3 / 16) * M * 2.0 ** (-(m - 3) * r / 2) > 15 / 16 + 1e-12: bad.append(('6.5', m, r))
# 6.5 direct: worst case over u,s>=r, u+ms<=N with I = worst allowed
for m in [4, 5, 7, 8, 9, 11, 13, 16, 25, 27, 32]:
    p = next(q for q in (2, 3, 5, 7, 11, 13) if m % q == 0); c = (m - 1) // (p - 1)
    lmax = (m - 1) // 2 if m % 2 else (m - 2) // 2
    for r in range(3, 12):
        I = 2 if r == 3 else (6 if r == 4 else (r - 1) * (T(r) - 1))
        for N in range((m + 1) * r, (m + 1) * r + 40):
            best = max(I * (r + c * u + lmax * m * s) for s in range(r, N) for u in range(r, N - m * s + 1)) if N - m * r >= r else None
            if best is not None and not best < B(N): bad.append(('6.5 direct', m, r, N, best, B(N)))
# 6.6
for N in range(21, 45):
    if not 1 + 35 * N < B(N): bad.append(('6.6', N))
for m in [25, 27, 32, 49, 64, 81, 121, 125, 128]:
    if m + 4 * sqrt(m) < 45: bad.append(('6.6 q0', m))
print('violations:', bad[:20], len(bad))
