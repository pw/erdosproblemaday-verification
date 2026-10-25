# Independent recomputation (seat B): rho from the integral characterisation u*rho(u) = ∫_{u-1}^u rho(t) dt,
# predicted density D(alpha) = P(V > U + alpha) = ∫_alpha^1 f(y) F(y - alpha) dy (mirror of the entry's formula),
# F(t) = rho(1/t), f(t) = rho(1/t - 1)/t.  Plus exact-integer counts at X = 10^6 for alpha = k/20.
import math
h=1e-4; K=int(round(1/h)); UMAX=40.0; n=int(UMAX/h)+1
R=[1.0]*n
# prefix integral of rho with trapezoid
C=[0.0]*n
for i in range(1,K+1): C[i]=C[i-1]+h
for i in range(K+1,n):
    u=i*h
    # ∫_{u-1}^{u} rho = C[i]-C[i-K]; C[i]=C[i-1]+h/2(R[i-1]+R[i]); unknown R[i]
    # u R = C[i-1] + h/2 R[i-1] + h/2 R[i] - C[i-K]
    R[i]=(C[i-1]+h/2*R[i-1]-C[i-K])/(u-h/2)
    C[i]=C[i-1]+h/2*(R[i-1]+R[i])
def rho(u):
    if u<=1: return 1.0
    if u>=UMAX: return 0.0
    x=u/h; i=int(x); t=x-i
    return R[i]*(1-t)+R[i+1]*t
for u,lit in [(2,0.306852819440055),(3,0.0486083882911316),(4,0.00491092564776083),(1/0.7,1-math.log(1/0.7))]:
    print(f"rho({u:.4f}) = {rho(u):.10f}  ref {lit:.10f}  diff {rho(u)-lit:.1e}")
F=lambda t: 0.0 if t<=0 else (1.0 if t>=1 else rho(1/t))
f=lambda t: rho(1/t-1)/t if t>0.02 else 0.0
def D(a,N=200000):
    lo,hi=max(a,1e-9),1.0; s=0.0; hh=(hi-lo)/N
    for j in range(N+1):
        y=lo+j*hh; w=1 if j in (0,N) else (4 if j%2 else 2)
        s+=w*f(y)*F(y-a)
    return s*hh/3
for a in [0.0,0.05,0.10,0.20,0.30,0.50]:
    print(f"alpha={a:.2f} predicted (mirror formula) = {D(a):.6f}")
