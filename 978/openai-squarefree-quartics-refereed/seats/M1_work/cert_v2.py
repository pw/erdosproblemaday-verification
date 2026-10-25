# Seat M1: independent exact re-check of Prop 10.1 / Appendix A, with coverage, direct-range
# and shift checks, plus MUTATION tests (each mutation must make the checker report failure).
import sys, math, random
from fractions import Fraction as F
from math import comb

K0 = 3000
TAU = F(1, 50000)
PREC = 10**30
STOP = F(2495, 10000)

def iroot(n, h):
    if n < 2: return n
    x = 1 << ((n.bit_length() + h - 1)//h)
    while True:
        y = ((h-1)*x + n // x**(h-1)) // h
        if y >= x: break
        x = y
    while x**h > n: x -= 1
    while (x+1)**h <= n: x += 1
    return x

def renc(q, h):
    """rigorous enclosure of q^(1/h)"""
    n = (q.numerator * PREC**h) // q.denominator
    r = iroot(n, h)
    lo, hi = F(r, PREC), F(r+1, PREC)
    assert lo**h <= q < hi**h
    return (lo, hi)

def imax(*iv): return (max(a for a,_ in iv), max(b for _,b in iv))

# Hilbert polynomial R(A,B) of Lemma 5.1, derived independently as the leading part of the
# (d-2)-fold step-(k,1) finite difference of binom(A+d-1,d-1)binom(B+d-1,d-1); we get the
# coefficient list of R(1,t) by exact polynomial arithmetic (no sympy, no paper formula).
def poly_mul(p, q):
    r = [F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q): r[i+j] += a*b
    return r
def leading_R(d):
    # represent bivariate homogeneous polys of degree n as dict {(i,j):coef} with i+j=n (A^i B^j)
    k = d-2
    P = {(d-1, d-1): F(1, math.factorial(d-1)**2)}
    for _ in range(d-2):
        Q = {}
        for (i,j),c in P.items():
            if i>0: Q[(i-1,j)] = Q.get((i-1,j),0) + k*i*c
            if j>0: Q[(i,j-1)] = Q.get((i,j-1),0) + j*c
        P = Q
    return P   # degree d homogeneous
def H_polys(d):
    R = leading_R(d)
    # H(t)=d! R(1,t); Ha=(d-1)! dR/dA(1,t); Hb=(d-1)! dR/dB(1,t)
    H = {}; Ha = {}; Hb = {}
    for (i,j),c in R.items():
        H[j] = H.get(j,0) + math.factorial(d)*c
        if i>0: Ha[j] = Ha.get(j,0) + math.factorial(d-1)*i*c
        if j>0: Hb[j-1] = Hb.get(j-1,0) + math.factorial(d-1)*j*c
    # compare with paper's closed form (5.2)/(10.5)
    for j in range(1, d):
        cj = comb(d,j)*comb(d-2,j-1)*(d-2)**(j-1)
        assert H.get(j,0) == cj, (d,j)
        assert Ha.get(j,0) == F(d-j,d)*cj and Hb.get(j-1,0) == F(j,d)*cj
    return H, Ha, Hb
def ev(p, t): return sum(c*t**e for e,c in p.items())

def thresholds(d, u, v, modeQ, mut):
    k = d-2
    def Psi(h, D):
        return renc((u*v)**h/((k*u+v)**(h-1)*D), h)
    dl = {}
    Dd = u+v if not mut.get('delta_d_min') else min(u, v)
    dl[d] = Psi(d, Dd)
    if modeQ:
        dl[3] = Psi(3, v)
        c3 = mut.get('quadric_const', 3)
        dl[2] = imax(Psi(2, min(3*u, 2*v, u+v)), renc(u*u/c3, 2))
    else:
        for h in range(2, d): dl[h] = Psi(h, min(u, v))
    g = (d-1)*(k-1) + (1 if d == 4 else 0) - (1 if (d == 4 and mut.get('no_quintic')) else 0)
    c1 = max(u/2, min(u, v/g))
    dl[1] = (c1, c1)
    E = {h: imax(*[dl[s] for s in range(h, d+1)]) for h in range(1, d+1)}
    return dl, E

def check_degree(d, mut):
    k = d-2
    H, Ha, Hb = H_polys(d)
    grid = [F(i,50) for i in range(1,500)]
    gv = [(t, ev(H,t), ev(Ha,t), ev(Hb,t)) for t in grid]
    phi = lambda e: e*(1 - k*e/d)
    fails = []
    cells = []
    best = None; bestQ = None; minvu = None; maxvu = None; mincut = None; minslack = None
    z = K0
    while True:
        eL, eH = F(z, K0), F(z+1, K0)
        if mut.get('gap_cell') == (d, z):
            eH = F(z+1, K0) - F(1, 10**6)          # mutation: shrink one cell -> coverage gap
        if phi(eL) < mut.get('stop', STOP):
            zstop = z; break
        bL, bH = d - k*eH, d - k*eL
        # t*: float pre-selection (any t* is legitimate; all inequalities verified exactly below)
        fe, fb = float(eH), float(bH)
        t, Ht, Hat, Hbt = min(gv, key=lambda r: (fe+fb*float(r[0]))**d/float(r[1]))
        x = ((d+1)*(eH+bH*t)/d**2)**d / Ht
        # w = least r/1e5 with w^(d-1) > x
        G0 = 100000
        r = iroot((x.numerator*G0**(d-1))//x.denominator, d-1)
        while F(r,G0)**(d-1) <= x: r += 1
        w = F(r, G0)
        if 'w_scale' in mut and mut['w_scale'][0] == (d, z): w = w*mut['w_scale'][1]
        m = (d-1)*w
        c1 = w**(d-1)*Ht / ((d+1)*(eH+bH*t)/d**2)**d
        c2 = w**(d-2)*min(Hat, Hbt) / ((eH+bH*t)/(d-1))**(d-1)
        if not (c1 > 1 and c2 > 1): fails.append(('cut', d, z, float(c1), float(c2)))
        if not (0 < m < 1 and min(eL, bL) > m): fails.append(('m', d, z))
        u, v = (eH-m)/d, (bH-m)/d
        if not (u > 0 and v > 0 and F(3,20) <= v/u <= 5):
            fails.append(('ratio', d, z, float(v/u))); z += 1; continue
        modeQ = (d == 4 and z < 4000)
        dl, E = thresholds(d, u, v, modeQ, mut)
        sE_hi = sum(E[h][1] for h in E); sE_lo = sum(E[h][0] for h in E)
        gap_lo, gap_hi = 1 - m - sE_hi, 1 - m - sE_lo
        if not gap_lo > F(1,1000): fails.append(('gap', d, z, float(gap_lo)))
        if best is None or gap_lo < best[0]:
            best = (gap_lo, gap_hi, z, dict(t=t, w=w, m=float(m), u=float(u), v=float(v),
                    E=[round(float(E[h][1]),6) for h in sorted(E)]))
        if modeQ:
            q = F(999,1000) - m - 2*u
            if not q > 0: fails.append(('fibre', d, z, float(q)))
            if bestQ is None or q < bestQ[0]: bestQ = (q, z)
        minvu = v/u if minvu is None else min(minvu, v/u)
        maxvu = v/u if maxvu is None else max(maxvu, v/u)
        mc = min(c1, c2); mincut = mc if mincut is None else min(mincut, mc)
        sl = min(eL, bL) - m; minslack = sl if minslack is None else min(minslack, sl)
        cells.append((eL, eH))
        z += 1
    # coverage of [1, zstop/K0] by the cells, endpoints included, no gaps
    if cells:
        cov_ok = cells[0][0] == 1 and cells[-1][1] == F(zstop, K0) and \
                 all(cells[i][1] >= cells[i+1][0] for i in range(len(cells)-1))
    else:
        cov_ok = (zstop == K0)
    if not cov_ok: fails.append(('coverage', d))
    # direct range: phi(zstop/K0) < 0.2495 and phi nonincreasing on [1, d/k]
    if not phi(F(zstop, K0)) < STOP: fails.append(('direct-start', d))
    # phi'(eta)=1-2k eta/d <= 0 for eta>=1 iff d<=2k
    if not d <= 2*k: fails.append(('phi-monotone', d))
    # direct-range weight check, exhaustive over the 1e-4 grid of eta in [zstop/K0, d/k] (+ overshoot pair)
    e = F(1, 10000)
    worst = F(0)
    i0 = (F(zstop, K0)/e).__floor__()
    i1 = (F(d, k)/e).__floor__()
    for i in range(i0, i1+1):
        lo = max(i*e, F(zstop, K0)); hi = min((i+1)*e, F(d, k))
        if lo > hi: continue
        etap = (i+1)*e                       # eta' for eta in [i e,(i+1)e)
        # b = d - k eta ranges over [d-k hi, d-k lo]; b' = e(floor(b/e)+1) <= e(floor((d-k lo)/e)+1)
        bp = e*(((d - k*lo)/e).__floor__() + 1)
        # but the direct range only covers eta with phi(eta)<=0.2495; on the boundary cell lo>=zstop/K0 already
        val = bp*etap/d
        worst = max(worst, val)
    extra = e*(F(d,k)+e)/d
    worst = max(worst, extra)
    if not worst < F(4999,10000)**2: fails.append(('direct-margin', d, float(worst)))
    return dict(fails=fails, zstop=zstop, ncells=len(cells), best=best, bestQ=bestQ,
                minvu=minvu, maxvu=maxvu, mincut=mincut, minslack=minslack, direct_worst=worst)

def check_shift(mut):
    fails = []
    # endpoint checks as in the paper
    for k in range(2, 7):
        for t in [F(3,20), F(5)]:
            for a, b in [(1,0),(0,1),(1,1)]:
                for h in range(2, k+3):
                    N = t*(1 + 1/t - F(h-1,h)*(k+1)/(k+t) - F(1,h)*(a+b)/(a+b*t))
                    if not N**h < (k+t)**(h-1)*(a+b*t): fails.append(('shift-endpoint', k, t, a, b, h))
    # dense numeric confirmation that D(t)<=1 on [3/20,5] (unimodality claim)
    worstD = 0
    for k in range(2, 7):
        for a, b in [(1,0),(0,1),(1,1)]:
            for h in range(2, k+3):
                for i in range(0, 4001):
                    t = 0.15 + (5-0.15)*i/4000
                    f = t/((k+t)**(h-1)*(a+b*t))**(1/h)
                    fp = f*(1/t - (h-1)/h/(k+t) - (b/h)/(a+b*t))
                    D = f + (1-t)*fp
                    worstD = max(worstD, D)
    if worstD > 1: fails.append(('shift-dense', worstD))
    # random direct tests of delta_h(U+s,V+s) <= delta_h(U,V)+s on the actual threshold formulas
    random.seed(1)
    worst = -1
    for _ in range(20000):
        d = random.randint(4, 8); k = d-2
        U = random.uniform(0.01, 0.6); V = U*random.uniform(0.15, 5); s = random.uniform(0, 0.5)
        modeQ = (d == 4 and random.random() < 0.5)
        def dels(U, V):
            P = lambda h, D: U*V/((k*U+V)**(h-1)*D)**(1/h)
            out = [P(d, U+V)]
            if modeQ: out += [P(3, V), max(P(2, min(3*U, 2*V, U+V)), U/3**0.5)]
            else: out += [P(h, min(U, V)) for h in range(d-1, 1, -1)]
            g = (d-1)*(k-1) + (d == 4)
            out.append(max(U/2, min(U, V/g)))
            return out
        a0 = dels(U, V); a1 = dels(U+s, V+s)
        worst = max(worst, max(x1 - x0 - s for x0, x1 in zip(a0, a1)))
    if worst > 1e-12: fails.append(('shift-random', worst))
    return fails, worstD, worst

def run(mut, label, degrees=range(4,9), verbose=True):
    allf = []
    out = {}
    for d in degrees:
        r = check_degree(d, mut)
        out[d] = r
        allf += r['fails']
    sf, wD, wr = check_shift(mut) if mut.get('shift', True) else ([], None, None)
    allf += sf
    print(f"[{label}] {'PASS' if not allf else 'FAIL'}  ({len(allf)} failures)" + (f" first: {allf[:3]}" if allf else ""))
    return out, allf, (wD, wr)

if __name__ == '__main__' and 'mut' not in sys.argv:
    base, f0, (wD, wr) = run({}, 'BASELINE')
    print(f"  shift: max D(t) on [3/20,5] (dense) = {wD:.6f}; max [delta(U+s,V+s)-delta(U,V)-s] random = {wr:.3e}")
    for d in range(4, 9):
        r = base[d]
        gl, gh, z, det = r['best']
        print(f"  d={d}: z_d={r['zstop']} cells={r['ncells']}  min true gap in [{float(gl):.7f},{float(gh):.7f}] at z={z} "
              f"(eta in [{z/K0:.5f},{(z+1)/K0:.5f}]); margin over 1/1000 = {float(gl-F(1,1000)):.7f}; "
              f"final exponent m+sumE+d*tau <= {float(1-gl+d*TAU):.7f}")
        print(f"        at min: {det}")
        if r['bestQ']: print(f"        mode Q: min(999/1000-m-2u) = {float(r['bestQ'][0]):.7f} at z={r['bestQ'][1]}")
        print(f"        v/u in [{float(r['minvu']):.4f},{float(r['maxvu']):.4f}]; min cut ratio {float(r['mincut']):.6f}; "
              f"min (min(eta-,b-)-m) {float(r['minslack']):.5f}; direct worst b'eta'/d = {float(r['direct_worst']):.7f} vs 0.4999^2=0.24990001")
if __name__ == '__main__':
    # ---------------- mutations: each must FAIL ----------------
    print("\nMUTATIONS (each should FAIL):")
    run({'gap_cell': (4, 3500), 'shift': False}, 'M-a: shrink cell z=3500 (d=4) by 1e-6 -> coverage gap', [4])
    run({'stop': F(2600, 10000), 'shift': False}, 'M-b: stop threshold 0.2495 -> 0.2600', [4,5,6,7,8])
    run({'delta_d_min': True, 'shift': False}, 'M-c: top-dim threshold D=U+V -> min(U,V)', [4,5,6,7,8])
    run({'no_quintic': True, 'shift': False}, 'M-d: quartic curve g=4 -> 3 (drop quintic removal)', [4])
    run({'quadric_const': 2, 'shift': False}, 'M-e: quartic surface 3/U^2 -> 2/U^2', [4])
    run({'w_scale': ((5, 3500), F(99,100)), 'shift': False}, 'M-f: shrink w by 1% in one cell (d=5,z=3500)', [5])
