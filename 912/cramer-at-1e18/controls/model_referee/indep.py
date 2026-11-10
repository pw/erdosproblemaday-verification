#!/usr/bin/env python3
# Referee's independent finite-n model expectations for Erdős #912 (no midpoint approximation).
# J-region: integers l > s = isqrt(n), grouped by k = n // l (so l in (n//(k+1), n//k], l > s).
# Per-integer exact log P(I_k empty) = sum_l log(1 - p_l).  Models: Cramér p_l = 1/log l;
# sieve-z: p_l = theta_z/log l if l has no prime factor <= z else 0 (coprimality by direct modulus).
# Small k (k < kc) are certain to be nonempty to within exp(-60) each; this is checked, not assumed.
import sys, math, numpy as np
n = int(sys.argv[1]); K0 = int(sys.argv[2])
s = math.isqrt(n); kmax = n // (s + 1)
ZMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 139
ZP = [p for p in range(2, ZMAX + 1) if all(p % q for q in range(2, p))]   # primes up to 139
theta = []; t = 1.0
for p in ZP: t *= p / (p - 1); theta.append(t)
L = math.log(n)
kc = int(math.isqrt(int(n / (70 * L))))
# check: for every k < kc the Cramér bound P0 <= exp(-len/log(n/k)) is < exp(-60), and the same for each z model
# (z model: P0 <= exp(-theta * cop_count / log b); cop_count >= len*phi/P - 2^pi(z) — use crude len/(theta) - 2^{pi(z)} only for small z;
#  instead we just compute those k exactly too if the bound fails)
k = np.arange(1, kc, dtype=np.int64)
a = np.maximum(n // (k + 1), s); b = n // k; ln = (b - a).astype(float)
bound = ln / np.log(b.astype(float))
assert bound.min() > 60, bound.min()
print(f"n={n} s={s} kmax={kmax} kc={kc} min len/log b for k<kc = {bound.min():.1f}  (each such k: P0 < e^-60)")
lhi = n // kc                      # all l in (s, lhi] have k = n//l in [kc, kmax]
nk = kmax - kc + 1
M = 1 + len(ZP)
lp0 = np.zeros((M, nk)); S1 = np.zeros(nk); S2 = np.zeros(nk); cnt = np.zeros((M, nk))
CH = 5_000_000
lo = s + 1
maxprob = np.zeros(M)
while lo <= lhi:
    hi = min(lhi, lo + CH - 1)
    l = np.arange(lo, hi + 1, dtype=np.int64)
    kk = n // l - kc
    lg = np.log(l.astype(np.float64))
    q = 1.0 / lg
    lp0[0] += np.bincount(kk, weights=np.log1p(-q), minlength=nk)
    cnt[0] += np.bincount(kk, minlength=nk)
    r = q / (1 - q)
    S1 += np.bincount(kk, weights=r, minlength=nk); S2 += np.bincount(kk, weights=r * r, minlength=nk)
    maxprob[0] = max(maxprob[0], q.max())
    cop = np.ones(l.size, bool)
    for j, p in enumerate(ZP):
        cop &= (l % p) != 0
        qq = theta[j] * q[cop]
        maxprob[j + 1] = max(maxprob[j + 1], qq.max())
        lp0[j + 1] += np.bincount(kk[cop], weights=np.log1p(-qq), minlength=nk)
        cnt[j + 1] += np.bincount(kk[cop], minlength=nk)
    lo = hi + 1
assert maxprob.max() < 1, maxprob
p0 = np.exp(lp0); pk = 1 - p0
base = kc - 1                       # k = 1..kc-1, all nonempty w.p. > 1 - e^-60
kidx = np.arange(kc, kmax + 1)
sel = kidx >= K0
names = ["cramer"] + [f"z={p}" for p in ZP]
print(f"{'model':8s} {'theta':>8s} {'E[J]':>16s} {'sd':>10s}")
out = {}
for m in range(M):
    E = base + pk[m].sum(); V = (pk[m] * p0[m]).sum()
    out[names[m]] = (E, math.sqrt(V))
    print(f"{names[m]:8s} {1.0 if m == 0 else theta[m-1]:8.4f} {E:16.3f} {math.sqrt(V):10.3f}")
# exact Poisson-binomial u_0,u_1,u_2 on k >= K0 (Cramér)
u0 = p0[0][sel].sum(); u1 = (p0[0] * S1)[sel].sum(); u2 = (p0[0] * (S1 * S1 - S2) / 2)[sel].sum()
print(f"Cramér exact Poisson-binomial on k>=K0={K0}: u0={u0:.2f} u1={u1:.2f} u2={u2:.2f}")
np.savez(f"/tmp/ref912/indep_{n}.npz", kidx=kidx, len=cnt[0], p0c=p0[0], p0z19=p0[ZP.index(19) + 1])
