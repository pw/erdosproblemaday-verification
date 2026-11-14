"""Number of orbits of Sym(10) on the 285,600 maximum independent sets of J(10,5,3) (union-find over two generators),
and the orbit sizes; also orbits under Sym(10) x complementation."""
import json
from itertools import combinations
from collections import Counter
N = 10
V = [frozenset(c) for c in combinations(range(N), 5)]; IDX = {s: i for i, s in enumerate(V)}
allsets = [tuple(s) for s in json.load(open('mis10_all.json'))]; pos = {s: i for i, s in enumerate(allsets)}
def vperm(p): return [IDX[frozenset(p[x] for x in s)] for s in V]
g1 = vperm([1, 0] + list(range(2, N))); g2 = vperm([(x + 1) % N for x in range(N)])
comp = [IDX[frozenset(range(N)) - s] for s in V]
par = list(range(len(allsets)))
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
def run(gens):
    global par; par = list(range(len(allsets)))
    for i, s in enumerate(allsets):
        for g in gens:
            j = pos[tuple(sorted(g[v] for v in s))]
            a, b = find(i), find(j)
            if a != b: par[a] = b
    return Counter(find(i) for i in range(len(allsets)))
c1 = run([g1, g2]); print('orbits under Sym(10):', len(c1), 'sizes', sorted(c1.values()))
c2 = run([g1, g2, comp]); print('orbits under Sym(10) x complement:', len(c2), 'sizes', sorted(c2.values()))
