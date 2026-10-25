#!/usr/bin/env python3
"""Finite/symbolic checks for Lemma 8.1 identity, Lemma 8.4 (four split rays), Lemma 8.6 (eq. 8.3 and F(r,theta)),
Lemma 8.7 (one boundary orbit), Lemma 8.8 (polynomial region <-> opposite sectors), with controls."""
import itertools, sys, random
import numpy as np, sympy as sp, mpmath as mp
fails = []
def chk(c, m):
    print(("  ok   " if c else "  FAIL ") + m)
    if not c: fails.append(m)

print("== Lemma 8.1 / 8.6 / 8.8 symbolic identities (sympy)")
r, e1, e2, w1, w2 = sp.symbols('r e1 e2 w1 w2', real=True)
lhs = (e1 - r*w1)**2 + (e2 - r*w2)**2          # |x+e-q|^2 with q-x = r w, |e|=|w|=1
chk(sp.simplify((lhs - (1 + r**2 - 2*r*(e1*w1+e2*w2))).subs({e2**2: 1-e1**2, w2**2: 1-w1**2}).expand().subs({e2**2: 1-e1**2, w2**2: 1-w1**2})) == 0,
    "|x+e-q|^2 = 1 + r^2 - 2r(e.w) for unit e,w")
t, th = sp.symbols('t theta', real=True)
vp = sp.Matrix([sp.cos(th), sp.sin(th)]); Jvp = sp.Matrix([-sp.sin(th), sp.cos(th)])
m = t/2*Jvp + sp.sqrt(1 - t**2/4)*vp
chk(sp.simplify(m.dot(m)) == 1 and sp.simplify((m - t*Jvp).dot(m - t*Jvp)) == 1, "(8.3): q'+(t/2)Jv'+sqrt(1-t^2/4)v' is at unit distance from q' and q'+tJv'")
R_, TH = sp.symbols('R Theta', real=True)
F = (R_*sp.cos(TH) - 1)**2 + (R_*sp.sin(TH))**2 - 1
chk(sp.simplify(F - (R_**2 - 2*R_*sp.cos(TH))) == 0 and F.subs({R_: 1, TH: sp.pi/3}) == 0
    and sp.simplify(sp.diff(F, TH).subs({R_: 1, TH: sp.pi/3}) - sp.sqrt(3)) == 0, "F(r,th)=r^2-2r cos th, F(1,pi/3)=0, dF/dth(1,pi/3)=sqrt3")
xi, up = sp.symbols('xi upsilon', real=True)
l = xi**2 + up**2
phi = sp.atan2(up, xi)
# l^3 sin^2(3 phi) = up^2(3xi^2-up^2)^2 : verify via (xi+i up)^3
chk(sp.expand(sp.im(sp.expand((xi + sp.I*up)**3)) - up*(3*xi**2 - up**2)) == 0, "Im (xi+i ups)^3 = ups(3xi^2-ups^2)  [so l^3 sin^2 3phi = P]")
d = sp.symbols('delta', positive=True)
chk(sp.simplify(sp.expand_trig(sp.sin(3*d)) - sp.sin(d)*(4*sp.cos(d)**2 - 1)) == 0, "sin 3d = sin d (4cos^2 d - 1)")
a_, b_ = sp.symbols('a b', real=True)
chk(sp.simplify(sp.expand_trig(sp.sin(a_-b_)*sp.sin(a_+b_)) - (sp.sin(a_)**2 - sp.sin(b_)**2)) == 0, "sin(a-b)sin(a+b) = sin^2 a - sin^2 b")
a1, a2 = sp.symbols('alpha1 alpha2', real=True)
Jac = sp.Matrix([[-sp.sin(a1), -sp.sin(a2)], [sp.cos(a1), sp.cos(a2)]]).det()
chk(sp.simplify(Jac - sp.sin(a2 - a1)) == 0, "Jacobian of (a1,a2)->e^{ia1}+e^{ia2} is sin(a2-a1) (= sin 2delta)")

