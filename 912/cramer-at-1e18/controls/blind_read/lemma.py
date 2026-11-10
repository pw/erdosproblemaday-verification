# Independent test of the Lemma for EVERY prime q with q^2 <= x+1 (not only divisors), x <= 2e5,
# its sharpness at q^2 = x+2, and the "bound is attained" count in the Theorem's proof.
import numpy as np, math
X = 200000
isp = np.ones(X + 2, bool); isp[:2] = False
for i in range(2, math.isqrt(X + 1) + 1):
    if isp[i]: isp[i*i::i] = False
P = np.nonzero(isp)[0]
def ex(x, p):
    e = 0; q = p
    while q <= x: e += x // q; q *= p
    return e
fails = []; fails_ext = 0; ext_checks = 0
from collections import Counter
for x in range(1, X + 1):
    ps = P[P <= x]
    if ps.size == 0: continue
    # exponents only near the small primes matter: compute for primes up to sqrt(x+2) and their right neighbour,
    # plus the multiset of all exponents via floor(x/p) for p > sqrt(x)
    lim = math.isqrt(x + 2) + 1
    small = [int(p) for p in ps if p <= lim]
    if not small: continue
    vals = Counter()
    for p in ps:
        p = int(p); vals[ex(x, p) if p * p <= x else x // p] += 1
    for q in small:
        if q * q <= x + 1 and (q, x) != (2, 3):
            if vals[ex(x, q)] != 1: fails.append((x, q))
        elif q * q == x + 2:
            ext_checks += 1
            if vals[ex(x, q)] != 1: fails_ext += 1
    if x == 20000: print("progress", x, "fails", len(fails))
print("Lemma failures (all q with q^2<=x+1, x<=2e5):", len(fails), fails[:5])
print("q^2 = x+2 cases:", ext_checks, "of which q not alone:", fails_ext)
