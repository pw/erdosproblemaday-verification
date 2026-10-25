# Literal check of w and v (Prop 3.1 definitions) for the Prop 4.2 family at k=4 (r=2, a=3),
# by deterministic tensor quadrature, versus the closed-form route (10)/(11).
import numpy as np, sys
from math import sqrt, exp
from common import *
lam=float(sys.argv[1]); logR=float(sys.argv[2]); beta,gamma=0.10,0.12
P=Profile(lam,logR); chi=chi_factory(beta,gamma)
k=4; r=int(np.floor(np.sqrt(k))); a=k-r+1
print("lam",lam,"logR",logR,"mu_g",P.mu,"supp",P.lo,P.hi,"k",k,"r",r,"a",a)
al=lambda j: exp(log_alpha(lam,j))
# 1-D grid for each coordinate t in [lo/k, gamma] (f vanishes beyond gamma since all t>0 and chi(S)=0 for S>=gamma)
n=int(sys.argv[3]) if len(sys.argv)>3 else 70
tl=np.log(P.lo/k); th=np.log(gamma)
xs=np.linspace(tl,th,n); ts=np.exp(xs); wts=np.full(n,xs[1]-xs[0])*ts; wts[0]*=.5; wts[-1]*=.5
gk=P.g(k*ts)            # g(k t)
# inner integral for T: int_0^inf g(k u) chi(S+u) du, done on its own fine log-grid
ul=np.linspace(np.log(P.lo/k),np.log(P.hi/k),4001); uu=np.exp(ul); wu=np.full(uu.size,ul[1]-ul[0])*uu; wu[0]*=.5; wu[-1]*=.5
gu=P.g(k*uu)
Sgrid=np.linspace(0,gamma+0.02,20001)
Ttab=np.array([(gu*wu*chi(s+uu)).sum() for s in Sgrid])
def Tint(S): # S array -> int g(ku) chi(S+u) du  (tabulated in S; integrand depends on t only via S)
    return np.interp(np.asarray(S,float),Sgrid,Ttab)
def fcoef(j): return (-1)**j/(sqrt(r)*sqrt(al(j)))
def Q(j,grids): # k^{j/2} prod g(k t_i) on tensor grid (list of 1D arrays broadcast)
    out=k**(j/2)
    for gg in grids: out=out*gg
    return out
def mesh(j):
    sh=[n]*j; G=[];W=1.0;S=0.0
    for i in range(j):
        s=[1]*j; s[i]=n
        G.append(gk.reshape(s)); W=W*wts.reshape(s); S=S+ts.reshape(s)
    return G,W,S
# f_j on grid (j>=a), T f_{j+1} on grid
def f(j,G,S): return fcoef(j)*Q(j,G)*chi(S) if a<=j<=k else 0.0
def Tf(jp1,G,S): # T f_{j+1}(t) = fcoef(j+1) * k^{(j+1)/2} prod g(k t_i) * int g(k u) chi(S+u) du
    if not (a<=jp1<=k): return 0.0
    return fcoef(jp1)*Q(jp1-1,G)*k**0.5*Tint(S)
w=0.0; v=0.0
for j in range(0,k+1):
    if j==0:
        fj=0.0; T=Tf(1,[],np.array(0.0)) if a<=1 else 0.0
        v+=al(0)*(fj+T)**2; continue
    G,W,S=mesh(j)
    fj=f(j,G,S); T=Tf(j+1,G,S)
    w+=al(j)*np.sum(W*np.asarray(fj)**2) if a<=j<=k else 0.0
    v+=al(j)*np.sum(W*np.asarray(fj+T)**2*np.ones_like(W))
v*=lam
print("LITERAL  w=%.6f  v=%.6f  v/lam=%.6f"%(w,v,v/lam))
# closed-form route via (10)/(11) with Monte Carlo over Q_j^2 (independent sampler)
rng=np.random.default_rng(1); N=2_000_000
U=P.sample(rng,(N,k))/k; Sc=np.cumsum(U,axis=1)
def H(S): return Tint(S)*k   # int g(u) chi(S+u/k) du = k * int g(k u') chi(S+u') du'
w2=np.mean(sum(chi(Sc[:,j-1])**2 for j in range(a,k+1)))/r
vv=0.0
for j in range(a,k):
    Sj=Sc[:,j-1]; br=chi(Sj)-np.sqrt((j+1)/(lam*k))*H(Sj); vv+=np.mean(br**2)/r
vv+=np.mean(chi(Sc[:,k-1])**2)/r
Sa1=Sc[:,a-2] if a>=2 else np.zeros(N)
vv+=(a/(lam*k))*np.mean(H(Sa1)**2)/r
print("FORMULA  w=%.6f  v/lam=%.6f   (MC N=%d)"%(w2,vv,N))
