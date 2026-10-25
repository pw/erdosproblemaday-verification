# Lemma 7.1 (greedy prefix skipping m), Lemma 8.3 (divisor density), Lemma 8.4 (grouping), exactly as written.
import math, random, sys
from fractions import Fraction
from sympy import factorint

def prefix(m, T=None):
    R, q = m-1, m
    ns, qs, exc = [], [m], 0
    while R > 0 and (T is None or q < T):
        a = -(-q // R)
        n = a if a != m else m+1
        if a == m: exc += 1
        R, q = n*R - q, n*q
        ns.append(n); qs.append(q)
        if T is None and q.bit_length() > 200000: return ns, R, q, qs, exc, 'CAP'
    return ns, R, q, qs, exc, 'ok'

fails = 0
def bad(msg):
    global fails; fails += 1; print("FAIL", msg)

exc_total = 0; maxj_slack = 1e9; maxR_ratio = 0
for m in range(4, 3001):
    for T in (2*m*m, 2*m*m+1, 7*m**3, m**6, 2*m*(10**30)):
        ns, R, q, qs, exc, st = prefix(m, T)
        exc_total += exc
        j = len(ns)
        if not all(ns[i] < ns[i+1] for i in range(j-1)): bad(("not increasing", m, T))
        if m in ns: bad(("contains m", m))
        if ns and ns[0] < 2: bad("n1<2")
        if not (0 <= R < 2*m): bad(("R range", m, T, R))
        maxR_ratio = max(maxR_ratio, R/m)
        if not (j < 3 + math.log2(math.log2(T))): bad(("j bound", m, T, j))
        maxj_slack = min(maxj_slack, 3 + math.log2(math.log2(T)) - j)
        if q != m*math.prod(ns): bad("q product")
        for i in range(j):
            if ns[i] > qs[i] + 1: bad(("n_i <= q_{i-1}+1", m, T, i))
        if Fraction(1, m) + sum(Fraction(1, n) for n in ns) + Fraction(R, q) != 1: bad(("decomp", m, T))
        if not q < T*T: bad(("q<T^2", m, T))
        if R > 0:
            if q < T: bad(("q>=T", m, T))
            x = Fraction(R, q)
            if not (x < Fraction(2*m, T) <= Fraction(1, m)): bad(("R/q<2m/T<=1/m", m, T))
            if not all(x < Fraction(1, n) for n in ns): bad(("R/q<1/n_i", m, T))
print("Lemma 7.1: m=4..3000 x 5 cutoffs; exceptional steps seen:", exc_total, "min slack in j bound:", round(maxj_slack, 3), "max R/m:", round(maxR_ratio, 3))

# no-cutoff variant (Section 7, finite exceptional m): terminate at R=0
for m in range(4, 41):
    ns, R, q, qs, exc, st = prefix(m, None)
    if st == 'CAP':
        print(f"  no-cutoff m={m}: hit bit cap after {len(ns)} steps (not a failure, just large)"); continue
    ok = R == 0 and Fraction(1, m) + sum(Fraction(1, n) for n in ns) == 1 and len(set(ns)) == len(ns) and m not in ns
    if not ok: bad(("no-cutoff", m))
print("no-cutoff variant m=4..40 checked")

# Lemma 8.3: divisor density <=> consecutive divisor ratios <= m (for all real w in [1,q])
def divisors_of_product(m, ns):
    f = {}
    for x in [m] + ns:
        for p, e in factorint(x).items(): f[p] = f.get(p, 0) + e
    ds = [1]
    for p, e in f.items(): ds = [d*p**i for d in ds for i in range(e+1)]
    return sorted(ds)

worst = 0
for m in range(4, 400):
    for T in (2*m*m, m**5):
        ns, R, q, qs, exc, st = prefix(m, T)
        ds = divisors_of_product(m, ns)
        assert ds[-1] == q
        ratio = max(ds[i+1]/ds[i] for i in range(len(ds)-1))
        worst = max(worst, ratio/m)
        if ratio > m: bad(("Lemma 8.3 ratio", m, T, ratio))
print("Lemma 8.3 on greedy q (m<400): max(consecutive divisor ratio / m) =", round(worst, 4))

# Lemma 8.3 on adversarial random sequences n <= q+1 (including n = q+1, which maximizes the gap)
random.seed(1)
worst = 0
for trial in range(3000):
    m = random.randint(2, 60); q = m; ns = []
    for step in range(random.randint(1, 4)):
        n = random.choice([q+1, q+1, random.randint(1, q+1)])
        ns.append(n); q *= n
        if q > 10**14: break
    ds = divisors_of_product(m, ns)
    ratio = max(ds[i+1]/ds[i] for i in range(len(ds)-1)) if len(ds) > 1 else 1
    worst = max(worst, ratio/m)
    if ratio > m: bad(("Lemma 8.3 random", m, ns, ratio))
print("Lemma 8.3 random n<=q+1 sequences: max ratio/m =", round(worst, 4))

# Lemma 8.4 grouping with greedy q: count groups for X in [1,q], verify step invariants and G bound
def group(X, m, ds):
    import bisect
    groups = []; Xi = X
    while Xi > 0:
        if Xi > m**4:
            w = Fraction(Xi, m*m)
            # largest divisor <= w; must be >= w/m
            idx = bisect.bisect_right(ds, w) - 1
            d = ds[idx]
            if not (Fraction(Xi, m**3) <= d <= Fraction(Xi, m*m)): return None
            s = Xi // d
            if not (m*m <= s <= m**3): return None
            Xn = Xi - d*s
            if not (0 <= Xn < d <= Fraction(Xi, m*m)): return None
            groups.append((d, s)); Xi = Xn
        else:
            groups.append((1, Xi)); Xi = 0
    return groups
worstG = -1e9
for m in range(4, 60):
    ns, R, q, qs, exc, st = prefix(m, m**12)
    ds = divisors_of_product(m, ns)
    for X in [1, 2, m**4, m**4+1, q] + [random.randint(1, q) for _ in range(200)]:
        g = group(X, m, ds)
        if g is None: bad(("grouping invariant", m, X)); continue
        assert sum(d*s for d, s in g) == X
        assert all(q % d == 0 and 1 <= s <= m**4 for d, s in g)
        bound = math.log(X)/(2*math.log(m)) + 2
        worstG = max(worstG, len(g) - bound)
        if len(g) > bound: bad(("G bound", m, X, len(g), bound))
print("Lemma 8.4: max(G - bound) =", round(worstG, 3), "(must be <= 0)")
print("TOTAL FAILS", fails)
