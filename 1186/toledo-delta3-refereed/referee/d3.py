# Referee's own exact model of the delta_3 problem. Written from the mathematics only.
from fractions import Fraction as F
U = 1096
BLOCKS = [28, 6, 28, 37, 59, 116, 116, 59, 37, 28, 6, 28]   # units of 1/548
EDGES = [0]
for b in BLOCKS: EDGES.append(EDGES[-1] + 2*b)              # units of 1/1096
SIGNS = [1 if k % 2 == 0 else -1 for k in range(12)]
assert EDGES[-1] == U

def sign_on(p, q):
    """sign of phi* on (p,q) in units; None if an edge is strictly inside"""
    for k in range(12):
        if EDGES[k] <= p and q <= EDGES[k+1]: return SIGNS[k]
    return None

def Phi(t):
    """int_0^t phi*, t a Fraction in [0,1]"""
    assert 0 <= t <= 1
    acc = F(0); x = t*U
    for k in range(12):
        lo, hi = EDGES[k], EDGES[k+1]
        if x <= lo: break
        acc += SIGNS[k]*(min(x, hi) - lo)
    return acc / U

def gstar(a):
    a = F(a)
    f1 = Phi((1+a)/2) - Phi(a/2)
    f2 = Phi(min(2*a, F(1))) - Phi(max(2*a-1, F(0)))
    return (f1+f2)/2

def phistar_at(t):
    """phi* at a non-edge point t (Fraction)"""
    x = t*U
    for k in range(12):
        if EDGES[k] < x < EDGES[k+1]: return SIGNS[k]
    raise ValueError('edge')

_H = None
def hnodes():
    global _H
    if _H is None:
        H = []
        for x in range(U+1):
            g = gstar(F(x, U))
            if x in EDGES[1:-1]:
                assert g == 0, ('g* nonzero at edge', x, g)
                H.append(F(0))
            else:
                s = SIGNS[0] if x == 0 else (SIGNS[-1] if x == U else phistar_at(F(x, U)))
                H.append(-s*g)
        _H = H
    return _H

def h_at(t):
    """h at a rational t by evaluating g* directly (not by interpolation)"""
    t = F(t)
    if t*U in EDGES[1:-1]: return F(0)
    x = t*U
    if x == 0: s = 1
    elif x == U: s = -1
    else: s = phistar_at(t)
    return -s*gstar(t)

# ---- areas of R ∩ [x0,x1]x[y0,y1], my route: rect minus the two excluded half-planes, integrating in b ----
def _int_pw_linear(f, lo, hi, brks):
    pts = sorted(set([lo, hi] + [b for b in brks if lo < b < hi]))
    acc = F(0)
    for u, v in zip(pts, pts[1:]):
        acc += (v-u)*(f(u)+f(v))/2   # f piecewise linear between pts
    return acc

def area_in(x0, x1, y0, y1):
    """x0..y1 Fractions in [0,1]; area of R ∩ rect"""
    rect = (x1-x0)*(y1-y0)
    # below: b < a/2  <=> a > 2b ; length in a of {a in [x0,x1]: a > 2b} = max(0, x1 - max(x0, 2b))
    below = _int_pw_linear(lambda b: max(F(0), x1 - max(x0, 2*b)), y0, y1, [x0/2, x1/2])
    # above: b > (1+a)/2 <=> a < 2b-1 ; length = max(0, min(x1, 2b-1) - x0)
    above = _int_pw_linear(lambda b: max(F(0), min(x1, 2*b-1) - x0), y0, y1, [(1+x0)/2, (1+x1)/2])
    return rect - below - above
