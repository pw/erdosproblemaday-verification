# Finite/symbolic checks for referee seat "whole". Run: nice -n 19 python3 -I identities.py
import sympy as sp
from fractions import Fraction as Fr
ok=lambda name,cond: print(("PASS " if cond else "FAIL ")+name)

D1,D2,D3=sp.symbols('D1 D2 D3',nonzero=True)
# (4.15) determinant of [[1/D2-1/D1, D2-D1],[1/D3-1/D1, D3-D1]]
det=sp.Matrix([[1/D2-1/D1,D2-D1],[1/D3-1/D1,D3-D1]]).det()
claim=(D1-D2)*(D1-D3)*(D2-D3)/(D1*D2*D3)
ok("(4.15) determinant", sp.simplify(det-claim)==0)
# control: wrong sign of last factor must FAIL
ok("(4.15) CONTROL wrong sign (expect FAIL)", sp.simplify(det-(D1-D2)*(D1-D3)*(D3-D2)/(D1*D2*D3))==0)
# quadratic term cancels on subtracting j=1 from j=2 (Prop 4.4)
dZ,dW=sp.symbols('dZ dW')
Ej=lambda D: sp.expand((D+dZ)*(1/D+dW)-1)
ok("Prop4.4: Ej = dZ/Dj + Dj dW + dZ dW", sp.simplify(Ej(D1)-(dZ/D1+D1*dW+dZ*dW))==0)
ok("Prop4.4: E2-E1 linear in (dZ,dW)", sp.Poly(sp.simplify(Ej(D2)-Ej(D1)),dZ,dW).total_degree()==1)

