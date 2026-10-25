#!/usr/bin/env python3
"""Exact / high-precision checks of the paper's constants, asymptotics, averaging step and Lemma 2."""
import itertools, random, math
from fractions import Fraction as F
from math import comb
import mpmath as mp
mp.mp.dps = 60

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out.append(s)

# (1) theta
t5 = F(4,3)**3 * F(5,6)**5
say("theta^5 =", t5, " == 6250/6561:", t5 == F(6250, 6561), " <1:", t5 < 1)
theta = mp.power(mp.mpf(4)/3, mp.mpf(3)/5) * mp.mpf(5)/6
eta = -mp.log(theta)
say("theta =", mp.nstr(theta, 20), " log theta =", mp.nstr(mp.log(theta), 20), " eta =", mp.nstr(eta, 20))
say("C must exceed 2/eta =", mp.nstr(2/eta, 20))
# Chingiz table factors
say("Chingiz factor on P_U (3/4)*(6/5) =", F(3,4)*F(6,5), " Bella factor (6/5); Bella add = P/5 =", F(6,5)-1, " = 2 * (1/10)")
say("(4/3)^{3H/5}(5/6)^H == theta^H identity: per-unit exponent check (4/3)^{3/5}(5/6) = theta  [definition]")

# (2) leading constants
c1 = 1/mp.log(mp.mpf(5)/3); c2 = 2/mp.log(3)
say("1/log(5/3) =", mp.nstr(c1, 15), " 2/log3 =", mp.nstr(c2, 15), " gap =", mp.nstr(c1-c2, 15), " 27>25 equivalence: log3 > 2log(5/3) <=>", 3 > F(25,9))

# (3) h - a log3 n >= a/2 for a = ceil(2 log3 n) + 2: exact check on n range
bad = 0
for n in range(2, 200001):
    L3 = mp.log(n)/mp.log(3)
    a = int(mp.ceil(2*L3)) + 2
    h = a*(a-1)//2
    if h - a*L3 < mp.mpf(a)/2 - mp.mpf('1e-40'): bad += 1
    if 3*comb(n, a) if a <= n else 0:
        pass
say("h - a log3 n >= a/2 for n in [2,200000]: failures =", bad)

# (4) When do the paper's own displayed bounds give Phi_init < 1 AND R(n) > a-1 ?
def conditions(L, C):
    # L = log n (natural), n huge -> work in logs; use paper's displayed upper bounds
    L3 = L/mp.log(3)
    a = mp.ceil(2*L3) + 2
    Qb = mp.power(3, 1 - a/2)                       # paper: sum Q <= 3^{1-a/2}
    l = mp.ceil(C*L)
    logbase = L - eta*(l-1)/2                       # log(n theta^{(l-1)/2})
    Pb = mp.mpf(6)/5 * mp.e**(l*logbase)            # paper: (6/5)(n theta^{(l-1)/2})^l
    R = 1 + mp.floor(mp.log((mp.e**L + mp.mpf(3)/2)/(l + mp.mpf(3)/2))/mp.log(mp.mpf(5)/3))
    return (Qb + Pb < 1), (R > a - 1), a, l, R, Qb + Pb
best = None
for C in [206, 210, 220, 230, 250, 300, 400]:
    lo = None
    for Lint in range(1, 2000):
        ok1, ok2, a, l, R, phib = conditions(mp.mpf(Lint), C)
        if ok1 and ok2:
            lo = Lint; break
    if lo is not None:
        ok1, ok2, a, l, R, phib = conditions(mp.mpf(lo), C)
        say(f"C={C} (C*eta={mp.nstr(C*eta,6)}): first integer log n with both Phi_init<1 (paper's bounds) and R(n)>=a : log n = {lo}  (a={int(a)}, l={int(l)}, R={int(R)}, Phi bound={mp.nstr(phib,4)})")
        if best is None or lo < best[0]: best = (lo, C)
say("=> 'sufficiently large' in the paper's argument means roughly n >= e^%d (best C tried = %d)" % best)

# (5) averaging identity
bad = 0
for s in range(2, 60):
    for l in range(2, s+1):
        if comb(s, l)*comb(l, 2) != comb(s, 2)*comb(s-2, l-2): bad += 1
