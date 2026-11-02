# My own (host) check of the two explicit finite ranges, decorrelated from seat A.
# Prop 7.2: Upsilon(n) = sum_{2<=m<=n, P+(m)^2<=n} log(m+1) <= (1-log2) n log n + 1.5 n for integers 2<=n<=N2.
# Prop 7.1: Lambda(x) = sum_{p<P(x)} log((p-1)!) >= x/2 - 3x/log x for 40 <= x < e^20 (step fn: test sup of RHS on each step).
import math, sys
import numpy as np
N2=int(sys.argv[1]) if len(sys.argv)>1 else 400000
# largest prime factor sieve
lpf=np.zeros(N2+1,dtype=np.int64)
for p in range(2,N2+1):
    if lpf[p]==0:
        lpf[p::p]=p   # overwritten by larger primes later => ends as largest prime factor
# Upsilon(n): m contributes for n >= max(m, P+(m)^2)
start=np.maximum(np.arange(N2+1), lpf*lpf)
add=np.zeros(N2+2)
for m in range(2,N2+1):
    s=start[m]
    if s<=N2: add[s]+=math.log(m+1)
U=np.cumsum(add)
worst=(None,-1e9)
c=1-math.log(2)
viol=0
for n in range(2,N2+1):
    rhs=c*n*math.log(n)+1.5*n
    if U[n]>rhs: viol+=1
    r=U[n]-c*n*math.log(n)
    if r/n>worst[1]: worst=(n,r/n)
print(f"Prop7.2 integers 2..{N2}: violations={viol}; max (Upsilon-(1-log2)n log n)/n = {worst[1]:.4f} at n={worst[0]}")
# control: Upsilon(12) by hand = log of prod over {2,3,4,6,8,9,12} (3-smooth? no: sqrt(12)=3.46 -> P+<=3) of (m+1)
hand=sum(math.log(m+1) for m in (2,3,4,6,8,9,12))
print("control Upsilon(12)",U[12],"hand",hand)
# Prop 7.1
X=math.exp(20)
ymax=int(math.isqrt(int(4*X+9)))//2+10
sv=np.ones(ymax+1,dtype=bool); sv[:2]=False
for i in range(2,int(ymax**0.5)+1):
    if sv[i]: sv[i*i::i]=False
pr=[int(p) for p in np.nonzero(sv)[0]]
lf=[math.lgamma(p) for p in pr]   # log((p-1)!)
# Lambda on [P(P+3), P'(P'+3)) = sum_{p<P} log((p-1)!)
cum=0.0; worst=(None,1e9); viol=0
f=lambda x: x/2-3*x/math.log(x)
for k in range(len(pr)-1):
    P,Pn=pr[k],pr[k+1]
    lo,hi=P*(P+3),Pn*(Pn+3)
    if hi<=40: cum+=lf[k]; continue
    if lo>X: break
    a=max(lo,40); b=min(hi,X)
    # f increasing for x>e^3; sup on [a,b) -> value at b
    m=cum-f(b)
    if m<0: viol+=1
    if m/b<worst[1]: worst=(b,m/b)
    cum+=lf[k]
print(f"Prop7.1 40<=x<e^20: violations={viol}; min (Lambda-RHS)/x = {worst[1]:.5f} near x={worst[0]}")
# control: x=40 -> P=5, Lambda = log(1!)+log(2!) = log 2
