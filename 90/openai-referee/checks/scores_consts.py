# Constants of Sections 5-6: delta=1/100, lambda=delta^2/2 (exact rational arithmetic).
from fractions import Fraction as F
import sys
def run(delta,lam,label):
    ok=True
    half=F(1,2)
    def c(r): return 1+lam if abs(r-half)<=delta else 1-lam
    def g(r): return c(r)*(r*r+(1-r)**2)-2*r*(1-r)
    # identity in (6.7)
    for r in [F(i,1000) for i in range(1001)]+[half-delta,half+delta]:
        assert g(r)==(2*r-1)**2+(c(r)-1)*(r*r+(1-r)**2)
    # (6.7) >= lam/2: inside window min is at r=1/2 (value lam/2 exactly); outside, infimum at the window edge
    grid=[F(i,100000) for i in range(100001)]
    eps=F(1,10**12)
    pts=grid+[half-delta,half+delta,half-delta-eps,half+delta+eps]
    m=min(g(r) for r in pts)
    c67 = m>=lam/2
    inf_out = 4*delta**2 - lam*(half+2*delta**2)   # limit of g at the window edge from outside
    print(f"[{label}] delta={delta} lam={lam}")
    print("  (6.7) min over grid+edges =",float(m)," >= lam/2:",c67, "; outside-edge infimum 4d^2-lam(1/2+2d^2) =",float(inf_out))
    print("  4d^2 - lam > lam/2 :", 4*delta**2-lam > lam/2)
    k55 = 4/(2*(F(1,4)-delta**2))
    print("  Prop 5.5 constant 4/(2(1/4-d^2)) =",float(k55)," <= 10 :", k55<=10)
    print("  10 d^2 < 1/4 :", 10*delta**2 < F(1,4), "  (sandwich lam/4 > 10 d^2 lam:", lam/4 > 10*delta**2*lam,")")
    print("  on window 2rho(1-rho) >= 2(1/4-d^2):", min(2*r*(1-r) for r in [half-delta,half+delta,half])>=2*(F(1,4)-delta**2))
    return c67 and (4*delta**2-lam>lam/2) and k55<=10 and 10*delta**2<F(1,4)
a=run(F(1,100),F(1,100)**2/2,"paper")
b=run(F(1,100),8*F(1,100)**2,"control lam=8 d^2 (should FAIL (6.7))")
c=run(F(1,5),F(1,5)**2/2,"control delta=1/5 (should FAIL 10d^2<1/4)")
print("ALL PAPER CONSTANT CHECKS PASS:",a,"| control1 passes?",b,"| control2 passes?",c)
