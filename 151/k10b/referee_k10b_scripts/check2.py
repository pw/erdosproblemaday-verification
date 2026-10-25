import subprocess, numpy as np, networkx as nx, itertools, time
from networkx.algorithms import isomorphism as iso
def g(s): return nx.from_graph6_bytes(s.encode())
def geng(a): return subprocess.run(['nauty-geng','-q']+a,capture_output=True,text=True).stdout.split()
def alpha(G): return max(len(c) for c in nx.find_cliques(nx.complement(G)))
def marked(N):
    N=nx.convert_node_labels_to_integers(N)
    E=list(N.edges()); m=len(E); p=N.number_of_nodes()
    cs=np.arange(1<<m,dtype=np.int64); alive=np.ones(1<<m,dtype=bool)
    for f in range(1<<p):
        mR=0; mB=0
        for i,(a,b) in enumerate(E):
            fa,fb=f>>a&1,f>>b&1
            if fa and fb: mR|=1<<i
            if (not fa) and (not fb): mB|=1<<i
        alive &= ~(((cs&mR)==0)&(((~cs)&mB)==0))
        if not alive.any(): return False
    return True
NOTE=['G?`F`w','G?bF`w','G?rF`w','G?q`qg','GCQb`o','GCR`r_','GCrb`o']
Gs=[g(s) for s in NOTE]
def sub(N,H): return iso.GraphMatcher(H,N).subgraph_is_monomorphic()
# controls
W=nx.circulant_graph(8,[3,4]); assert sub(nx.cycle_graph(8),W) and not sub(W,nx.cycle_graph(8))
assert marked(nx.complete_graph(4)) and not marked(nx.complete_graph(3)) and not marked(nx.complete_bipartite_graph(4,4))
print("containment poset (row i is spanning subgraph of col j), note numbering:")
for i,N in enumerate(Gs,1):
    print(f" N8.{i}:", [j for j,H in enumerate(Gs,1) if j!=i and sub(N,H)])
# upward closure among triangle-free 8-vertex graphs
tf8=geng(['-t','8']); canon7={nx.weisfeiler_lehman_graph_hash(G) for G in Gs}
sup=[s for s in tf8 if any(sub(N,g(s)) for N in Gs)]
print("triangle-free 8-vertex graphs:",len(tf8),"; containing some N8.i spanning:",len(sup),
      "; all among the seven:", all(any(nx.is_isomorphic(g(s),G) for G in Gs) for s in sup))
nm=[s for s in tf8 if marked(g(s))]
print("marked triangle-free 8-vertex graphs:",len(nm),"; same set as note:",sorted(nm)==sorted(NOTE))
# 9-vertex triangle-free: max edges overall, non-bipartite, alpha<=4, alpha<=5; marked ones
t9=geng(['-t','9'])
rows=[]
for s in t9:
    G=g(s); rows.append((G.number_of_edges(), nx.is_bipartite(G), alpha(G), min(d for _,d in G.degree()), s))
print("9-vertex triangle-free graphs:",len(t9))
print(" max edges overall:",max(r[0] for r in rows))
print(" max edges non-bipartite:",max(r[0] for r in rows if not r[1]))
print(" max edges alpha<=4:",max(r[0] for r in rows if r[2]<=4), " alpha<=5:",max(r[0] for r in rows if r[2]<=5))
print(" max edges alpha<=6 (Bikov 2.7, d-3=6):",max(r[0] for r in rows if r[2]<=6))
# marked among non-bipartite with >=14 edges, descending
t0=time.time(); best=None
for e in range(20,12,-1):
    cand=[r for r in rows if r[0]==e and not r[1] and r[3]>=1]
    mk=[r[4] for r in cand if marked(g(r[4]))]
    print(f"  e={e}: non-bipartite no-isolated triangle-free {len(cand)}, marked {len(mk)} {mk[:5]}  ({time.time()-t0:.0f}s)",flush=True)
    if mk: best=e; break
print("max edges of a 9-vertex triangle-free graph whose vertex set is marked:",best)
