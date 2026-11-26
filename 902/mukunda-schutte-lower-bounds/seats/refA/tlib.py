"""Referee A's own tournament helpers (written from scratch; no repo code used).

Representation: adjacency matrix A (numpy int8), A[i,j]=1 iff i -> j.
Bitmasks: inmask[v] = Python int with bit w set iff w -> v (w beats v).
D(X) = common dominators = AND of inmask over X (automatically excludes X,
since no vertex beats itself and x in X cannot beat x' in X and itself...
careful: x in X could beat all other members of X; but x does not beat x,
so bit x is absent from inmask[x], hence absent from the AND).
"""
import itertools
import numpy as np


def is_prime(p):
    if p < 2:
        return False
    i = 2
    while i * i <= p:
        if p % i == 0:
            return False
        i += 1
    return True


def paley(p):
    assert is_prime(p) and p % 4 == 3
    qr = {(x * x) % p for x in range(1, p)}
    A = np.zeros((p, p), dtype=np.int8)
    for i in range(p):
        for j in range(p):
            if i != j and ((j - i) % p) in qr:
                A[i, j] = 1  # i -> j iff j-i is a nonzero square
    return A


def check_tournament(A):
    n = A.shape[0]
    assert A.shape == (n, n)
    assert np.all(np.diag(A) == 0)
    S = A + A.T
    off = ~np.eye(n, dtype=bool)
    assert np.all(S[off] == 1), "not a tournament"
    assert set(np.unique(A)) <= {0, 1}
    return True


def inmasks(A):
    n = A.shape[0]
    m = []
    for v in range(n):
        x = 0
        for w in range(n):
            if A[w, v]:
                x |= 1 << w
        m.append(x)
    return m


def outmasks(A):
    n = A.shape[0]
    m = []
    for v in range(n):
        x = 0
        for w in range(n):
            if A[v, w]:
                x |= 1 << w
        m.append(x)
    return m


def popcount(x):
    return bin(x).count("1")


def D(inm, X):
    """common dominators of the vertex set X (bitmask)."""
    r = -1
    for x in X:
        r &= inm[x]
    return r


def triple_counts(A):
    """returns dict (i,j,k)->|D|, plus sigma (1 transitive, 0 cyclic)."""
    n = A.shape[0]
    inm = inmasks(A)
    res = {}
    for i, j, k in itertools.combinations(range(n), 3):
        res[(i, j, k)] = popcount(inm[i] & inm[j] & inm[k])
    return res


def sigma(A, Y):
    i, j, k = Y
    # transitive iff some vertex beats the other two
    for a, b, c in ((i, j, k), (j, i, k), (k, i, j)):
        if A[a, b] and A[a, c]:
            return 1
    return 0


def min_dom(A, s):
    n = A.shape[0]
    inm = inmasks(A)
    best = None
    for X in itertools.combinations(range(n), s):
        r = -1
        for x in X:
            r &= inm[x]
        c = popcount(r) if r != -1 else n
        if best is None or c < best:
            best = c
    return best


def has_S(A, s):
    """True iff every s-set has a dominator; returns (bool, witness)."""
    n = A.shape[0]
    inm = inmasks(A)
    for X in itertools.combinations(range(n), s):
        r = -1
        for x in X:
            r &= inm[x]
        if r == 0:
            return False, X
    return True, None
