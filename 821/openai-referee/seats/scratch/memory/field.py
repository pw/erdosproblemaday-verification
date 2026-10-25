# Exact arithmetic in Q(sqrt2, i): element = (a,b,c,d) meaning (a + b*s) + i*(c + d*s), s = sqrt(2).
from fractions import Fraction as Fr

def E(a=0, b=0, c=0, d=0):
    return (Fr(a), Fr(b), Fr(c), Fr(d))

ZERO = E(0); ONE = E(1)

def add(x, y): return (x[0]+y[0], x[1]+y[1], x[2]+y[2], x[3]+y[3])
def sub(x, y): return (x[0]-y[0], x[1]-y[1], x[2]-y[2], x[3]-y[3])
def neg(x): return (-x[0], -x[1], -x[2], -x[3])

def _m2(a, b, e, f):  # (a+b s)(e+f s)
    return (a*e + 2*b*f, a*f + b*e)

def mul(x, y):
    a, b, c, d = x; e, f, g, h = y
    xx = _m2(a, b, e, f); yy = _m2(c, d, g, h); xy = _m2(a, b, g, h); yx = _m2(c, d, e, f)
    return (xx[0]-yy[0], xx[1]-yy[1], xy[0]+yx[0], xy[1]+yx[1])

def conj(x): return (x[0], x[1], -x[2], -x[3])

def inv(x):
    a, b, c, d = x
    n0 = a*a + 2*b*b + c*c + 2*d*d
    n1 = 2*a*b + 2*c*d
    den = n0*n0 - 2*n1*n1
    if den == 0: raise ZeroDivisionError
    ninv = E(n0/den, -n1/den)
    return mul(conj(x), ninv)

def div(x, y): return mul(x, inv(y))

def powe(x, n):
    r = ONE
    if n < 0: x = inv(x); n = -n
    for _ in range(n): r = mul(r, x)
    return r

def scal(x, fr): fr = Fr(fr); return (x[0]*fr, x[1]*fr, x[2]*fr, x[3]*fr)

def sqrt_of_q(q):
    """exact sqrt of a rational q, returned in Q(sqrt2): q must be a rational square or 2*square"""
    q = Fr(q)
    from math import isqrt
    def issq(fr):
        n, d = fr.numerator, fr.denominator
        rn, rd = isqrt(n), isqrt(d)
        return (rn*rn == n and rd*rd == d), Fr(rn, rd)
    ok, r = issq(q)
    if ok: return E(r)
    ok, r = issq(q/2)   # q = 2 r^2 -> sqrt q = r*sqrt2
    if ok: return E(0, r)
    raise ValueError("sqrt(q) not in Q(sqrt2)")

# zeta8 = e(1/8) = (1+i)/sqrt2 = (sqrt2/2)(1+i)
ZETA8 = E(0, Fr(1, 2), 0, Fr(1, 2))
_Z8 = [ONE]
for _ in range(7): _Z8.append(mul(_Z8[-1], ZETA8))
assert mul(_Z8[7], ZETA8) == ONE

def e8(n):   # e(n/8)
    return _Z8[n % 8]

def fmt(x):
    a, b, c, d = x
    parts = []
    for coef, name in ((a, ''), (b, '*sqrt2'), (c, '*i'), (d, '*i*sqrt2')):
        if coef != 0: parts.append(f"({coef}){name}")
    return ' + '.join(parts) if parts else '0'

def approx(x):
    s = 2 ** 0.5
    return complex(float(x[0]) + float(x[1]) * s, float(x[2]) + float(x[3]) * s)
