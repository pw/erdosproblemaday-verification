#!/usr/bin/env python3
"""Exact finite checks for Section 5 (Lemma 5.1) and Section 6.1 of
'The weak pinned planar distance theorem' (OpenAI, 23 Sep 2026).
Run:  python3 -I check_variance.py [control]
  no argument      -> all checks on correct definitions; must print ALL PASS
  control=wrongR   -> R_B with inside-branch probability (k-1)/n instead of k/n; must FAIL
  control=noexcl   -> drop the p>=2/k restriction in (5.7)'s P_B(C^2) >= p^2/2; must FAIL
  control=n2       -> (6.2) at n=2; must FAIL
  control=const1   -> (6.2) with constant 1 instead of 2 at n=3; must FAIL
  control=diagmin  -> min{a1+a2,b1+b2} <= sum_i min{a_i,b_i} (diagonal only); must FAIL
  control=dependent-> (6.4) with Y'=Y (no conditional independence); must FAIL
"""
from fractions import Fraction as F
import random, sys, math

CONTROL = sys.argv[1] if len(sys.argv) > 1 else None
rng = random.Random(604)
FAILS = []
def check(cond, msg):
    if not cond:
        FAILS.append(msg)

# ---------- laws ----------
def nu_law(n, B):
    k = len(B); return {x: (F(1, k) if x in B else F(0)) for x in range(n)}

def PB_law(n, B):
    k = len(B); return {(x, y): F(1, k*(k-1)) for x in B for y in B if x != y}

def pi_law(n):
    return {(x, y): F(1, n*(n-1)) for x in range(n) for y in range(n) if x != y}

def RB_law(n, B):
    """R_B by its sampling definition: X ~ unif(B); w.p. k/n Y ~ unif(B minus X), else Y ~ unif(P minus B)."""
    k = len(B)
    if k == n:
        return pi_law(n)
    pin = F(k, n) if CONTROL != 'wrongR' else F(k-1, n)
    out = [y for y in range(n) if y not in B]
    law = {}
    for x in B:
        for y in B:
            if y != x:
                law[(x, y)] = law.get((x, y), 0) + F(1, k)*pin*F(1, k-1)
        for y in out:
            law[(x, y)] = law.get((x, y), 0) + F(1, k)*(1-pin)*F(1, len(out))
    return law

def cellmass(law, C):
    Cs = set(C); return sum((v for (x, y), v in law.items() if x in Cs and y in Cs), F(0))

def marg(law, n, idx):
    m = {z: F(0) for z in range(n)}
    for (x, y), v in law.items():
        m[(x, y)[idx]] += v
    return m

def signed(n, B):
    D = {}
    for law, c in ((PB_law(n, B), 1), (RB_law(n, B), -2), (pi_law(n), 1)):
        for key, v in law.items():
            D[key] = D.get(key, 0) + c*v
    return D

def H_formula(n, k, b, m):
    p, a = F(b, k), F(m, n)
    return (p-a)**2 + (F(2*k, n)-1)*p*(1-p)/(k-1) - a*(1-a)/(n-1)

# ---------- Check A: R_B marginals, closed forms, (5.4), zero mass / zero marginal sum ----------
nA = 0
for trial in range(400):
    n = rng.randint(2, 9); k = rng.randint(2, n)
    B = sorted(rng.sample(range(n), k))
    C = sorted(rng.sample(range(n), rng.randint(0, n)))
    m = len(C); b = len(set(B) & set(C)); p = F(b, k); a = F(m, n)
    R = RB_law(n, B); PB = PB_law(n, B); pi = pi_law(n)
    check(sum(R.values()) == 1, f"R_B total mass {n,B}")
    check(marg(R, n, 0) == nu_law(n, B), f"R_B first marginal != nu {n,B}")
    check(marg(R, n, 1) == {z: F(1, n) for z in range(n)}, f"R_B second marginal != alpha {n,B}")
    check(cellmass(PB, C) == p*p - p*(1-p)/(k-1), f"P_B(C^2) formula {n,B,C}")
    check(cellmass(R, C) == a*p - F(k, n)*p*(1-p)/(k-1), f"R_B(C^2) formula {n,B,C}")
    check(cellmass(R, C) == p*(F(k, n)*F(b-1, k-1) + F(m-b, n)) or k == n, f"R_B(C^2) first form {n,B,C}")
    check(cellmass(pi, C) == a*a - a*(1-a)/(n-1), f"pi(C^2) formula {n,B,C}")
    D = signed(n, B)
    check(cellmass(D, C) == H_formula(n, k, b, m), f"(5.4) {n,B,C}")
    if m <= 1:
        check(cellmass(D, C) == 0 and H_formula(n, k, b, m) == 0, f"singleton exact zero {n,B,C}")
    check(sum(D.values()) == 0, f"signed total mass {n,B}")
    mx, my = marg(D, n, 0), marg(D, n, 1)
    check(all(mx[z] + my[z] == 0 for z in range(n)), f"signed marginal sum {n,B}")
    # zero integral against ANY additive kernel b* + S(x) + S(y)
    bstar = F(rng.randint(-20, 20), rng.randint(1, 7)); S = [F(rng.randint(0, 30), rng.randint(1, 5)) for _ in range(n)]
    check(sum(v*(bstar + S[x] + S[y]) for (x, y), v in D.items()) == 0, f"additive kernel integral {n,B}")
    nA += 1

