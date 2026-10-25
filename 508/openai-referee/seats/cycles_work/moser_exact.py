#!/usr/bin/env python3
"""Exact verification of the Moser placement certificate (paper eqs. 8.5, 8.6, 8.4; Lemma 8.9).
Field arithmetic: Q(sqrt3, sqrt11) with basis (1, s3, s11, s33); all coefficients Fractions.
Sign decisions: a linear form a + b*s3 + c*s11 + d*s33 with rational a..d is evaluated with
rigorous rational enclosures of s3, s11, s33 (math.isqrt at scale 10^40); the sign is certified
iff the enclosure excludes 0, otherwise the script reports UNDECIDED (never a pass).
"""
from fractions import Fraction as F
from math import isqrt
import itertools, sys

class Q:
    __slots__ = ("c",)
    def __init__(s, a=0, b=0, c=0, d=0):
        s.c = (F(a), F(b), F(c), F(d))
    def __add__(s, o):
        o = o if isinstance(o, Q) else Q(o); return Q(*[x+y for x, y in zip(s.c, o.c)])
    __radd__ = __add__
    def __neg__(s): return Q(*[-x for x in s.c])
    def __sub__(s, o): return s + (-(o if isinstance(o, Q) else Q(o)))
    def __rsub__(s, o): return Q(o) - s
    def __mul__(s, o):
        o = o if isinstance(o, Q) else Q(o)
        a1, b1, c1, d1 = s.c; a2, b2, c2, d2 = o.c
        # s3^2=3, s11^2=11, s33^2=33, s3*s11=s33, s3*s33=3*s11, s11*s33=11*s3
        a = a1*a2 + 3*b1*b2 + 11*c1*c2 + 33*d1*d2
        b = a1*b2 + b1*a2 + 11*(c1*d2 + d1*c2)
        c = a1*c2 + c1*a2 + 3*(b1*d2 + d1*b2)
        d = a1*d2 + d1*a2 + b1*c2 + c1*b2
        return Q(a, b, c, d)
    __rmul__ = __mul__
    def __eq__(s, o):
        o = o if isinstance(o, Q) else Q(o); return s.c == o.c
    def __repr__(s): return "Q(%s)" % ", ".join(str(x) for x in s.c)

S3, S11, S33 = Q(0, 1), Q(0, 0, 1), Q(0, 0, 0, 1)
assert S3*S3 == Q(3) and S11*S11 == Q(11) and S3*S11 == S33 and S33*S33 == Q(33)

SC = 10**40
def encl(n):  # rational lo < sqrt(n) < hi, certified by squaring
    r = isqrt(n*SC*SC); lo, hi = F(r, SC), F(r+1, SC)
    assert lo*lo <= n < hi*hi
    return lo, hi
E = [None, encl(3), encl(11), encl(33)]

def sign(q):
    lo = hi = q.c[0]
    for k in (1, 2, 3):
        a = q.c[k]; l, h = E[k]
        if a >= 0: lo += a*l; hi += a*h
        else: lo += a*h; hi += a*l
    if lo > 0: return 1, lo, hi
    if hi < 0: return -1, lo, hi
    if lo == hi == 0: return 0, lo, hi
    return None, lo, hi  # UNDECIDED

class C:  # complex number with Q parts
    def __init__(s, re, im=0):
        s.re = re if isinstance(re, Q) else Q(re); s.im = im if isinstance(im, Q) else Q(im)
    def __add__(s, o): return C(s.re+o.re, s.im+o.im)
    def __sub__(s, o): return C(s.re-o.re, s.im-o.im)
    def __mul__(s, o): return C(s.re*o.re - s.im*o.im, s.re*o.im + s.im*o.re)
    def n2(s): return s.re*s.re + s.im*s.im

half = F(1, 2)
A = C(S3*half, Q(half)); B = C(S3*half, Q(-half)); T = C(S3, 0)
u = C(Q(F(5, 6)), S11*F(1, 6))
V = {"0": C(0, 0), "A": A, "B": B, "T": T, "uA": u*A, "uB": u*B, "uT": u*T}
EDGES = [("0","A"),("0","B"),("A","B"),("T","A"),("T","B"),
         ("0","uA"),("0","uB"),("uA","uB"),("uT","uA"),("uT","uB"),("T","uT")]

def check_edges(P, edges, tag):
    ok = True
    for a, b in edges:
        d2 = (P[a]-P[b]).n2()
        good = (d2 == Q(1))
        ok &= good
        print(f"  [{tag}] |{a}-{b}|^2 = {d2}  -> {'UNIT (exact)' if good else 'NOT UNIT  <-- REJECT'}")
    return ok

