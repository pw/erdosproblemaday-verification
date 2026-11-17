# Independent check of the proof's integer bookkeeping (both the ceil and the floor versions).
# For each m>=4 consider delta in (2/(m+1), 2/m]. Worst case over the proof's free parameters:
#   i* in [1, floor(1/delta)], g >= 1, |S| >= ceil(delta g) (>=1), |P| >= ceil(i* delta g), |P| >= |S| (optional),
#   s >= max(2, ceil(delta g)) when g>=2, |Y| = |P|+|S|-1 <= g, a = g-|Y|, t = ceil(a/ceil(s/2)), h = i*+1+t.
# Smaller |S|,|P|,s only increase h, so the worst case takes the minima. h is nonincreasing in delta (ceilings),
# so the sup over the interval is the right-limit delta -> 2/(m+1)+ ; we take delta = 2/(m+1) + 1e-15 exactly.
from fractions import Fraction as F
from math import ceil, floor
import sys
def cdiv(a,b): return -(-a//b)
def worst(delta, G, require_P_ge_S=True):
    best=(0,None)
    for i in range(1, floor(1/delta)+1):
        h=i+1
        if h>best[0]: best=(h,(1,i,'g=1'))
        for g in range(2, G+1):
            x=delta*g
            S=max(1,ceil(x)); P=ceil(i*x)
            if require_P_ge_S: P=max(P,S)
            s=max(2,ceil(x))
            Y=P+S-1
            if Y>g: continue          # impossible configuration under Kneser's equality
            a=g-Y
            t=cdiv(a,cdiv(s,2))
            h=i+1+t
            if h>best[0]: best=(h,(g,i,P,S,s,a,t))
    return best
eps=F(1,10**15)
viol_floor=0; viol_ceil=0; rows=[]
MMAX=int(sys.argv[1]) if len(sys.argv)>1 else 120
for m in range(4, MMAX+1):
    G=max(60, 12*(m+1))
    for label,delta in (("lim+",F(2,m+1)+eps),("2/m",F(2,m))):
        h,arg=worst(delta,G)
        h2,_=worst(delta,G,require_P_ge_S=False)
        fb=floor(2/delta)-1; cb=ceil(2/delta)-1
        if max(h,h2)>fb: viol_floor+=1; print("FLOOR VIOLATION",m,label,h,h2,fb,arg)
        if max(h,h2)>cb: viol_ceil+=1; print("CEIL VIOLATION",m,label,h,h2,cb,arg)
        if m<=12 or m%20==0: rows.append((m,label,h,h2,fb,cb,arg))
for r in rows: print(r)
print("m range 4..%d: floor violations=%d ceil violations=%d"%(MMAX,viol_floor,viol_ceil))
# control: replace growth ceil(s/2) by 1 (no Lemma 1) -> must exceed the floor bound somewhere
def worst_ctrl(delta,G):
    b=0
    for i in range(1, floor(1/delta)+1):
        for g in range(2,G+1):
            x=delta*g; S=max(1,ceil(x)); P=max(ceil(i*x),S); Y=P+S-1
            if Y>g: continue
            b=max(b,i+1+(g-Y))
    return b
c=sum(1 for m in range(4,40) if worst_ctrl(F(2,m+1)+eps,12*(m+1))>m-1)
print("control (growth 1 instead of ceil(s/2)): m in 4..39 exceeding floor bound:",c)
# control 2: drop the '+1' slack, i.e. pretend |Y| >= |P|+|S| - 2 : must break somewhere
def worst_ctrl2(delta,G):
    b=0
    for i in range(1, floor(1/delta)+1):
        for g in range(2,G+1):
            x=delta*g; S=max(1,ceil(x)); P=max(ceil(i*x),S); s=max(2,ceil(x)); Y=P+S-2
            if Y>g: continue
            a=max(0,g-Y); b=max(b,i+1+cdiv(a,cdiv(s,2)))
    return b
c2=sum(1 for m in range(4,40) if worst_ctrl2(F(2,m+1)+eps,12*(m+1))>m-1)
print("control2 (|Y|>=|P|+|S|-2): m in 4..39 exceeding floor bound:",c2)
