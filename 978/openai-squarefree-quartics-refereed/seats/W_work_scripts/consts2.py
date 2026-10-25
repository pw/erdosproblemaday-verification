from sympy import primerange, factorint
def rho(co,m):
    c=0
    for a in range(m):
        v=0
        for x in co: v=(v*a+x)%m
        if v==0:c+=1
    return c
def euler(co,P=20000):
    pr=1.0
    for p in primerange(2,P):
        r=rho(co,p*p) if p<450 else rho(co,p)
        pr*=1-r/(p*p)
    return pr
co=[1,0,-1,0,2]
print('n^4-n^2+2 Euler',round(euler(co),6))
c=0;N=20000
for n in range(1,N+1):
    if all(e<2 for e in factorint(n**4-n*n+2).values()): c+=1
print('empirical',c/N)
