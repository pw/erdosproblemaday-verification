"""Count ALL proper 21-colourings of J(10,5,3) invariant under g = (0 1 2 3 4 5 6)(7)(8)(9).
g fixes no 5-set, and no maximum independent set is g-invariant (12 is not a multiple of 7), so such a colouring is three
g-orbits of classes; each base class meets 12 distinct g-orbits of 5-sets, and the three supports partition the 36 orbits."""
import json
from itertools import combinations
from collections import defaultdict
N = 10
V = [frozenset(c) for c in combinations(range(N), 5)]; IDX = {s: i for i, s in enumerate(V)}
g = [(x + 1) % 7 if x < 7 else x for x in range(N)]
gv = [IDX[frozenset(g[x] for x in s)] for s in V]
orb = [-1] * len(V); no = 0
for i in range(len(V)):
    if orb[i] >= 0: continue
    x = i
    while orb[x] < 0: orb[x] = no; x = gv[x]
    no += 1
assert no == 36
allsets = json.load(open('mis10_all.json'))
by_support = defaultdict(set)      # support mask -> set of class-orbits (canonical: min over the 7 shifts)
for F in allsets:
    os_ = {orb[v] for v in F}
    if len(os_) != 12: continue
    cur = tuple(sorted(F)); best = cur
    for _ in range(6):
        cur = tuple(sorted(gv[v] for v in cur)); best = min(best, cur)
    by_support[sum(1 << o for o in os_)].add(best)
masks = list(by_support); mult = {m: len(by_support[m]) for m in masks}
print('supports:', len(masks), '; class-orbits:', sum(mult.values()))
full = (1 << 36) - 1; total = 0; triples = 0
has0 = [m for m in masks if m & 1]
for m1 in has0:
    for m2 in masks:
        if m1 & m2: continue
        m3 = full ^ m1 ^ m2
        if m2 < m3 and m3 in mult: triples += 1; total += mult[m1] * mult[m2] * mult[m3]
print('support triples partitioning the 36 orbits:', triples, '; colourings invariant under g:', total)
