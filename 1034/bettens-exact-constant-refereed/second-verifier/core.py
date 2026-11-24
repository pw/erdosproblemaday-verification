"""Shared helpers for the decorrelated #1034 verifier (our own code; shares nothing with the deposit's verify.py).

Field K = Q(sqrt3): an element is a pair (a, b) of Fractions meaning a + b*sqrt3, real embedding sqrt3 > 0.
Graph/flag masks: bit idx(i,j) set iff {i,j} is an edge, pairs listed as itertools.combinations(range(n), 2).
"""
import os
import gzip
import itertools
import json
from fractions import Fraction

DEPOSIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'deposit')

# ---------------- field Q(sqrt3), exact ----------------
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))


def kparse(pair):
    a, b = pair
    return (Fraction(a), Fraction(b))


def kadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def ksub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def kneg(x):
    return (-x[0], -x[1])


def kmul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def kscale(x, q):
    """multiply by a rational q"""
    return (x[0] * q, x[1] * q)


def kinv(x):
    a, b = x
    n = a * a - 3 * b * b  # norm; nonzero unless x == 0 (sqrt3 irrational)
    if n == 0:
        raise ZeroDivisionError('inverse of zero in Q(sqrt3)')
    return (a / n, -b / n)


def ksign(x):
    """exact sign of a + b*sqrt3 in the real embedding sqrt3 > 0"""
    a, b = x
    sa = (a > 0) - (a < 0)
    sb = (b > 0) - (b < 0)
    if sa == 0:
        return sb
    if sb == 0 or sa == sb:
        return sa
    # opposite signs: compare a^2 with 3 b^2 (never equal unless both 0)
    return sa if a * a > 3 * b * b else sb


def kiszero(x):
    return x[0] == 0 and x[1] == 0


def kfloat(x):
    return float(x[0]) + float(x[1]) * 3 ** 0.5


# ---------------- graphs ----------------
def pairs(n):
    return list(itertools.combinations(range(n), 2))


PIDX = {n: {p: i for i, p in enumerate(pairs(n))} for n in range(1, 9)}


def edge(mask, n, i, j):
    if i == j:
        return 0
    if i > j:
        i, j = j, i
    return (mask >> PIDX[n][(i, j)]) & 1


def relabel(mask, n, perm):
    """new graph in which vertex perm[v] plays the role old vertex v played"""
    out = 0
    for b, (i, j) in enumerate(pairs(n)):
        if (mask >> b) & 1:
            a, c = perm[i], perm[j]
            if a > c:
                a, c = c, a
            out |= 1 << PIDX[n][(a, c)]
    return out


def restrict(mask, n, verts):
    """induced labelled graph on verts (in the given order) as a len(verts)-vertex mask"""
    m = len(verts)
    out = 0
    for b, (i, j) in enumerate(pairs(m)):
        if edge(mask, n, verts[i], verts[j]):
            out |= 1 << b
    return out


def load_model():
    with open(DEPOSIT + '/verification_model.json') as f:
        return json.load(f)


def load_cert():
    with gzip.open(DEPOSIT + '/certificate.json.gz', 'rt') as f:
        return json.load(f)
