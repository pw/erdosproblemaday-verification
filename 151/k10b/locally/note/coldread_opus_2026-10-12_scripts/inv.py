import itertools, networkx as nx
from networkx.algorithms import isomorphism as iso
from collections import Counter
W=nx.circulant_graph(8,[1,4])
G21=nx.from_graph6_bytes(b'T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB')
pts=range(7); lines=[frozenset({i,(i+1)%7,(i+3)%7}) for i in range(7)]
flags=[(p,L) for L in lines for p in L]
F=nx.Graph(); F.add_nodes_from(range(21))
for i,(p,L) in enumerate(flags):
    for j,(q,M) in enumerate(flags):
        if i<j and p not in M and q not in L: F.add_edge(i,j)
print("F iso G21:", nx.is_isomorphic(F,G21))
# hand count: neighbours of (p,L) = (q,M), q off L, M through q missing p
ok=True
for i,(p,L) in enumerate(flags):
    hand={(q,M) for q in pts if q not in L for M in lines if q in M and p not in M}
    comp={flags[j] for j in F[i]}
    ok &= (hand==comp and len(hand)==8)
print("hand neighbour description matches, 8 each:", ok)
def report(G,name):
    n=G.number_of_nodes(); E=G.number_of_edges(); degs=set(dict(G.degree()).values())
    tri=sum(nx.triangles(G).values())//3
    links=all(nx.is_isomorphic(G.subgraph(G[v]),W) for v in G)
    om=max(len(c) for c in nx.find_cliques(G)); al=max(len(c) for c in nx.find_cliques(nx.complement(G)))
    lam=Counter(len(set(G[u])&set(G[v])) for u,v in G.edges())
    mu=Counter(); struct=Counter()
    for u,v in itertools.combinations(G,2):
        if not G.has_edge(u,v):
            C=set(G[u])&set(G[v]); H=G.subgraph(C); mu[len(C)]+=1
            struct[(len(C),H.number_of_edges(),tuple(sorted(d for _,d in H.degree())))]+=1
    auts=list(iso.GraphMatcher(G,G).isomorphisms_iter())
    orb={m[0] for m in auts}
    def order(m):
        k=1; cur=dict(m)
        while any(cur[x]!=x for x in cur): cur={x:m[cur[x]] for x in cur}; k+=1
        return k
    oc=Counter(order(m) for m in auts)
    # regular cyclic subgroup <=> element whose cycle type is a single n-cycle
    ncyc=0
    for m in auts:
        x=0; c=0
        while True:
            x=m[x]; c+=1
            if x==0: break
        if c==n and order(m)==n: ncyc+=1
    print(f"{name}: n={n} E={E} deg={degs} tri={tri} linksM8={links} omega={om} alpha={al} girth={nx.girth(G)} diam={nx.diameter(G)} lambda={dict(lam)} mu={dict(mu)} commonnbhd={dict(struct)} |Aut|={len(auts)} VT={len(orb)==n} elt-orders={dict(sorted(oc.items()))} n-cycles={ncyc}")
    return auts
report(F,"F21")
P=nx.Graph(); P.add_nodes_from(range(17)); Q={(x*x)%17 for x in range(1,17)}
P.add_edges_from((a,b) for a in range(17) for b in range(a+1,17) if (b-a)%17 in Q)
report(P,"P17")
print("P17 self-complementary:", nx.is_isomorphic(P, nx.complement(P)))
# links of P17: cubic, triangle-free, alpha
for v in [0]:
    H=P.subgraph(P[v]); print("P17 link: degs",set(dict(H.degree()).values()),"tri",sum(nx.triangles(H).values())//3,"alpha",max(len(c) for c in nx.find_cliques(nx.complement(H))))
# L(Heawood) distance-3
H=nx.heawood_graph(); LH=nx.line_graph(H); d=dict(nx.all_pairs_shortest_path_length(LH))
D3=nx.Graph(); D3.add_nodes_from(LH); D3.add_edges_from((u,v) for u,v in itertools.combinations(LH,2) if d[u][v]==3)
print("dist-3 of L(Heawood) iso F21:", nx.is_isomorphic(D3,F), " diameter L(Heawood):", nx.diameter(LH))
# L(Heawood) vs flags sharing a point or a line: check F's mu=4 pairs are exactly flags sharing an element
share=sum(1 for i,j in itertools.combinations(range(21),2) if (flags[i][0]==flags[j][0] or flags[i][1]==flags[j][1]))
print("pairs of flags sharing point or line:", share)
# Cayley graph of Z7:Z3 with referee's S
def mul(g,h): (a,b),(c,dd)=g,h; return ((a+pow(2,b,7)*c)%7,(b+dd)%3)
Gp=[(a,b) for a in range(7) for b in range(3)]
def inv(g): return next(h for h in Gp if mul(g,h)==(0,0))
S={(0,1),(0,2),(1,0),(1,1),(2,1),(3,2),(6,0),(6,2)}
print("S inverse-closed:", all(inv(s) in S for s in S))
C=nx.Graph(); C.add_nodes_from(Gp); C.add_edges_from((g,h) for g in Gp for h in Gp if g!=h and mul(inv(g),h) in S)
print("Cayley(Z7:Z3,S) iso F21:", nx.is_isomorphic(C,F), "nonabelian:", mul((1,0),(0,1))!=mul((0,1),(1,0)))
# correlations: polarity p -> line, check a duality preserves adjacency
