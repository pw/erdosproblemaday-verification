#!/usr/bin/env python3
# Summary table for #912: exact h(n) vs the finite-n Cramér expectation, G–I's Theorem 1.2 expansion, sieve models.
import math, re, numpy as np, sys
g = 0.5772156649015329
def small_model(s):   # E[#model-primes <= s] with 2 counted as certain (G–I's model starts at 3)
    tot = 1.0; lo = 3; C = 10**7; parts = []
    while lo <= s:
        hi = min(s, lo + C - 1); l = np.arange(lo, hi + 1, dtype=np.float64)
        parts.append(float(np.sum(1.0 / np.log(l)))); lo = hi + 1
    return tot + math.fsum(parts)
rows = []
for e in map(int, sys.argv[1:]):
    n = 10**e
    hf = open(f'hfast_1e{e}.out').read(); md = open(f'model_1e{e}.out').read()
    h = int(re.search(r' h=(\d+)', hf).group(1)); pis = int(re.search(r'pi_s=(\d+)', hf).group(1)); J = int(re.search(r' J=(\d+)', hf).group(1))
    m = {}
    for line in md.splitlines():
        w = line.split()
        if w and (w[0] == 'cramer' or w[0].startswith('z=')) and len(w) == 6: m[w[0]] = (float(w[2]), float(w[3]))
    s = math.isqrt(n); scale = math.sqrt(n / math.log(n)); L = math.log(n); LL = math.log(L)
    sm = small_model(s)
    EC = sm + m['cramer'][0]; Ez19 = sm + m['z=19'][0]
    GI = math.sqrt(2 * math.pi) * scale * (1 - LL / (2 * L) + (1 + g + math.log(8)) / (2 * L))
    gapJ = (J - m['cramer'][0]) / scale
    rows.append((e, h, h / scale, pis, sm, J, m['cramer'][0], m['cramer'][1], (J - m['cramer'][0]) / m['cramer'][1], EC / scale, GI / scale,
                 m['z=19'][0], (J - m['z=19'][0]) / m['z=19'][1], gapJ, gapJ * L / LL, (J - m['z=19'][0]) / (J - m['cramer'][0])))
    print(f"1e{e}: h={h} ratio={h/scale:.6f} | pi(s)={pis} model_small={sm:.1f} | J={J} E_C[J]={m['cramer'][0]:.1f} sd={m['cramer'][1]:.1f} Z={rows[-1][8]:+.1f}"
          f" | E_C[h]/scale={EC/scale:.6f}  G-I formula/scale={GI/scale:.6f} | E_z19[J]={m['z=19'][0]:.1f} Z19={rows[-1][12]:+.1f}"
          f" | (J-E_C)/scale={gapJ:.5f}  x logn/loglogn={gapJ*L/LL:.4f} | residual frac after z19={rows[-1][15]:.3f}")
