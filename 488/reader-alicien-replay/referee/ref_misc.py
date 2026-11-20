# Misc checks: {2,3} value 49/40; Remark 8 for non-primitive pairs; Section 5 triples claim (9<=M<=18).
import numpy as np
from math import lcm
from fractions import Fraction
from itertools import combinations
def Bcum(A,N):
    cov=np.zeros(N+1,dtype=np.int8)
    for a in A: cov[a::a]=1
    return np.cumsum(cov,dtype=np.int64)
def suprat(A,span=3):
    M=max(A); L=lcm(*A); N=M+(span+1)*L; c=Bcum(A,N); W=int(c[L])
    r=c[1:]/np.arange(1,N+1); suf=np.maximum.accumulate(r[::-1])[::-1]
    ns=np.arange(M,M+span*L+1); ratio=np.maximum(suf[ns],W/L)/(c[ns]/ns)
    i=int(np.argmax(ratio)); n=int(ns[i])
    cand=max([Fraction(int(c[m]),m) for m in range(n+1,n+L+1)]+[Fraction(W,L)])
    return cand/Fraction(int(c[n]),n), n
print("{2,3}:",suprat((2,3)))
# Remark 8 read literally for non-primitive pairs (a|b): is B(n)/n > (1/a+1/b)/2 for n>=b ?
for A in [(3,6),(4,8),(5,10),(4,12)]:
    a,b=A; L=lcm(a,b); c=Bcum(A,b+3*L)
    fails=[n for n in range(b,b+3*L+1) if not Fraction(int(c[n]),n) > (Fraction(1,a)+Fraction(1,b))/2]
    print("Remark8 literal, nonprimitive",A,"first failures:",fails[:4])
# triples
bad=0
for M in range(9,19):
    best=(Fraction(0),None)
    for a,b in combinations(range(2,M),2):
        A=(a,b,M)
        if any(y%x==0 for x,y in combinations(A,2)): continue
        r,n=suprat(A)
        if r>best[0]: best=(r,(A,n))
    ok= best[1][0]==(M-2,M-1,M)
    bad+= not ok
    print(M,best[1],float(best[0]),"claim ok" if ok else "CLAIM FAILS")
print("triple mismatches:",bad)
