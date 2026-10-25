import sys,random
sys.path.insert(0, sys.argv[1])
from local_spot import solve
from fractions import Fraction as F
def divisors(n):
    ds=[1];m=n;p=2
    fac={}
    while p*p<=m:
        while m%p==0: fac[p]=fac.get(p,0)+1; m//=p
        p+=1
    if m>1: fac[m]=fac.get(m,0)+1
    for p,e in fac.items(): ds=[d*p**k for d in ds for k in range(e+1)]
    return ds
random.seed(7); mism=0; found=0
for _ in range(3000):
    xs=random.sample(range(18,400),random.choice([2,2,3]))
    s=sum(F(1,x) for x in xs); a,b=s.numerator,s.denominator
    forb=set(random.sample(range(18,400),15))
    # oracle: all (x,y), x<y, x>=18, (ax-b)(ay-b)=b^2
    sols=[]
    for q in divisors(b*b):
        if (b+q)%a==0 and (b+b*b//q)%a==0:
            x=(b+q)//a; y=(b+b*b//q)//a
            if x<y and x>=18 and x not in forb and y not in forb: sols.append((x,y))
    got=solve(a,b,2,18,forb)
    if bool(got)!=bool(sols): mism+=1; print("MISMATCH",xs,forb,got,sols)
    if sols: found+=1
print("two-term oracle: cases=3000 with-solution=",found,"mismatches=",mism)
