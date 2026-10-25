#!/usr/bin/env python3
"""Link census for Erdős #151 at k = 10 (n = R(3,10) ∈ {40,41}).

In a minimum counterexample (Veljjanoski/AlyciaBHZ reduction, Corollary 2): for every vertex v,
beta(P_v) <= d(v) - g, g = R(3,k) - R(3,k-1), P_v = G[N(v)] minus isolated vertices.
Writing i(v) = #isolated vertices of G[N(v)], p = |P_v| = d - i, this is  i + tau(P_v) >= g,
i.e. tau(P) >= g - i  where tau(P) = p - beta(P) is the clique-transversal number of the link.

This script enumerates, for every p <= 9, all graphs P on p vertices WITHOUT isolated vertices
(nauty-geng), computes beta(P) exactly (largest set containing no maximal clique of size >= 2),
and tabulates, for each (d, i), how many links are admissible and what they look like.
beta is computed twice: brute force over subsets (p <= 9 => 512 subsets) and via the complement
characterisation (a set is free iff it contains no maximal clique), as a self-check.
"""
import itertools, subprocess, sys, collections
import networkx as nx

def maximal_cliques(G):
    return [frozenset(c) for c in nx.find_cliques(G) if len(c) >= 2]

def beta_bruteforce(G):
    V = list(G.nodes()); cl = maximal_cliques(G)
    best = 0
    for r in range(len(V), -1, -1):
        for S in itertools.combinations(V, r):
            S = frozenset(S)
            if not any(c <= S for c in cl):
                return r
    return 0

def beta_tau(G):
    """tau = min hitting set of the maximal cliques (size>=2); beta = p - tau."""
    V = list(G.nodes()); cl = maximal_cliques(G)
    for r in range(0, len(V)+1):
        for D in itertools.combinations(V, r):
            D = set(D)
            if all(c & D for c in cl):
                return len(V) - r
    raise RuntimeError

def links(p):
    if p == 0:
        yield nx.empty_graph(0); return
    # geng: -d1 = min degree 1 (no isolated vertices)
    out = subprocess.run(['nauty-geng', '-q', '-d1', str(p)], capture_output=True, text=True).stdout
    for line in out.split():
        yield nx.from_graph6_bytes(line.encode())

def main():
    results = {}
    for p in range(0, 10):
        rows = []
        for G in links(p):
            b1 = beta_bruteforce(G); b2 = beta_tau(G)
            assert b1 == b2, (p, nx.to_graph6_bytes(G), b1, b2)
            tri_free = sum(nx.triangles(G).values()) == 0
            alpha = max(len(c) for c in nx.find_cliques(nx.complement(G))) if p else 0
            Delta = max((d for _, d in G.degree()), default=0)
            rows.append((nx.to_graph6_bytes(G, header=False).decode().strip(), b1, p - b1, alpha, Delta, tri_free))
        results[p] = rows
        print(f"p={p}: {len(rows)} graphs without isolated vertices", file=sys.stderr)
    for n, g in ((40, 4), (41, 5)):
        print(f"\n===== n = {n}, k = 10, g = {g}: admissible links need i + tau(P) >= {g}, d = i + p <= 9 =====")
        print(f"{'d':>2} {'i':>2} {'p':>2} {'#links':>7} {'tri-free':>8} {'max beta':>8} {'alpha range':>11} {'Delta range':>11}")
        total_by_d = collections.Counter()
        for d in range(0, 10):
            for i in range(0, d+1):
                p = d - i
                adm = [r for r in results[p] if i + r[2] >= g]
                if not adm:
                    continue
                total_by_d[d] += len(adm)
                tf = sum(1 for r in adm if r[5])
                print(f"{d:>2} {i:>2} {p:>2} {len(adm):>7} {tf:>8} {max(r[1] for r in adm):>8} "
                      f"{min(r[3] for r in adm):>2}..{max(r[3] for r in adm):<8} {min(r[4] for r in adm):>2}..{max(r[4] for r in adm):<8}")
        print("admissible links per degree d:", dict(total_by_d))
        print("minimum degree forced:", min(total_by_d) if total_by_d else None)
        # list the i = 0 links explicitly (the 'dense' links)
        for d in range(0, 10):
            adm = [r for r in results[d] if r[2] >= g]
            if adm and d >= 7:
                print(f"  i=0, d={d}: {len(adm)} links; triangle-free among them: {[r[0] for r in adm if r[5]][:12]}")
    import json
    json.dump({p: results[p] for p in results}, open('/home/exedev/MathDyad/erdos151/link_census.json', 'w'))

if __name__ == '__main__':
    main()
