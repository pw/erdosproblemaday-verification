# My own exact rebuild of one slab certificate (S + eps I) and the inner certificate (P), from my own constants.
import sys, json, time; sys.path.insert(0, '.')
from d3 import *
from t2_constants_lib import my_bathtub
from math import lcm
H = hnodes()
fn = sys.argv[1]
cert = json.load(open(fn)); grid = cert['grid']; n = len(grid)-1
cells = []
for i in range(n):
    p, q = grid[i], grid[i+1]; a, b = my_bathtub(p, q)
    cells.append(dict(s=sign_on(p, q), w=F(q-p, U), a=a, b=b))
full, cut = [], []
for i in range(n):
    for j in range(n):
        x0, x1, y0, y1 = F(grid[i],U), F(grid[i+1],U), F(grid[j],U), F(grid[j+1],U)
        A = area_in(x0, x1, y0, y1); W = (x1-x0)*(y1-y0)
        if A == 0: continue
        if A == W: full.append((i, j))
        else: cut.append((i, j, A, W-A))
# polynomial: c0 + sum lin_i y_i + sum_{i<=j} Q[(i,j)] y_i y_j
c0 = F(0); lin = [F(0)]*n; Qd = {}
def addq(i, j, v):
    if v == 0: return
    if i > j: i, j = j, i
    Qd[(i, j)] = Qd.get((i, j), F(0)) + v
def aff_mul(coef, A1, A2):
    """add coef*A1*A2, A = (k, {i: c})"""
    global c0
    k1, d1 = A1; k2, d2 = A2
    c0 += coef*k1*k2
    for i, c in d1.items(): lin[i] += coef*c*k2
    for j, c in d2.items(): lin[j] += coef*c*k1
    for i, ci in d1.items():
        for j, cj in d2.items(): addq(i, j, coef*ci*cj)
ONE = (F(1), {})
Yf = lambda i: (F(0), {i: F(1)}); Of = lambda i: (F(1), {i: F(-1)}); Zf = lambda i: (F(1), {i: F(-2)})
mvec = {i: cells[i]['w'] for i in range(n)}
# L part
for i, c in enumerate(cells): lin[i] += c['a']; addq(i, i, c['b'])
for (i, j) in full: addq(i, j, cells[i]['s']*cells[j]['s']*cells[i]['w']*cells[j]['w'])
inner = 'rin' in cert
if not inner:
    theta = [F(t) for t in cert['theta']]; assert len(theta) == len(cut)
    for t, (i, j, Ain, Aout) in enumerate(cut):
        ww = cells[i]['w']*cells[j]['w']; th = theta[t]
        if cells[i]['s']*cells[j]['s'] > 0:   # th*0 + (1-th)*(ww y y - Aout)
            c0 += (1-th)*(-Aout); addq(i, j, (1-th)*ww)
        else:                                 # th*(-Ain) + (1-th)*(-ww y y)
            c0 += th*(-Ain); addq(i, j, -(1-th)*ww)
    lo, hi = F(cert['lo']), F(cert['hi']); B = F(cert['B']); eps = F(cert['eps'])
    c0 -= B
    ML = (-lo, dict(mvec)); MH = (hi, {i: -v for i, v in mvec.items()})
    for kind, idx, mu in cert['forms']:
        mu = F(mu); assert mu >= 0; m_ = -mu
        if kind == 'yy': aff_mul(m_, Yf(idx[0]), Yf(idx[1]))
        elif kind == '11': aff_mul(m_, Of(idx[0]), Of(idx[1]))
        elif kind == 'y1': aff_mul(m_, Yf(idx[0]), Of(idx[1]))
        elif kind == 'yd': aff_mul(m_, Yf(idx), Of(idx))
        elif kind == '11d': aff_mul(m_, Of(idx), Of(idx))
        elif kind == 'y': aff_mul(m_, Yf(idx), ONE)
        elif kind == '1': aff_mul(m_, Of(idx), ONE)
        elif kind == 'mlo': aff_mul(m_, ML, ONE)
        elif kind == 'mhi': aff_mul(m_, MH, ONE)
        elif kind == 'mm': aff_mul(m_, ML, MH)
        elif kind == 'mlo_y': aff_mul(m_, ML, Yf(idx))
        elif kind == 'mlo_1': aff_mul(m_, ML, Of(idx))
        elif kind == 'mhi_y': aff_mul(m_, MH, Yf(idx))
        elif kind == 'mhi_1': aff_mul(m_, MH, Of(idx))
        elif kind == 'tri':
            i, j, k, s = idx; assert len({i, j, k}) == 3 and s[0]*s[1]*s[2] == 1
            aff_mul(m_, ONE, ONE); aff_mul(m_*s[0], Zf(i), Zf(j)); aff_mul(m_*s[1], Zf(j), Zf(k)); aff_mul(m_*s[2], Zf(i), Zf(k))
        else: raise SystemExit('unknown kind ' + kind)
    N1 = n+1
    S = [[F(0)]*N1 for _ in range(N1)]
    S[0][0] = c0 + eps
    for i in range(n): S[0][i+1] = S[i+1][0] = lin[i]/2
    for (i, j), v in Qd.items():
        if i == j: S[i+1][i+1] += v
        else: S[i+1][j+1] += v/2; S[j+1][i+1] += v/2
    for i in range(n): S[i+1][i+1] += eps
    M = S; bound = B - eps*(1+n)
    print('claim == my B - eps(1+n):', F(cert['claim']) == bound, float(bound))
else:
    rin = F(cert['rin'])
    for (i, j, Ain, Aout) in cut:
        if cells[i]['s']*cells[j]['s'] < 0: addq(i, j, -cells[i]['w']*cells[j]['w'])
    MR = (rin, {i: -v for i, v in mvec.items()}); M0 = (F(0), dict(mvec))
    for key, v in cert['lam'].items():
        i, j = map(int, key.split(',')); v = F(v); assert v >= 0; aff_mul(-v, Yf(i), Of(j))
    for j, v in enumerate(cert['nu']): v = F(v); assert v >= 0; aff_mul(-v, Yf(j), MR)
    kap = F(cert['kap']); assert kap >= 0; aff_mul(-kap, M0, MR)
    for key, v in cert['N'].items():
        i, j = map(int, key.split(',')); v = F(v); assert v >= 0 and i <= j; aff_mul(-v*(1 if i == j else 2), Yf(i), Yf(j))
    for i, v in enumerate(cert['c']): v = F(v); assert v >= 0; aff_mul(-v, Yf(i), ONE)
    print('constant residual', c0, ' nonzero linear residuals', sum(1 for v in lin if v != 0))
    M = [[F(0)]*n for _ in range(n)]
    for (i, j), v in Qd.items():
        if i == j: M[i][i] += v
        else: M[i][j] += v/2; M[j][i] += v/2
json.dump([[str(x) for x in row] for row in M], open(sys.argv[2], 'w'))
print('wrote', sys.argv[2], 'dim', len(M))
