#!/usr/bin/env python3
# Same pair term, linear (not exponentiated) resummation: Delta E = sum P0_C * (-q^2 D(H)).
import math, re, numpy as np
exec(open('pair_check.py').read().split("def pair_delta")[0].replace('print(f"C2', '#').replace('    print(f"D(', '    pass #'))
for e in (15, 16, 17, 18):
    n = 10**e; s = math.isqrt(n); kmax = n // (s + 1); tot = 0.0; CH = 10_000_000; k0 = 1
    while k0 <= kmax:
        k = np.arange(k0, min(kmax, k0 + CH - 1) + 1, dtype=np.int64)
        aa = np.maximum(n // (k + 1), s); bb = n // k; H = bb - aa
        mid = 0.5 * (aa.astype(float) + bb.astype(float)) + 0.5; q = 1.0 / np.log(mid)
        lp0 = H * np.log1p(-q); use = (H > 0) & (lp0 > -80)
        tot += float(np.sum(np.exp(lp0[use]) * (-(q[use] ** 2) * D[H[use]]))); k0 += CH
    md = open(f'model_1e{e}.out').read(); hf = open(f'hfast_1e{e}.out').read()
    J = int(re.search(r' J=(\d+)', hf).group(1)); EC = float([l.split() for l in md.splitlines() if l.startswith('cramer ')][0][2])
    print(f"1e{e}: linear pair term {tot:.0f} = {tot/(J-EC):.4f} of the gap", flush=True)
