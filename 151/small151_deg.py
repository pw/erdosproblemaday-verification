#!/usr/bin/env python3
"""Erdős #151 on small n: is τ(G) ≤ n − H(n) for every graph on n vertices?
τ(G) = min size of a set meeting every maximal clique of size ≥ 2 (equivalently n − max size of a set
containing no maximal clique of size ≥ 2). H(n) = max k with every triangle-free n-vertex graph having an
independent k-set = max{k : R(3,k) ≤ n} (R(3,k): 1,3,6,9,14,18,23,28,36 for k=1..9).
Prune: if α(G) ≥ H(n) an independent set works. Report every graph with τ(G) > n − H(n)."""
import subprocess, itertools, sys
R3 = {1: 1, 2: 3, 3: 6, 4: 9, 5: 14, 6: 18, 7: 23, 8: 28, 9: 36}
def Hn(n): return max(k for k, r in R3.items() if r <= n)
def parse_g6(s):
    data = [ord(c) - 63 for c in s]; n = data[0]; bits = []
    for d in data[1:]: bits += [(d >> (5 - i)) & 1 for i in range(6)]
    adj = [0] * n; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: adj[i] |= 1 << j; adj[j] |= 1 << i
            k += 1
    return n, adj
def maximal_cliques(n, adj):
    # Bron–Kerbosch on bitmasks
    out = []
    def bk(R, P, X):
        if not P and not X:
            if bin(R).count("1") >= 2: out.append(R)
            return
        u = (P | X).bit_length() - 1
        cand = P & ~adj[u]
        while cand:
            v = cand & -cand; cand ^= v; vi = v.bit_length() - 1
            bk(R | v, P & adj[vi], X & adj[vi]); P &= ~v; X |= v
    bk(0, (1 << n) - 1, 0); return out
def alpha(n, adj):
    best = 0
    def rec(P, size):
        nonlocal best
        if size + bin(P).count("1") <= best: return
        if not P: best = max(best, size); return
        v = P & -P; vi = v.bit_length() - 1
        rec(P & ~adj[vi] & ~v, size + 1); rec(P & ~v, size)
    rec((1 << n) - 1, 0); return best
def max_cliquefree_set(n, adj, cliques, need):
    # is there a set S of size `need` containing no maximal clique? (then τ ≤ n - need)
    for S in itertools.combinations(range(n), need):
        m = sum(1 << i for i in S)
        if not any((c & m) == c for c in cliques): return True
    return False
def main():
    for n in [int(x) for x in sys.argv[1:]]:
        h = Hn(n); total = 0; checked = 0; bad = []
        proc = subprocess.Popen(["nauty-geng", "-q", "-D" + str(Hn(n) - 1), str(n)], stdout=subprocess.PIPE, text=True)
        for line in proc.stdout:
            total += 1; nn, adj = parse_g6(line.strip())
            if alpha(nn, adj) >= h: continue
            checked += 1; cl = maximal_cliques(nn, adj)
            if not max_cliquefree_set(nn, adj, cl, h): bad.append(line.strip())
        print(f"n={n} H(n)={h}: {total} graphs, {checked} with alpha<H checked, counterexamples: {len(bad)} {bad[:5]}", flush=True)
main()
