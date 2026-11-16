"""es3_6.py -- extraspecial 3^{1+6} (= F_27 trace model, z = 729, a = 28 by the spread):
the paper needs omega >= 11 here (T(10) = 17 < 28).  Find a large clique among the 364 projective
points, re-verify it by evaluating the form directly on explicit vectors, then run the exact C MCQ
for cliques of size >= best+1 with a time limit (report proven/unproven honestly)."""
import sys, itertools, numpy as np
import probe
from graphlib import c_heurclique, c_clique, check_clique, colour_sat, c_dsatur, c_tabu
p, d = 3, 6
Ms, info = probe.trace_forms(3, 3, 1, __import__('random').Random(5))
M = Ms[0]
print('trace form Gram matrix (F_27 trace model, c=%s):' % info['c'], M.tolist())
z, k, adj, reps = probe.build_graph(p, d, Ms)
X = probe.all_vectors(p, d)
print('z=%d twin classes=%d' % (z, k))
best = []
for seed in range(1, 9):
    C = c_heurclique(k, adj, 400, seed)
    if len(C) > len(best):
        best = C
vecs = [X[reps[c]] for c in best]
direct_ok = all(int(u @ M @ v) % 3 != 0 for u, v in itertools.combinations(vecs, 2))
print('best heuristic clique size %d; direct form check (pairwise beta != 0): %s' % (len(best), direct_ok))
print('clique vectors:', [list(map(int, v)) for v in vecs])
# spread colouring (28 colours) and lower bound alpha
col = probe.spread_colouring(p, d, M, reps)
from graphlib import check_colouring
print('F_27-line spread colouring: %d colours, proper=%s' % (max(col) + 1, check_colouring(k, adj, col)))
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 600
Cx, pr = c_clique(k, adj, tl, len(best) + 1)
print('exact C MCQ search for cliques of size >= %d (time limit %.0fs): %s, proven=%s' % (len(best) + 1, tl, 'none' if Cx is None else '%d-clique found %s' % (len(Cx), Cx), pr))
