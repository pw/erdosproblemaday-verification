# Independent exact re-check of Section 10 / Appendix A certificate (seat M1).
# All comparisons exact (Fractions); radicals enclosed rigorously via integer nth roots.
import sys, itertools
from fractions import Fraction as F
from math import comb, isqrt
import sympy as sp

K0, G0 = 3000, 100000
TAU = F(1, 50000)
PREC = 10**40   # radical enclosure resolution 1e-40

def iroot(n, h):
    """floor(n^(1/h)) for integer n>=0"""
    if n < 2: return n
    x = int(round(n ** (1.0/h))) if n < 10**300 else 1 << ((n.bit_length() + h - 1)//h)
    # Newton refine
    while True:
        y = ((h-1)*x + n // x**(h-1)) // h
        if y >= x: break
        x = y
    while x**h > n: x -= 1
    while (x+1)**h <= n: x += 1
    return x

def root_enclosure(q, h):
    """rigorous [lo,hi] with lo <= q^(1/h) <= hi, q Fraction >= 0"""
    # q^(1/h) = (q*PREC^h)^(1/h)/PREC
    num = q.numerator * PREC**h
    den = q.denominator
    n = num // den           # floor(q*PREC^h)
    r = iroot(n, h)
    lo = F(r, PREC)
    hi = F(r + 1, PREC)      # (r+1)^h > n >= ... ; and q*PREC^h < n+1 <= (r+1)^h
    assert lo**h <= q <= hi**h
    return (lo, hi)

def imax(*ivs):
    return (max(a for a, b in ivs), max(b for a, b in ivs))

# ---------- Hilbert polynomial R(A,B) derived independently ----------
A, B, t = sp.symbols('A B t', positive=True)
def R_from_series(d):
    k = d - 2
    expr = A**(d-1) * B**(d-1) / sp.factorial(d-1)**2
    for _ in range(d-2):
        expr = k*sp.diff(expr, A) + sp.diff(expr, B)
    return sp.expand(expr)
def R_paper(d):
    k = d - 2
    return sp.expand(sum(sp.binomial(d, j)*sp.binomial(d-2, j-1)*k**(j-1)*A**(d-j)*B**j
                         for j in range(1, d)) / sp.factorial(d))

def hilbert_numeric_check(d, Aval, Bval):
    """exact dim of bidegree (Aval,Bval) part of C[a,b]/(d-2 forms of bidegree (k,1)) via series coeff"""
    k = d - 2
    z1, z2 = sp.symbols('z1 z2')
    # coefficient extraction of (1-z1^k z2)^(d-2) / ((1-z1)^d (1-z2)^d)
    tot = 0
    for i in range(d-1):
        c = comb(d-2, i) * (-1)**i
        a, b = Aval - k*i, Bval - i
        if a < 0 or b < 0: continue
        tot += c * comb(a+d-1, d-1) * comb(b+d-1, d-1)
    return tot

polys = {}
for d in range(4, 9):
    Rs = R_from_series(d); Rp = R_paper(d)
    assert sp.simplify(Rs - Rp) == 0, d
    H = sp.expand(sp.factorial(d) * Rp.subs({A: 1, B: t}))
    Ha = sp.expand(sp.factorial(d-1) * sp.diff(Rp, A).subs({A: 1, B: t}))
    Hb = sp.expand(sp.factorial(d-1) * sp.diff(Rp, B).subs({A: 1, B: t}))
    polys[d] = (sp.Poly(H, t), sp.Poly(Ha, t), sp.Poly(Hb, t))
    # numeric sanity: leading term of the CI Hilbert function equals R
    Av = 600; Bv = 300
    exact = hilbert_numeric_check(d, Av, Bv)
    approx = Rp.subs({A: Av, B: Bv})
    rel = abs(float(exact - approx)) / float(approx)
    print(f"d={d}: R from series == R paper; CI HF at (600,300) rel.dev from R = {rel:.4f}")

def ev(p, x):
    return sum(F(int(c)) * x**int(e[0]) for e, c in zip(p.monoms(), p.coeffs()))

# ---------- the certificate ----------
results = {}
global_min = None
for d in range(4, 9):
    k = d - 2
    Hp, Hap, Hbp = polys[d]
    grid = [F(i, 50) for i in range(1, 500)]
    gridvals = [(tt, ev(Hp, tt), ev(Hap, tt), ev(Hbp, tt)) for tt in grid]
    g = (d-1)*(k-1) + (1 if d == 4 else 0)
    z = K0
    rec = dict(min_gap_lo=None, min_gap_hi=None, min_gap_z=None, min_Q=None, min_Q_z=None,
               min_vu=None, max_vu=None, min_slack_m=None, min_cut1=None, min_cut2=None, cells=0)
    while True:
        eL, eH = F(z, K0), F(z+1, K0)
        if eL*(1 - k*eL/d) < F(2495, 10000):
            zd = z; break
        bL, bH = d - k*eH, d - k*eL
        # prescription: t* minimizes (eH+bH t)^d / H(t), first on ties
        best = None
        for (tt, H, Ha, Hb) in gridvals:
            val = (eH + bH*tt)**d / H
            if best is None or val < best[0]:
                best = (val, tt, H, Ha, Hb)
        _, ts, H, Ha, Hb = best
        x = ((d+1)*(eH + bH*ts)/d**2)**d / H
        assert 0 <= x < 1
        # w = least r/G0 with (r/G0)^(d-1) > x
        lo_r = iroot((x.numerator * G0**(d-1)) // x.denominator, d-1)
        r = lo_r
        while F(r, G0)**(d-1) <= x: r += 1
        while r > 1 and F(r-1, G0)**(d-1) > x: r -= 1
        w = F(r, G0)
        m = (d-1)*w
        # (10.4)
        cut1 = w**(d-1)*H / ((d+1)*(eH+bH*ts)/d**2)**d
        cut2 = w**(d-2)*min(Ha, Hb) / ((eH+bH*ts)/(d-1))**(d-1)
        assert cut1 > 1 and cut2 > 1, (d, z)
        assert 0 < m < 1 and min(eL, bL) > m, (d, z)
        u, v = (eH - m)/d, (bH - m)/d
        assert u > 0 and v > 0 and F(3, 20) <= v/u <= 5, (d, z, v/u)
        modeQ = (d == 4 and z < 4000)
        def Psi(h, D):
            return root_enclosure((u*v)**h / ((k*u+v)**(h-1) * D), h)
        deltas = {}
        deltas[d] = Psi(d, u+v)
        if modeQ:
            deltas[3] = Psi(3, v)
            deltas[2] = imax(Psi(2, min(3*u, 2*v, u+v)), root_enclosure(u*u/3, 2))
        else:
            for h in range(2, d):
                deltas[h] = Psi(h, min(u, v))
        deltas[1] = (max(u/2, min(u, v/g)),)*2
        E = {}
        for h in range(1, d+1):
            E[h] = imax(*[deltas[s] for s in range(h, d+1)])
        sumE = (sum(E[h][0] for h in E), sum(E[h][1] for h in E))
        gap_lo = 1 - m - sumE[1]       # rigorous lower bound of true gap
        gap_hi = 1 - m - sumE[0]
        assert gap_lo > F(1, 1000), (d, z, float(gap_lo))
        if rec['min_gap_lo'] is None or gap_lo < rec['min_gap_lo']:
            rec.update(min_gap_lo=gap_lo, min_gap_hi=gap_hi, min_gap_z=z,
                       detail=dict(ts=ts, w=w, m=m, u=u, v=v,
                                   E={h: float(E[h][0]) for h in E}))
        if modeQ:
            q = F(999, 1000) - (m + 2*u)
            assert q > 0
            if rec['min_Q'] is None or q < rec['min_Q']:
                rec['min_Q'], rec['min_Q_z'] = q, z
        rec['min_vu'] = v/u if rec['min_vu'] is None else min(rec['min_vu'], v/u)
        rec['max_vu'] = v/u if rec['max_vu'] is None else max(rec['max_vu'], v/u)
        sl = min(eL, bL) - m
        rec['min_slack_m'] = sl if rec['min_slack_m'] is None else min(rec['min_slack_m'], sl)
        rec['min_cut1'] = cut1 if rec['min_cut1'] is None else min(rec['min_cut1'], cut1)
        rec['min_cut2'] = cut2 if rec['min_cut2'] is None else min(rec['min_cut2'], cut2)
        rec['cells'] += 1
        z += 1
    rec['zd'] = zd
    results[d] = rec
    print(f"\nd={d}: z_d={zd} (eta_stop={F(zd,K0)}={float(F(zd,K0)):.6f}), cells={rec['cells']}")
    print(f"  true min gap (1-m-sumE) in [{float(rec['min_gap_lo']):.9f}, {float(rec['min_gap_hi']):.9f}] at z={rec['min_gap_z']} (eta in [{rec['min_gap_z']/K0:.5f},{(rec['min_gap_z']+1)/K0:.5f}])")
    print(f"  detail: {rec['detail']}")
    print(f"  margin over 1/1000: {float(rec['min_gap_lo'] - F(1,1000)):.9f};  final exponent with d*tau: {float(1 - rec['min_gap_lo'] + d*TAU):.9f}")
    if rec['min_Q'] is not None:
        print(f"  mode Q: min (999/1000 - m - 2u) = {float(rec['min_Q']):.9f} at z={rec['min_Q_z']}")
    print(f"  v/u range [{float(rec['min_vu']):.5f}, {float(rec['max_vu']):.5f}]; min(min(eta-,b-)-m)={float(rec['min_slack_m']):.6f}")
    print(f"  min cut1 ratio {float(rec['min_cut1']):.8f}, min cut2 ratio {float(rec['min_cut2']):.8f}")
    # phi check at stop, and before stop
    phi = lambda e: e*(1-k*e/d)
    print(f"  phi(z_d/K)={float(phi(F(zd,K0))):.8f} <0.2495 ; phi((z_d-1)/K)={float(phi(F(zd-1,K0))):.8f} >=0.2495")

table = {4: (5124, F(191,100000)), 5: (4084, F(293,50000)), 6: (3552, F(321,2500)),
         7: (3226, F(23177,100000)), 8: (3003, F(31683,100000))}
print("\nTable comparison (paper's rounded gap must be <= true gap lower bound):")
for d in range(4, 9):
    zd, tg = table[d]
    rec = results[d]
    print(f" d={d}: z_d paper {zd} vs mine {rec['zd']}; paper gap {float(tg):.6f} vs true gap >= {float(rec['min_gap_lo']):.8f}; consistent={rec['zd']==zd and tg <= rec['min_gap_lo']}")
