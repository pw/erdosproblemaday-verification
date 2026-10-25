#!/usr/bin/env python3
"""Same as pool.py (complete pool of primes with e_p | N, completeness certificate prod p^{v_p(G)} == G) but with
Phi_n(x) computed by the Mobius product over divisors (integers only) so large N are fast. Output pool_N.json."""
import sys, json
from math import gcd, lcm
from sympy import factorint, isprime, divisors, mobius
N=int(sys.argv[1]); G=gcd(2**N-1,3**N-1); divs=divisors(N)
def phi(n,b):
    num=den=1
    for d in divisors(n):
        mu=mobius(n//d)
        if mu==1: num*=b**d-1
        elif mu==-1: den*=b**d-1
    return num//den
P2={a:phi(a,2) for a in divs}; P3={b:phi(b,3) for b in divs}
primes=set(); fails=[]
for a in divs:
    for b in divs:
        g=gcd(gcd(P2[a],P3[b]),G)
        if g<=1: continue
        f=factorint(g)
        for p in f:
            if not isprime(p): fails.append((a,b,p.bit_length()))
            else: primes.add(p)
prod=1; pool=[]
for p in sorted(primes):
    if p in (2,3): continue
    v=0; t=G
    while t%p==0: t//=p; v+=1
    prod*=p**v
    def order(a):
        for d in divs:
            if pow(a,d,p)==1: return d
    o2,o3=order(2),order(3); e=lcm(o2,o3)
    gen=None
    fe=factorint(e)
    for i in range(o2):
        for j in range(o3):
            h=pow(2,i,p)*pow(3,j,p)%p
            if all(pow(h,e//q,p)!=1 for q in fe): gen=h; break
        if gen: break
    table={}; t=1
    for k in range(e): table[t]=k; t=t*gen%p
    u,v3=table[2%p],table[3%p]; assert gcd(gcd(u,v3),e)==1
    pool.append({"p":p,"e":e,"ord2":o2,"ord3":o3,"u":u,"v":v3})
pool.sort(key=lambda r:(r["e"],r["p"])); dens=sum(1/r["e"] for r in pool)
print("N",N,"G bits",G.bit_length(),"pool",len(pool),"COMPLETE" if prod==G else f"INCOMPLETE cofactor bits {(G//prod).bit_length()} fails {fails}","sum1/e",round(dens,4),"largest p",max(r["p"] for r in pool))
json.dump({"N":N,"complete":prod==G,"pool":pool,"density":dens},open(f"pool_{N}.json","w"),indent=1)
