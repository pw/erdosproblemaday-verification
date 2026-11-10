#!/usr/bin/env python3
"""Lead seat's INDEPENDENT check of the Hardy–Littlewood pair correction (Erdős #912).
Per interval of H integers at height x (q = 1/log x), HL changes the second factorial cumulant of the prime count by
2 q^2 D(H), D(H) = sum_{d=1}^{H-1} (H-d)(S(d)-1), S = Hardy–Littlewood singular series (S(d)=0 for odd d,
S(d) = 2 C2 prod_{p|d, p>2} (p-1)/(p-2) for even d). To second order log P(empty) = log P_Cramér(empty) + q^2 D(H), so
  Delta E[J] = sum_k P0_C(k) * (1 - exp(q_k^2 D(H_k))).
Also checks D(H) against Montgomery–Soundararajan eq. (17) for k = 2: D(H) = -H log H / 2 + (2 - gamma - log 2pi) H / 2 + o(H).
Usage: pair_check.py e1 e2 ...   (n = 10^e; reads model_1e<e>.out and hfast_1e<e>.out for the gap)
"""
import sys, math, re, numpy as np

HMAX = 20000
# C2 twin-prime constant
def primes_upto(N):
    s = np.ones(N + 1, bool); s[:2] = False
    for i in range(2, int(N ** .5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0]
P = primes_upto(2_000_000)
C2 = float(np.prod(1.0 - 1.0 / (P[1:].astype(float) - 1) ** 2))   # tail beyond 2e6 contributes ~1e-7 relative
S = np.zeros(HMAX + 1)
for d in range(2, HMAX + 1, 2):
    v = 2 * C2; m = d
    while m % 2 == 0: m //= 2
    p = 3
    while p * p <= m:
        if m % p == 0:
            v *= (p - 1) / (p - 2)
            while m % p == 0: m //= p
        p += 2
    if m > 1: v *= (m - 1) / (m - 2)
    S[d] = v
a = S - 1.0; a[0] = 0.0
d_idx = np.arange(HMAX + 1, dtype=float)
A = np.cumsum(a); B = np.cumsum(d_idx * a)
D = np.zeros(HMAX + 1)
for H in range(2, HMAX + 1): D[H] = H * A[H - 1] - B[H - 1]
g = 0.5772156649015329
print(f"C2 = {C2:.10f} (literature 0.6601618158)")
for H in (100, 1000, 10000, 20000):
    ms = -0.5 * H * math.log(H) + 0.5 * (2 - g - math.log(2 * math.pi)) * H
    print(f"D({H}) = {D[H]:.1f}   M–S eq.(17) k=2 main terms = {ms:.1f}   diff/sqrt(H) = {(D[H]-ms)/math.sqrt(H):+.3f}")

def pair_delta(n):
    s = math.isqrt(n); kmax = n // (s + 1)
    tot = 0.0; CH = 10_000_000; k0 = 1
    while k0 <= kmax:
        k = np.arange(k0, min(kmax, k0 + CH - 1) + 1, dtype=np.int64)
        aa = n // (k + 1); bb = n // k
        aa = np.maximum(aa, s); H = bb - aa
        ok = H > 0
        mid = 0.5 * (aa.astype(np.float64) + bb.astype(np.float64)) + 0.5
        q = 1.0 / np.log(mid)
        lp0 = H * np.log1p(-q)
        use = ok & (lp0 > -80)
        if np.any(use):
            Hu = H[use]
            assert Hu.max() <= HMAX, Hu.max()
            p0 = np.exp(lp0[use]); qq = q[use]
            tot += float(np.sum(p0 * (1.0 - np.exp(qq * qq * D[Hu]))))
        k0 += CH
    return tot

for e in map(int, sys.argv[1:]):
    n = 10 ** e
    md = open(f'model_1e{e}.out').read(); hf = open(f'hfast_1e{e}.out').read()
    J = int(re.search(r' J=(\d+)', hf).group(1))
    EC = float([l.split() for l in md.splitlines() if l.startswith('cramer ')][0][2])
    dE = pair_delta(n); gap = J - EC
    print(f"1e{e}: gap J-E_C = {gap:.1f}   HL pair-only Delta E = {dE:.1f}   ratio = {dE/gap:.4f}", flush=True)
