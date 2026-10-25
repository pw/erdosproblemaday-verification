# Seat S: exact test of Lemma 5.1's key inequality in the Gaussian setting, with a negative control.
#   E_S H(F_S(Y)) - H(Hdat) <= s * av_c H(phi_c(Y) | Hdat)            (proof of Lemma 5.1)
# and then the printed conclusion (5.1): av_c[log p_c - H(phi_c(Y)|Hdat)] <= (eps+kappa) Lbar
# with eps, kappa defined as tightly as the hypotheses allow.
# Negative control: dropping the -H(Hdat) term must produce violations (the shared cost is load-bearing).
import math, random, itertools
from collections import defaultdict
random.seed(11)
primes = [101, 109, 113, 137, 149, 157, 173, 181, 193, 197]   # all = 1 mod 4, inside [T,2T] with T=101
primes = [p for p in primes if p <= 2*101]
def sqrtm1(p):
    for x in range(p):
        if (x*x + 1) % p == 0: return x
roots = {p: sqrtm1(p) for p in primes}
coords = [(p, s) for p in primes for s in (+1, -1)]
k = len(primes); Lbar = sum(math.log(p) for p in primes)/k
def phi(c, z): p, s = c; a, b = z; return (a + s*roots[p]*b) % p
def H(d): return -sum(v*math.log(v) for v in d.values() if v > 0)
def ent(joint, f):
    d = defaultdict(float)
    for w, pr in joint.items(): d[f(w)] += pr
    return H(d)
def cond(joint, f, g): return ent(joint, lambda w: (f(w), g(w))) - ent(joint, g)
worst_main = -1e9; worst_concl = -1e9; worst_nc = -1e9
for trial in range(120):
    # Y spread over many lattice points (high joint entropy); Hdat correlated with Y (sometimes strongly)
    pts = [(random.randint(-3000, 3000), random.randint(-3000, 3000)) for _ in range(random.randint(20, 120))]
    joint = {}
    mode = trial % 3
    for y in pts:
        for hh in range(random.randint(1, 6)):
            key = hh if mode == 0 else (hash(y) % 7 + hh if mode == 1 else hash((y, hh)) % 50)
            joint[(y, key)] = joint.get((y, key), 0) + random.random()
    tot = sum(joint.values()); joint = {kk: v/tot for kk, v in joint.items()}
    HH = ent(joint, lambda w: w[1])
    condc = [cond(joint, lambda w, c=c: phi(c, w[0]), lambda w: w[1]) for c in coords]
    avcond = sum(condc)/len(condc)
    for s in [1, 2, 3]:
        vals = []
        for sub in itertools.combinations(primes, s):
            for signs in itertools.product((+1, -1), repeat=s):
                S = list(zip(sub, signs))
                vals.append(ent(joint, lambda w: tuple(phi(c, w[0]) for c in S)))
        ES = sum(vals)/len(vals)
        worst_main = max(worst_main, ES - HH - s*avcond)
        worst_nc = max(worst_nc, ES - s*avcond)          # negative control: no shared-cost term
        eps = max(0.0, 1 - ES/(s*Lbar)); kappa = HH/(s*Lbar)
        lhs = sum(math.log(c[0]) - condc[j] for j, c in enumerate(coords))/len(coords)
        worst_concl = max(worst_concl, lhs - (eps + kappa)*Lbar)
print("max[E_S H(F_S Y) - H(Hdat) - s av H(phi|Hdat)]  (must be <= 0):", worst_main)
print("max[(5.1) LHS - (eps+kappa) Lbar]                 (must be <= 0):", worst_concl)
print("NEGATIVE CONTROL max[E_S H(F_S Y) - s av H(phi|Hdat)] (should be > 0):", worst_nc)
