#!/usr/bin/env python3
"""Stage A2'/A3' (lighter replacement for validate.py's A2/A3, which timed out): f_leg vs f_enum vs f_enum2."""
import time
from multiprocessing import Pool
from ref700 import *
def job(t):
    p, q, r = t; n = p * q * r
    return t, f_leg(n), f_enum(p, q, r), f_enum2(t)
if __name__ == "__main__":
    t0 = time.time(); P = sieve(5000); T = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if j + 1 >= len(P) or P[i] * P[j] * P[j + 1] > 2_000_000: break
            for k in range(j + 1, len(P)):
                p, q, r = P[i], P[j], P[k]; n = p * q * r
                if n > 2_000_000: break
                h = (p * 7919 + q * 104729 + r * 31)
                if n <= 20_000 or (n <= 300_000 and h % 15 == 0) or h % 120 == 0: T.append((p, q, r))
    print(f"A2' sample: {len(T)} prime triples (all with n<=2e4, 1/15 of n<=3e5, 1/120 of n<=2e6)", flush=True)
    bad = ab = be = rl = rg = 0
    with Pool(6) as pool:
        for t, a, b, c in pool.imap_unordered(job, T, chunksize=8):
            n = t[0] * t[1] * t[2]
            if not (a == b == c): bad += 1; print("A2' MISMATCH", t, a, b, c, flush=True)
            ab += a * a > n; be += a * a <= n; rl += t[2] < t[0] * t[1]; rg += t[2] > t[0] * t[1]
    print(f"A2' mismatches={bad}; f>sqrt n: {ab}, f<sqrt n: {be}; r<pq: {rl}, r>pq: {rg}  ({time.time()-t0:.0f}s)", flush=True)
    H = [(p, q, r) for i, p in enumerate(P) if p <= 260 for q in P[i+1:i+12] for r in P[i+2:i+14]
         if q < r and r - q > q - p and 2 * (r - p) ** 2 < p]
    with Pool(6) as pool:
        for t, a, b, c in pool.imap(job, H):
            p, q, r = t
            print(f"A3' {t} d={q-p} h={r-q} e={r-p} f_leg={a} f_enum={b} f_enum2={c} f==pq:{a==p*q} agree:{a==b==c}", flush=True)
    print(f"done {time.time()-t0:.0f}s")
