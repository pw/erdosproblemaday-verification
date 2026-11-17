"""Second route for the final arithmetic of Theorem D: enumerate every integer configuration the proof allows
(g, i*, s=|S'|, |S|, |P|) for delta in a rational grid, take the proof's worst-case h = i*+1+t with
t = ceil(max(0, g-(|P|+|S|-1)) / ceil(s/2)), and compare with ceil(2/delta)-1 and floor(2/delta)-1.
Exact rational arithmetic (fractions). Constraints used are exactly the ones the proof derives:
 g>=1; 1 <= i* <= floor(1/delta); |P| >= i*·delta·g; |S| >= delta·g; |P| >= |S| (P = i*S contains S, 0 in S);
 |P|+|S|-1 <= g; s >= delta·g, s >= 2 if g >= 2, s <= g. Control: replacing ceil(s/2) by 1 must break the bound."""
from fractions import Fraction as F
from math import ceil, floor
def worst(delta, G, growth=lambda s:(s+1)//2):
    best=(0,None)
    for g in range(1,G+1):
        for i in range(1, floor(1/delta)+1):
            if g==1:
                h=i+1
                if h>best[0]: best=(h,(g,i))
                continue
            Pmin=max(1,ceil(i*delta*g)); Smin=max(1,ceil(delta*g)); smin=max(2,ceil(delta*g))
            for S in range(Smin,g+1):
                for P in range(max(Pmin,S),g+2-S):
                    a=max(0,g-(P+S-1))
                    for s in range(smin,g+1):
                        t=0 if a==0 else -(-a//growth(s))
                        h=i+1+t
                        if h>best[0]: best=(h,(g,i,S,P,s))
                        break  # h is nonincreasing in s; smallest s is worst
    return best
viol=0; above_floor=[]; rows=0
deltas=sorted({F(p,q) for q in range(2,41) for p in range(1,q) if F(p,q)<=F(1,2)})
for d in deltas:
    G=int(ceil(2/d))+3   # g <= s/delta <= g/delta ... g/s<=1/delta and s<=g gives no cap; use a generous cap below
    G=max(G, 3*int(ceil(1/d))+6)
    h,cfg=worst(d,G)
    cb=ceil(2/d)-1; fb=floor(2/d)-1; rows+=1
    if h>cb: viol+=1; print("VIOLATION",d,h,cb,cfg)
    if h>fb: above_floor.append((str(d),h,fb,cfg))
print(f"deltas={rows} violations_of_ceil_bound={viol}  proof-bound exceeds floor shape at {len(above_floor)} deltas")
print("examples:",above_floor[:6])
# control: growth 1 per step (no Lemma 1) must exceed the ceil bound somewhere
c=0
for d in deltas[::7]:
    h,cfg=worst(d, max(int(ceil(2/d))+3, 3*int(ceil(1/d))+6), growth=lambda s:1)
    if h>ceil(2/d)-1: c+=1
print("control (growth 1): deltas exceeding ceil bound =",c,"of",len(deltas[::7]))
