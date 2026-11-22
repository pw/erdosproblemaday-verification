#!/usr/bin/env python3
"""Closest failures to the 2e^2<p boundary: triples with h>d and p <= 2e^2 < 1.25p, p <= 12000."""
import math
from multiprocessing import Pool
from ref700 import sieve, f_enum2
PR = sieve(13000)
T = []
for a, p in enumerate(PR):
    if p < 3 or p > 12000: continue
    for b in range(a + 1, len(PR)):
        q = PR[b]
        if 2 * (q - p) ** 2 >= 1.25 * p: break
        for c in range(b + 1, len(PR)):
            r = PR[c]; e = r - p
            if 2 * e * e >= 1.25 * p: break
            if 2 * e * e >= p and r - q > q - p: T.append((p, q, r))
def job(t): return t, f_enum2(t)
if __name__ == "__main__":
    with Pool(4) as pool: res = pool.map(job, T, chunksize=10)
    fails = [(t, f) for t, f in res if f * f <= t[0] * t[1] * t[2]]
    fails.sort(key=lambda x: 2 * (x[0][2] - x[0][0]) ** 2 / x[0][0])
    print(f"triples with h>d and p<=2e^2<1.25p, p<=12000: {len(T)}; with f<=sqrt n: {len(fails)}")
    for t, f in fails[:10]:
        p, q, r = t; e = r - p
        print(f"  {t} d={q-p} h={r-q} e={e} 2e^2/p={2*e*e/p:.4f} f={f}")
