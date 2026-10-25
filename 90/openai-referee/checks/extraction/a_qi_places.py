# Exact toy in N = Q(i) (normal, d_N = 2): all places with the weights of Lemma 4.1.
#  archimedean entries: identity and complex conjugation, weight 1/2 each (total 1)
#  finite place P above l: n_P = [N_P:Q_l] copies of weight 1/2, |l|_P = 1/l  =>  |u|_P = l^(-v_P(u)/e_P)
# Checks: unit equations; (7.13) exactly; log|lambda|_v = n_rq(v) - n_pq(v) at every place;
# product formula; 2h(lambda) = sum*|log|lambda|_v|; the (5.14)/(7.1) place identity
#   -log|(d-d')(1/d-1/d')|_v = 2alpha - (b'-b)  and  T_v >= 0  at every place.
from fractions import Fraction as F
import math, itertools

class G:  # Gaussian rational a + b i
    __slots__=("a","b")
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __sub__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a-o.a,s.b-o.b)
    def __rsub__(s,o): return G(o)-s
    def __neg__(s): return G(-s.a,-s.b)
    def __mul__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a*o.a-s.b*o.b, s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def conj(s): return G(s.a,-s.b)
    def norm(s): return s.a*s.a+s.b*s.b
    def inv(s): n=s.norm(); assert n!=0; return G(s.a/n,-s.b/n)
    def __truediv__(s,o): o=o if isinstance(o,G) else G(o); return s*o.inv()
    def __rtruediv__(s,o): return G(o)*s.inv()
    def __eq__(s,o): o=o if isinstance(o,G) else G(o); return s.a==o.a and s.b==o.b
    def iszero(s): return s.a==0 and s.b==0
    def __repr__(s): return "(%s + %s*i)"%(s.a,s.b)

def gauss_divides(pi, u):   # u, pi Gaussian INTEGERS: does pi | u in Z[i]?
    q = u / pi
    return q.a.denominator==1 and q.b.denominator==1

def primes_above(l):
    """list of (pi, e, n_copies) for the Gaussian primes above rational prime l."""
    if l==2: return [(G(1,1), 2, 2)]
    if l%4==3: return [(G(l,0), 1, 2)]
    for a in range(1,int(math.isqrt(l))+1):
        b2=l-a*a; b=math.isqrt(b2)
        if b*b==b2: return [(G(a,b),1,1),(G(a,-b),1,1)]
    raise ValueError

def vpi(u, pi):
    """pi-adic valuation of a nonzero Gaussian rational u."""
    assert not u.iszero()
    den = math.lcm(u.a.denominator, u.b.denominator)
    num = u*den                       # Gaussian integer
    def vint(x):
        v=0
        while gauss_divides(pi, x): x = x/pi; v+=1
        return v
    return vint(num) - vint(G(den))

def relevant_primes(*els):
    ps=set()
    for u in els:
        den = math.lcm(u.a.denominator, u.b.denominator)
        num = u*den                     # Gaussian integer
        for x in (int(num.norm()), den):
            m=x; p=2
            while p*p<=m:
                while m%p==0: ps.add(p); m//=p
                p+=1
            if m>1: ps.add(m)
    ps.add(2)
    return sorted(ps)

def places(primes):
    """list of (name, weight, logabs function)"""
    pl=[("inf_id", F(1,2), lambda u: 0.5*math.log(float(u.norm()))),
        ("inf_conj", F(1,2), lambda u: 0.5*math.log(float(u.conj().norm())))]
    for l in primes:
        for (pi,e,ncop) in primes_above(l):
            for c in range(ncop):
                pl.append(("P%d[%s]#%d"%(l,pi,c), F(1,2),
                           (lambda pi,e,l: (lambda u: -(vpi(u,pi)/e)*math.log(l)))(pi,e,l)))
    return pl

def wsum(pl, f):  # weighted sum over places
    return sum(float(w)*f(name,lg) for (name,w,lg) in pl)

def height(pl,u): return wsum(pl, lambda n,lg: max(0.0, lg(u)))

def unit(m,n): # (m+ni)^2/(m^2+n^2): Gaussian rational of norm 1
    z=G(m,n); return (z*z)/(m*m+n*n)

def pt(x): # point -> (z,w) = (x1+i x2, x1-i x2)
    return (G(x[0],x[1]), G(x[0],-x[1]))

