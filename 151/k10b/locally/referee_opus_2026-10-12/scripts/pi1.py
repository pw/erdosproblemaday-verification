# H1 of the clique (triangle) complex over F2 and Z, and pi1 order via coset enumeration, for the found graphs.
import sys, itertools, networkx as nx
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
def rank_f2(rows, ncols):
    # rows: list of sets of column indices (F2 vectors); gaussian elimination
    piv = {}
    r = 0
    for row in rows:
        v = 0
        for c in row: v ^= (1 << c)
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; r += 1; break
    return r
for line in open(sys.argv[1]):
    s = line.strip()
    if not s: continue
    G = nx.from_graph6_bytes(s.encode()); n = G.number_of_nodes()
    E = sorted(tuple(sorted(e)) for e in G.edges()); eid = {e:i for i,e in enumerate(E)}
    T = [tuple(sorted(c)) for c in nx.enumerate_all_cliques(G) if len(c)==3]
    assert not any(len(c)==4 for c in nx.enumerate_all_cliques(G))
    # boundary d1: edges -> vertices; d2: triangles -> edges
    r1 = rank_f2([{a,b} for a,b in E], n)
    r2 = rank_f2([{eid[(a,b)],eid[(a,c)],eid[(b,c)]} for a,b,c in T], len(E))
    h1_f2 = (len(E) - r1) - r2
    h2_f2 = len(T) - r2
    # integer H1 via Smith normal form of d2 restricted (cycle space rank over Q via ranks)
    D2 = Matrix.zeros(len(E), len(T))
    for j,(a,b,c) in enumerate(T):
        D2[eid[(a,b)], j] = 1; D2[eid[(b,c)], j] = 1; D2[eid[(a,c)], j] = -1
    D1 = Matrix.zeros(n, len(E))
    for i,(a,b) in enumerate(E): D1[a,i] = -1; D1[b,i] = 1
    rk1 = D1.rank(); rk2 = D2.rank()
    snf = smith_normal_form(D2)
    diag = [snf[i,i] for i in range(min(snf.shape)) if snf[i,i] != 0]
    tors = [abs(d) for d in diag if abs(d) != 1]
    betti1 = (len(E) - rk1) - rk2
    print(f"n={n} |E|={len(E)} |T|={len(T)} chi={n-len(E)+len(T)}  H1(F2) dim={h1_f2}  H2(F2) dim={h2_f2}  H1(Z): rank {betti1}, torsion {tors}", flush=True)
    # pi1: spanning tree generators, triangle relators
    tree = nx.bfs_tree(G, 0); tedges = {tuple(sorted(e)) for e in tree.edges()}
    gens = [e for e in E if e not in tedges]
    F = free_group(" ".join(f"g{i}" for i in range(len(gens))))[0]
    gsym = F.generators; gidx = {e:i for i,e in enumerate(gens)}
    def ed(a,b):
        e = tuple(sorted((a,b)))
        if e in tedges: return F.identity
        g = gsym[gidx[e]]
        return g if a < b else g**-1
    rels = [ed(a,b)*ed(b,c)*ed(c,a) for a,b,c in T]
    P = FpGroup(F, rels)
    try:
        print(f"   pi1 order (coset enumeration): {P.order()}", flush=True)
    except Exception as ex:
        print("   pi1 order: failed", ex)
