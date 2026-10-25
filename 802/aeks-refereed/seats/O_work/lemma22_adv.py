# Adversarial families for Lemma 2.2: threshold-straddling neighbourhood weights.
import random, sys
from fractions import Fraction as Fr
import networkx as nx
sys.path.insert(0, '/tmp/oaimath/184/seats/O_work/scripts')
from lemma22 import check, multipartite, make_Kr_free, STATS

rng = random.Random(7)
res_all = []
def run(G, w, r, eps, label):
    for rule in ['first', 'maxw', 'minw', 'random']:
        res = check(G, w, r, eps, rule, rng)
        res_all.append((label, r, eps, rule, res))
        if not res['ok'] or not res['ok_mass34']:
            print('FAIL', label, r, eps, rule, res)

# 1. disjoint union of K_{r-1}: total weight s, each vertex weight c; nbhd weight (r-2)c vs eta*s
for r in [3, 4, 5]:
    for k in [2, 3, 5, 8]:
        G = nx.disjoint_union_all([nx.complete_graph(r - 1)] * k)
        n = G.number_of_nodes()
        for eps in [Fr(1, 2), Fr(1, 4), Fr(1, 8)]:
            # uniform weight 1: s = n, nbhd weight r-2; threshold eta*s = eps*n/4
            w = {v: Fr(1) for v in G}
            run(G, w, r, eps, f'unionK{r-1}x{k}')
            # perturb so some nbhds straddle the threshold exactly
            s = Fr(n)
            for v in G:
                w2 = dict(w)
            w2 = {v: Fr(1) + Fr(rng.randint(-50, 50), 1000) for v in G}
            run(G, w2, r, eps, f'unionK{r-1}x{k}-pert')

# 2. exact-threshold equality: neighbourhood weight == eta*s exactly must NOT be removed (strict >)
for r in [3, 4]:
    G = nx.complete_multipartite_graph(*([2] * (r - 1)))
    G = nx.convert_node_labels_to_integers(G)
    n = G.number_of_nodes()
    eps = Fr(1, 2)
    # choose weights so that some nbhd weight equals eps*s/4 exactly is hard with dense graph; scan rationals
    for trial in range(200):
        w = {v: Fr(rng.randint(1, 20), rng.choice([1, 3, 7])) for v in G}
        run(G, w, r, eps, 'multi-scan')

# 3. hubs: many hubs each adjacent to its own K_{r-2}-free block, plus a shared tail
for r in [4, 5]:
    for trial in range(40):
        G = nx.Graph()
        nid = 0
        hubs = rng.randint(2, 4)
        for h in range(hubs):
            hub = nid; nid += 1
            blk = make_Kr_free(rng.randint(2, 4), 0.8, r - 1, rng)
            mp = {}
            for v in blk.nodes(): mp[v] = nid; nid += 1
            G.add_node(hub)
            for v in blk.nodes(): G.add_edge(hub, mp[v])
            for a, b in blk.edges(): G.add_edge(mp[a], mp[b])
        # random extra edges keeping K_r-free
        nodes = list(G.nodes())
        for _ in range(rng.randint(0, 8)):
            a, b = rng.sample(nodes, 2)
            G.add_edge(a, b)
            if any(len(c) >= r for c in nx.find_cliques(G)):
                G.remove_edge(a, b)
        w = {v: Fr(rng.randint(1, 1000), rng.choice([1, 100, 10**4])) for v in G}
        for eps in [Fr(1, 2), Fr(1, 20), Fr(1, 10**4)]:
            run(G, w, r, eps, 'hubs')

n_ok = sum(1 for x in res_all if x[4]['ok'] and x[4]['ok_mass34'])
print('adversarial runs', len(res_all), 'all three properties + 3/4 bound OK:', n_ok)
mx = max(res_all, key=lambda x: x[4]['EM_over_eps_s2'])
print('max E M/(eps s^2):', float(mx[4]['EM_over_eps_s2']), mx[:4])
mx = max(res_all, key=lambda x: x[4]['maxm_over_b'])
print('max (max m)/b_r:', float(mx[4]['maxm_over_b']), mx[:4])
print('max support:', max(x[4]['support'] for x in res_all))
print('min p_i/(eps/8):', float(STATS['pmin_over_eps8']))
