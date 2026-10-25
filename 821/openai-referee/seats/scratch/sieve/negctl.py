# Negative controls for buchstab.py: perturbed versions of (7.18) must NOT match.
import math
from scipy.integrate import quad
import buchstab as B   # reuses D(g,w) from the definition (7.15); module runs nothing without argv
b1=0.2
Db=B.D(b1,1.0)
# (a) wrong lower-roughness parameter in the integrand: D_{0.9a}(1-a)
r1,_=quad(lambda a: B.D(0.9*a,1-a)/a, b1, 0.5, points=[0.25,1/3],limit=200)
# (b) wrong measure: da instead of da/a
r2,_=quad(lambda a: B.D(a,1-a), b1, 0.5, points=[0.25,1/3],limit=200)
# (c) wrong combinatorial coefficient: drop the factor l (i.e. use 1/l! for the (l-1)-term), emulate by l/l! -> 1/l!
def Dbad(g,w):
    tot=1.0/w; l=2
    while l*g<=w+1e-15:
        tot+=B.J(l-1,w-g,g)/math.factorial(l)/l   # extra 1/l
        l+=1
    return tot
r3,_=quad(lambda a: Dbad(a,1-a)/a, b1, 0.5, points=[0.25,1/3],limit=200)
print(f"target D_b1(1)-1 = {Db-1:.10f}; (a) {r1:.10f}  (b) {r2:.10f}  (c) {r3:.10f}")
