# Where does the new bound k^{c k floor(log2 r)} overtake the published lower bounds?
# Compare (ln bound)/k as functions of L = ln k (exact division by k = e^L done analytically; no overflow).
import math

def logstar(x):                      # FH convention: iterations of natural log until value <= 1
    n = 0
    while x > 1:
        x = math.log(x); n += 1
    return n

def new(L, c, r):  return c * L * (r.bit_length() - 1)                    # ln(k^{c k fl}) / k
def cfs(L):        return L * math.exp(-L) + (1 - math.exp(-L)) * math.log(2)  # ln(k 2^{k-1}) / k
def ks(L, r):      return (1 - math.exp(-L)) * math.log(r)                 # ln(r^{k-1}) / k  (beta=1)
def fh3(L):        return math.log(2) * (1 + logstar(L)) / 4               # ln(2^{k log*k /4}) / k, log*k = 1+log*(ln k)

def crossover(fn, fo, lo, hi):
    assert not fn(lo) > fo(lo), "new already ahead at lo"
    assert fn(hi) > fo(hi), "new not ahead at hi"
    for _ in range(200):
        mid = (lo + hi) / 2
        if fn(mid) > fo(mid): hi = mid
        else: lo = mid
    return hi

c = 1e-5
for name, r, fo in [("CFS Thm1, r=2", 2, cfs), ("KS Thm2, r=2, beta=1", 2, lambda L: ks(L, 2)),
                    ("FH Thm1, r=3", 3, fh3), ("KS Thm2, r=3, beta=1", 3, lambda L: ks(L, 3))]:
    L = crossover(lambda L: new(L, c, r), fo, 1.0, 1e7)
    print(f"{name:22s} new > old from ln k = {L:10.3f}  i.e. k ~ 10^{L/math.log(10):8.1f}   (log* k there = {1+logstar(L)})")
print("ln2/c =", math.log(2)/c, "  ln3/c =", math.log(3)/c)
# CONTROL (must contradict the 'astronomical crossover' conclusion): deliberately wrong constant c = 1
L = crossover(lambda L: new(L, 1.0, 2), cfs, 0.1, 50.0)
print(f"CONTROL c=1: new > CFS from ln k = {L:.4f} (k ~ {math.exp(L):.3f})  -> small, so the check can say 'not astronomical'")
