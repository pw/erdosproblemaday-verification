# Same V-mesh at LARGE k (D = 3, 4, 8, 16), where the full mesh (2m ~ 1e7..1e30 cells) cannot be enumerated.
# Windows of cells: at the cut, at the threshold rho = eta, at zero, and 3 random places.  Each window uses a LOCAL
# coordinate in which every endpoint is computed without cancellation (80-digit mpmath):
#   cut window:  s = signed distance from the cut;  left endpoints s = a_j, right endpoints s = -a_j.
#   zero window: u = signed distance from zero;     left endpoints u = -b_j, right endpoints u = +b_j,
#                b_j = 1/2 - a_j = alpha e^{j theta} expm1((m-j) theta)   (exact rewriting since alpha(e^R - 1) = 1/2).
#   middle windows: t = a_j (left family; the mirror cells are isometric images, rho is mirror-invariant).
# On every left cell [a_j, a_{j+1}] in a window: mesh:width at both closure endpoints, and for N(I) = [l-w, r+w]
# the number of endpoints (<= 49) and the min width of cells whose closure meets N(I) (>= w/16); N(I) is asserted to
# lie inside the generated window so the count is complete.
# Closed form for mesh:truncated: densest 4H-arc in {rho >= eta} starts at the threshold point; count =
#   1 + #{j : eta <= a_j <= eta + 4H}.
import math, random, bisect
import mpmath
from sympy import nextprime
mpmath.mp.dps = 80
mpf = mpmath.mpf
random.seed(1)

def iroot_ceil(k, r):
    D = max(int(mpmath.floor(mpf(k)**(mpf(1)/r))), 1)
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def params(k):
    D = iroot_ceil(k, 10); P = nextprime(k)
    c = mpf(1)/10**5; lk = mpmath.log(k); lP = mpmath.log(P)
    e = max(1, int(mpmath.ceil(c*k*lk/(D*lP))))
    while e > 1 and (e-1)*lP >= c*k*lk/D: e -= 1
    while e*lP < c*k*lk/D: e += 1
    alpha = mpmath.exp(-(D+1)*e*lP)
    R = mpmath.log(1 + 1/(2*alpha))
    m = int(mpmath.ceil(mpf(k)**2*R))
    return dict(k=k, D=D, P=P, e=e, alpha=alpha, R=R, m=m, theta=R/m, H=mpf(1)/mpf(k)**2, eta=mpf(1)/(1000*D))

def a_of(pr, j):  return pr['alpha']*mpmath.expm1(j*pr['theta'])
def b_of(pr, j):  return pr['alpha']*mpmath.exp(j*pr['theta'])*mpmath.expm1((pr['m']-j)*pr['theta'])   # = 1/2 - a_j
def w_of(pr, j):  return pr['alpha']*mpmath.exp(j*pr['theta'])*mpmath.expm1(pr['theta'])               # = a_{j+1} - a_j

def window_check(pr, j0, j1, kind, pad=60):
    m, H, al = pr['m'], pr['H'], pr['alpha']
    lo, hi = max(0, j0 - pad), min(m, j1 + pad)
    if kind == 'cut':
        pts = sorted(set([a_of(pr, j) for j in range(lo, hi+1)] + [-a_of(pr, j) for j in range(max(1, lo), hi+1)]))
        cell = lambda j: (a_of(pr, j), a_of(pr, j+1))
    elif kind == 'zero':
        pts = sorted(set([-b_of(pr, j) for j in range(lo, hi+1)] + [b_of(pr, j) for j in range(lo, hi+1)]))
        cell = lambda j: (-b_of(pr, j), -b_of(pr, j+1))
    else:
        pts = [a_of(pr, j) for j in range(lo, hi+1)]
        cell = lambda j: (a_of(pr, j), a_of(pr, j+1))
    viol = 0; maxcnt = 0; minrt = None; lo_r = None; hi_r = None; n = 0
    for j in range(max(j0, 0), min(j1, m-1) + 1):
        l, r = cell(j); w = w_of(pr, j); n += 1
        assert abs((r - l) - w) <= mpf(10)**-60 * w + mpf(10)**-75, "width formula mismatch"
        for rho in (a_of(pr, j), a_of(pr, j+1)):             # rho at the two closure endpoints of the left cell j
            s = rho + al; rt = w/(H*s)
            lo_r = rt if lo_r is None else min(lo_r, rt); hi_r = rt if hi_r is None else max(hi_r, rt)
            if not (H*s/4 <= w <= 2*H*s <= 2*H): viol += 1
        Lb, Rb = l - w, r + w
        assert pts[0] < Lb, ("window too small (left)", kind, j)
        assert Rb < pts[-1], ("window too small (right)", kind, j)
        i_l = bisect.bisect_left(pts, Lb); i_r = bisect.bisect_right(pts, Rb)
        c = i_r - i_l
        seg = pts[max(0, i_l - 1): min(len(pts), i_r + 1)]     # endpoints of every cell whose closure meets N(I)
        mw = min(seg[i+1] - seg[i] for i in range(len(seg) - 1))
        rt2 = mw/w
        minrt = rt2 if minrt is None else min(minrt, rt2); maxcnt = max(maxcnt, c)
        if c > 49 or rt2 < mpf(1)/16: viol += 1
    return n, viol, lo_r, hi_r, maxcnt, minrt

for k in [1025, 10**6, 10**9, 10**12]:
    pr = params(k); m = pr['m']
    jeta = int(mpmath.ceil(mpmath.log(1 + pr['eta']/pr['alpha'])/pr['theta']))
    wins = [(0, 200, 'cut'), (jeta - 100, jeta + 100, 'mid'), (m - 200, m - 1, 'zero')] + \
           [(x, x + 100, 'mid') for x in (random.randrange(400, m - 400) for _ in range(3))]
    tot = [0, 0]; LO = HI = MR = None; MC = 0
    for (j0, j1, kind) in wins:
        n, v, lo_r, hi_r, mc, mr = window_check(pr, j0, j1, kind)
        tot[0] += n; tot[1] += v; MC = max(MC, mc)
        LO = lo_r if LO is None else min(LO, lo_r); HI = hi_r if HI is None else max(HI, hi_r); MR = mr if MR is None else min(MR, mr)
    th, al, eta, H = pr['theta'], pr['alpha'], pr['eta'], pr['H']
    n_in = int(mpmath.floor(mpmath.log(1 + (eta + 4*H)/al)/th)) - int(mpmath.ceil(mpmath.log(1 + eta/al)/th)) + 1
    print("k=%-14d D=%-3d e=%-7d m=%s theta/H=%s | %d cells: viol=%d, |I|/(H(rho+a)) in [%s,%s], max#endpoints(N(I))=%d, min|J|/w=%s | densest 4H-arc of V_eta: %d breakpoints vs 16004D=%d (ratio %.3f)"
          % (k, pr['D'], pr['e'], mpmath.nstr(mpf(m), 4), mpmath.nstr(th/H, 8), tot[0], tot[1], mpmath.nstr(LO, 6), mpmath.nstr(HI, 6), MC, mpmath.nstr(MR, 6),
             n_in + 1, 16004*pr['D'], (n_in + 1)/(16004*pr['D'])))
