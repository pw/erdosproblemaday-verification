#!/usr/bin/env python3
"""Decorrelated recount of (I3,L3)-free oriented graph types on n=7,8 vertices via nauty-geng:
an oriented graph with no independent triple and no transitive triangle has an underlying graph with
alpha<=2 and no K4 (every 4-tournament contains a transitive triple), and every triangle oriented cyclically.
geng enumerates underlying graphs up to iso; we then enumerate cyclic-triangle orientations and dedupe
orientations under the underlying graph's automorphisms + reversal-free canonical form by brute force."""
import subprocess, itertools, sys
def graphs(n):
    out = subprocess.run(["nauty-geng", "-q", str(n)], capture_output=True, text=True).stdout.split()
    return out
def parse_g6(s):
    data = [ord(c) - 63 for c in s]; n = data[0]; bits = []
    for d in data[1:]:
        bits += [(d >> (5 - i)) & 1 for i in range(6)]
    E = set(); k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: E.add((i, j))
            k += 1
    return n, E
def alpha_le2_K4free(n, E):
    adj = {i: set() for i in range(n)}
    for i, j in E: adj[i].add(j); adj[j].add(i)
    for a, b, c in itertools.combinations(range(n), 3):
        if b not in adj[a] and c not in adj[a] and c not in adj[b]: return False
    for Q in itertools.combinations(range(n), 4):
        if all(y in adj[x] for x, y in itertools.combinations(Q, 2)): return False
    return True
def orientations(n, E):
    E = sorted(E); tris = [(a, b, c) for a, b, c in itertools.combinations(range(n), 3) if (a, b) in set(E) and (a, c) in set(E) and (b, c) in set(E)]
    Es = set(E)
    res = []
    # backtrack over edges; each triangle must be cyclic: for triangle a<b<c, orientations (ab,bc,ca) cyclic iff a->b->c->a or a<-b<-c<-a
    order = E
    assign = {}
    def tri_ok(t):
        a, b, c = t
        e = [(a, b), (b, c), (a, c)]
        if any(x not in assign for x in e): return True
        ab, bc, ac = assign[(a, b)], assign[(b, c)], assign[(a, c)]  # 1 means low->high
        # cyclic: a->b, b->c, c->a  => ab=1, bc=1, ac=0 ; or reverse: ab=0,bc=0,ac=1
        return (ab == 1 and bc == 1 and ac == 0) or (ab == 0 and bc == 0 and ac == 1)
    def rec(i):
        if i == len(order): res.append(dict(assign)); return
        e = order[i]
        for v in (1, 0):
            assign[e] = v
            if all(tri_ok(t) for t in tris if e in [(t[0], t[1]), (t[1], t[2]), (t[0], t[2])]): rec(i + 1)
            del assign[e]
    rec(0); return res
def canon(n, E, asg):
    arcs = set()
    for (i, j), v in asg.items(): arcs.add((i, j) if v == 1 else (j, i))
    best = None
    for p in itertools.permutations(range(n)):
        key = tuple(sorted((p[u], p[v]) for u, v in arcs))
        if best is None or key < best: best = key
    return best
for n in (7, 8):
    cnt = 0; seen = set()
    gs = graphs(n)
    for g in gs:
        nn, E = parse_g6(g)
        if not alpha_le2_K4free(nn, E): continue
        for asg in orientations(nn, E):
            seen.add(canon(nn, E, asg))
    print(f"n={n}: underlying graphs {len(gs)} total; (I3,L3)-free oriented types = {len(seen)}", flush=True)
