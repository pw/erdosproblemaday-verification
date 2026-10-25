import sympy as sp
u,v,p,a,b,c,d=sp.symbols('u v p a b c d')
Q0=[(1,0),(-1,0),(0,1),(0,-1)]
pts=[]
for (q0,q1) in Q0:
    pts.append(( (u*q0-v*q1, v*q0+u*q1), (-v*q0-u*q1, u*q0-v*q1), 1))   # R_+ q, D, weight
for (q0,q1) in Q0:
    pts.append(( (u*q0+v*q1, -v*q0+u*q1), (-v*q0+u*q1, -u*q0-v*q1), 1))  # R_- q
for (q0,q1) in Q0:
    pts.append(( (sp.Integer(q0),sp.Integer(q1)), (0,0), -2))
S=sum(w*(p+a*x[0]+b*x[1]+c*Dx[0]+d*Dx[1])**2 for x,Dx,w in pts)
rhs=4*(u**2+v**2)*(c**2+d**2)+4*(u**2+v**2-1)*(a**2+b**2)
print("Lean weighted_coordinate_square identity:", sp.expand(S-rhs)==0)
# paper (31) moments with p_i=(1,x_i)
M0=sp.zeros(3,3); M1=sp.zeros(3,3); M2=sp.zeros(3,3)
for x,Dx,w in pts:
    P=sp.Matrix([1,x[0],x[1]]); DP=sp.Matrix([0,Dx[0],Dx[1]])
    M0+=w*P*P.T; M1+=w*DP*P.T; M2+=w*DP*DP.T
sub={v:sp.sqrt(1-u**2)}
print("sum b p p^T =", sp.simplify(M0.subs(sub)))
print("sum b dp p^T =", sp.simplify(M1.subs(sub)))
print("sum b dp dp^T =", sp.simplify(M2.subs(sub)))
# Liouville: Lean parameter vs paper t (partial sums)
from fractions import Fraction
from math import factorial
lean=sum(Fraction(1,10**factorial(m+1)) for m in range(0,5))
paper=sum(Fraction(1,10**factorial(m)) for m in range(1,6))
print("Lean partial == paper partial:", lean==paper, float(lean))
# rounding window
import itertools
print("weights sum:", 8*1+4*(-2))
