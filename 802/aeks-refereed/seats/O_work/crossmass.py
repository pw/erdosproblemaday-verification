# Brute-force test of (2.5) at the (multi-start) global maximizer: all pairs S, D.
import sys, random, math
import numpy as np, networkx as nx
sys.path.insert(0, '/tmp/oaimath/184/seats/O_work/scripts')
from maxim import global_max, F

def subset_sums(vals):
    s = np.zeros(1)
    for a in vals:
        s = np.concatenate([s, s + a])
    return s  # index bit i <-> vals[i]

def gx(x, s):
    return np.where(s > 0, s * (x + np.maximum(0, -np.log(np.where(s > 0, s, 1)))), 0.0)

def worst_ratio(A, w, xs, disjoint_too=True):
    n = len(w)
    N = 1 << n
    wsum = subset_sums(w)  # w(D) for all D, and w(S) for all S
    out = {x: (0.0, None) for x in xs}
    outd = {x: (0.0, None) for x in xs}
    masks = np.arange(N)
    for S in range(1, N):
        sind = np.array([(S >> i) & 1 for i in range(n)], float)
        wS = wsum[S]
        a = w * (A @ (sind * w))  # a_v = w_v w(N(v) ∩ S)
        e = subset_sums(a)        # e_w(S, D) for all D
        for x in xs:
            if wS > math.exp(x):
                continue
            g = float(gx(x, np.array(wS)))
            ok = wsum <= math.exp(x)
            m = np.max(np.where(ok, e, -1))
            if m / g > out[x][0]:
                D = int(np.argmax(np.where(ok, e, -1)))
                out[x] = (m / g, (S, D))
            if disjoint_too:
                okd = ok & ((masks & S) == 0)
                md = np.max(np.where(okd, e, -1))
                if md / g > outd[x][0]:
                    outd[x] = (md / g, (S, int(np.argmax(np.where(okd, e, -1)))))
    return out, outd

def make_Kr_free(n, p, r, rng):
    G = nx.gnp_random_graph(n, p, seed=rng.randrange(10**9))
    while True:
        cl = [c for c in nx.find_cliques(G) if len(c) >= r]
        if not cl: return G
        c = rng.choice(cl); a, b = rng.sample(c, 2); G.remove_edge(a, b)

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]))
    ngraphs = int(sys.argv[2]); nmax = int(sys.argv[3])
    xs = [1.0, 1.5, 2.0, 3.0, 10.0]
    graphs = []
    for t in range(ngraphs):
        kind = rng.choice(['gnp', 'gnp', 'tri', 'bip', 'blowC5', 'k4free_dense'])
        n = rng.randint(5, nmax)
        if kind == 'gnp':
            G = make_Kr_free(n, rng.choice([0.4, 0.6, 0.8, 1.0]), 4, rng)
        elif kind == 'tri':
            sz = [rng.randint(1, max(1, n // 2)) for _ in range(3)]
            G = nx.convert_node_labels_to_integers(nx.complete_multipartite_graph(*sz))
        elif kind == 'bip':
            sz = [rng.randint(1, n - 1)]; sz.append(max(1, n - sz[0]))
            G = nx.convert_node_labels_to_integers(nx.complete_multipartite_graph(*sz))
        elif kind == 'blowC5':
            # blow-up of C5 with random part sizes (triangle-free)
            sizes = [rng.randint(1, 2) for _ in range(5)]
            G = nx.Graph(); parts = []; c = 0
            for s in sizes:
                parts.append(list(range(c, c + s))); c += s
            G.add_nodes_from(range(c))
            for i in range(5):
                for a in parts[i]:
                    for b in parts[(i + 1) % 5]:
                        G.add_edge(a, b)
        else:
            # random 3-partite graph with dense cross edges (K4-free automatically)
            lab = [rng.randrange(3) for _ in range(n)]
            G = nx.Graph(); G.add_nodes_from(range(n))
            for a in range(n):
                for b in range(a + 1, n):
                    if lab[a] != lab[b] and rng.random() < 0.85:
                        G.add_edge(a, b)
        if G.number_of_nodes() > nmax:
            continue
        assert not any(len(c) >= 4 for c in nx.find_cliques(G))
        graphs.append((kind, G))
    glob = {x: (0, None) for x in xs}; globd = {x: (0, None) for x in xs}
    maxres = 0; nonlocal_ = 0
    for kind, G in graphs:
        A, w, val, res, loc, nloc = global_max(G, seed=rng.randrange(10**6))
        maxres = max(maxres, res)
        if not loc: nonlocal_ += 1
        out, outd = worst_ratio(A, w, xs)
        for x in xs:
            if out[x][0] > glob[x][0]: glob[x] = (out[x][0], kind, G.number_of_nodes(), G.number_of_edges(), nloc)
            if outd[x][0] > globd[x][0]: globd[x] = (outd[x][0], kind, G.number_of_nodes(), G.number_of_edges())
    print(f'graphs={len(graphs)} max stationarity residual={maxres:.2e} best-point-not-local-max={nonlocal_}')
    for x in xs:
        print(f'x={x}: worst e_w(S,D)/g_x(w(S)) all pairs = {glob[x][0]:.4f} {glob[x][1:]} | disjoint pairs = {globd[x][0]:.4f}  (claim: <= 16r^2 = 256; disjoint proof constant A_4+3 = {7+8*2+(1+8)*math.log(2):.2f})')
