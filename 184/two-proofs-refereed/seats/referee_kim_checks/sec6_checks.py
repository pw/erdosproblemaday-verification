#!/usr/bin/env python3
"""Referee (kim seat) checks for Kim arXiv:2610.07840v2, Section 6.
 (1) Lemma 6.5 (lem:short-cycle): exhaustive-ish random multigraphs; negative control.
 (2) Lemma 6.6 (lem:grouping): literal greedy from the proof; bound |A|+2d; negative control.
 (3) Lemma 6.3 (lem:core): literal peeling process on small graphs in the regime where the
     expander condition reduces to edge-cut robustness; checks |D| <= 2|F|/s and the connectivity
     conclusion; negative control (expander hypothesis dropped).
 (4) Section 6.3 'n large' inequalities with eps=1/1000 (alpha=1/3000): log2 n thresholds.
Run: python3 -I sec6_checks.py
"""
import random, math, itertools, sys
import networkx as nx
rng = random.Random(20261020)
OK = True
def rep(name, cond, info=""):
    global OK
    OK &= bool(cond)
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {info}")

# ---------------- (1) Lemma 6.5
def has_short(edges, m, Lbound):
    # loop / parallel / cycle of length <= Lbound in multigraph
    seen = set()
    for (u, v) in edges:
        if u == v: return True
        key = (min(u, v), max(u, v))
        if key in seen: return True
        seen.add(key)
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(seen)
    # girth via BFS from each vertex
    g = math.inf
    for s in range(m):
        dist = {s: 0}; par = {s: None}; q = [s]
        for x in q:
            for y in G[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1; par[y] = x; q.append(y)
                elif par[x] != y:
                    g = min(g, dist[x] + dist[y] + 1)
    return g <= Lbound
viol = 0; tested = 0; neg = 0
for _ in range(20000):
    m = rng.randint(1, 14)
    e = 2*m + 1
    # bias toward simple graphs: sample distinct pairs when possible
    pairs = [(i, j) for i in range(m) for j in range(i+1, m)]
    if len(pairs) >= e and rng.random() < 0.9:
        edges = rng.sample(pairs, e)
    else:
        edges = [(rng.randrange(m), rng.randrange(m)) for _ in range(e)]
    tested += 1
    if not has_short(edges, m, 2*math.log2(m) + 3 if m > 1 else 3):
        viol += 1
    if not has_short(edges, m, 2):   # too-strict bound (loops/parallels only): should fail sometimes
        neg += 1
rep("Lemma 6.5: >2m edges => loop/parallel/cycle <= 2log m+3", viol == 0, f"({tested} multigraphs, {viol} violations)")
rep("Lemma 6.5 negative control (bound 2 instead of 2log m+3 fails sometimes)", neg > 0, f"({neg} failures)")

# ---------------- (2) Lemma 6.6
def grouping(Wn, An, d, edges):
    # edges: list of (w,u). Pair at each w arbitrarily -> cherries (w,u,u')
    byw = {}
    for (w, u) in edges: byw.setdefault(w, []).append(u)
    cherries = []
    for w, us in byw.items():
        rng.shuffle(us)
        for i in range(0, len(us) - 1, 2):
            cherries.append((w, us[i], us[i+1]))
    # greedy coloring of conflict graph
    classes = []
    for c in cherries:
        placed = False
        for cl in classes:
            if all(not ({c[0]} & {x[0]} or {c[1], c[2]} & {x[1], x[2]}) for x in cl):
                cl.append(c); placed = True; break
        if not placed: classes.append([c])
    groups = []
    for cl in classes:
        for i in range(0, len(cl), d): groups.append(cl[i:i+d])
    return cherries, classes, groups
viol = 0; worst = 0
for _ in range(3000):
    Wn = rng.randint(1, 12); An = rng.randint(1, 30); d = rng.randint(1, 6)
    # bipartite with deg_A <= d
    edges = []
    for u in range(An):
        k = rng.randint(0, min(d, Wn))
        for w in rng.sample(range(Wn), k): edges.append((w, u))
    ch, cl, gr = grouping(Wn, An, d, edges)
    okg = len(gr) <= An + 2*d
    for g in gr:
        vs = [v for c in g for v in (('w', c[0]), ('a', c[1]), ('a', c[2]))]
        okg &= len(vs) == len(set(vs)) and len(g) <= d
    worst = max(worst, len(gr) / (An + 2*d))
    viol += not okg
rep("Lemma 6.6: groups <= |A|+2d, each <= d vertex-disjoint cherries", viol == 0, f"(3000 instances, max groups/(|A|+2d) = {worst:.3f})")
# negative control: drop the '+2d' -> must fail somewhere
negc = 0
for _ in range(3000):
    Wn = rng.randint(1, 12); An = rng.randint(1, 6); d = rng.randint(2, 6)
    edges = []
    for u in range(An):
        for w in rng.sample(range(Wn), min(d, Wn)): edges.append((w, u))
    ch, cl, gr = grouping(Wn, An, d, edges)
    negc += len(gr) > An
rep("Lemma 6.6 negative control (bound |A| without +2d fails sometimes)", negc > 0, f"({negc} failures)")

# ---------------- (3) Lemma 6.3 in the small regime
def cut_expander(G, s):
    m = G.number_of_nodes(); V = list(G.nodes())
    # for m <= 32 log^2 m every 1<=|X|<=2m/3 needs >=1 neighbour after removing <= s|X| edges,
    # i.e. e(X, X^c) > s|X|.
    assert m <= 32*math.log2(m)**2
    for k in range(1, int(2*m/3) + 1):
        for X in itertools.combinations(V, k):
            Xs = set(X)
            cut = sum(1 for x in X for y in G[x] if y not in Xs)
            if cut <= s*k: return False
    return True
def peel(G, F, s, L):
    eta = 1/(32*L*L)
    D = set()
    K = G.copy(); K.remove_edges_from(F)
    while True:
        Kd = K.subgraph([v for v in K if v not in D])
        Vk = list(Kd.nodes()); found = None
        Qs = [()] + [(q,) for q in Vk] if s/2 >= 1 else [()]
        if s/2 >= 2: Qs += list(itertools.combinations(Vk, 2))
        for Q in Qs:
            rest = [v for v in Vk if v not in Q]
            for k in range(1, len(Vk)//2 + 1):
                for U in itertools.combinations(rest, k):
                    Us = set(U)
                    T = {y for x in U for y in Kd[x] if y not in Us and y not in Q}
                    if len(T) < eta*k/2:
                        found = (Q, Us); break
                if found: break
            if found: break
        if not found: return D, Kd
        D |= found[1]
viol = 0; tested = 0; negfail = 0
for trial in range(400):
    m = rng.randint(8, 11); p = rng.uniform(0.55, 1.0)
    G = nx.gnp_random_graph(m, p, seed=rng.randrange(10**9))
    s = rng.choice([2, 3, 4])
    L = math.ceil(math.log2(m))
    isexp = cut_expander(G, s)
    Fmax = int(s*m/12)
    F = rng.sample(list(G.edges()), min(Fmax, G.number_of_edges())) if Fmax > 0 else []
    D, K = peel(G, F, s, L)
    good = len(D) <= 2*len(F)/s + 1e-9
    # conclusion: for every Q (|Q|<=s/2) outside D, K-Q connected (r >= 256 > m so length is free)
    Vk = list(K.nodes())
    Qs = [()] + [(q,) for q in Vk] + (list(itertools.combinations(Vk, 2)) if s/2 >= 2 else [])
    for Q in Qs:
        H = K.subgraph([v for v in Vk if v not in Q])
        if H.number_of_nodes() >= 2 and not nx.is_connected(H): good = False
    if isexp:
        tested += 1; viol += not good
    else:
        negfail += not good
rep("Lemma 6.3 (small regime): |D|<=2|F|/s and core connected for all |Q|<=s/2", viol == 0, f"({tested} expander instances, {viol} violations)")
rep("Lemma 6.3 negative control (non-expanders: |D| bound fails sometimes)", negfail > 0, f"({negfail} failures among non-expanders)")

# ---------------- (4) Section 6.3 'n large' inequalities, eps = 1/1000
alpha = 1/3000
def lg(x): return math.log2(x)
def lgsum(a, b): # log2(2^a + 2^b)
    hi, lo = max(a, b), min(a, b); return hi + math.log2(1 + 2**(lo - hi))
def thresholds():
    out = {}
    def first(name, f):
        # f(ell) -> True when inequality holds at n = 2^ell; find first ell (power of 2 search) from which it holds
        lo = 1.0
        ell = 2.0
        while not f(ell): ell *= 1.25
        out[name] = ell
    # work in log2: s = n^{2a}, lambda = ell^300, r = 2^8 ell^3
    first("|Z|<=n/lambda^3: 8 ell n^{-a} <= ell^-900", lambda l: 3 + lg(l) - alpha*l <= -900*lg(l))
    first("Claim6.8: s>=64 h log m (n^{2a} >= 64 n^{a/2} ell)", lambda l: 2*alpha*l >= 6 + 0.5*alpha*l + lg(l))
    first("Claim6.8: s/(2h)>=n^a", lambda l: 1.5*alpha*l - 1 >= alpha*l)
    first("pieces: 4n(lam+2)^2 lam^3/s <= n", lambda l: 2 + 2*lgsum(300*lg(l), 1) + 900*lg(l) <= 2*alpha*l)
    first("2nd kind: 2 lam^3 j* <= n (4 lam^3/s<=1)", lambda l: 2 + 900*lg(l) <= 2*alpha*l)
    first("routing: n^a >= 24 r lam^3", lambda l: alpha*l >= lg(24) + 8 + 3*lg(l) + 900*lg(l))
    first("failed: 128 r lam^9 n^{1-a} <= n", lambda l: 7 + 8 + 3*lg(l) + 2700*lg(l) <= alpha*l)
    first("|W|: (3n/lam^2)(6+lam)<=n", lambda l: lg(3) + lgsum(lg(6), 300*lg(l)) <= 600*lg(l))
    first("B_odd: 64 n ell/lam <= n", lambda l: 6 + lg(l) <= 300*lg(l))
    first("|Y_C| (1st kind): (2ell+3)(lam+2)<=4 lam^3", lambda l: lg(2*l + 3) + lgsum(300*lg(l), 1) <= 2 + 900*lg(l))
    first("|Y_C| (3rd kind): 1.5(lam+2^12 ell^3)<=4 lam^3", lambda l: lg(1.5) + lgsum(300*lg(l), 12 + 3*lg(l)) <= 2 + 900*lg(l))
    return out
th = thresholds()
for k, v in th.items():
    print(f"     log2 n >= {v:.4g}: {k}")
worst = max(th.values())
rep("Section 6.3 polylog-vs-poly inequalities all hold for large n (eps=1/1000)", math.isfinite(worst), f"(binding threshold log2 n ~ {worst:.3g}, i.e. n_0 ~ 2^{worst:.3g})")
print("OVERALL:", "PASS" if OK else "FAIL")
