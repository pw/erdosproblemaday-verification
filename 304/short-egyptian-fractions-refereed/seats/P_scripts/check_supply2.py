# Lemma 8.2 mechanism (exceptional primes, bilinear 5-product representation) for moderate u,
# and an end-to-end run of the Prop 8.1 construction (Lemmas 7.1, 8.3 constructive divisor, 8.4, 8.2) for one m.
import math, random, sys
from fractions import Fraction
from sympy import prime, primerange, isprime, nextprime
random.seed(7)
fails = 0
def bad(msg):
    global fails; fails += 1; print("FAIL", msg)

def ell(v): return math.ceil(4*math.log(v)/math.log(2))
PR = list(primerange(2, 20000))

# ---- Part A: exceptional primes for A = divisors of P(u), u odd moderate
def image_size(p, primes):
    S = {1}; full = p if any(q % p == 0 for q in primes) else p-1
    for q in primes:
        r = q % p
        S |= {(x*r) % p for x in S}
        if len(S) >= full: break
    return len(S), full
for u in (101, 501, 1001, 2001, 3001):
    L = ell(u); primes = PR[:L]
    logP = sum(math.log(q) for q in primes)
    B = 0; minratio = 1e9
    for p in primerange(2, u+1):
        h, full = image_size(p, primes)
        if h <= p**0.75: B += 1
        minratio = min(minratio, h/p**0.75)
    bound = 2*u**0.75*logP/math.log(2)
    print(f"u={u}: ell(u)={L}, N=2^{L} >= u^4: {2**L >= u**4}, exceptional primes B(u)={B}, (8.3) bound={bound:.0f}, min |A_p|/p^(3/4)={minratio:.2f}")

# ---- Part B: the exponential-sum bound |E e_p(rU)| <= sqrt(p)/h for a few p with H = A_p small-ish (brute force)
import cmath
def check_bilinear(p, H):
    h = len(H); worst = 0
    for r in range(1, p):
        s = sum(cmath.exp(2j*math.pi*r*a*b/p) for a in H for b in H)
        worst = max(worst, abs(s)/h**2)
    return worst, math.sqrt(p)/h
for p in (31, 61, 101):
    H = sorted(random.sample(range(p), int(p**0.75)+1))
    w, b = check_bilinear(p, H)
    print(f"bilinear p={p} h={len(H)}: max|E e_p(rU)|={w:.4f} <= sqrt(p)/h={b:.4f}: {w <= b+1e-12}")
    if w > b + 1e-12: bad("bilinear")

# ---- Part C: end-to-end Prop 8.1 construction for one m (demo K = P(Y)^2 * S0!, S0 covers the small s)
m = int(sys.argv[1]) if len(sys.argv) > 1 else 50
Y = m**4; LY = ell(Y); PY = math.prod(PR[:LY]); S0 = 60
K = PY*PY*math.factorial(S0)
print(f"\nm={m}: ell(Y)={LY}, log K={math.log(K):.1f}, (32/log2) log m loglog m={32/math.log(2)*math.log(m)*math.log(math.log(m)):.1f}")

def subset_divisor(primes):
    d = 1
    for q in primes:
        if random.random() < 0.5: d *= q
    return d

def rep_prime(p, Pu_primes):
    """five e_i | P(u)^2 (each a product of two divisors of P(u)) with p | sum; returns (e list, t)."""
    table = {}
    for _ in range(4000):
        d = subset_divisor(Pu_primes); table.setdefault(d % p, d)
    for attempt in range(200000):
        es = [subset_divisor(Pu_primes)*subset_divisor(Pu_primes) for _ in range(4)]
        tau = (-sum(es)) % p
        if tau == 0: continue
        d2 = subset_divisor(Pu_primes)
        if d2 % p == 0: continue
        need = tau*pow(d2, -1, p) % p
        if need in table:
            es.append(table[need]*d2)
            tot = sum(es); assert tot % p == 0
            return es, tot // p
    return None

Pcache = {}
def supply(s):
    if s <= S0: return [(s, 1)]
    u = s if s % 2 else s-1
    extra = [] if s % 2 else [(1, 1)]
    Lu = ell(u); Pu = PR[:Lu]
    # three primes summing to u
    for p1 in primerange(max(3, u//3), u):
        rest = u - p1
        found = None
        for p2 in primerange(3, rest//2+1):
            if isprime(rest - p2): found = (p1, p2, rest-p2); break
        if found: break
    out = list(extra)
    for p in found:
        r = rep_prime(p, Pu)
        if r is None: return None
        es, t = r
        out += [(e, t) for e in es]
    return out

# Greedy prefix never leaves R>0 for small m (checked separately), so build a synthetic chain obeying
# exactly the Lemma 8.3 hypothesis (q0=m, multipliers n<=q+1) up to q >= 2mK, and a numerator R<2m.
T = 2*m*K
q = m; ns, qs = [], [m]
while q < T:
    n = random.choice([q+1, random.randint(2, q+1), random.randint(2, 50)])
    ns.append(n); q *= n; qs.append(q)
R = random.randint(1, 2*m-1)
j = len(ns)
print(f"synthetic chain length {j}, R={R}, q has {q.bit_length()} bits")
def div(w, lvl):
    """constructive divisor of qs[lvl] in [w/m, w] for real w in [1, qs[lvl]] (proof of Lemma 8.3)."""
    if lvl == 0: return 1
    qp, n = qs[lvl-1], ns[lvl-1]
    if w <= qp: return div(w, lvl-1)
    if w >= n: return n*div(w/n, lvl-1)
    return qp

X = R*K; assert 1 <= X < q
Xi = X; groups = []
while Xi > 0:
    if Xi > m**4:
        w = Fraction(Xi, m*m); d = div(w, j)
        if not (q % d == 0 and Fraction(Xi, m**3) <= d <= w): bad("divisor"); break
        s = Xi // d; groups.append((d, s)); Xi -= d*s
    else:
        groups.append((1, Xi)); Xi = 0
G = len(groups)
print(f"groups G={G} (bound log X/(2 log m)+2 = {math.log(X)/(2*math.log(m))+2:.1f})")
assert sum(d*s for d, s in groups) == X
tail = []; maxh = 0
for d, s in groups:
    sup = supply(s)
    if sup is None: bad(("supply", s)); continue
    maxh = max(maxh, len(sup))
    if sum(Fraction(e, t) for e, t in sup) != s: bad(("supply sum", s))
    for e, t in sup:
        if K % e: bad(("e|K", e))
        assert q % d == 0
        tail.append((q//d)*(K//e)*t)
print(f"max summands per s: {maxh} (claim <=16); tail terms={len(tail)} (<= 16G={16*G})")
# exact identity: sum over groups of (d/(qK)) * s = X/(qK) = R/q  (already exact per group)
print("all tail denominators > m:", all(x > m for x in tail))
print(f"tail length {len(tail)} vs 16*G={16*G}")
# direct exact check of the full sum with Fractions on the tail (may be slow but exact)
acc = Fraction(0)
for x in tail: acc += Fraction(1, x)
print("exact: sum of tail unit fractions == R/q :", acc == Fraction(R, q))
if acc != Fraction(R, q): bad("tail sum")
print("TOTAL FAILS", fails)
