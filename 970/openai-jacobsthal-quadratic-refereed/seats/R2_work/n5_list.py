# N5: Prop 8.2 "fixed whole-box list" mechanics on a toy bin.
# (a) two distinct reduced rationals share at most log|A1D2-A2D1|/log R aligning primes (all pairs checked);
#     control: non-reduced duplicates (2A/2D vs A/D) have det 0 and share every aligning prime.
# (b) the Cauchy list-size bound M <= 2/c_p^2 once n_p >= 2C/c_p^2, on adversarial classes built to align many rationals.
import math, random
from math import gcd
def isp(n): return n>1 and all(n%q for q in range(2,int(n**.5)+1))
R=2000; P=[p for p in range(R,int(1.3*R)+1) if isp(p)]; n_p=len(P)
rnd=random.Random(5)
rats=[(A,D) for D in range(1,30) for A in range(-60,61) if gcd(A,D)==1]
# adversarial classes: 8 target rationals, each forced on a disjoint 1/8 of the primes
targets=rnd.sample(rats,8)
a={}
for i,p in enumerate(P):
    A,D=targets[i%8]; a[p]=(A*pow(D,-1,p))%p
def aligners(A,D): return frozenset(p for p in P if (D*a[p]-A)%p==0)
al={r:aligners(*r) for r in rats}
worst=0.0; viol=0
for i in range(len(rats)):
    A1,D1=rats[i]; s1=al[rats[i]]
    if not s1: continue
    for j in range(i+1,len(rats)):
        A2,D2=rats[j]; c=len(s1 & al[rats[j]])
        if c:
            det=abs(A1*D2-A2*D1); bound=math.log(det)/math.log(R)
            worst=max(worst,c/bound) if bound>0 else worst
            if c>bound+1e-9: viol+=1
print("n_p=%d rationals=%d | max common/bound ratio=%.3f violations=%d"%(n_p,len(rats),worst,viol))
A,D=targets[0]; print("control non-reduced (%d/%d vs %d/%d): det=%d, common aligning primes=%d"%(A,D,2*A,2*D,A*2*D-2*A*D,len(al[(A,D)])))
for cp in [0.05,0.1,0.12]:
    M=sum(1 for r in rats if len(al[r])>=cp*n_p)
    print("c_p=%.2f: list size M=%d  bound 2/c_p^2=%.0f"%(cp,M,2/cp**2))
