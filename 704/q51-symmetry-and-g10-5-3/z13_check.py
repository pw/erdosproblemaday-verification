"""Second instrument for S3 (no code shared with z13.c): enumerate the copies of W with INF = 0 through wstruct's role
description, keep those meeting 33 distinct Z13-orbits, search exact 3-covers of the 99 orbits with numpy.
Orbit ids come from a canonical-translate dictionary on frozensets (z13.c uses rotated bitmasks)."""
import sys, numpy as np
from itertools import combinations, permutations
from multiprocessing import Pool
N = 13
def canon(s): return min(tuple(sorted((x + c) % N for x in s)) for c in range(N))
V = [frozenset(c) for c in combinations(range(N), 5)]
reps = sorted({canon(s) for s in V}); OID = {r: i for i, r in enumerate(reps)}; assert len(reps) == 99
ORB = {s: OID[canon(s)] for s in V}
def pairings(pts):
    if not pts: yield []; return
    a = pts[0]
    for i in range(1, len(pts)):
        for rest in pairings(pts[1:i] + pts[i + 1:]): yield [(a, pts[i])] + rest
def work(A):
    out = []; others = [x for x in range(1, N) if x not in A]; hist = {}
    for Bs in combinations(others, 3):
        sh = [x for x in others if x not in Bs]
        core6 = frozenset((0,) + A); core9 = frozenset((0,) + Bs)
        sun = [ORB[core6 | {x}] for x in sh] + [ORB[core9 | {y}] for y in range(N) if y not in core9]
        sunset = set(sun)
        for b in permutations(Bs):
            for pr in pairings(sh):
                for S12, S13, S23 in permutations(pr):
                    blocks = (frozenset((A[0], b[0]) + S12 + S13), frozenset((A[1], b[1]) + S12 + S23), frozenset((A[2], b[2]) + S13 + S23))
                    orbs = set(sunset)
                    for B in blocks:
                        for x in B: orbs.add(ORB[B - {x}])
                    d = len(orbs); hist[d] = hist.get(d, 0) + 1
                    if d == 33 and len(sunset) == 15:
                        m = sum(1 << o for o in orbs); out.append((m & (2**64 - 1), m >> 64))
    return out, hist
if __name__ == '__main__':
    with Pool(5) as p: res = p.map(work, list(combinations(range(1, N), 3)), chunksize=4)
    hist = {}; kept = []
    for out, h in res:
        kept += out
        for k, v in h.items(): hist[k] = hist.get(k, 0) + v
    print('copies with INF=0:', sum(hist.values()), '; histogram tail:', {k: hist[k] for k in sorted(hist)[-4:]}, '; kept:', len(kept), flush=True)
    lo = np.array([k[0] for k in kept], dtype=np.uint64); hi = np.array([k[1] for k in kept], dtype=np.uint64)
    FL = np.uint64(2**64 - 1); FH = np.uint64(2**35 - 1); S = set(kept); sols = 0; pairs = 0
    for i in range(len(kept)):
        dis = np.nonzero(((lo & lo[i]) == 0) & ((hi & hi[i]) == 0))[0]
        pairs += len(dis)
        for j in dis:
            rl = int(FL ^ lo[i] ^ lo[j]); rh = int(FH ^ hi[i] ^ hi[j])
            if (rl, rh) in S: sols += 1
    print('ordered disjoint pairs:', pairs, '; ordered exact 3-covers (i,j,rest):', sols)
