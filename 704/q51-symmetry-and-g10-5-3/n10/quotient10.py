"""21-colourings of G(10,5,3) invariant under a given permutation g of the 10 points (g of prime order q):
exact cover of the g-orbits of 5-sets by (a) g-invariant maximum independent sets, (b) g-orbits of maximum independent sets F
whose q images are pairwise disjoint (F meets every g-orbit at most once and contains no g-fixed 5-set).  CP-SAT.
Usage: quotient10.py "<cycle type e.g. 7,1,1,1>" [seconds] [comp]   (comp: compose g with complementation S -> [10]\\S)"""
import sys, json
from itertools import combinations
from ortools.sat.python import cp_model
N = 10
V = [frozenset(c) for c in combinations(range(N), 5)]; IDX = {s: i for i, s in enumerate(V)}
ct = [int(x) for x in sys.argv[1].split(',')]; assert sum(ct) == N
secs = float(sys.argv[2]) if len(sys.argv) > 2 else 300; comp = len(sys.argv) > 3 and sys.argv[3] == 'comp'
g = list(range(N)); pos = 0
for L in ct:
    for i in range(L): g[pos + i] = pos + (i + 1) % L
    pos += L
ALL = frozenset(range(N))
def act(i):
    s = frozenset(g[x] for x in V[i]);  return IDX[ALL - s] if comp else IDX[s]
gv = [act(i) for i in range(len(V))]
# order of the induced permutation on vertices
def order(p):
    o = 1; q = p[:]
    while q != list(range(len(p))): q = [p[x] for x in q]; o += 1
    return o
q = order(gv)
orb = [-1] * len(V); orbs = []
for i in range(len(V)):
    if orb[i] >= 0: continue
    o = []; x = i
    while orb[x] < 0: orb[x] = len(orbs); o.append(x); x = gv[x]
    orbs.append(o)
print(f'g cycle type {ct}{" + complement" if comp else ""}: order on vertices {q}; vertex orbits {len(orbs)} sizes {sorted(set(len(o) for o in orbs))}', flush=True)
allsets = json.load(open('mis10_all.json'))
inv = {}; free = {}
for F in allsets:
    Fs = frozenset(F); img = frozenset(gv[v] for v in F)
    if img == Fs: inv[frozenset(orb[v] for v in F)] = F
    else:
        os_ = [orb[v] for v in F]
        if len(set(os_)) == 12 and all(len(orbs[o]) == q for o in os_): free.setdefault(frozenset(os_), F)
print(f'invariant classes (distinct orbit-supports): {len(inv)}; free class-orbits (distinct supports): {len(free)}', flush=True)
m = cp_model.CpModel(); cand = [(k, F, 1) for k, F in inv.items()] + [(k, F, q) for k, F in free.items()]
x = [m.NewBoolVar(f'x{i}') for i in range(len(cand))]
cont = [[] for _ in orbs]
for i, (k, F, w) in enumerate(cand):
    for o in k: cont[o].append(x[i])
for o in range(len(orbs)): m.AddExactlyOne(cont[o]) if cont[o] else m.AddBoolOr([])
m.Add(sum(w * x[i] for i, (k, F, w) in enumerate(cand)) == 21)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = secs; sv.parameters.num_workers = 4
st = sv.Solve(m); print('status', sv.StatusName(st), 'wall', round(sv.WallTime(), 1), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    classes = []
    for i, (k, F, w) in enumerate(cand):
        if sv.Value(x[i]):
            cur = list(F)
            for _ in range(w): classes.append(sorted(cur)); cur = [gv[v] for v in cur]
    cov = sorted(v for c in classes for v in c)
    ok = len(classes) == 21 and cov == list(range(252)) and all(len(V[a] & V[b]) != 3 for c in classes for a, b in combinations(c, 2))
    print('21-colouring verified:', ok, flush=True)
    tag = sys.argv[1].replace(',', '_') + ('_comp' if comp else '')
    json.dump(dict(g=g, comp=comp, classes=[[sorted(V[v]) for v in c] for c in classes]), open(f'colouring21_sym_{tag}.json', 'w'))
