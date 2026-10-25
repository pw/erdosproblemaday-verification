"""Host seat: evaluate Sarid's two-branch bound as a function of the max-cut input I0 and the split rho0.
F(a,mu) low-density envelope (paper (15)); high branch H(rho0) = rho0/8 - rho0^2/4 + gamma/4. The overall bound is
max(H(rho0), max_{a,mu} F). With I0 = 2/47 (BCL) and rho0 = 7/22 it must give ~0.026176 < 131/5000; with the
elementary EFPS value I0 = 1/18 it must be compared to Razborov's 27/1024."""
from fractions import Fraction as F
import math
GAMMA = F(3,64) + F(1,50_000_000_000)
def L(a): a=min(a,1-a); return min(4*a*a, a*(1-a))
def Fval(a, mu, rho0, I0):
    c = 1-a; P = a*rho0/2 + c*I0
    return min(P - (1+a)*mu/(4*c), mu/4) - L(a)*mu**3/c**2
def low_max(rho0, I0, N=4000):
    best=(-1,None,None)
    for i in range(1, N):
        a = i/(2*N)             # a in (0,1/2)
        c = 1-a
        for mu in (min(2*c*(a*rho0/2+c*I0), 4*I0*c*c), 4*I0*c*c):
            v = Fval(a, mu, rho0, I0)
            if v > best[0]: best=(v,a,mu)
    return best
def high(rho0): return rho0/8 - rho0**2/4 + float(GAMMA)/4
for name, I0 in (("BCL 2/47", 2/47), ("EFPS 1/18", 1/18)):
    for rho0 in (5/16, 0.3184, 7/22, 0.33, 0.35):
        lo = low_max(rho0, I0); hi = high(rho0)
        print(f"{name:10s} rho0={rho0:.4f}  high={hi:.6f}  low_max={lo[0]:.6f} at a={lo[1]:.4f}  overall={max(hi,lo[0]):.6f}  (27/1024={27/1024:.6f}, 131/5000={131/5000})")
