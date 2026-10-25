import itertools, subprocess, networkx as nx
from networkx.algorithms import isomorphism as iso
def g(s): return nx.from_graph6_bytes(s.encode())
def alpha(G): return max(len(c) for c in nx.find_cliques(nx.complement(G)))
def tri(G): return sum(nx.triangles(G).values())//3
NOTE=['G?`F`w','G?bF`w','G?rF`w','G?q`qg','GCQb`o','GCR`r_','GCrb`o']
for i,s in enumerate(NOTE,1):
    G=g(s); print(f"note N8.{i} {s} e={G.number_of_edges()} degs={sorted(d for _,d in G.degree())} alpha={alpha(G)} tri={tri(G)} mindeg={min(d for _,d in G.degree())}")
# Bikov figure readings (octagon positions)
P=['T','TR','R','BR','B','BL','L','TL']; ix={p:i for i,p in enumerate(P)}
def mk(edges):
    G=nx.Graph(); G.add_nodes_from(range(8)); G.add_edges_from((ix[a],ix[b]) for a,b in (e.split('-') for e in edges)); return G
B={}
B[1]=mk(['T-B','T-BR','TL-BR','TL-B','TR-BL','TR-B','L-R','L-BR','R-B','BL-BR'])
B[2]=mk(['T-B','T-BL','TL-B','TL-BR','TR-L','TR-BR','L-R','L-B','R-BL','BL-BR'])
B[4]=mk(['T-B','T-BR','TL-BR','TL-B','TR-BL','TR-B','L-R','L-BR','R-BL','R-B','BL-BR'])
B[5]=mk(['T-B','T-BL','T-BR','TL-R','TL-BR','TL-B','TR-L','TR-BL','TR-BR','L-B','R-BL'])
B[6]=mk(['T-B','T-BR','TL-BR','TL-B','TR-L','TR-BL','TR-B','L-R','L-BR','R-BL','R-B','BL-BR'])
B[7]=nx.circulant_graph(8,[3,4])
for k,G in sorted(B.items()):
    m=[i for i,s in enumerate(NOTE,1) if nx.is_isomorphic(G,g(s))]
    print(f"Bikov fig N8.{k}: e={G.number_of_edges()} tri={tri(G)} alpha={alpha(G)} == note N8.{m}")
B[3]=mk(['T-B','T-BL','T-BR','TL-R','TL-BR','TL-B','TR-L','TR-B','L-BR','R-BL'])
G=B[3]; m=[i for i,s in enumerate(NOTE,1) if nx.is_isomorphic(G,g(s))]
print(f"Bikov fig N8.3: e={G.number_of_edges()} tri={tri(G)} alpha={alpha(G)} == note N8.{m}")
