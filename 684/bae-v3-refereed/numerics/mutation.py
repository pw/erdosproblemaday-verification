# Control: would the literal comparison catch a definitional slip? Mutant = primes < k instead of ≤ k.
from math import comb
def f(n, strict):
    for k in range(1, n+1):
        m, u = comb(n, k), 1
        lim = k - 1 if strict else k
        for p in range(2, lim + 1):
            while m % p == 0: m //= p; u *= p
        if u > n*n: return k
    return 0
oe = {}
for line in open('b392019.txt'):
    if line.startswith('#') or not line.strip(): continue
    n, v = map(int, line.split()); oe[n] = v
good = sum(f(n, False) == oe[n] for n in oe); bad = [n for n in oe if f(n, True) != oe[n]]
print(f"faithful: {good}/{len(oe)} agree; mutant (p<k): {len(bad)} disagreements, first {bad[:8]}")
