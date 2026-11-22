#!/usr/bin/env python3
"""Stage B: test the theorem, C1 and sharpness with the exact f_enum2 (validated in stage A)."""
import sys, time, math
from multiprocessing import Pool
from ref700 import *

PR = sieve(2_100_000); PS = set(PR)

def hyp_triples(pmax, pmin=3):
    out = []
    import bisect
    i0 = bisect.bisect_left(PR, pmin)
    for a in range(i0, len(PR)):
        p = PR[a]
        if p > pmax: break
        for b in range(a + 1, len(PR)):
            q = PR[b]
            if 2 * (q - p + 2) ** 2 >= p: break
            for c in range(b + 1, len(PR)):
                r = PR[c]
                if 2 * (r - p) ** 2 >= p: break
                if r - q > q - p: out.append((p, q, r))
    return out

def job(t):
    p, q, r = t
    f = f_enum2(t)
    return (p, q, r, f)

if __name__ == "__main__":
    t0 = time.time()
    STAGE = sys.argv[1] if len(sys.argv) > 1 else "all"
        # ---- B1: all hypothesis triples p <= 20000 ----
    if STAGE in ("all", "B1"):
        H = hyp_triples(20000)
        n6000 = sum(1 for t in H if t[0] <= 6000)
        print(f"B1 hypothesis triples: p<=6000: {n6000} (submitter/lead say 2952); p<=20000: {len(H)} (lead says 24601)")
        print(f"B1 smallest p: {H[:4]}")
        with Pool(8) as pool:
            res = pool.map(job, H, chunksize=20)
        bad_thm = [x for x in res if x[3] ** 2 <= x[0] * x[1] * x[2]]
        bad_c1 = [x for x in res if x[3] != x[0] * x[1]]
        print(f"B1 f computed exactly for {len(res)} triples: f<=sqrt n: {len(bad_thm)}; f != pq: {len(bad_c1)}  ({time.time()-t0:.0f}s)")
        for x in bad_thm[:20]: print("  THEOREM FAILS", x)
        for x in bad_c1[:20]: print("  C1 FAILS", x)
        # extreme e within B1
        def emax(p): return math.isqrt((p - 1) // 2)
        ext = [x for x in res if (x[2] - x[0]) >= emax(x[0]) - 1]
        print(f"B1 triples with e within 1 of the allowed max isqrt((p-1)/2): {len(ext)}, all f==pq: {all(x[3]==x[0]*x[1] for x in ext)}; e.g. {ext[:5]}")
        d2 = [x for x in res if x[1] - x[0] == 2]
        print(f"B1 triples with d=2: {len(d2)}, all f==pq: {all(x[3]==x[0]*x[1] for x in d2)}; largest h with d=2: {max(d2, key=lambda x: x[2]-x[1])}")
        sys.stdout.flush()

    if STAGE in ("all", "B23"):
        def emax(p): return math.isqrt((p - 1) // 2)
        # ---- B2: large-p edge cases ----
        edge = []
        for p0 in (50_000, 100_003, 300_000, 1_000_003, 2_000_003):
            # first (p, p+2, p+6) prime triple at or above p0 (d=2, h=4, e=6)
            p = next(x for x in PR if x >= p0 and x + 2 in PS and x + 6 in PS); edge.append((p, p + 2, p + 6))
        # max-e triples with p around 30k-100k (e near isqrt((p-1)/2)), one per start point, d=2 and d~e/2
        for p0 in (30_000, 60_000, 100_000):
            found = 0
            for p in (x for x in PR if x >= p0):
                E = emax(p); E -= E % 2
                for e in (E, E - 2):
                    r = p + e
                    if r not in PS: continue
                    for d in (2, e // 2 - (e // 2) % 2):
                        q = p + d
                        if q in PS and r - q > d: edge.append((p, q, r)); found += 1
                if found >= 2: break
        edge = sorted(set(edge))
        print(f"B2 edge triples: {edge}")
        with Pool(min(5, len(edge))) as pool:
            res2 = pool.map(job, edge)
        for (p, q, r, f) in res2:
            print(f"B2 {p},{q},{r} d={q-p} h={r-q} e={r-p} 2e^2<p:{2*(r-p)**2<p} f={f} f==pq:{f==p*q} f^2>n:{f*f>p*q*r}")
        sys.stdout.flush()

        # ---- B3: sharpness / necessity of each hypothesis ----
        # (i) h>d but 2e^2 >= p (just outside), with e^2 < 2p, p<=3000
        T = []
        for a, p in enumerate(PR):
            if p > 3000: break
            for b in range(a + 1, len(PR)):
                q = PR[b]
                if (q - p) ** 2 >= 2 * p: break
                for c in range(b + 1, len(PR)):
                    r = PR[c]; e = r - p
                    if e * e >= 2 * p: break
                    T.append((p, q, r))
        with Pool(5) as pool:
            res3 = pool.map(job, T, chunksize=50)
        def cls(p, q, r):
            d, h, e = q - p, r - q, r - p
            return ("h>d" if h > d else ("h=d" if h == d else "h<d"), "2e2<p" if 2*e*e < p else ("e2<p" if e*e < p else "e2<2p"))
        from collections import Counter
        tot = Counter(); above = Counter(); fp = Counter(); fpq = Counter()
        for (p, q, r, f) in res3:
            k = cls(p, q, r); tot[k] += 1
            if f * f > p * q * r: above[k] += 1
            if f == p: fp[k] += 1
            if f == p * q: fpq[k] += 1
        print("B3 prime triples p<=3000 with e^2<2p, by (gap order, size band): total / f>sqrt n / f==p / f==pq")
        for k in sorted(tot): print(f"   {k}: {tot[k]} / {above[k]} / {fp[k]} / {fpq[k]}")
        sm = [(p, q, r, f) for (p, q, r, f) in res3 if cls(p, q, r) == ("h>d", "e2<p") and f * f <= p * q * r][:8]
        print(f"B3 smallest failures with h>d and p/2 <= e^2 < p: {sm}")
        sm2 = [(p, q, r, f) for (p, q, r, f) in res3 if cls(p, q, r)[0] != "h>d" and cls(p,q,r)[1]=="2e2<p" and f * f > p * q * r][:8]
        print(f"B3 triples with h<=d, 2e^2<p and f>sqrt n (would show h>d is not necessary): {sm2}")
        print(f"B3 103*107*113: f={f_enum2((103,107,113))} sqrt n={math.isqrt(103*107*113)}")
        print(f"done {time.time()-t0:.0f}s")
