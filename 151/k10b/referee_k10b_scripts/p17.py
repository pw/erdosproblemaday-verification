import sys, itertools, networkx as nx
sys.path.insert(0,'/tmp/ref151b/scripts')
exec(open(''+__import__('os').path.join(__import__('os').path.dirname(__file__),'check3.py')+'').read().split('# controls')[0])
QR={(x*x)%17 for x in range(1,17)}
E=[(a,b) for a,b in itertools.combinations(range(17),2) if (b-a)%17 in QR]
A=adjs(17,E); T=triangles(17,E,A)
G=nx.Graph(E); W=nx.circulant_graph(8,[1,4])
print("P17: edges",len(E),"triangles",len(T),"K4-free:",max(len(c) for c in nx.find_cliques(G))==3,
      "every link = Wagner:",all(nx.is_isomorphic(G.subgraph(G[v]),W) for v in G))
print("P17 arrows (3,3):",arrows(17,E))
