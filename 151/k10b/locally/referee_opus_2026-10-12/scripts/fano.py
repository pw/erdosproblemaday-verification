import itertools, networkx as nx
G = nx.from_graph6_bytes(b"T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB")
lines = [frozenset({i%7,(i+1)%7,(i+3)%7}) for i in range(7)]
flags = [(p,L) for L in lines for p in L]; assert len(flags)==21
inc = nx.Graph()  # Heawood graph
for p,L in flags: inc.add_edge(('p',p),('L',L))
LH = nx.line_graph(inc); LH = nx.convert_node_labels_to_integers(LH)
D = dict(nx.all_pairs_shortest_path_length(LH))
print("L(Heawood): n", LH.number_of_nodes(), "deg", set(dict(LH.degree()).values()), "diam", nx.diameter(LH), "distance-regular", nx.is_distance_regular(LH), nx.intersection_array(LH) if nx.is_distance_regular(LH) else "")
for d in (2,3):
    H = nx.Graph(); H.add_nodes_from(LH)
    H.add_edges_from((u,v) for u in LH for v in LH if u<v and D[u][v]==d)
    print(f"distance-{d} graph of L(Heawood): deg {set(dict(H.degree()).values())}, iso to G21: {nx.is_isomorphic(H,G)}")
# explicit flag description: (p,L)~(q,M) iff p not in M and q not in L  (and p!=q, L!=M)
H = nx.Graph(); H.add_nodes_from(range(21))
for i,j in itertools.combinations(range(21),2):
    (p,L),(q,M) = flags[i],flags[j]
    if p not in M and q not in L: H.add_edge(i,j)
print("flags, adjacent iff p∉M and q∉L: deg", set(dict(H.degree()).values()), "iso G21:", nx.is_isomorphic(H,G))
# Cayley graph on Z7 x| Z3: elements (a,b), (a,b)*(c,d) = (a + 2^b c mod 7, b+d mod 3)
els = [(a,b) for a in range(7) for b in range(3)]
def mul(x,y): return ((x[0] + pow(2,x[1],7)*y[0])%7, (x[1]+y[1])%3)
def inv(x):
    for y in els:
        if mul(x,y)==(0,0): return y
idx = {e:i for i,e in enumerate(els)}
W = nx.circulant_graph(8,[1,4])
from itertools import combinations
nonid = [e for e in els if e!=(0,0)]
pairs = []; seen=set()
for e in nonid:
    if e in seen: continue
    f = inv(e); seen.add(e); seen.add(f); pairs.append((e,f))
print("F21 inverse-pairs:", len(pairs))
found = []
for S4 in combinations(pairs, 4):
    S = set(x for pr in S4 for x in pr)
    if len(S)!=8: continue
    L = nx.Graph(); L.add_nodes_from(S)
    for s,t in combinations(S,2):
        if mul(inv(s),t) in S: L.add_edge(s,t)
    if all(d==3 for _,d in L.degree()) and nx.is_isomorphic(L,W):
        C = nx.Graph(); C.add_nodes_from(range(21))
        for g in els:
            for s in S: C.add_edge(idx[g], idx[mul(g,s)])
        found.append((sorted(S), nx.is_connected(C), nx.is_isomorphic(C,G)))
print("locally-M8 Cayley graphs on F21 = Z7:Z3:", len(found), " connected/iso-to-G21:", sorted(set((c,i) for _,c,i in found)))
print("example S:", found[0][0] if found else None)