print("== Lemma 8.8: (8.4) <=> endpoints phi+-delta strictly in opposite-sign sin(3.) sectors (random test, n=200000)")
rng = np.random.default_rng(1)
N = 200000
z = (rng.uniform(-2, 2, N) + 1j*rng.uniform(-2, 2, N)); z = z[(abs(z) > 1e-3) & (abs(z) < 2 - 1e-9)]
X, Y = z.real, z.imag; L = X**2 + Y**2
P = Y**2*(3*X**2 - Y**2)**2; Pp = L**3*(1 - L/4)*(L - 1)**2
ph = np.angle(z); dl = np.arccos(np.abs(z)/2)
prod = np.sin(3*(ph - dl))*np.sin(3*(ph + dl))
summ = np.exp(1j*(ph - dl)) + np.exp(1j*(ph + dl))
chk(np.max(np.abs(summ - z)) < 1e-12, "unit directions phi-delta, phi+delta sum to z")
margin = np.abs(Pp - P) > 1e-9
agree = ((P < Pp) == (prod < 0))[margin]
chk(agree.all(), f"(P<P') == (sin3(phi-d) sin3(phi+d) < 0) on {margin.sum()} points with |P'-P|>1e-9: disagreements {np.sum(~agree)}")
bad = ((P > Pp) == (prod < 0))[margin]
chk(np.sum(~bad) > 0.4*margin.sum(), f"  control: the reversed inequality P>P' disagrees with the sector test on {np.sum(~bad)} of {margin.sum()} points (must be many) -> comparison not vacuous")
print(f"   fraction of the disk of radius 2 in the region: {np.mean(P[margin] < Pp[margin]):.3f}")

print("== Moser vertices: independent angular check with mpmath (50 digits) of opposite-sector endpoints")
mp.mp.dps = 50
s3, s11 = mp.sqrt(3), mp.sqrt(11)
A = (s3 + 1j)/2; B = (s3 - 1j)/2; T = s3 + 0j; u = (5 + 1j*s11)/6
G = {"0": mp.mpc(0), "A": mp.mpc(A), "B": mp.mpc(B), "T": mp.mpc(T), "uA": u*A, "uB": u*B, "uT": u*T}
Mrot = mp.mpc(35, 12)/37; c = mp.mpc(-290, 149)/250
for g, val in G.items():
    zz = Mrot*(val + c); rr = abs(zz); p_ = mp.arg(zz); dd = mp.acos(rr/2)
    s_minus, s_plus = mp.sin(3*(p_ - dd)), mp.sin(3*(p_ + dd))
    chk(0 < rr < 2 and s_minus*s_plus < 0, f"{g:>2}: |z|={mp.nstr(rr,8)}  sin3(phi-d)={mp.nstr(s_minus,6)}  sin3(phi+d)={mp.nstr(s_plus,6)}  opposite signs")

def ang_sign(e, v):  # sign of e.v for angles (degrees, integer grid) -- exact on the grid via sympy-free rule
    dd = (v - e) % 360
    if dd == 90 or dd == 270: return 0
    return 1 if (dd < 90 or dd > 270) else -1

print("== Lemma 8.4 grid check: four rays v_0..v_3 on a 15-degree grid (24^4 configurations, vectorised)")
step = 15; nd = 360//step
# exact sign of cos(angle) for e at half-steps (k+1/2)*step and v at j*step: angle difference is an odd multiple of step/2
def sgn_tab():
    T = np.zeros((nd, nd), dtype=np.int8)
    for k in range(nd):
        for j in range(nd):
            dd = ((j*step) - (k*step + step/2)) % 360
            T[k, j] = 1 if (dd < 90 or dd > 270) else -1     # never exactly 90/270 on this grid
    return T
