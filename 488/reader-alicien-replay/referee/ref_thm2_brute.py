# Brute-force Theorem 2 (|A|<=2) and Remark 8 using exact periodic structure. Referee scratch.
# For n in [maxA, maxA+3L], sup_{m>n} B(m)/m = max( max_{n<m<=N} B(m)/m , W/L ) with N >= n+L (periodicity),
# where W = B(L); the limit W/L is approached but attained only if some B(m)/m equals it.
import numpy as np, sys
from math import lcm, gcd
from fractions import Fraction
MAXB=int(sys.argv[1]) if len(sys.argv)>1 else 150
def Bcum(A,N):
    cov=np.zeros(N+1,dtype=np.int8)
    for a in A: cov[a::a]=1
    c=np.cumsum(cov,dtype=np.int64); return c
best=(0,None); worst_strict=[]; r8_fail=0; r8_min=(9,None); count=0; viol=0
sets=[(a,) for a in range(2,MAXB+1)]+[(a,b) for b in range(3,MAXB+1) for a in range(2,b)]
for A in sets:
    M=max(A); L=lcm(*A); N=M+4*L
    c=Bcum(A,N); W=int(c[L])
    m_idx=np.arange(1,N+1); r=c[1:]/m_idx            # r[k-1]=B(k)/k
    # suffix max over m in (n, N]
    suf=np.maximum.accumulate(r[::-1])[::-1]         # suf[k-1]=max_{m>=k} r
    ns=np.arange(M,M+3*L+1)
    supm=np.maximum(suf[ns], W/L)                    # suf[ns] = max_{m>=n+1}
    rn=c[ns]/ns
    ratio=supm/rn
    i=int(np.argmax(ratio)); count+=1
    if ratio[i]>best[0]: best=(float(ratio[i]),(A,int(ns[i])))
    if ratio[i]>=2-1e-12: viol+=1; print("VIOLATION/near",A,ns[i],ratio[i])
    if len(A)==2 and A[1]%A[0]:
        a,b=A; u=L//b; v=L//a
        ok=(2*c[ns]*L > ns*(u+v))
        if not ok.all(): r8_fail+=1; print("Remark8 fail",A,ns[~ok][:5])
        q=(2*c[ns]*L)/(ns*(u+v)); j=int(np.argmin(q))
        if q[j]<r8_min[0]: r8_min=(float(q[j]),(A,int(ns[j])))
print(f"sets checked={count} (all |A|<=2 with max<= {MAXB}); max sup ratio={best[0]:.6f} at A,n={best[1]}; near-violations={viol}")
print(f"Remark 8 (primitive pairs): failures={r8_fail}; min of 2B(n)L/(n(u+v)) = {r8_min[0]:.6f} at {r8_min[1]}")
# exact recheck of the best
(A,n)=best[1]; L=lcm(*A); c=Bcum(A,n+L+1); W=int(c[L])
cand=max([Fraction(int(c[m]),m) for m in range(n+1,n+L+1)]+[Fraction(W,L)])
print("exact best:",A,n,"sup B(m)/m =",cand,"B(n)/n =",Fraction(int(c[n]),n),"ratio =",cand/Fraction(int(c[n]),n), "=", float(cand/Fraction(int(c[n]),n)))
