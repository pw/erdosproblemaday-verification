#!/usr/bin/env python3
"""Exact toy check of Lemma 4.1 (paper pp. 12-14) and its three-case split.

One place (weight 1), two coordinates j=1,2, each with a FIXED realized nested
hierarchy given by an ultrametric 'sharing depth' d_j (Pi_j(r) = classes of
d_j >= r).  Fibers e = (source x_e, target set F_e, constant h_e); the raw-depth
sum i_j+i_j' = h_e on the fiber is (3.3), so Delta_j+Delta_j' = d_j+d_j'-h_e.
All arithmetic is Fraction (exact).  Every level integral is computed exactly as
sum over the open intervals between breakpoints of (value at midpoint)*(length);
on the two unbounded intervals every integrand is asserted to be exactly 0.
"""
from fractions import Fraction as Fr
import random, sys

def ultrametric(n, rng, maxlev=12, den=2):
    cl = [[i] for i in range(n)]
    ts = sorted((Fr(rng.randint(0, maxlev*den), den) for _ in range(n-1)), reverse=True)
    d = {}
    for t in ts:                       # merges at non-increasing depth => ultrametric
        a, b = rng.sample(range(len(cl)), 2)
        for x in cl[a]:
            for y in cl[b]:
                d[(x, y)] = d[(y, x)] = t
        cl = [c for k, c in enumerate(cl) if k not in (a, b)] + [cl[a] + cl[b]]
    return d

def is_ultra(d, n):
    return all(d[(x, z)] >= min(d[(x, y)], d[(y, z)])
               for x in range(n) for y in range(n) for z in range(n)
               if len({x, y, z}) == 3)

def cell(d, n, r, x):
    return frozenset([x] + [z for z in range(n) if z != x and d[(x, z)] >= r])

def partition(d, n, r, strict=True):
    cells = {cell(d, n, r, x) for x in range(n)}
    if strict:  # cells must be disjoint (genuine partition)
        assert sum(len(c) for c in cells) == n, "NOT A PARTITION (hierarchy not nested)"
    return cells

def giant(C, n): return 2*len(C) > n

def family(d, n, r):
    """Transformed multiset C_j(r): actual nongiant cells + complement of giant."""
    P = frozenset(range(n)); fam = []; G = None
    for C in partition(d, n, r):
        if giant(C, n): G = C
        else: fam.append((C, 'act'))
    if G is not None: fam.append((P - G, 'comp'))
    return fam, G

def integrate(fn, bps):
    """Exact integral over R of a piecewise-constant dict-valued fn."""
    b = sorted(set(bps)); tot = {}
    for v in fn(b[0] - 1).values(): assert v == 0, "nonzero on (-inf,b0)"
    for v in fn(b[-1] + 1).values(): assert v == 0, "nonzero on (bK,inf)"
    for lo, hi in zip(b, b[1:]):
        for k, v in fn((lo + hi) / 2).items():
            tot[k] = tot.get(k, 0) + v * (hi - lo)
    return tot

def pos(t): return t if t > 0 else Fr(0)

