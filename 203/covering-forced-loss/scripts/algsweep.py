#!/usr/bin/env python3
"""Algebraic-factorisation variant for a block of primes: m = t^{N0}.  For d = gcd(N0, LCM) with LCM = lcm(p-1 : p in block)
the admissible cosets of a block prime p are those c with m ≡ -h^{-c} (mod p) an N0-th power residue, i.e. a
gcd(d,p-1)-th power residue; the free set F_d = ∪_{odd prime q | d} qZ² ∪ ([4|d] {k≡2 (4), l≡0 (4)}).
Prints U_d = max |∪ admissible cosets ∪ F_d| / T² for every d | LCM, via maxunion2 (exact brute force).
Usage: algsweep.py pool.json p1,p2,...  (T = lcm(e_p) must be divisible by every odd q | LCM we use as free set: we
only build qZ² for q | d AND q | T; other q are credited as a density allowance by the caller)."""
import sys, json, subprocess, numpy as np
from math import gcd, lcm
from sympy import divisors, factorint, primefactors
pool={r["p"]:r for r in json.load(open(sys.argv[1]))["pool"]}
S=[int(x) for x in sys.argv[2].split(",")]
rows=[pool[p] for p in S]
T=1
for r in rows: T=lcm(T,r["e"])
LCM=1
for p in S: LCM=lcm(LCM,p-1)
# generator h of H_p consistent with (u,v): h^u = 2, h^v = 3.  Recover: find a,b with a*u+b*v ≡ 1 (mod e) -> h = 2^a 3^b.
def gen(r):
    p,e,u,v=r["p"],r["e"],r["u"],r["v"]
    for a in range(e):
        for b in range(e):
            if (a*u+b*v)%e==1:
                h=pow(2,a,p)*pow(3,b,p)%p
                assert pow(h,u,p)==2%p and pow(h,v,p)==3%p
                return h
    raise RuntimeError
H={r["p"]:gen(r) for r in rows}
blk="blk_%s.txt"%("_".join(map(str,S)))
open(blk,"w").write("".join(f"{r['e']} {r['u']} {r['v']}\n" for r in rows))
k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
def fixed_bits(d):
    F=np.zeros((T,T),dtype=bool)
    for q in primefactors(d):
        if q==2: continue
        assert T%q==0, (q,T)
        F|=((k%q==0)&(l%q==0))
    if d%4==0: F|=((k%4==2)&(l%4==0))
    return F
results={}
for d in divisors(LCM):
    allowed=[]
    for r in rows:
        p,e=r["p"],r["e"]; g=gcd(d,p-1); h=H[p]
        ok=[c for c in range(e) if pow((-pow(h,(-c)%e,p))%p,(p-1)//g,p)==1]
        allowed.append(ok)
    if d==1: allowed[0]=[0]  # translation invariance, no fixed set, no constraints
    af=f"allow_{d}.txt"; open(af,"w").write("".join(" ".join(map(str,a))+"\n" for a in allowed))
    F=fixed_bits(d); fb="-"
    if F.any():
        fb=f"fixed_{d}.bin"; bits=np.packbits(F.reshape(-1),bitorder="little"); 
        pad=(-(len(bits)))%8; bits=np.concatenate([bits,np.zeros(pad,dtype=np.uint8)]); bits.tofile(fb)
    out=subprocess.run(["nice","-n","19","./maxunion2",blk,af,fb],capture_output=True,text=True).stdout
    mx=[l_ for l_ in out.splitlines() if l_.startswith("MAX")][0]
    dens=float(mx.split("density=")[1].split()[0]); nconf=float(out.split("configs=")[1].split()[0]); fx=float(out.split("fixed=")[1].split("(")[1].split(")")[0])
    results[d]={"U":dens,"configs":nconf,"F":fx,"allowed":[len(a) for a in allowed],"out":out}
    print(f"d={d:4d} gcd-constrained allowed counts {[len(a) for a in allowed]} F={fx:.4f} configs={nconf:.0f} U_d={dens:.6f}",flush=True)
json.dump(results,open("algsweep_%s.json"%("_".join(map(str,S))),"w"),indent=1)
print("max U_d over d:",max(r["U"] for r in results.values()),"at d =",max(results,key=lambda d:results[d]["U"]))
