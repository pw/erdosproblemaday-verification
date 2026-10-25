#!/usr/bin/env python3
"""Invariants of the two locally-M8 graphs + a literal (3,3)-free colouring certificate for each, written to <g6>.colouring"""
import sys, itertools, networkx as nx
from pysat.solvers import Glucose3
for line in open(sys.argv[1]):
    s=line.strip()
    if not s: continue
    G=nx.from_graph6_bytes(s.encode()); n=G.number_of_nodes()
    dist=nx.single_source_shortest_path_length(G,0); dd={}
    for v,d in dist.items(): dd[d]=dd.get(d,0)+1
    mus={}
    for u,v in itertools.combinations(range(n),2):
        if not G.has_edge(u,v):
            m=len(set(G[u])&set(G[v])); mus[m]=mus.get(m,0)+1
    print(f"{s}: n={n} girth={nx.girth(G)} diameter={nx.diameter(G)} distance-distribution-from-0={dict(sorted(dd.items()))} common-neighbours-of-non-adjacent-pairs={dict(sorted(mus.items()))} chromatic-number>={max(len(c) for c in nx.find_cliques(G))}")
    E=list(G.edges()); idx={frozenset(e):i+1 for i,e in enumerate(E)}
    tris=[t for t in nx.enumerate_all_cliques(G) if len(t)==3]
    with Glucose3() as sv:
        for t in tris:
            v=[idx[frozenset(p)] for p in itertools.combinations(t,2)]; sv.add_clause(v); sv.add_clause([-x for x in v])
        assert sv.solve(); model=sv.get_model()
    red=[E[i] for i in range(len(E)) if model[i]>0]; R={frozenset(e) for e in red}
    mono=[t for t in tris if all(frozenset(p) in R for p in itertools.combinations(t,2)) or not any(frozenset(p) in R for p in itertools.combinations(t,2))]
    assert not mono
    with open(f"{'G21' if n==21 else 'P17'}.colouring","w") as f:
        f.write(f"# graph6 {s}\n# red edges of a (K3,K3)-free 2-colouring ({len(red)} red of {len(E)}); every other edge blue; {len(tris)} triangles, 0 monochromatic\n")
        for a,b in red: f.write(f"{a} {b}\n")
    print(f"  colouring certificate written: {len(red)} red edges, {len(E)-len(red)} blue, {len(tris)} triangles checked")
