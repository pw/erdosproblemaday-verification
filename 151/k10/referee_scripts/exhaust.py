#!/usr/bin/env python3
"""Hostile-referee exhaustive checks of T1-T5 (NOTES_k10.md) on ALL graphs with <= NMAX vertices (nauty-geng).
Everything is bitmask brute force; beta computed by subset enumeration. Each lemma is tested in its FULL stated
generality (all independent I, all minimal transversals, all independent A), not a special case."""
import sys, subprocess, itertools
import networkx as nx
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
MUT = sys.argv[2] if len(sys.argv) > 2 else ''
fails = {}
def chk(cond, key):
    if MUT:
        if not cond: fails[key] = fails.get(key, 0) + 1
        return
    assert cond, key

def graphs(n):
    out = subprocess.run(['nauty-geng', '-q', str(n)], capture_output=True, text=True).stdout.split()
    for s in out: yield nx.from_graph6_bytes(s.encode())

def setup(G):
    n = G.number_of_nodes(); adj = [0]*n
    for a, b in G.edges(): adj[a] |= 1 << b; adj[b] |= 1 << a
    cl = [sum(1 << v for v in c) for c in nx.find_cliques(G) if len(c) >= 2]
    return n, adj, cl

def free(S, cl): return all((c & S) != c for c in cl)

def beta_mask(mask, adj):
    """beta of G[mask]: maximal cliques of the induced subgraph, brute force."""
    verts = [v for v in range(len(adj)) if mask >> v & 1]
    H = nx.Graph(); H.add_nodes_from(verts)
    for v in verts:
        for u in verts:
            if u < v and adj[v] >> u & 1: H.add_edge(u, v)
    cl = [sum(1 << x for x in c) for c in nx.find_cliques(H) if len(c) >= 2]
    best = 0
    # enumerate subsets of mask
    sub = mask
    while True:
        pc = bin(sub).count('1')
        if pc > best and all((c & sub) != c for c in cl): best = pc
        if sub == 0: break
        sub = (sub - 1) & mask
    return best

def subsets(m):
    sub = m
    while True:
        yield sub
        if sub == 0: break
        sub = (sub - 1) & m

def popc(x): return bin(x).count('1')

def link_min_transversals(v, adj):
    N = adj[v]; verts = [u for u in range(len(adj)) if N >> u & 1]
    H = nx.Graph(); H.add_nodes_from(verts)
    for a in verts:
        for b in verts:
            if a < b and adj[a] >> b & 1: H.add_edge(a, b)
    cls = [sum(1 << x for x in c) for c in nx.find_cliques(H)] if verts else []  # incl. singletons
    best = None; res = []
    for r in range(len(verts)+1):
        for D in itertools.combinations(verts, r):
            Dm = sum(1 << x for x in D)
            if all(c & Dm for c in cls): res.append(Dm)
        if res: return res, cls
    return [0], cls

def indep_sets(n, adj, within=None):
    within = (1 << n) - 1 if within is None else within
    sub = within
    while True:
        ok = True
        x = sub
        while x:
            v = (x & -x).bit_length() - 1; x &= x - 1
            if adj[v] & sub: ok = False; break
        if ok: yield sub
        if sub == 0: break
        sub = (sub - 1) & within

stats = dict(graphs=0, T1=0, T2=0, T3=0, T4=0, T5=0, DeltaBeta=0, K4free_col=0)
for n in range(1, NMAX+1):
    for G in graphs(n):
        stats['graphs'] += 1
        n_, adj, cl = setup(G); full = (1 << n) - 1
        bG = beta_mask(full, adj)
        lone = [(a, b) for a, b in G.edges() if not (adj[a] & adj[b])]
        NL = [0]*n
        for a, b in lone: NL[a] |= 1 << b; NL[b] |= 1 << a
        # Delta(P) <= beta(P) for P = G itself
        assert max((popc(a) for a in adj), default=0) <= bG; stats['DeltaBeta'] += 1
        trans = [link_min_transversals(v, adj) for v in range(n)]
        # T1 clique bound: for v in a clique K, |K|>=3 => beta(P_v) >= |K|-2 ; beta(P_v) = beta of G[N(v)] minus isolated
        for v in range(n):
            N = adj[v]; iso = 0
            x = N
            while x:
                u = (x & -x).bit_length() - 1; x &= x - 1
                if not (adj[u] & N): iso |= 1 << u
            bP = beta_mask(N & ~iso, adj) if (N & ~iso) else 0
            assert popc(trans[v][0][0]) == popc(N) - bP, ("t(v) != d - beta(P_v)", nx.to_graph6_bytes(G), v)
            for c in nx.find_cliques(G):
                if v in c and len(c) >= 3:
                    chk(bP >= len(c) - (1 if MUT=='T1' else 2), 'T1'); stats['T1'] += 1
        # T2: every independent I (nonempty), every combination of minimal transversals
        for I in (range(1, full+1) if MUT=='T2' else indep_sets(n, adj)):
            if I == 0: continue
            Iv = [v for v in range(n) if I >> v & 1]
            for combo in itertools.product(*[trans[v][0] for v in Iv]):
                D = 0
                for d in combo: D |= d
                rest = full & ~I & ~D
                chk(bG >= popc(I) + beta_mask(rest, adj), 'T2')
                stats['T2'] += 1
        # T3: for every w, U_w; every independent A in U_w: N(w) | A free
        for w in range(n):
            Nw = adj[w]; U = 0
            for u in range(n):
                if u == w or (Nw >> u & 1): continue
                # maximal cliques of G[N(u)] incl. singletons
                Nu = adj[u]; vs = [x for x in range(n) if Nu >> x & 1]
                H = G.subgraph(vs)
                blocked = any((sum(1 << x for x in c) & ~(Nu & Nw)) == 0 for c in nx.find_cliques(H)) if vs else False
                if not blocked: U |= 1 << u
            for A in (subsets(U) if MUT=='T3' else indep_sets(n, adj, U)):
                chk(free(Nw | A, cl), 'T3'); stats['T3'] += 1
        # T4: every independent I, every independent A outside I with no lone edge to I
        for I in indep_sets(n, adj):
            cand = 0
            for u in range(n):
                if not (I >> u & 1) and not (NL[u] & I): cand |= 1 << u
            for A in (subsets(cand) if MUT=='T4' else indep_sets(n, adj, cand)):
                chk(free(I | A, cl), 'T4'); stats['T4'] += 1
        # T5: for each lone edge va: S = (NL(v)-a) | (NL(a)-v); S minus ANY vertex cover of lone edges between halves is free
        for (v, a) in lone + [(b, a) for a, b in lone]:
            X1 = NL[v] & ~(1 << a); X2 = NL[a] & ~(1 << v)
            assert X1 & X2 == 0
            S = X1 | X2
            le = [(x, y) for x, y in lone if ((X1 >> x & 1) and (X2 >> y & 1)) or ((X1 >> y & 1) and (X2 >> x & 1))]
            sub = S
            while True:
                if MUT=='T5' or all((sub >> x & 1) or (sub >> y & 1) for x, y in le):
                    chk(free(S & ~sub, cl), 'T5'); stats['T5'] += 1
                if sub == 0: break
                sub = (sub - 1) & S
    print(n, stats, flush=True)
print("MUTATION", MUT, "fails:", fails) if MUT else print("ALL EXHAUSTIVE CHECKS PASS", stats)
