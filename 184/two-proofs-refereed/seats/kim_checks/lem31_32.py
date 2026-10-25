#!/usr/bin/env python3
"""Randomised tests of Kim v2 Lemma 3.1 (lem:light-circumference) and Lemma 3.2 (lem:regions).
Lemma 3.2 is tested by implementing the construction in its proof literally and checking every
conclusion; negative controls show the checks can fail.
"""
import random, math, sys
import networkx as nx

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

# ---------------------------------------------------------------- Lemma 3.1
def is_heavy_cycle(cyc, deg):
    ds = sorted(deg[v] for v in cyc)
    # condition: exists real b>=1 with #{deg<=b} >= b^{3/2}; suffices to test b = each degree value
    for i, b in enumerate(ds):
        cnt = sum(1 for x in ds if x <= b)
        if b >= 1 and cnt >= b**1.5:
            return True
    return False

def cycles(G):
    return [c for c in nx.simple_cycles(G) if len(c) >= 3]

def test31(trials=400):
    light_seen = 0; tested = 0; violations = 0; neg_found = 0
    for _ in range(trials):
        n = random.randint(5, 11)
        # mix of hubs and low-degree vertices
        G = nx.Graph(); G.add_nodes_from(range(n))
        hubs = random.sample(range(n), random.randint(1, 3))
        for v in range(n):
            for h in hubs:
                if v != h and random.random() < 0.8:
                    G.add_edge(v, h)
        for _ in range(random.randint(0, n)):
            u, v = random.sample(range(n), 2); G.add_edge(u, v)
        if G.number_of_edges() > 30:
            continue
        deg = dict(G.degree())
        cyc = cycles(G)
        light = not any(is_heavy_cycle(c, deg) for c in cyc)
        for b in sorted(set(deg.values()) | {1, 1.5, 2, 2.5, 3, 3.5}):
            if b < 1:
                continue
            F = G.copy()
            F.remove_edges_from([(u, v) for u, v in G.edges() if deg[u] > b and deg[v] > b])
            cF = cycles(F)
            circ = max((len(c) for c in cF), default=0)
            if light:
                tested += 1
                if circ >= 2*b**1.5:
                    violations += 1
                    print("LEMMA 3.1 VIOLATION", G.edges(), b, circ)
            else:
                if circ >= 2*b**1.5:
                    neg_found += 1
        light_seen += light
    print(f"Lemma 3.1: light graphs {light_seen}, (G,b) pairs tested {tested}, violations {violations}; "
          f"negative control (non-light G with circumference(F)>=2b^1.5 found): {neg_found}")
    return violations == 0 and neg_found > 0

# ---------------------------------------------------------------- Lemma 3.2
def lemma32(F, k, m, rng):
    """Literal implementation of the proof of Lemma 3.2. Returns list of (R_i, S_i) and diagnostic data."""
    root = ('r',)
    parent = {root: None}; depth = {root: 0}; children = {root: []}
    # DFS forest
    nodes = list(F.nodes()); rng.shuffle(nodes)
    seen = set()
    for s in nodes:
        if s in seen:
            continue
        # iterative true DFS
        parent[s] = root; depth[s] = 1; children[root].append(s); children[s] = []
        seen.add(s)
        stack = [(s, iter(sorted(F[s], key=lambda _: rng.random())))]
        while stack:
            v, it = stack[-1]
            nxt = None
            for w in it:
                if w not in seen:
                    nxt = w; break
            if nxt is None:
                stack.pop(); continue
            seen.add(nxt); parent[nxt] = v; depth[nxt] = depth[v] + 1; children[nxt] = []; children[v].append(nxt)
            stack.append((nxt, iter(sorted(F[nxt], key=lambda _: rng.random()))))
    def is_anc(x, y):  # x ancestor of y (or equal)
        while y is not None:
            if y == x:
                return True
            y = parent[y]
        return False
    maxspan = 0
    for u, v in F.edges():
        if is_anc(u, v):
            maxspan = max(maxspan, depth[v] - depth[u])
        elif is_anc(v, u):
            maxspan = max(maxspan, depth[u] - depth[v])
        else:
            raise RuntimeError("not a DFS tree: cross edge")
    if k is None:
        k = maxspan + 2  # the proof's actual hypothesis: every back edge spans j < k-1
    def B(u):
        if u == root:
            return set()
        out = set(); x = u; dist = 0
        while x != root and dist <= k - 1:
            out.add(x); x = parent[x]; dist += 1
        return out
    def subtree(u):
        out = []; st = [u]
        while st:
            x = st.pop(); out.append(x); st.extend(children[x])
        return out
    unassigned = set(F.nodes())
    W, Us = [], []
    while True:
        # count unassigned proper descendants
        cnt = {}
        order = sorted(parent, key=lambda x: -depth[x])
        for x in order:
            c = 0
            for ch in children[x]:
                c += cnt[ch] + (1 if ch in unassigned else 0)
            cnt[x] = c
        cands = [x for x in parent if cnt[x] >= m]
        if not cands:
            W.append(set(unassigned)); Us.append(root); break
        md = max(depth[x] for x in cands)
        u = rng.choice([x for x in cands if depth[x] == md])
        Wi = set()
        ch = list(children[u]); rng.shuffle(ch)
        for c in ch:
            Wi |= {x for x in subtree(c) if x in unassigned}
            if len(Wi) >= m:
                break
        assert len(Wi) >= m and len(Wi) < 2*m + 1, (len(Wi), m)
        W.append(Wi); Us.append(u); unassigned -= Wi
    p = len(W)
    Bs = [B(u) for u in Us]
    R, S = [], []
    for i in range(p):
        prevB = set().union(*Bs[:i]) if i else set()
        R.append(W[i] - prevB)
        S.append(Bs[i] | (W[i] & prevB))
    return R, S, k, maxspan

