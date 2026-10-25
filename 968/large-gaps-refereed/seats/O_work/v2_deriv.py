# Symbolic check of (4) and of "signed complete mixed derivative of F~_j = F_j + F_{j+1}(.,0) is f_j + T f_{j+1}" for j=1,2.
import sympy as sp
s1,s2,s3,v1,v2,v3,u=sp.symbols('s1 s2 s3 v1 v2 v3 u',positive=True)
f1=sp.exp(-2*s1)*s1**2
f2=sp.exp(-s1-s2)*s1*s2*(1+s1*s2)
f3=sp.exp(-s1-s2-s3)*s1*s2*s3
F1=sp.integrate(f1.subs(s1,v1+s1),(s1,0,sp.oo))                      # int_{s>=v1}
F2=sp.integrate(sp.integrate(f2,(s1,v1,sp.oo)),(s2,v2,sp.oo))
F3=sp.integrate(sp.integrate(sp.integrate(f3,(s1,v1,sp.oo)),(s2,v2,sp.oo)),(s3,v3,sp.oo))
print("(4) j=1:",sp.simplify(-sp.diff(F1,v1)-f1.subs(s1,v1)))
print("(4) j=2:",sp.simplify(sp.diff(F2,v1,v2)-f2.subs({s1:v1,s2:v2})))
Ft1=F1+F2.subs(v2,0); Tf2=sp.integrate(f2.subs({s1:v1,s2:u}),(u,0,sp.oo))
print("F~1:",sp.simplify(-sp.diff(Ft1,v1)-(f1.subs(s1,v1)+Tf2)))
Ft2=F2+F3.subs(v3,0); Tf3=sp.integrate(f3.subs({s1:v1,s2:v2,s3:u}),(u,0,sp.oo))
print("F~2:",sp.simplify(sp.diff(Ft2,v1,v2)-(f2.subs({s1:v1,s2:v2})+Tf3)))
Ft0=sp.Integer(0)+F1.subs(v1,0); print("F~0 = f0 + int f1:",sp.simplify(Ft0-sp.integrate(f1,(s1,0,sp.oo))))
