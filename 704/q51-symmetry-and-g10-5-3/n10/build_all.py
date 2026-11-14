"""Build mis10_all.json (all 285,600 maximum independent sets of J(10,5,3), as sorted vertex-index tuples in
itertools.combinations(range(10), 5) order) from mis10_v0.json (the 13,600 that contain {0,1,2,3,4}; written by mis10.py)."""
import json, random
from itertools import combinations
N = 10
V = [frozenset(c) for c in combinations(range(N), 5)]; IDX = {s: i for i, s in enumerate(V)}
base = json.load(open('mis10_v0.json'))
allsets = set()
for tgt in V:
    rest = [x for x in range(N) if x not in tgt]; p = dict(zip(range(5), sorted(tgt))); p.update(dict(zip(range(5, 10), rest)))
    for F in base:
        allsets.add(frozenset(IDX[frozenset(p[x] for x in V[i])] for i in F))
allsets = sorted(tuple(sorted(s)) for s in allsets)
assert len(allsets) == 285600
assert all(len(V[a] & V[b]) != 3 for s in random.sample(allsets, 300) for a, b in combinations(s, 2))
json.dump(allsets, open('mis10_all.json', 'w')); print('maximum independent sets:', len(allsets))
