# Section 6 checks: (6.2) exact under the stationarity substitution + numeric at true maximizers;
# (6.3) first line as an exact combinatorial identity; (6.4)/(6.5) at maximizers; greedy induction of Prop 6.1.
import sys, math, random, itertools
from fractions import Fraction as Fr
import numpy as np, networkx as nx
sys.path.insert(0, '/tmp/oaimath/184/seats/O_work/scripts')
from maxim import global_max, F
from crossmass import make_Kr_free

rng = random.Random(3)
def tri_mass(G, w):
    return sum(w[a] * w[b] * w[c] for a, b, c in (t for t in itertools.combinations(G.nodes(), 3)
               if G.has_edge(t[0], t[1]) and G.has_edge(t[0], t[2]) and G.has_edge(t[1], t[2])))
def M(G, w, nodes=None):
    E = G.edges() if nodes is None else G.subgraph(nodes).edges()
    return sum(w[a] * w[b] for a, b in E)

# (6.3) first line, exact, arbitrary positive rational weights
fails63 = 0
for t in range(300):
    G = make_Kr_free(rng.randint(3, 10), rng.choice([0.3, 0.6, 0.9]), rng.choice([4, 5]), rng)
    w = {v: Fr(rng.randint(1, 50), rng.randint(1, 50)) for v in G}
    W = sum(w.values())
    lhs = sum(w[v] * (w[v] + sum(w[u] for u in G[v]) + M(G, w, [v] + list(G[v]))) for v in G)
    rhs = sum(w[v] ** 2 for v in G) + 2 * M(G, w) + sum(w[v] ** 2 * sum(w[u] for u in G[v]) for v in G) + 3 * tri_mass(G, w)
    if lhs != rhs: fails63 += 1
print('(6.3) first-line identity, exact, 300 graphs: failures =', fails63)

# (6.2) exact with log(1/w_u) replaced by L_u := w(N(u)) (the stationarity relation (2.1))
fails62 = 0
for t in range(300):
    G = make_Kr_free(rng.randint(2, 10), rng.choice([0.3, 0.6, 0.9]), 4, rng)
    w = {v: Fr(rng.randint(1, 50), rng.randint(1, 50)) for v in G}
    L = {v: sum(w[u] for u in G[v]) for v in G}
    Fsub = lambda nodes: sum(w[u] * (1 + L[u]) for u in nodes) - M(G, w, nodes)   # F with -log w_u := L_u
    for v in G:
        Av = [v] + list(G[v]); rest = [u for u in G if u not in Av]
        if Fsub(list(G)) - Fsub(rest) != sum(w[u] for u in Av) + M(G, w, Av): fails62 += 1
print('(6.2) exact under stationarity substitution: failures =', fails62)

# numeric (6.2), (6.4), (6.5) at true maximizers, and greedy induction of Prop 6.1
maxerr62 = 0; viol64 = 0; viol65 = 0; nchk = 0; greedy_rows = []
for t in range(60):
    G = make_Kr_free(rng.randint(5, 12), rng.choice([0.4, 0.6, 0.8]), 4, rng)
    G = nx.convert_node_labels_to_integers(G)
    Delta = max(3, max(dict(G.degree()).values()))
    A, w, Fstar, res, loc, _ = global_max(G, nrand=30, seed=t)
    n = len(w); W = w.sum(); Mw = 0.5 * w @ A @ w
    nchk += 1
    if W < n / Delta - 1e-12: viol64 += 1
    if 2 * Mw / W > math.log(Delta) + 1e-12: viol65 += 1
    for v in range(n):
        Av = [v] + list(np.nonzero(A[v])[0]); rest = [u for u in range(n) if u not in Av]
        Ar_ = A[np.ix_(rest, rest)]
        lhs = Fstar - (F(Ar_, w[rest]) if rest else 0.0)
        rhs = w[Av].sum() + 0.5 * w[Av] @ A[np.ix_(Av, Av)] @ w[Av]
        maxerr62 = max(maxerr62, abs(lhs - rhs))
    # greedy induction along the proof
    H = G.copy(); chosen = 0; worst_beta = 0.0; ok = True; F0 = Fstar
    while H.number_of_nodes() > 0:
        H = nx.convert_node_labels_to_integers(H)
        A, w, Fs, _, _, _ = global_max(H, nrand=20, seed=chosen)
        m = len(w); W = w.sum(); Mw = 0.5 * w @ A @ w
        wd = {i: w[i] for i in range(m)}
        T = float(tri_mass(H, wd))
        if Mw > 0: worst_beta = max(worst_beta, T / Mw)
        costs = []
        for v in range(m):
            Av = [v] + list(np.nonzero(A[v])[0])
            costs.append(w[Av].sum() + 0.5 * w[Av] @ A[np.ix_(Av, Av)] @ w[Av])
        avg = sum(w[v] / W * costs[v] for v in range(m))
        beta = T / Mw if Mw > 0 else 0.0
        if avg > 1 + (4 + 3 * beta) * Mw / W + 1e-9: ok = False
        v = int(np.argmin(costs))
        Av = set([v] + list(np.nonzero(A[v])[0]))
        Hn = H.subgraph([u for u in H if u not in Av]).copy()
        if Hn.number_of_nodes():
            _, _, Fn, _, _, _ = global_max(nx.convert_node_labels_to_integers(Hn), nrand=20, seed=99)
        else:
            Fn = 0.0
        if Fn < Fs - costs[v] - 1e-9: ok = False
        H = Hn; chosen += 1
    Deff = 3 + 1.5 * worst_beta
    alpha = len(max(nx.find_cliques(nx.complement(G)), key=len))
    greedy_rows.append((G.number_of_nodes(), Delta, chosen, alpha, F0, F0 / (Deff * math.log(Delta)), ok))
print(f'maximizers checked: {nchk}; (6.4) W>=n/Delta violations: {viol64}; (6.5) 2M/W<=log Delta violations: {viol65}; max |(6.2) error| at maximizers: {maxerr62:.2e}')
print('greedy runs: all step-inequalities OK:', all(r[-1] for r in greedy_rows),
      '; greedy size >= F*/(D_eff log Delta) in all:', all(r[2] >= r[5] - 1e-9 for r in greedy_rows),
      '; min greedy/(F*/(D_eff log Delta)) =', min(r[2] / r[5] for r in greedy_rows))
print('sample rows (n, Delta, greedy |I|, alpha, F*, F*/(D_eff logDelta), ok):')
for r in greedy_rows[:6]: print(r)
