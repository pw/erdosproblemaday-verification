# Seat S: exact toy check of the sharpened proportional-pair bound (claim 1, seat G finding 1)
#   Pr(pi(u)=pi(v)) <= 2 * M^-k * s^-1 * maxcount * (hq/N)^6
# where maxcount = max over residue pairs of #proportional lift pairs (<= C N^3, the residue-blind count),
# in a Blinov-shaped toy: rows 1,2 deterministic given the label (L1=L2=r), row 3 fresh digits in [1,L3],
# M = L3/r choices each, G_h uniform-ish fixed in SL3(Z/h), V = G_q(a+S) slab cap, u mod q uniform on V.
# Everything is enumerated exactly with Fractions.  Also checks the three sub-claims separately:
#   (alpha) Pr(c'_3 = c'_1 c_1^-1 c_3 mod h) <= M^-k,  (beta) Pr(v_q in F_q u_q) <= 2/s,
#   containment {proportional lifts} subset of alpha&beta, independence Pr(a&b)=Pr(a)Pr(b).
# Usage: python3 -I prop_toy.py <seed> <K> <labels:1|4> [mutation]
#   mutations: none | bigL (L3 > B) | stale (row 3 a function of the label) | noncap (V has 3 pts on a line thru 0)
#              | zeroinV | wrongalpha (test c'_3 = c_3 instead) | tightclaim (claim M^-(k+1) instead of M^-k)
import sys, random, math
from fractions import Fraction as F
from collections import defaultdict
seed, K, nlab = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
mut = sys.argv[4] if len(sys.argv) > 4 else "none"
rng = random.Random(seed)
B, k, r = 11, 2, 2
h = B**k
M = 4; L3 = r*M
if mut == "bigL": M = 12; L3 = r*M          # L3 = 24 > B = 11
q, nu, w = 7, 3, 3                          # 3 is a nonsquare mod 7
assert pow(nu, (q-1)//2, q) == q-1
N = h*q*K
def inv(a, m): return pow(a % m, -1, m)
def det3(G, m):
    a = G
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])) % m
def matvec(G, x, m): return tuple(sum(G[i][j]*x[j] for j in range(3)) % m for i in range(3))
# G_h in SL3(Z/h)
while True:
    G = [[rng.randrange(h) for _ in range(3)] for _ in range(3)]
    d = det3(G, h)
    if math.gcd(d, h) == 1:
        di = inv(d, h); G[0] = [(x*di) % h for x in G[0]]; assert det3(G, h) == 1; break
# labels and deterministic top rows; residues are arbitrary functions of the label (as in the construction)
labels = [(0, 0), (0, 1), (1, 0), (1, 1)][:nlab]
def dig(res, L): return r if res % r == 0 else res % r      # L1 = L2 = r: unique digit in [1,r]
def column(lab, d3):
    l0, l1 = lab
    row1 = [1, dig(l0 + l1, r)]                 # position 0: residue 1 -> digit 1 (c_1 a unit)
    row2 = [dig(l0, r), dig(l1, r)]             # tags
    c1 = sum(x * B**v for v, x in enumerate(row1)) % h
    c2 = sum(x * B**v for v, x in enumerate(row2)) % h
    c3 = sum(x * B**v for v, x in enumerate(d3)) % h
    return (c1, c2, c3)
def row3_choices(lab):
    res = [lab[0]*lab[1] % r, lab[1] % r]       # prescribed residues of the bottom digits
    if mut == "stale":
        return [tuple(next(x for x in range(1, L3+1) if x % r == res[v]) for v in range(k))]
    per = [[x for x in range(1, L3+1) if x % r == res[v]] for v in range(k)]
    assert all(len(p) == M for p in per)
    out = [()]
    for p in per: out = [o + (x,) for o in out for x in p]
    return out
cols = defaultdict(F)                           # distribution of the digit column c
for lab in labels:
    ch = row3_choices(lab)
    for d3 in ch: cols[column(lab, d3)] += F(1, len(labels) * len(ch))
# auxiliary cap
S = [(x, y, (x*x - nu*y*y) % q) for x in range(w) for y in range(q)]
def collinear(p, a, b):
    u = [(a[i]-p[i]) % q for i in range(3)]; v = [(b[i]-p[i]) % q for i in range(3)]
    return all((u[i]*v[j]-u[j]*v[i]) % q == 0 for i in range(3) for j in range(3))
while True:
    a1 = rng.randrange(q)
    if all((a1 + x) % q for x in range(w)): break
a = (a1, rng.randrange(q), rng.randrange(q))
while True:
    Gq = [[rng.randrange(q) for _ in range(3)] for _ in range(3)]
    if det3(Gq, q): break
V = sorted({matvec(Gq, tuple((a[i]+p[i]) % q for i in range(3)), q) for p in S})
if mut == "noncap":   # replace V by points on lines through 0, three per line
    base = V[:7]; V = sorted({tuple((t*x) % q for x in b) for b in base for t in (1, 2, 3)})
