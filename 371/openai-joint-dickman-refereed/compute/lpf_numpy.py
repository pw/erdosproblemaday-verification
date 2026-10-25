# Independent second instrument: largest prime factor by ascending-prime OVERWRITE (lpf[p::p] = p for every prime p <= N+1),
# no division at all; counts inc/dec at checkpoints; joint counts at a grid of (a,b) by exact integer comparison
# P(n) <= n^a  <=>  log P(n) <= a log n done in float64 with a tolerance flag for near-boundary cases.
import numpy as np, sys
N=int(sys.argv[1]); M=N+2
lpf=np.ones(M,dtype=np.int64)
isc=np.ones(M,dtype=bool); isc[:2]=False
for i in range(2,int(M**0.5)+1):
    if isc[i]: isc[i*i::i]=False
ps=np.nonzero(isc)[0]
for p in ps: lpf[p::p]=p
n=np.arange(2,N+1); a=lpf[2:N+1]; b=lpf[3:N+2]
inc=np.cumsum(a<b); dec=np.cumsum(b<a)
for X in [10**k*m for k in range(1,12) for m in (1,2,5) if 10**k*m<=N]:
    print(f"CP X={X} inc={inc[X-2]} dec={dec[X-2]}")
ln=np.log(n.astype(np.float64)); u=np.log(a.astype(np.float64))/ln; v=np.log(b.astype(np.float64))/ln
for A in (0.2,0.3,0.5,0.7):
    for B in (0.2,0.3,0.5,0.7):
        print(f"JOINT X={N} a={A} b={B} count={int(np.count_nonzero((u<=A+1e-12)&(v<=B+1e-12)))} near_boundary={int(np.count_nonzero((np.abs(u-A)<1e-9)|(np.abs(v-B)<1e-9)))}")
