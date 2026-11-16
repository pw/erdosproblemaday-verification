"""sharp.py -- the paper's sharp examples, computed exactly.

Inputs: sharp/es_graphs.txt (GAP export of ExtraspecialGroup(2^(2r+1),+/-), r=2,3,4, and
ExtraspecialGroup(243,3/9)); plus the F_9 'trace' determinant model built here from its bilinear
map (no GAP): V = F_9^2 = F_3^4, beta(x,y) = Tr_{F9/F3}(x1*y2 - x2*y1).

For each: omega exact (C MCQ, proven; Python MCQ as second implementation where small),
alpha exact (max independent set = clique of complement, C MCQ proven), a lower bound
max(omega, ceil(k/alpha)), a upper bound from a verified colouring (DSATUR / tabucol / SAT),
SAT UNSAT at (a-1) as an independent lower-bound certificate when feasible.
Also writes sharp/f9_table.txt (multiplication table of the 243-element group
(v,c)(w,d) = (v+w, c+d+2*beta(v,w))) for GAP IdGroup.
"""
import itertools, time, sys
from graphlib import (parse_rows, check_clique, check_colouring, max_clique, dsatur, colour_sat,
                      c_clique, c_dsatur, c_tabu, T)


def analyse(label, k, adj, z, expect_omega=None, expect_a=None, py_clique=True, sat_lb=True):
    t0 = time.time()
    C, pr = c_clique(k, adj, 3000, 0)
    w = len(C)
    line = ['%s: z=%d twin-classes=%d' % (label, z, k)]
    line.append('omega=%d (C MCQ proven=%s, witness %s)' % (w, pr, C))
    if py_clique:
        w2 = len(max_clique(k, adj))
        line.append('python MCQ omega=%d' % w2)
        assert w2 == w
    full = (1 << k) - 1
    cadj = [(~adj[v]) & full & ~(1 << v) for v in range(k)]
    I, pra = c_clique(k, cadj, 3000, 0)
    alpha = len(I)
    lo = max(w, -(-k // alpha))
    line.append('alpha=%d (proven=%s) => a >= max(omega, ceil(%d/%d)) = %d' % (alpha, pra, k, alpha, lo))
    col = c_dsatur(k, adj)
    hi = max(col) + 1
    how = 'DSATUR'
    if hi > lo:
        for seed in range(1, 6):
            c2 = c_tabu(k, adj, lo, 2000000, seed)
            if c2 is not None:
                col, hi, how = c2, lo, 'tabucol(seed %d)' % seed
                break
    if hi > lo:
        c3 = colour_sat(k, adj, lo, C)
        if c3 is not None:
            col, hi, how = c3, max(c3) + 1, 'SAT'
    assert check_colouring(k, adj, col)
    line.append('colouring with %d colours by %s (verified proper)' % (hi, how))
    exact = (hi == lo)
    sat_note = ''
    if sat_lb and hi > w:
        r = colour_sat(k, adj, hi - 1, C)
        sat_note = 'SAT(%d colours, clique-seeded) = %s' % (hi - 1, 'UNSAT' if r is None else 'SAT?!')
        if r is None:
            exact = True
        line.append(sat_note)
    a = hi if exact else None
    line.append('=> a = %s ; T(omega)=%d ; (T(omega)-1)^2=%d ; z=%d' % (a if a is not None else '[%d,%d]' % (lo, hi), T(w), (T(w) - 1) ** 2, z))
    status = []
    if expect_omega is not None:
        status.append('omega %s expected %d' % ('==' if w == expect_omega else '!=', expect_omega))
    if expect_a is not None:
        status.append('a %s expected %d' % ('==' if a == expect_a else '!=', expect_a))
    line.append('; '.join(status) + ' (%.1fs)' % (time.time() - t0))
    print('\n   '.join(line))
    sys.stdout.flush()
    return w, a, alpha


# ---- F_9 arithmetic: a + b*i with i^2 = -1 over F_3 ----
def f9mul(x, y):
    a, b = x
    c, d = y
    return ((a * c - b * d) % 3, (a * d + b * c) % 3)


def f9sub(x, y):
    return ((x[0] - y[0]) % 3, (x[1] - y[1]) % 3)


def tr(x):
    return (2 * x[0]) % 3


def beta_f9(v, w):
    x1, x2 = (v[0], v[1]), (v[2], v[3])
    y1, y2 = (w[0], w[1]), (w[2], w[3])
    return tr(f9sub(f9mul(x1, y2), f9mul(x2, y1)))


def f9_model():
    V = list(itertools.product(range(3), repeat=4))
    nz = [v for v in V if any(v)]
    # Gram matrix on the standard basis, check alternating + nondegenerate
    E = [tuple(1 if i == j else 0 for i in range(4)) for j in range(4)]
    G = [[beta_f9(E[i], E[j]) for j in range(4)] for i in range(4)]
    for v in V:
        assert beta_f9(v, v) == 0
    rad = [v for v in nz if all(beta_f9(v, w) == 0 for w in V)]
    assert not rad, 'trace form degenerate?'
    # bilinearity spot check
    for v in V[:20]:
        for w in V[:20]:
            for u in V[:10]:
                vw = tuple((a + b) % 3 for a, b in zip(v, w))
                assert beta_f9(vw, u) == (beta_f9(v, u) + beta_f9(w, u)) % 3
    # twin classes: same centraliser {w: beta(v,w)=0}
    cent = {}
    for v in nz:
        key = frozenset(w for w in nz if beta_f9(v, w) == 0)
        cent.setdefault(key, []).append(v)
    reps = [vs[0] for vs in cent.values()]
    k = len(reps)
    adj = [0] * k
    for i in range(k):
        for j in range(k):
            if beta_f9(reps[i], reps[j]) != 0:
                adj[i] |= 1 << j
    # spread from the 10 F_9-lines: colour of v = the F_9-line through v
    F9 = [(a, b) for a in range(3) for b in range(3)]
    line_of = {}
    lines = []
    for v in nz:
        if v in line_of:
            continue
        L = set()
        for lam in F9:
            if lam == (0, 0):
                continue
            x1 = f9mul(lam, (v[0], v[1]))
            x2 = f9mul(lam, (v[2], v[3]))
            L.add((x1[0], x1[1], x2[0], x2[1]))
        for u in L:
            line_of[u] = len(lines)
        lines.append(L)
    spread_col = [line_of[r] for r in reps]
    assert check_colouring(k, adj, spread_col)
    print('F_9 trace model: Gram matrix over F_3 basis =', G, '; 80 nonzero vectors, %d twin classes (projective points); '
          'F_9-line spread gives a verified proper colouring with %d colours' % (k, len(lines)))
    # multiplication table for GAP: elements (v, c) indexed v-major
    elems = [(v, c) for v in V for c in range(3)]
    idx = {e: i for i, e in enumerate(elems)}
    with open('sharp/f9_table.txt', 'w') as f:
        rows = []
        for (v, c) in elems:
            row = []
            for (w, d) in elems:
                s = tuple((a + b) % 3 for a, b in zip(v, w))
                row.append(idx[(s, (c + d + 2 * beta_f9(v, w)) % 3)] + 1)
            rows.append('[' + ','.join(map(str, row)) + ']')
        f.write('F9TABLE := [' + ',\n'.join(rows) + '];\n')
    return k, adj


def main():
    print('== extraspecial groups exported by GAP')
    for line in open('sharp/es_graphs.txt'):
        body = line.split('#')[0].split()
        label, order, z, k = body[0], int(body[1]), int(body[2]), int(body[3])
        kk, adj = parse_rows(body[4:])
        if label.startswith('ES2'):
            r = {32: 2, 128: 3, 512: 4}[order]
            analyse(label, kk, adj, z, 2 * r + 1, 2 ** r + 1, py_clique=(kk <= 63), sat_lb=(kk <= 63))
        else:
            analyse(label, kk, adj, z, 7, 10)
    print('== F_9 trace model from its bilinear map (no GAP)')
    k, adj = f9_model()
    w, a, alpha = analyse('F9-trace-model', k, adj, 81, 7, 10)
    # independent second check of "no 8-clique": exhaustive over 8-subsets is C(40,8)=76.9M -- instead
    # proven-empty search for cliques of size >= 8 by the C MCQ and the Python MCQ (above)
    C8, pr = c_clique(k, adj, 3000, 8)
    print('   C MCQ search for cliques of size >= 8: %s, proven=%s' % ('none' if C8 is None else C8, pr))


if __name__ == '__main__':
    main()
