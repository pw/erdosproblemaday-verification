import numpy as np
from math import lgamma, log, exp, sqrt
def sstep(x):
    x=np.asarray(x,float); out=np.zeros_like(x)
    m=(x>0)&(x<1); a=np.exp(-1/x[m]); b=np.exp(-1/(1-x[m])); out[m]=a/(a+b); out[x>=1]=1.0
    return out
def phi(u,R): return (1/u)*sstep((u-0.5)/0.5)*(1-sstep((u-R)/R))
class Profile:
    """g from Lemma 4.1 for given lam, logR (explicit smooth phi_R)."""
    def __init__(self,lam,logR,n=200001):
        self.lam=lam; R=float(np.exp(logR)); self.R=R
        x=np.linspace(np.log(0.5),np.log(2*R),n); u=np.exp(x); p=phi(u,R)
        w=np.full(n,x[1]-x[0]); w[0]*=.5; w[-1]*=.5
        A=np.sum(p*u*w); B=np.sum(u*p*p*u*w); N2=np.sum(p*p*u*w); M2=np.sum(u**3*p*p*w)
        self.c=c=lam*N2/A**2; self.N=np.sqrt(N2)
        self.mu=c*B/N2; self.s2=c*c*M2/N2-self.mu**2
        self.lo=c/2; self.hi=2*R*c
        # CDF of density g^2 in variable U=c*v, v ~ phi^2/N2 ; tabulate on log grid
        dens_v=p*p/N2*u            # density in x=log v
        cdf=np.concatenate([[0],np.cumsum(0.5*(dens_v[1:]+dens_v[:-1])*(x[1]-x[0]))]); cdf/=cdf[-1]
        self._cdf=cdf; self._logU=x+np.log(c)
    def g(self,U):  # g(U)=c^{-1/2} g0(U/c), g0=phi/N
        U=np.asarray(U,float); return phi(np.maximum(U/self.c,1e-300),self.R)/self.N/np.sqrt(self.c)
    def sample(self,rng,size):
        return np.exp(np.interp(rng.random(size),self._cdf,self._logU))
def chi_factory(beta,gamma):
    return lambda s: 1-sstep((np.asarray(s,float)-beta)/(gamma-beta))
def log_alpha(lam,j): return j*log(lam)-lgamma(j+1)
