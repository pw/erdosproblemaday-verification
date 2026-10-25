import itertools, networkx as nx
from networkx.algorithms import isomorphism as iso
from collections import Counter
from sympy.combinatorics import Permutation, PermutationGroup
G = nx.from_graph6_bytes(b"T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB"); n = G.number_of_nodes()
print("n", n, "edges", G.number_of_edges(), "degrees", set(dict(G.degree()).values()))
print("girth", nx.girth(G), "diameter", nx.diameter(G))
for v in [0]:
    d = nx.single_source_shortest_path_length(G, v); print("distance distribution from 0:", sorted(Counter(d.values()).items()))
lam = Counter(len(set(G[u])&set(G[v])) for u,v in G.edges())
mu = Counter(len(set(G[u])&set(G[v])) for u,v in itertools.combinations(G,2) if not G.has_edge(u,v))
print("lambda multiset", dict(lam), " mu multiset (non-adjacent pairs)", dict(mu))
mu_by_dist = Counter((nx.shortest_path_length(G,u,v), len(set(G[u])&set(G[v]))) for u,v in itertools.combinations(G,2) if not G.has_edge(u,v))
print("(dist, mu) counts", dict(mu_by_dist))
# distance-regularity / intersection array
print("distance-regular?", nx.is_distance_regular(G))
auts = [m for m in iso.GraphMatcher(G,G).isomorphisms_iter()]
print("|Aut|", len(auts))
A = PermutationGroup([Permutation([m[i] for i in range(n)]) for m in auts])
print("group order", A.order(), "transitive", A.is_transitive())
stab = A.stabilizer(0)
orbs = sorted(sorted(o) for o in stab.orbits())
print("suborbits of Stab(0):", [(len(o), nx.shortest_path_length(G,0,o[0])) for o in orbs])
# regular subgroups: elements of order 7 and 3
els = list(A.generate())
o7 = [g for g in els if g.order()==7]; o3 = [g for g in els if g.order()==3]
print("#elements of order 7:", len(o7), "order 3:", len(o3), "order 2:", sum(1 for g in els if g.order()==2))
regs = set()
for a in o7[:6]:
    for b in o3:
        H = PermutationGroup([a,b])
        if H.order()==21:
            regs.add(tuple(sorted(tuple(h.array_form) for h in H.generate())))
print("#subgroups of order 21 generated (from first 6 order-7 elements):", len(regs))
for R in regs:
    H = PermutationGroup([Permutation(list(p)) for p in R])
    print("  order-21 subgroup: transitive", H.is_transitive(), "abelian", H.is_abelian, "orbits", [len(o) for o in H.orbits()])
# derived/structure
print("Aut abelian?", A.is_abelian, " derived subgroup order", A.derived_subgroup().order(), " is_simple(derived)", A.derived_subgroup().is_simple if hasattr(A.derived_subgroup(),'is_simple') else None)
print("centre order", A.center().order())
