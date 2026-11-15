from fractions import Fraction as F
from math import gcd, floor, ceil
worst=[];cnt=0
for p in range(1,14):
    for mask in range(1,1<<p):
        S=[r for r in range(p) if mask>>r&1]
        d=F(len(S),p)
        if d>F(1,2): continue
        g=0
        for r in S: g=gcd(g,r)
        if gcd(g,p)!=1: continue   # generate Z/p (=> every modulus condition for periodic? approx)
        # min t>=1 with r in tS
        reach={r:1 for r in S}; frontier=set(S); t=1
        while len(reach)<p:
            t+=1; new=set()
            for x in frontier:
                for s in S:
                    y=(x+s)%p
                    if y not in reach: reach[y]=t; new.add(y)
            frontier=set(reach)  # all sums of <=t? need exact t; use sets of exactly t
        # recompute properly: exact t-fold sums
        cur=set(S); best={r:1 for r in S}; t=1
        while len(best)<p:
            t+=1; cur={(x+s)%p for x in cur for s in S}
            for y in cur: best.setdefault(y,t)
        ro=max(best.values()); cnt+=1
        lo=floor(1/(d/2))-1  # floor(2/d)-1
        if ro>lo: worst.append((p,S,str(d),ro,lo))
        if ro>4*ceil(1/d)-4: print("EXCEEDS C",p,S,ro)
print(cnt,"sets; beating floor(2/d)-1:",len(worst)); print(worst[:20])
