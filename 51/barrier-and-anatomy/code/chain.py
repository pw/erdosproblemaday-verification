# Verify the July safe-marker chain exactly (bnb) and greedily extend it: at each step append the prime power p^e
# (p prime, e in {1,2}, p not yet used) that maximises R while n*p^e stays the LEAST preimage of phi(n*p^e).
import sys, time
from fractions import Fraction
from math import prod
from sympy import factorint, primerange, totient
from bnb import ell
def phi_fac(n):
    f=factorint(n); a=1; fa={}
    for p,e in f.items():
        for q,k in factorint(p-1).items(): fa[q]=fa.get(q,0)+k
        if e>1: fa[p]=fa.get(p,0)+e-1
    a=1
    for q,k in fa.items(): a*=q**k
    return a, fa
def is_least(n):
    a,fa=phi_fac(n)
    m,cov=ell(a,fa)
    return m==n, m, a, cov
def main():
    chain=[3,5,17,47,347,1187,1367,5387]
    n=1
    for p in chain:
        n*=p
        ok,m,a,cov=is_least(n)
        print(f"append {p:6d}: least={ok}  R={float(Fraction(n,a)):.12f}  a={a}  {'' if ok else 'least is '+str(cov)}")
    sys.stdout.flush()
    PMAX=int(sys.argv[1]) if len(sys.argv)>1 else 20000
    STEPS=int(sys.argv[2]) if len(sys.argv)>2 else 4
    used=set(chain)
    for step in range(STEPS):
        t=time.time(); best=None
        for p in primerange(3,PMAX):
            if p in used: continue
            for e in (1,2):
                cand=n*p**e
                ok,m,a,cov=is_least(cand)
                if ok:
                    R=Fraction(cand,a)
                    if best is None or R>best[0]: best=(R,p,e,a)
                # first p that works gives the largest p/(p-1); later p only smaller, so stop scanning at first success per e
            if best is not None and best[1]==p: break
        if best is None: print('no extension below',PMAX); break
        R,p,e,a=best; n*=p**e; used.add(p)
        print(f"step {step}: append {p}^{e}  R={float(R):.12f}  a={a} (log10 {len(str(a))-1})  [{time.time()-t:.0f}s]"); sys.stdout.flush()
    print('final n =',factorint(n))

if __name__=="__main__":
    main()
