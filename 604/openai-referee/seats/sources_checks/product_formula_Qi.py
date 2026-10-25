# Check the paper's normalisation (3.2) in K = Q(i), [K:Q] = 2 (one complex place, no real places):
#   finite place v | p: |.|_v extends |p|_p = 1/p, sigma_v = [K_v:Q_p]/[K:Q];  complex place: ordinary modulus, sigma = 2/[K:Q] = 1.
#   Claim: sum_v sigma_v log|z|_v = 0 for z != 0, and sum_{v|inf} sigma_v = 1.
# Gaussian-prime valuations computed by exact division in Z[i]. Controls: (a) squared modulus at the complex place
# with sigma=1 (double counting), (b) finite weights not divided by [K:Q]; both must FAIL.
import math, random
def gdivmod_exact(a, b):           # return a/b if b | a in Z[i], else None; a,b as (re,im)
    (x, y), (u, v) = a, b
    n = u*u + v*v
    re, im = x*u + y*v, y*u - x*v
    if re % n or im % n: return None
    return (re // n, im // n)
def val(z, pi):
    k = 0
    while True:
        q = gdivmod_exact(z, pi)
        if q is None: return k
        z, k = q, k + 1
def gaussian_prime_over(p):        # a Gaussian prime pi with N(pi)=p, p = 1 mod 4 or p = 2
    for a in range(1, int(p**0.5) + 1):
        b2 = p - a*a; b = int(round(b2**0.5))
        if b*b == b2: return (a, b)
def factor(n):
    f, d = {}, 2
    while d*d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def total(z, mode):
    N = z[0]**2 + z[1]**2
    s_fin = 0.0
    for p in factor(N):
        places = []                # (sigma_v, log|z|_v)
        if p == 2:
            places.append((2/2, -val(z, (1, 1)) * 0.5 * math.log(2)))      # e=2: |1+i|_v = 2^(-1/2), n_v = 2
        elif p % 4 == 3:
            places.append((2/2, -val(z, (p, 0)) * math.log(p)))            # inert: n_v = 2
        else:
            a, b = gaussian_prime_over(p)
            for pi in ((a, b), (a, -b)):
                places.append((1/2, -val(z, pi) * math.log(p)))           # split: n_v = 1 each
        for sig, lg in places:
            s_fin += sig * (2 if mode == "undivided" else 1) * lg
    mod = math.hypot(*z)
    s_inf = 1.0 * (2*math.log(mod) if mode == "squared" else math.log(mod))
    return s_fin + s_inf
random.seed(7)
zs = [(random.randint(-300, 300), random.randint(-300, 300)) for _ in range(400)]
zs = [z for z in zs if z != (0, 0)]
for mode in ("paper", "squared", "undivided"):
    worst = max(abs(total(z, mode)) for z in zs)
    print("%-10s max |sum sigma_v log|z|_v| over %d Gaussian integers = %.3e  -> %s" %
          (mode, len(zs), worst, "HOLDS" if worst < 1e-9 else "FAILS"))
print("sum_{v|inf} sigma_v = 2/[K:Q] * (#complex places = 1) =", 2/2*1)