if mut == "zeroinV": V = sorted(set(V[:-1]) | {(0, 0, 0)})
s = len(V)
iscap = not any(collinear(V[i], V[j], V[l]) for i in range(s) for j in range(i+1, s) for l in range(j+1, s))
print(f"seed={seed} K={K} labels={nlab} mut={mut}: B={B} k={k} h={h} M={M} L3={L3} q={q} s={s} N={N} cap={iscap} 0inV={(0,0,0) in V} |supp c|={len(cols)}")
# exact sub-claims
def alpha(c, cp):
    if mut == "wrongalpha": return cp[2] % h == c[2] % h
    return (cp[2] - cp[0] * inv(c[0], h) * c[2]) % h == 0
def minors_vanish(x, y, m): return all((x[i]*y[j]-x[j]*y[i]) % m == 0 for i in range(3) for j in range(i+1, 3))
def beta(v, vp):
    return minors_vanish(v, vp, q)              # rank(v|v') <= 1 mod q  (= v' on the line F_q v when v != 0)
PA = sum(p*pp for c, p in cols.items() for cp, pp in cols.items() if alpha(c, cp))
PB = F(sum(1 for v in V for vp in V if beta(v, vp)), s*s)
PAB = sum(p*pp for c, p in cols.items() for cp, pp in cols.items() if alpha(c, cp)) * PB  # independence => product
# lifts: outcome = (c, v);  residue mod hq via CRT, K^3 lifts in [0,N)^2 x [N,2N)
def crt(xh, xq): return (xh * q * inv(q, h) + xq * h * inv(h, q)) % (h*q)
def lifts(c, v):
    rh = matvec(G, c, h)
    x0 = [crt(rh[i], v[i]) for i in range(3)]
    for e1 in range(K):
        for e2 in range(K):
            for e3 in range(K):
                yield (x0[0] + h*q*e1, x0[1] + h*q*e2, N + x0[2] + h*q*e3)
def prim(u):
    g = math.gcd(math.gcd(u[0], u[1]), u[2]); return (u[0]//g, u[1]//g, u[2]//g)
outcomes = [(c, v, p / s) for c, p in cols.items() for v in V]
zmap = defaultdict(list)                        # direction -> [(outcome index, multiplicity)]
for oi, (c, v, p) in enumerate(outcomes):
    cnt = defaultdict(int)
    for u in lifts(c, v): cnt[prim(u)] += 1
    for z, m in cnt.items(): zmap[z].append((oi, m))
Pprop = F(0); paircount = defaultdict(int); distinct_ratio = 0
for z, lst in zmap.items():
    for (o1, m1) in lst:
        for (o2, m2) in lst:
            paircount[(o1, o2)] += m1 * m2
            if o1 != o2: distinct_ratio += m1 * m2
maxcount = max(paircount.values())
contain_viol = 0; minor_viol = 0
for (o1, o2), cnt in paircount.items():
    c, v, p = outcomes[o1]; cp, vp, pp = outcomes[o2]
    Pprop += p * pp * F(cnt, K**6)
    if not (alpha(c, cp) and beta(v, vp)): contain_viol += 1
    if not minors_vanish(c, cp, h): minor_viol += 1
Mk = F(1, M**k)
if mut == "tightclaim": Mk = F(1, M**(k+1))
bound = 2 * Mk * F(1, s) * F(maxcount, K**6)
Peq = sum(p*p for (c, v, p) in outcomes) * F(1, K**3)    # Pr(u = v) exactly
fails = []
if PA > Mk: fails.append(f"(alpha) Pr={PA} > M^-k={Mk}")
if PB > F(2, s): fails.append(f"(beta) Pr={PB} > 2/s={F(2, s)}")
if contain_viol: fails.append(f"containment violated on {contain_viol} residue pairs with proportional lifts")
if mut != "wrongalpha" and minor_viol: fails.append(f"minors of (c|c') nonzero on {minor_viol} proportional residue pairs")
if Pprop > PA * PB * F(maxcount, K**6): fails.append("Pr(prop) > Pr(alpha&beta)*maxcount/K^6")
if Pprop > bound: fails.append(f"FINAL: Pr(prop)={float(Pprop):.4e} > bound={float(bound):.4e}")
print(f"  Pr(alpha)={float(PA):.5f} (M^-k={float(Mk):.5f})  Pr(beta)={float(PB):.5f} (2/s={2/s:.5f})  "
      f"Pr(prop)={float(Pprop):.4e}  Pr(u=v)={float(Peq):.4e}  bound={float(bound):.4e}  truth/bound={float(Pprop/bound):.3f}  "
      f"maxcount={maxcount}  distinct-outcome proportional lift pairs={distinct_ratio}")
if fails:
    print("  FAIL:", *fails, sep="\n    "); sys.exit(1)
print("  PASS")
