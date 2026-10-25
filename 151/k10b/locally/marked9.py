#!/usr/bin/env python3
"""All MARKED triangle-free graphs on 9 vertices without isolated vertices (Bikov Def. 3.3: V(N) marked in N), by edge
count — the admissible core links of a degree-9 vertex in a K4-free minimal (3,3)-Ramsey graph (Prop. 3.4 + §8).
Controls: K4 marked, K3 not, Wagner marked, K_{4,4} not; the 8-vertex run must return exactly Bikov's seven."""
import subprocess, numpy as np, networkx as nx
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
assert marked(nx.complete_graph(4)) and not marked(nx.complete_graph(3)) and marked(nx.circulant_graph(8,[1,4])) and not marked(nx.complete_bipartite_graph(4,4))
g8=[s for s in subprocess.run(['nauty-geng','-q','-t','-d1','8'],capture_output=True,text=True).stdout.split() if marked(nx.from_graph6_bytes(s.encode()))]
print("8-vertex marked triangle-free (no isolated):", len(g8), g8); assert len(g8)==7
gs=subprocess.run(['nauty-geng','-q','-t','-d1','9'],capture_output=True,text=True).stdout.split()
out=[]
for s in gs:
    G=nx.from_graph6_bytes(s.encode())
    if G.number_of_edges()>16: continue      # 17+ edges: non-bipartite max is 17 and both 17-edge graphs are unmarked (paley_check.py)
    if nx.is_bipartite(G): continue           # bipartite links are never marked
    if marked(G): out.append((G.number_of_edges(),s))
out.sort()
print(f"9-vertex triangle-free, no isolated vertex, non-bipartite, <=16 edges: {len(gs)} scanned; MARKED: {len(out)}")
by={}
for m,s in out: by.setdefault(m,[]).append(s)
for m in sorted(by): print(f"  {m} edges: {len(by[m])} {by[m]}")
open("marked9.g6","w").write("\n".join(s for _,s in out)+"\n")
