"""Wider second route: same constraint system as proof_arith_check.py but closed-form worst case per (g, i*)
(smallest |S|, |P|, s are worst), delta = p/q for q <= 60, g up to 60/delta. Checks the integer form
h <= floor(2/delta) - 1 (Theorem D, integer bookkeeping) and reports the tightest cases."""
from fractions import Fraction as F
from math import ceil, floor
viol=0; tight=0; n=0
for q in range(2,61):
    for p in range(1,q):
        d=F(p,q)
        if d>F(1,2) or F(p,q).denominator!=q: continue
        n+=1; target=floor(2/d)-1; worst=0
        for g in range(1,int(60/d)+2):
            for i in range(1,floor(1/d)+1):
                if g==1: h=i+1
                else:
                    e=ceil(d*g); S=max(1,e); P=max(ceil(i*d*g),S); s=max(2,e)
                    a=max(0,g-(P+S-1)); h=i+1+(0 if a==0 else -(-a//((s+1)//2)))
                worst=max(worst,h)
        if worst>target: viol+=1; print("VIOLATION",d,worst,target)
        if worst==target: tight+=1
print(f"deltas={n} violations_of_floor(2/delta)-1={viol} deltas_where_proof_bound_equals_it={tight}")
