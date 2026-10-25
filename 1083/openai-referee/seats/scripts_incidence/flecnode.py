import sympy as sp, random
x,y,z,u,v=sp.symbols('x y z u v')
def Rpoly(F):
    A=sp.diff(F,z);B=sp.diff(F,x);C=sp.diff(F,y)
    V=[A*u,A*v,-B*u-C*v]; X=[x,y,z]
    H=[[sp.diff(F,X[i],X[j]) for j in range(3)] for i in range(3)]
    q=sp.expand(sum(H[i][j]*V[i]*V[j] for i in range(3) for j in range(3)))
    T=[[[sp.diff(F,X[i],X[j],X[k]) for k in range(3)] for j in range(3)] for i in range(3)]
    c=sp.expand(sum(T[i][j][k]*V[i]*V[j]*V[k] for i in range(3) for j in range(3) for k in range(3)))
    # binary forms in (u,v) of formal degrees 2 and 3: Sylvester resultant via dehomogenized polys with formal degree
    qa=[sp.expand(q).coeff(u,2-i).coeff(v,i) for i in range(3)]
    ca=[sp.expand(c).coeff(u,3-i).coeff(v,i) for i in range(4)]
    M=sp.zeros(5,5)
    for r in range(2):
        for i in range(4): M[r,r+i]=ca[i]
    for r in range(3):
        for i in range(3): M[2+r,r+i]=qa[i]
    return sp.expand(M.det(method='berkowitz'))
# ruled cubic: Whitney umbrella x^2 = y^2 z, param (s r, s, r^2)
F1=x**2-y**2*z
R1=Rpoly(F1); s,r=sp.symbols('s r')
print('umbrella: deg R =',sp.Poly(R1,x,y,z).total_degree(),' bound 17d-24 =',17*3-24,' R on surface =',sp.simplify(R1.subs({x:s*r,y:s,z:r**2})))
# non-ruled cubic: Fermat x^3+y^3+z^3-1 ; check R not divisible by F at random surface points
F2=x**3+y**3+z**3-1
R2=Rpoly(F2)
print('fermat: deg R =',sp.Poly(R2,x,y,z).total_degree())
random.seed(3); vals=[]
for _ in range(3):
    a,b=sp.Rational(random.randint(1,9),7),sp.Rational(random.randint(1,9),5)
    zz=sp.nsolve(F2.subs({x:a,y:b}),z,0.5+0.5j) if False else None
    rts=sp.Poly(F2.subs({x:a,y:b}),z).nroots()
    vals.append(complex(R2.subs({x:a,y:b,z:rts[0]}).evalf()))
print('fermat: |R| at 3 generic surface points =',[abs(t) for t in vals])
# on a line of the Fermat cubic: (t, -t, 1)?  x^3+y^3+z^3-1 = t^3 - t^3 + 1 - 1 = 0
t=sp.symbols('t')
print('fermat: R on line (t,-t,1) =',sp.simplify(R2.subs({x:t,y:-t,z:1})))
