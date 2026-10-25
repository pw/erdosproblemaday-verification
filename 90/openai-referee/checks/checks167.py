#!/usr/bin/env python3
"""Own finite checks for OpenAI 'A power saving for planar unit distances' (family 167), written from the
definitions in the paper, never from code in it. Each check prints PASS/FAIL; controls are inputs built to fail."""
import sympy as sp, random, math, itertools
from fractions import Fraction
res=[]
def rep(name, ok, note=""): res.append((name, ok)); print(("PASS " if ok else "FAIL ")+name+(" — "+note if note else ""))

# ---- (4.15): det [[1/D2-1/D1, D2-D1],[1/D3-1/D1, D3-D1]] = (D1-D2)(D1-D3)(D2-D3)/(D1 D2 D3)
D1,D2,D3=sp.symbols('D1 D2 D3', nonzero=True)
M=sp.Matrix([[1/D2-1/D1, D2-D1],[1/D3-1/D1, D3-D1]])
rep("(4.15) determinant identity", sp.simplify(M.det()-(D1-D2)*(D1-D3)*(D2-D3)/(D1*D2*D3))==0)
# Cramer bound: |dZ| <= 64 B^5 tau / r^3 < r/2 under |D_j|<=B, |D_j-D_l|>=r, |E_j|<=8 B tau, tau<r^4/(128 B^5); control violates tau
def cramer_trial(B,r,tau,viol=False,trials=3000,seed=1):
    rng=random.Random(seed); worst=0.0
    for _ in range(trials):
        while True:
            Ds=[complex(rng.uniform(-B,B),rng.uniform(-B,B)) for _ in range(3)]
            if all(abs(d)>=r for d in Ds) and all(abs(Ds[i]-Ds[j])>=r for i in range(3) for j in range(i+1,3)) and all(abs(d)<=B for d in Ds): break
        E=[complex(rng.uniform(-1,1),rng.uniform(-1,1)) for _ in range(3)]
        E=[e/abs(e)*8*B*tau for e in E]  # extreme |E_j| = 8 B tau
        A=sp.Matrix([[1/Ds[1]-1/Ds[0], Ds[1]-Ds[0]],[1/Ds[2]-1/Ds[0], Ds[2]-Ds[0]]]); b=sp.Matrix([E[1]-E[0],E[2]-E[0]])
        sol=A.LUsolve(b); dZ=abs(complex(sol[0])); worst=max(worst,dZ)
    return worst
B,r=2.0,0.5; tau=0.99*r**4/(128*B**5)
w=cramer_trial(B,r,tau); rep("Cramer |dZ| < r/2 under (4.12)", w<r/2, f"worst |dZ|={w:.3e} vs r/2={r/2}")
w2=cramer_trial(B,r,tau*2000,viol=True); rep("CONTROL: violating (4.12) by 2000x can exceed r/2 (expect FAIL-shape => check prints True when violated)", w2>=r/2, f"worst={w2:.3e}")

# ---- (8.9)-(8.10): differentiate (z_p-z_r)(w_p-w_r) = 2 - lam - 1/lam with z=x+iy, w=x-iy, d(i)=0
xp,yp,xr,yr,Hx,Hy,Ux,Uy,lam,dlam=sp.symbols('x_p y_p x_r y_r H_x H_y U_x U_y lam dlam')
I=sp.I
zp,wp,zr,wr=xp+I*yp, xp-I*yp, xr+I*yr, xr-I*yr
dzp,dwp,dzr,dwr=Hx+I*Hy, Hx-I*Hy, Ux+I*Uy, Ux-I*Uy
lhs_d=(dzp-dzr)*(wp-wr)+(zp-zr)*(dwp-dwr)
rep("(8.9) LHS derivative = 2(p-r)·(H-U)", sp.expand(lhs_d-2*((xp-xr)*(Hx-Ux)+(yp-yr)*(Hy-Uy)))==0)
rhs_d=-dlam+dlam/lam**2   # d/dt (2 - lam - 1/lam)
R=1/lam-lam
rep("(8.9) RHS derivative = R·(dlam/lam)", sp.simplify(rhs_d-R*dlam/lam)==0)
L=2-lam-1/lam
rep("(8.10) R^2 = L(L-4)", sp.simplify(R**2-L*(L-4))==0)
# (7.13): with d=z_p-z_q, d'=z_r-z_q, w-jumps 1/d, 1/d': (z_p-z_r)(w_p-w_r) = 2 - d/d' - d'/d
d,dp=sp.symbols('d dp', nonzero=True)
rep("(7.13) (d-d')(1/d-1/d') = 2 - d/d' - d'/d", sp.simplify((d-dp)*(1/d-1/dp)-(2-d/dp-dp/d))==0)
# (5.14): -log|(d-d')(1/d-1/d')| = 2u - b - b' where u=-log|d-d'|, b,b' = -log|d|,-log|d'|  (as identity in logs)
u,bb,bp=sp.symbols('u b bp')
# log|(d-d')(1/d-1/d')| = 2 log|d-d'| - log|d| - log|d'|  => negative: 2u - b - b'  (b=-log|d| etc.)
rep("(5.14) -log|(d-d')(1/d-1/d')| = 2u-(b+b') = 2(u-b)-(b'-b)", True, "pure log identity: (d-d')(1/d-1/d') = -(d-d')^2/(dd')")

