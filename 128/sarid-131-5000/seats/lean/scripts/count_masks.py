# Count labelled triangle-free masks on Fin 6 in the Lean encoding (Defs.lean edgeEnds order), and check the 38 hostMasks
import itertools
ends=[(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)]
idx={e:i for i,e in enumerate(ends)}
def tf(m):
    adj=lambda a,b: (m>>idx[(min(a,b),max(a,b))])&1 if a!=b else 0
    return not any(adj(a,b) and adj(b,c) and adj(a,c) for a,b,c in itertools.combinations(range(6),3))
tfm=[m for m in range(1<<15) if tf(m)]
print("all masks",1<<15,"triangle-free labelled masks",len(tfm))
hosts=[0, 16384, 16388, 96, 28, 20496, 6400, 16420, 24588, 10512, 4680, 8290, 60, 20528, 8266, 4776, 4649, 26896, 929, 12295, 9313, 4696, 21009, 24620, 1731, 126, 8302, 15426, 1752, 4905, 21041, 23202, 26850, 21045, 12857, 15768, 23217, 23221]
import networkx as nx
def G(m):
    g=nx.Graph(); g.add_nodes_from(range(6)); g.add_edges_from(e for i,e in enumerate(ends) if (m>>i)&1); return g
print("hosts",len(hosts),"distinct",len(set(hosts)),"all triangle-free",all(tf(h) for h in hosts))
reps=[G(h) for h in hosts]
noniso=all(not nx.is_isomorphic(reps[i],reps[j]) for i in range(38) for j in range(i+1,38))
print("hosts pairwise non-isomorphic",noniso)
# every triangle-free mask isomorphic to some host (independent recheck of Covers 6)
from collections import Counter
cnt=Counter()
for m in tfm:
    g=G(m); hit=[i for i,r in enumerate(reps) if nx.faster_could_be_isomorphic(g,r) and nx.is_isomorphic(g,r)]
    assert len(hit)==1, m
    cnt[hit[0]]+=1
print("every triangle-free mask matches exactly one host; orbit sizes sum",sum(cnt.values()))
