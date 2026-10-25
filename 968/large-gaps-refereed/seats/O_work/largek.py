# Monte Carlo of w and v/lam for the Prop 4.2 family at large k (via (10),(11) structure, coupled paths over j),
# versus the paper's bounds (10) and (12).
import numpy as np, sys, time
from math import sqrt, floor
from common import *
lam=float(sys.argv[1]); logR=float(sys.argv[2]); ks=[int(float(x)) for x in sys.argv[3].split(',')]
beta,gamma=0.10,0.12
P=Profile(lam,logR); chi=chi_factory(beta,gamma); d=beta-P.mu; B=P.hi; s2=P.s2
print(f"lam={lam} logR={logR} mu_g={P.mu:.5f} d={d:.5f} B={B:.4g} s_g^2={s2:.4g}  2B/d={2*B/d:.3g}",flush=True)
ul=np.linspace(np.log(P.lo),np.log(P.hi),6001); uu=np.exp(ul); wu=np.full(uu.size,ul[1]-ul[0])*uu; wu[0]*=.5; wu[-1]*=.5
gu=P.g(uu); print("  check int g =",(gu*wu).sum()," sqrt(lam)=",sqrt(lam))
rng=np.random.default_rng(12345)
for k in ks:
    t0=time.time(); r=int(floor(sqrt(k))); a=k-r+1
    Sg=np.linspace(0,gamma+0.05,40001); Htab=np.array([(gu*wu*chi(s+uu/k)).sum() for s in Sg])
    H=lambda S: np.interp(S,Sg,Htab)
    reps=int(max(50,min(400,2e9/k)))
    W=[];V=[]
    jj=np.arange(a,k)            # interior j=a..k-1
    cj=np.sqrt((jj+1)/(lam*k))
    for rep in range(reps):
        tot=0.0; n=a-1
        while n>0:
            m=min(n,5_000_000); tot+=P.sample(rng,m).sum(); n-=m
        Sa1=tot/k
        inc=np.cumsum(P.sample(rng,r))/k     # S_a..S_k
        Sj=Sa1+inc                           # index 0 -> j=a, last -> j=k
        chiS=chi(Sj)
        W.append(np.mean(chiS**2))
        inter=chiS[:-1]-cj*H(Sj[:-1])
        V.append((np.sum(inter**2)+chiS[-1]**2+(a/(lam*k))*H(Sa1)**2)/r)
    W=np.array(W);V=np.array(V)
    v0=(np.sum((1-np.sqrt((jj+1)/k))**2)+1+a/k)/r
    lb_w=1-s2/(k*d*d); ub_v=2/r+(r/k)**2+4*s2/(k*d*d)
    print(f" k={k:.0e} r={r} reps={reps}: w={W.mean():.6f}±{W.std()/np.sqrt(reps):.1e} [paper LB (10): {lb_w:.4g}]  "
          f"v/lam={V.mean():.4e}±{V.std()/np.sqrt(reps):.1e} [cutoff-free value {v0:.4e}; paper UB (12): {ub_v:.4g}{'' if k>=2*B/d else ' (k<2B/d: UB not claimed)'}]  "
          f"v/w={V.mean()*lam/W.mean():.3e}  ({time.time()-t0:.0f}s)",flush=True)