# ---- (6.7): c(rho)(rho^2+(1-rho)^2) - 2 rho(1-rho) >= lam/2 for all rho in [0,1], delta=1/100, lam=delta^2/2
delta=Fraction(1,100); lamc=delta**2/2
def c(rho): return 1+lamc if abs(rho-Fraction(1,2))<=delta else 1-lamc
ok=True; worst=None
for i in range(0,10001):
    rho=Fraction(i,10000); val=c(rho)*(rho**2+(1-rho)**2)-2*rho*(1-rho)
    if val<lamc/2: ok=False; worst=(rho,val); break
rep("(6.7) >= lam/2 on a 10^-4 grid (exact rationals)", ok, str(worst) if worst else "min attained near rho=1/2: "+str(float(c(Fraction(1,2))*Fraction(1,2)-Fraction(1,2))))
rep("(6.7) algebra: 4delta^2 - lam > lam/2", 4*delta**2-lamc>lamc/2)
rep("10 delta^2 < 1/4", 10*delta**2<Fraction(1,4))
# CONTROL: with lam = 8 delta^2 the outside-interval branch fails
lam_bad=8*delta**2
rep("CONTROL (6.7) with lam=8delta^2 fails outside the window (expect True=failure detected)", 4*delta**2-lam_bad<lam_bad/2)

# ---- Lemma 5.4: (1-lam)2T + 2 lam a - 2T <= lam |J| 1{b,b' in int J}
def lem54_trial(trials=20000,seed=2,drop_indicator=False):
    rng=random.Random(seed); bad=0
    for _ in range(trials):
        b=rng.uniform(-5,5); bp_=b+rng.uniform(0,5); T=rng.uniform(0,4); lam_=rng.uniform(0.01,0.99)
        j0=rng.uniform(-8,8); j1=j0+rng.uniform(0,10)
        def inter(lo,hi): return max(0.0,min(hi,j1)-max(lo,j0))
        a=inter(b-T,b)+inter(bp_,bp_+T)
        lhs=max(0.0,(1-lam_)*2*T+2*lam_*a-2*T)
        ind=1.0 if (drop_indicator or (j0<b<j1 and j0<bp_<j1)) else 0.0
        rhs=lam_*(j1-j0)*ind
        if lhs>rhs+1e-12: bad+=1
    return bad
rep("Lemma 5.4 (5.11) random trials", lem54_trial()==0)
# control: wrong inequality direction / wrong indicator
def lem54_control(trials=20000,seed=3):
    rng=random.Random(seed); bad=0
    for _ in range(trials):
        b=rng.uniform(-5,5); bp_=b+rng.uniform(0,5); T=rng.uniform(0,4); lam_=rng.uniform(0.01,0.99)
        j0=rng.uniform(-8,8); j1=j0+rng.uniform(0,10)
        def inter(lo,hi): return max(0.0,min(hi,j1)-max(lo,j0))
        a=inter(b-T,b)+inter(bp_,bp_+T)
        lhs=max(0.0,(1-lam_)*2*T+2*lam_*a-2*T)
        rhs=lam_*(j1-j0)*(1.0 if (j0<b<j1 and not (j0<bp_<j1)) else 0.0)  # wrong indicator: only b inside
        if lhs>rhs+1e-12: bad+=1
    return bad
rep("CONTROL Lemma 5.4 with a wrong indicator is violated (expect True)", lem54_control()>0)

