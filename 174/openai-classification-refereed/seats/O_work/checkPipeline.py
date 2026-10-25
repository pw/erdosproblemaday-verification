# End-to-end exact check of Lemma 3.1 -> Lemma 4.2/4.3 -> Lemma 4.1 on the 2-point set A={0,1} in R^1.
# Tensor certificate: w1=(v=0,u=1), w2=(v=1,u=0), C=[[1,-1/2],[-1/2,0]]:
#   (e1(x)e1)T = C22 (1(x)1)=0, (e2(x)e2)T = (C11+2C12+C22)(1(x)1)=0, G(T)=C11=1.
import itertools, math
from fractions import Fraction as Fr
import sympy as sp

C = [[Fr(1), Fr(-1, 2)], [Fr(-1, 2), Fr(0)]]
# Lambda_1 = {lam : e1(w(lam)) = lam2 = 0},  Lambda_2 = {lam : e2(w(lam)) = lam1+lam2 = 0}
key1 = lambda l: l[1]            # coset of Lambda_1
key2 = lambda l: l[0] + l[1]     # coset of Lambda_2

# --- Lemma 3.1: find nu on a box with (9) and (10) by exact linear algebra
box = [(a, b) for a in range(-2, 3) for b in range(-2, 3)]
nu = sp.symbols('n0:%d' % len(box))
eqs = []
for kf in (key1, key2):
    for val in set(kf(l) for l in box):
        eqs.append(sum(nu[j] for j, l in enumerate(box) if kf(l) == val))
eqs.append(sum(nu))
for a in range(2):
    eqs.append(sum(nu[j]*box[j][a] for j in range(len(box))))
for a in range(2):
    for b in range(2):
        eqs.append(sum(nu[j]*box[j][a]*box[j][b] for j in range(len(box))) - sp.Rational(C[a][b].numerator, C[a][b].denominator))
sol = sp.linsolve(eqs, nu)
assert sol != sp.EmptySet, 'no nu on this box'
part = list(sol)[0]
free = sorted(set().union(*[p.free_symbols for p in part]), key=str)
part = [p.subs({f: 0 for f in free}) for p in part]
NU = {box[j]: Fr(int(sp.numer(part[j])), int(sp.denom(part[j]))) for j in range(len(box)) if part[j] != 0}
print('Lemma 3.1 nu (support %d):' % len(NU), NU)

# --- Lemma 4.2: b_* = int_0^1 phi_{S+tC} dt, S = eps P_H + L P_V (H = span e1 = im U^T, V = span e2)
eps, Lv = 0.01, 1.0
Cf = [[float(x) for x in r] for r in C]
def phi(Q, x):
    det = Q[0][0]*Q[1][1] - Q[0][1]*Q[1][0]
    inv = [[Q[1][1]/det, -Q[0][1]/det], [-Q[1][0]/det, Q[0][0]/det]]
    q = x[0]*(inv[0][0]*x[0] + inv[0][1]*x[1]) + x[1]*(inv[1][0]*x[0] + inv[1][1]*x[1])
    return math.exp(-q/2) / (2*math.pi*math.sqrt(det))
def bstar(x, m=64):
    tot = 0.0
    for i in range(m):          # midpoint rule in t
        t = (i + 0.5)/m
        Q = [[eps + t*Cf[0][0], t*Cf[0][1]], [t*Cf[1][0], Lv + t*Cf[1][1]]]
        tot += phi(Q, x)
    return tot/m

n, Rad = 16, 6.0
SCALE = 10**15
# d_n(lam) = n^{2-k} b(lam/n) with k=2, b = b_* truncated to |x|<=Rad (the b_R of the proof; the
# rational-approximation step of Lemma 4.3 then replaces d_n by a nearby rational vector)
d = {}
r = int(Rad*n)
for a in range(-r, r+1):
    for b in range(-r, r+1):
        x = (a/n, b/n)
        if x[0]**2 + x[1]**2 <= Rad**2:
            val = int(round(bstar(x)*SCALE))
            if val: d[(a, b)] = val          # integer = SCALE * rational d
# --- Lemma 4.3: mu = nu * d  (exact; scaled by SCALE * common denominator of nu)
den = math.lcm(*[v.denominator for v in NU.values()])
NUi = {g: int(v*den) for g, v in NU.items()}
mu = {}
for g, vg in NUi.items():
    for l, vl in d.items():
        key = (g[0]+l[0], g[1]+l[1])
        mu[key] = mu.get(key, 0) + vg*vl
mu = {k: v for k, v in mu.items() if v}
# exact checks
for kf, name in ((key1, 'Lambda_1'), (key2, 'Lambda_2')):
    push = {}
    for l, v in mu.items(): push[kf(l)] = push.get(kf(l), 0) + v
    assert all(v == 0 for v in push.values()), name
print('zero pushforward on Gamma/Lambda_1 and Gamma/Lambda_2: exact OK (support %d)' % len(mu))
sd = sum(d.values())
for a in range(2):
    for b in range(2):
        lhs = sum(v*l[a]*l[b] for l, v in mu.items())
        assert Fr(lhs, den) == sd*C[a][b], (a, b)
print('second moment sum mu lam lam^T = (sum d) C: exact OK')
zeta = Fr(sd, SCALE*n*n)                                   # zeta = n^{-2} sum d   (d in true units)
neg = Fr(sum(-v*l[0]*l[0] for l, v in mu.items() if v < 0), den*SCALE*n*n)   # sum mu_- |U lam/n|^2, U=(1,0)
ratio = neg/zeta
print('zeta = %.6f   negative moment / zeta = %.5f   (Lemma 4.2 predicts <= ~tr(USU^T)=eps=%.3f up to discretisation)' % (float(zeta), float(ratio), eps))
eta = Fr(1, 20)
assert ratio < eta
# --- Lemma 4.1: lists; positive list mu_+ copies of w(lam/n) = (v,u) = (lam2/n, lam1/n)
evals = lambda l: (Fr(l[1], n), Fr(l[0] + l[1], n))   # (e1, e2) at a1=0, a2=1
for i in range(2):
    pos, neg_ = {}, {}
    for l, v in mu.items():
        val = evals(l)[i]
        if v > 0: pos[val] = pos.get(val, 0) + v
        else: neg_[val] = neg_.get(val, 0) - v
    assert pos == neg_, i
print('coordinate multisets of f_i and g_i equal for i=1,2 (before common appended rows): exact OK')
Bp = Fr(sum(v*l[0]**2 for l, v in mu.items() if v > 0), den*SCALE*n*n) / zeta
Bm = Fr(sum(-v*l[0]**2 for l, v in mu.items() if v < 0), den*SCALE*n*n) / zeta
print('B_+ - B_- =', Bp - Bm, '  tr B_- = %.5f < eta = %s' % (float(Bm), eta))
q = eta/(1 + eta)
# after appending (0, sqrt(eta - B_-)) to both lists and dividing by sqrt(1+eta):
print('|f1-f2|^2 =', (Bp + (eta - Bm))/(1 + eta), ' |g1-g2|^2 =', (Bm + (eta - Bm))/(1 + eta), ' q =', q)
