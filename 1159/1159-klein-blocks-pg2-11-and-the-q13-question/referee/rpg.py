"""Referee's own PG(2,p) for prime p, written from scratch (no import of author's code).
Points/lines: nonzero vectors of F_p^3 normalised so the FIRST nonzero coordinate is 1.
Incidence: point P on line L  <=>  P.L == 0 (mod p)."""
import itertools

def norm(v, p):
    v = [x % p for x in v]
    for x in v:
        if x:
            inv = pow(x, p - 2, p)
            return tuple((y * inv) % p for y in v)
    raise ValueError("zero vector")

def plane(p):
    pts = sorted({norm(v, p) for v in itertools.product(range(p), repeat=3) if any(v)})
    assert len(pts) == p * p + p + 1
    idx = {P: i for i, P in enumerate(pts)}
    lines = pts[:]  # line coordinates, same normal form
    inc = [frozenset(i for i, P in enumerate(pts) if sum(a * b for a, b in zip(P, L)) % p == 0) for L in lines]
    # axioms: every line q+1 points, every point on q+1 lines, two lines meet in exactly one point
    assert all(len(l) == p + 1 for l in inc)
    deg = [0] * len(pts)
    for l in inc:
        for i in l: deg[i] += 1
    assert all(d == p + 1 for d in deg)
    for a, b in itertools.combinations(range(len(inc)), 2):
        assert len(inc[a] & inc[b]) == 1
    return pts, idx, lines, inc

def spectrum(S_idx, inc):
    from collections import Counter
    S = set(S_idx)
    return dict(sorted(Counter(len(S & l) for l in inc).items()))

def matmul(A, B, p):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) % p for j in range(3)) for i in range(3))

def matvec(A, v, p):
    return tuple(sum(A[i][k] * v[k] for k in range(3)) % p for i in range(3))

def det(A, p):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])) % p

def inv(A, p):
    d = det(A, p)
    assert d, "singular"
    di = pow(d, p - 2, p)
    C = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            m = [[A[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
            C[i][j] = ((-1) ** (i + j)) * (m[0][0] * m[1][1] - m[0][1] * m[1][0])
    # inverse = adj / det, adj = C^T
    return tuple(tuple((C[j][i] * di) % p for j in range(3)) for i in range(3))

def mnorm(A, p):
    """normalise a matrix up to scalar: first nonzero entry (row-major) = 1"""
    flat = [x % p for r in A for x in r]
    for x in flat:
        if x:
            iv = pow(x, p - 2, p)
            f = [(y * iv) % p for y in flat]
            return (tuple(f[0:3]), tuple(f[3:6]), tuple(f[6:9]))
    raise ValueError

def solve3(M, b, p):
    """solve M x = b (M given as list of columns? no: rows)"""
    Mi = inv(M, p)
    return matvec(Mi, b, p)

def frame_matrix(P, p):
    """P = 4 vectors in general position. Return matrix A with A e_i ~ P_i (i=1..3), A (1,1,1) ~ P_4."""
    cols = P[:3]
    M = tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))  # columns P1 P2 P3
    a = solve3(M, P[3], p)
    assert all(a), "not general position"
    return tuple(tuple((cols[j][i] * a[j]) % p for j in range(3)) for i in range(3))

def proj_from_frames(P, Q, p):
    """unique projectivity sending P_i -> Q_i (i=1..4), both frames"""
    A = frame_matrix(P, p); B = frame_matrix(Q, p)
    return mnorm(matmul(B, inv(A, p), p), p)

def general_position(vs, p):
    for a, b, c in itertools.combinations(vs, 3):
        M = (a, b, c)
        if det(M, p) == 0:
            return False
    return True
