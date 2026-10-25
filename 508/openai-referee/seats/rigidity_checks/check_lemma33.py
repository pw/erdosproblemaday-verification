# Lemma 3.3 (p.18-19): exact verification of the two unit-direction identities and the
# auxiliary algebraic facts used in Lemma 2.7 (p.13) and Sec 3.5 (p.21). With FAILING controls.
import sympy as sp
A,B,t,x,r,th = sp.symbols('A B t x r theta', positive=True)
I = sp.I
def absq(z):  # |z|^2 for z built from real symbols
    z = sp.expand(z); return sp.simplify(sp.expand(z*sp.conjugate(z)))
# u on the unit circle: rational parametrization u(t)=(1+it)/(1-it) (all of S^1 except -1), and u = e^{i theta}
u_par = (1+I*t)/(1-I*t)
u_tri = sp.cos(th)+I*sp.sin(th)
L = sp.sqrt(A*B)
ok = True
for name,u in [('u(t)=(1+it)/(1-it)',u_par),('u=e^{i theta}',u_tri)]:
    imu = sp.im(sp.expand_complex(u))
    rhs = (A-B)**2 + 4*A*B*imu**2
    e1 = sp.simplify(sp.expand_complex(absq(A-B*u**2) - rhs))
    e2 = sp.simplify(sp.expand_complex(absq(-L+(A-B)*u+L*u**2) - rhs))
    e3 = sp.simplify(sp.expand_complex((-L+(A-B)*u+L*u**2) - u*((A-B)+L*(u-1/u))))
    e4 = sp.simplify(sp.expand_complex((u-1/u) - 2*I*imu))
    e5 = sp.simplify(sp.expand_complex(r*u + r*sp.conjugate(u) - 2*r*sp.re(sp.expand_complex(u))))
    print(name, '(3.14) first =', e1, '| second =', e2, '| factorization =', e3, '| u-1/u-2iIm u =', e4, '| ru+r ubar-2rRe u =', e5)
    ok &= all(e==0 for e in (e1,e2,e3,e4,e5))
    # FAILING controls: replace L by 2L, and by (A+B)/2 ; drop |u|=1 (u -> 2u)
    c1 = sp.simplify(sp.expand_complex(absq(-2*L+(A-B)*u+2*L*u**2) - rhs))
    c2 = sp.simplify(sp.expand_complex(absq(-(A+B)/2+(A-B)*u+(A+B)/2*u**2) - rhs))
    c3 = sp.simplify(sp.expand_complex(absq(A-B*(2*u)**2) - ((A-B)**2 + 4*A*B*sp.im(sp.expand_complex(2*u))**2)))
    print('   controls (must be NONZERO): L->2L:', sp.factor(c1), '| L->(A+B)/2:', sp.factor(c2), '| u->2u:', sp.factor(c3))
    ok &= all(c!=0 for c in (c1,c2,c3))
# exact numeric instance with algebraic numbers (F = real algebraic numbers): A=2, B=3, u=(1+i*sqrt(2))/sqrt(3)
uu = (1+I*sp.sqrt(2))/sp.sqrt(3)
assert sp.simplify(uu*sp.conjugate(uu)) == 1
Ln = sp.sqrt(6)
lhs = sp.nsimplify(sp.simplify(sp.expand(sp.Abs(2-3*uu**2)**2)))
mid = (2-3)**2 + 4*6*sp.im(uu)**2
rhs2 = sp.simplify(sp.expand(sp.Abs(-Ln+(2-3)*uu+Ln*uu**2)**2))
print('exact instance A=2,B=3,u=(1+i sqrt2)/sqrt3: |A-Bu^2|^2 =', sp.simplify(lhs), ' (A-B)^2+4AB Im^2 =', sp.simplify(mid), ' |-L+(A-B)u+Lu^2|^2 =', sp.simplify(rhs2))
ok &= sp.simplify(lhs-mid)==0 and sp.simplify(rhs2-mid)==0
# p.13: every real x with |x|<2 is k+k' with k,k' in K: k = x/2 + i sqrt(1-x^2/4)
k = x/2 + I*sp.sqrt(1-x**2/4); kp = x/2 - I*sp.sqrt(1-x**2/4)
print('p.13 decomposition: |k|^2-1 =', sp.simplify(sp.expand_complex(k*sp.conjugate(k)).subs(x,sp.Rational(1,3))-1),
      '(at x=1/3), k+k\'-x =', sp.simplify(k+kp-x), ', k(1/3)=', k.subs(x,sp.Rational(1,3)))
# p.19 Lemma 3.4: formal expansion u(ha) = 1 + 2iha - 2h^2a^2 + ...
h,a = sp.symbols('h a')
ser = sp.series((1+I*h*a)/(1-I*h*a), h, 0, 4).removeO()
print('Lemma 3.4 series u(ha) =', sp.expand(ser))
ok &= sp.expand(ser - (1+2*I*h*a-2*h**2*a**2-2*I*h**3*a**3))==0
print('Lemma 3.4: 4a = (a+1)^2-(a-1)^2 :', sp.expand((a+1)**2-(a-1)**2))
print('ALL IDENTITIES OK' if ok else 'FAILURE')
