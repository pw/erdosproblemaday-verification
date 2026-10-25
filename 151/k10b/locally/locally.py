#!/usr/bin/env python3
"""Enumerate connected graphs G in which every vertex's induced neighbourhood is isomorphic to a given graph X
("locally X" graphs), with at most NMAX vertices.  Vertex-by-vertex completion: vertex 0 gets the link X; then each
vertex v in index order is completed — its known neighbours K must embed as an INDUCED subgraph of X (embeddings
quotiented by Aut(X)), the free link slots are filled by existing undecided vertices or by new vertices, and the
link edges/non-edges among N(v) are forced from X; v is then closed (all remaining pairs become non-edges).  A
branch dies when an edge would hit a closed vertex or a forced non-edge, a non-edge an existing edge, a degree
exceeds k, or the vertex count exceeds NMAX.  Output: the found graphs up to isomorphism, with node counts.
Controls (classical theorems): locally K3 = {K4}; locally C4 = {octahedron}; locally C5 = {icosahedron};
locally Petersen on <= 21 vertices = {Kneser K(7,2)} (Hall 1980: 21, 63, 65).  usage: locally.py X NMAX  (X in
{K3,C4,C5,C6,Petersen,M8,Q3})"""
import sys, itertools, time
import networkx as nx
from networkx.algorithms import isomorphism as iso
sys.setrecursionlimit(10000)
def make_X(name):
    return {'K3': nx.complete_graph(3), 'C4': nx.cycle_graph(4), 'C5': nx.cycle_graph(5), 'C6': nx.cycle_graph(6),
            'Petersen': nx.petersen_graph(), 'M8': nx.circulant_graph(8,[1,4]), 'Q3': nx.hypercube_graph(3)}[name]
