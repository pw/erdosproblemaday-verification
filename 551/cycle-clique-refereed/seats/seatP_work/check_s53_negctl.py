# Sanity test of Lemma 5.3 (contrapositive): H with alpha(H)<=2, n > max(k, 2*omega(H)), k>=5  ==>  H has C_{k+1}.
import subprocess, sys, networkx as nx
from itertools import combinations
def has_cycle_len(adj, n, L):
    # simple DFS for a cycle of exactly L vertices; start at min vertex
    for s in range(n):
        stack = [(s, 1 << s, 1)]
        # DFS with path
        def dfs(v, mask, ln):
            if ln == L:
                return bool(adj[v] >> s & 1)
            m = adj[v] & ~mask
            while m:
                b = m & -m; w = b.bit_length() - 1; m ^= b
                if w <= s: continue
                if dfs(w, mask | b, ln + 1): return True
            return False
        if dfs(s, 1 << s, 1): return True
    return False
tot = 0; viol = 0
for n in range(6, int(sys.argv[1]) + 1):
    out = subprocess.run(["nauty-geng", "-tq", str(n)], capture_output=True, text=True).stdout.split()
    for g6 in out:
        Hc = nx.from_graph6_bytes(g6.encode())        # triangle-free complement
        H = nx.complement(Hc)                          # alpha(H) <= 2
        om = max(len(c) for c in nx.find_cliques(H)) if H.number_of_edges() else 1
        adj = [0]*n
        for u, w in H.edges(): adj[u] |= 1 << w; adj[w] |= 1 << u
        for k in range(5, n):
            if n > k and n >= 2*om:
                tot += 1
                if not has_cycle_len(adj, n, k+1):
                    viol += 1; print("VIOLATION", n, k, om, g6)
print("instances checked:", tot, "violations:", viol)
