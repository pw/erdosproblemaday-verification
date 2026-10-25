# Lemma 6.1 (strict-cross sampling): finite checks of each ingredient + a failing control.
import itertools, math, random, sys
random.seed(167)

def in_cross(x, y):
    (u, v), (a, b) = x, y
    return (u == a) != (v == b)          # exactly one coordinate agrees

# (1) trace count: crosses induce <= (2k+1)^2 distinct index subsets of 2k pooled samples
def n_patterns(samples, family):
    pats = set()
    for S in family(samples):
        pats.add(tuple(S(x) for x in samples))
    return len(pats)

def cross_family(samples):
    A = sorted({u for u, _ in samples}) + ['*']    # '*' = a label not among the samples
    B = sorted({v for _, v in samples}) + ['*']
    for a in A:
        for b in B:
            yield (lambda x, y=(a, b): in_cross(x, y))

def three_rows_family(samples):                   # CONTROL family: unions of <= 3 full rows
    A = sorted({u for u, _ in samples})
    for r in range(0, 4):
        for T in itertools.combinations(A, r):
            yield (lambda x, T=set(T): x[0] in T)

worst = 0; ctrl_fail = False
for trial in range(300):
    k = random.randint(1, 14)
    m = random.choice([1, 2, 3, 5, 2 * k, 4 * k])        # label alphabet size
    samples = [(random.randrange(m), random.randrange(m)) for _ in range(2 * k)]
    c = n_patterns(samples, cross_family)
    assert c <= (2 * k + 1) ** 2, (k, c)
    worst = max(worst, c / (2 * k + 1) ** 2)
# extreme: all 2k first labels distinct and all 2k second labels distinct
for k in range(1, 15):
    s = [(i, i + 1000) for i in range(2 * k)]
    c = n_patterns(s, cross_family)
    assert c <= (2 * k + 1) ** 2
    cc = n_patterns(s, three_rows_family)
    if cc > (2 * k + 1) ** 2:
        ctrl_fail = True
    if k in (2, 8, 14):
        print(f"k={k}: distinct cross traces={c} (bound {(2*k+1)**2}); CONTROL <=3-row unions traces={cc}")
print("max ratio traces/(2k+1)^2 over random trials:", round(worst, 3))
print("CONTROL family exceeds (2k+1)^2 for some k:", ctrl_fail)

# (2) hypergeometric: P(all m misses in 2nd half) = C(2k-m,k)/C(2k,k) <= 2^-m
bad = 0
for k in range(1, 81):
    for m in range(0, 2 * k + 1):
        p = math.comb(2 * k - m, k) / math.comb(2 * k, k) if m <= k else 0.0
        prod = 1.0
        for i in range(m):
            prod *= (k - i) / (2 * k - i) if m <= k else 0
        if m <= k:
            assert abs(p - prod) < 1e-12 * max(1, p)
        assert p <= 2.0 ** (-m) + 1e-15, (k, m, p)
        if m >= 1 and m <= k and p > 2.0 ** (-m - 1):
            bad += 1                     # CONTROL: the sharper claim 2^{-m-1} fails
print("hypergeometric <= 2^-m: all k<=80 OK; CONTROL '<= 2^-(m+1)' violated in", bad, "cases")

# (3) Chebyshev step: for k*alpha >= 8 and beta > alpha, P(Bin(k,beta) < k alpha/2) <= 1/2
def binom_cdf_below(k, beta, thr):   # P(N < thr)
    return sum(math.comb(k, j) * beta ** j * (1 - beta) ** (k - j) for j in range(k + 1) if j < thr)
worst_ch = 0
for k in range(8, 161):
    for i in range(1, 41):
        alpha = max(8 / k, i / 41)
        if alpha >= 1: continue
        beta = min(alpha + 1e-9, 1 - 1e-12)
        worst_ch = max(worst_ch, binom_cdf_below(k, beta, k * alpha / 2))
print("max P(Bin(k,beta)<k alpha/2) over k alpha>=8 grid:", f"{worst_ch:.3e}", "(claim <= 1/2)")
ctrl = binom_cdf_below(1, 0.31, 1 * 0.3 / 2)
print("CONTROL k alpha=0.3 (hypothesis violated): P =", ctrl, "> 1/2:", ctrl > 0.5)

# (4) Monte Carlo of the first assertion; independence is load-bearing.
# nu uniform on an n x n grid; every cross has nu-mass 2(n-1)/n^2 < 1-alpha.
n, k, alpha = 10, 200, 0.4
bound = 2 * (2 * k + 1) ** 2 * 2.0 ** (-k * alpha / 2)
states = [(i, j) for i in range(n) for j in range(n)]
ys = [(a, b) for a in range(n) for b in range(n)]   # labels outside the grid give rows/cols: also small
def event(X):
    for y in ys:
        if all(in_cross(x, y) for x in X):
            return True
    # y with an unseen label: cross = a full column (or row); X all in one column?
    if len({x[1] for x in X}) == 1 or len({x[0] for x in X}) == 1:
        return True
    return False
T = 2000
iid_hits = sum(event([random.choice(states) for _ in range(k)]) for _ in range(T))
dep_hits = 0
for _ in range(T):
    x = random.choice(states); dep_hits += event([x] * k)       # CONTROL: X_1=...=X_k
print(f"MC n={n},k={k},alpha={alpha}: bound={bound:.3e}; iid frequency={iid_hits}/{T}; "
      f"CONTROL dependent samples frequency={dep_hits}/{T}")

# (5) second assertion (6.3), exact toy: two histories h1,h2 with nu_h1=delta_x1, nu_h2=delta_x2,
# x1=(0,0), x2=(1,1); q's neighbours have each history with prob 1/2.  nu~_q=(delta_x1+delta_x2)/2.
def fail_prob(k, template_law):
    tot = 0.0
    alpha = k ** -0.25
    for (c1, prob) in template_law(k):           # c1 = number of h1's in template
        present = set()
        if c1 > 0: present.add('h1')
        if c1 < k: present.add('h2')
        nu = {'h1': (0, 0), 'h2': (1, 1)}
        labs = [0, 1, '*']
        bad = False
        for y in itertools.product(labs, labs):
            if all(in_cross(nu[h], y) for h in present):          # y in Y_theta (exact atoms)
                mass = 0.5 * in_cross((0, 0), y) + 0.5 * in_cross((1, 1), y)
                if mass < 1 - alpha: bad = True
        tot += prob * bad
    return tot
iid = lambda k: [(c, math.comb(k, c) * 0.5 ** k) for c in range(k + 1)]
det = lambda k: [(k, 1.0)]                       # CONTROL: template = k copies of one history
for k in (300, 1000):
    b = 4 * (2 * k + 1) ** 2 * 2.0 ** (-(k ** 0.75) / 2)
    print(f"(6.3) toy k={k}: bound={b:.3e}; iid templates P={fail_prob(k, iid):.3e} (=2^(1-k));"
          f" CONTROL deterministic template P={fail_prob(k, det)}")