d,dp=sp.symbols('d dp',nonzero=True)
# (5.14)/(7.13): (d-d')(1/d-1/d') = 2 - d/d' - d'/d = -(d-d')^2/(d d')
ok("(7.13) identity", sp.simplify((d-dp)*(1/d-1/dp)-(2-d/dp-dp/d))==0)
ok("(5.14) product = -(d-d')^2/(dd')", sp.simplify((d-dp)*(1/d-1/dp)+(d-dp)**2/(d*dp))==0)
# (8.10): R=1/lam-lam, L=2-lam-1/lam  =>  R^2 = L(L-4)
lam=sp.symbols('lam',nonzero=True)
L=2-lam-1/lam; R=1/lam-lam
ok("(8.10) R^2=L(L-4)", sp.simplify(R**2-L*(L-4))==0)
ok("(8.10) CONTROL R^2=L(L+4) (expect FAIL)", sp.simplify(R**2-L*(L+4))==0)
# (8.9): differentiate (z_p-z_r)(w_p-w_r) with z=x+iy, w=x-iy, d i = 0
x1,y1,x2,y2,hx,hy,ux,uy=sp.symbols('x1 y1 x2 y2 hx hy ux uy')
t=sp.symbols('t')
X1=x1+t*hx;Y1=y1+t*hy;X2=x2+t*ux;Y2=y2+t*uy
Lt=((X1+sp.I*Y1)-(X2+sp.I*Y2))*((X1-sp.I*Y1)-(X2-sp.I*Y2))
dL=sp.diff(Lt,t).subs(t,0)
ok("(8.9) LHS = 2(p-r).(H-U)", sp.simplify(sp.expand(dL-2*((x1-x2)*(hx-ux)+(y1-y2)*(hy-uy))))==0)
# derivative of 2-lam-1/lam along d lam = lam*A : equals R*A
A=sp.symbols('A')
ok("(8.9) RHS: d(2-lam-1/lam) = (1/lam - lam)*(dlam/lam)", sp.simplify(sp.diff(L,lam)*lam*A-R*A)==0)
# (8.15)
z,u,v,b,a=sp.symbols('z u v b a')
w=v+b/(z-u); wr=v+b/(a-u)
Ll=sp.simplify((z-a)*(w-wr))
zeta=sp.symbols('zeta')
ok("(8.15) L = -b(zeta-1)^2/zeta", sp.simplify(Ll.subs(z,u+zeta*(a-u))-(-b*(zeta-1)**2/zeta))==0)
q=sp.expand(sp.numer(sp.together(-b*(zeta-1)**2/zeta-4)))
ok("(8.15) L-4=0 <=> b z^2+(4-2b)z+b=0", sp.simplify(q+(b*zeta**2+(4-2*b)*zeta+b))==0)
ok("(8.15) discriminant 16(1-b)", sp.simplify(sp.discriminant(b*zeta**2+(4-2*b)*zeta+b,zeta)-16*(1-b))==0)
Lb1=-(zeta-1)**2/zeta
ok("b=1: L(L-4) = ((zeta^2-1)/zeta)^2", sp.simplify(Lb1*(Lb1-4)-((zeta**2-1)/zeta)**2)==0)
# line case: w = e z + e', r on line => L = e (z-a)^2
e,ep=sp.symbols('e ep')
ok("line case L=e(z-a)^2", sp.simplify((z-a)*((e*z+ep)-(e*a+ep))-e*(z-a)**2)==0)
# Section 2 exponent bookkeeping
gam=Fr(27,50); eta=gam-Fr(1,2)
ok("eta = 1/25", eta==Fr(1,25))
ok("2/3-gamma = 19/150", Fr(2,3)-gam==Fr(19,150))
ok("t^{-a/2}(UV)^{-eta}, UV>=t^{-a/4}: exponent -49/100", -Fr(1,2)+eta/4==Fr(-49,100))
ok("xi_t exponent: (uv)^{1/6} with uv<=t^{-a/8}: -1/48", Fr(-1,8)*Fr(1,6)==Fr(-1,48))
# Lemma 2.7: D <= [2(1+2a) - (2+3a)] log t = a log t (+o)
aa=sp.symbols('a',positive=True)
ok("Lemma2.7 exponent gap = a", sp.simplify(2*(1+2*aa)-(2+3*aa)-aa)==0)
# Section 5/6 numerics
delta=Fr(1,100); lamc=delta**2/2
ok("4d^2 lam/(2(1/4-d^2)) <= 10 d^2 lam", 4*delta**2*lamc/(2*(Fr(1,4)-delta**2))<=10*delta**2*lamc)
ok("10 delta^2 < 1/4", 10*delta**2<Fr(1,4))
ok("lam/4 > 10 delta^2 lam (6.3 sandwich nondegenerate)", lamc/4>10*delta**2*lamc)
ok("(6.7) outside: 4d^2 - lam > lam/2", 4*delta**2-lamc>lamc/2)
rho=sp.symbols('rho')
expr=lambda c: c*(rho**2+(1-rho)**2)-2*rho*(1-rho)
ok("(6.7) algebraic identity", sp.simplify(expr(sp.Symbol('c'))-((2*rho-1)**2+(sp.Symbol('c')-1)*(rho**2+(1-rho)**2)))==0)
import numpy as np
grid=np.linspace(0,1,200001); dl=0.01; lm=dl**2/2
c=np.where(np.abs(grid-0.5)<=dl,1+lm,1-lm)
val=c*(grid**2+(1-grid)**2)-2*grid*(1-grid)
ok("(6.7) min over rho grid >= lam/2 (min=%.3e, lam/2=%.3e)"%(val.min(),lm/2), val.min()>=lm/2-1e-15)
# Lemma 7.2 Young: 6 th sqrt(C0 A S) <= A/4 + 36 C0 th^2 S
A_,S_,C0,th=sp.symbols('A S C0 th',positive=True)
ok("Lemma 7.2 Young", sp.simplify((A_/4+36*C0*th**2*S_)-6*th*sp.sqrt(C0*A_*S_) - (sp.sqrt(A_)/2-6*th*sp.sqrt(C0*S_))**2)==0)
# Prop 4.4 constants: 64 B^5 tau / r^3 < r/2 when tau < r^4/(128 B^5)
Bv,rv,tv=sp.symbols('B r tau',positive=True)
ok("Prop4.4: tau=r^4/(128B^5) gives 64B^5tau/r^3 = r/2 (strict for smaller tau)", sp.simplify(64*Bv**5*(rv**4/(128*Bv**5))/rv**3-rv/2)==0)
# 8B tau bound: sqrt2 tau(2B) + (2B+sqrt2 tau) sqrt2 tau <= 8 B tau for B>=2, tau<=1
ok("Prop4.4: 8B tau error bound (B=2,tau=1 worst)", (np.sqrt(2)*1*4+(4+np.sqrt(2))*np.sqrt(2))<=8*2)
# Cor 3.3: inner product = hashed strict-cross indicator; 4*sqrt(18)<18
ok("4 sqrt 18 < 18", 4*np.sqrt(18)<18)
for (a1,b1,a2,b2) in [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1)]:
    ip=(a1==a2)+(b1==b2)-2*((a1,b1)==(a2,b2)); sc=((a1==a2)!=(b1==b2))
    ok(f"Cor3.3 ip==strict-cross at {(a1,b1,a2,b2)}", ip==sc)
# Lemma 3.1 constant: B'*sqrt(8B^2*(D/2K)^{1/2}) <= 4BB'(D/K)^{1/4}
ok("Lemma 3.1 constant sqrt(8)/2^{1/4} <= 4", np.sqrt(8)/2**0.25<=4)
# Lemma 8.5 count
ok("N=20,j=5: N d1 - 3j > N(d1-1) for d1 in {1,2}", all(20*d1-15>20*(d1-1) for d1 in (1,2)))
