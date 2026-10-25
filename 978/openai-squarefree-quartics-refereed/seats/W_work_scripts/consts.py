# Euler-product density of squarefree values of n^4+2, n^4+1, n^4-2n^2+2 vs empirical counts, vs Carella's stated constants
from sympy import primerange
import math
def rho(coeffs, m):
    # count roots mod m of polynomial with integer coeffs (highest first)
    c=0
    for a in range(m):
        v=0
        for co in coeffs: v=(v*a+co)%m
        if v==0: c+=1
    return c
def euler(coeffs, P=20000):
    prod=1.0
    for p in primerange(2,P):
        if p*p<=200000:
            r=rho(coeffs,p*p)
        else:
            r=rho(coeffs,p)  # simple roots lift uniquely for p not dividing disc
        prod*=1-r/(p*p)
    return prod
def emp(f,N):
    import sympy
    # squarefree test via trial division by p^2 up to sqrt is expensive; use factorint for moderate N
    cnt=0
    from sympy import factorint
    for n in range(1,N+1):
        v=f(n)
        sq=True
        for p,e in factorint(v).items():
            if e>=2: sq=False;break
        if sq: cnt+=1
    return cnt/N
polys={'n^4+2':([1,0,0,0,2],lambda n:n**4+2,0.757159),'n^4+1':([1,0,0,0,1],lambda n:n**4+1,0.981003),'n^4-2n^2+2':([1,0,-2,0,2],lambda n:n**4-2*n*n+2,0.963802)}
for name,(co,f,car) in polys.items():
    e=euler(co)
    print(name,'Euler product (p<2e4) =',round(e,6),' Carella states',car, ' empirical n<=20000:',round(emp(f,20000),6))
