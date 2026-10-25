import sys
from functools import lru_cache
def factor(n):
    f={};d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1 if d==2 else 2
    if n>1: f[n]=f.get(n,0)+1
    return f
def divisors(n):
    ds=[1]
    for p,e in factor(n).items():
        ds=[d*p**k for d in ds for k in range(e+1)]
    return sorted(ds)
def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1;s=0
    while d%2==0: d//=2;s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def minphi(m):
    primes=sorted(d+1 for d in divisors(m) if isprime(d+1))
    @lru_cache(None)
    def rec(m,i):
        # least n with phi(n)=m using primes from primes[i:] (each prime at most once), largest-first order irrelevant
        if m==1: return 1
        best=None
        for j in range(i,len(primes)):
            p=primes[j]
            if (p-1)>m: break
            if m%(p-1): continue
            q=m//(p-1); pk=p
            while True:
                r=rec(q,j+1)
                if r is not None:
                    c=pk*r
                    if best is None or c<best: best=c
                if q%p: break
                q//=p; pk*=p
        return best
    return rec(m,0)
for a in map(int,sys.argv[1:]):
    l=minphi(a); print(a, l, factor(l) if l else None, (l/a if l else None))
