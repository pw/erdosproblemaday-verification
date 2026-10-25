import math, cmath, random
from math import gcd
from sympy import totient, factorint, mobius
def ram(d,h):
    return sum(cmath.exp(2j*math.pi*h*r/d) for r in range(1,d+1) if gcd(r,d)==1).real
bad=0
for j in range(1,13):
    for q in range(1,13):
        if any(e>1 for e in factorint(q).values()): continue
        d=j*q
        lhs=sum(ram(d,h)**2 for h in range(d) if gcd(h,q)==1)/totient(d)**2
        rhs= j/(totient(j)*totient(q)) if gcd(j,q)==1 else 0
        if abs(lhs-rhs)>1e-9: bad+=1; print("mismatch",j,q,lhs,rhs)
print("(8.12) mismatches:",bad)
# substitution identity: random rough-ish a,b,c,m with c|am+1, c|bm+1, a-b=jc
cnt=0
for _ in range(20000):
    c=random.randint(2,200); m=random.randint(1,10**4)
    if gcd(m,c)!=1: continue
    # choose a with c | am+1
    inv = pow(m,-1,c); a0 = (-inv)%c
    a = a0 + c*random.randint(1,50); b = a0 + c*random.randint(1,50)
    if a==b or a<=0 or b<=0: continue
    j=(a-b)//c; assert (a-b)%c==0
    la=(a*m+1)//c; lb=(b*m+1)//c
    assert (a*m+1)%c==0 and (b*m+1)%c==0
    assert b*la + j == a*lb
    cnt+=1
print("substitution identity checked",cnt)
# constants
h0=(1-math.log(2))/2
print("h0",h0,"2h0",2*h0,"1-6h0",1-6*h0,"1-5h0",1-5*h0,"2log2-1-h0",2*math.log(2)-1-h0)
print("kappa1+.04-.32",1-5*h0+.04-.32)
print("alpha0=1.6log2",1.6*math.log(2))
# singular series and its mean
def S(j):
    v=j/totient(j)
    for p in [p for p in range(2,2000) if all(p%k for k in range(2,int(p**.5)+1))]:
        if j%p: v*=1-1/(p-1)**2
    return v
T=2000
vals=[S(j) for j in range(1,T+1)]
print("mean S(j) j<=",T,sum(vals)/T, " S(1),S(2),S(4),S(6):",vals[0],vals[1],vals[3],vals[5])
