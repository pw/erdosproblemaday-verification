# Enumerate all distinct k-term Egyptian expansions of 1 (exact arithmetic), k<=KMAX.
# Output: pickle of {k: list of tuples}
import sys, pickle, time
from math import gcd
from sympy import factorint

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
OUT = sys.argv[2] if len(sys.argv) > 2 else '/tmp/oaimath/025/seats/P_scripts/expansions.pkl'

def divisors_from_fact(f):
    ds = [1]
    for p, e in f.items():
        ds = [d * p**i for d in ds for i in range(e + 1)]
    return ds

def two_term(num, den, lo, prefix, out):
    # 1/x + 1/y = num/den, lo <= x < y ; (num x - den)(num y - den) = den^2
    f = factorint(den)
    f2 = {p: 2 * e for p, e in f.items()}
    D = den * den
    for d1 in divisors_from_fact(f2):
        if d1 >= den:
            continue
        d2 = D // d1
        if (d1 + den) % num or (d2 + den) % num:
            continue
        x = (d1 + den) // num
        y = (d2 + den) // num
        if x >= lo and x < y:
            out.append(tuple(prefix + [x, y]))

def rec(num, den, t, lo, prefix, out):
    if t == 1:
        if num == 1 and den >= lo:
            out.append(tuple(prefix + [den]))
        return
    if t == 2:
        two_term(num, den, lo, prefix, out)
        return
    # x > den/num (strict since more terms follow), x < t*den/num
    xmin = max(lo, den // num + 1)
    xmax = (t * den - 1) // num  # x <= (t*den-1)/num  <=> num*x < t*den
    for x in range(xmin, xmax + 1):
        n2 = num * x - den
        d2 = den * x
        g = gcd(n2, d2)
        rec(n2 // g, d2 // g, t - 1, x + 1, prefix + [x], out)

res = {}
for k in range(1, KMAX + 1):
    t0 = time.time()
    out = []
    if k == 1:
        out = [(1,)]
    else:
        rec(1, 1, k, 2, [], out)
    out = sorted(set(out))
    # exact verification of each
    from fractions import Fraction
    for tup in out:
        assert sum(Fraction(1, n) for n in tup) == 1, tup
        assert all(tup[i] < tup[i+1] for i in range(len(tup)-1))
    res[k] = out
    print(f"k={k} F={len(out)} time={time.time()-t0:.1f}s", flush=True)
pickle.dump(res, open(OUT, 'wb'))
