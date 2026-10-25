# Semi-analytic (characteristic-function) evaluation of w and v/lam for the Prop 4.2 family at HUGE k,
# where direct Monte Carlo is impossible (lambda=3 needs k >= 2B/d ~ 2.5e14 before the paper's bounds apply).
# S_k = (1/k) sum_{i<=k} U_i, U_i iid with density g^2. Density of S_k obtained by inverting
#   E exp(i xi (S_k - mu)) = exp(k [log(1 + i eta mu + rho(eta)) - i eta mu]),  eta = xi/k,
#   rho(eta) = int (e^{i eta U} - 1 - i eta U) g(U)^2 dU  (computed with cancellation-free formulas).
# Approximation (stated in the report): all j in [a-1,k] use the law of S_k (mean differs by <= mu*r/k).
# v/lam assembled from deficiency variables a=1-chi, b=1-H/sqrt(lam) (zero off the tail) to avoid 1-2c+c^2 cancellation.
import numpy as np, sys, time
from math import sqrt, floor
from common import Profile, chi_factory
lam=float(sys.argv[1]); logR=float(sys.argv[2]); ks=[int(float(x)) for x in sys.argv[3].split(',')]
beta,gamma=0.10,0.12
P=Profile(lam,logR); chi=chi_factory(beta,gamma); mu=P.mu; s2=P.s2; B=P.hi; d=beta-mu
nU=200001
xU=np.linspace(np.log(P.lo),np.log(P.hi),nU); U=np.exp(xU)
wq=np.full(nU,xU[1]-xU[0]); wq[0]*=.5; wq[-1]*=.5
gU=P.g(U); dens=gU*gU*U*wq            # g^2 dU weights
nu=gU*U*wq/np.sqrt(lam)               # nu = g/sqrt(lam) dU weights (prob.)
print(f"lam={lam} logR={logR} mu_g={mu:.6f} d={d:.5f} B={B:.4g} s_g^2={s2:.4g}; quad checks: int g^2={dens.sum():.8f} int nu={nu.sum():.8f} mean={np.sum(U*dens):.6f}",flush=True)
def rho(eta):
    x=np.outer(eta,U)
    re=-2*np.sin(x/2)**2
    small=x<1e-2
    im=np.where(small,-x**3/6+x**5/120-x**7/5040,np.sin(x)-x)
    return (re+1j*im)@dens
for k in ks:
    t0=time.time(); r=int(floor(sqrt(k))); a_=k-r+1
    sd=sqrt(s2/k); jump=B/k
    lo=max(0.0,mu-12*sd)-0.01; hi=max(gamma+jump,mu+40*sd)+0.01
    N=2**15; Ls=hi-lo; dy=Ls/N; y=lo+dy*np.arange(N)
    dxi=2*np.pi/Ls; M=N//2; xi=dxi*np.arange(M+1)
    K=np.empty(M+1,complex)
    K[:]=-np.inf+0j; cut=M+1
    for c0 in range(0,M+1,64):
        eta=xi[c0:c0+64]/k; z=1j*eta*mu+rho(eta)
        az=np.abs(z); ser=z-z*z/2+z**3/3-z**4/4; ex=np.log(1+z)
        K[c0:c0+64]=k*(np.where(az<1e-3,ser,ex)-1j*eta*mu)   # exact log(1+z); 4-term series only where |z|<1e-3
        if np.all(K[c0:c0+64].real<-745): cut=c0; break   # |cf| < 1e-323 beyond
    phi=np.where(np.isfinite(K.real),np.exp(K),0)*np.exp(-1j*xi*(lo-mu))     # cf of (S-lo)
    # p(y_n) = (dxi/2pi) [phi0 + 2 Re sum_m phi_m e^{-i xi_m n dy}]
    E=np.fft.fft(np.concatenate([phi,np.zeros(N-M-1)]))   # sum_m phi_m e^{-2pi i m n/N}
    p=(dxi/(2*np.pi))*(2*E.real-phi[0].real); p=np.maximum(p,0)*dy
    tot=p.sum(); mean=np.sum(p*y)/tot
    a=1-chi(y)
    # b(y) = int nu(u) (1-chi(y+u/k)) du : bin u/k on the y-grid
    edges=np.arange(0,int(np.ceil(jump/dy))+2)*dy
    Pl=np.histogram(U/k,bins=edges,weights=nu)[0]
    yy=lo+dy*np.arange(N+len(Pl)); ayy=1-chi(yy)
    b=np.array([np.dot(Pl,ayy[n+np.arange(len(Pl))]) for n in range(N)]) if len(Pl)<64 else np.convolve(ayy,Pl[::-1],'valid')[:N]
    tail=p[y>beta-jump].sum()
    Ea=np.sum(p*a);Ea2=np.sum(p*a*a);Eb=np.sum(p*b);Eb2=np.sum(p*b*b)
    w=1-2*Ea+Ea2
    jj=np.arange(a_,k,dtype=np.float64); cj=np.sqrt((jj+1)/k)
    cbar=cj.mean() if len(cj) else 1.0
    Ecb_a2=np.sum(p*(cbar*b-a)**2); Ecb_a=cbar*Eb-Ea
    interior=(np.sum((1-cj)**2)+len(cj)*Ecb_a2+2*np.sum(1-cj)*Ecb_a)/r
    top=w/r; bottom=(a_/k)*(1-2*Eb+Eb2)/r
    v=interior+top+bottom
    v0=(np.sum((1-cj)**2)+1+a_/k)/r
    print(f" k={k:.1e} r={r}: mass={tot:.6f} mean={mean:.6f}(mu={mu:.6f}) P(S>beta-B/k)={tail:.3e} | w={w:.10f} [LB(10) {1-s2/(k*d*d):.6g}]"
          f" v/lam={v:.6e} [cutoff-free {v0:.6e}; UB(12) {2/r+(r/k)**2+4*s2/(k*d*d):.4g}{'' if k>=2*B/d else ' (k<2B/d: not claimed)'}] xi_cut={cut}/{M} ({time.time()-t0:.0f}s)",flush=True)
