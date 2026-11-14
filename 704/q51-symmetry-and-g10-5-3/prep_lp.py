"""Tables for the conditioned LP: fix class 1 = W (Appendix A). Aut(W), its orbits on points / 4-sets / 5-sets outside W."""
from itertools import combinations, permutations, product
from wstruct import WA, copy_from_roles
N = 13
ROLE = dict(inf=10, a=(0, 11, 6), b=(1, 12, 7), S=((2, 5), (3, 4), (8, 9)))   # S12, S13, S23
# Aut(W) by brute force over role-preserving relabellings, then checked to fix W; count must be 48
auts = []
pairs_idx = {0: (0, 1), 1: (0, 2), 2: (1, 2)}          # S[0]=S12, S[1]=S13, S[2]=S23
for sg in permutations(range(3)):
    for eps in product((0, 1), repeat=3):
        p = list(range(N))
        for i in range(3):
            p[ROLE['a'][i]] = ROLE['a'][sg[i]]; p[ROLE['b'][i]] = ROLE['b'][sg[i]]
        for t in range(3):
            i, j = pairs_idx[t]; tgt = tuple(sorted((sg[i], sg[j])))
            t2 = [k for k, v in pairs_idx.items() if v == tgt][0]
            src, dst = ROLE['S'][t], ROLE['S'][t2]
            if eps[t]: dst = dst[::-1]
            p[src[0]] = dst[0]; p[src[1]] = dst[1]
        assert sorted(p) == list(range(N))
        assert {frozenset(p[x] for x in s) for s in WA} == WA
        auts.append(tuple(p))
assert len(set(auts)) == 48
def orbits(objs):
    seen = {}; reps = []
    for o in objs:
        if o in seen: continue
        orb = {frozenset(p[x] for x in o) for p in auts}
        for q in orb: seen[q] = len(reps)
        reps.append(sorted(orb, key=sorted))
    return seen, reps
V5 = [frozenset(c) for c in combinations(range(N), 5)]
V4 = [frozenset(c) for c in combinations(range(N), 4)]
V6 = [frozenset(c) for c in combinations(range(N), 6)]
out5, reps5 = orbits([s for s in V5 if s not in WA])
o4, reps4 = orbits(V4)
o6, reps6 = orbits(V6)
opt, repspt = orbits([frozenset([x]) for x in range(N)])
mask = lambda s: sum(1 << x for x in s)
with open('tables.txt', 'w') as f:
    f.write(f'{len(reps5)} {len(reps4)} {len(reps6)} {len(repspt)}\n')
    for s in V5: f.write(f'5 {mask(s)} {out5.get(s, -1)}\n')
    for s in V4: f.write(f'4 {mask(s)} {o4[s]}\n')
    for s in V6: f.write(f'6 {mask(s)} {o6[s]}\n')
    for x in range(N): f.write(f'1 {x} {opt[frozenset([x])]}\n')
import json
json.dump(dict(n5=len(reps5), n4=len(reps4), n6=len(reps6), npt=len(repspt),
               size5=[len(r) for r in reps5], size4=[len(r) for r in reps4], size6=[len(r) for r in reps6], sizept=[len(r) for r in repspt],
               rep5=[sorted(r[0]) for r in reps5], rep4=[sorted(r[0]) for r in reps4], rep6=[sorted(r[0]) for r in reps6],
               reppt=[sorted(r[0]) for r in repspt], auts=auts), open('orbits.json', 'w'))
print('Aut(W) = 48 OK; orbits on 5-sets outside W:', len(reps5), 'sizes sum', sum(len(r) for r in reps5),
      '; on 4-sets:', len(reps4), '; on 6-sets:', len(reps6), '; on points:', [len(r) for r in repspt])
