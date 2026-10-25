#!/usr/bin/env python3
"""Computational controls for the k=10 lemmas (Erdős #151 follow-up, 2026-10-12).

Lemma 2' (independent-set version of Veljjanoski's Lemma 2): for an independent set I and, for each v in I,
a set D_v ⊆ N(v) meeting every maximal clique of G[N(v)] (isolated vertices of G[N(v)] counting as cliques),
   beta(G) >= |I| + beta(G - I - ∪D_v).
Corollary (blocking): for any vertex w and any u ∉ N[w],  N(w) ∪ {u} is free  iff  N(u)∩N(w) contains no
maximal clique of G[N(u)] (isolated vertices of G[N(u)] included).
Corollary (lone-edge domination): if |I| = beta(G) is a maximum independent set with alpha(G) = beta(G), then every
u ∉ I has a neighbour v ∈ I with uv in no triangle.   (Direct: I ∪ {u} is free iff no lone edge u–I.)

Each claim is tested on random graphs; each test is MUTATED (a wrong version must fail) so a pass means something.
"""
import itertools, random, sys
import networkx as nx

def maxcl(G):
    return [frozenset(c) for c in nx.find_cliques(G) if len(c) >= 2]

def is_free(S, cl):
    S = frozenset(S); return not any(c <= S for c in cl)

def beta(G):
    V = list(G.nodes()); cl = maxcl(G)
    for r in range(len(V), -1, -1):
        for S in itertools.combinations(V, r):
            if is_free(S, cl): return r
    return 0

def link_transversals(G, v):
    """All minimal D ⊆ N(v) meeting every maximal clique of G[N(v)] incl. isolated vertices."""
    N = list(G.neighbors(v)); H = G.subgraph(N)
    cl = [frozenset(c) for c in nx.find_cliques(H)]  # includes singletons for isolated vertices
    out = []
    for r in range(0, len(N)+1):
        for D in itertools.combinations(N, r):
            D = frozenset(D)
            if all(c & D for c in cl): out.append(D)
        if out: break
    return out, cl

random.seed(151)
tested = {'lemma2p': 0, 'blocking': 0, 'lone': 0}
mut_fail = {'lemma2p': 0, 'blocking': 0, 'lone': 0}
for trial in range(400):
    n = random.randint(6, 11); p = random.choice([0.3, 0.45, 0.6])
    G = nx.gnp_random_graph(n, p, seed=random.randrange(10**9))
    cl = maxcl(G); bG = beta(G)
    # ---- Lemma 2' with |I| in {1,2,3}
    comp = nx.complement(G)
    m = random.choice([1, 2, 3])
    inds = [frozenset(S) for S in itertools.combinations(G.nodes(), m) if all(not G.has_edge(a, b) for a, b in itertools.combinations(S, 2))]
    if not inds:
        inds = [frozenset([v]) for v in G.nodes()]
    I = random.choice(inds)
    Ds = []
    for v in I:
        tr, _ = link_transversals(G, v); Ds.append(random.choice(tr))
    D = frozenset().union(*Ds) if Ds else frozenset()
    H = G.subgraph(set(G.nodes()) - set(I) - D)
    assert bG >= len(I) + beta(H), ("Lemma 2' FAILS", n, p, I, D)
    tested['lemma2p'] += 1
    # mutation: drop the isolated-vertex requirement (D need only hit cliques of size >= 2) -> should sometimes fail
    Dm = []
    for v in I:
        N = list(G.neighbors(v)); Hl = G.subgraph(N)
        cl2 = [frozenset(c) for c in nx.find_cliques(Hl) if len(c) >= 2]
        found = None
        for r in range(0, len(N)+1):
            for Dc in itertools.combinations(N, r):
                if all(c & frozenset(Dc) for c in cl2): found = frozenset(Dc); break
            if found is not None: break
        Dm.append(found)
    Dm = frozenset().union(*Dm) if Dm else frozenset()
    Hm = G.subgraph(set(G.nodes()) - set(I) - Dm)
    if bG < len(I) + beta(Hm): mut_fail['lemma2p'] += 1
    # ---- blocking corollary
    w = random.choice(list(G.nodes())); Nw = set(G.neighbors(w))
    for u in set(G.nodes()) - Nw - {w}:
        free = is_free(Nw | {u}, cl)
        Nu = set(G.neighbors(u)); Hu = G.subgraph(Nu)
        clu = [frozenset(c) for c in nx.find_cliques(Hu)] if Nu else []
        blocked = any(c <= (Nu & Nw) for c in clu)
        assert free == (not blocked), ("blocking FAILS", n, p, w, u)
        tested['blocking'] += 1
        # mutation: ignore isolated link vertices
        blocked_m = any(c <= (Nu & Nw) for c in clu if len(c) >= 2)
        if free != (not blocked_m): mut_fail['blocking'] += 1
    # ---- lone-edge domination (when alpha == beta)
    alpha = max(len(c) for c in nx.find_cliques(comp))
    if alpha == bG:
        lone = {frozenset(e) for e in G.edges() if not (set(G[e[0]]) & set(G[e[1]]))}
        for I in (frozenset(c) for c in nx.find_cliques(comp) if len(c) == alpha):
            for u in set(G.nodes()) - I:
                assert any(frozenset((u, v)) in lone for v in I), ("lone-edge domination FAILS", n, p, I, u)
                tested['lone'] += 1
                # mutation: require an edge in exactly one triangle instead of none
                if not any(G.has_edge(u, v) and len(set(G[u]) & set(G[v])) == 1 for v in I):
                    mut_fail['lone'] += 1
print("tested:", tested)
print("mutated versions failed at least once (must be > 0 for each):", mut_fail)
assert all(v > 0 for v in mut_fail.values()), "a mutation never failed: that control is vacuous"
print("ALL CONTROLS PASS")
