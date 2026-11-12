# Independent brute-force checker for Theorem "long" (a_n >= 8 n^3 => some <= 2n elements of
# {x+1..x+a_n} have product divisible by prod A). Exact DP over capped valuation vectors.
import random, sys, itertools, time
from math import prod

def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def vp(b, p):
    v = 0
    while b % p == 0: b //= p; v += 1
    return v

def min_cover(A, x):
    """exact min |B|, B subset of {x+1..x+max A}, prod A | prod B. Returns (min, witness)."""
    m = max(A)
    need = {}
    for a in A:
        for p, e in factor(a).items(): need[p] = need.get(p, 0) + e
    ps = sorted(need); E = tuple(need[p] for p in ps)
    # capped vectors of interval elements; keep element ids for a witness
    groups = {}
    for b in range(x + 1, x + m + 1):
        v = tuple(min(vp(b, p), e) for p, e in zip(ps, E))
        if any(v): groups.setdefault(v, []).append(b)
    items = []
    for v, bs in groups.items():
        sat = max(e for e, vi in zip(E, v) if vi > 0)   # copies beyond this are useless
        items.extend((v, b) for b in bs[:sat])
    zero = tuple(0 for _ in ps)
    dp = {zero: (0, ())}
    for v, b in items:
        new = dict(dp)
        for s, (c, w) in dp.items():
            t = tuple(min(si + vi, e) for si, vi, e in zip(s, v, E))
            if t not in new or new[t][0] > c + 1:
                new[t] = (c + 1, w + (b,))
        dp = new
    best = dp.get(E)
    assert best is not None   # whole interval always works (P | m! * binom)
    c, w = best
    assert len(set(w)) == c and all(x + 1 <= b <= x + m for b in w)
    assert prod(w) % prod(A) == 0          # independent check of the witness
    return c, w

def brute_min(A, x):
    m = max(A); P = prod(A); I = range(x + 1, x + m + 1)
    for k in range(0, m + 1):
        for S in itertools.combinations(I, k):
            if prod(S) % P == 0: return k
    return None

log = open('/tmp/e708/refA/longcheck.log', 'w')
def out(*a):
    s = ' '.join(str(t) for t in a); print(s, flush=True); log.write(s + '\n'); log.flush()

# --- controls
c1 = min_cover([10, 12, 15, 20], 50)[0]; c2 = min_cover([5, 10, 12, 15, 20], 50)[0]
out("control Prop small: A={10,12,15,20},x=50 ->", c1, "(paper: 5);  A={5,10,12,15,20},x=50 ->", c2, "(paper: 6)")
out("control prop gap: A={13,17}, x=2274114691 ->", min_cover([13, 17], 2274114691)[0], "(paper: 2)")
# DP vs subset brute force on tiny instances
rng = random.Random(708)
bad = 0
for t in range(400):
    n = rng.randint(1, 4); M = rng.randint(4, 16)
    A = sorted(rng.sample(range(2, M + 1), min(n, M - 1)))
    if M not in A: A[-1] = M; A = sorted(set(A))
    x = rng.randint(0, 200)
    d = min_cover(A, x)[0]; bf = brute_min(A, x)
    if d != bf: bad += 1; out("DP/BRUTE MISMATCH", A, x, d, bf)
out("DP vs subset brute force on 400 tiny instances: mismatches =", bad)
# mutation: does the instrument go red on a FALSE claim (min <= n) ?
red = 0
for t in range(300):
    n = rng.randint(2, 5); M = rng.randint(10, 40)
    A = sorted(set(rng.sample(range(2, M), n - 1) + [M]))
    x = rng.randint(0, 100)
    if min_cover(A, x)[0] > len(A): red += 1
out("mutated claim 'min<=n' on 300 short-interval instances: violations found =", red, "(must be >0)")

# --- the theorem
def smooth_near(lo, hi):
    # pick a highly composite-ish number in [lo,hi]
    cands = [k for k in range(lo, hi + 1) if max(factor(k)) <= 13]
    return rng.choice(cands)

stats = {}
t0 = time.time()
worst = {}
for n, lo, hi, trials in ((2, 64, 2000, 2500), (3, 216, 3000, 1500)):
    viol = 0; hist = {}
    for t in range(trials):
        mode = t % 3
        an = rng.randint(lo, hi) if mode == 0 else smooth_near(lo, hi)
        pool = list(range(2, an))
        if mode == 2:
            pool = [k for k in pool if max(factor(k)) <= 13] or pool
        rest = rng.sample(pool, n - 1)
        A = sorted(set(rest + [an]))
        if len(A) != n: continue
        xm = rng.randrange(4)
        if xm == 0: x = 0
        elif xm == 1: x = rng.randint(0, 10**6)
        elif xm == 2: x = rng.randint(0, 10**15)
        else:
            L = 1
            for a in A: L = L * a // __import__('math').gcd(L, a)
            x = (rng.randint(1, 10**6) * L - rng.randint(0, an)) if L > an else rng.randint(0, 10**9)
            x = max(x, 0)
        c, w = min_cover(A, x)
        hist[c] = hist.get(c, 0) + 1
        if c > 2 * n:
            viol += 1; out("COUNTEREXAMPLE", n, A, x, c, w)
        if c > worst.get(n, (0,))[0]: worst[n] = (c, A, x, w)
    out("n=%d: %d instances, a_n in [%d,%d]; histogram of min|B|: %s; violations of <=2n: %d; worst %s"
        % (n, sum(hist.values()), lo, hi, dict(sorted(hist.items())), viol, worst.get(n)))
out("elapsed %.0fs" % (time.time() - t0))
