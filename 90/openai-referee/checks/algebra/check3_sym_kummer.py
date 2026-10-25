import sympy as sp
z,w,X = sp.symbols('z w X')
# ---------- (a) symmetry of a real unit circle with non-real centre u = 1+2i ----------
u = 1 + 2*sp.I
ubar = sp.conjugate(u)
f = sp.expand((z-u)*(w-ubar) - 1)          # the real unit circle |p-(1,2)| = 1 in (z,w) coordinates
fbar = lambda P: sp.expand(sp.conjugate(P).subs({sp.conjugate(z):z, sp.conjugate(w):w}))  # conjugate coefficients only
imgA = sp.expand(f.subs({z:w, w:z}, simultaneous=True))           # image under A:(z,w)->(w,z) has equation f(w,z)=0
imgB = sp.expand(fbar(f).subs({z:w, w:z}, simultaneous=True))      # image under B:(z,w)->(wbar,zbar): fbar(w,z)=0
print("eq of image under A:", imgA, "| equals f?", sp.expand(imgA - f) == 0)
print("eq of image under B:", imgB, "| equals f?", sp.expand(imgB - f) == 0)
ok_A = ok_B = 0
for k in range(12):
    th = sp.Rational(k,12)*2*sp.pi
    x, y = 1+sp.cos(th), 2+sp.sin(th)
    zp, wp = x+sp.I*y, x-sp.I*y
    assert sp.simplify(f.subs({z:zp, w:wp})) == 0
    # image points
    zA, wA = wp, zp
    zB, wB = sp.conjugate(wp), sp.conjugate(zp)
    ok_A += sp.simplify(f.subs({z:zA, w:wA})) == 0
    ok_B += sp.simplify(f.subs({z:zB, w:wB})) == 0
    if k == 1: print("  sample real point p=(%s,%s): A-image = %s point (x,-y); B-image fixes p: %s" % (sp.nsimplify(x), sp.nsimplify(y), (sp.simplify(zA), sp.simplify(wA)), sp.simplify(zB-zp)==0 and sp.simplify(wB-wp)==0))
print("real points (of 12) whose A-image stays on the circle:", ok_A, "; B-image:", ok_B)
sol = sp.solve([f, imgA], [z, w], dict=True)
print("common points of the circle and its A-image:", len(sol), "(bounded, so the A-version of the Bezout step would NOT force equality)")
# symmetric under B iff v = ubar ; under A iff v = u
uu, vv = sp.symbols('u v')
g = sp.expand((z-uu)*(w-vv) - 1)
gB = sp.expand(g.subs({z:w, w:z}, simultaneous=True).subs({uu:sp.conjugate(uu), vv:sp.conjugate(vv)}))
print("B-symmetry of (z-u)(w-v)=1 requires coefficient equality:", sp.solve(sp.Poly(g-gB, z, w).coeffs(), [vv], dict=True))
# line z=c: image under B is w=conj(c)
c = sp.Symbol('c')
print("line z-c: B-image equation", sp.expand((z-c).subs({z:w}).subs(c, sp.conjugate(c))))
# ---------- (b) toy Kummer independence: line case (V1=V2 = real axis, w=z), anchors a=0,7,19 ----------
def kummer_poly(Ds, var):
    y1,y2,y3 = sp.symbols('y1 y2 y3')
    e = X - y1 - 2*y2 - 3*y3
    e = sp.resultant(y3**2 - Ds[2], e, y3)
    e = sp.resultant(y2**2 - Ds[1], e, y2)
    e = sp.resultant(y1**2 - Ds[0], e, y1)
    return sp.Poly(sp.expand(e), X)
anchors = [0, 7, 19]
Dl = [sp.expand((z-a)**2*((z-a)**2-4)) for a in anchors]           # L = (z-a)^2 on the line w=z
for S in [[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]:
    prod = sp.Mul(*[Dl[i] for i in S])
    _, fl = sp.factor_list(prod)
    odd = [str(fa) for fa,ex in fl if ex % 2 == 1]
    print("subset", S, "odd-exponent factors:", odd)
P = kummer_poly(Dl, z)
fac = sp.factor_list(P.as_expr(), X, z)
print("line case: deg_X of min-poly candidate =", P.degree(), "; irreducible factors' X-degrees:", [sp.degree(fa, X) for fa,ex in fac[1]])
# control: anchors on the common UNIT circle |z|=1 (u=0,b=1) -> L(L-4) is a square, degree must collapse
zeta = sp.symbols('zeta')
def Lcirc(a, b):  # on (z-u)(w-v)=b with u=v=0 : w = b/z ; anchor abscissa a
    a, b = sp.Integer(a), sp.Integer(b)
    return sp.together((z-a)*(b/z - b/a))
for b in [1, 2]:
    Dc = [sp.together(Lcirc(a, b)*(Lcirc(a, b)-4)) for a in [2, 3, 5]]
    Dc = [sp.expand(sp.numer(d)*sp.denom(d)) for d in Dc]          # same square class, now a polynomial
    Pc = kummer_poly(Dc, z)
    fc = sp.factor_list(Pc.as_expr(), X, z)
    print("circle b=%d: irreducible factors' X-degrees:" % b, sorted(sp.degree(fa, X) for fa,ex in fc[1]))