# ---------- hierarchy machinery (one 'place': nested partitions at rational levels) ----------
def random_hierarchy(n):
    """Q_0={P} refined successively down to singletons at levels r_0<r_1<...; Pi(r)=Q_t for r in (r_{t-1}, r_t],
    Pi(r)={P} for r<=r_0, singletons for r>r_{T-1}.  Returns (levels, partitions, depth)."""
    parts = [[list(range(n))]]
    while any(len(c) > 1 for c in parts[-1]):
        new = []
        for c in parts[-1]:
            c = c[:]; rng.shuffle(c)
            if len(c) > 1 and rng.random() < 0.7:
                cut = sorted(rng.sample(range(1, len(c)), rng.randint(1, min(3, len(c)-1))))
                pieces = [c[i:j] for i, j in zip([0]+cut, cut+[len(c)])]
                new.extend(sorted(pc) for pc in pieces)
            else:
                new.append(sorted(c))
        parts.append(new)
    T = len(parts)-1
    levels = [F(rng.randint(-15, 15), 1)]
    for _ in range(T):
        levels.append(levels[-1] + F(rng.randint(1, 9), rng.randint(1, 4)))
    depth = {}
    for x in range(n):
        for y in range(n):
            if x != y:
                t = max(i for i in range(T+1) if any(x in c and y in c for c in parts[i]))
                depth[(x, y)] = levels[t]
    # pieces: (lo, hi, partition) with Pi(r) = partition on (lo, hi]; plus the coarse ray (-inf, r_0] with {P}
    pieces = [(levels[t-1], levels[t], parts[t]) for t in range(1, T)]  # t=T is singletons beyond r_{T-1}
    return levels, parts, depth, pieces

def transformed(n, part):
    """giant replaced by complement; multiset. Returns (cells, giant or None)."""
    giant = [c for c in part if 2*len(c) > n]
    if not giant:
        return [list(c) for c in part], None
    G = giant[0]
    comp = [z for z in range(n) if z not in G]
    return [comp] + [list(c) for c in part if c is not G], G

def MSL(n, levels, parts, pieces):
    """M, S(x), L(x,y) by their definitions (exact)."""
    r0 = levels[0]
    # giant exists on (-inf, r0] (cell P) and on pieces with a giant
    M = r0
    for lo, hi, part in pieces:
        if transformed(n, part)[1] is not None:
            M = max(M, hi)
    S = [F(0)]*n
    L = {}
    for lo, hi, part in pieces:
        cells, G = transformed(n, part)
        if G is not None:
            for z in range(n):
                if z not in G: S[z] += hi - lo
        for C in cells:
            for x in C:
                for y in C:
                    if x != y: L[(x, y)] = L.get((x, y), 0) + (hi - lo)
    return M, S, L

nB = 0
for trial in range(150):
    n = rng.randint(3, 9)
    levels, parts, depth, pieces = random_hierarchy(n)
    M, S, L = MSL(n, levels, parts, pieces)
    # (3.5): d = M + L - S(x) - S(y)
    for (x, y), d in depth.items():
        check(d == M + L.get((x, y), 0) - S[x] - S[y], f"(3.5) n={n}")
    # per-place version of (5.3): integral over levels of sum_C D(C^2) == E_D[d] == integral of sum_C H_B(C) via (5.4)
    k = rng.randint(2, n); B = sorted(rng.sample(range(n), k)); D = signed(n, B)
    lhs = F(0); lhs_formula = F(0)
    for lo, hi, part in pieces:
        for C in transformed(n, part)[0]:
            lhs += (hi - lo)*cellmass(D, C)
            lhs_formula += (hi - lo)*H_formula(n, k, len(set(B) & set(C)), len(C))
    ED = sum(v*depth[key] for key, v in D.items())
    check(lhs == ED, f"integrated signed cell mass != E_D[d] n={n}")
    check(lhs_formula == ED, f"integrated (5.4) != E_D[d] n={n}")
    nB += 1

