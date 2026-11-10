#!/usr/bin/env python3
# Per t-bin HL pair-only excess at n = 10^18 (same bins as model.c: width 0.05 in t = k/sqrt(n/log n)), for the figure.
import math, numpy as np
src = open('pair_check.py').read().split("def pair_delta")[0]
exec(src.replace('print(f"C2', '#').replace('    print(f"D(', '    pass #'))
n = 10**18; s = math.isqrt(n); kmax = n // (s + 1); scale = math.sqrt(n / math.log(n))
NB = 120; out = np.zeros(NB + 1); CH = 10_000_000; k0 = 1
while k0 <= kmax:
    k = np.arange(k0, min(kmax, k0 + CH - 1) + 1, dtype=np.int64)
    aa = np.maximum(n // (k + 1), s); bb = n // k; H = bb - aa
    mid = 0.5 * (aa.astype(float) + bb.astype(float)) + 0.5; q = 1.0 / np.log(mid)
    lp0 = H * np.log1p(-q); use = (H > 0) & (lp0 > -80)
    b = np.minimum((k / scale / 0.05).astype(np.int64), NB)
    val = np.zeros(k.size); Hu = H[use]; qq = q[use]
    val[use] = np.exp(lp0[use]) * (1 - np.exp(qq * qq * D[Hu]))
    np.add.at(out, b, val); k0 += CH
with open('pair_bins_1e18.txt', 'w') as f:
    for i in range(NB + 1): f.write(f"{i*0.05:.2f} {out[i]:.3f}\n")
print('total', out.sum())
