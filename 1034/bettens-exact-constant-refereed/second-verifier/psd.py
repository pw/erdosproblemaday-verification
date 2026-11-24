"""Step 3: exact PSD of all 82 certificate matrices over Q(sqrt3) by symmetric Gaussian elimination with
LARGEST-DIAGONAL pivoting (sign comparisons decided exactly), plus exact signs of all multipliers and slacks,
plus planted controls.

PSD test (sound and complete for symmetric matrices):
  repeat on the remaining index set S:
    d = max_{i in S} A[i][i]  (exact comparison in the real embedding)
    if d > 0: pivot on it, A <- Schur complement A_SS - a a^T / d   (PSD iff Schur complement PSD)
    if d < 0: NOT PSD
    if d == 0: all remaining diagonals are <= 0; PSD iff the whole remaining submatrix is exactly zero
"""
import os
import json
import sys
import time
from fractions import Fraction
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import kparse, kadd, ksub, kmul, kinv, ksign, kiszero, kfloat, load_cert, load_model

T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)


def psd_exact(M):
    """M: list of lists of (Fraction, Fraction). Returns (is_psd, info)."""
    n = len(M)
    A = [row[:] for row in M]
    for i in range(n):
        for j in range(i):
            if A[i][j] != A[j][i]:
                return False, f'not symmetric at ({i},{j})'
    S = list(range(n))
    rank = 0
    pivots = []
    while S:
        best = S[0]
        for i in S[1:]:
            if ksign(ksub(A[i][i], A[best][best])) > 0:
                best = i
        d = A[best][best]
        sd = ksign(d)
        if sd < 0:
            return False, f'negative largest diagonal {kfloat(d):.3e} at index {best} after {rank} pivots'
        if sd == 0:
            for i in S:
                for j in S:
                    if not kiszero(A[i][j]):
                        return False, (f'zero pivot with nonzero entry at ({i},{j}) = {kfloat(A[i][j]):.3e} '
                                       f'after {rank} pivots')
            return True, {'rank': rank, 'n': n, 'kernel': len(S), 'min_pivot': min(pivots) if pivots else None}
        rank += 1
        pivots.append(kfloat(d))
        S.remove(best)
        di = kinv(d)
        col = {i: kmul(A[i][best], di) for i in S}  # a_i / d
        for ii, i in enumerate(S):
            ci = col[i]
            if kiszero(ci):
                continue
            ai = A[best][i]
            for j in S[ii:]:
                # A_ij -= a_i a_j / d   (keep exact symmetry by writing both triangles)
                v = ksub(A[i][j], kmul(ci, A[best][j]))
                A[i][j] = v
                A[j][i] = v
    return True, {'rank': rank, 'n': n, 'kernel': 0, 'min_pivot': min(pivots) if pivots else None}


def job(args):
    bi, M = args
    t = time.time()
    Mk = [[kparse(x) for x in r] for r in M]
    ok, info = psd_exact(Mk)
    return bi, ok, info, time.time() - t


