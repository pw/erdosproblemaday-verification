import numpy as np, math
N=3_000_001
lpf=np.ones(N+2,dtype=np.int64)  # largest prime factor
lpf[0]=0
for p in range(2,N+2):
    if lpf[p]==1:  # p prime (not yet marked)
        lpf[p::p]=p
lpf[1]=1
n=np.arange(2,N+1,dtype=np.float64)
P0=lpf[2:N+1].astype(np.float64); P1=lpf[3:N+2].astype(np.float64)
worst=0
for a,b in [(0.3,0.3),(0.5,0.5),(0.4,0.7),(0.7,0.2),(0.9,0.9),(0.55,0.35)]:
    weak=(P0<=n**a)&(P1<=n**b)
    strict=(P0<n**a)&(P1<(n+1)**b)
    for X in [10**4,10**5,10**6,3*10**6]:
        k=X-1
        A=int(strict[:k].sum()); B=int(weak[:k].sum())
        bound=math.floor(X**a)+math.floor((X+1)**b)
        ok=abs(A-B)<=bound
        worst=max(worst,abs(A-B)/X)
        if not ok: print('VIOLATION',a,b,X,A,B,bound)
    print(f"a={a} b={b} X=3e6: weak={B/ (3*10**6):.5f} strict={A/(3*10**6):.5f} |A-B|={abs(A-B)} bound={bound}")
inc=(P0<P1); dec=(P1<P0)
print('P(n)<P(n+1) density to 3e6:', inc.mean(), ' reverse:', dec.mean(), ' equal:', 1-inc.mean()-dec.mean())
print('max |A-B|/X', worst)
