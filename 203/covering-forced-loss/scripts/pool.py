#!/usr/bin/env python3
"""#203 complete prime pool for a given N: all primes p ∤ 6 with e_p := |<2,3> mod p| dividing N.
Route: G = gcd(2^N-1, 3^N-1); split G by cyclotomic pairs gcd(Phi_a(2), Phi_b(3), G) over a,b | N; factor each piece with
sympy; COMPLETENESS CERTIFICATE = prod over found primes p^{v_p(G)} == G (then no prime divisor of G is missing).
For each prime: e_p (= lcm(ord 2, ord 3), computed directly by brute force on the small group), and the character
(u,v): 2 = g^u, 3 = g^v in <2,3> = <g>, so L_p = {(k,l): u k + v l ≡ 0 mod e}.  Output JSON pool_N.json."""
import sys, json
from math import gcd, lcm
from sympy import cyclotomic_poly, factorint, isprime, divisors
from sympy.abc import x
N=int(sys.argv[1])
G=gcd(2**N-1, 3**N-1)
divs=divisors(N)
Phi2={a:int(cyclotomic_poly(a, 2)) for a in divs}
Phi3={b:int(cyclotomic_poly(b, 3)) for b in divs}
primes={}
for a in divs:
    for b in divs:
        g=gcd(gcd(Phi2[a],Phi3[b]),G)
        if g<=1: continue
        f=factorint(g)
        for p in f: primes[p]=primes.get(p,0)
# completeness certificate
prod=1
pool=[]
for p in sorted(primes):
    if p in (2,3): continue
    v=0; t=G
    while t%p==0: t//=p; v+=1
    prod*=p**v
    assert isprime(p)
    # e_p directly: order of 2, order of 3 mod p by brute force (both divide N)
    def order(a):
        for d in sorted(divisors(N)):
            if pow(a,d,p)==1: return d
        raise RuntimeError
    o2,o3=order(2),order(3); e=lcm(o2,o3); assert N%e==0
    # generator of <2,3>: find 2^i 3^j of order e
    gen=None
    for i in range(o2):
        for j in range(o3):
            h=pow(2,i,p)*pow(3,j,p)%p
            if all(pow(h,e//q,p)!=1 for q in factorint(e)):
                gen=h; break
        if gen: break
    assert gen is not None
    table={}
    t=1
    for k in range(e):
        table[t]=k; t=t*gen%p
    assert len(table)==e
    u,v3=table[2%p],table[3%p]
    assert gcd(gcd(u,v3),e)==1
    pool.append({"p":p,"e":e,"ord2":o2,"ord3":o3,"u":u,"v":v3})
complete = (prod==G) or (prod==G//3**0)  # 3 never divides G? 3 | 2^N-1 iff N even; 3 ∤ 3^N-1 so 3 ∤ G; 2 ∤ G.
print("N",N,"G bits",G.bit_length(),"pool size",len(pool),"COMPLETE" if prod==G else f"INCOMPLETE (missing cofactor bits {(G//prod).bit_length()})")
pool.sort(key=lambda r:(r["e"],r["p"]))
dens=sum(1/r["e"] for r in pool)
print("sum 1/e_p =",round(dens,4))
for r in pool: print(f"  p={r['p']:>12} e={r['e']:5d} ord2={r['ord2']:5d} ord3={r['ord3']:5d} (u,v)=({r['u']},{r['v']})")
json.dump({"N":N,"complete":prod==G,"pool":pool,"density":dens},open(f"pool_{N}.json","w"),indent=1)
