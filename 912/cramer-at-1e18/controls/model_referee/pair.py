#!/usr/bin/env python3
# Referee: parameter-free second-order (pair-correlation / Hardy–Littlewood singular series) correction to the
# Cramér-model E[J].  For an interval with H integers at height x (q = 1/log x), the HL pair correlation changes
# the second factorial cumulant by 2 q^2 D(H), D(H) = sum_{d<H} (H-d)(S(d)-1), so to second order
#   log P0_true = log P0_Cramér + q^2 D(H).
# D_full uses the full singular series S(d); D_z uses the truncated S_z(d) = prod_{p<=z}(...), which is EXACTLY the
# pair correlation of model.c's sieve model z (so the z=19 line validates the pair-only approximation against model.c).
import sys, math, numpy as np
HMAX = 6000
def primes(N):
    s = np.ones(N + 1, bool); s[:2] = False
    for i in range(2, math.isqrt(N) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]
PR = primes(10**6)
C2 = float(np.prod(1 - 1.0 / (PR[1:].astype(float) - 1) ** 2))     # twin prime constant (tail beyond 1e6 ~ 1e-7)
d = np.arange(HMAX + 1)
def S_full():
    S = np.where(d % 2 == 0, 2 * C2, 0.0); S[0] = 0
    for p in PR[1:]:
        if p > HMAX: break
        m = (d % p == 0) & (d > 0)
        S[m] *= (p - 1) / (p - 2)
    return S
def S_trunc(z):
    S = np.ones(HMAX + 1)
    for p in PR:
        if p > z: break
        S *= np.where(d % p == 0, p / (p - 1), p * (p - 2) / (p - 1) ** 2)
    return S
def Dtab(S):
    g = S - 1.0; g[0] = 0
    G1 = np.cumsum(g); G2 = np.cumsum(d * g)
    H = np.arange(HMAX + 1)
    D = np.zeros(HMAX + 1)
    D[2:] = H[2:] * G1[1:-1] - G2[1:-1]          # sum_{d=1}^{H-1} (H-d) g(d)
    return D
Dfull = Dtab(S_full()); D19 = Dtab(S_trunc(19)); D5 = Dtab(S_trunc(5))
for H in (10, 30, 100, 1000):
    print(f"# D_full({H}) = {Dfull[H]:.3f}  vs -H logH/2 + A H = {-H*math.log(H)/2 + (1-0.5772156649-math.log(2*math.pi))/2*H:.3f}   D_19={D19[H]:.3f}")
for e in map(int, sys.argv[1:]):
    n = 10 ** e; s = math.isqrt(n); kmax = n // (s + 1)
    kc = int(math.isqrt(int(n / (70 * math.log(n)))))
    tot = {"full": 0.0, "z19": 0.0, "z5": 0.0}
    CH = 20_000_000; k0 = kc
    while k0 <= kmax:
        k = np.arange(k0, min(kmax, k0 + CH - 1) + 1, dtype=np.int64)
        a = np.maximum(n // (k + 1), s); b = n // k; H = b - a
        mid = 0.5 * (a + b) + 0.5; q = 1.0 / np.log(mid.astype(float))
        p0 = np.exp(H * np.log1p(-q))
        Hc = np.minimum(H, HMAX)
        assert (p0[H > HMAX] < 1e-25).all()
        for key, D in (("full", Dfull), ("z19", D19), ("z5", D5)):
            tot[key] += float(np.sum(p0 * -np.expm1(q * q * D[Hc])))
        k0 += CH
    scale = math.sqrt(n / math.log(n)); L = math.log(n); LL = math.log(L)
    print(f"1e{e}: pair-only predicted dE[J]: full HL = {tot['full']:.1f}  z=19 = {tot['z19']:.1f}  z=5 = {tot['z5']:.1f}"
          f"   | full/scale = {tot['full']/scale:.5f}  (x L/LL = {tot['full']/scale*L/LL:.4f})", flush=True)
