"""Carry many images of the paper's 33-set (each normalised so an ordered pair meeting in 4 becomes (v,u)) down the
s=33 tree; collect the leaves they land in; write those leaves with tau-1 (must be SAT) to lv_minus1.txt."""
import sys, json, random
from itertools import combinations
out = sys.argv[1]; rng = random.Random(5)
man = json.load(open(out + '/manifest.json')); n, v, u = man['n'], man['v'], man['u']
V = [frozenset(c) for c in combinations(range(n), 5)]; I = {x: i for i, x in enumerate(V)}
W0 = [{1,2,3,4,5},{1,2,3,4,6},{1,2,3,5,6},{1,2,4,5,6},{1,3,4,5,6},{2,3,4,5,6},{3,6,9,10,12},{3,6,9,10,13},{3,6,9,12,13},{3,6,10,12,13},{3,9,10,12,13},{6,9,10,12,13},{4,5,7,8,9},{4,5,7,8,10},{4,5,7,9,10},{4,5,8,9,10},{4,7,8,9,10},{5,7,8,9,10},{1,3,7,11,12},{1,4,7,11,12},{1,5,7,11,12},{1,6,7,11,12},{1,7,9,11,12},{1,7,10,11,12},{1,2,8,11,13},{2,3,8,11,13},{2,4,8,11,13},{2,5,8,11,13},{2,6,8,11,13},{2,7,8,11,13},{2,8,9,11,13},{2,8,10,11,13},{2,8,11,12,13}]
W0 = [frozenset(x - 1 for x in s) for s in W0]
assert len(set(W0)) == 33 and all(len(a & b) != 3 for a, b in combinations(W0, 2))
nodes = {nd['id']: nd for nd in man['nodes']}
kids = {}
for nd in man['nodes']:
    if nd['parent'] is not None: kids.setdefault(nd['parent'], {})[nd['kind']] = nd['id']
leafline = {int(l.split()[0]): l for l in open(out + '/leaves.txt')}
def comps(gens):
    par = list(range(n))
    def f(x):
        while par[x] != x: x = par[x]
        return x
    for a, b in gens: par[f(a)] = f(b)
    c = {}
    for x in range(n): c.setdefault(f(x), []).append(x)
    return list(c.values())
hit = {}
pairs = [(A, B) for A in W0 for B in W0 if len(A & B) == 4]
for (A, B) in pairs:
    for rep in range(3):
        C = sorted(A & B); a = list(A - B)[0]; b = list(B - A)[0]; rest = [x for x in range(n) if x not in A | B]
        rng.shuffle(C); rng.shuffle(rest)
        g = [0] * n
        for x, y in zip(C + [a, b] + rest, [0, 1, 2, 3, 4, 5] + list(range(6, n))): g[x] = y
        W = {I[frozenset(g[e] for e in s)] for s in W0}; assert v in W and u in W
        cur = 1
        while cur in kids:
            nd = nodes[cur]; r = nd['r']; O = set(nodes[kids[cur]['exclude']]['excluded_orbit'])
            meet = sorted(W & O)
            if not meet: cur = kids[cur]['exclude']; continue
            x = rng.choice(meet); h = list(range(n))
            for Bk in comps(nd['gens']):
                xi = [e for e in Bk if e in V[x]]; xo = [e for e in Bk if e not in V[x]]
                ri = [e for e in Bk if e in V[r]]; ro = [e for e in Bk if e not in V[r]]
                for p, q in zip(xi + xo, ri + ro): h[p] = q
            W = {I[frozenset(h[e] for e in V[w])] for w in W}; cur = kids[cur]['include']
        F = set(nodes[cur]['F']); R = {int(z) - 1 for z in leafline[cur].split()[3:]}
        assert F <= W and (W - F - {v, u}) <= R and len(W - F - {v, u}) == nodes[cur]['tau'] - 1
        hit[cur] = hit.get(cur, 0) + 1
with open('/tmp/ref704/lv_minus1.txt', 'w') as f:
    for lid in sorted(hit):
        t = leafline[lid].split(); t[1] = str(int(t[1]) - 1); f.write(' '.join(t) + '\n')
print('pairs', len(pairs), 'images', 3 * len(pairs), 'distinct leaves hit', len(hit), sorted(hit.items()))
