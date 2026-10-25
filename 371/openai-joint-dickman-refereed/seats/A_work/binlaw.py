import math, numpy as np
from scipy import integrate
# limit law J=3
M2 = integrate.quad(lambda v: math.log(3*(1-v))/v, 1/3, 2/3)[0]
lim = {(0,1): math.log(1.5), (2,0): M2/2, (1,0): math.log(2)-M2}
lim[(0,0)] = 1 - sum(lim.values())
print("limit law J=3:", {k: round(v,4) for k,v in lim.items()})
x = 3_000_000
N = 9*x
# largest-prime-power structure: compute Omega in bins via spf sieve
spf = np.zeros(N+1, dtype=np.int32)
for p in range(2, int(N**0.5)+1):
    if spf[p] == 0:
        idx = np.arange(p*p, N+1, p)
        sel = spf[idx] == 0
        spf[idx[sel]] = p
r = np.arange(N+1, dtype=np.int64)
spf_full = np.where(spf == 0, r, spf).astype(np.int64)
b1lo, b1hi, b2hi = x**(1/3), x**(2/3), x
def counts(n):
    c1 = c2 = 0
    while n > 1:
        p = spf_full[n]; n //= p
        if b1lo < p <= b1hi: c1 += 1
        elif b1hi < p <= b2hi: c2 += 1
    return c1, c2
import random
random.seed(0)
def law(alpha, beta, q, a, samples=200000):
    res = {}
    for _ in range(samples):
        n = random.randrange(int(alpha*x)+1, int(beta*x)+1)
        n = n - ((n - a) % q)
        if n <= alpha*x: n += q
        k = counts(n)
        res[k] = res.get(k, 0) + 1
    return {k: round(v/samples,4) for k,v in sorted(res.items())}
print("(x,2x], q=1   :", law(1,2,1,0))
print("(5x,6x], 2 mod 7:", law(5,6,7,2))
print("(0.2x,0.5x], 3 mod 4:", law(0.2,0.5,4,3))
