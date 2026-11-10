import numpy as np, math
def sieve(N):
    s = np.ones(N + 1, bool); s[:2] = False
    for i in range(2, math.isqrt(N) + 1):
        if s[i]: s[i*i::i] = False
    return s
M0 = 10**9; W = 4 * 10**6; KMIN = 300
PMAX = M0 // (KMIN - 1) + 10**5
isp = sieve(PMAX); pi = np.cumsum(isp).astype(np.int64)
sp = np.nonzero(sieve(math.isqrt(M0 + W) + 2))[0]
m = np.arange(M0, M0 + W, dtype=np.int64); rem = m.copy(); lpf = np.ones(W, np.int64)
for p in sp:
    st = (-M0) % p
    idx = np.arange(st, W, p)
    lpf[idx] = p
    r = rem[idx]
    while True:
        dv = (r % p == 0)
        if not dv.any(): break
        r = np.where(dv, r // p, r)
    rem[idx] = r
lpf = np.where(rem > 1, rem, lpf)       # cofactor is a prime larger than every sieving prime
n = m - 1
Q = lpf; big = Q * Q > m; k = np.where(big, m // np.maximum(Q,1), 0)
sel = big & (k >= KMIN)
print("steps", W, " with Q>sqrt(m):", int(big.sum()), " k>=KMIN:", int(sel.sum()))
nn, kk, QQ = n[sel], k[sel], Q[sel]
ss = np.floor(np.sqrt(nn.astype(np.float64))).astype(np.int64); ss -= (ss*ss > nn); ss += ((ss+1)*(ss+1) <= nn)
assert QQ.max() < PMAX and (nn // (kk - 1)).max() < PMAX
loA = np.maximum(nn // (kk + 1), ss)
A = (pi[QQ - 1] - pi[loA]) == 0
hiB = nn // (kk - 1); loB = np.maximum(nn // kk, ss)
B = (pi[hiB] - pi[loB]) == 1
moves = int(np.sum(A ^ B)); up = int(np.sum(A & ~B)); down = int(np.sum(~A & B))
print(f"real local share near 1e9: {moves/W:.4f}  (up {up/W:.4f}, down {down/W:.4f})")
# Cramer probabilities for the same (k,Q) events
lenA = (QQ - 1) - loA; lenB = hiB - loB - 1
xA = 0.5 * (loA + QQ).astype(float); xB = 0.5 * (QQ + hiB).astype(float)
pA = np.exp(lenA * np.log1p(-1 / np.log(xA))); pB = np.exp(lenB * np.log1p(-1 / np.log(xB)))
print(f"Cramer conditional on the same events: {np.sum(pA + pB - 2*pA*pB)/W:.4f}")
print(f"  P(A): real {A.mean():.4f} Cramer {pA.mean():.4f}   P(B): real {B.mean():.4f} Cramer {pB.mean():.4f}")
print(f"  P(A&B): real {(A&B).mean():.4f}  product-of-real-marginals-per-bin: ", end='')
L = math.sqrt(M0 / math.log(M0)); t = kk / L; b = np.minimum((t / 0.05).astype(int), 200)
pa = np.bincount(b, A, 201) / np.maximum(np.bincount(b, None, 201), 1); pb = np.bincount(b, B, 201) / np.maximum(np.bincount(b, None, 201), 1)
ind = pa[b] + pb[b] - 2 * pa[b] * pb[b]
print(f"{(pa[b]*pb[b]).mean():.4f}")
print(f"independence with REAL binned marginals: {ind.sum()/W:.4f}")
# event count vs model's sum_k 1/(k log(n/k)) over k>=KMIN
ks = np.arange(KMIN, math.isqrt(M0) + 1, dtype=float); print(f"events/W real {sel.sum()/W:.4f}  model sum_k 1/(k log(n/k)) {np.sum(1/(ks*np.log(M0/ks))):.4f}")
print("decade bf 1e8-1e9 share 0.0444; model local at 1e9 (move_density.log) 0.0560")
# split by k <= L vs k > L, and check the elementary per-k bound #A(k) <= (W/k)/H_k + 1
mv = A ^ B; Lk = int(L)
print(f"moves with k<=L: {mv[kk<=Lk].sum()/W:.4f}   k>L: {mv[kk>Lk].sum()/W:.4f}   (1/log n = {1/math.log(M0):.4f})")
cntA = np.bincount(kk, A); Hk = (M0 / (np.arange(cntA.size) * (np.arange(cntA.size) + 1.0) + 1e-9))
ks = np.arange(KMIN, Lk + 1); bound = (W / ks) / (Hk[ks] - 2) + 2
print("max over k<=L of #A(k)/bound:", float(np.max(cntA[ks] / bound)))
