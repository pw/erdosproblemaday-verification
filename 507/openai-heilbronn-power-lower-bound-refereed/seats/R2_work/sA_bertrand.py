import math
from sympy import primerange, factorint, binomial
# P(x) < 4^x (log form) for integers up to 2e5
ps = list(primerange(2, 200001)); lp = 0.0; i = 0; worst = -1e9
for x in range(1, 200001):
    while i < len(ps) and ps[i] <= x: lp += math.log(ps[i]); i += 1
    worst = max(worst, lp - x*math.log(4))
print("max over x<=2e5 of log P(x) - x log 4 =", worst)
# exponent claims for C(2n, n), n up to 400
bad = 0
for n in range(3, 401):
    f = factorint(binomial(2*n, n))
    for p, e in f.items():
        if p**e > 2*n: bad += 1
        if 2*n/3 < p <= n: bad += 1
        if p > math.sqrt(2*n) and e > 1: bad += 1
        if n < p <= 2*n and e != 1: bad += 1
print("C(2n,n) exponent-claim violations for 3<=n<=400:", bad)
# threshold for (n/3) log4 > sqrt(2n) log(2n) + log(2n+1)
f = lambda n: (n/3)*math.log(4) - math.sqrt(2*n)*math.log(2*n) - math.log(2*n+1)
last_bad = max(n for n in range(1, 10**6) if f(n) <= 0)
print("last n with (n/3)log4 <= sqrt(2n)log(2n)+log(2n+1):", last_bad)