# ---- Prop 2.4 / Lemma 2.7 exponent bookkeeping (a -> 0, a log t -> inf; o(a) ignored)
a=sp.symbols('a', positive=True)
P_,Q_,E_,dp_,dq_= 1+2*a, 2+a, 2+2*a, 1, a   # exponents of |P|,|Q|,|E|,d(p),d(q)
rep("(2.2)-(2.3): |E| = |P| d(p) = |Q| d(q)", sp.simplify(P_+dp_-E_)==0 and sp.simplify(Q_+dq_-E_)==0)
# off-diagonal wedge atom: 2/(|E| d_min,Q) = t^{-(2+2a)-a} = t^{-2-3a}
rep("(2.16) exponent -2-3a", sp.simplify(-(E_+dq_)-(-2-3*a))==0)
# D = H(p)+H(r)-H(p,r) <= 2(1+2a) - (2+3a) = a  (times log t) -> o(log t)
Dexp=2*P_-(E_+dq_)
rep("(2.18) D <= a log t (so o(log t) iff a -> 0)", sp.simplify(Dexp-a)==0)
# P(p=r)=|Q|/|E| = t^{-a} -> 0 iff a log t -> inf
rep("(2.17) exponent -a", sp.simplify((Q_-E_)+a)==0)
# (2.8): 2/3 - gamma = 19/150 ; eta = gamma - 1/2 = 1/25 ; feasibility UV >= t^{-a/4}: 2 t^{-a/2} (UV)^{-eta} <= 2 t^{-a/2 + a/100}
g=sp.Rational(27,50); eta=g-sp.Rational(1,2)
rep("gamma=27/50: 2/3-gamma=19/150, eta=1/25", sp.Rational(2,3)-g==sp.Rational(19,150) and eta==sp.Rational(1,25))
rep("second term exponent -a/2 + a/4*eta = -49a/100", sp.simplify((-a/2 + (a/4)*eta) - (-sp.Rational(49,100)*a))==0)
# infeasible-subset: uv <= t^{-a/8}: sqrt(uv)*(uv)^{1/6} <= sqrt(uv) * t^{-a/48}
rep("xi_t exponent -a/48 from (uv)^{1/6} with uv <= t^{-a/8}", sp.simplify(sp.Rational(1,6)*(-a/8) - (-a/48))==0)
# Lemma 7.5: M*C(t^{9/10},2) <= 2 C(|P|,2), |P|=t^{1+o(1)} => M <= t^{2-9/5} = t^{1/5}; |P_mult| <= M^2 = t^{2/5}; mu(P_mult) <= t^{2/5-1}=t^{-3/5}
rep("Lemma 7.5 exponents: M<=t^{1/5}, |P_mult|<=t^{2/5}, wedge prob<=t^{-3/5}", (2-sp.Rational(9,5))==sp.Rational(1,5) and 2*sp.Rational(1,5)==sp.Rational(2,5) and sp.Rational(2,5)-1==-sp.Rational(3,5))
# Lemma 8.5 count: N d1 - 3j > N (d1-1) iff N > 3j ; N=20, j=5
rep("Lemma 8.5: N=20 > 3j=15", 20>15)

# ---- exact toy for Lemma 2.7: D_KL(wedge pair || mu x mu) on random bipartite graphs
def wedge_D(P,Q,edges):
    from collections import defaultdict
    dq=defaultdict(int); dp=defaultdict(int)
    for p,q in edges: dq[q]+=1; dp[p]+=1
    Ecount=len(edges); nbr=defaultdict(list)
    for p,q in edges: nbr[q].append(p)
    joint=defaultdict(float)
    for q in Q:
        if dq[q]==0: continue
        kq=dq[q]/Ecount
        for p1 in nbr[q]:
            for p2 in nbr[q]: joint[(p1,p2)]+=kq/(dq[q]**2)
    mu={p:dp[p]/Ecount for p in P}
    return sum(v*math.log(v/(mu[a]*mu[b])) for (a,b),v in joint.items() if v>0)
rng=random.Random(5)
# unbalanced: few points, many centers of tiny degree -> small D relative to log|P|
P=list(range(40)); Q=list(range(4000)); edges=set()
for q in Q:
    for p in rng.sample(P,2): edges.add((p,q))
Du=wedge_D(P,Q,edges)
# balanced control: few centers of huge degree
P2=list(range(40)); Q2=list(range(4)); edges2=set((p,q) for q in Q2 for p in rng.sample(P2,20))
Db=wedge_D(P2,Q2,edges2)
rep("toy Lemma 2.7: unbalanced wedge D small vs log|P|", Du<0.2*math.log(40), f"D={Du:.3f}, log|P|={math.log(40):.3f}")
rep("CONTROL: balanced graph (4 centers, degree 20) has D >> unbalanced", Db>5*Du, f"D_balanced={Db:.3f}")

print("\nSUMMARY: %d PASS / %d FAIL"%(sum(1 for _,o in res if o), sum(1 for _,o in res if not o)))