def main():
    cert = load_cert()
    model = load_model()
    mats = cert['matrices']
    assert len(mats) == 82 == len(model['matrix_blocks'])
    with Pool(6) as pool:
        res = pool.map(job, list(enumerate(mats)), chunksize=1)
    allok = True
    singular = []
    for bi, ok, info, dt in sorted(res):
        allok &= ok
        if ok and info['kernel']:
            singular.append((bi, info['n'], info['kernel']))
        if not ok or bi in (0, 5, 7) or dt > 5:
            log(f'block {bi}: PSD={ok} {info} ({dt:.1f}s)')
    log(f'PSD: {sum(1 for r in res if r[1])}/82 matrices PSD; singular blocks (index, size, exact kernel dim): {singular}')
    log(f'min positive pivot over all blocks: {min(r[2]["min_pivot"] for r in res if r[1] and r[2]["min_pivot"]):.3e}')

    # signs
    lam = [kparse(x) for x in cert['scalar_multipliers']]
    sl = [kparse(x) for x in cert['graph_slacks']]
    neg_l = [j for j in range(817) if ksign(lam[j]) < 0]
    neg_s = [h for h in range(1044) if ksign(sl[h]) < 0]
    mixed_s = sum(1 for x in sl if ksign((x[0], 0)) * ksign((x[1], 0)) < 0)
    log(f'signs: lambda_0..815 + beta negative: {neg_l}; zero lambdas: {sum(kiszero(x) for x in lam[:816])}; '
        f'beta sign {ksign(lam[816])} ({kfloat(lam[816]):.6g})')
    log(f'signs: negative slacks: {neg_s}; zero slacks: {sum(kiszero(x) for x in sl)}; '
        f'slacks whose a and b parts have opposite signs (decided by squaring): {mixed_s}; '
        f'min positive slack {min(kfloat(x) for x in sl if ksign(x) > 0):.3e}')
    print('PSD+SIGNS OK' if allok and not neg_l and not neg_s else 'PSD+SIGNS FAILED')

    # ---------------- controls
    F = Fraction
    k = lambda a, b=0: (F(a), F(b))
    log('--- PSD/sign controls ---')
    ctrl = []
    ctrl.append(('indefinite [[1,2],[2,1]]', [[k(1), k(2)], [k(2), k(1)]], False))
    ctrl.append(('zero pivot, nonzero column [[1,0,0],[0,0,1],[0,1,0]]',
                 [[k(1), k(0), k(0)], [k(0), k(0), k(1)], [k(0), k(1), k(0)]], False))
    ctrl.append(('zero diagonal, nonzero column [[0,1],[1,5]]', [[k(0), k(1)], [k(1), k(5)]], False))
    ctrl.append(('singular PSD [[2,1,0],[1,1/2,0],[0,0,0]]', [[k(2), k(1), k(0)], [k(1), k(F(1, 2)), k(0)],
                                                              [k(0), k(0), k(0)]], True))
    ctrl.append(('sqrt3 entries PSD [[2, sqrt3],[sqrt3, 3/2]] (det 0)', [[k(2), k(0, 1)], [k(0, 1), k(F(3, 2))]], True))
    ctrl.append(('sqrt3 entries indefinite [[2, sqrt3],[sqrt3, 3/2 - 1e-40]]',
                 [[k(2), k(0, 1)], [k(0, 1), k(F(3, 2) - F(1, 10 ** 40))]], False))
    for bi in (5, 12, 7):
        M = [[kparse(x) for x in r] for r in mats[bi]]
        n = len(M)
        Mm = [[(M[i][j][0] - (F(1, 10 ** 30) if i == j else 0), M[i][j][1]) for j in range(n)] for i in range(n)]
        ctrl.append((f'real singular block {bi} minus 1e-30*I', Mm, False))
    M = [[kparse(x) for x in r] for r in mats[3]]
    ctrl.append(('real block 3 with off-diagonal pushed past det=0', [[M[0][0], kadd(M[0][1], k(10))],
                                                                     [kadd(M[1][0], k(10)), M[1][1]]], False))
    for label, M, expect in ctrl:
        ok, info = psd_exact(M)
        log(f'control {label}: PSD={ok} (expected {expect}) -> {"PASS" if ok == expect else "CONTROL FAILED"}; {info}')
        assert ok == expect
    # sign controls: values straddling zero by 1e-15 relative
    s_neg = (F(1732050807568877, 10 ** 15), F(-1))  # 1.732050807568877 - sqrt3 < 0
    s_pos = (F(1732050807568878, 10 ** 15), F(-1))  # > 0
    log(f'sign control 1.732050807568877 - sqrt3: sign {ksign(s_neg)} (expect -1); '
        f'1.732050807568878 - sqrt3: sign {ksign(s_pos)} (expect +1)')
    assert ksign(s_neg) == -1 and ksign(s_pos) == 1
    hneg = next(h for h in range(1044) if ksign(sl[h]) > 0)
    sl2 = list(sl)
    sl2[hneg] = (-sl[hneg][0], -sl[hneg][1])
    bad = [h for h in range(1044) if ksign(sl2[h]) < 0]
    log(f'sign control: negate slack[{hneg}] -> negative slacks found {bad} (expect [{hneg}])')
    assert bad == [hneg]
    log('controls done')


if __name__ == '__main__':
    main()
