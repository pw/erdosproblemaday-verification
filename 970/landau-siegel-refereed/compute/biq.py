"""Exact arithmetic in R = Z[a,b], a^2 = d, b^2 = 2, elements as 4-tuples (z1,z2,z3,z4) = z1 + z2 a + z3 b + z4 ab.
Seat C, oaimath/003. Pure Python ints (exact) + mod-p embeddings for split primes (K -> F_p)."""
import math, random
from sympy.ntheory import isprime
from sympy.functions.combinatorial.numbers import legendre_symbol as _ls
def legendre_symbol(a, p): return int(_ls(a, p))
from sympy.ntheory.residue_ntheory import sqrt_mod

def mul(x, y, d):
    x1, x2, x3, x4 = x; y1, y2, y3, y4 = y
    return (x1*y1 + d*x2*y2 + 2*x3*y3 + 2*d*x4*y4,
            x1*y2 + x2*y1 + 2*(x3*y4 + x4*y3),
            x1*y3 + x3*y1 + d*(x2*y4 + x4*y2),
            x1*y4 + x4*y1 + x2*y3 + x3*y2)

def add(x, y): return tuple(u+v for u, v in zip(x, y))
def sub(x, y): return tuple(u-v for u, v in zip(x, y))
ONE = (1, 0, 0, 0); ZERO = (0, 0, 0, 0)
def sig(x): return (x[0], -x[1], x[2], -x[3])      # a -> -a
def tau(x): return (x[0], x[1], -x[2], -x[3])      # b -> -b
def sigtau(x): return (x[0], -x[1], -x[2], x[3])
def norm(x, d):
    y = mul(mul(x, sig(x), d), mul(tau(x), sigtau(x), d), d)
    assert y[1] == y[2] == y[3] == 0, y
    return y[0]

def rpow(x, k, d):
    r = ONE
    base = x
    while k:
        if k & 1: r = mul(r, base, d)
        base = mul(base, base, d); k >>= 1
    return r

def vp_int(z, p):
    if z == 0: return math.inf
    v = 0
    while z % p == 0: z //= p; v += 1
    return v

def vp_R(x, p):
    """largest e with x in p^e R, i.e. all four coordinates divisible by p^e."""
    return min(vp_int(z, p) for z in x)

def frob_class(p, d):
    """Frobenius of odd p not dividing d in Gal(K/Q) = {id, sigma, tau, sigmatau}."""
    if p == 2 or d % p == 0: return 'ram'
    ld = legendre_symbol(d % p, p); l2 = legendre_symbol(2, p)
    return {(1, 1): 'id', (-1, 1): 'sigma', (1, -1): 'tau', (-1, -1): 'sigtau'}[(ld, l2)]

def split_primes(d, nbits=62, count=1, seed=1):
    """primes p ~ 2^nbits, p = 1 mod 8, (d/p)=1, p not dividing d; returns list of (p, s, t) with s^2=d, t^2=2 mod p."""
    rng = random.Random(seed)
    out = []
    while len(out) < count:
        p = rng.randrange(2**(nbits-1), 2**nbits) | 1
        if p % 8 != 1 or not isprime(p) or d % p == 0: continue
        if legendre_symbol(d % p, p) != 1: continue
        s = sqrt_mod(d % p, p); t = sqrt_mod(2, p)
        assert s*s % p == d % p and t*t % p == 2
        out.append((p, s, t))
    return out

def embed(x, p, s, t, e1=1, e2=1):
    return (x[0] + x[1]*e1*s + x[2]*e2*t + x[3]*e1*e2*s*t) % p

# coordinate maps for the three row factors; 'paper' = (theta, sigma theta, sigmatau theta)
def coord_maps(variant):
    if variant == 'paper':  return (lambda x: x, sig, sigtau)
    if variant == 'tau':    return (lambda x: x, tau, sigtau)        # wrong conjugate in slot 2
    if variant == 'wrong2': return (lambda x: x, lambda x: add(sig(x), ONE), sigtau)  # slot 2 = sigma(theta)+1
    raise ValueError(variant)
