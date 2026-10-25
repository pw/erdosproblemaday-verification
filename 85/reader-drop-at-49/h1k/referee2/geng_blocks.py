"""Independent decision of the k = 5 instances by exhaustive enumeration (nauty-geng, no SAT, no h1cube code):
all 4-regular C4-free graphs on 18 vertices (geng -f -d4 -D4 18), and for each, every partition of V into 6 triples T
satisfying the block rule (every vertex has <= 1 neighbour in T  <=>  pairwise codegree 0 inside T, which also forces
e(T) <= 1).  Reports, per graph, the partitions found and their e-patterns, and which admit a pairing of the 6 blocks
into 3 pairs with no edges between paired blocks (the non-relaxed block form).  Usage: geng_blocks.py file.g6"""
import sys, itertools
import networkx as nx

def partitions(G):
    V = sorted(G); adj = {v: set(G[v]) for v in V}
    ok = lambda a, b: not (adj[a] & adj[b])
    tri = [T for T in itertools.combinations(V, 3) if all(ok(a, b) for a, b in itertools.combinations(T, 2))]
    by = {v: [T for T in tri if v in T] for v in V}
    out = []
    def rec(used, chosen):
        free = [v for v in V if v not in used]
        if not free:
            out.append(list(chosen)); return
        v = free[0]
        for T in by[v]:
            if used.isdisjoint(T):
                chosen.append(T); rec(used | set(T), chosen); chosen.pop()
    rec(set(), [])
    return out, adj

def e(T, adj): return sum(1 for a, b in itertools.combinations(T, 2) if b in adj[a])

graphs = nx.read_graph6(sys.argv[1]); graphs = graphs if isinstance(graphs, list) else [graphs]
tot_p = tot_e1 = tot_pairable = tot_e1_pairable = 0
for gi, G in enumerate(graphs):
    P, adj = partitions(G)
    e1 = [p for p in P if all(e(T, adj) == 1 for T in p)]
    def pairable(p):
        blocks = [set(T) for T in p]
        cross = lambda X, Y: any(b in adj[a] for a in blocks[X] for b in blocks[Y])
        def rec(rem):
            if not rem: return True
            X = rem[0]
            return any(not cross(X, Y) and rec([Z for Z in rem if Z not in (X, Y)]) for Y in rem[1:])
        return rec(list(range(6)))
    pp = [p for p in P if pairable(p)]
    tot_p += len(P); tot_e1 += len(e1); tot_pairable += len(pp); tot_e1_pairable += sum(1 for p in pp if p in e1)
    if P:
        pats = sorted({tuple(sorted(e(T, adj) for T in p)) for p in P})
        print(f"graph {gi}: {len(P)} block partitions, e-patterns {pats}, all-e=1: {len(e1)}, pairable: {len(pp)}")
print(f"TOTAL over {len(graphs)} graphs: partitions {tot_p}, with e==1 on every block {tot_e1}, "
      f"pairable (no paired-block edges) {tot_pairable}, pairable AND e==1 {tot_e1_pairable}")