# ---------- Check C: (5.5), (5.6) pre-gamma form, (5.7), and the pointwise combination ----------
nC = 0
for trial in range(400):
    n = rng.randint(3, 12)
    fam = []
    for _ in range(rng.randint(1, 4)):
        k = rng.randint(2, n-1) if n > 2 else 2
        fam.append((sorted(rng.sample(range(n), k)), F(rng.randint(1, 5), 1)))
    tot = sum(w for _, w in fam); scale = F(rng.randint(1, 4), 4)  # total weight omega in (0,1]
    fam = [(B, w*scale/tot) for B, w in fam]; omega = sum(w for _, w in fam)
    # M = smallest constant with E_F nu <= M alpha
    Mc = max(sum(w*nu_law(n, B)[x] for B, w in fam)/F(1, n) for x in range(n))
    eps = max([F(1, len(B)-1) for B, _ in fam] + [F(1, n-1)])
    for _ in range(6):
        C = sorted(rng.sample(range(n), rng.randint(0, n)))
        m = len(C); a = F(m, n); piC = a*a - a*(1-a)/(n-1)
        ps = [(F(len(set(B) & set(C)), len(B)), len(B), w) for B, w in fam]
        Hbar = sum(w*H_formula(n, len(B), len(set(B) & set(C)), m) for B, w in fam)
        # Hbar computed directly from the three laws as well
        Hbar2 = sum(w*(cellmass(PB_law(n, B), C) - 2*cellmass(RB_law(n, B), C)) for B, w in fam) + omega*cellmass(pi_law(n), C)
        check(Hbar == Hbar2, "Hbar averaged formula (omega factor)")
        if m >= 2:
            check(a*a/2 <= piC <= a*a, "(5.5)")
            # (5.6) before inserting n^{-gamma}: Hbar >= E(p-a)^2 - eps(M+1)a
            check(Hbar >= sum(w*(p-a)**2 for p, k, w in ps) - eps*(Mc+1)*a, "(5.6) pre-gamma")
            # (5.7): Hbar >= 1/2 E[p^2 1{p>=2/k}] - 4 M pi
            if CONTROL == 'noexcl':
                small = sum(w*p*p for p, k, w in ps)
            else:
                small = sum(w*p*p for p, k, w in ps if p >= F(2, k))
            check(Hbar >= small/2 - 4*Mc*piC, "(5.7)")
            # pieces of (5.7)
            for B, w in fam:
                pb = F(len(set(B) & set(C)), len(B)); kk = len(B)
                if CONTROL == 'noexcl' or pb >= F(2, kk):
                    check(cellmass(PB_law(n, B), C) >= pb*pb/2, "P_B(C^2) >= p^2/2")
                check(cellmass(RB_law(n, B), C) <= a*pb, "R_B(C^2) <= ap")
        else:
            check(Hbar == 0, "m<=1 exact zero (averaged)")
        # pointwise combination with real gamma, c: G <= Hbar + E
        kmin = min(len(B) for B, _ in fam)
        gam = math.log(kmin)/math.log(n)            # so every k >= n^gamma
        c = rng.uniform(0.01, 0.99)*min(gam, 1/3)    # 0 < c < gamma, c < 1/3
        thr = n**(1-c)
        Gc = 0.0
        for p, k, w in ps:
            if m > thr: Gc += float(w*(p-a)**2)
            elif p >= F(2, k): Gc += float(w*p*p)/2
        E = 4*(float(Mc)+1)*n**(c-gam)*float(piC)*(m > thr) + 4*float(Mc)*float(piC)*(2 <= m <= thr)
        check(Gc <= float(Hbar) + E + 1e-12, "pointwise G <= Hbar + errors")
    nC += 1

# ---------- Check D: min inequality ----------
nD = 0
for trial in range(5000):
    a1, a2, b1, b2 = (F(rng.randint(0, 20), rng.randint(1, 5)) for _ in range(4))
    lhs = min(a1+a2, b1+b2)
    rhs = (min(a1, b1)+min(a2, b2)) if CONTROL == 'diagmin' else sum(min(ai, bj) for ai in (a1, a2) for bj in (b1, b2))
    check(lhs <= rhs, f"min inequality {a1,a2,b1,b2}")
    nD += 1

# ---------- Check E: (6.2) from (3.6), W2 = b* + 2A ----------
nE = 0
def check62(n, S, bstar, const=2):
    pairs = [(x, y) for x in range(n) for y in range(n) if x != y]
    Ls = {(x, y): bstar + S[x] + S[y] for x, y in pairs}
    if min(Ls.values()) < 0: return True
    W2 = sum(Ls.values())/len(pairs); A = sum(S)/n
    ok = (W2 == bstar + 2*A)
    for x in range(n):
        avg = sum(Ls[(x, y)] for y in range(n) if y != x)/(n-1)
        ok &= (avg == W2 + F(n-2, n-1)*(S[x]-A))
        ok &= (S[x] >= A - const*W2)
    return ok
