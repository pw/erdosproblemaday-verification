#!/usr/bin/env python3
"""Positive control for h1norm.py's construction, on ER(7): x passant (degree 8, N(x) a perfect matching, every other
vertex has exactly one neighbour in N(x) -- the same anchor structure, with groups of 6 instead of 5 and targets 7/8).
Relabel exactly as h1norm does (x=0, N(x)=1..8 matched 1-2,3-4,5-6,7-8, B_i consecutive, sorted by target), fix all
edges at 0..8, free = the 48 others.  SB = class transpositions (same B_i, same target) + every matching-preserving
permutation of 1..8 whose induced map on the B_i preserves targets.  Lex-descend ER(7) by the generators; the CNF
must ACCEPT the descended graph and (discriminating) REJECT raw ER(7) if raw is not already a local leader."""
import itertools, sys
sys.path.insert(0, '/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
from pysat.solvers import Cadical153
q = 7
pts = []
for v in itertools.product(range(q), repeat=3):
    if v == (0, 0, 0): continue
    f = next(z for z in v if z); inv = pow(f, q - 2, q); w = tuple(z * inv % q for z in v)
    if w not in pts: pts.append(w)
n = len(pts); dot = lambda u, v: sum(a * b for a, b in zip(u, v)) % q
E0 = [(i, j) for i, j in itertools.combinations(range(n), 2) if dot(pts[i], pts[j]) == 0]
adj = {v: set() for v in range(n)}
for i, j in E0: adj[i].add(j); adj[j].add(i)
ab = {i for i in range(n) if dot(pts[i], pts[i]) == 0}
x = next(v for v in range(n) if v not in ab and not (adj[v] & ab))
N = sorted(adj[x]); M = []
left = set(N)
while left:
    u = min(left); w = next(iter(adj[u] & left)); M.append((u, w)); left -= {u, w}
order = [x] + [v for p in M for v in p]
lab = {v: i for i, v in enumerate(order)}
for u in [v for p in M for v in p]:
    Bu = sorted((w for w in adj[u] if w != x and w not in adj[x]), key=lambda w: len(adj[w]))
    assert len(Bu) == 6
    for w in Bu: lab[w] = len(lab)
assert len(lab) == n
E = sorted(tuple(sorted((lab[a], lab[b]))) for a, b in E0)
deg = [0] * n
for a, b in E: deg[a] += 1; deg[b] += 1
S = list(range(9)); fixed = [e for e in E if e[0] < 9 or e[1] < 9]
assert set((1, 2)) and (1, 2) in fixed and (7, 8) in fixed
B = {i: list(range(9 + 6 * (i - 1), 15 + 6 * (i - 1))) for i in range(1, 9)}
for i in B: assert all((i, v) in set(fixed) for v in B[i])
target = {v: deg[v] for v in range(9, n)}
cnf, var, F, adjS, st, cls = fsenc.build(n, S, fixed, target, highs=(), sb="all", r1=False, r1b=False)
pairs = [(1, 2), (3, 4), (5, 6), (7, 8)]; perms = []
for order_ in itertools.permutations(range(4)):
    for flips in itertools.product((0, 1), repeat=4):
        sig = {}
        for a, b_ in enumerate(order_):
            p, qq = pairs[a]; P, Q = pairs[b_]
            if flips[a]: P, Q = Q, P
            sig[p], sig[qq] = P, Q
        if all(sig[i] == i for i in range(1, 9)): continue
        pi = list(range(n))
        for i in range(1, 9):
            pi[i] = sig[i]
            for k in range(6): pi[B[i][k]] = B[sig[i]][k]
        if all(deg[pi[v]] == deg[v] for v in range(n)) and all(tuple(sorted((pi[a], pi[b]))) in set(fixed) for a, b in fixed):
            perms.append(pi)
top = max([abs(l) for c in cnf.clauses for l in c] + [len(var)])
top, nc = fsenc.add_perm_sb(cnf, var, n, perms, top)
ordv = sorted(var); Eset = set(E)
X = {e for e in E if e[0] >= 9 and e[1] >= 9}
vec = lambda X: [1 if e in X else 0 for e in ordv]
gens = []
for C in cls:
    for i, j in itertools.combinations(C, 2):
        t = list(range(n)); t[i], t[j] = j, i; gens.append(t)
gens += perms
steps = 0
while True:
    cur = vec(X); moved = False
    for g in gens:
        Y = {e for e in ordv if tuple(sorted((g[e[0]], g[e[1]]))) in X}
        if vec(Y) < cur: X = Y; moved = True; steps += 1; break
    if not moved: break
d2, mc = c4cnf.check_graph(n, fixed + list(X))
with Cadical153(bootstrap_with=cnf.clauses) as s:
    acc = s.solve(assumptions=[var[e] if e in X else -var[e] for e in var])
    raw = {e for e in E if e[0] >= 9 and e[1] >= 9}
    accraw = s.solve(assumptions=[var[e] if e in raw else -var[e] for e in var])
print(f"ER(7)-anchor n={n} classes={[len(c) for c in cls]} perms={len(perms)} descent_steps={steps} "
      f"descended_valid={all(d2[u] == deg[u] for u in range(n)) and mc == 1} CNF_accepts_descended={acc} raw_accepted={accraw}")
