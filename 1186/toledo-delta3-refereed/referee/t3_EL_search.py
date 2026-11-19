# Adversarial search for E(sigma) - L(y(sigma)) < 0 on a fine grid; exact confirmation of the best candidates.
import sys, json, time; sys.path.insert(0, '.')
import numpy as np
from d3 import *
H = hnodes()
GF = 2192                       # fine grid: cells of width 1/2192 (each 1/1096 unit split in two)
r = GF // U                     # 2
which = sys.argv[1] if len(sys.argv) > 1 else 'inner'
d = json.load(open('verify_grids.json'))
key = [k for k in d if which in k][0]
V = d[key]; grid = V['grid']; n = len(grid) - 1
print('certificate grid from', key.split('/')[-1], 'n =', n, ' fine grid 1/%d' % GF)

# exact fine-cell data
def hfine(xf):   # h at xf/GF exactly by interpolation on the 1/1096 lattice (Lemma 1 checked linear)
    q, rem = divmod(xf, r)
    if rem == 0: return H[q]
    return H[q] + (H[q+1]-H[q])*F(rem, r)
Hk = [F(1, GF)*(hfine(k)+hfine(k+1))/2 for k in range(GF)]
sk = np.array([sign_on(k//r, k//r+1) for k in range(GF)])
Hf = np.array([float(x) for x in Hk])

# 4*GF^2*area(R ∩ fine_k x fine_l), integer, by the corner formula (third area route)
def Gbelow(x, y):   # area [0,x]x[0,y] ∩ {b <= a/2}, units 1/GF, times 4
    x = x.astype(np.int64); y = y.astype(np.int64)
    return np.where(x <= 2*y, x*x, 4*(x*y - y*y))
def Gabove(x, y):   # area [0,x]x[0,y] ∩ {b >= (GF+a)/2}, times 4: t = min(x, max(0, 2y-GF)); 4*(t*y - t*GF/2) - t^2
    x = x.astype(np.int64); y = y.astype(np.int64)
    t = np.minimum(x, np.maximum(0, 2*y - GF))
    return 4*t*y - 2*t*GF - t*t
idx = np.arange(GF+1)
X0, Y0 = np.meshgrid(idx[:-1], idx[:-1], indexing='ij'); X1, Y1 = X0+1, Y0+1
def rectarea4(Gf):
    return Gf(X1, Y1) - Gf(X0, Y1) - Gf(X1, Y0) + Gf(X0, Y0)
A4 = 4 - rectarea4(Gbelow) - rectarea4(Gabove)          # 4*GF^2 * area_in, fine cells have area 1 (units)
assert A4.min() >= 0 and A4.max() <= 4
# spot-check the corner formula against d3.area_in
import random
random.seed(1)
for _ in range(300):
    k, l = random.randrange(GF), random.randrange(GF)
    assert F(int(A4[k, l]), 4*GF*GF) == area_in(F(k, GF), F(k+1, GF), F(l, GF), F(l+1, GF)), (k, l)
print('fine area matrix ok; |R| =', A4.sum()/(4*GF*GF))
Af = A4.astype(float)/(4*GF*GF)

# certificate-grid data (own constants; t2 proved equal to verify.js's)
from t2_constants_lib import my_bathtub
cells = []
for i in range(n):
    p, q = grid[i], grid[i+1]
    a, b = my_bathtub(p, q)
    cells.append((p, q, sign_on(p, q), F(q-p, U), a, b))
a_ = np.array([float(c[4]) for c in cells]); b_ = np.array([float(c[5]) for c in cells])
w_ = np.array([float(c[3]) for c in cells]); s_ = np.array([c[2] for c in cells])
cellof = np.empty(GF, dtype=int)
for i, (p, q, *_r) in enumerate(cells): cellof[p*r:q*r] = i
Wavg = np.zeros((n, GF))
for k in range(GF): Wavg[cellof[k], k] = 1.0/((cells[cellof[k]][1]-cells[cellof[k]][0])*r)
full = [tuple(x) for x in V['full']]; cut = [(i, j, F(ai), F(ao)) for i, j, ai, ao in V['cut']]
Mfull = np.zeros((n, n))
for i, j in full: Mfull[i, j] += s_[i]*s_[j]*w_[i]*w_[j]
ci = np.array([c[0] for c in cut]); cj = np.array([c[1] for c in cut])
cs = s_[ci]*s_[cj]; cww = w_[ci]*w_[cj]; cAin = np.array([float(c[2]) for c in cut]); cAout = np.array([float(c[3]) for c in cut])

def E_float(sig):
    u = sk*sig
    return Hf@sig + u@Af@u
def L_float(y):
    val = a_@y + b_@(y*y) + y@Mfull@y
    yy = y[ci]*y[cj]
    pos = np.maximum(0.0, cww*yy - cAout); neg = np.maximum(-cAin, -cww*yy)
    return val + np.where(cs > 0, pos, neg).sum()
def grad(sig):
    u = sk*sig
    gE = Hf + sk*((Af+Af.T)@u)
    y = Wavg@sig
    gy = a_ + 2*b_*y + (Mfull+Mfull.T)@y
    yy = y[ci]*y[cj]
    # active branch derivatives
    act_pos = (cs > 0) & (cww*yy - cAout > 0)
    act_neg = (cs < 0) & (-cww*yy > -cAin)
    coef = np.where(act_pos, cww, 0.0) + np.where(act_neg, -cww, 0.0)
    np.add.at(gy, ci, coef*y[cj]); np.add.at(gy, cj, coef*y[ci])
    return gE - Wavg.T@gy

def EL_exact(sig_num, D):
    """sig = sig_num/D with integer numerators; exact E - L"""
    sig_num = np.asarray(sig_num, dtype=np.int64)
    u = (sk*sig_num).astype(object)
    # quadratic: sum_kl A4_kl u_k u_l / (4 GF^2 D^2); do in Python ints via int64 blocks
    Au = A4.astype(np.int64) @ (sk*sig_num).astype(np.int64)     # each |entry| <= 4*GF*D  fits
    quad = int(((sk*sig_num).astype(np.int64) * Au).astype(object).sum())
    E = sum(Hk[k]*int(sig_num[k]) for k in range(GF) if sig_num[k]) / D + F(quad, 4*GF*GF*D*D)
    y = []
    for i, (p, q, *_r) in enumerate(cells):
        y.append(F(int(sig_num[p*r:q*r].sum()), (q-p)*r*D))
    L = sum(c[4]*y[i] + c[5]*y[i]*y[i] for i, c in enumerate(cells))
    for i, j in full: L += cells[i][2]*cells[j][2]*cells[i][3]*cells[j][3]*y[i]*y[j]
    for (i, j, Ain, Aout) in cut:
        ww = cells[i][3]*cells[j][3]; yy = y[i]*y[j]
        if cells[i][2]*cells[j][2] > 0: L += max(F(0), ww*yy - Aout)
        else: L += max(-Ain, -ww*yy)
    return E - L, E, L

rng = np.random.default_rng(12345)
best = []   # (value, sig)
def record(sig, tag):
    v = E_float(sig) - L_float(Wavg@sig)
    best.append((v, tag, sig.copy()))

# --- adversarial constructions ---
# (1) correction specimen: sigma = t on [0,16/1096]
for t in [0.1, 0.25, 0.5, 1.0]:
    sig = np.zeros(GF); sig[0:16*r] = t; record(sig, 'corr t=%g' % t)
# (2) per cell: sigma = t at the far end from argmin h, and sublevel-set indicators, and single fine cells
for i, (p, q, s, w, a, b) in enumerate(cells):
    seg = [float(hfine(k)) for k in range(p*r, q*r+1)]
    kmin = int(np.argmin(seg))
    lenc = (q-p)*r
    for frac in [0.25, 0.5, 1.0]:
        m = max(1, int(lenc*frac))
        sig = np.zeros(GF)
        if kmin <= lenc//2: sig[q*r-m:q*r] = 1.0
        else: sig[p*r:p*r+m] = 1.0
        record(sig, 'far-end cell %d frac %g' % (i, frac))
        # sublevel: the m fine cells with the smallest h
        order = np.argsort(Hf[p*r:q*r]); sig = np.zeros(GF); sig[p*r + order[:m]] = 1.0
        record(sig, 'sublevel cell %d frac %g' % (i, frac))
# (3) cut-pair corners: for each cut pair choose sigma on I_i, I_j to put sigma x sigma mass where it hurts the bound
for (i, j, Ain, Aout) in cut:
    pi, qi = cells[i][0]*r, cells[i][1]*r; pj, qj = cells[j][0]*r, cells[j][1]*r
    sub = A4[pi:qi, pj:qj]
    for half in (0.5, 1.0):
        sig = np.zeros(GF)
        if cells[i][2]*cells[j][2] > 0:   # want little mass inside R: pick rows/cols with smallest inside area
            rs = np.argsort(sub.sum(1)); cs_ = np.argsort(sub.sum(0))
        else:                              # want mass inside R
            rs = np.argsort(-sub.sum(1)); cs_ = np.argsort(-sub.sum(0))
        mi = max(1, int((qi-pi)*half)); mj = max(1, int((qj-pj)*half))
        sig[pi + rs[:mi]] = 1.0; sig[pj + cs_[:mj]] = 1.0
        record(sig, 'cutcorner (%d,%d) %g' % (i, j, half))
# (4) breakpoint flips: sigma = 1 on [e, e+k] or [e-k, e]
for e in EDGES[1:-1]:
    for k in [1, 2, 4, 8, 16, 32]:
        sig = np.zeros(GF); sig[e*r:e*r+k] = 1.0; record(sig, 'flip right of %d len %d' % (e, k))
        sig = np.zeros(GF); sig[e*r-k:e*r] = 1.0; record(sig, 'flip left of %d len %d' % (e, k))
# (5) sublevel sets of h globally
order = np.argsort(Hf)
for m in [8, 32, 128, 256, 438, 600, 876, 1096]:
    sig = np.zeros(GF); sig[order[:m]] = 1.0; record(sig, 'global sublevel %d' % m)
print('constructions:', len(best), ' min E-L (float) =', min(b[0] for b in best))

# --- projected gradient descent from many starts, minimising E - L ---
t0 = time.time()
starts = 0
while time.time() - t0 < float(sys.argv[2] if len(sys.argv) > 2 else 600):
    kind = rng.integers(4)
    if kind == 0: sig = rng.random(GF) * rng.random()
    elif kind == 1: sig = (rng.random(GF) < rng.random()*0.3).astype(float)
    elif kind == 2:
        sig = np.zeros(GF); c0 = rng.integers(GF); L0 = rng.integers(1, 200); sig[c0:c0+L0] = rng.random()
    else:
        sig = best[rng.integers(len(best))][2] * (0.5 + rng.random()); sig = np.clip(sig + 0.05*rng.standard_normal(GF), 0, 1)
    lr = 2.0
    v = E_float(sig) - L_float(Wavg@sig)
    for it in range(300):
        g = grad(sig)
        new = np.clip(sig - lr*g, 0, 1)
        nv = E_float(new) - L_float(Wavg@new)
        if nv < v: sig, v = new, nv; lr *= 1.2
        else: lr *= 0.5
        if lr < 1e-6: break
    best.append((v, 'descent kind %d' % kind, sig.copy())); starts += 1
print('descents:', starts, ' time %.0f s' % (time.time()-t0))
best.sort(key=lambda b: b[0])
print('lowest float values:')
for v, tag, sig in best[:8]:
    print('  %.3e  %s  m=%.4f' % (v, tag, sig.mean()))
# exact confirmation of the 12 lowest (sigma rounded to dyadic D = 1024)
D = 1024
mins = []
for v, tag, sig in best[:12] + [b for b in best if b[1].startswith('corr')]:
    num = np.rint(sig*D).astype(np.int64)
    d_, E_, L_ = EL_exact(num, D)
    mins.append(d_)
    print('  exact E-L = %s (%.3e)  E=%.3e L=%.3e  %s' % ('0' if d_ == 0 else ('%s...' % str(d_)[:40]), float(d_), float(E_), float(L_), tag))
print('MIN exact E - L over confirmed candidates:', min(mins), float(min(mins)))