def region(z):
    xi, up = z.re, z.im
    l = xi*xi + up*up
    P = up*up*(3*xi*xi - up*up)*(3*xi*xi - up*up)
    Pp = l*l*l*(1 - l*F(1, 4))*(l - 1)*(l - 1)
    s1, l1, h1 = sign(l); s2, l2, h2 = sign(4 - l); s3, l3, h3 = sign(Pp - P)
    ok = (s1 == 1 and s2 == 1 and s3 == 1)
    return ok, (s1, s2, s3), (float(l1), float(l3)), l, P, Pp

def check_region(P, tag):
    allok = True
    for g, z in P.items():
        ok, sg, (lval, gap), *_ = region(z)
        allok &= ok
        print(f"  [{tag}] {g:>2}: z~({float(sign(z.re)[1]):+.6f},{float(sign(z.im)[1]):+.6f})  l~{lval:.6f}  "
              f"P'-P >= {gap:.6g}  signs(l,4-l,P'-P)={sg}  -> {'IN REGION' if ok else 'OUTSIDE/UNDECIDED  <-- REJECT'}")
    return allok

print("== 1. Unplaced Moser graph (8.5): eleven edges exactly unit")
ok1 = check_edges(V, EDGES, "G")
print("   all unit:", ok1)

print("== 2. Moser graph has no proper 3-colouring (brute force 3^7), has a proper 4-colouring (control)")
names = list(V)
def colourings(k):
    return [f for f in itertools.product(range(k), repeat=7)
            if all(f[names.index(a)] != f[names.index(b)] for a, b in EDGES)]
n3, n4 = len(colourings(3)), len(colourings(4))
print(f"   proper 3-colourings: {n3}   proper 4-colourings: {n4}")

print("== 3. Placement (8.6): z_g = M (g + c), M=(35+12i)/37, c=(-290+149i)/250")
M = C(Q(F(35, 37)), Q(F(12, 37))); c = C(Q(F(-290, 250)), Q(F(149, 250)))
print("   |M|^2 =", M.n2(), "(exact)")
Z = {g: M*(z + c) for g, z in V.items()}
ok3 = check_edges(Z, EDGES, "placed")
print("   all placed edges unit:", ok3)
print("== 4. Region (8.4) + 0<l<4 for every placed vertex (exact field values, certified signs)")
ok4 = check_region(Z, "placed")
print("   all seven in region:", ok4)
print("   distinct vertices:", len({tuple(z.re.c + z.im.c) for z in Z.values()}) == 7)

print("== 5. CONTROLS (each must be REJECTED)")
Zp = dict(Z); Zp["uT"] = Z["uT"] + C(Q(F(1, 100)), 0)
c1 = check_edges(Zp, [("T", "uT"), ("uT", "uA"), ("uT", "uB")], "perturbed uT by +0.01")
print("   control 5a (perturbed vertex) edges all unit?", c1, "(expected False)")
c2 = check_edges(Z, [("0", "T"), ("A", "uA")], "non-edges")
print("   control 5b (non-unit pairs claimed as edges) all unit?", c2, "(expected False)")
c3 = check_region({"origin": C(0, 0), "1.5e^{i pi/6}": C(S3*F(3, 4), Q(F(3, 4))),
                   "unit-circle 1": C(1, 0), "radius 2": C(2, 0)}, "bad points")
print("   control 5c (points that must lie outside) all in region?", c3, "(expected False)")
Zc = {g: (z + c) for g, z in V.items()}   # translation only, no rotation
c4 = check_region(Zc, "no rotation")
print("   control 5d (placement without the rotation M) all in region?", c4, "(expected False)")
Zd = {g: M*(z + C(Q(F(-290, 250)), Q(F(149, 250))) + C(Q(F(3, 10)), 0)) for g, z in V.items()}
c5 = check_region(Zd, "shifted by M*0.3")
print("   control 5e (placement shifted by M*0.3) all in region?", c5, "(expected False)")
u_bad = C(Q(F(5, 6)), S11*F(1, 5))
Vb = dict(V); Vb["uA"], Vb["uB"], Vb["uT"] = u_bad*A, u_bad*B, u_bad*T
c6 = check_edges(Vb, [("T", "uT"), ("0", "uA")], "wrong u=(5/6)+i*sqrt11/5")
print("   control 5f (wrong rotation u) all unit?", c6, "(expected False)")
verdict = ok1 and n3 == 0 and n4 > 0 and ok3 and ok4 and not any([c1, c2, c3, c4, c5, c6])
print("VERDICT:", "CERTIFICATE VERIFIED, ALL CONTROLS REJECTED" if verdict else "FAILURE")
sys.exit(0 if verdict else 1)
