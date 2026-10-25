import itertools, networkx as nx
def maxcl(G): return [frozenset(c) for c in nx.find_cliques(G) if len(c) >= 2]
def is_free(S, cl): S = frozenset(S); return not any(c <= S for c in cl)
def beta(G):
    V = list(G.nodes()); cl = maxcl(G)
    for r in range(len(V), -1, -1):
        for S in itertools.combinations(V, r):
            if is_free(S, cl): return r
    return 0
def alpha(G): return max((len(c) for c in nx.find_cliques(nx.complement(G))), default=0) if G.number_of_nodes() else 0
def lone_edges(G): return [frozenset(e) for e in G.edges() if not (set(G[e[0]]) & set(G[e[1]]))]
def link(G, v):
    H = G.subgraph(G[v]).copy(); iso = [x for x in H if H.degree(x) == 0]
    P = H.copy(); P.remove_nodes_from(iso); return H, P, len(iso)
def min_trans(G, v):
    H = G.subgraph(G[v]); N = list(H.nodes()); cls = [frozenset(c) for c in nx.find_cliques(H)] if N else []
    for r in range(len(N)+1):
        out = [frozenset(D) for D in itertools.combinations(N, r) if all(c & set(D) for c in cls)]
        if out: return out
def report(name, G):
    G = nx.convert_node_labels_to_integers(G)
    cl = maxcl(G); b = beta(G); a = alpha(G); L = lone_edges(G)
    ts = {}
    for v in G:
        H, P, i = link(G, v); bP = beta(P) if P.number_of_nodes() else 0
        t = G.degree(v) - bP; ts[v] = t
        assert len(min_trans(G, v)[0]) == t
        for c in nx.find_cliques(G):
            if v in c and len(c) >= 3: assert bP >= len(c) - 2
    # T2 over all independent sets I and all minimal transversal combos
    nT2 = 0
    for r in range(1, a+1):
        for I in itertools.combinations(G.nodes(), r):
            if any(G.has_edge(x, y) for x, y in itertools.combinations(I, 2)): continue
            for combo in itertools.product(*[min_trans(G, v) for v in I]):
                D = frozenset().union(*combo)
                H = G.subgraph(set(G) - set(I) - D)
                assert b >= len(I) + beta(H), (name, I, D); nT2 += 1
    print(f"{name}: n={G.number_of_nodes()} m={G.number_of_edges()} beta={b} alpha={a} omega={max(len(c) for c in nx.find_cliques(G))} "
          f"Delta={max(d for _,d in G.degree())} lone={len(L)} t-values={sorted(set(ts.values()))} T2-instances={nT2} OK")
    return G
pet = nx.petersen_graph()
octa = nx.octahedral_graph()
K4p = nx.complete_graph(4)
for e, (x, y) in enumerate([(0,1),(2,3),(0,2)]):   # pendant triangle on three edges of K4
    z = 10 + e; K4p.add_edge(x, z); K4p.add_edge(y, z)
W5 = nx.wheel_graph(6)   # hub + C5
K6p = nx.complete_graph(6); K6p.add_edges_from([(0,6),(6,7),(7,0)])  # K6 with a pendant triangle: clique-bound test
for name, G in [("Petersen", pet), ("octahedron", octa), ("K4+3 pendant triangles", K4p), ("5-wheel", W5), ("K6+pendant triangle", K6p)]:
    report(name, G)
# T1 clique bound sharpness at an exact instance: v in K_m, beta(P_v) >= m-2 with equality for K_m itself
for m in range(3, 9):
    G = nx.complete_graph(m); H, P, i = link(G, 0); assert beta(P) == m - 2
print("K_m: beta(link) = m-2 exactly for m=3..8 (T1 clique bound tight on K_m)")
