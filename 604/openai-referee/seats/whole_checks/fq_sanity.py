# Sanity test (brief item (i)): P = F_q^2 inside the field F_{q^2} = F_q(i).
# For q = 3 mod 4: Z1(u,v) = u + i v, Z2(u,v) = u - i v are INJECTIVE on P and t(x,y) = dZ1*dZ2 = du^2+dv^2 is NONZERO
# for distinct points -- i.e. every hypothesis of Sec.3.1 that the paper takes from the reals holds -- yet every pin sees
# only q-1 = sqrt(n)-1 distinct values and every pair lies in a fiber of size q+1 ~ sqrt(n): F_n(s) = 1 for s <= log(q+1)/log(q^2).
# CONTROL that must FAIL the hypotheses: q = 1 mod 4 (i in F_q): Z1 not injective and t vanishes on distinct pairs (isotropic lines).
from collections import Counter
def run(q):
    # F_{q^2} for q = 3 mod 4 as pairs (a,b) = a + b*i with i^2 = -1; for q = 1 mod 4 take i = a square root of -1 in F_q
    pts = [(u,v) for u in range(q) for v in range(q)]
    n = len(pts)
    if q % 4 == 3:
        Z1 = lambda p: (p[0] % q, p[1] % q)          # u + i v  as an element of F_q(i)
        Z2 = lambda p: (p[0] % q, (-p[1]) % q)       # u - i v
    else:
        I = next(x for x in range(q) if (x*x+1) % q == 0)
        Z1 = lambda p: (p[0] + I*p[1]) % q
        Z2 = lambda p: (p[0] - I*p[1]) % q
    inj1 = len({Z1(p) for p in pts}) == n; inj2 = len({Z2(p) for p in pts}) == n
    zero_t = 0; minvals = n; maxfib_min = n; fibsizes = Counter()
    for x in pts:
        vals = Counter()
        for y in pts:
            if y == x: continue
            t = ((y[0]-x[0])**2 + (y[1]-x[1])**2) % q    # = (Z1(y)-Z1(x))(Z2(y)-Z2(x)) in F_{q^2}; lies in F_q
            if t == 0: zero_t += 1; continue
            vals[t] += 1
        minvals = min(minvals, len(vals))
        for y in pts:
            if y == x: continue
            t = ((y[0]-x[0])**2 + (y[1]-x[1])**2) % q
            if t: fibsizes[vals[t]] += 1
    return n, inj1, inj2, zero_t, minvals, dict(fibsizes)
for q in (3, 7, 11, 19, 23, 5, 13):
    n, i1, i2, z, mv, fs = run(q)
    print(f"q={q:2d} (q mod 4 = {q%4}) n={n:4d} Z1 injective={i1} Z2 injective={i2} distinct pairs with t=0: {z:5d} "
          f"MIN over pins of #distinct nonzero t = {mv} (sqrt n = {n**.5:.0f}); fiber sizes over ordered pairs: {fs}")