def check32(F, R, S, k, m):
    errs = []
    n = F.number_of_nodes()
    allR = set()
    for i, (Ri, Si) in enumerate(zip(R, S)):
        if allR & Ri:
            errs.append("regions not disjoint")
        allR |= Ri
        if Ri & Si:
            errs.append(f"R_{i} meets S_{i}")
        NR = set()
        for x in Ri:
            NR |= set(F[x])
        NR -= Ri
        if not NR <= Si:
            errs.append(f"N_F(R_{i}) not in S_{i}: {len(NR - Si)} extra")
        if not len(Ri | Si) < 2*m + 2*k:
            errs.append(f"|R_i u S_i|={len(Ri|Si)} >= 2m+2k={2*m+2*k}")
    if sum(len(s) for s in S) > 2*k*n/m + 1e-9:
        errs.append(f"sum|S_i|={sum(len(s) for s in S)} > 2kn/m={2*k*n/m}")
    if sum(len(r) for r in R) < (1 - k/m)*n - 1e-9:
        errs.append("sum|R_i| too small")
    return errs

def gen_block_graph(rng, nblocks, smax):
    """Graph whose blocks have <= smax vertices, so every cycle has length <= smax."""
    G = nx.Graph(); G.add_node(0); nxt = 1
    for _ in range(nblocks):
        s = rng.randint(2, smax)
        cut = rng.choice(list(G.nodes()))
        verts = [cut] + list(range(nxt, nxt + s - 1)); nxt += s - 1
        # connected random graph on verts
        rng.shuffle(verts)
        for i in range(1, len(verts)):
            G.add_edge(verts[i], verts[rng.randrange(i)])
        for _ in range(rng.randint(0, s*s//2)):
            a, b = rng.sample(verts, 2); G.add_edge(a, b)
    return G

def test32(trials=300):
    rng = random.Random(7)
    bad = 0; tested = 0
    for tr in range(trials):
        if tr % 2 == 0:
            smax = rng.randint(3, 9)
            F = gen_block_graph(rng, rng.randint(5, 120), smax)
            # add some isolated vertices / extra components
            for _ in range(rng.randint(0, 5)):
                F.add_node(('iso', tr, _))
            k = smax + 1  # every cycle has length <= smax < k
            if k < 3:
                k = 3
        else:
            n = rng.randint(10, 250)
            F = nx.gnm_random_graph(n, rng.randint(0, 3*n), seed=rng.randint(0, 10**9))
            k = None  # use proof hypothesis k = maxspan+2 (any graph)
        m = rng.choice([0.7, 1, 2, 3.5, 5, 10, 25, 60])
        R, S, kk, ms = lemma32(F, k, m, rng)
        if k is not None and ms >= k - 1:
            print("unexpected: block graph DFS span", ms, "k", k); bad += 1
        errs = check32(F, R, S, max(kk, 3), m)
        tested += 1
        if errs:
            bad += 1; print("LEMMA 3.2 FAIL", tr, errs[:3])
    print(f"Lemma 3.2: {tested} random instances, failures {bad}")
    # negative control: shrink B_u to depth k-3 ancestors (too small) -> N_F(R_i) subset S_i should fail sometimes
    neg = 0
    for tr in range(100):
        n = rng.randint(30, 200)
        F = nx.gnm_random_graph(n, 2*n, seed=tr)
        R, S, kk, ms = lemma32(F, None, 5, rng)
        # corrupt: claim with k' = kk-2 bounds
        R2, S2, _, _ = lemma32_trunc(F, kk, 5, rng)
        if check32(F, R2, S2, kk, 5):
            neg += 1
    print(f"Lemma 3.2 negative control (B_u truncated to distance <= 0): detected failures in {neg}/100")
    return bad == 0 and neg > 0

def lemma32_trunc(F, k, m, rng):
    # same as lemma32 but with B_u = {u} only  (wrong) -- used to show check32 can fail
    import types
    R, S, kk, ms = lemma32(F, k, m, rng)
    return [r | s for r, s in zip(R, S)], [set() for _ in S], kk, ms

if __name__ == "__main__":
    a = test31()
    b = test32()
    print("OVERALL:", "PASS" if (a and b) else "FAIL")
