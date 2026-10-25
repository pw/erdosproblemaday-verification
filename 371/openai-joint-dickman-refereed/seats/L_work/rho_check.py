import numpy as np, math
# Comparator construction: rho(u)=1 (u<=1); stepApprox n+1 (u) = 1 - int_1^{max(1,u)} f(t-1)/max(1,t) dt
h=1e-4; U=4.0
us=np.arange(0,U+h/2,h); rho=np.ones_like(us)
k1=int(round(1/h))
for i in range(k1+1,len(us)):
    # rho(u)=1-int_1^u rho(t-1)/t dt, trapezoid incremental
    t0,t1=us[i-1],us[i]
    rho[i]=rho[i-1]-0.5*h*(rho[i-1-k1]/t0+rho[i-k1]/t1)
def r(u): return float(np.interp(u,us,rho))
print('rho(2) =',r(2.0),' 1-ln2 =',1-math.log(2))
print('rho(3) =',r(3.0),' known 0.0486083882911...')
print('rho(1.5)=',r(1.5),' 1-ln1.5=',1-math.log(1.5))
# empirical joint law and ordering at X=2e6
X=2_000_001
lpf=np.zeros(X+2,dtype=np.int64)
for p in range(2,X+2):
    if lpf[p]==0:
        lpf[p::p]=p   # increasing p overwrites => largest prime factor
n=np.arange(2,X,dtype=np.int64)
P=lpf[2:X]; Q=lpf[3:X+1]
for a,b in [(0.5,0.5),(0.5,0.7),(0.3,0.8)]:
    ev=(P<=n**a)&(Q<=n**b)
    print(f'a={a} b={b}: empirical {ev.sum()/X:.4f}  rho(1/a)rho(1/b)={r(1/a)*r(1/b):.4f}  marg {np.mean(P<=n**a):.4f} vs {r(1/a):.4f}')
print('P+(n)<P+(n+1) density:', np.mean(P<Q)*(X-2)/X)
