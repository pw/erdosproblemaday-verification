"""esp.py p r TLIM -- extraspecial p^{1+2r} via the F_{p^r} trace model: z = p^{2r}, a = p^r + 1
(spread colouring verified + counting bound k/alpha); omega: heuristic clique re-verified on explicit
vectors, then exact C MCQ for size >= best+1 with time limit.  Reports whether a <= T(omega_lb) and
z <= (T(omega_lb)-1)^2 are certified."""
import sys, itertools, random
import probe
from graphlib import c_heurclique, c_clique, check_colouring, T
p, r, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
d = 2 * r
Ms, info = probe.trace_forms(p, r, 1, random.Random(5))
M = Ms[0]
z, k, adj, reps = probe.build_graph(p, d, Ms)
X = probe.all_vectors(p, d)
best = []
for seed in range(1, 6):
    C = c_heurclique(k, adj, 200, seed)
    if len(C) > len(best):
        best = C
vecs = [X[reps[c]] for c in best]
direct_ok = all(int(u @ M @ v) % p != 0 for u, v in itertools.combinations(vecs, 2))
col = probe.spread_colouring(p, d, M, reps)
ncol = max(col) + 1
full = (1 << k) - 1
cadj = [(~adj[v]) & full & ~(1 << v) for v in range(k)]
I, pra = c_clique(k, cadj, tl, 0)
print('p=%d r=%d: z=%d projective points=%d; spread colouring %d colours proper=%s; alpha=%d (proven=%s) => a >= %d'
      % (p, r, z, k, ncol, check_colouring(k, adj, col), len(I), pra, -(-k // len(I))))
w = len(best)
print('  clique found: %d (direct form check %s) vectors=%s' % (w, direct_ok, [list(map(int, v)) for v in vecs]))
print('  T(%d)=%d vs a=%d -> cert_a=%s ; (T-1)^2=%d vs z=%d -> cert_z=%s' % (w, T(w), ncol, ncol <= T(w), (T(w) - 1) ** 2, z, z <= (T(w) - 1) ** 2))
Cx, pr = c_clique(k, adj, tl, w + 1)
print('  exact C MCQ for cliques >= %d (limit %.0fs): %s, proven=%s' % (w + 1, tl, 'none' if Cx is None else 'found size %d' % len(Cx), pr))
