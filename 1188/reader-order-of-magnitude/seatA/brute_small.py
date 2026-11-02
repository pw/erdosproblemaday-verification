# direct-definition brute force for small x (independent of the bucket/cumsum code)
import math
from fractions import Fraction
def lpf(n):
    p=1; d=2
    while d*d<=n:
        while n%d==0: p=d; n//=d
        d+=1
    return max(p,n) if n>1 else p
def isprime(n): return n>1 and all(n%d for d in range(2,math.isqrt(n)+1))
c=1-math.log(2); worst=(-9,0)
for x in range(2,3001):
    S=[n for n in range(2,x+1) if lpf(n)**2<=x]
    U=math.fsum(math.log(n+1) for n in S)
    r=(U-c*x*math.log(x))/x
    assert r<=1.5
    if r>worst[0]: worst=(r,x)
print("Upsilon direct, 2<=x<=3000: max ratio %.6f at x=%d"%worst)
print("S_50 =",[n for n in range(2,51) if lpf(n)**2<=50])
# Lambda direct with exact integer factorials, 40<=x<=3000
worst=(-9,0)
for x in range(40,3001):
    P=max(p for p in range(2,x) if isprime(p) and p*(p+3)<=x)
    prod=1
    for p in range(2,P):
        if isprime(p): prod*=math.factorial(p-1)
    lam=math.log(prod)
    assert lam >= x/2-3*x/math.log(x), x
    if x>=404:
        g=(x/2-lam)*math.log(x)/x
        if g>worst[0]: worst=(g,x)
print("Lambda direct (exact factorials), 40<=x<=3000: no violation; worst normalised gap %.4f at x=%d"%worst)
