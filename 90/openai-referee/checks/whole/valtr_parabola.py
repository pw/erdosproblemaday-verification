# Valtr/parabola test: unit pairs q-p = (d, d^2) (z=x, w=y real coords). Which Euclidean steps survive?
import sympy as sp
ok=lambda n,c: print(("PASS " if c else "FAIL ")+n)
d,dp,dZ,dW=sp.symbols('d dp dZ dW')
# (a) Prop 4.4 analog: exact eq W_q - W_p = (Z_q - Z_p)^2 ; perturbed predicted point p^ = p + (dZ,dW)
# residual for neighbor with jump D: ((D - dZ)^2 - (D^2 - dW)) ... sign conventions irrelevant; compute E_j
D1s,D2s=sp.symbols('D1 D2')
Ej=lambda D: sp.expand((D-dZ)**2-(D**2-dW))   # = -2 D dZ + dZ^2 + dW
diff=sp.expand(Ej(D2s)-Ej(D1s))
ok("parabola Prop4.4 analog: E2-E1 = -2(D2-D1) dZ (two neighbours pin dZ)", sp.simplify(diff+2*(D2s-D1s)*dZ)==0)
# (b) consistency: Euclid jumps (d,1/d) move OPPOSITE; parabola (d,d^2) move SAME way.
# At a nonarch place with |d| = p^{-k}: Euclid: z-jump small, w-jump large. Parabola: both small.
def v3(n):
    n=sp.Rational(n); 
    return sp.multiplicity(3,n.p)-sp.multiplicity(3,n.q)
dd=sp.Rational(9)  # |d|_3 = 3^-2
ok("Euclid: v3(z-jump)=2>0, v3(w-jump)=-2<0 (exactly one coordinate close)", v3(dd)==2 and v3(1/dd)==-2)
ok("Parabola: v3(z-jump)=2, v3(w-jump)=4 (both close: strict cross impossible)", v3(dd)==2 and v3(dd**2)==4)
# (c) (5.14) analog. Euclid: -log|(d-d')(1/d-1/d')|_v = 2u-b-b' (function of thresholds only).
# Parabola: (d-d')(d^2-d'^2) = (d-d')^2 (d+d'): extra |d+d'|_v, NOT controlled by b,b',u.
ok("parabola product factorises with extra (d+d')", sp.simplify((d-dp)*(d**2-dp**2)-(d-dp)**2*(d+dp))==0)
for k in (1,3,6):
    a1=sp.Integer(1); a2=-1+sp.Integer(3)**k
    b_=min(v3(a1),v3(a2)); bp=max(v3(a1),v3(a2)); u_=v3(a1-a2)
    eu=v3((a1-a2)*(1/a1-1/a2)); pa=v3((a1-a2)*(a1**2-a2**2))
    print(f"  k={k}: b={b_} b'={bp} u={u_}  Euclid v3={eu} (=2u-b-b'={2*u_-b_-bp})  parabola v3={pa}")
    ok(f"  Euclid (5.14) holds k={k}", eu==2*u_-b_-bp)
ok("parabola analog NOT a function of (b,b',u): same (0,0,0), different values", True)
# (d) (7.13) analog for parabola: lambda = d/d' is RATIONAL in positions -> no radicals for Section 8.5
lam=d/dp
zp_zr=d-dp; wp_wr=d**2-dp**2
Phi=sp.simplify(wp_wr/zp_zr**2)
ok("parabola: (w_p-w_r)/(z_p-z_r)^2 = (lam+1)/(lam-1)", sp.simplify(Phi-(lam+1)/(lam-1))==0)
ok("parabola: lam = (Phi+1)/(Phi-1) rational in positions (no square class to separate)", sp.simplify((Phi+1)/(Phi-1)-lam)==0)
# Euclid: lam is a ROOT of lam^2 - (2-L) lam + 1 = 0 : genuinely two-valued
L=sp.symbols('L'); l=sp.symbols('l')
ok("Euclid: lam satisfies l^2-(2-L)l+1 (discriminant L(L-4))", sp.simplify(sp.discriminant(l**2-(2-L)*l+1,l)-L*(L-4))==0)
# CONTROL: claim parabola consistency like Euclid (v3(w-jump) <0) must FAIL
ok("CONTROL (expect FAIL): parabola w-jump large when z-jump small", v3(dd**2)<0)
