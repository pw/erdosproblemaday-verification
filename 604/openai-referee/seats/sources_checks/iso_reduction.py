# Check: #{ordered (x,y), x!=y, k_P(x,y) >= T}  <=  2*A/(T-1)  for T >= 2,
# where A = #{(x,{y,z}) : y!=z, |xy| = |xz|} (apex-isosceles triples, degenerate ones included).
# This is the reduction "isosceles-triangle bound => Theorem 1.1 for large s".
# Exact integer squared distances. Control: a deliberately wrong bound (A/(10*(T-1))) must FAIL somewhere.
import itertools, random, sys
from collections import Counter
def stats(P, T):
    rich = 0; A = 0
    for x in P:
        c = Counter((y[0]-x[0])**2 + (y[1]-x[1])**2 for y in P if y != x)
        for d, k in c.items():
            A += k*(k-1)//2
            if k >= T: rich += k          # each y in a fiber of size k >= T is a rich pair (x,y)
    return rich, A
def check(bound_factor, label):
    bad = 0; tot = 0
    configs = []
    for m in (5, 6, 7, 8):
        configs.append(("grid%d" % m, [(i, j) for i in range(m) for j in range(m)]))
    random.seed(1)
    for t in range(6):
        configs.append(("rand%d" % t, list({(random.randrange(12), random.randrange(12)) for _ in range(45)})))
    configs.append(("circle+centre", [(0,0),(5,0),(-5,0),(0,5),(0,-5),(3,4),(4,3),(-3,4),(-4,3),(3,-4),(4,-3),(-3,-4),(-4,-3)]))
    for name, P in configs:
        for T in range(2, 13):
            rich, A = stats(P, T)
            tot += 1
            if not (rich * (T-1) <= bound_factor * A):
                bad += 1
                if bad <= 3: print("  %s VIOLATION %s n=%d T=%d rich=%d A=%d" % (label, name, len(P), T, rich, A))
    print("%s: %d/%d cases violate" % (label, bad, tot))
    return bad
b1 = check(2.0, "claimed bound rich*(T-1) <= 2A")
b2 = check(0.2, "CONTROL rich*(T-1) <= 0.2A (wrong)")
print("RESULT:", "PASS" if b1 == 0 and b2 > 0 else "FAIL")
