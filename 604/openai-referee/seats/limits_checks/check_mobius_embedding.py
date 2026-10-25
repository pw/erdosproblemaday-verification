# §7.3 prelimit claim: on a fiber (fixed source x, fixed squared distance t), after the
# normalization U_j = e^{m_j} Z_j + b_j at ANY complex embedding, U_2(z) = Phi(U_1(z)) with
# Phi(w) = b + t'/(w-a), (a,b,a',b') = (U_1(x),U_2(x),U_1(y),U_2(y)) for one fiber edge (x,y).
# Test at a NON-REAL embedding of Q(2^(1/3), i): c=2^(1/3) -> c*omega, i -> i.
from fractions import Fraction as F
import cmath, math, random
random.seed(7)
c_real = 2**(1/3); omega = cmath.exp(2j*math.pi/3)
sig = lambda c0, c1, c2: c0 + c1*(c_real*omega) + c2*(c_real*omega)**2   # sigma(c0 + c1 c + c2 c^2)
ident = lambda c0, c1, c2: c0 + c1*c_real + c2*c_real**2
def circle_pt(s):  # rational point on unit circle
    s = F(s); return ((1-s*s)/(1+s*s), 2*s/(1+s*s))
# source x = (c, c^2); fiber points y = x + c*(p,q): squared distance c^2 for every y
x = ((0,1,0), (0,0,1))
fiber = [((0,1+p,0), (0,q,1)) for (p,q) in (circle_pt(s) for s in (F(1,3),F(2,5),F(-7,4),F(5,11),F(13,2),F(-1,9)))]
nonfiber = ((0,F(3,2),0), (0,F(1,7),1))      # CONTROL: x + c*(1/2,1/7), not on the circle
for emb_name, emb in (("identity (real)", ident), ("c->c*omega (non-real)", sig)):
    Z1 = lambda P: emb(*map(float,P[0])) + 1j*emb(*map(float,P[1]))
    Z2 = lambda P: emb(*map(float,P[0])) - 1j*emb(*map(float,P[1]))
    m1, m2, b1, b2 = 0.37, -1.2, 0.5-0.25j, -2+1j     # arbitrary normalization
    U1 = lambda P: math.exp(m1)*Z1(P) + b1
    U2 = lambda P: math.exp(m2)*Z2(P) + b2
    conj_gap = abs(Z2(fiber[0]) - Z1(fiber[0]).conjugate())
    a, b = U1(x), U2(x); ap, bp = U1(fiber[0]), U2(fiber[0])
    tp = (ap-a)*(bp-b)
    Phi = lambda w: b + tp/(w-a)
    prods = [(U1(y)-a)*(U2(y)-b) for y in fiber]
    target = math.exp(m1+m2)*(emb(0,1,0)**2)          # e^(m1+m2) * sigma(c)^2 = e^(m1+m2) sigma(t), t = c^2
    print(f"[{emb_name}] |Z2 - conj(Z1)| = {conj_gap:.3f}")
    print("   max |(U1(y)-U1(x))(U2(y)-U2(x)) - e^(m1+m2) sigma(t)| over fiber =", max(abs(p-target) for p in prods))
    print("   max |U2(y) - Phi(U1(y))| over fiber =", max(abs(U2(y)-Phi(U1(y))) for y in fiber))
    print("   CONTROL non-fiber point: |U2(z) - Phi(U1(z))| =", abs(U2(nonfiber)-Phi(U1(nonfiber))))
