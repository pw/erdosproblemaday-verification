# Exact implementation of Lemma 2.2 (random multipliers), enumerating the finite law with Fractions.
import itertools, random, sys
from fractions import Fraction as Fr
import networkx as nx

def b_r(r, eps):
    return Fr(2) ** (r * (r - 2)) * (Fr(1) / eps) ** (r - 2)

def has_clique(G, nodes, k):
    H = G.subgraph(nodes)
    if k <= 1: return len(nodes) >= k
    for c in nx.find_cliques(H):
        if len(c) >= k: return True
    return False

STATS = {'pmin_over_eps8': None}

def multipliers(G, nodes, w, r, eps, rule, rng):
    """Return law: list of (prob, {v: m_v}) over vertices `nodes`."""
    nodes = list(nodes)
    if not nodes:
        return [(Fr(1), {})]
    assert not has_clique(G, nodes, r), "input not K_r-free"
    if r == 2:
        assert G.subgraph(nodes).number_of_edges() == 0
        return [(Fr(1), {v: Fr(1) for v in nodes})]
    s = sum(w[v] for v in nodes)
    eta = eps / 4
    remaining = set(nodes)
    parts = []
    while True:
        elig = []
        for u in sorted(remaining):
            nw = sum(w[x] for x in G[u] if x in remaining)
            if nw > eta * s:
                elig.append((u, nw))
        if not elig:
            break
        if rule == 'first':
            u = elig[0][0]
        elif rule == 'maxw':
            u = max(elig, key=lambda t: (t[1], -t[0]))[0]
        elif rule == 'minw':
            u = min(elig, key=lambda t: (t[1], t[0]))[0]
        else:
            u = rng.choice(elig)[0]
        Vi = sorted(x for x in G[u] if x in remaining)
        # K_{r-1}-freeness of the removed neighbourhood
        assert not has_clique(G, Vi, r - 1), "neighbourhood contains K_{r-1}"
        parts.append(Vi)
        remaining -= set(Vi)
    R = sorted(remaining)
    # remainder edge mass (2.4)
    MR = sum(w[a] * w[b] for a, b in G.subgraph(R).edges())
    assert MR <= eta * s * sum(w[v] for v in R) / 2 <= eta * s * s / 2
    if not parts:
        return [(Fr(1), {v: Fr(1) for v in nodes})]
    si = [sum(w[v] for v in P) for P in parts]
    for x in si:
        assert x > eta * s
    b = sum(si)
    assert b <= s
    law = []
    zero = {v: Fr(0) for v in nodes}
    m = dict(zero)
    for v in R: m[v] = Fr(2)
    law.append((Fr(1, 2), m))
    for P, sP in zip(parts, si):
        p = sP / (2 * b)
        assert p > eps / 8, (p, eps)
        ratio = p / (eps / 8)
        if STATS['pmin_over_eps8'] is None or ratio < STATS['pmin_over_eps8']:
            STATS['pmin_over_eps8'] = ratio
        sub = multipliers(G, P, w, r - 1, eps / 4, rule, rng)
        for q, mp in sub:
            m = dict(zero)
            for v in P: m[v] = mp[v] / p
            law.append((p * q, m))
    return law

def check(G, w, r, eps, rule, rng):
    nodes = sorted(G.nodes())
    law = multipliers(G, nodes, w, r, eps, rule, rng)
    s = sum(w[v] for v in nodes)
    tot = sum(p for p, _ in law)
    assert tot == 1, tot
    B = b_r(r, eps)
    maxm = max((m[v] for _, m in law for v in nodes), default=Fr(0))
    minm = min((m[v] for _, m in law for v in nodes), default=Fr(0))
    means = {v: sum(p * m[v] for p, m in law) for v in nodes}
    EM = sum(p * sum(w[a] * m[a] * w[b] * m[b] for a, b in G.edges()) for p, m in law)
    ok_mean = all(means[v] == 1 for v in nodes)
    ok_range = (minm >= 0) and (maxm <= B)
    ok_mass = EM <= eps * s * s
    ok_mass34 = EM <= Fr(3, 4) * eps * s * s or EM <= eps * s * s / 8
    return dict(ok=ok_mean and ok_range and ok_mass, ok_mean=ok_mean, ok_range=ok_range, ok_mass=ok_mass,
                ok_mass34=ok_mass34, support=len(law), maxm_over_b=maxm / B, EM_over_eps_s2=EM / (eps * s * s),
                M0_over_eps_s2=sum(w[a]*w[b] for a,b in G.edges())/(eps*s*s))

def make_Kr_free(n, p, r, rng):
    G = nx.gnp_random_graph(n, p, seed=rng.randrange(10**9))
    while True:
        cl = [c for c in nx.find_cliques(G) if len(c) >= r]
        if not cl: return G
        c = rng.choice(cl)
        a, b = rng.sample(c, 2)
        G.remove_edge(a, b)

def multipartite(sizes):
    G = nx.complete_multipartite_graph(*sizes)
    return nx.convert_node_labels_to_integers(G)

def rand_weights(G, rng, mode):
    w = {}
    for v in G.nodes():
        if mode == 'unif':
            w[v] = Fr(rng.randint(1, 100), 100)
        elif mode == 'heavy':
            w[v] = Fr(rng.randint(1, 1000), rng.choice([1, 10, 1000, 10**6]))
        else:
            w[v] = Fr(1)
    return w

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    ntests = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    epss = [Fr(1, 2), Fr(1, 4), Fr(1, 8), Fr(1, 50), Fr(1, 1000), Fr(1, 10**6)]
    worst = {}
    nfail = 0; count = 0
    for t in range(ntests):
        r = rng.choice([3, 4, 4, 5, 5])
        kind = rng.choice(['gnp', 'gnp', 'turan', 'multi'])
        if kind == 'gnp':
            n = rng.randint(4, 12 if r < 5 else 11)
            G = make_Kr_free(n, rng.choice([0.3, 0.5, 0.7, 0.9]), r, rng)
        elif kind == 'turan':
            n = rng.randint(r - 1, 12)
            k = r - 1
            sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
            G = multipartite([x for x in sizes if x > 0])
        else:
            k = rng.randint(2, r - 1)
            G = multipartite([rng.randint(1, 4) for _ in range(k)])
        mode = rng.choice(['unif', 'heavy', 'ones'])
        w = rand_weights(G, rng, mode)
        eps = rng.choice(epss)
        rule = rng.choice(['first', 'maxw', 'minw', 'random'])
        res = check(G, w, r, eps, rule, rng)
        count += 1
        if not res['ok'] or not res['ok_mass34']:
            nfail += 1
            print('FAIL', kind, r, eps, rule, G.number_of_nodes(), res)
        key = r
        cur = worst.get(key)
        if cur is None:
            worst[key] = dict(maxm=res['maxm_over_b'], EM=res['EM_over_eps_s2'], supp=res['support'])
        else:
            cur['maxm'] = max(cur['maxm'], res['maxm_over_b']); cur['EM'] = max(cur['EM'], res['EM_over_eps_s2']); cur['supp'] = max(cur['supp'], res['support'])
    print('tests', count, 'failures', nfail)
    for r in sorted(worst):
        c = worst[r]
        print(f"r={r}: max (max m_v)/b_r = {float(c['maxm']):.3e}; max E M/(eps s^2) = {float(c['EM']):.4f}; max support = {c['supp']}")
    print('min p_i/(eps/8) over all recursion levels:', float(STATS['pmin_over_eps8']))
