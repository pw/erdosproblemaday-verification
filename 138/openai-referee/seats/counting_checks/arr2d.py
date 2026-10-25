"""Exact face enumeration for a line arrangement in a closed axis box (Fractions).
Lines are (A, B, C) meaning A*a + B*b = C.  Returns one rational sample point in the
relative interior of every face (vertex / edge / region) of the arrangement formed by
the given lines together with the 4 box lines, restricted to the closed box."""
from fractions import Fraction as Fr
from itertools import combinations

def norm_line(A, B, C):
    A, B, C = Fr(A), Fr(B), Fr(C)
    if A != 0:
        s = A
    elif B != 0:
        s = B
    else:
        raise ValueError("degenerate line")
    return (A / s, B / s, C / s)

def face_points(lines, box):
    x0, x1, y0, y1 = [Fr(v) for v in box]
    L = set(norm_line(*l) for l in lines)
    L |= {(Fr(1), Fr(0), x0), (Fr(1), Fr(0), x1), (Fr(0), Fr(1), y0), (Fr(0), Fr(1), y1)}
    L = sorted(L)
    inbox = lambda p: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
    on = {i: set() for i in range(len(L))}
    verts = set()
    for i, j in combinations(range(len(L)), 2):
        A1, B1, C1 = L[i]; A2, B2, C2 = L[j]
        det = A1 * B2 - A2 * B1
        if det == 0:
            continue
        p = ((C1 * B2 - C2 * B1) / det, (A1 * C2 - A2 * C1) / det)
        if inbox(p):
            verts.add(p); on[i].add(p); on[j].add(p)
    pts = set(verts)
    for i, (A, B, C) in enumerate(L):
        vs = sorted(on[i], key=(lambda p: p[0]) if B != 0 else (lambda p: p[1]))
        for p, q in zip(vs, vs[1:]):
            m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
            pts.add(m)
            eps = None
            for j, (A2, B2, C2) in enumerate(L):
                if j == i:
                    continue
                f = A2 * m[0] + B2 * m[1] - C2
                g = A2 * A + B2 * B
                if f == 0:
                    raise RuntimeError("midpoint on another line")
                if g != 0:
                    r = abs(f) / abs(g)
                    eps = r if eps is None or r < eps else eps
            eps = Fr(1) if eps is None else eps / 2
            for sgn in (1, -1):
                pt = (m[0] + sgn * eps * A, m[1] + sgn * eps * B)
                if inbox(pt):
                    pts.add(pt)
    return pts

def sgn(x):
    return (x > 0) - (x < 0)

def sign_vector(lines, p):
    return tuple(sgn(A * p[0] + B * p[1] - C) for (A, B, C) in lines)
