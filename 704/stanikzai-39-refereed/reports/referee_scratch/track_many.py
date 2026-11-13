"""Coverage control (referee's own code): random independent sets W containing v,u are carried down the tree.
At an internal node with exclude-orbit O and representative r: if W meets O, pick x in W∩O and build the explicit
ground permutation g in the Young subgroup of the components of the node's transposition graph with g(x)=r
(block by block: x∩B -> r∩B, B\\x -> B\\r), apply it to W, go to the include child; else go to the exclude child.
At the leaf: W' must be independent, contain F ∪ {v,u}, and W' \\ (F∪{v,u}) must lie in the leaf residual."""
import sys, json, random
from itertools import combinations
out, trials, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
man = json.load(open(out + '/manifest.json'))
n, v, u = man['n'], man['v'], man['u']
V = [frozenset(c) for c in combinations(range(n), 5)]; I = {x: i for i, x in enumerate(V)}; N = len(V)
nodes = {nd['id']: nd for nd in man['nodes']}
kids = {}
for nd in man['nodes']:
    if nd['parent'] is not None: kids.setdefault(nd['parent'], {})[nd['kind']] = nd['id']
leafR = {}
for l in open(out + '/leaves.txt'):
    t = list(map(int, l.split())); leafR[t[0]] = {x - 1 for x in t[3:]}
def comps(gens):
    par = list(range(n))
    def f(x):
        while par[x] != x: x = par[x]
        return x
    for a, b in gens: par[f(a)] = f(b)
    c = {}
    for x in range(n): c.setdefault(f(x), []).append(x)
    return list(c.values())
indep = lambda W: all(len(V[a] & V[b]) != 3 for a, b in combinations(W, 2))
cnt = {}; sizes = []
for t in range(trials):
    W = {v, u}; cand = list(range(N)); rng.shuffle(cand)
    for w in cand:
        if w not in W and all(len(V[w] & V[x]) != 3 for x in W): W.add(w)
    if rng.random() < 0.5:                       # also test non-maximal sets
        keep = rng.randint(2, len(W)); W = {v, u} | set(rng.sample(sorted(W - {v, u}), keep - 2))
    sizes.append(len(W)); cur = 1
    while cur in kids:
        nd = nodes[cur]; r = nd['r']; O = set(nodes[kids[cur]['exclude']]['excluded_orbit'])
        meet = sorted(W & O)
        if not meet: cur = kids[cur]['exclude']; continue
        x = rng.choice(meet); g = list(range(n))
        for B in comps(nd['gens']):
            xi = [e for e in B if e in V[x]]; xo = [e for e in B if e not in V[x]]
            ri = [e for e in B if e in V[r]]; ro = [e for e in B if e not in V[r]]
            assert len(xi) == len(ri), 'x not in orbit of r'
            for a, b in zip(xi + xo, ri + ro): g[a] = b
        W2 = {I[frozenset(g[e] for e in V[w])] for w in W}
        assert len(W2) == len(W) and r in W2 and {v, u} <= W2
        W = W2; cur = kids[cur]['include']
    F = set(nodes[cur]['F'])
    assert indep(W) and F <= W and {v, u} <= W, ('leaf invariant', cur)
    rest = W - F - {v, u}
    if cur in leafR: assert rest <= leafR[cur], ('rest not in leaf residual', cur)
    else: assert not rest, cur
    cnt[cur] = cnt.get(cur, 0) + 1
print(f'TRACK-MANY OK trials={trials} distinct_leaves_hit={len(cnt)} |W| min/max={min(sizes)}/{max(sizes)}')
