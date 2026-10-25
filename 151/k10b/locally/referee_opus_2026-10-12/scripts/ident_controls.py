import itertools, networkx as nx
def g(s): return nx.from_graph6_bytes(s.encode())
K333 = nx.complete_multipartite_graph(3,3,3)
rook = lambda a,b: nx.cartesian_product(nx.complete_graph(a), nx.complete_graph(b))
J63 = nx.Graph(); S=[frozenset(c) for c in itertools.combinations(range(6),3)]
J63.add_edges_from((x,y) for x,y in itertools.combinations(S,2) if len(x&y)==2)
roots=[]
for i,j in itertools.combinations(range(4),2):
    for si in (1,-1):
        for sj in (1,-1):
            v=[0]*4; v[i]=si; v[j]=sj; roots.append(tuple(v))
C24=nx.Graph(); C24.add_edges_from((a,b) for a,b in itertools.combinations(roots,2) if sum(x*y for x,y in zip(a,b))==1)
checks = [("K33 answer","H}q|r|}",K333,"K_{3,3,3}"),
          ("Rook33 answer 16","O}zTdMYbY^KvUu[\\fqpzR",nx.complement(rook(4,4)),"complement of K4xK4"),
          ("Rook33 answer 20","S~rLTMYdW?LPXRUJIbXatKjSNM?XrGFo{",J63,"J(6,3)"),
          ("Q3 answer 15","N}qDlY[\\Z\\JwMwO~fbo",nx.complement(rook(3,5)),"complement of K3xK5"),
          ("Q3 answer 24","W}qDlY[?A?cBCEAE?a?Aj?dg?rbc[RQY`WjCHpM?lDW@kM_",C24,"24-cell (D4 roots, inner product 1)")]
for name,s,H,hn in checks: print(f"{name} ≅ {hn}: {nx.is_isomorphic(g(s),H)}")
