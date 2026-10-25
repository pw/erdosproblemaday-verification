import itertools, networkx as nx, sys
for f in sys.argv[1:]:
    lines=open(f).read().splitlines(); g6=lines[0].split()[-1]
    G=nx.from_graph6_bytes(g6.encode())
    red={frozenset(map(int,l.split())) for l in lines[1:] if l.strip() and not l.startswith('#')}
    assert all(G.has_edge(*tuple(e)) for e in red)
    tris=[t for t in itertools.combinations(G,3) if all(G.has_edge(a,b) for a,b in itertools.combinations(t,2))]
    mono=sum(1 for t in tris if len({frozenset(p) in red for p in itertools.combinations(t,2)})==1)
    print(f, "n",G.number_of_nodes(),"edges",G.number_of_edges(),"red",len(red),"triangles",len(tris),"monochromatic",mono)
