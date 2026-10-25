# Targeted extension of the July chain: try appending safe primes p = 2q+1 (q prime) in increasing order, p > 5387,
# and report every p for which n*p is the least preimage of phi(n*p) (exact, bnb).
import sys, time
from fractions import Fraction
from sympy import isprime, primerange
from chain import is_least
n=3*5*17*47*347*1187*1367*5387
hits=0; t=time.time()
for q in primerange(2694, int(sys.argv[1])):
    p=2*q+1
    if not isprime(p): continue
    ok,m,a,cov=is_least(n*p)
    if ok:
        hits+=1; print(f"p={p} (q={q}) least: R={float(Fraction(n*p,a)):.12f} a={a} [{time.time()-t:.0f}s]", flush=True)
        if hits>=3: break
print('done', time.time()-t, flush=True)
