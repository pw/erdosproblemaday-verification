# Independent link check (explicit isomorphism by brute force, no networkx matcher) + common-neighbourhood types.
import itertools, networkx as nx
from collections import Counter
W = {(i,(i+1)%8) for i in range(8)} | {(i,(i+4)%8) for i in range(8)}
W = {frozenset(e) for e in W}; assert len(W)==12
def is_M8(Gs, verts):
    verts = list(verts)
    E = {frozenset((a,b)) for a,b in itertools.combinations(verts,2) if Gs.has_edge(a,b)}
    if len(E)!=12: return None
    for perm in itertools.permutations(range(8)):
        f = dict(zip(verts, perm))
        if all(frozenset((f[a],f[b])) in W for a,b in map(tuple,E)): return f
    return None
def shape(H):
    degs = sorted(d for _,d in H.degree())
    comps = sorted(len(c) for c in nx.connected_components(H))
    return f"n{H.number_of_nodes()} e{H.number_of_edges()} degs{degs} comps{comps}"
for name, g6 in [("G21", b"T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB"), ("P17", b"P|fLKfH[QJkSVDMJDrGm]A|g")]:
    G = nx.from_graph6_bytes(g6)
    ok = all(is_M8(G, list(G[v])) is not None for v in G)
    types = Counter(shape(G.subgraph(set(G[u])&set(G[v]))) for u,v in itertools.combinations(G,2) if not G.has_edge(u,v))
    print(name, "every link explicitly isomorphic to C8(1,4):", ok)
    for t,c in sorted(types.items()): print("   non-adjacent pair, induced common nbhd:", t, "x", c)
