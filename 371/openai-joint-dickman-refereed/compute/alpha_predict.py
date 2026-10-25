# Predicted natural density of {n : P(n+1) > P(n) n^alpha} under the product law of Theorem 1.1:
# D(alpha) = (mu x mu){(x,y): y > x + alpha}, mu with CDF F(t) = rho(1/t) on (0,1], density f(t) = rho(1/t - 1)/t,
# D(alpha) = ∫_0^{1-alpha} f(x) (1 - F(x+alpha)) dx.  rho by Heun on u rho'(u) = -rho(u-1), h = 1e-4 (checked in rho_check2.py).
import numpy as np
h=1e-4; U=np.arange(0,60+h/2,h); R=np.ones_like(U); k1=int(round(1/h))
for i in range(k1+1,len(U)): R[i]=R[i-1]+h*(-R[i-1-k1]/U[i-1]-R[i-k1]/U[i])/2
rho=lambda u: np.interp(u,U,R)
F=lambda t: np.where(t<=0,0.0,np.where(t>=1,1.0,rho(1/np.maximum(t,1e-12))))
f=lambda t: rho(1/t-1)/t
for a in [0,0.05,0.1,0.2,0.3,0.5]:
    x=np.linspace(1e-6,1-a,400001); print(f"alpha={a:.2f} predicted D={np.trapezoid(f(x)*(1-F(x+a)),x):.6f}")
x=np.linspace(1e-6,1,400001); print("mass check ∫f =",np.trapezoid(f(x),x))
