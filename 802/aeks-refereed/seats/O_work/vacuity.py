# Show the small-n brute force cannot distinguish a global maximizer from ANY stationary point:
# at a stationary point, e_w(S,D) <= w(S) * min(w(D), log(|S|/w(S)))  (stationarity + Jensen),
# so ratio <= max(1, min(e^x, log n)/x), which is < 256 unless log n > ~1880.
import sys, math, random
import numpy as np, networkx as nx
sys.path.insert(0, '/tmp/oaimath/184/seats/O_work/scripts')
from maxim import coord_ascent, newton, residual, is_local_max, F
from crossmass import worst_ratio
rng = random.Random(5)
xs = [1.0, 2.0, 3.0]
rows = []
for sizes in [(5, 5), (3, 8), (2, 9), (4, 4, 4), (2, 3, 6), (1, 5, 6)]:
    G = nx.convert_node_labels_to_integers(nx.complete_multipartite_graph(*sizes))
    n = G.number_of_nodes(); A = nx.to_numpy_array(G, nodelist=range(n))
    pts = []
    starts = [np.full(n, 0.3)] + [np.random.default_rng(i).uniform(0, 1, n) for i in range(40)]
    # symmetric (part-constant) start, solved by Newton directly -> typically a saddle
    for s in starts:
        for solver in ['ca', 'newton']:
            try:
                w = coord_ascent(A, s) if solver == 'ca' else newton(A, s, iters=200)
                w = newton(A, w)
            except Exception:
                continue
            if np.all(np.isfinite(w)) and np.all(w > 0) and residual(A, w) < 1e-10:
                if not any(np.max(np.abs(w - p)) < 1e-8 for p in pts):
                    pts.append(w)
    vals = [F(A, p) for p in pts]
    best = int(np.argmax(vals))
    for i, p in enumerate(pts):
        out, _ = worst_ratio(A, p, xs, disjoint_too=False)
        rows.append((sizes, i == best, is_local_max(A, p), round(vals[i], 4), [round(out[x][0], 3) for x in xs],
                     [round(max(1, min(math.exp(x), math.log(n)) / x), 3) for x in xs]))
for r in rows:
    print(r)
viol = [r for r in rows if any(a > b + 1e-9 for a, b in zip(r[4], r[5]))]
print('stationary points:', len(rows), ' exceeding the trivial stationarity bound:', len(viol))
