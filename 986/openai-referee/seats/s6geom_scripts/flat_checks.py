import sympy as sp
x,y,z=sp.symbols('x y z')
X=[x,y,z]
def Qs(F,q):
    g=[sp.diff(F,v) for v in X]
    Hm=sp.Matrix(3,3,lambda i,j: sp.diff(F,X[i],X[j]))
    gv=sp.Matrix(g)
    e=[sp.Matrix([1,0,0]),sp.Matrix([0,1,0]),sp.Matrix([0,0,1])]
    out=[]
    for i in range(3):
        for j in range(3):
            a=e[i].cross(gv); b=e[j].cross(gv)
            out.append(sp.expand((a.T*Hm*b)[0,0]))
    return out
def divisible_all(F,q):
    PF=sp.Poly(F,*X,modulus=q)
    res=[]
    for Qij in Qs(F,q):
        P=sp.Poly(Qij,*X,modulus=q)
        if P.is_zero: res.append(True); continue
        r=P.rem(PF)  # multivariate remainder is not canonical; use reduced Groebner-free test via sympy div
        res.append(r.is_zero)
    return res
q=7
tests={
 'plane z-2x-3y':z-2*x-3*y,
 'quadric z-xy (doubly ruled)':z-x*y,
 'cubic z-x^3-y':z-x**3-y,
 'z-x^2 (cylinder)':z-x**2,
 'degree q: z-x^7':z-x**7,
 'degree q: z-x^7-y^7':z-x**7-y**7,
}
for name,F in tests.items():
    qs=Qs(F,q)
    allzero=all(sp.Poly(Qij,*X,modulus=q).is_zero for Qij in qs)
    # divisibility test: substitute z = solve for z when F linear in z: F = z - h(x,y)
    h=sp.solve(F,z)[0]
    sub=[sp.Poly(sp.expand(Qij.subs(z,h)),x,y,modulus=q).is_zero for Qij in qs]
    print(f"{name:32s} all Q_ij==0 mod {q}: {allzero};  F | all Q_ij (vanish on branch): {all(sub)}")
