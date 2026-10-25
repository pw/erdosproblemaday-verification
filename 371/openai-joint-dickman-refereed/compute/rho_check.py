# Is OpenAI's comparator `rho` (DelayConstruction.delay (-1)) Dickman's rho? Evaluate the Lean definition LITERALLY
# (stepApprox σ (n+1) u = 1 + σ ∫_1^{max 1 u} stepApprox σ n (t-1) / max 1 t dt, delay σ u = stepApprox σ ⌈u⌉₊ u)
# and compare with (i) an independent characterisation u·ρ(u) = ∫_{u-1}^{u} ρ(t) dt solved on a grid by a
# different method (high-order collocation / fine trapezoid), (ii) literature values.
import mpmath as mp
mp.mp.dps=30
from functools import lru_cache
import math
def step(n,u,sig=-1):
    u=mp.mpf(u)
    if n==0: return mp.mpf(1)
    up=max(mp.mpf(1),u)
    if up==1: return mp.mpf(1)
    # integrand piecewise-smooth with breaks at integers
    pts=[mp.mpf(1)]+[mp.mpf(k) for k in range(2,int(mp.floor(up))+1) if k<up]+[up]
    f=lambda t: step(n-1,t-1,sig)/max(mp.mpf(1),t)
    return 1+sig*mp.quad(f,pts)
def delay(u,sig=-1):
    n=int(mp.ceil(u)) if u>0 else 0
    return step(n,u,sig)
# independent: piecewise exact recursion via rho(u) = rho(k) - ∫_k^u rho(t-1)/t dt, rho on [0,1]=1, using Chebyshev-free
# fine trapezoid on a uniform grid h (second instrument: different quadrature, different recursion organisation)
import numpy as np
h=1e-5; U=np.arange(0,6+h/2,h); R=np.ones_like(U); k1=int(round(1/h))
for i in range(k1+1,len(U)):
    # rho'(u) = -rho(u-1)/u ; Heun step
    u0=U[i-1]; u1=U[i]
    d0=-R[i-1-k1]/u0; d1=-R[i-k1]/u1
    R[i]=R[i-1]+h*(d0+d1)/2
def rho_grid(u): return float(np.interp(u,U,R))
lit={2:0.30685281944005469058,3:0.04860838829,4:0.004910925648,5:0.0003547247005}
print("u   lean_def(mp)              grid(Heun h=1e-5)       literature")
for u in [0.5,1,1.5,2,2.5,3,10/3,4,5]:
    L=delay(mp.mpf(u)); print(f"{u:<5.4g} {mp.nstr(L,18):<24} {rho_grid(u):<22.15g} {lit.get(u,'')}")
print("closed form check on (1,2]: 1-ln u at 1.5:", 1-math.log(1.5))
