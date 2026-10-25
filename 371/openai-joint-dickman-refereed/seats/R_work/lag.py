import numpy as np
from sympy import primerange, factorint
J=20000
primes=list(primerange(2,200000))
# S(j) = j/phi(j) * prod_{p not| j}(1-1/(p-1)^2)
logC = sum(np.log(1-1/(p-1)**2) for p in primes if p>2)  # all p>2 factor
S=np.zeros(J+1); fac={}
for j in range(1,J+1):
    f=factorint(j); fac[j]=f
    if 2 not in f: S[j]=0; continue
    v=1.0
    for p in f: v*= p/(p-1)
    lp=logC - sum(np.log(1-1/(p-1)**2) for p in f if p>2)
    S[j]=v*np.exp(lp)
def SP(j,P1):
    f=fac[j]; v=1.0
    for p in primerange(2,P1+1):
        if p in f: v*=1/(1-1/p)
        else: v*=1-1/(p-1)**2
    return v
for P1 in [3,7,13,31,101]:
    d=np.array([abs(S[j]-SP(j,P1)) for j in range(1,J+1)])
    cs=np.cumsum(d)/np.arange(1,J+1)
    print(P1, "sup_T<=%d mean|S-S_P1| ="%J, cs.max(), " at T=",cs.argmax()+1, " mean up to J:",cs[-1])
print("mean S up to J:", S[1:].mean())
