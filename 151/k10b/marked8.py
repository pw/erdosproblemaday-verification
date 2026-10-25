#!/usr/bin/env python3
"""Re-derive Bikov's seven 'marked' triangle-free 8-vertex graphs N8.1..N8.7 (referee's criterion, verbatim),
enumerate the (3,4;8)-graphs (triangle-free, alpha<=3, 8 vertices), and test whether any N8.i is a spanning
subgraph (not nec. induced) of a (3,4;8)-graph.  Controls: K4 marked, K3 not; (3,4;8) count must be 3; C8 and the
Wagner graph as containment controls (C8 IS a spanning subgraph of the Wagner graph; K_{4,4} is NOT a subgraph of
any (3,4;8)-graph because alpha(K44)=4 and adding edges inside a side makes a triangle... actually K44 has
alpha 4 so it is not itself (3,4;8); containment control: the empty graph on 8 vertices embeds in everything)."""
import itertools, subprocess, sys
import networkx as nx, numpy as np
from networkx.algorithms import isomorphism as iso

def marked(N):
    E = list(N.edges()); m = len(E); p = N.number_of_nodes()
    cs = np.arange(1 << m, dtype=np.int64)
    alive = np.ones(1 << m, dtype=bool)
    for f in range(1 << p):
        mR = 0; mB = 0
        for i, (a, b) in enumerate(E):
            fa, fb = f >> a & 1, f >> b & 1
            if fa and fb: mR |= 1 << i
            if not fa and not fb: mB |= 1 << i
        ok = ((cs & mR) == 0) & (((~cs) & mB) == 0)
        alive &= ~ok
        if not alive.any(): return False
    return bool(alive.any())

assert marked(nx.complete_graph(4)) and not marked(nx.complete_graph(3))
def geng(args):
    return subprocess.run(['nauty-geng','-q']+args, capture_output=True, text=True).stdout.split()
def alpha(G):
    return max(len(c) for c in nx.find_cliques(nx.complement(G)))
tf8 = geng(['-t','8'])
N8 = [s for s in tf8 if marked(nx.from_graph6_bytes(s.encode()))]
print("triangle-free 8-vertex graphs:", len(tf8), "; marked (N8.i):", len(N8), N8)
R348 = [s for s in tf8 if alpha(nx.from_graph6_bytes(s.encode())) <= 3]
print("(3,4;8)-graphs:", len(R348), R348, "edges:", [nx.from_graph6_bytes(s.encode()).number_of_edges() for s in R348])
assert len(R348) == 3, "control: exactly three (3,4;8)-graphs are known"
def spanning_sub(H, N):   # is N (8 vertices) a spanning subgraph of H (8 vertices)?
    GM = iso.GraphMatcher(H, N)
    return GM.subgraph_is_monomorphic()
C8 = nx.cycle_graph(8); W = nx.circulant_graph(8,[1,4])
assert alpha(W)==3 and spanning_sub(W, C8) and spanning_sub(W, nx.empty_graph(8))
assert not spanning_sub(C8, W)
for s in N8:
    N = nx.from_graph6_bytes(s.encode())
    hits = [h for h in R348 if spanning_sub(nx.from_graph6_bytes(h.encode()), N)]
    print(f"N8 {s}: edges={N.number_of_edges()} degs={sorted(d for _,d in N.degree())} alpha={alpha(N)} "
          f"spanning subgraph of (3,4;8)-graphs: {hits}")
