#!/usr/bin/env python3
"""Stage B4: pure Legendre brute force over EVERY k in (1, n/2] (no Lucas, no reduction) on edge-case hypothesis
triples up to n ~ 1.1e9, plus the 103*107*113 control and one triple with h>d just outside 2e^2<p."""
import math, time
from multiprocessing import Pool
from ref700 import sieve, f_leg, hyp

PR = sieve(5000); PS = set(PR)
def first(pmin, d, e):
    for p in PR:
        if p >= pmin and p + d in PS and p + e in PS: return (p, p + d, p + e)

cases = [(101, 103, 107)]
cases.append(first(393, 2, 14)); cases.append(first(393, 6, 14))       # e=14 at the smallest p allowed (2*196<p)
cases.append(first(801, 2, 20)); cases.append(first(801, 8, 20))       # e=20, p just above 800
cases.append(first(969, 2, 22)); cases.append(first(969, 10, 22))      # e=22 = isqrt((p-1)/2) for p in [969,1057)
cases.append(first(1000, 2, 6))                                        # d=2, h=4, n ~ 1e9
cases += [(103, 107, 113)]                                             # submitter's sharpness control
cases = [c for c in cases if c]

def job(t):
    p, q, r = t; t0 = time.time(); f = f_leg(p * q * r)
    return (t, f, time.time() - t0)

if __name__ == "__main__":
    with Pool(len(cases)) as pool:
        for (t, f, dt) in pool.imap(job, cases):
            p, q, r = t; n = p * q * r; d, h, e = q - p, r - q, r - p
            print(f"B4 {t} n={n} d={d} h={h} e={e} 2e^2={2*e*e} hyp={hyp(*t)} f_leg(all k)={f} pq={p*q} "
                  f"f==pq:{f==p*q} f>sqrt n:{f*f>n}  [{dt:.0f}s]", flush=True)
