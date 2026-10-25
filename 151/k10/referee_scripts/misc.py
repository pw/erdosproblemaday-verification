import itertools, subprocess, random
import networkx as nx
import numpy as np
from ortools.sat.python import cp_model
R3 = {0:0, 1:1, 2:3, 3:6, 4:9, 5:14, 6:18, 7:23, 8:28, 9:36}
for n in (40, 41):
    print(n, [n - m - R3[10 - m] + 1 for m in range(1, 10)])
# T4 refinement counting: x vertices with exactly one lone I-neighbour (x <= 9), rest >= 2
for n in (40, 41):
    out = n - 9
    print("n", n, "outside I:", out, "min sum i(v) =", min(x + 2*(out - x) for x in range(0, 10)))
# --- Property B for graphs with every edge in <= 2 triangles (exhaustive n<=8) + positive control K6
def propB(G):
    tris = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    E = {frozenset(e): i for i, e in enumerate(G.edges())}
    m = cp_model.CpModel(); x = [m.NewBoolVar(str(i)) for i in range(len(E))]
    for a, b, c in tris:
        s = x[E[frozenset((a,b))]] + x[E[frozenset((b,c))]] + x[E[frozenset((a,c))]]
        m.Add(s >= 1); m.Add(s <= 2)
    s = cp_model.CpSolver(); s.parameters.num_search_workers = 1
    r = s.Solve(m); assert r in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.INFEASIBLE)
    return r != cp_model.INFEASIBLE
assert not propB(nx.complete_graph(6)), "positive control: K6 must NOT be 2-colourable"
g = nx.complete_graph(3); C5 = nx.cycle_graph(5); graham = nx.complement(nx.disjoint_union(nx.complement(g), nx.complement(C5)))
assert not propB(graham), "positive control: Graham K3+C5 must NOT be 2-colourable"
cnt = 0
for n in range(3, 9):
    for s in subprocess.run(['nauty-geng', '-q', str(n)], capture_output=True, text=True).stdout.split():
        G = nx.from_graph6_bytes(s.encode())
        if all(len(set(G[a]) & set(G[b])) <= 2 for a, b in G.edges()):
            assert propB(G), s; cnt += 1
random.seed(7); rc = 0
while rc < 300:
    n = random.randint(10, 22); G = nx.gnp_random_graph(n, random.choice([0.25, 0.35, 0.5]), seed=random.randrange(10**9))
    # thin out until every edge in <= 2 triangles
    changed = True
    while changed:
        changed = False
        for a, b in list(G.edges()):
            if len(set(G[a]) & set(G[b])) > 2: G.remove_edge(a, b); changed = True; break
    if sum(nx.triangles(G).values()) == 0: continue
    assert propB(G); rc += 1
print(f"Property B holds on all {cnt} graphs (n<=8) and {rc} random graphs (n<=22) with every edge in <=2 triangles; K6 and K3+C5 controls correctly non-colourable")
# --- 'a triangle shares an edge with at most one of the triangles through a given edge' (K4-free)
bad_any = 0; bad_excl = 0; tested = 0
for n in range(3, 8):
    for s in subprocess.run(['nauty-geng', '-q', str(n)], capture_output=True, text=True).stdout.split():
        G = nx.from_graph6_bytes(s.encode())
        if any(len(c) >= 4 for c in nx.find_cliques(G)): continue
        tris = [frozenset(c) for c in nx.enumerate_all_cliques(G) if len(c) == 3]
        for e in G.edges():
            e = frozenset(e); through = [T for T in tris if e <= T]
            for T in tris:
                tested += 1
                k = sum(1 for T2 in through if T2 != T and len(T & T2) == 2)
                if k > 1:
                    bad_any += 1
                    if not (e <= T): bad_excl += 1
print(f"K4-free n<=7: (triangle, edge) pairs {tested}; T shares an edge with >1 OTHER triangle through e: {bad_any} times, of which with e not in T: {bad_excl}")
# --- Bikov Thm 8.2 check: triangle-free N on p vertices with V(N) a 'marked vertex set'
def marked(N):
    E = list(N.edges()); m = len(E); p = N.number_of_nodes()
    if m > 20: raise SystemExit("too many edges")
    cs = np.arange(1 << m, dtype=np.int64)   # bit i = 1 means edge i RED
    alive = np.ones(1 << m, dtype=bool)        # colourings not yet extendable by any f
    for f in range(1 << p):                    # f bit = 1 means vertex-edge to v RED
        mR = 0; mB = 0
        for i, (a, b) in enumerate(E):
            fa, fb = f >> a & 1, f >> b & 1
            if fa and fb: mR |= 1 << i         # both v-edges red: edge ab must not be red
            if not fa and not fb: mB |= 1 << i # both blue: ab must not be blue
        ok = ((cs & mR) == 0) & (((~cs) & mB) == 0)
        alive &= ~ok
        if not alive.any(): return False
    return bool(alive.any())
assert marked(nx.complete_graph(4)), "control: V(K4) is marked in K4 (Bikov)"
assert not marked(nx.complete_graph(3)), "control: |W|<=3 never marked"
for p in range(1, 9):
    gs = subprocess.run(['nauty-geng', '-q', '-t', str(p)], capture_output=True, text=True).stdout.split()
    hits = [s for s in gs if marked(nx.from_graph6_bytes(s.encode()))]
    print(f"triangle-free p={p}: {len(gs)} graphs, V(N) marked in {len(hits)}", hits[:8])
