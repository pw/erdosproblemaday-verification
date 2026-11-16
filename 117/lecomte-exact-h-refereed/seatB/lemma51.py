# Lemma 5.1 test bed on binary class-2 groups (beta: F2^nu x F2^nu -> F2^e, zero common radical).
# Hypotheses: all scalar radicals abelian, all scalar ranks >= 4, a noncentral radical R of rank d,
# N = omega <= 2d+4.  Claimed conclusions: d in {4,6}, N >= 9, every fibre of P/R has width <= 2.
# Also re-checks a(P) <= T(N) and strictness for N >= 9.
import random, sys, collections
from class2 import rank2, form_val, comm_structure, solve_graph
from solve import T
rng = random.Random(int(sys.argv[1])); trials = int(sys.argv[2]); nus = [int(x) for x in sys.argv[3].split(',')]

def alt_of_rank(nu, r, rng):
    # random alternating form of rank r: pull back a symplectic form on F2^r along a random surjection
    while True:
        M = [rng.getrandbits(nu) for _ in range(r)]  # rows: r linear functionals on F2^nu
        if rank2(M, nu) == r: break
    B = [0] * nu
    for i in range(nu):
        for j in range(nu):
            v = 0
            for k in range(0, r, 2):
                a1 = M[k] >> i & 1; a2 = M[k + 1] >> i & 1
                b1 = M[k] >> j & 1; b2 = M[k + 1] >> j & 1
                v ^= (a1 & b2) ^ (a2 & b1)
            if v: B[i] |= 1 << j
    return B

stats = collections.Counter()
for t in range(trials):
    nu = rng.choice(nus); e = rng.choice([2, 2, 3])
    Bs = [alt_of_rank(nu, rng.choice([4, 4, 6]) if nu >= 6 else 4, rng) for _ in range(e)]
    beta = comm_structure(Bs, nu)
    V = list(range(1, 1 << nu))
    if any(all(beta(v, 1 << j) == 0 for j in range(nu)) for v in V): continue
    forms = []
    okhyp = True
    for mask in range(1, 1 << e):
        C = [0] * nu
        for k in range(e):
            if mask >> k & 1: C = [C[i] ^ Bs[k][i] for i in range(nu)]
        rk = rank2(C, nu)
        if rk == 0: okhyp = False; break   # dependent forms
        rad = [v for v in range(1 << nu) if all(form_val(C, v, 1 << j, nu) == 0 for j in range(nu))]
        ab = all(beta(u, w) == 0 for u in rad for w in rad)
        forms.append((rk, rad, ab))
    if not okhyp: continue
    if not all(ab for rk, rad, ab in forms) or not all(rk >= 4 for rk, rad, ab in forms): continue
    nonc = [(rk, rad) for rk, rad, ab in forms if len(rad) > 1]
    if not nonc: continue
    om, ex, a, nmax = solve_graph(V, lambda v, w: beta(v, w) == 0, tl=120)
    if not ex: stats['omega inexact'] += 1
    if a > T(om) or (om >= 9 and a >= T(om)):
        print('*** profile failure', nu, e, om, a, Bs, flush=True)
    for rk, rad in nonc:
        d = rk
        if om <= 2 * d + 4:
            # widths: fibre over g has width |beta(g, rad)| (R abelian)
            radset = set(rad)
            wmax = max(len({beta(g, r) for r in rad}) for g in V)
            okc = (d in (4, 6)) and om >= 9 and wmax <= 2
            stats[('L5.1 applies', nu, d, om, a, wmax, okc)] += 1
            if not okc: print('*** Lemma 5.1 conclusion fails', nu, e, d, om, wmax, Bs, flush=True)
        else:
            stats[('avg range', nu, d)] += 1
for k, v in sorted(stats.items(), key=str): print(k, v)
