#!/usr/bin/env python3
"""Second instrument for marked8.py's containment table: brute force over all 8! vertex bijections, no networkx
matcher.  Reads graph6 by hand (no nx.from_graph6_bytes either).  Prints the same table; the two must agree."""
import itertools
def g6_edges(s):
    b=[ord(c)-63 for c in s]; n=b[0]; bits=''.join(format(x,'06b') for x in b[1:])
    E=set(); k=0
    for j in range(1,n):
        for i in range(j):
            if bits[k]=='1': E.add((i,j))
            k+=1
    return n,E
N8=['G?`F`w','G?bF`w','G?rF`w','G?q`qg','GCQb`o','GCR`r_','GCrb`o']
R348=['GCQb`o','GCR`r_','GCrb`o']
def contained(N,H):
    n,EN=g6_edges(N); m,EH=g6_edges(H); assert n==m==8
    for perm in itertools.permutations(range(8)):
        if all(((perm[a],perm[b]) in EH or (perm[b],perm[a]) in EH) for a,b in EN): return True
    return False
# controls
C8='G?`@`_'  # not needed as g6; build by hand
def edges_to_g6check(): pass
# empty graph on 8 vertices embeds everywhere; a graph with 13 edges can't embed in a 12-edge one
assert all(contained('G???????',h) for h in R348)
assert not contained('GCrb`o','GCQb`o')   # 12 edges into 10: impossible
assert contained('GCrb`o','GCrb`o')
for s in N8:
    hits=[h for h in R348 if contained(s,h)]
    print(f"N8 {s}: spanning subgraph of (3,4;8)-graphs: {hits}")
