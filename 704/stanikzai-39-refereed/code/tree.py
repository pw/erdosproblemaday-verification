"""Our own orbital-branching decomposition for 'α(J(n,5,3)) ≤ s', after the pair reduction.

Route (shares no code with the submission; a DIFFERENT tree built with the SAME technique, orbital branching, from a different root):
  P1  a family of 5-subsets of [n] with pairwise intersections ≤ 2 has ≤ ⌊C(n,3)/10⌋ members;
      so if s+1 > ⌊C(n,3)/10⌋, any independent set of size s+1 has two members meeting in exactly 4.
  P2  Sym(n) is transitive on ordered pairs of 5-sets meeting in 4  ⇒  WLOG v={0,1,2,3,4}, u={0,1,2,3,5} ∈ I.
  P3  α ≤ s  ⇔  no clique of size s−1 in Gbar[R], R = {w ≠ v,u : |w∩v| ≠ 3, |w∩u| ≠ 3}, Gbar = complement of J.
  P4  orbital branching (Ostrowski et al.) with the Young subgroup of a partition of [n], generators = adjacent
      transpositions inside blocks, every generator CHECKED to be an automorphism of J mapping the node's residual
      set onto itself. Branch vertex: RULE 'largest' (used for every published run) = a vertex of a largest orbit
      (ties: max residual degree, then smallest index); RULE 'maxdeg' = a max-degree vertex (abandoned: 17,552 leaves).
Usage: python3 tree.py n s LEAFMAX outdir
"""
import sys, json, os, hashlib
from itertools import combinations
from math import comb

n, s, LEAFMAX, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
RULE = sys.argv[5] if len(sys.argv) > 5 else 'maxdeg'   # 'maxdeg' or 'largest' (largest orbit, ties: max degree, then smallest index)
DMAX = 40
assert s + 1 > comb(n, 3) // 10, "pair reduction P1 does not apply"
V = [sum(1 << x for x in c) for c in combinations(range(n), 5)]
idx = {m: i for i, m in enumerate(V)}
N = len(V)
pc = lambda x: bin(x).count('1')
adjJ = [0] * N
for i in range(N):
    for j in range(N):
        if i != j and pc(V[i] & V[j]) == 3:
            adjJ[i] |= 1 << j
FULL = (1 << N) - 1
adjG = [(FULL & ~adjJ[i]) & ~(1 << i) for i in range(N)]       # complement graph Gbar
v, u = idx[0b11111], idx[0b101111]
assert pc(V[v] & V[u]) == 4
R0 = FULL & ~adjJ[v] & ~adjJ[u] & ~(1 << v) & ~(1 << u)
tau0 = (s + 1) - 2

def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b

_permcache = {}
def vperm(a, b):
    """vertex permutation induced by the transposition (a b) of [n]; checked to be an automorphism of J."""
    key = (a, b)
    if key not in _permcache:
        def img(m):
            ba, bb = (m >> a) & 1, (m >> b) & 1
            m &= ~((1 << a) | (1 << b))
            return m | (ba << b) | (bb << a)
        p = [idx[img(m)] for m in V]
        # automorphism check of J: adjacency preserved for every vertex
        for i in range(N):
            im = 0
            for j in bits(adjJ[i]):
                im |= 1 << p[j]
            assert im == adjJ[p[i]], "generator is not an automorphism of J"
        _permcache[key] = p
    return _permcache[key]

def image(R, p):
    im = 0
    for j in bits(R):
        im |= 1 << p[j]
    return im

def refine(part, m):
    newp = []
    for B in part:
        b1 = [x for x in B if (m >> x) & 1]
        b2 = [x for x in B if not (m >> x) & 1]
        newp += [b for b in (b1, b2) if b]
    return newp

