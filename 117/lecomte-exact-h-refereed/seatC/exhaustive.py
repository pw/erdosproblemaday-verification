"""exhaustive.py -- ALL commutation structures of class-2 groups with elementary abelian central
quotient V = F_p^d and commutator map into an elementary abelian p-group.

Commutation x~y (noncommuting) iff some form in W is nonzero on (x,y), where W is the F_p-span of the
coordinate forms of the commutator map: a subspace of Alt(V) = Lambda^2 V* (dim m = d(d-1)/2).
So the noncommuting graph (hence omega, a, and z = |V/rad W|) depends only on W.  We enumerate EVERY
subspace W of dimension e (as reduced-row-echelon generator matrices), for the requested e.

usage: python3 exhaustive.py p d e_list out_prefix      e.g.  3 4 1,2,3,4,5,6 ex/p3d4
For each W: omega exact (python MCQ, witness checked), a exact (DSATUR + clique-seeded SAT; witness
colouring checked), z.  Flags a > T(omega), z > (T(omega)-1)^2 (omega>=3), and equality a = T(omega).
"""
import sys, itertools, time, json
import numpy as np
from collections import defaultdict
from graphlib import T, max_clique, chromatic, check_clique, check_colouring


def rref_matrices(p, m, e):
    """all e x m reduced row echelon matrices of rank e over F_p."""
    for piv in itertools.combinations(range(m), e):
        free = []  # positions (row, col) that are free: col > piv[row], col not a pivot
        for r in range(e):
            for c in range(piv[r] + 1, m):
                if c not in piv:
                    free.append((r, c))
        for vals in itertools.product(range(p), repeat=len(free)):
            A = np.zeros((e, m), dtype=np.int64)
            for r in range(e):
                A[r, piv[r]] = 1
            for (r, c), v in zip(free, vals):
                A[r, c] = v
            yield A


def gaussian_binomial(m, e, p):
    num = 1
    den = 1
    for i in range(e):
        num *= p ** (m - i) - 1
        den *= p ** (i + 1) - 1
    return num // den


def main():
    p, d = int(sys.argv[1]), int(sys.argv[2])
    elist = [int(x) for x in sys.argv[3].split(',')]
    prefix = sys.argv[4]
    chunk, nchunks = (map(int, sys.argv[5].split('/')) if len(sys.argv) > 5 else (0, 1))
    N = p ** d
    X = np.array([[(idx // p ** i) % p for i in range(d)] for idx in range(N)], dtype=np.int64)
    pairs = [(i, j) for i in range(d) for j in range(i + 1, d)]
    m = len(pairs)
    # D[k] = x_i y_j - x_j y_i for pair k, as N x N
    D = np.stack([(np.outer(X[:, i], X[:, j]) - np.outer(X[:, j], X[:, i])) % p for (i, j) in pairs])  # m x N x N
    Dflat = D.reshape(m, N * N)
    summary = []
    allflags = []
    for e in elist:
        t0 = time.time()
        expected = gaussian_binomial(m, e, p)
        cnt = 0
        dist = defaultdict(int)          # (omega, a, z) -> count
        worst = (0, None)
        flags = defaultdict(list)
        seen = 0
        for A in rref_matrices(p, m, e):
            seen += 1
            if (seen - 1) % nchunks != chunk:
                continue
            cnt += 1
            if cnt % 10000 == 0:
                print('   progress e=%d: %d done (%.0fs)' % (e, cnt, time.time() - t0)); sys.stdout.flush()
            vals = (A @ Dflat) % p                     # e x N^2
            nonc = (vals != 0).any(axis=0).reshape(N, N)
            rad = ~nonc.any(axis=1)
            z = N // int(rad.sum())
            classes = {}
            for v in range(N):
                if not rad[v]:
                    classes.setdefault(nonc[v].tobytes(), v)
            reps = list(classes.values())
            k = len(reps)
            if k == 0:
                w, a = 1, 1
            else:
                sub = nonc[np.ix_(reps, reps)]
                adj = [int(sum(1 << int(j) for j in np.nonzero(sub[i])[0])) for i in range(k)]
                C = max_clique(k, adj)
                assert check_clique(adj, C)
                w = len(C)
                a, col, src = chromatic(k, adj, C)
                assert check_colouring(k, adj, col) and max(col) + 1 == a
            dist[(w, a, z)] += 1
            t = T(w)
            r = a / t
            if r > worst[0]:
                worst = (r, (w, a, z, A.tolist()))
            if a > t:
                flags['A-VIOL'].append((w, a, z, A.tolist()))
            if w >= 3 and z > (t - 1) ** 2:
                flags['Z-VIOL'].append((w, a, z, A.tolist()))
            if w >= 3 and a == t:
                flags['A-EQ'].append((w, a, z))
            if w >= 3 and z == (t - 1) ** 2:
                flags['Z-EQ'].append((w, a, z))
        el = time.time() - t0
        lines = ['p=%d d=%d e=%d chunk %d/%d: subspaces analysed %d of %d enumerated (Gaussian binomial [%d,%d]_%d = %d) in %.1fs' % (p, d, e, chunk, nchunks, cnt, seen, m, e, p, expected, el)]
        assert seen == expected
        lines.append('   (omega, a, z) -> #subspaces: ' + ', '.join('%s:%d' % (key, c) for key, c in sorted(dist.items())))
        lines.append('   worst a/T(omega) = %.4f at (omega,a,z)=%s' % (worst[0], worst[1][:3] if worst[1] else None))
        for key in ['A-VIOL', 'Z-VIOL', 'A-EQ', 'Z-EQ']:
            L = flags[key]
            if key.endswith('VIOL'):
                lines.append('   %s: %d%s' % (key, len(L), (' e.g. ' + json.dumps(L[0])) if L else ''))
            else:
                c = defaultdict(int)
                for x in L:
                    c[x] += 1
                lines.append('   %s: %d %s' % (key, len(L), dict(c)))
        print('\n'.join(lines))
        sys.stdout.flush()
        summary.extend(lines)
        allflags.extend([(e, k2, v) for k2 in ('A-VIOL', 'Z-VIOL') for v in flags[k2]])
    open(prefix + '.summary.txt', 'w').write('\n'.join(summary) + '\n')
    with open(prefix + '.violations.json', 'w') as f:
        json.dump(allflags, f)


if __name__ == '__main__':
    main()