say("identity C(s,l)C(l,2) = C(s,2)C(s-2,l-2) for 2<=l<=s<60: failures =", bad)

# (6) Lemma 2 recursion worst case: m_{i+1} = ceil(3/5 (m_i - 1)); R(m) exact via integers
def R_exact(m, l):
    k = 0
    while 5**(k+1) * (2*l + 3) <= 3**(k+1) * (2*m + 3): k += 1
    return 1 + k
bad_rec = 0; checked = 0; float_mism = 0; exact_boundary = 0
for l in range(2, 80):
    for m in range(l, 4000):
        R = R_exact(m, l)
        if 5**(R-1) * (2*l + 3) == 3**(R-1) * (2*m + 3): exact_boundary += 1
        mi = m
        for i in range(R):
            checked += 1
            if mi < l: bad_rec += 1; break
            mi = math.ceil(F(3, 5) * (mi - 1))
        Rf = 1 + int(mp.floor(mp.log((m + mp.mpf(3)/2)/(l + mp.mpf(3)/2))/mp.log(mp.mpf(5)/3)))
        if Rf != R: float_mism += 1
say("Lemma 2 worst-case recursion (m_{i+1}=ceil(3/5(m_i-1))), 2<=l<80, l<=m<4000: steps checked =", checked, " m_i<l before step R: failures =", bad_rec)
say("  (exact-boundary cases where (m+3/2)/(l+3/2) is exactly a power of 5/3:", exact_boundary, "; a float log/floor evaluation of R disagrees with the exact integer R in", float_mism, "of them -- instrument artifact, exact R used)")
say("algebra: (3/5)(m-1)+3/2 == (3/5)(m+3/2):", F(3,5)*(F(7)-1)+F(3,2) == F(3,5)*(F(7)+F(3,2)))

# (7) Lemma 2 + averaging on actual graphs. Build graphs as complements of sparse random graphs,
#     keep those with every l-set >= 3/5 dense, brute-force the averaging claim for s in [l, l+3] and s=n,
#     then run the greedy with an ADVERSARIAL choice (vertex of at-least-average degree with the SMALLEST
#     such degree) and check: chosen degree >= 3/5(m_i-1), result is a clique, size >= R(n) (R(n)>=3 here).
rng = random.Random(778)
def graph_trials(n, l, q, trials):
    got = 0; bad_avg = 0; bad_clique = 0; sizes = []
    for _ in range(trials):
        adj = {v: set(range(n)) - {v} for v in range(n)}
        for i in range(n):
            for j in range(i+1, n):
                if rng.random() < q: adj[i].discard(j); adj[j].discard(i)
        def eC(S): return sum(1 for i, j in itertools.combinations(S, 2) if j in adj[i])
        if any(5*eC(U) < 3*comb(l, 2) for U in itertools.combinations(range(n), l)): continue
        got += 1
        for s in list(range(l, min(n, l+3)+1)) + [n]:
            for S in itertools.combinations(range(n), s):
                if 5*eC(S) < 3*comb(s, 2): bad_avg += 1
        V = set(range(n)); clique = []
        R = R_exact(n, l)
        for i in range(R):
            if len(V) < l: bad_clique += 1; break
            degs = {v: len(adj[v] & V) for v in V}
            avg = F(sum(degs.values()), len(V))
            cands = [v for v in V if degs[v] >= avg]
            v = min(cands, key=lambda u: degs[u])
            if degs[v] < F(3, 5) * (len(V) - 1): bad_clique += 1
            clique.append(v); V = adj[v] & V
        for x, y in itertools.combinations(clique, 2):
            if y not in adj[x]: bad_clique += 1
        if len(clique) < R: bad_clique += 1
        sizes.append(len(clique))
    return got, bad_avg, bad_clique, R_exact(n, l)
for (n, l, q, T) in [(14, 3, 0.06, 200), (14, 4, 0.12, 200), (16, 4, 0.12, 60), (17, 5, 0.15, 20)]:
    got, ba, bc, R = graph_trials(n, l, q, T)
    say(f"graphs n={n} l={l}: {got} graphs with all l-sets >=3/5 dense; averaging failures={ba}; greedy/clique failures={bc} (R(n)={R})")

open('/tmp/erdos778/seats/A_hostile/out_analytic.txt', 'w').write("\n".join(out) + "\n")