root_part = [[0, 1, 2, 3], [4, 5], list(range(6, n))]
nodes = [dict(id=1, parent=None, kind='root', F=[], R=R0, tau=tau0, part=root_part, depth=0)]
import heapq, time
T0=time.time()
frontier = [(-pc(R0), 1, 0)]
leaves = []
internal = []
while frontier:
    _, _, k = heapq.heappop(frontier)
    if len(nodes) % 20000 < 2: print('progress nodes', len(nodes), 'leaves', len(leaves), 'frontier', len(frontier), 'maxR', -frontier[0][0] if frontier else 0, round(time.time()-T0,1), flush=True)
    nd = nodes[k]
    R, tau = nd['R'], nd['tau']
    size = pc(R)
    if tau <= 0:
        nd['leaf'] = 'SAT_TRIVIAL'; leaves.append(k); continue
    if size < tau:
        nd['leaf'] = 'UNSAT_SIZE'; leaves.append(k); continue
    if size <= LEAFMAX or nd['depth'] >= DMAX:
        nd['leaf'] = 'SOLVE'; leaves.append(k); continue
    gens = [(B[i], B[i + 1]) for B in nd['part'] for i in range(len(B) - 1)]
    # check every generator maps R onto itself
    for (a, b) in gens:
        assert image(R, vperm(a, b)) == R, f"generator ({a} {b}) does not preserve R at node {nd['id']}"
    # orbits by union-find
    par = {}
    def find(x):
        while par.get(x, x) != x:
            par[x] = par.get(par[x], par[x]); x = par[x]
        return x
    for (a, b) in gens:
        p = vperm(a, b)
        for j in bits(R):
            ra, rb = find(j), find(p[j])
            if ra != rb: par[max(ra, rb)] = min(ra, rb)
    # branch vertex: max degree in Gbar[R]
    if RULE == 'maxdeg':
        r = max(bits(R), key=lambda j: (pc(adjG[j] & R), -j))
    else:
        osz = {}
        for j in bits(R): osz[find(j)] = osz.get(find(j), 0) + 1
        r = max(bits(R), key=lambda j: (osz[find(j)], pc(adjG[j] & R), -j))
    rr = find(r)
    O = 0
    for j in bits(R):
        if find(j) == rr: O |= 1 << j
    assert (O >> r) & 1 and (O & ~R) == 0
    nd.update(r=r, orbit_size=pc(O), gens=gens)
    internal.append(k)
    inc = dict(id=len(nodes) + 1, parent=nd['id'], kind='include', F=nd['F'] + [r], R=R & adjG[r],
               tau=tau - 1, part=refine(nd['part'], V[r]), depth=nd['depth'] + 1)
    exc = dict(id=len(nodes) + 2, parent=nd['id'], kind='exclude', F=nd['F'], R=R & ~O,
               tau=tau, part=nd['part'], depth=nd['depth'] + 1, excluded_orbit=sorted(bits(O)))
    nodes.append(inc); nodes.append(exc)
    heapq.heappush(frontier, (-pc(inc['R']), inc['id'], len(nodes) - 2))
    heapq.heappush(frontier, (-pc(exc['R']), exc['id'], len(nodes) - 1))

os.makedirs(out, exist_ok=True)
gtxt = []
for a in range(N):
    for b in bits(adjG[a]):
        if a < b: gtxt.append(f"e {a+1} {b+1}\n")
gtxt = f"p edge {N} {len(gtxt)}\n" + ''.join(gtxt)
open(out + '/gbar.col', 'w').write(gtxt)
man = dict(rule=RULE, n=n, s=s, tau0=tau0, v=v, u=u, LEAFMAX=LEAFMAX, N=N, R0_size=pc(R0), gbar_sha256=hashlib.sha256(gtxt.encode()).hexdigest(), nodes=[], leaves=[])
for nd in nodes:
    rec = dict(id=nd['id'], parent=nd['parent'], kind=nd['kind'], F=nd['F'], tau=nd['tau'], size=pc(nd['R']), depth=nd['depth'])
    if 'r' in nd: rec.update(r=nd['r'], orbit_size=nd['orbit_size'], gens=nd['gens'])
    if 'excluded_orbit' in nd: rec['excluded_orbit'] = nd['excluded_orbit']
    if 'leaf' in nd: rec['leaf'] = nd['leaf']
    man['nodes'].append(rec)
nsolve = 0
lines = []
for k in sorted(leaves, key=lambda k: nodes[k]['id']):
    nd = nodes[k]
    if nd['leaf'] != 'SOLVE':
        man['leaves'].append(dict(id=nd['id'], status=nd['leaf'], size=pc(nd['R']), tau=nd['tau'], F=nd['F'])); continue
    verts = list(bits(nd['R']))
    lines.append(f"{nd['id']} {nd['tau']} {len(verts)} " + ' '.join(str(x + 1) for x in verts) + "\n")
    man['leaves'].append(dict(id=nd['id'], status='SOLVE', size=len(verts), tau=nd['tau'], F=nd['F']))
    nsolve += 1
ltxt = ''.join(lines)
open(out + '/leaves.txt', 'w').write(ltxt)
man['leaves_sha256'] = hashlib.sha256(ltxt.encode()).hexdigest()
json.dump(man, open(out + '/manifest.json', 'w'))
from collections import Counter
print('nodes', len(nodes), 'internal', len(internal), 'leaves', len(leaves), 'to_solve', nsolve,
      Counter(nodes[k]['leaf'] for k in leaves))
sz = sorted(pc(nodes[k]['R']) for k in leaves if nodes[k]['leaf'] == 'SOLVE')
print('leaf sizes min/median/max', sz[0] if sz else None, sz[len(sz)//2] if sz else None, sz[-1] if sz else None)
