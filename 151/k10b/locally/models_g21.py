#!/usr/bin/env python3
"""Our own check of the referee's two models of G21 (graph6 T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB):
 (1) Fano-plane flag graph: vertices = the 21 flags (p,L) of PG(2,2), (p,L) ~ (q,M) iff p ∉ M and q ∉ L;
 (2) the distance-3 graph of the line graph of the Heawood graph (= flags, adjacent iff the two flags are at distance 3
     in the flag/line graph).  Both must be isomorphic to G21 and to each other; P(17) must NOT be."""
import itertools, networkx as nx
G21=nx.from_graph6_bytes(b'T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB')
pts=range(7); lines=[frozenset({i,(i+1)%7,(i+3)%7}) for i in range(7)]   # Fano plane via the difference set {0,1,3}
assert all(len(a&b)==1 for a,b in itertools.combinations(lines,2)) and all(sum(1 for L in lines if p in L)==3 for p in pts)
flags=[(p,L) for L in lines for p in L]; assert len(flags)==21
F=nx.Graph(); F.add_nodes_from(range(21))
for i,(p,L) in enumerate(flags):
    for j,(q,M) in enumerate(flags):
        if i<j and p not in M and q not in L: F.add_edge(i,j)
print("Fano flag graph: n=21 edges=%d regular=%s iso to G21: %s" % (F.number_of_edges(), len({d for _,d in F.degree()})==1, nx.is_isomorphic(F,G21)))
H=nx.heawood_graph(); LH=nx.line_graph(H); assert LH.number_of_nodes()==21
D=nx.Graph(); D.add_nodes_from(LH.nodes()); dist=dict(nx.all_pairs_shortest_path_length(LH))
for u,v in itertools.combinations(LH.nodes(),2):
    if dist[u][v]==3: D.add_edge(u,v)
print("distance-3 graph of L(Heawood): edges=%d iso to G21: %s" % (D.number_of_edges(), nx.is_isomorphic(D,G21)))
P=nx.paley_graph(17).to_undirected() if hasattr(nx,'paley_graph') else None
if P is not None: print("P(17) iso to G21:", nx.is_isomorphic(P,G21), "(must be False)")
W=nx.circulant_graph(8,[1,4]); print("all 21 links of the flag graph ≅ M8:", all(nx.is_isomorphic(F.subgraph(F[v]),W) for v in F))
