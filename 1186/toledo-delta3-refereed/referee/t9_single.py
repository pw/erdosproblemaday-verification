import sys, json; sys.path.insert(0, '.')
from d3 import *
H = hnodes()
grid = json.load(open('/home/exedev/MathDyad/erdos1186/repo/certs/delta3/inner-r20-g24_4_8.json'))['grid']
def beta(p, q, y):   # exact bathtub value: integral of h over the lowest-level set of measure w*y
    w = F(q-p, U); target = w*y
    vals = sorted(set(H[p:q+1]))
    def meas_int(v):
        m = F(0); I = F(0)
        for x in range(p, q):
            h0, h1 = H[x], H[x+1]; lo, hi = min(h0, h1), max(h0, h1)
            if v <= lo: continue
            if v >= hi: m += F(1, U); I += F(1, U)*(h0+h1)/2; continue
            frac = (v-lo)/(hi-lo); m += F(1, U)*frac; I += F(1, U)*frac*(lo+v)/2
        return m, I
    for k in range(len(vals)-1):
        m0, _ = meas_int(vals[k]); m1, _ = meas_int(vals[k+1])
        if m0 <= target <= m1:
            v = vals[k] + (vals[k+1]-vals[k])*(target-m0)/(m1-m0) if m1 > m0 else vals[k]
            return meas_int(v)[1]
    return meas_int(vals[-1])[1]
viol = 0; tests = 0; worst = None
for i in range(len(grid)-1):
    p, q = grid[i], grid[i+1]; w = F(q-p, U)
    seg = H[p:q+1]
    mono = all(seg[k] <= seg[k+1] for k in range(len(seg)-1)) or all(seg[k] >= seg[k+1] for k in range(len(seg)-1))
    if mono: continue
    a = w*min(seg)
    single = max(abs(F(1)/((H[x+1]-H[x])*U)) for x in range(p, q))
    b1 = w*w/(2*single)
    from t2_constants_lib import my_bathtub
    _, bsum = my_bathtub(p, q)
    for t in range(1, 17):
        y = F(t, 16); tests += 1
        B = beta(p, q, y)
        assert B >= a*y + bsum*y*y
        if B < a*y + b1*y*y:
            viol += 1
print('non-monotone cells, single-slope reading: violations', viol, 'of', tests, ' (summed reading: 0 violations by assert)')
