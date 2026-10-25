from sympy import symbols, Poly, factor_list, gcd, factorint
from math import gcd as g
x=symbols('x')
f=Poly(x**6+33*x**5+21*x**4+63*x**3+18*x**2+24*x+48,x)
print('factor_list over Q:',factor_list(f.as_expr()))
vals=[f.eval(n) for n in range(0,40)]
G=0
for v in vals: G=g(G,int(v))
print('fixed divisor gcd f(0..39) =',G, factorint(G))
# rho(2^4), rho(2^5), rho(3^4)
def rho(m): return sum(1 for a in range(m) if f.eval(a)%m==0)
for m in [16,32,81,3**5,5**4]:
    print('rho(%d)=%d'%(m,rho(m)))
# is 2^4 | f(n) for all n?  is any n with 2^5 not dividing?
print('all 16|f(n) for n<64:', all(int(f.eval(n))%16==0 for n in range(64)))
print('exists n with 32 not| f(n):', any(int(f.eval(n))%32!=0 for n in range(64)))
# f mod 16 vs falling factorial
ff=Poly(x*(x-1)*(x-2)*(x-3)*(x-4)*(x-5),x)
print('f - x(x-1)...(x-5) coeffs mod 16:', [int(c)%16 for c in (f-ff).all_coeffs()])
