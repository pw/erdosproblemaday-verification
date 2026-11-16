# Lemma 5.2 test bed: class-2 binary groups with P/Z(P) = F2^5, every nonzero scalar form of rank 4
# (so every scalar radical is abelian, noncentral, of rank d=4, widths <= 2).  Lemma 5.1 => N >= 9;
# Lemma 5.2 claims: if N <= 10 then a(P) = N = 9.  We sample random pencils (dim W = 2,3,4) and record (N, a).
import random, sys, collections
from class2 import rank2, form_val, random_alt, comm_structure, solve_graph
rng = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
nu = 5; seen = collections.Counter(); examples = {}
for t in range(trials):
    e = rng.choice([2, 2, 3, 3, 4])
    Bs = [random_alt(nu, rng) for _ in range(e)]
    ok = True
    for mask in range(1, 1 << e):
        C = [0] * nu
        for k in range(e):
            if mask >> k & 1: C = [C[i] ^ Bs[k][i] for i in range(nu)]
        if rank2(C, nu) != 4: ok = False; break
    if not ok: continue
    beta = comm_structure(Bs, nu)
    V = list(range(1, 1 << nu))
    if any(all(beta(v, 1 << j) == 0 for j in range(nu)) for v in V): continue
    om, ex, a, nmax = solve_graph(V, lambda v, w: beta(v, w) == 0, tl=120)
    key = (e, om if ex else -om, a)
    seen[key] += 1
    if key not in examples: examples[key] = Bs
    if ex and om <= 10 and not (om == 9 and a == 9):
        print('*** COUNTEREXAMPLE to Lemma 5.2', e, om, a, Bs, flush=True)
    if ex and om < 9:
        print('*** COUNTEREXAMPLE to Lemma 5.1 (N>=9)', e, om, a, Bs, flush=True)
for k, v in sorted(seen.items()): print('dimW=%d omega=%d a=%d count=%d' % (k[0], k[1], k[2], v))