ST = sgn_tab()
cfg = np.array(list(itertools.product(range(nd), repeat=4)), dtype=np.int16)        # (24^4, 4)
S = ST[:, cfg]                                                                        # (24 mids, Ncfg, 4)
split_all = np.all((S[:, :, 0] != S[:, :, 2]) & (S[:, :, 1] != S[:, :, 3]), axis=0)  # Lean's InterfaceFourSplit
good = cfg[split_all]
def diag(sv):
    for j in range(4):
        if sv[j] == 1 and sv[(j+1) % 4] == 1: return "U" if (j+1) % 2 == 0 else "V"
viol = []; n1 = n2 = 0
for v in good:
    v = [int(x)*step for x in v]
    svs = [tuple(int(ST[k, vi//step]) for vi in v) for k in range(nd)]
    ds = [diag(sv) for sv in svs]
    for vi in v:
        if v.count(vi) != v.count((vi+180) % 360): viol.append(("not antipodally paired", v))
    lines = {vi % 180 for vi in v}
    if len(lines) == 1:
        n1 += 1
        if len(set(ds)) != 1: viol.append(("one line but both diagonals", v))
        continue
    n2 += 1
    if len(lines) != 2: viol.append(("more than two lines", v))
    for j in range(4):
        if (v[j] + 180) % 360 != v[(j+2) % 4]: viol.append(("opposite directions not at opposite edges", v))
    proj = {}
    for k, dg in enumerate(ds): proj.setdefault((k*step + step/2) % 180, set()).add(dg)
    if any(len(x) > 1 for x in proj.values()): viol.append(("d(-e) != d(e)", v))
    seq = [next(iter(proj[key])) for key in sorted(proj)]
    if sum(seq[i] != seq[(i+1) % len(seq)] for i in range(len(seq))) != 2: viol.append(("not U-arc/V-arc", v))
    lenU = step*seq.count("U")
    if min(lenU, 180 - lenU) > 90: viol.append(("no arc <= pi/2", v))
chk(len(good) > 0 and not viol, f"configs split at every generic direction: {len(good)} ({n2} two-line, {n1} one-line) of {len(cfg)}; Lemma 8.4 violations: {len(viol)} {viol[:3]}")
chk(np.sum(np.all((S[:, :, 0] != S[:, :, 2]) | (S[:, :, 1] != S[:, :, 3]), axis=0)) > len(good),
    "  control: a weaker (wrong) split test admits strictly more configurations -> the detector discriminates")

print("== Lemma 8.7 grid check: three rays on a 5-degree grid; R-orbits all of whose consecutive pairs meet B (vectorised)")
def max_orbits(nrays, stp, sub=1):
    n = 360//stp; R = 60//stp; q = 90//stp
    cfg = np.array(list(itertools.product(range(0, n, sub), repeat=nrays)), dtype=np.int16)
    Bm = np.zeros((len(cfg), n), dtype=bool)
    rows = np.arange(len(cfg))
    for i in range(nrays):
        Bm[rows, (cfg[:, i] + q) % n] = True; Bm[rows, (cfg[:, i] - q) % n] = True
    cnt = np.zeros(len(cfg), dtype=np.int16)
    for e0 in range(R):
        orb = [(e0 + R*j) % n for j in range(6)]
        ok = np.ones(len(cfg), dtype=bool)
        for j in range(6): ok &= Bm[:, orb[j]] | Bm[:, orb[(j+1) % 6]]
        cnt += ok
    return len(cfg), int(cnt.max()), np.bincount(cnt)
N3, m3, h3 = max_orbits(3, 5)
chk(m3 <= 1, f"three rays, 5-degree grid: {N3} configs, max qualifying orbits = {m3}, histogram {h3.tolist()}")
N4, m4, h4 = max_orbits(4, 5, sub=3)
chk(m4 >= 2, f"  control: four rays (15-degree subgrid, {N4} configs): max qualifying orbits = {m4} (>=2 shows the detector can exceed 1)")
print("RESULT:", "ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURE(S): {fails}")
sys.exit(1 if fails else 0)
