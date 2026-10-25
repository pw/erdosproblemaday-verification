# Is OpenAI's comparator `rho` (= DelayConstruction.delay (-1)) Dickman's rho?
# Lean def: stepApprox σ 0 = 1; stepApprox σ (n+1) u = 1 + σ ∫_1^{max 1 u} stepApprox σ n (t-1) / max 1 t dt;
#           delay σ u = stepApprox σ ⌈u⌉₊ u ;  rho = delay (-1).
# Instrument 1: the definition LITERALLY, Picard iteration on a fine grid (trapezoid), n = ⌈u⌉ iterations.
# Instrument 2: mpmath quadrature of the definition, nested, for u <= 3.
# Instrument 3: an independent characterisation, the ODE u·ρ'(u) = -ρ(u-1) (Heun), plus literature values.
import numpy as np, mpmath as mp, math
h=2e-5; U=np.arange(0,6+h/2,h); k1=int(round(1/h))
def picard(n):
    f=np.ones_like(U)
    for _ in range(n):
        shifted=np.ones_like(U); shifted[k1:]=f[:-k1]
        integrand=shifted/np.maximum(1.0,U)
        cum=np.concatenate([[0],np.cumsum((integrand[1:]+integrand[:-1])*h/2)])
        g=1-(cum-cum[k1]); g[:k1+1]=1.0
        f=g
    return f
P={n:picard(n) for n in range(0,7)}
def lean_grid(u):
    n=int(math.ceil(u)) if u>0 else 0
    return float(np.interp(u,U,P[n]))
mp.mp.dps=20
def step_mp(n,u):
    u=mp.mpf(u)
    if n==0 or u<=1: return mp.mpf(1)
    pts=[mp.mpf(1)]+[mp.mpf(k) for k in range(2,int(mp.floor(u))+1) if k<u]+[u]
    return 1-mp.quad(lambda t: step_mp(n-1,t-1)/max(mp.mpf(1),t),pts)
R=np.ones_like(U)
for i in range(k1+1,len(U)):
    R[i]=R[i-1]+h*(-R[i-1-k1]/U[i-1]-R[i-k1]/U[i])/2
lit={2:0.306852819440055,3:0.0486083882911316,4:0.00491092564776083,5:0.000354724700456040}
print(f"{'u':<7}{'Lean def (grid Picard)':<24}{'Lean def (mpmath)':<22}{'ODE (Heun)':<22}{'literature'}")
for u in [0.5,1.0,1.5,2.0,2.5,3.0,10/3,4.0,5.0]:
    m = mp.nstr(step_mp(int(math.ceil(u)),u),15) if u<=2.5 else '-'
    print(f"{u:<7.4g}{lean_grid(u):<24.12g}{m:<22}{float(np.interp(u,U,R)):<22.12g}{lit.get(u,'')}")
print("stability (n=6 vs n=ceil u) at 2.5, 3.7:", lean_grid(2.5)-float(np.interp(2.5,U,P[6])), lean_grid(3.7)-float(np.interp(3.7,U,P[6])))
print("negative control: one iteration short at u=2.5:", float(np.interp(2.5,U,P[2])), "vs", lean_grid(2.5))
