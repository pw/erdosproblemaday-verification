# Independent check of the move-density paragraph.
# (1) exact recount of up/down moves for n+1 <= 1e7 via the jump rule + prime counts (must equal bf: 283889 / 281802)
# (2) at n ~ 1e9: real local move share in a window, decomposed into A = "class k empty", B = "class k-1 holds only Q",
#     vs Cramer probabilities for the SAME (k,Q) events, vs independence with real (binned) marginals.
import numpy as np, math, sys
def sieve(N):
    s = np.ones(N + 1, bool); s[:2] = False
    for i in range(2, math.isqrt(N) + 1):
        if s[i]: s[i*i::i] = False
    return s
# ---- (1) exact to 1e7
N = 10**7
isp = sieve(N + 10); pi = np.cumsum(isp).astype(np.int64)
lpf = np.zeros(N + 1, np.int64)
for p in np.nonzero(isp[:N+1])[0]:
    lpf[p::p] = p            # increasing p overwrites -> largest prime factor
m = np.arange(2, N + 1, dtype=np.int64); n = m - 1
Q = lpf[2:]; big = Q * Q > m
k = np.where(big, m // Q, 0)
s = np.array([math.isqrt(int(x)) for x in n]) if False else np.floor(np.sqrt(n.astype(np.float64))).astype(np.int64)
s -= (s*s > n); s += ((s+1)*(s+1) <= n)
mm, nn, kk, QQ, ss = m[big], n[big], k[big], Q[big], s[big]
loA = np.maximum(nn // (kk + 1), ss)
A = (pi[QQ - 1] - pi[loA]) == 0
k1 = np.maximum(kk - 1, 1)
B = (kk >= 2) & ((pi[nn // k1] - pi[np.maximum(nn // kk, ss)]) == 1)
d = A.astype(int) - B.astype(int)
ok = mm != 4
print("exact to 1e7: up", int(np.sum((d == 1) & ok)), "down", int(np.sum((d == -1) & ok)), "(bf: 283889 / 281802; m=4 is +1 separately)")
