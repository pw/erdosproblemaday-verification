"""Independent replay of a tree manifest (second implementation of the decomposition check).
Rebuilds J(n,5,3) from frozensets (not tree.py's bitmask code), recomputes every node's residual set from scratch
from (F, excluded orbits along the root path), and checks:
  (a) root = common non-neighbours of v,u; v,u meet in exactly 4; P1 bound s+1 > floor(C(n,3)/10);
  (b) at every internal node: each generator (a b) is a transposition of [n] that maps the node's residual set onto
      itself (so it is an automorphism of the residual graph); the excluded set O equals the orbit of r under the
      group they generate (closure computed here); every generator maps the forced family F + {v,u} onto itself; r in O ⊆ R; include child = (F+[r], R ∩ Nbar(r), tau-1);
      exclude child = (F, R \\ O, tau);
  (c) every node has 0 or 2 children; leaves = nodes without children; leaves.txt lines = SOLVE leaves exactly,
      with tau = s-1-|F| and the recomputed residual sets; non-SOLVE leaves are UNSAT_SIZE with |R| < tau.
Prints REPLAY OK or raises."""
import sys, json, hashlib
from itertools import combinations
from math import comb
out = sys.argv[1]
man = json.load(open(out + '/manifest.json'))
n, s = man['n'], man['s']
V = [frozenset(c) for c in combinations(range(n), 5)]
I = {x: i for i, x in enumerate(V)}
N = len(V)
assert s + 1 > comb(n, 3) // 10
v, u = man['v'], man['u']
assert V[v] == frozenset(range(5)) and V[u] == frozenset([0, 1, 2, 3, 5]) and len(V[v] & V[u]) == 4
nonadjJ = lambda a, b: len(V[a] & V[b]) != 3            # 'adjacent in Gbar' for a != b
R0 = frozenset(w for w in range(N) if w not in (v, u) and nonadjJ(w, v) and nonadjJ(w, u))
assert len(R0) == man['R0_size']
nodes = {nd['id']: nd for nd in man['nodes']}
kids = {}
for nd in man['nodes']:
    if nd['parent'] is not None: kids.setdefault(nd['parent'], []).append(nd['id'])
def tperm(a, b):
    def f(w):
        S = V[w]
        return I[frozenset(b if x == a else a if x == b else x for x in S)]
    return f
Rof = {1: R0}
assert nodes[1]['F'] == [] and nodes[1]['tau'] == s - 1
order = sorted(nodes)
nint = 0
for i in order:
    nd = nodes[i]; R = Rof[i]
    assert len(R) == nd['size'], (i, len(R), nd['size'])
    ch = kids.get(i, [])
    if not ch:
        assert 'leaf' in nd; continue
    assert len(ch) == 2 and 'r' in nd; nint += 1
    r = nd['r']; assert r in R
    gens = [tperm(a, b) for (a, b) in nd['gens']]
    fam = frozenset(nd['F'] + [v, u])
    for (a, b), g in zip(nd['gens'], gens):
        assert 0 <= a < n and 0 <= b < n and a != b
        assert frozenset(g(w) for w in R) == R, f'generator does not preserve R at node {i}'
        # needed for the uniqueness classification: each branching permutation maps the forced family (with v,u) onto itself
        assert frozenset(g(w) for w in fam) == fam, f'generator does not fix the forced family at node {i}'
    orb = {r}; stack = [r]
    while stack:
        w = stack.pop()
        for g in gens:
            x = g(w)
            if x not in orb: orb.add(x); stack.append(x)
    assert orb <= R
    inc = [nodes[c] for c in ch if nodes[c]['kind'] == 'include'][0]
    exc = [nodes[c] for c in ch if nodes[c]['kind'] == 'exclude'][0]
    assert frozenset(exc['excluded_orbit']) == orb, f'orbit mismatch at node {i}'
    assert inc['F'] == nd['F'] + [r] and inc['tau'] == nd['tau'] - 1
    assert exc['F'] == nd['F'] and exc['tau'] == nd['tau']
    Rof[inc['id']] = frozenset(w for w in R if w != r and nonadjJ(w, r))
    Rof[exc['id']] = R - orb
# every forced family is independent in J and avoids v,u-adjacency
for i in order:
    F = nodes[i]['F']
    fam = F + [v, u]
    assert all(nonadjJ(a, b) for a, b in combinations(fam, 2)) and len(set(fam)) == len(fam)
    assert nodes[i]['tau'] == s - 1 - len(F)
# leaves file
lines = open(out + '/leaves.txt').read().splitlines()
assert hashlib.sha256(''.join(l + '\n' for l in lines).encode()).hexdigest() == man['leaves_sha256']
solve_ids = set()
for l in lines:
    t = list(map(int, l.split()))
    lid, tau, k, vs = t[0], t[1], t[2], [x - 1 for x in t[3:]]
    assert k == len(vs) and frozenset(vs) == Rof[lid] and len(vs) == len(set(vs))
    assert tau == nodes[lid]['tau'] and not kids.get(lid)
    solve_ids.add(lid)
leaves = [i for i in order if not kids.get(i)]
for i in leaves:
    if i not in solve_ids:
        assert nodes[i]['leaf'] == 'UNSAT_SIZE' and len(Rof[i]) < nodes[i]['tau'], i
# global complement graph file
g = open(out + '/gbar.col').read()
assert hashlib.sha256(g.encode()).hexdigest() == man['gbar_sha256']
E = set()
for line in g.splitlines():
    if line[0] == 'e':
        a, b = map(int, line.split()[1:]); E.add((a - 1, b - 1))
assert E == {(a, b) for a in range(N) for b in range(a + 1, N) if nonadjJ(a, b)}
print(f'REPLAY OK n={n} s={s} nodes={len(nodes)} internal={nint} leaves={len(leaves)} solve={len(solve_ids)} '
      f'size_pruned={len(leaves) - len(solve_ids)} gbar_edges={len(E)}')
