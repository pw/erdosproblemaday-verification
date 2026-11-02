# Host's exact check of the paper's explicit examples (Example 3.3, 4.4 all 6720 paddings, 4.5 depth-two tree),
# built from the CONSTRUCTION RULES (not copied residues), then compared with the residues printed in the paper.
import numpy as np, itertools, math, sys
from math import lcm
def crt(conds):
    a,m=0,1
    for r,n in conds:
        g=math.gcd(m,n); assert (r-a)%g==0
        l=m//g*n; t=((r-a)//g*pow(m//g,-1,n//g))%(n//g); a=(a+m*t)%l; m=l
    return a,m
def check(classes,L=None):
    mods=[n for a,n in classes]
    assert len(set(mods))==len(mods), "moduli not distinct"
    L=L or lcm(*mods)
    for n in mods: assert L%n==0
    cnt=np.zeros(L,dtype=np.int16)
    for a,n in classes: cnt[a%n::n]+=1
    cover=bool(cnt.min()>=1)
    priv=[bool((cnt[a%n::n]==1).any()) for a,n in classes]
    return cover, all(priv), L
pos=[(0,2),(0,3),(1,4),(5,6),(7,12)]
print("CONTROL+ classical:",check(pos))
print("CONTROL- +3 mod 8:",check(pos+[(3,8)]))
print("CONTROL- drop 7 mod 12:",check(pos[:-1]))
def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def isprime(n): return n>1 and all(n%k for k in range(2,int(n**.5)+1))
def build(P,I,x,split,tau,order):
    """split: dict (q,u) -> list of (I-part e, residue r mod e, padding) leaves. order: levels list for iota."""
    FPP=[q for q in range(2,P) if any(q==j**k for j in range(2,q+1) if isprime(j) and j not in I for k in range(1,20))]
    jq=lambda q: next(j for j in range(2,q+1) if isprime(j) and q%j==0)
    MF=lambda m: lcm(1,*[q for q in FPP if q<m])
    assert FPP==order,(FPP,order)
    cl=[]
    for q in FPP:
        j=jq(q); qo=q//j
        adm=[d for d in divisors(MF(q)) if d%j and q*d<=x]
        for u in range(1,j):
            if (q,u) in split:
                for e,r,s in split[(q,u)]:
                    assert MF(q)%s==0 and s%j
                    cl.append(crt([(qo*u,q),(r,e),(0,s)]))
            else:
                s=adm[u-1]; cl.append(crt([(qo*u,q),(0,s)]))
    iota={q:i+1 for i,q in enumerate(order)}
    assert tau[0]==1 and all(tau[iota[q]]==q for q in FPP)
    for t in range(P):
        assert MF(P)%tau[t]==0; cl.append(crt([(t,P),(0,tau[t])]))
    assert max(n for a,n in cl)<=x, max(n for a,n in cl)
    return cl
# Example 3.3 (printed system)
ex33=[(1,2),(1,3),(2,6),(2,4),(0,5),(6,10),(12,15),(8,20),(24,30)]
print("Ex3.3 printed:",check(ex33))
# Example 4.4: P=13, I={5}, x=600, split (11,1) by 5 with paddings 1,2,3,4,6
tau44=[1,2,3,4,7,8,9,11,6,12,14,18,21]
sp={(11,1):[(5,v,s) for v,s in zip(range(5),[1,2,3,4,6])]}
S=build(13,{5},600,sp,tau44,[2,3,4,7,8,9,11])
print("Ex4.4 built:",len(S),"classes, max modulus",max(n for a,n in S),check(S,360360))
printed=[(45,55),(56,110),(12,165),(188,220),(144,330)]
print("Ex4.4 split classes match printed:", all(c in S for c in printed))
# all 6720 paddings
pool=[d for d in divisors(504) if d<=600//55 and d%11]
print("pool",pool)
base=[c for c in S if c not in printed]
L=360360; cnt0=np.zeros(L,dtype=np.int16)
for a,n in base: cnt0[a::n]+=1
ok=0; systems=set(); nall=0
for perm in itertools.permutations(pool,5):
    nall+=1
    sc=[crt([(1,11),(v,5),(0,s)]) for v,s in zip(range(5),perm)]
    cl=base+sc
    assert len({n for a,n in cl})==len(cl)
    cnt=cnt0.copy()
    for a,n in sc: cnt[a::n]+=1
    if cnt.min()>=1 and all((cnt[a::n]==1).any() for a,n in cl): ok+=1
    systems.add(frozenset(cl))
print(f"Ex4.4 all paddings: {ok}/{nall} minimal distinct coverings; distinct systems {len(systems)}")
# Example 4.5: P=13, I={5,7}, x=2310; root of T(11,1) label 7; child 0 label 5
tau45=[1,2,3,4,8,9,11,6,12,18,22,24,33]
leaves=[(7,v,s) for v,s in zip(range(1,7),[1,2,3,4,6,8])]+[(35,crt([(0,7),(w,5)])[0],s) for w,s in zip(range(5),[1,2,3,4,6])]
S5=build(13,{5,7},2310,{(11,1):leaves},tau45,[2,3,4,8,9,11])
pr45=[(1,77),(100,154),(45,231),(144,308),(12,462),(496,616),(210,385),(56,770),(672,1155),(1288,1540),(1134,2310)]
print("Ex4.5 built:",len(S5),"classes, max modulus",max(n for a,n in S5),check(S5,360360))
print("Ex4.5 split classes match printed:", all(c in S5 for c in pr45))
b5=[c for c in S5 if c not in pr45[6:]]
c0=np.zeros(L,dtype=np.int16)
for a,n in b5: c0[a::n]+=1
ok=0;n120=0
for perm in itertools.permutations([1,2,3,4,6]):
    n120+=1
    sc=[crt([(1,11),(0,7),(w,5),(0,s)]) for w,s in zip(range(5),perm)]
    cl=b5+sc; cnt=c0.copy()
    for a,n in sc: cnt[a::n]+=1
    if len({n for a,n in cl})==len(cl) and cnt.min()>=1 and all((cnt[a::n]==1).any() for a,n in cl): ok+=1
print(f"Ex4.5 all 120 orderings of the I-part-35 group: {ok}/{n120}")
