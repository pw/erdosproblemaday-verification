import itertools, networkx as nx
W=nx.circulant_graph(8,[1,4]); assert nx.is_isomorphic(W,nx.circulant_graph(8,[3,4]))
hits=[]
for n in range(9,42):
    reps=list(range(1,(n+1)//2 + (0 if n%2 else 1)))  # 1..floor(n/2)
    for k in (3,4):   # S = 4 pairs (8 elems) or 3 pairs + n/2 (needs even n): handled below
        pass
    pairs=[a for a in range(1,(n-1)//2+1)]
    cand=[]
    for T in itertools.combinations(pairs,4): cand.append(sorted(set([t%n for t in T]+[(-t)%n for t in T])))
    if n%2==0:
        for T in itertools.combinations(pairs,3):
            S=sorted(set([t%n for t in T]+[(-t)%n for t in T]+[n//2]))
            if len(S)==7: pass
    for S in cand:
        if len(S)!=8: continue
        Ss=set(S); L=nx.Graph(); L.add_nodes_from(S)
        L.add_edges_from((s,t) for s,t in itertools.combinations(S,2) if (t-s)%n in Ss)
        if L.number_of_edges()==12 and nx.is_isomorphic(L,W): hits.append((n,S))
print("circulants Z_n (n<=41), 8-element symmetric S without n/2, locally Wagner:",len(hits)); 
for h in hits[:40]: print(h)
# even n: S may contain n/2 -> 8 = 1 + 2*3.5 impossible; 8 elements with n/2 means odd count; so no.
