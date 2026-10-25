# All primes p>=5 with e_p <= M (M=5040), via factoring g_d = gcd(2^d-1,3^d-1) for every d<=M.
# Every such prime divides g_{e_p}. Completeness per d is certified by cofactor==1.
import math, json, sys, time
from fractions import Fraction
from sympy import factorint, isprime, n_order
M = int(sys.argv[1]) if len(sys.argv) > 1 else 5040
known = set()
t0 = time.time()
maxdig = 0
for d in range(1, M + 1):
    g = math.gcd(2**d - 1, 3**d - 1)
    maxdig = max(maxdig, len(str(g)))
    rem = g
    for p in known:
        if rem % p == 0:
            while rem % p == 0: rem //= p
    if rem > 1:
        f = factorint(rem)
        for p in f:
            assert isprime(p)
            known.add(p)
        for p in f:
            while rem % p == 0: rem //= p
    assert rem == 1
    if d % 500 == 0: print(d, len(known), f"{time.time()-t0:.1f}s", flush=True)
rows = []
for p in sorted(known):
    if p < 5: continue
    a, b = n_order(2, p), n_order(3, p)
    e = a * b // math.gcd(a, b)
    if e <= M: rows.append((p, e))
print("max digits of g_d:", maxdig, " primes with e_p<=M:", len(rows))
json.dump(rows, open(f"/tmp/evidence203/all_e_le_{M}.json", "w"))
