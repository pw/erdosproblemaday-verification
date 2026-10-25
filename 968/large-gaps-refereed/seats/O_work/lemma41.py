# Lemma 4.1 numerics: explicit smooth phi_R, check A_R>=log R, B_R<=log(4R), 1/2<=N_R^2<=2,
# the scaling identities for g, and mu_g = lam*B_R/A_R^2 <= lam*log(4R)/(log R)^2.
# Also reports support endpoints and variance s_g^2 of density g^2 (needed in Prop 4.2).
import numpy as np, sys, json
def sstep(x):                       # smooth step: 0 for x<=0, 1 for x>=1, C^infinity
    x=np.asarray(x,float); out=np.zeros_like(x)
    m=(x>0)&(x<1); a=np.exp(-1/x[m]); b=np.exp(-1/(1-x[m])); out[m]=a/(a+b); out[x>=1]=1.0
    return out
def phi(u,R):                       # =1/u on [1,R], 0<=phi<=1/u, support [1/2,2R]
    return (1/u)*sstep((u-0.5)/0.5)*(1-sstep((u-R)/R))
def moments(R,n=400001):
    # integrate in x=log u over [log(1/2), log(2R)] ; du = u dx
    x=np.linspace(np.log(0.5),np.log(2*R),n); u=np.exp(x); p=phi(u,R)
    w=np.full(n,(x[1]-x[0])); w[0]*=0.5; w[-1]*=0.5
    A=np.sum(p*u*w); B=np.sum(u*p*p*u*w); N2=np.sum(p*p*u*w); M2=np.sum(u*u*p*p*u*w)
    return A,B,N2,M2
res={}
for lam,beta in [(3.0,0.1),(1.0,0.1),(0.5,0.1)]:
    for logR in [5,10,12,15,20,25,30,33,35,40]:
        R=float(np.exp(logR)); A,B,N2,M2=moments(R)
        ok=(A>=np.log(R)-1e-9, B<=np.log(4*R)+1e-9, 0.5<=N2<=2)
        c=lam*N2/A**2                 # c = lam/(int g0)^2, int g0 = A/sqrt(N2)
        # g(u)=c^{-1/2} g0(u/c): int g^2 = int g0^2 =1 ; int g = sqrt(c) int g0 ; mu_g = c*int v g0^2
        int_g=np.sqrt(c)*A/np.sqrt(N2); int_g2=N2/N2; mu=c*B/N2
        second=c*c*M2/N2; s2=second-mu**2
        bound=lam*np.log(4*R)/np.log(R)**2
        res.setdefault(str(lam),[]).append(dict(logR=logR,A=A,logR_=np.log(R),B=B,log4R=np.log(4*R),N2=N2,ok=all(ok),
              int_g=int_g,sqrt_lam=np.sqrt(lam),mu_g=mu,mu_formula=lam*B/A**2,mu_bound=bound,
              supp_lo=c/2,supp_hi=2*R*c,s2=s2,beta=beta))
for lam,rows in res.items():
    print("lambda=",lam)
    for r in rows:
        print(" logR=%2d A=%.4f(>=%.1f) B=%.4f(<=%.4f) N2=%.5f ok=%s  int g=%.6f (sqrt lam %.6f) mu_g=%.5f =lamB/A^2 %.5f <= %.5f  supp=[%.3g,%.3g] s_g^2=%.3g"%(
            r['logR'],r['A'],r['logR_'],r['B'],r['log4R'],r['N2'],r['ok'],r['int_g'],r['sqrt_lam'],r['mu_g'],r['mu_formula'],r['mu_bound'],r['supp_lo'],r['supp_hi'],r['s2']))
json.dump(res,open('lemma41.json','w'),indent=1)
