# Targeted adversarial instances (Erdos-Suranyi pair-product shape) in the long range a_n >= 8n^3.
import sys
sys.argv = ['x']
src = open('/tmp/e708/refA/longcheck.py').read().split("log = open")[0]
exec(src)   # defines factor, vp, min_cover, brute_min only
import itertools
def isp(n): return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))
out = open('/tmp/e708/refA/longcheck_es.log', 'w')
worst = 0
for trip in itertools.combinations([p for p in range(11, 60) if isp(p)], 3):
    p1, p2, p3 = trip
    A = sorted([p1 * p2, p1 * p3, p2 * p3]); n = 3; m = A[-1]
    if m < 8 * n**3: continue
    if not (2 * p1 * p1 > p3 * p3): continue
    u = p1 * p2 * p3
    for k in (1, 2, 7):
        x = k * u - (m + 1) // 2
        c, w = min_cover(A, x)
        worst = max(worst, c)
        line = "A=%s x=%d min=%d witness=%s" % (A, x, c, w)
        out.write(line + "\n")
        if c > 2 * n: print("COUNTEREXAMPLE", line)
print("E-S shaped n=3 long instances done; max min|B| =", worst, "(2n = 6)")
out.write("max min|B| = %d\n" % worst)