TOL=1e-12
fails=0
# configuration: centre q, neighbours p, r, and a second neighbour q' of p
q = (F(2,7), F(-1,3))
u1, u2, u3 = unit(4,1), unit(5,2), unit(3,2)          # norms 17, 29, 13
p = (q[0]+u1.a, q[1]+u1.b); r = (q[0]+u2.a, q[1]+u2.b)
qq = (p[0]-u3.a, p[1]-u3.b)                             # q' with p - q' = u3
zq,wq = pt(q); zp,wp = pt(p); zr,wr = pt(r); zqq,wqq = pt(qq)
d, dd = zp-zq, zr-zq
assert d*(wp-wq)==1 and dd*(wr-wq)==1 and (zp-zqq)*(wp-wqq)==1, "unit equations"
lam = d/dd
lhs = (zp-zr)*(wp-wr); rhs = 2 - lam - lam.inv()
print("(7.13) exact:", lhs==rhs, " |p-r|^2 =", lhs)
if not lhs==rhs: fails+=1
pl = places(relevant_primes(d,dd,lam, zp-zqq, d-(zp-zqq)))
print("number of place entries:", len(pl), " total weight", sum(w for _,w,_ in pl))
npq = lambda lg: -lg(d); nrq = lambda lg: -lg(dd)
for (name,w,lg) in pl:
    if abs(lg(lam) - (nrq(lg)-npq(lg)))>TOL: fails+=1; print("  FAIL log|lam| at",name)
pf = wsum(pl, lambda n,lg: lg(lam))
h = height(pl, lam); s_abs = wsum(pl, lambda n,lg: abs(lg(lam)))
print("product formula sum* log|lam|_v = %.3e ; 2h(lam) = %.12f ; sum*|log|lam|_v| = %.12f"%(pf, 2*h, s_abs))
if abs(pf)>TOL or abs(2*h-s_abs)>TOL: fails+=1
print("h(lam) = %.6f ;  ||n_pq - n_rq||_1 = %.6f"%(h, wsum(pl, lambda n,lg: abs(npq(lg)-nrq(lg)))))
# (5.14)-type identity of Lemma 7.1 for the point star p with neighbours q, q'
D, DD = zp-zq, zp-zqq
x = (D-DD)*(D.inv()-DD.inv())
for (name,w,lg) in pl:
    nb, nbb = -lg(D), -lg(DD); b, bp = min(nb,nbb), max(nb,nbb)
    u = -lg(D-DD); alpha = u-b
    cv = math.log(2) if name.startswith("inf") else 0.0
    if abs(-lg(x) - (2*alpha-(bp-b)))>TOL: fails+=1; print("  FAIL (5.14) at",name)
    if alpha+cv < -TOL: fails+=1; print("  FAIL T_v>=0 at",name)
print("sum* -log|(d-d')(1/d-1/d')|_v = %.3e (product formula)"%wsum(pl, lambda n,lg: -lg(x)))
# other elements: 2h(u) = sum*|log|u|_v|, h(1/u)=h(u)
for u in [G(3,4)/G(7,0), G(1,1), G(5,12)/G(2,3), lam*lam*G(1,2), x]:
    pl2 = places(relevant_primes(u))
    a, c = 2*height(pl2,u), wsum(pl2, lambda n,lg: abs(lg(u)))
    if abs(a-c)>TOL or abs(height(pl2,u)-height(pl2,u.inv()))>TOL: fails+=1
    print("  u=%-28s 2h=%.10f  sum*|log|=%.10f  h(1/u)=%.10f"%(u, a, c, height(pl2,u.inv())))
print("TOTAL FAILURES:", fails)

# ---------- CONTROLS (must FAIL) ----------
print("\nCONTROL 1: sign-flipped identity log|lam|_v = n_pq - n_rq :",
      sum(1 for (nm,w,lg) in pl if abs(lg(lam)-(npq(lg)-nrq(lg)))>TOL), "places disagree (expect >0)")
plbad = [(n, (F(1) if n.startswith("inf") else w), lg) for (n,w,lg) in pl]  # archimedean weight 1 each
print("CONTROL 2: archimedean weights 1 each -> product formula sum = %.4f (expect !=0)"%wsum(plbad, lambda n,lg: lg(G(3,0))))
print("CONTROL 3: 'h = (1/4) sum*|log|' -> %.6f vs h = %.6f (expect unequal)"%(s_abs/4, h))

# ---------- INDEPENDENT cross-check of h(lam) via the Mahler measure (no place list used) ----------
# lam has |lam|=1 at both archimedean embeddings and lam + 1/lam = 2 - |p-r|^2 (from (7.13)),
# so its minimal polynomial is a x^2 - b x + a with a = denominator; h = (1/2) log M = (1/2) log a.
tr = 2 - lhs.a            # lam + 1/lam, rational
a_lead = tr.denominator; b_mid = tr.numerator
g = math.gcd(a_lead, b_mid)
print("\nMahler cross-check: min poly %d x^2 - %d x + %d ; (1/2)log M = %.12f vs place-sum h = %.12f"
      %(a_lead, b_mid, a_lead, 0.5*math.log(a_lead), h))
assert g==1 and abs(0.5*math.log(a_lead)-h)<1e-12
print("NOTE: a first version of relevant_primes() took primes of the NORM only; it silently dropped the")
print("places above 17 and 29 (norm-1 elements), still passed the product formula and 2h=sum|log| checks,")
print("and reported h(lam)=1.4166 instead of 3.1003. The Mahler cross-check above is what catches that class.")
