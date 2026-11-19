import sys
sys.path.insert(0, ".")
from d3 import *
H = hnodes()
def my_bathtub(p, q):
    w = F(q-p, U)
    vals = sorted(set(H[p:q+1]))
    mn = vals[0]
    a = w*mn
    if any(H[x] == H[x+1] for x in range(p, q)): return a, F(0)
    def meas(v):   # |{t in [p,q]/U : h(t) < v}|
        acc = F(0)
        for x in range(p, q):
            lo, hi = min(H[x], H[x+1]), max(H[x], H[x+1])
            if v <= lo: continue
            if v >= hi: acc += F(1, U); continue
            acc += F(1, U)*(v-lo)/(hi-lo)
        return acc
    ms = [meas(v) for v in vals]
    assert ms[0] == 0 and ms[-1] == w
    # m is linear between consecutive node values -> check at midpoints
    sup = F(0)
    for k in range(len(vals)-1):
        mid = (vals[k]+vals[k+1])/2
        assert 2*meas(mid) == ms[k]+ms[k+1]
        sup = max(sup, (ms[k+1]-ms[k])/(vals[k+1]-vals[k]))
    b = w*w/(2*sup)
    return a, b

