# Exact R on the "full" diagonals a_K = phi(prod_{p<=y} p^K) — the family Theorem 1 uses — by the bnb instrument (exact integers)
# and the trivial-cover bound prod p/(p-1). Fractions printed exactly via the cover found.
import sys
from fractions import Fraction
from math import prod
from bnb import ell
from sympy import totient, primerange
S = sys.argv[1]; Kmax = int(sys.argv[2])
P = [int(t) for t in S.split(",")] if "," in S else list(primerange(2, int(S)+1)); y = max(P)
bound = prod(Fraction(p, p-1) for p in P)
print(f"y={y} primes {P} trivial bound prod p/(p-1) = {bound} = {float(bound):.6f}")
for K in range(2, Kmax+1):
    nK = prod(p**K for p in P); a = int(totient(nK))
    fac = {}
    for p in P:
        e=0; t=a
        while t % p == 0: t//=p; e+=1
        if e: fac[p]=e
    n, cov = ell(a, fac)
    R = Fraction(n, a)
    missing = [p for p in P if all(q != p for q,_ in cov)]; inS = all(all(p in P for p in __import__("sympy").factorint(q-1)) for q,_ in cov)
    print(f"K={K:3d} R={float(R):.12f} (R<bound: {R<bound}) S-primes absent: {missing} cover all S-smooth-shifted: {inS}  cover={cov}")
