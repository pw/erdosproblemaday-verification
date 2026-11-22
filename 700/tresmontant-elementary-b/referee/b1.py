#!/usr/bin/env python3
"""B1 split: every hypothesis triple with PLO < p <= PHI; exact f via f_enum2; incremental output."""
import sys, math, time
from multiprocessing import Pool
from ref700 import f_enum2
from tests import hyp_triples
PLO, PHI, W = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
def job(t): return t, f_enum2(t)
if __name__ == "__main__":
    t0 = time.time()
    H = [t for t in hyp_triples(PHI) if t[0] > PLO]
    print(f"range ({PLO},{PHI}]: {len(H)} hypothesis triples", flush=True)
    done = bad_thm = bad_c1 = 0; maxe = 0; d2 = 0
    with Pool(W) as pool:
        for t, f in pool.imap_unordered(job, H, chunksize=4):
            p, q, r = t; n = p * q * r; done += 1
            if f * f <= n: bad_thm += 1; print("THEOREM FAILS", t, f, flush=True)
            if f != p * q: bad_c1 += 1; print("C1 FAILS", t, f, flush=True)
            if r - p >= math.isqrt((p - 1) // 2) - 1: maxe += 1
            if q - p == 2: d2 += 1
            if done % 1000 == 0: print(f"  {done}/{len(H)} ok so far ({time.time()-t0:.0f}s)", flush=True)
    print(f"RESULT ({PLO},{PHI}]: triples={len(H)} computed={done} f<=sqrt n: {bad_thm}  f!=pq: {bad_c1}  "
          f"(of which e within 1 of max: {maxe}, d=2: {d2})  {time.time()-t0:.0f}s", flush=True)
