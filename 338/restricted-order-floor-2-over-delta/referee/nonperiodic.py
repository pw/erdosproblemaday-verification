# Sanity: exact restricted order (max over [N/2,N]) for a few non-periodic sets vs floor(2/delta)-1.
import numpy as np, math, random
from intdp import min_distinct
N=30000
def report(name,A):
    A=sorted(a for a in A if 1<=a<=N)
    # lower density proxy: min over x in [N/10,N] of A(x)/x
    cnt=np.zeros(N+1,dtype=np.int64); cnt[A]=1; cum=np.cumsum(cnt)
    xs=np.arange(N//10,N+1); dens=(cum[xs]/xs).min()
    c=min_distinct(set(A),N); w=c[N//2:].max()
    print(f"{name}: density~{dens:.4f} exact max order on [N/2,N]={w}  floor bound={math.floor(2/dens)-1}")
alpha=(5**0.5-1)/2
report("Bohr {n alpha}<0.3",[n for n in range(1,N+1) if (n*alpha)%1<0.3])
report("0,1 mod 5 x Bohr 1/2",[n for n in range(1,N+1) if n%5 in (0,1) and ((n//5)*alpha)%1<0.5])
random.seed(1)
report("random p=0.22",[n for n in range(1,N+1) if random.random()<0.22])
report("0 mod 4 full + 1 mod 4 Bohr 1/3",[n for n in range(1,N+1) if n%4==0 or (n%4==1 and ((n//4)*alpha)%1<1/3)])
