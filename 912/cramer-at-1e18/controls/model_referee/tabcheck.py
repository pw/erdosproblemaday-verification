# brute-force check of model.c's coprime-prefix construction: F(x) = (x//P)*phi + tab[x % P], tab[y] = #{1<=u<=y : gcd(u,P)=1}
import numpy as np, math, random
pr = [2,3,5,7,11,13,17,19]; P = 1; phi = 1; random.seed(912)
for z, p in enumerate(pr):
    P *= p; phi *= p - 1
    u = np.arange(0, P + 1, dtype=np.int64); ok = np.ones(P + 1, np.int64); ok[0] = 0
    for q in pr[:z+1]: ok[u % q == 0] = 0
    tab = np.cumsum(ok)
    bad = 0
    for _ in range(300):
        a = random.randrange(10**6, 10**12); b = a + random.randrange(0, 5000)
        F = lambda x: (x // P) * phi + int(tab[x % P])
        direct = sum(1 for l in range(a + 1, b + 1) if all(l % q for q in pr[:z+1]))
        bad += (F(b) - F(a) != direct)
    print(f"z={p} P={P} phi={phi} tab[P]={tab[P]} (should = phi) mismatches in 300 random intervals: {bad}")
