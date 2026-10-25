#!/usr/bin/env python3
"""POSITIVE composition control on polarity graphs ER(q), q odd: same saturation as the strata.
A passant point x (non-absolute, polar line with no absolute point) has q+1 neighbours, all of degree q+1,
so sum_{u in N(x)} (deg u - 1) = (q+1)q = n - 1 with n = q^2+q+1: R1 and R1b are THEOREMS for any completion.
Instance: highs = a maximal set of pairwise non-adjacent passant points (all their edges fixed); every other
edge free; targets = ER(q) degrees.  BASE = c4cnf only.  PIPE = fsenc (R1 + R1b + class SB) + block-and-target
preserving high-permutation SB.  ER(q) itself solves BASE, so both must be SAT; enumerate all solutions of each,
compare isomorphism classes with highs coloured (pynauty) -- they must be EQUAL -- and check R1/R1b on BASE."""
import itertools, sys, time
from pathlib import Path
from pysat.solvers import Cadical153
from pynauty import Graph, certificate
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fsenc, c4cnf
q = int(sys.argv[1]); LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
pts = []
for v in itertools.product(range(q), repeat=3):
    if v == (0, 0, 0): continue
    f = next(z for z in v if z); inv = pow(f, q - 2, q)
    w = tuple(z * inv % q for z in v)
    if w not in pts: pts.append(w)
n = len(pts); assert n == q * q + q + 1
dot = lambda u, v: sum(a * b for a, b in zip(u, v)) % q
E0 = [(i, j) for i, j in itertools.combinations(range(n), 2) if dot(pts[i], pts[j]) == 0]
adj = {v: set() for v in range(n)}
for i, j in E0: adj[i].add(j); adj[j].add(i)
absol = {i for i in range(n) if dot(pts[i], pts[i]) == 0}
passant = [x for x in range(n) if x not in absol and not (adj[x] & absol)]
highs = []
for x in passant:
    if all(x not in adj[y] for y in highs): highs.append(x)
h = len(highs)
blk = {v: tuple(sorted(highs.index(y) for y in adj[v] if y in highs)) for v in range(n) if v not in highs}
lows = sorted(blk, key=lambda v: (blk[v], len(adj[v])))
order = highs + lows; lab = {v: i for i, v in enumerate(order)}
E = sorted(tuple(sorted((lab[a], lab[b]))) for a, b in E0)
deg = [0] * n
for a, b in E: deg[a] += 1; deg[b] += 1
H = list(range(h)); fixed = [e for e in E if e[0] < h or e[1] < h]
target = {v: deg[v] for v in range(h, n)}
blocks = [tuple(sorted(a for a in H if (a, v) in set(fixed))) for v in range(h, n)]
def perm_of(sig):
    pi = list(range(n)); slots = {}
    for i, b in enumerate(blocks): slots.setdefault((b, deg[h + i]), []).append(h + i)
    used = {k: 0 for k in slots}
    for a in H: pi[a] = sig[a]
    for i, b in enumerate(blocks):
        key = (tuple(sorted(sig[x] for x in b)), deg[h + i])
        if key not in slots or used[key] >= len(slots[key]): return None
        pi[h + i] = slots[key][used[key]]; used[key] += 1
    return pi
perms = []
for a, b in itertools.combinations(H, 2):
    sig = list(range(h)); sig[a], sig[b] = b, a
    p = perm_of(sig)
    if p: perms.append(p)
def enum(clauses, var):
    out, edges = [], sorted(var)
    with Cadical153(bootstrap_with=clauses) as s:
        while s.solve():
            m = set(l for l in s.get_model() if l > 0)
            on = [e for e in edges if var[e] in m]; out.append(on)
            s.add_clause([-var[e] for e in on] + [var[e] for e in edges if var[e] not in m])
            if len(out) >= LIMIT: return out, False
    return out, True
def cert(on):
    a = {v: [] for v in range(n)}
    for x, y in list(fixed) + on: a[x].append(y); a[y].append(x)
    return certificate(Graph(n, adjacency_dict=a, vertex_coloring=[set(H), set(range(h, n))]))
def r1ok(on):
    a = {v: set() for v in range(n)}
    for x, y in list(fixed) + on: a[x].add(y); a[y].add(x)
    return all(len(a[v] & a[x]) == 1 for x in H for v in range(n) if v != x)
t0 = time.time()
base, var, F, adjS = c4cnf.build(n, H, fixed, target)
bs, bd = enum(base.clauses, var)
cnf, var2, F2, adjS2, st, cls = fsenc.build(n, H, fixed, target, highs=H, sb="all", r1=True, r1b=True, hdeg=q + 1)
top = max([abs(l) for c in cnf.clauses for l in c] + [len(var)])
top, nc = fsenc.add_perm_sb(cnf, var, n, perms, top)
ps, pd = enum(cnf.clauses, var)
A = {cert(on) for on in bs}; B = {cert(on) for on in ps}
er = cert([e for e in E if e[0] >= h and e[1] >= h])
print(f"ER({q}) n={n} highs={h} classes={st['sb_classes']} highperms={len(perms)} r1b_clauses={st.get('r1b_clauses')} "
      f"base_solutions={len(bs)}{'' if bd else '+'} pipe_solutions={len(ps)}{'' if pd else '+'} orbits_base={len(A)} "
      f"orbits_pipe={len(B)} EQUAL={A == B} ER_in_base={er in A} ER_in_pipe={er in B} base_all_R1R1b={all(r1ok(o) for o in bs)} "
      f"{round(time.time() - t0, 1)}s", flush=True)
