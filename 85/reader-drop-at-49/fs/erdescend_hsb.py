#!/usr/bin/env python3
"""Production-scale witness test for the HIGH-PERMUTATION SB (extends the referee's erdescend.py, ref/).
ER(q) with S = pairwise non-adjacent passant points as highs (degree q+1; R1/R1b are theorems there).
Generators: class transpositions (all pairs) + every permutation sigma of S (searched over Sym(S) for |S| <= 7)
that maps the multiset of (block, target) to itself, turned into vertex permutations exactly as fsenc does.
Descend ER(q) by any generator g with X o g <lex X until no generator improves; the FULL CNF (base + R1 + R1b +
class SB + add_perm_sb for those perms) must ACCEPT the descended graph.  Discriminating: also report whether
the raw ER(q) (not a local leader) is rejected."""
import itertools, sys
sys.path.insert(0, '/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
from pysat.solvers import Cadical153
q = int(sys.argv[1]); nh = int(sys.argv[2]); skip = int(sys.argv[3]) if len(sys.argv) > 3 else 0
pts = []
for v in itertools.product(range(q), repeat=3):
    if v == (0, 0, 0): continue
    f = next(z for z in v if z); inv = pow(f, q - 2, q); w = tuple(z * inv % q for z in v)
    if w not in pts: pts.append(w)
n = len(pts); dot = lambda u, v: sum(a * b for a, b in zip(u, v)) % q
E = [(i, j) for i, j in itertools.combinations(range(n), 2) if dot(pts[i], pts[j]) == 0]
adj = {v: set() for v in range(n)}
for i, j in E: adj[i].add(j); adj[j].add(i)
deg = [len(adj[v]) for v in range(n)]
ab = {i for i in range(n) if dot(pts[i], pts[i]) == 0}
passant = [x for x in range(n) if x not in ab and not (adj[x] & ab)]
S = []
for x in passant[skip:]:
    if all(x not in adj[y] for y in S) and len(S) < nh: S.append(x)
fixed = [e for e in E if e[0] in S or e[1] in S]
target = {v: deg[v] for v in range(n) if v not in S}
cnf, var, F, adjS, st, cls = fsenc.build(n, S, fixed, target, highs=S, sb="all", r1=True, r1b=True, hdeg=q + 1)
lows = [v for v in range(n) if v not in S]
key = {v: (frozenset(adjS[v]), deg[v]) for v in lows}
perms = []
for img in itertools.permutations(S):
    sig = dict(zip(S, img))
    if all(sig[s] == s for s in S): continue
    slots = {}
    for v in lows: slots.setdefault(key[v], []).append(v)
    pi = {s: sig[s] for s in S}; ok = True; used = {k: 0 for k in slots}
    for v in lows:
        k2 = (frozenset(sig[s] for s in key[v][0]), key[v][1])
        if k2 not in slots or used[k2] >= len(slots[k2]): ok = False; break
        pi[v] = slots[k2][used[k2]]; used[k2] += 1
    if ok: perms.append([pi[v] for v in range(n)])
top = max([abs(l) for c in cnf.clauses for l in c] + [len(var)])
top, nc = fsenc.add_perm_sb(cnf, var, n, perms, top)
order = sorted(var)
X = {e for e in E if e[0] not in S and e[1] not in S}
vec = lambda X: [1 if e in X else 0 for e in order]
gens = []
for C in cls:
    for i, j in itertools.combinations(C, 2):
        t = list(range(n)); t[i], t[j] = j, i; gens.append(t)
gens += perms
steps = 0
while True:
    cur = vec(X); moved = False
    for g in gens:
        Y = {e for e in order if tuple(sorted((g[e[0]], g[e[1]]))) in X}   # Y_p = X_{g(p)}
        if vec(Y) < cur:
            X = Y; moved = True; steps += 1; break
    if not moved: break
d2, mc = c4cnf.check_graph(n, fixed + list(X))
with Cadical153(bootstrap_with=cnf.clauses) as s:
    okfull = s.solve(assumptions=[var[e] if e in X else -var[e] for e in var])
    orig = {e for e in E if e[0] not in S and e[1] not in S}
    okorig = s.solve(assumptions=[var[e] if e in orig else -var[e] for e in var])
print(f"ER({q}) n={n} highs={len(S)} classes={st['sb_classes']} high_perms={len(perms)} perm_clauses={nc} descent_steps={steps} "
      f"descended_valid={all(d2[u] == deg[u] for u in range(n)) and mc == 1} FULL_CNF_accepts_descended={okfull} raw_ER_accepted={okorig}", flush=True)
