import numpy as np, math
N=10**7; M=N+2
gpf=np.zeros(M,dtype=np.int32); is_p=np.ones(M,dtype=bool); is_p[:2]=False
for p in range(2,int(M**.5)+1):
    if is_p[p]: is_p[p*p::p]=False
for p in np.nonzero(is_p)[0]: gpf[p::p]=p
n=np.arange(2,N+1,dtype=np.float64); ln=np.log(n)
U=np.log(gpf[2:N+1])/ln; V=np.log(gpf[3:N+2])/ln
# limiting law density u(t)=rho(1/t-1)/t on (0,1)
h=1e-4; uu=np.arange(0,40,h); rho=np.ones_like(uu); m=int(round(1/h))
for i in range(m+1,len(uu)):
    rho[i]=rho[i-1]+h*(-rho[i-1-m]/uu[i-1]-rho[i-m]/uu[i])/2
t=np.linspace(1e-4,1,20000); dens=np.interp(1/t-1,uu,rho)/t; dt=t[1]-t[0]
w=dens*dt; w/=w.sum()
for a in [0.0,0.1,0.2,0.4]:
    pred=sum(w[i]*w[t>t[i]+a].sum() for i in range(0,len(t),1))
    emp=np.mean(V>U+a)
    print(f"alpha={a}: empirical(n<=1e7)={emp:.4f}  limit P(V-U>alpha)={pred:.4f}")
