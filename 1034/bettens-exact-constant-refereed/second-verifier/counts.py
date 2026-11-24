"""Route A, combinatorial half: for every order-7 graph H, count the rooted configurations that the
coefficient of H in each generator is an average over.

Semantics (paper sections 4-5): coefficient of H in [[G_1...G_r]]_sigma is the probability, over a
uniformly random injective placement of the k roots in V(H) and uniformly random disjoint extension
sets of the right sizes in the remaining vertices, that the roots induce sigma (as labelled) and each
extension set induces G_i.  Lower-order terms are lifted by the same average (unused vertices ignored).

We store integer counts; normalisations are applied in evalA.py:
  b5  : k=5 types, two single-vertex extensions (A,B) ordered: 2520 root maps * 2 ordered pairs
  b3  : k=3 types, two 2-vertex extensions (A,B) ordered: 210 * 6
  b1  : type [1,0], two 3-vertex extensions ordered: 7 * 20
  t0  : tau = labelled triangle, single vertices (a,b,c) ordered; c carries D: 210 * 24
  t6  : tau, 3-vertex extension A and single vertex c carrying D: 210 * 4
  bol : type K4-01, remaining three vertices; stores 3*(X^3 - 11 X E + 30 T + 15 P3) summed over roots: 840 * 3
Flags are keyed by canonical mask = min over orderings of the extension vertices (roots fixed).
"""
import os
import itertools
import json
import pickle
import sys
import time
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import PIDX, load_model

N = 7
V = range(N)
PL = {ell: [(i, j, 1 << PIDX[ell][(i, j)]) for (i, j) in itertools.combinations(range(ell), 2)] for ell in range(1, 8)}
ROOTS = {k: list(itertools.permutations(V, k)) for k in (1, 3, 4, 5)}

TYPES5 = None  # set of labelled 5-vertex type masks used by blocks
TYPES3 = None


def tmask(adj, verts, ell):
    m = 0
    for i, j, bit in PL[ell]:
        if adj[verts[i]][verts[j]]:
            m |= bit
    return m


def canon_ext(adj, roots, ext):
    ell = len(roots) + len(ext)
    return min(tmask(adj, roots + o, ell) for o in itertools.permutations(ext))


def count_one(args):
    rep, = args
    adj = [[0] * N for _ in V]
    for (i, j), b in PIDX[N].items():
        if (rep >> b) & 1:
            adj[i][j] = adj[j][i] = 1
    out = {'b5': {}, 'b3': {}, 'b1': Counter(), 't0all': Counter(), 't0D': Counter(),
           't6all': Counter(), 't6D': Counter(), 'bol3': 0,
           'edges': sum(adj[i][j] for i, j in itertools.combinations(V, 2)),
           'theta_hits': Counter()}
    # k = 5
    for th in ROOTS[5]:
        s = tmask(adj, th, 5)
        if s not in TYPES5:
            continue
        out['theta_hits'][('5', s)] += 1
        u, v = [x for x in V if x not in th]
        fu = tmask(adj, th + (u,), 6)
        fv = tmask(adj, th + (v,), 6)
        c = out['b5'].setdefault(s, Counter())
        c[(fu, fv)] += 1
        c[(fv, fu)] += 1
    # k = 3
    for th in ROOTS[3]:
        s = tmask(adj, th, 3)
        rest = [x for x in V if x not in th]
        if s in TYPES3:
            out['theta_hits'][('3', s)] += 1
            c = out['b3'].setdefault(s, Counter())
            for A in itertools.combinations(rest, 2):
                B = tuple(x for x in rest if x not in A)
                c[(canon_ext(adj, th, A), canon_ext(adj, th, B))] += 1
        if s == 7:  # labelled triangle tau
            Dflag = {x: int(adj[x][th[0]] + adj[x][th[1]] + adj[x][th[2]] >= 2) for x in rest}
            single = {x: tmask(adj, th + (x,), 4) for x in rest}
            for a, b, cc in itertools.permutations(rest, 3):
                out['t0all'][(single[a], single[b])] += 1
                if Dflag[cc]:
                    out['t0D'][(single[a], single[b])] += 1
            for cc in rest:
                A = tuple(x for x in rest if x != cc)
                F = canon_ext(adj, th, A)
                out['t6all'][F] += 1
                if Dflag[cc]:
                    out['t6D'][F] += 1
    # k = 1
    for th in ROOTS[1]:
        rest = [x for x in V if x not in th]
        for A in itertools.combinations(rest, 3):
            B = tuple(x for x in rest if x not in A)
            out['b1'][(canon_ext(adj, th, A), canon_ext(adj, th, B))] += 1
    # k = 4, Bollobas type K4 minus edge 01 (mask 62), sector = common neighbours of roots 0,1
    for th in ROOTS[4]:
        if tmask(adj, th, 4) != 62:
            continue
        out['theta_hits'][('4', 62)] += 1
        a, b, c = [x for x in V if x not in th]
        X = {x: adj[x][th[0]] & adj[x][th[1]] for x in (a, b, c)}
        x3 = X[a] * X[b] * X[c]
        xe = (X[a] * X[b] * X[c] * adj[b][c] + X[b] * X[a] * X[c] * adj[a][c] + X[c] * X[a] * X[b] * adj[a][b])
        ne = adj[a][b] + adj[a][c] + adj[b][c]
        T = x3 * (ne == 3)
        P3 = x3 * (ne == 2)
        out['bol3'] += 3 * x3 - 11 * xe + 90 * T + 45 * P3
    out['b5'] = {s: dict(c) for s, c in out['b5'].items()}
    out['b3'] = {s: dict(c) for s, c in out['b3'].items()}
    for k in ('b1', 't0all', 't0D', 't6all', 't6D', 'theta_hits'):
        out[k] = dict(out[k])
    return out


def init(t5, t3):
    global TYPES5, TYPES3
    TYPES5, TYPES3 = t5, t3


def main():
    t0 = time.time()
    model = load_model()
    t5 = {b['type'][1] for b in model['matrix_blocks'] if b['type'][0] == 5}
    t3 = {b['type'][1] for b in model['matrix_blocks'] if b['type'][0] == 3 and b['flag_order'] == 5}
    basis = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basis.json')))
    init(t5, t3)
    with Pool(6, initializer=init, initargs=(t5, t3)) as pool:
        res = pool.map(count_one, [(r['rep'],) for r in basis], chunksize=8)
    pickle.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'counts.pkl'), 'wb'))
    # internal consistency: totals of each count family
    for H, r in zip(basis, res):
        assert sum(r['b1'].values()) == 7 * 20
        assert sum(r['t0all'].values()) * 4 == sum(r['t6all'].values()) * 24
        assert sum(r['t6all'].values()) == 4 * r['theta_hits'].get(('3', 7), 0)
    print(f'counted {len(res)} graphs, types5={len(t5)}, types3={sorted(t3)}, {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
