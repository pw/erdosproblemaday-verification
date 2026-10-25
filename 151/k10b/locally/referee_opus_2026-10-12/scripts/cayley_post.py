import networkx as nx, collections
P17=nx.from_graph6_bytes(b"P|fLKfH[QJkSVDMJDrGm]A|g"); G21=nx.from_graph6_bytes(b"T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB")
tabs={}
lines=open("/tmp/ref151/gap/tables.txt").read().split("\n"); i=0
while i<len(lines):
    if not lines[i].strip(): i+=1; continue
    h=lines[i].split(None,2); n,g=int(h[0]),int(h[1]); tabs[(n,g)]=[list(map(int,lines[i+1+r].split())) for r in range(n)]; i+=1+n
summary=collections.Counter()
for l in open("/tmp/ref151/cayley_S.txt"):
    p=l.split(); n,g=int(p[1]),int(p[2]); S=list(map(int,p[3:])); T=tabs[(n,g)]
    C=nx.Graph(); C.add_nodes_from(range(n)); C.add_edges_from((x,T[x][s]) for x in range(n) for s in S)
    comps=[C.subgraph(c) for c in nx.connected_components(C)]
    desc=[("P17" if nx.is_isomorphic(H,P17) else "G21" if nx.is_isomorphic(H,G21) else f"OTHER{H.number_of_nodes()}") for H in comps]
    summary[(n,g,len(comps),tuple(sorted(collections.Counter(desc).items())))]+=1
for k,v in sorted(summary.items()): print(f"SmallGroup({k[0]},{k[1]}): {v} connection sets -> {k[2]} component(s): {dict(k[3])}")
