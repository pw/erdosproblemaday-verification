# Rectangle cancellation behind (7.15), exact in Q(i).
# An 8-cycle of unit edges p-q1-r-q4-p'-q2-r'-q3-p exists iff u1+u3+u5+u7 = u2+u4+u6+u8 for unit
# Gaussian rationals (p=q1+u1, r=q1+u2, r=q4+u3, p'=q4+u4, p'=q2+u5, r'=q2+u6, r'=q3+u7, p=q3+u8).
# Then lam_pr=u1/u2, lam_p'r=u4/u3, lam_p'r'=u5/u6, lam_pr'=u8/u7 and chi = u1u3u5u7/(u2u4u6u8).
import sys, itertools, random, math
sys.path.insert(0, "/tmp/oaimath/167/checks/extraction")
from a_qi_places import G, F, places, relevant_primes, wsum, height, unit, pt   # (re-runs the toy; harmless)
random.seed(1)
units = set()
for (m,n) in [(2,1),(3,2),(4,1),(4,3),(5,2),(1,2),(2,3),(1,4),(3,4),(2,5)]:
    for sm in (1,-1):
        for sn in (1,-1):
            for sw in (False, True):
                u = unit(sm*m, sn*n); u = G(u.b,u.a) if sw else u
                units.add((u.a,u.b))
units |= {(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))}
units = sorted(units)
print("unit vectors:", len(units))
L = 1
for (a,b) in units: L = math.lcm(L, a.denominator, b.denominator)
iu = [(int(a*L), int(b*L)) for (a,b) in units]
sums = {}
for comb in itertools.combinations_with_replacement(range(len(units)), 4):
    s = (sum(iu[i][0] for i in comb), sum(iu[i][1] for i in comb))
    sums.setdefault(s, []).append(comb)
found = None
for s, lst in sums.items():
    if len(lst) < 2: continue
    for A, B in itertools.combinations(lst, 2):
        if set(A) & set(B): continue
        for pa in itertools.permutations(A):
            for pb in itertools.permutations(B):
                u = [None]*9
                u[1],u[3],u[5],u[7] = [G(*units[i]) for i in pa]
                u[2],u[4],u[6],u[8] = [G(*units[i]) for i in pb]
                q1 = G(0); p = q1+u[1]; r = q1+u[2]; q4 = r-u[3]; pp = q4+u[4]
                q2 = pp-u[5]; rr = q2+u[6]; q3 = rr-u[7]
                assert p == q3+u[8]
                P_ = [p,r,pp,rr]; Q_ = [q1,q2,q3,q4]
                if any(P_[i]==P_[j] for i in range(4) for j in range(i+1,4)): continue
                if any(Q_[i]==Q_[j] for i in range(4) for j in range(i+1,4)): continue
                chi = (u[1]*u[3]*u[5]*u[7])/(u[2]*u[4]*u[6]*u[8])
                if chi == G(1): continue
                found = (u, p, r, pp, rr, q1, q2, q3, q4, chi); break
            if found: break
        if found: break
    if found: break
u, p, r, pp, rr, q1, q2, q3, q4, chi = found
print("p=%s r=%s p'=%s r'=%s\nq1=%s q2=%s q3=%s q4=%s"%(p,r,pp,rr,q1,q2,q3,q4))
def W(zv): return zv.conj()        # real point: w = conj(z)
fails = 0
edges = {("p","r"):(p,r,q1), ("p'","r'"):(pp,rr,q2), ("p","r'"):(p,rr,q3), ("p'","r"):(pp,r,q4)}
lam = {}
for k,(a,b,q) in edges.items():
    for x in (a,b): assert (x-q)*(W(x)-W(q)) == 1      # unit incidences
    lam[k] = (a-q)/(b-q)
    ok = (a-b)*(W(a)-W(b)) == 2 - lam[k] - lam[k].inv()   # (7.13)
    fails += (not ok)
chi2 = lam[("p","r")]*lam[("p'","r'")]/(lam[("p","r'")]*lam[("p'","r")])
assert chi2 == chi
print("(7.13) on all four rectangle edges:", "OK" if fails==0 else "FAIL", "; chi =", chi)
pl = places(relevant_primes(*(list(lam.values())+[chi])))
names = [n for n,_,_ in pl]
# arbitrary unary profiles a_x(v) and the binary defects b_pr(v) = log|lam_pr|_v + a_p(v) - a_r(v)
a = {x:{n:random.uniform(-5,5) for n in names} for x in ["p","r","p'","r'"]}
lg = {n:f for n,_,f in pl}
def b(k,n): return lg[n](lam[k]) + a[k[0]][n] - a[k[1]][n]
# CONTROL: a NON-alternating product lam_pr*lam_pr'/(lam_p'r*lam_p'r') -- unary profiles must NOT cancel.
# (Note: flipping the sign convention of a in b_pr is NOT a valid control: any unary profile cancels
#  around an alternating rectangle whatever its sign; a first version of this script used it and it "passed".)
chi_bad = lam[("p","r")]*lam[("p","r'")]/(lam[("p'","r")]*lam[("p'","r'")])
mx = 0; mxw = 0
for n in names:
    lhs = lg[n](chi)
    rhs = b(("p","r"),n)+b(("p'","r'"),n)-b(("p","r'"),n)-b(("p'","r"),n)
    rhw = b(("p","r"),n)+b(("p","r'"),n)-b(("p'","r"),n)-b(("p'","r'"),n)
    mx = max(mx, abs(lhs-rhs)); mxw = max(mxw, abs(lg[n](chi_bad)-rhw))
print("max_v |log|chi|_v - (b_pr+b_p'r'-b_pr'-b_p'r)(v)| = %.2e   (CONTROL non-alternating product: %.2e, expect >> 0)"%(mx,mxw))
fails += mx > 1e-9
hchi = height(pl, chi); l1 = wsum(pl, lambda n,f: abs(f(chi)))
bnorm = {k: wsum(pl, lambda n,f,k=k: abs(b(k,n))) for k in edges}
print("h(chi) = %.6f ; (1/2) sum*|log|chi|_v| = %.6f ; (1/2)(sum of the four ||b||_1) = %.6f ; 4*max||b||_1/2 = %.6f"
      %(hchi, l1/2, sum(bnorm.values())/2, 2*max(bnorm.values())))
fails += abs(hchi - l1/2) > 1e-9
fails += hchi > sum(bnorm.values())/2 + 1e-9
# independent cross-check of h(chi): Mahler measure of the min poly of chi (|chi|=1 at both embeddings)
tr = chi + chi.inv(); assert tr.b == 0
print("Mahler: min poly %d x^2 - %d x + %d -> (1/2)log %d = %.6f"%(tr.a.denominator, tr.a.numerator, tr.a.denominator, tr.a.denominator, 0.5*math.log(tr.a.denominator)))
fails += abs(0.5*math.log(tr.a.denominator) - hchi) > 1e-9
print("CONTROL: claim h(chi) <= (1/4) sum*|log|chi|_v| ->", hchi <= l1/4 + 1e-12, "(expect False)")
print("TOTAL FAILURES:", fails)
