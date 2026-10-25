#!/usr/bin/env python3
"""Independent checks on the graphs the locally-M8 search found: regular of degree 8, every link ≅ M8 (networkx), K4-free,
alpha, triangles, arrowing (K3,K3)^e by Glucose AND by CP-SAT (agree), automorphism count / vertex-transitivity, and
whether the 17-vertex one is Paley(17)."""
import sys, itertools
import networkx as nx
from networkx.algorithms import isomorphism as iso
from pysat.solvers import Glucose3
from ortools.sat.python import cp_model
W = nx.circulant_graph(8,[1,4])
P = nx.Graph(); P.add_nodes_from(range(17)); Q={(x*x)%17 for x in range(1,17)}
P.add_edges_from((a,b) for a in range(17) for b in range(a+1,17) if (b-a)%17 in Q)
def arrows_sat(G):
    E=list(G.edges()); idx={frozenset(e):i+1 for i,e in enumerate(E)}
    tris=[t for t in nx.enumerate_all_cliques(G) if len(t)==3]
    with Glucose3() as sv:
        for t in tris:
            v=[idx[frozenset(p)] for p in itertools.combinations(t,2)]; sv.add_clause(v); sv.add_clause([-x for x in v])
        sat=sv.solve(); model=sv.get_model() if sat else None
    if sat:
        red={E[i] for i in range(len(E)) if model[i]>0}; R={frozenset(e) for e in red}
        mono=sum(1 for t in tris if all(frozenset(p) in R for p in itertools.combinations(t,2)) or not any(frozenset(p) in R for p in itertools.combinations(t,2)))
        assert mono==0
    return not sat
def arrows_cp(G):
    E=list(G.edges()); idx={frozenset(e):i for i,e in enumerate(E)}
    m=cp_model.CpModel(); x=[m.NewBoolVar(str(i)) for i in E]
    for t in (t for t in nx.enumerate_all_cliques(G) if len(t)==3):
        s=sum(x[idx[frozenset(p)]] for p in itertools.combinations(t,2)); m.Add(s>=1); m.Add(s<=2)
    sv=cp_model.CpSolver(); sv.parameters.num_search_workers=2; r=sv.Solve(m)
    assert r in (cp_model.OPTIMAL,cp_model.FEASIBLE,cp_model.INFEASIBLE); return r==cp_model.INFEASIBLE
assert arrows_sat(nx.complete_graph(6)) and arrows_cp(nx.complete_graph(6))
for line in open(sys.argv[1]):
    s=line.strip()
    if not s: continue
    G=nx.from_graph6_bytes(s.encode()); n=G.number_of_nodes()
    degs={d for _,d in G.degree()}
    links=all(nx.is_isomorphic(G.subgraph(G[v]),W) for v in G)
    k4=any(len(c)>=4 for c in nx.find_cliques(G))
    alpha=max(len(c) for c in nx.find_cliques(nx.complement(G)))
    tri=sum(nx.triangles(G).values())//3
    GM=iso.GraphMatcher(G,G); auts=sum(1 for _ in GM.isomorphisms_iter())
    orbits=set(); 
    for m in iso.GraphMatcher(G,G).isomorphisms_iter(): orbits.add(m[0])
    a1=arrows_sat(G); a2=arrows_cp(G)
    print(f"{s}: n={n} edges={G.number_of_edges()} degrees={degs} all-links-M8={links} K4={k4} alpha={alpha} triangles={tri} |Aut|={auts} orbit-of-0-size={len(orbits)} (vertex-transitive={len(orbits)==n}) arrows: glucose={a1} cpsat={a2}" + (f"  ≅Paley17={nx.is_isomorphic(G,P)}" if n==17 else ""), flush=True)