if CONTROL == 'n2':
    check(check62(2, [F(0), F(10)], F(-10)), "(6.2) at n=2")
elif CONTROL == 'const1':
    check(check62(3, [F(0), F(1), F(1)], F(-1), const=1), "(6.2) with constant 1 at n=3")
else:
    for trial in range(3000):
        n = rng.randint(3, 10)
        S = [F(rng.randint(0, 40), rng.randint(1, 6)) for _ in range(n)]
        mn = min(S[x]+S[y] for x in range(n) for y in range(n) if x != y)
        bstar = -mn + F(rng.randint(0, 5), rng.randint(1, 5)) * (rng.random() < 0.7)
        check(check62(n, S, bstar), f"(6.2) n={n}")
        nE += 1
    check(check62(3, [F(0), F(1), F(1)], F(-1)), "(6.2) tight example n=3 with constant 2")

# ---------- Check F: layer-cake identity and (6.4) on two random hierarchies ----------
nF = 0
for trial in range(120):
    n = rng.randint(3, 9)
    H = [random_hierarchy(n) for _ in range(2)]
    Ms, Ss, Gpieces = [], [], []
    for levels, parts, depth, pieces in H:
        M, S, L = MSL(n, levels, parts, pieces)
        Ms.append(M); Ss.append(S)
        # giant pieces (lo, hi, G) for r < M  (coarse ray (-inf, r0]: G = P, complement empty)
        gp = [(lo, hi, transformed(n, part)[1]) for lo, hi, part in pieces if transformed(n, part)[1] is not None]
        Gpieces.append(gp)
        # layer cake: {z : S(z) > u} = P \ G(M-u) for u>0 off ties
        for _ in range(5):
            u = F(rng.randint(1, 400), 7) + F(1, 1013)
            r = M - u
            Gr = None
            if r <= levels[0]: Gr = list(range(n))
            for lo, hi, G in gp:
                if lo < r <= hi: Gr = G
            if Gr is None:  # r in a piece without giant cannot happen for r < M (nesting)
                check(False, "giant missing below M"); continue
            check(set(z for z in range(n) if S[z] > u) == set(range(n)) - set(Gr), "layer cake")
    # fiber family
    fam = []
    for _ in range(rng.randint(1, 4)):
        k = rng.randint(2, n-1); fam.append((sorted(rng.sample(range(n), k)), F(rng.randint(1, 5))))
    tot = sum(w for _, w in fam); fam = [(B, w/tot) for B, w in fam]
    Ssum = [Ss[0][z] + Ss[1][z] for z in range(n)]
    lhs = F(0)
    for B, w in fam:
        k = len(B)
        if CONTROL == 'dependent':
            lhs += w*sum(F(1, k)*Ssum[y] for y in B)
        else:
            lhs += w*sum(F(1, k*k)*min(Ssum[y], Ssum[y2]) for y in B for y2 in B)
    rhs = F(0)
    for i in range(2):
        for B, w in fam:
            k = len(B)
            for lo, hi, G in Gpieces[i]:
                if hi <= Ms[i]:
                    comp = set(range(n)) - set(G)
                    rhs += w*(hi-lo)*F(len(comp & set(B)), k)**2
    check(lhs <= 2*rhs, f"(6.4) n={n}: {lhs} vs {2*rhs}")
    nF += 1

# ---------- Check G: w-symmetry makes original and transformed cut sums agree; (6.7) integrand invariance ----------
def wfun(u, d=F(1, 5)):
    if u <= d/2 or u >= 1-d/2: return F(0)
    if d <= u <= 1-d: return F(1)
    return (u - d/2)/(d/2) if u < d else (1-d/2-u)/(d/2)
nG = 0
for trial in range(100):
    n = rng.randint(3, 9); levels, parts, depth, pieces = random_hierarchy(n)
    for lo, hi, part in pieces:
        cells, G = transformed(n, part)
        check(sum(wfun(F(len(c), n)) for c in part) == sum(wfun(F(len(c), n)) for c in cells), "l_j transform invariance")
    for _ in range(20):
        p, a = F(rng.randint(0, 50), 50), F(rng.randint(0, 50), 50)
        f = lambda p, a: abs(wfun(p)-wfun(a)) + wfun(a)*abs(p-a)
        check(f(p, a) == f(1-p, 1-a), "(6.7) integrand symmetry")
    nG += 1

print(f"control={CONTROL}  checksA={nA} hierB={nB} famC={nC} minD={nD} E62={nE} F64={nF} Gw={nG}")
if FAILS:
    from collections import Counter
    print("FAIL:", len(FAILS), "failures; first kinds:", Counter(f.split(' ')[0] + ' ' + ' '.join(f.split(' ')[1:3]) for f in FAILS).most_common())
    sys.exit(1)
print("ALL PASS")
