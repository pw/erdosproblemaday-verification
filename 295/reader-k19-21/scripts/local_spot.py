#!/usr/bin/env python3
"""Our own r->(r-1) local replacement search (written from scratch) to spot-check Bae's surgery logs.
Question per case: given reference A and removed S (|S|=r), do r-1 distinct integers >=18, none in A\\S
(re-using removed ones allowed), sum to sum(1/S)?  Usage: local_spot.py r nsample seed [fixed comma list]"""
import sys, random, itertools
from fractions import Fraction as F
from math import gcd, isqrt
A=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,43,44,45,46,48,50,52,54,63,275,14143068,10457416992]
def solve(a,b,t,d,forb):
    # find t distinct ints >= d, not in forb, increasing, summing to a/b
    if t==1:
        return (b//a,) if b%a==0 and b//a>=d and b//a not in forb else None
    x=max(d,b//a+1)
    while x*a < t*b:                        # need 1/x > a/(t b)
        if x not in forb:
            if t==2:
                # (ax-b)(ay-b)=b^2 with x<y  =>  ax-b < b  (already) ; test directly
                num=b*x; den=a*x-b
                if num%den==0 and num//den>x and num//den not in forb: return (x,num//den)
                # quadratic necessary condition: x^2 - a x + b >= 0 ; once a^2>4b and x passed small root, no more solutions
                if a*a>4*b and x*x-a*x+b<0: return None
            else:
                # optimistic bound: t smallest allowed >= x
                s=F(0);k=0;z=x
                while k<t:
                    if z not in forb: s+=F(1,z);k+=1
                    z+=1
                if s < F(a,b): return None
                aa,bb=a*x-b,b*x;g=gcd(aa,bb)
                r=solve(aa//g,bb//g,t-1,x+1,forb)
                if r: return (x,)+r
        x+=1
    return None
def case(S, ref=A):
    forb=set(ref)-set(S); s=sum((F(1,x) for x in S),F(0))
    return solve(s.numerator,s.denominator,len(S)-1,18,forb)
if __name__=='__main__':
    # positive controls: must FIND replacements
    OURS35=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,42,43,44,45,48,50,52,54,63,640,337280,1735650,68479214496]
    pc1=case([42,640,337280,1735650,68479214496],OURS35); print("posctl our35 5->4:",pc1)
    pc2=case([18,19],A+[]) ; print("posctl 2->1 {18,19}? (expect None: 1/18+1/19 not unit)",pc2)
    pc3=case([20,30],A); print("posctl 2->1 {20,30} -> 1/12:",pc3)   # 1/20+1/30=1/12, 12<18 so expect None
    pc4=case([30,45,63],A); print("posctl 3->2 {30,45,63}:",pc4)
    assert pc1 is not None and sum(F(1,x) for x in pc1)==F(1,42)+F(1,640)+F(1,337280)+F(1,1735650)+F(1,68479214496)
    r,n,seed=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    fixed=[int(x) for x in sys.argv[4].split(',')] if len(sys.argv)>4 else []
    pool=[x for x in A if x not in fixed]
    allc=list(itertools.combinations(pool,r-len(fixed)))
    random.seed(seed); samp=random.sample(allc,min(n,len(allc)))
    found=0
    for c in samp:
        res=case(list(c)+fixed)
        if res: found+=1; print("WITNESS",sorted(list(c)+fixed),res)
    print(f"r={r} fixed={fixed} family={len(allc)} sampled={len(samp)} witnesses={found}")