class Toy:
    def __init__(s, n, d, fibers, lam, tau, H):
        s.n, s.d, s.fib, s.lam, s.tau, s.H = n, d, fibers, lam, tau, H
        s.E = [(x, y) for (x, F, h) in fibers for y in F]
        assert len(set(s.E)) == len(s.E)
        s.q = Fr(1, len(s.E)); s.B0 = Fr(n*(n-1), len(s.E))   # q <= B0*pi exactly
        s.w = [Fr(len(F), len(s.E)) for (x, F, h) in fibers]
        s.P = frozenset(range(n))
    def mu(s, F, C): return Fr(len(F & C), len(F))

    # ---------- global (occurrence-level) quantities for coordinate j ----------
    def glob(s, j):
        n, d, lam, tau = s.n, s.d[j], s.lam, s.tau
        Gl = {}  # giant at midpoint levels, for S_j
        def fn(r):
            fam, G = family(d, n, r)
            o = dict(W2=0, Acomp=0, EqL=0, EqLng=0, Tlarge=0, Tcomp=0, Tact=0,
                     comp_a_small=0, large_bound=0, S=[0]*n)
            for C, kind in fam:
                m = len(C); a = Fr(m, n); pi = Fr(m*(m-1), n*(n-1))
                qC = s.q * sum(1 for (x, y) in s.E if x in C and y in C)
                t = sum(wi*s.mu(F, C) for wi, (x, F, h) in zip(s.w, s.fib)
                        if x in C and s.mu(F, C) < lam)
                o['W2'] += pi; o['EqL'] += qC
                if kind == 'act': o['EqLng'] += qC
                else: o['Acomp'] += a
                if a >= tau:
                    o['Tlarge'] += t; o['large_bound'] += 2*lam*pi/tau**2
                    assert m >= 2 and t <= lam <= 2*lam*pi/tau**2   # (4.3) step
                elif kind == 'comp':
                    o['Tcomp'] += t; o['comp_a_small'] += a
                    assert t <= qC <= s.B0*pi <= s.B0*tau*a
                else:
                    o['Tact'] += t
            S = [Fr(1) if (G is not None and z not in G) else Fr(0) for z in range(n)]
            o['S'] = 0; o.update({('S', z): S[z] for z in range(n)})
            return o
        bps = list(d.values())
        res = integrate(fn, bps)
        res['A'] = sum(res[('S', z)] for z in range(n)) / n
        return res

    def Lng(self, j, x, y):
        """int 1{x,y share a NONGIANT actual j-cell at level r} dr."""
        n, d = self.n, self.d[j]
        def fn(r):
            C = cell(d, n, r, x)
            return {'L': Fr(1) if (y in C and not giant(C, n)) else Fr(0)}
        return integrate(fn, list(d.values())).get('L', 0)

    # ---------- per-fiber three-case split for coordinate j ----------
    def fiber(s, j, e, stats):
        n, lam, tau, H = s.n, s.lam, s.tau, s.H
        dj, dk = s.d[j], s.d[3 - j]
        x, F, h = s.fib[e]
        def fn(r):
            U = cell(dj, n, r, x); p = s.mu(F, U)
            Vm = cell(dk, n, h - r - H, x); Vp = cell(dk, n, h - r + H, x)
            assert Vp <= Vm                                   # V+ subset V-
            Dm = s.mu(F, s.P - (U | Vm)); Dp = s.mu(F, U & Vp)
            ret = (not giant(U, n)) and Fr(len(U), n) < tau and p < lam
            case = 1 if not giant(Vm, n) else (2 if not giant(Vp, n) else 3)
            o = dict(tot=p if ret else 0, c1=0, c2=0, c3=0, Dm=Dm, Dp=Dp,
                     Vm_ng=(s.mu(F, Vm) if not giant(Vm, n) else 0),
                     c1_Dm=0, c3_Dp=0, c3_rest=0, c2_raw=Fr(1) if case == 2 else 0)
            if ret:
                o['c%d' % case] = p
                if case == 1:
                    assert 1 - p <= s.mu(F, Vm) + Dm                 # cover
                    assert p <= 2*lam*(s.mu(F, Vm) + Dm)            # Case 1
                    o['c1_Dm'] = Dm
                    if not p <= lam*(s.mu(F, Vm) + Dm): stats['C3viol'] += 1
                    stats['n1'] += 1
                elif case == 2: stats['n2'] += 1
                else:
                    assert p == s.mu(F, U - Vp)                # Case 3 identity
                    o['c3_Dp'] = Dp; o['c3_rest'] = s.mu(F, U - Vp)
                    if p > 0: stats['n3'] += 1
            return o
        bps = []
        for z in range(n):
            if z != x:
                bps += [dj[(x, z)], h - H - dk[(x, z)], h + H - dk[(x, z)]]
        I = integrate(fn, bps)
        # exact identities of the proof
        Ey = lambda f: sum(f(y) for y in F) / len(F)
        S = lambda y: dj[(x, y)] + dk[(x, y)] - h                  # = Delta_j + Delta_j'
        assert I['Dm'] == Ey(lambda y: pos(h - dj[(x, y)] - dk[(x, y)] - H))
        assert I['Dp'] == Ey(lambda y: pos(dj[(x, y)] + dk[(x, y)] - h - H))
        assert I['Dm'] + I['Dp'] == Ey(lambda y: pos(abs(S(y)) - H))   # (4.4) integrand
        assert I['c2_raw'] == 2*H          # straddle set has length EXACTLY 2H
        assert I['c2'] <= 2*lam*H          # Case 2 bound
        assert I['tot'] == I['c1'] + I['c2'] + I['c3']
        assert I['c3'] == I['c3_Dp'] + I['c3_rest']
        # level change r' = h - r - H: int mu(V-)1{V- nongiant} dr = E_y L^ng_{j'}(x,y)
        assert I['Vm_ng'] == Ey(lambda y: s.Lng(3 - j, x, y))
        return I

    def Nj(s, j, y):
        n, d = s.n, s.d[j]
        vals = sorted({d[(y, z)] for z in range(n) if z != y})
        cells = [cell(d, n, v, y) for v in vals] + [frozenset([y])]
        small = [C for C in cells if len(C) < s.tau*n]
        for A in small:
            for B in small: assert A <= B or B <= A          # nested chain
        N = frozenset().union(*small)
        assert len(N) < s.tau*n
        return N

    def case3_levelchange(s, j, Igl):
        """Pointwise in r' = h_e - r + H: fiber-summed Case-3 mass <= the
        N_j(y) double sum <= B0*tau*alpha(P minus G_j'(r'))."""
        n, H, dk = s.n, s.H, s.d[3 - j]
        N = {y: s.Nj(j, y) for y in range(n)}
        def fn(rp):
            lhs = 0
            for e, (x, F, h) in enumerate(s.fib):
                r = h - rp + H
                U = cell(s.d[j], n, r, x); p = s.mu(F, U)
                Vm = cell(dk, n, h - r - H, x); Vp = cell(dk, n, h - r + H, x)
                ret = (not giant(U, n)) and Fr(len(U), n) < s.tau and p < s.lam
                if ret and giant(Vp, n):
                    lhs += s.w[e]*s.mu(F, U - Vp)
            fam, G = family(dk, n, rp)
            if G is None: r1 = r2 = Fr(0)
            else:
                r1 = sum(s.q for (x, y) in s.E if y not in G and x in N[y] and x != y)
                r2 = s.B0*s.tau*Fr(n - len(G), n)
            assert lhs <= r1 <= r2, (lhs, r1, r2)
            return dict(lhs=lhs, r1=r1, r2=r2)
        bps = list(dk.values())
        for e, (x, F, h) in enumerate(s.fib):
            for z in range(n):
                if z != x:
                    for b in (s.d[j][(x, z)], h - H - dk[(x, z)], h + H - dk[(x, z)]):
                        bps.append(h - b + H)
        return integrate(fn, bps)

