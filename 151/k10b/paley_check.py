#!/usr/bin/env python3
"""Our own check of the referee's lead: Paley(17) is K4-free, every link is the Wagner graph, 68 edges, 68 triangles,
and it does NOT arrow (K3,K3)^e (a (3,3)-free colouring found by SAT and re-verified literally).  Also: the maximum
number of edges of a MARKED triangle-free 9-vertex graph (Bikov Def. 3.3, V(N) marked in N) — bipartite links are
never marked (extend by colouring one side's v-edges red, the other's blue), so the elementary cap is the largest
non-bipartite triangle-free 9-vertex graph, 17 edges; we test every triangle-free 9-vertex graph with >= 15 edges."""
import itertools, subprocess
import networkx as nx, numpy as np
from pysat.solvers import Glucose3
from networkx.algorithms import isomorphism as iso
P=nx.Graph(); P.add_nodes_from(range(17)); Q={(x*x)%17 for x in range(1,17)}
for a in range(17):
    for b in range(a+1,17):
        if (b-a)%17 in Q: P.add_edge(a,b)
W=nx.circulant_graph(8,[1,4])
assert all(d==8 for _,d in P.degree()) and not any(len(c)>=4 for c in nx.find_cliques(P))
links_ok=all(nx.is_isomorphic(P.subgraph(P[v]),W) for v in P)
tri=sum(nx.triangles(P).values())//3
E=list(P.edges()); idx={frozenset(e):i+1 for i,e in enumerate(E)}
tris=[t for t in nx.enumerate_all_cliques(P) if len(t)==3]
with Glucose3() as sv:
    for t in tris:
        v=[idx[frozenset(p)] for p in itertools.combinations(t,2)]; sv.add_clause(v); sv.add_clause([-x for x in v])
    sat=sv.solve(); model=sv.get_model() if sat else None
if sat:
    red={e for e in E if model[idx[frozenset(e)]-1]>0}
    mono=sum(1 for t in tris if all(frozenset(p) in {frozenset(x) for x in red} for p in itertools.combinations(t,2)) or not any(frozenset(p) in {frozenset(x) for x in red} for p in itertools.combinations(t,2)))
else: mono=None
print(f"Paley(17): edges={P.number_of_edges()} triangles={tri} all links Wagner={links_ok} arrows={not sat} (literal recount of monochromatic triangles in the SAT colouring: {mono})")
assert links_ok and P.number_of_edges()==68 and tri==68 and sat and mono==0
# marked 9-vertex triangle-free graphs with many edges
def marked(N):
    E=list(N.edges()); m=len(E); p=N.number_of_nodes()
    cs=np.arange(1<<m,dtype=np.int64); alive=np.ones(1<<m,dtype=bool)
    for f in range(1<<p):
        mR=0; mB=0
        for i,(a,b) in enumerate(E):
            fa,fb=f>>a&1,f>>b&1
            if fa and fb: mR|=1<<i
            if not fa and not fb: mB|=1<<i
        ok=((cs&mR)==0)&(((~cs)&mB)==0); alive&=~ok
        if not alive.any(): return False
    return bool(alive.any())
assert marked(nx.complete_graph(4)) and not marked(nx.complete_graph(3))
assert marked(nx.from_graph6_bytes(b'GCrb`o')) and not marked(nx.complete_bipartite_graph(4,4))
gs=subprocess.run(['nauty-geng','-q','-t','9'],capture_output=True,text=True).stdout.split()
by_m={}
for s in gs:
    G=nx.from_graph6_bytes(s.encode()); m=G.number_of_edges()
    if m>=15: by_m.setdefault(m,[]).append((s,nx.is_bipartite(G)))
for m in sorted(by_m,reverse=True):
    res=[(s,bip,marked(nx.from_graph6_bytes(s.encode()))) for s,bip in by_m[m]]
    print(f"triangle-free 9-vertex graphs with {m} edges: {len(res)}; bipartite {sum(b for _,b,_ in res)}; marked {sum(k for _,_,k in res)} {[s for s,_,k in res if k]}")
