# Independent check of Lemma 4.1: build g = c^{-1/2} g0(u/c), g0 = phi_R/N_R, by its DEFINITION on a grid,
# and integrate g^2, g, u g^2 directly (no use of the paper's closed forms), then compare with 1, sqrt(lam),
# lam*B_R/A_R^2 and the bound lam*log(4R)/(log R)^2. Also reports the Prop 4.2 thresholds 2B/d and s_g^2/d^2.
import numpy as np, sys
def sstep(x):
    x=np.asarray(x,float); out=np.zeros_like(x)
    m=(x>0)&(x<1); a=np.exp(-1/x[m]); b=np.exp(-1/(1-x[m])); out[m]=a/(a+b); out[x>=1]=1.0
    return out
def phi(u,R): return (1/u)*sstep((u-0.5)/0.5)*(1-sstep((u-R)/R))
def integ(fvals,x):  # trapezoid in x
    return np.trapezoid(fvals,x)
for lam,logR,beta in [(3.0,33,0.10),(3.0,26,0.12),(1.0,12,0.10),(0.5,5,0.10)]:
    R=float(np.exp(logR))
    x=np.linspace(np.log(0.25),np.log(4*R),600001); u=np.exp(x)
    p=phi(u,R)
    A=integ(p*u,x); B=integ(u*p*p*u,x); N2=integ(p*p*u,x)
    g0=p/np.sqrt(N2); c=lam/integ(g0*u,x)**2
    # g on its own grid U = c*u (log grid shifts by log c); evaluate g(U) by definition
    U=c*u; xU=x+np.log(c); gU=c**-0.5*phi(U/c,R)/np.sqrt(N2)
    I2=integ(gU*gU*U,xU); I1=integ(gU*U,xU); mu=integ(U*gU*gU*U,xU); m2=integ(U*U*gU*gU*U,xU)
    s2=m2-mu**2; supp=U[gU>0]; Bend=supp.max(); lo=supp.min(); d=beta-mu
    print(f"lam={lam} logR={logR}: A-logR={A-logR:+.4f}(>=0) log4R-B_R={np.log(4*R)-B:+.4f}(>=0) N2={N2:.4f} in[1/2,2]")
    print(f"   int g^2={I2:.8f}  int g={I1:.8f} (sqrt lam={np.sqrt(lam):.8f})  mu_g={mu:.6f} lamB/A^2={lam*B/A**2:.6f} bound={lam*np.log(4*R)/logR**2:.6f}")
    print(f"   supp g ~ [{lo:.3g},{Bend:.3g}]  s_g^2={s2:.4g}  beta={beta} d={d:.5f}  2B/d={2*Bend/d:.3g}  s^2/d^2={s2/d**2:.3g}")