def run_instance(seed, stats):
    rng = random.Random(seed)
    n = rng.randint(9, 15)
    d = {1: ultrametric(n, rng), 2: ultrametric(n, rng)}
    assert is_ultra(d[1], n) and is_ultra(d[2], n)
    fibers = []
    for x in rng.sample(range(n), rng.randint(3, n)):
        others = [z for z in range(n) if z != x]; rng.shuffle(others)
        k = 0
        while k < len(others) - 3 and rng.random() < 0.7:
            sz = rng.randint(3, min(9, len(others) - k)); F = frozenset(others[k:k+sz]); k += sz
            sums = sorted(d[1][(x, y)] + d[2][(x, y)] for y in F)
            h = sums[len(sums)//2] + Fr(rng.randint(-4, 4), 2)
            fibers.append((x, F, h))
    if not fibers: return None
    lam = rng.choice([Fr(1, 5), Fr(1, 3), Fr(2, 5), Fr(49, 100)])
    tau = max(Fr(2, n), rng.choice([Fr(2, n), Fr(1, 4), Fr(3, 8), Fr(1, 2), Fr(1)]))
    H = rng.choice([Fr(0), Fr(1, 2), Fr(1), Fr(2)])
    t = Toy(n, d, fibers, lam, tau, H)
    G = {j: t.glob(j) for j in (1, 2)}
    T = W2 = A = EqL = 0; act_fiber = 0; ERRm = ERRp = ERR44 = 0
    c = dict(c1=0, c2=0, c3=0, c1main=0, c1err=0, c3err=0, c3rest=0)
    for j in (1, 2):
        g = G[j]; k = 3 - j
        assert g['Acomp'] == g['A']                 # int of a over complements = A
        assert g['Tlarge'] <= g['large_bound']
        assert g['Tcomp'] <= t.B0*t.tau*g['comp_a_small'] <= t.B0*t.tau*g['A']
        T += g['Tlarge'] + g['Tcomp'] + g['Tact']; W2 += g['W2']; A += g['A']; EqL += g['EqL']
        for e in range(len(fibers)):
            I = t.fiber(j, e, stats); we = t.w[e]
            act_fiber += we*I['tot']
            for key in ('c1', 'c2', 'c3'): c[key] += we*I[key]
            c['c1main'] += we*2*t.lam*I['Vm_ng']; c['c1err'] += we*2*t.lam*I['c1_Dm']
            c['c3err'] += we*I['c3_Dp']; c['c3rest'] += we*I['c3_rest']
            ERRm += we*I['Dm']; ERRp += we*I['Dp']
            x, F, h = fibers[e]
            ERR44 += we*sum(pos(abs(d[j][(x, y)] + d[k][(x, y)] - h) - H) for y in F)/len(F)
        L3 = t.case3_levelchange(j, g)
        c3j = sum(t.w[e]*t.fiber(j, e, {'C3viol':0,'n1':0,'n2':0,'n3':0})['c3_rest'] for e in range(len(fibers)))
        assert L3['lhs'] == c3j                     # level change r'=h-r+H preserves the integral
        assert L3['r2'] == t.B0*t.tau*G[k]['A']     # integrates to B0 tau A_{j'}
        if L3['r2'] > 0: stats['c3ratio'] = max(stats['c3ratio'], float(L3['lhs']/L3['r2']))
    assert act_fiber == G[1]['Tact'] + G[2]['Tact']   # occurrence sum == per-fiber sum
    assert ERRm + ERRp == ERR44
    assert EqL <= t.B0*W2                           # q <= B0 pi
    assert c['c1'] <= c['c1main'] + c['c1err']
    assert c['c1main'] <= 2*t.lam*EqL
    assert c['c2'] <= 4*t.lam*t.H
    if c['c1main'] + c['c1err'] > 0: stats['c1ratio'] = max(stats['c1ratio'], float(c['c1']/(c['c1main'] + c['c1err'])))
    if t.H > 0: stats['c2ratio'] = max(stats['c2ratio'], float(c['c2']/(4*t.lam*t.H)))
    assert c['c3'] == c['c3err'] + c['c3rest']
    bound = (2*t.lam*W2/t.tau**2 + t.B0*t.tau*A                 # large + complements
             + 2*t.lam*t.B0*W2 + 2*t.lam*ERRm                    # Case 1
             + 4*t.lam*t.H                                       # Case 2
             + ERRp + t.B0*t.tau*A)                              # Case 3
    assert T <= bound, (T, bound)
    stats['inst'] += 1
    stats['ratio'] = max(stats['ratio'], float(T/bound) if bound else 0)
    for key in ('c1', 'c2', 'c3'):
        if c[key] > 0: stats['pos_' + key] += 1
    return True

def control_C1():
    """Fake fiber violating (3.3): targets have DIFFERENT raw sums h_y."""
    n = 9; rng = random.Random(7)
    d = {1: ultrametric(n, rng), 2: ultrametric(n, rng)}
    x = 0; F = frozenset(range(1, 9)); H = Fr(1)
    hy = {y: d[1][(x, y)] + d[2][(x, y)] + Fr(rng.choice([-3, 3]), 1) for y in F}  # true i1+i2
    he = sorted(hy.values())[len(hy)//2]       # the single level-change constant
    t = Toy(n, d, [(x, F, he)], Fr(2, 5), Fr(1, 2), H)
    I = t.fiber(1, 0, {'C3viol':0,'n1':0,'n2':0,'n3':0})
    true = sum(pos(abs(d[1][(x, y)] + d[2][(x, y)] - hy[y]) - H) for y in F) / len(F)
    return I['Dm'] + I['Dp'], true

def control_C2():
    """Coordinate j NOT nested (balls of a non-ultrametric d): N_j(y0) is large."""
    n = 20; dj = {}; dk = {}
    for a in range(n):
        for b in range(n):
            if a != b:
                dj[(a, b)] = Fr(5) if (0 in (a, b) and 1 <= a + b <= 12) else Fr(0)
                dk[(a, b)] = Fr(10) if (a and b) else Fr(0)
    ultra_j = is_ultra(dj, n)
    fibers = [(k, frozenset(range(n)) - {k}, Fr(5)) for k in range(1, 13)]
    lam, tau, H = Fr(1, 5), Fr(3, 20), Fr(1)
    t = Toy(n, {1: dj, 2: dk}, fibers, lam, tau, H)
    try:
        partition(dj, n, Fr(3)); part_ok = True
    except AssertionError: part_ok = False
    # Case-3 mass with U := ball, bypassing the partition requirement
    lhs = 0
    for e, (x, F, h) in enumerate(fibers):
        def fn(r):
            U = cell(dj, n, r, x); p = t.mu(F, U)
            Vp = cell(dk, n, h - r + H, x)
            ret = (not giant(U, n)) and Fr(len(U), n) < tau and p < lam
            return {'m': t.mu(F, U - Vp) if (ret and giant(Vp, n)) else Fr(0)}
        bps = [Fr(0), Fr(5), h + H - Fr(10), h + H]
        lhs += t.w[e]*integrate(fn, bps).get('m', 0)
    Ak = t.glob(2)['A']
    N0 = frozenset([0] + [k for k in range(1, 13)])   # union of the 'cells' {k,0}
    return ultra_j, part_ok, len(N0), tau*n, lhs, t.B0*tau*Ak

def show_example():
    for seed in range(17750, 20000):
        rng = random.Random(10_000 + seed)
        n = 8
        d = {1: ultrametric(n, rng, maxlev=6), 2: ultrametric(n, rng, maxlev=6)}
        x = 0; F = frozenset(rng.sample(range(1, n), 6))
        sums = sorted(d[1][(x, y)] + d[2][(x, y)] for y in F)
        h = sums[len(sums)//2] + Fr(rng.randint(-2, 2), 2)
        t = Toy(n, d, [(x, F, h)], Fr(2, 5), Fr(1, 2), Fr(1, 2))
        I = t.fiber(1, 0, {'C3viol':0,'n1':0,'n2':0,'n3':0})
        if not (I['c1'] > 0 and I['c2'] > 0 and I['c3_rest'] > 0 and I['Vm_ng'] > 0): continue
        if max(abs(d[1][(x, y)] + d[2][(x, y)] - h) for y in F) > 1: continue
        print("WORKED EXAMPLE (seed %d): n=8, source x=0, F=%s, h_e=%s, lam=2/5, tau=1/2, H=1/2, j=1" % (10_000+seed, sorted(F), h))
        print("  d_1(0,y):", {y: str(d[1][(0, y)]) for y in range(1, n)})
        print("  d_2(0,y):", {y: str(d[2][(0, y)]) for y in range(1, n)})
        print("  Delta_1+Delta_2 on F:", {y: str(d[1][(0, y)] + d[2][(0, y)] - h) for y in sorted(F)})
        bps = sorted(set(sum(([d[1][(0, z)], h - t.H - d[2][(0, z)], h + t.H - d[2][(0, z)]] for z in range(1, n)), [])))
        print("  %-13s %-16s %-6s %-6s %-6s %-5s %-5s %-4s" % ("r-interval", "U", "p", "D-", "D+", "case", "kept", "V+gt"))
        for lo, hi in zip(bps, bps[1:]):
            r = (lo + hi)/2
            U = cell(d[1], n, r, 0); p = t.mu(F, U)
            Vm = cell(d[2], n, h - r - t.H, 0); Vp = cell(d[2], n, h - r + t.H, 0)
            case = 1 if not giant(Vm, n) else (2 if not giant(Vp, n) else 3)
            kept = (not giant(U, n)) and Fr(len(U), n) < t.tau and p < t.lam
            print("  (%5s,%5s) %-16s %-6s %-6s %-6s %-5d %-5s %-4s" % (lo, hi, sorted(U), p, t.mu(F, t.P-(U|Vm)), t.mu(F, U & Vp), case, kept, giant(Vp, n)))
        print("  integrals: total kept p =", I['tot'], "= c1+c2+c3 =", I['c1'], "+", I['c2'], "+", I['c3'])
        print("  Case1 bound 2lam*int mu(V-)1{ng} + 2lam*int_{C1} D- =", 2*t.lam*I['Vm_ng'], "+", 2*t.lam*I['c1_Dm'])
        print("  Case2 bound 2*lam*H =", 2*t.lam*t.H, " (raw straddle length =", I['c2_raw'], "= 2H)")
        print("  Case3: c3 = int_{C3} D+ + int_{C3} mu(U\\V+) =", I['c3_Dp'], "+", I['c3_rest'])
        print("  int D- =", I['Dm'], " int D+ =", I['Dp'], " E(|Delta+Delta'|-H)+ =", I['Dm'] + I['Dp'])
        return
    print("no example found")

if __name__ == '__main__':
    pass
    stats = dict(inst=0, C3viol=0, n1=0, n2=0, n3=0, ratio=0.0, c3ratio=0.0, c1ratio=0.0, c2ratio=0.0,
                 pos_c1=0, pos_c2=0, pos_c3=0)
    seeds = range(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
    for sd in seeds: run_instance(sd, stats)
    print("instances passed (all exact assertions):", stats['inst'])
    print("instances with positive Case-1/2/3 mass:", stats['pos_c1'], stats['pos_c2'], stats['pos_c3'])
    print("retained level-intervals hit, cases 1/2/3:", stats['n1'], stats['n2'], stats['n3'])
    print("max T(lambda)/bound over instances: %.4f" % stats['ratio'])
    print("max Case-3 ratio (level-changed mass / B0 tau A_j'): %.4f" % stats['c3ratio'])
    print("max Case-1 ratio (actual / (2 lam E_q L^ng + 2 lam D-)): %.4f" % stats['c1ratio'])
    print("max Case-2 ratio (actual / 4 lam H): %.4f" % stats['c2ratio'])
    print("SHARPNESS: Case-1 levels violating p <= lam*(mu(V-)+D-) [factor 2 dropped]:", stats['C3viol'])
    a, b = control_C1()
    print("CONTROL C1 (fiber with non-constant i1+i2): int(D-+D+) = %s  vs  E(|Delta+Delta'|-H)+ = %s  -> %s"
          % (a, b, "MATCH (control did not fail!)" if a == b else "MISMATCH: identity rejects a non-fiber"))
    u, po, N, tn, lhs, rhs = control_C2()
    print("CONTROL C2 (non-nested j-'hierarchy'): ultrametric=%s partition=%s |N_j(y0)|=%d vs tau*n=%s;"
          " Case-3 mass %s (=%.4f) vs B0*tau*A_j' %s (=%.4f) -> %s"
          % (u, po, N, tn, lhs, float(lhs), rhs, float(rhs), "BOUND FAILS" if lhs > rhs else "bound holds (control did not fail!)"))
