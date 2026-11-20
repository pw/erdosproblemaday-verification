# Check Section 5 claim: over primitive pairs with max A = M (4<=M<=35), max sup ratio = (2M-3)^2/(2(M-1)^2) at {M-1,M}.
import numpy as np
from math import lcm
from fractions import Fraction
def Bcum(A,N):
    cov=np.zeros(N+1,dtype=np.int8)
    for a in A: cov[a::a]=1
    return np.cumsum(cov,dtype=np.int64)
bad=0
for M in range(4,36):
    best=(0,None)
    for a in range(2,M):
        if M%a==0: continue
        A=(a,M); L=lcm(a,M); N=M+4*L; c=Bcum(A,N); W=int(c[L])
        r=c[1:]/np.arange(1,N+1); suf=np.maximum.accumulate(r[::-1])[::-1]
        ns=np.arange(M,M+3*L+1); ratio=np.maximum(suf[ns],W/L)/(c[ns]/ns)
        i=int(np.argmax(ratio))
        if ratio[i]>best[0]+1e-12: best=(ratio[i],(a,int(ns[i])))
    f=(2*M-3)**2/(2*(M-1)**2)
    ok=abs(best[0]-f)<1e-9 and best[1][0]==M-1
    bad+=not ok
    if not ok or M in (4,5,10,35): print(M,best,f,ok)
print("Section5 mismatches:",bad)