class Search:
    def __init__(self, X, nmax, verbose=False, dump=None):
        self.dump = dump
        X = nx.convert_node_labels_to_integers(X); self.X = X; self.k = X.number_of_nodes(); self.nmax = nmax
        self.Xadj = [set(X[i]) for i in range(self.k)]
        self.auts = [tuple(m[i] for i in range(self.k)) for m in iso.GraphMatcher(X, X).isomorphisms_iter()]
        self.found = []; self.nodes = 0; self.verbose = verbose; self.t0 = time.time(); self.maxn = 0; self.refused = 0
    def embeddings(self, K, adj, non):
        """embeddings phi: K -> V(X) respecting every DECIDED pair (edge -> X-edge, forced non-edge -> X-non-edge;
        undecided pairs are free and get decided by the completion), one representative per Aut(X)-orbit"""
        out = []
        def bt(i, phi, used):
            if i == len(K): out.append(tuple(phi)); return
            u = K[i]
            for x in range(self.k):
                if x in used: continue
                ok = True
                for j in range(i):
                    w = K[j]; ex = (phi[j] in self.Xadj[x])
                    if (w in adj[u] and not ex) or (w in non[u] and ex): ok = False; break
                if ok: phi.append(x); used.add(x); bt(i+1, phi, used); phi.pop(); used.discard(x)
        bt(0, [], set())
        reps = []
        for phi in out:
            orbit_min = min(tuple(s[x] for x in phi) for s in self.auts)
            if orbit_min == phi: reps.append(phi)
        return reps
    def run(self):
        k = self.k; n = k + 1
        adj = [set() for _ in range(n)]; non = [set() for _ in range(n)]
        for i in range(k): adj[0].add(i+1); adj[i+1].add(0)
        for a in range(k):
            for b in range(a+1, k):
                if b in self.Xadj[a]: adj[a+1].add(b+1); adj[b+1].add(a+1)
                else: non[a+1].add(b+1); non[b+1].add(a+1)
        self.rec(adj, non, {0}, 1)
        return self.found
    def record(self, adj):
        G = nx.Graph(); G.add_nodes_from(range(len(adj)))
        for u in range(len(adj)):
            for w in adj[u]:
                if u < w: G.add_edge(u, w)
        for H in self.found:
            if H.number_of_nodes() == G.number_of_nodes() and nx.is_isomorphic(G, H): return
        self.found.append(G)
        g6 = nx.to_graph6_bytes(G, header=False).decode().strip()
        print(f"  FOUND locally-X graph on {G.number_of_nodes()} vertices, {G.number_of_edges()} edges  (search nodes {self.nodes}, {time.time()-self.t0:.0f}s)  graph6 {g6}", flush=True)
        if self.dump:
            with open(self.dump, "a") as f: f.write(g6 + "\n")
    def rec(self, adj, non, closed, v):
        self.nodes += 1
        if self.verbose and self.nodes % 100000 == 0:
            print(f"  ... {self.nodes} nodes, {len(adj)} vertices in state, completing v={v}, {time.time()-self.t0:.0f}s", flush=True)
        n = len(adj)
        self.maxn = max(self.maxn, n)
        if v == n: self.record(adj); return
        k = self.k; K = sorted(adj[v])
        if len(K) > k: return
        U = [u for u in range(n) if u != v and u not in adj[v] and u not in non[v]]
        for phi in self.embeddings(K, adj, non):
            pos = {K[i]: phi[i] for i in range(len(K))}
            slots = [s for s in range(k) if s not in set(phi)]
            self.fill(adj, non, closed, v, K, pos, slots, 0, {}, U, 0)
    def fill(self, adj, non, closed, v, K, pos, slots, i, assign, U, newcount):
        n = len(adj)
        if i == len(slots):
            self.complete(adj, non, closed, v, pos, assign, newcount); return
        s = slots[i]
        # existing undecided vertices
        for u in U:
            if u in assign.values(): continue
            ok = True
            for w, pw in pos.items():       # consistency with known neighbours of v
                if pw in self.Xadj[s]:
                    if w in non[u] or (w in closed and u not in adj[w]): ok = False; break
                else:
                    if w in adj[u]: ok = False; break
            if ok:
                for s2, u2 in assign.items():    # consistency with earlier filled slots
                    if u2 < 0: continue
                    if s2 in self.Xadj[s]:
                        if u2 in non[u]: ok = False; break
                    else:
                        if u2 in adj[u]: ok = False; break
            if ok:
                assign[s] = u; self.fill(adj, non, closed, v, K, pos, slots, i+1, assign, U, newcount); del assign[s]
        # a new vertex (indices allocated in slot order; new vertices are interchangeable, so one branch)
        if n + newcount + 1 <= self.nmax:
            assign[s] = -(newcount+1); self.fill(adj, non, closed, v, K, pos, slots, i+1, assign, U, newcount+1); del assign[s]
        else: self.refused += 1
    def complete(self, adj, non, closed, v, pos, assign, newcount):
        n = len(adj); k = self.k
        adj = [set(a) for a in adj] + [set() for _ in range(newcount)]
        non = [set(a) for a in non] + [set() for _ in range(newcount)]
        closed = set(closed)
        where = dict(pos)                       # vertex -> X-position
        for s, u in assign.items():
            if u < 0: u = n + (-u) - 1
            where[u] = s
        def add_edge(a, b):
            if b in adj[a]: return True
            if a in closed or b in closed or b in non[a]: return False
            adj[a].add(b); adj[b].add(a)
            return len(adj[a]) <= k and len(adj[b]) <= k
        def add_non(a, b):
            if b in adj[a]: return False
            non[a].add(b); non[b].add(a); return True
        for u in where:
            if u not in adj[v]:
                if not add_edge(v, u): return
        Nv = list(where)
        for a, b in itertools.combinations(Nv, 2):
            if where[b] in self.Xadj[where[a]]:
                if not add_edge(a, b): return
            else:
                if not add_non(a, b): return
        if len(adj[v]) != k: return
        closed.add(v)
        for u in range(len(adj)):
            if u != v and u not in adj[v]: non[v].add(u); non[u].add(v)
        # a vertex with degree k whose known link already contradicts X dies later at its own completion
        self.rec(adj, non, closed, v + 1)
if __name__ == "__main__":
    name, nmax = sys.argv[1], int(sys.argv[2]); verbose = "-v" in sys.argv
    dump = None
    for a in sys.argv[3:]:
        if a.startswith("--dump="): dump = a[7:]
    S = Search(make_X(name), nmax, verbose, dump)
    print(f"locally {name} (k={S.k}, |Aut X|={len(S.auts)}), NMAX={nmax}", flush=True)
    found = S.run()
    print(f"DONE: {len(found)} graph(s) up to isomorphism: {[(G.number_of_nodes(), G.number_of_edges()) for G in found]}; search nodes {S.nodes}; max vertices in play {S.maxn}; branches refused by the cap {S.refused}; {time.time()-S.t0:.1f}s", flush=True)
