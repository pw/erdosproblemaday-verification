#!/usr/bin/env python3
"""Check 6: Lemma 2.4 (unequal column bounds): for R1 >= R2 >= R3 >= 1, t != 0,
   #{(u1,u2,u3) in (Z^3)^3 : |u_j| <= R_j, det(u1,u2,u3) = t}  <=  C (R1R2R3)^2 (log 2R1)^2.
Exact counts via det = u1 . (u2 x u3), grouping (u2,u3) by their cross product.
Instrument control: direct triple enumeration for radii <= 3 must agree exactly.
Reported: ratio count / ((R1R2R3)^2 (log 2R1)^2) over radii up to 8 and several t (bounded is the claim;
finite data can only show no growth).
Mutations: (i) bound with one power of R3 removed, (R1R2)^2 R3 (log 2R1)^2 -> ratio must grow with R3;
(ii) t = 0 (excluded by the lemma) for contrast.
"""
import itertools, math, time
import numpy as np

def ball(R):
    m = int(math.floor(R))
    ax = np.arange(-m, m + 1, dtype=np.int64)
    X = np.array(np.meshgrid(ax, ax, ax, indexing='ij')).reshape(3, -1).T
    return X[(X * X).sum(axis=1) <= R * R]

def counts(R1, R2, R3, ts):
    b1, b2, b3 = ball(R1), ball(R2), ball(R3)
    u2 = np.repeat(b2, len(b3), axis=0); u3 = np.tile(b3, (len(b2), 1))
    n = np.cross(u2, u3)
    un, cnt = np.unique(n, axis=0, return_counts=True)
    out = {t: 0 for t in ts}
    CH = 4000
    for s in range(0, len(un), CH):
        dots = b1 @ un[s:s + CH].T          # (|b1|, chunk)
        c = cnt[s:s + CH]
        for t in ts:
            out[t] += int(((dots == t).sum(axis=0) * c).sum())
    return out

def brute(R1, R2, R3, ts):
    b1, b2, b3 = ball(R1), ball(R2), ball(R3)
    out = {t: 0 for t in ts}
    for u1 in b1:
        n = np.cross(b2[:, None, :], b3[None, :, :]).reshape(-1, 3)
        d = n @ u1
        for t in ts: out[t] += int((d == t).sum())
    return out

def main():
    t0 = time.time()
    ts = [1, 2, 3, 5, 6, 12, 30, 60, 0]
    # instrument control
    for rad in ((2, 2, 2), (3, 2, 1), (3, 3, 3)):
        a = counts(*rad, ts); b = brute(*rad, ts)
        print(f"control radii {rad}: grouped == brute force: {a == b}  (t=1 count {a[1]}, t=0 count {a[0]})")
    print(f"[{time.time()-t0:.0f}s]")
    configs = [(R, R, R) for R in (2, 3, 4, 5, 6, 7, 8)] + \
              [(8, 8, 1), (8, 8, 2), (8, 8, 4), (8, 4, 1), (8, 4, 2), (8, 2, 1), (8, 1, 1), (6, 6, 3), (8, 6, 3), (8, 8, 6)]
    rows = []
    worst = 0.0
    for (R1, R2, R3) in configs:
        c = counts(R1, R2, R3, ts)
        norm = (R1 * R2 * R3) ** 2 * math.log(2 * R1) ** 2
        mut = (R1 * R2) ** 2 * R3 * math.log(2 * R1) ** 2
        rat = {t: c[t] / norm for t in ts}
        nz = max(rat[t] for t in ts if t != 0)
        worst = max(worst, nz)
        rows.append(((R1, R2, R3), c, rat))
        print(f"radii {(R1,R2,R3)}: max_t!=0 count/((R1R2R3)^2 log^2 2R1) = {nz:.4f}; "
              f"t=1: {c[1]} ({rat[1]:.4f}); t=60: {c[60]} ({rat[60]:.4f}); "
              f"t=0 contrast: {rat[0]:.4f}; MUTATION (R1R2)^2 R3 ratio (t=1): {c[1]/mut:.4f}  [{time.time()-t0:.0f}s]", flush=True)
    print(f"\nPOSITIVE: worst ratio over all configs and t != 0: {worst:.4f}")
    print("MUTATION drop one power of R3: ratio count(t=1)/((R1R2)^2 R3 log^2) at R1=R2=8, R3=1,2,4,6,8:")
    for (R1, R2, R3) in ((8, 8, 1), (8, 8, 2), (8, 8, 4), (8, 8, 6), (8, 8, 8)):
        r = next(x for x in rows if x[0] == (R1, R2, R3))
        print(f"   R3={R3}: {r[1][1] / ((R1*R2)**2 * R3 * math.log(2*R1)**2):.4f}   (paper-normalised: {r[2][1]:.4f})")

if __name__ == "__main__":
    main()
