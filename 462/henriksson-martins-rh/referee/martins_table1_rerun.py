import sys, math
import numpy as np
def spf_window(lo, hi):
    # least prime factor for n in [lo, hi]
    n = hi - lo + 1
    lp = np.zeros(n, dtype=np.int64)
    r = int(math.isqrt(hi)) + 1
    small = np.ones(r+1, dtype=bool); small[:2] = False
    for i in range(2, int(r**0.5)+1):
        if small[i]: small[i*i::i] = False
    primes = np.nonzero(small)[0]
    for p in primes:
        start = ((lo + p - 1)//p)*p
        if start == p: start += p  # p itself is prime, skip
        idx = np.arange(start - lo, n, p)
        sel = idx[lp[idx] == 0]
        lp[sel] = p
    return lp
def S(C, x, L=None):
    H = C*math.sqrt(x)*math.log(x)**2
    lo = math.ceil(x); hi = math.floor(x+H)
    lp = spf_window(lo, hi)
    ns = np.arange(lo, hi+1, dtype=np.float64)
    comp = lp > 0
    s = float(np.sum(lp[comp]/ns[comp]))
    out = [x, H, s, int(np.sum(~comp))]
    for Lv in (3, 10):
        m = comp & (lp >= math.sqrt(x)/Lv)
        out.append(float(np.sum(lp[m]/ns[m])))
    return out
for x in [10**6, 2*10**6, 10**7, 10**8]:
    print(S(1.0, x), flush=True)
print(S(0.25, 10**9), flush=True)
