# Independent re-check of item 5 WITHOUT the discrete-log parametrisation:
# a coset of L_p is the fibre {(k,l): 2^k 3^l == r (mod p)} for r in H_p. Enumerate r-tuples directly.
import itertools, math
import numpy as np
from fractions import Fraction
def run(primes):
    T = 1
    H = {}
    for p in primes:
        Hp = sorted({pow(2,k,p)*pow(3,l,p)%p for k in range(p) for l in range(p)})
        H[p] = Hp; T = T*len(Hp)//math.gcd(T, len(Hp))
    k = np.arange(T)
    res = {}
    for p in primes:
        pk = np.array([pow(2,int(i),p) for i in k]); pl = np.array([pow(3,int(i),p) for i in k])
        res[p] = (np.outer(pk, pl) % p).ravel()
    masks = {p: {r: res[p] == r for r in H[p]} for p in primes}
    best = -1; n = 0
    def rec(i, acc):
        nonlocal best, n
        if i == len(primes):
            n += 1; c = int(acc.sum()); best = max(best, c); return
        p = primes[i]
        for r in H[p]:
            rec(i+1, masks[p][r] if acc is None else acc | masks[p][r])
    rec(0, None)
    return T, best, n
for primes in [(5,7,11,13), (5,7,11,13,17)]:
    T, best, n = run(primes)
    print(primes, f"T={T} choices={n} max={best} density={Fraction(best,T*T)}")
