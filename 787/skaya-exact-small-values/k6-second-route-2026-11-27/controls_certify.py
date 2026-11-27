"""Controls for check_certs.certify (our checker).
Positive: two hand-derived certificates.  Negative, GUARANTEED-to-fail mutations: for a sample of archive
certificates, drop one term and PROVE the remaining equalities are realisable by an exact rational point
(0 < x_0 < ... < x_21, every remaining x_i + x_j = x_l holds exactly): then no certificate of any weights
exists, so the checker must reject.  Also: zero weights, out-of-range / degenerate triples, single-weight
sign flips and +1 perturbations (these are not guaranteed to fail; acceptances are counted and re-proved)."""
import sys, gzip, json, random
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/787/check')
from check_certs import certify, M

def exact_point(m, T):
    """Exact rational point with x_0 >= 1, x_{t+1}-x_t >= 1 and all equalities of T, or None.
    LP (HiGHS) gives a vertex; we re-solve its tight constraints exactly with Fractions and verify."""
    A_eq = np.array([[(1 if c in (i, j) else -1 if c == l else 0) for c in range(m)] for (i, j, l) in T]) if T else None
    A_ub = np.zeros((m, m)); b_ub = -np.ones(m)
    A_ub[0, 0] = -1
    for t in range(m - 1): A_ub[t + 1, t] = 1; A_ub[t + 1, t + 1] = -1
    res = linprog(np.arange(1, m + 1), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=(np.zeros(len(T)) if T else None),
                  bounds=(None, None), method='highs')
    if res.status != 0: return None
    x = res.x
    rows = [[Fraction(v) for v in r] + [Fraction(0)] for r in (A_eq if T else [])]
    slack = A_ub @ x - b_ub
    for t in range(m):
        if abs(slack[t]) < 1e-7: rows.append([Fraction(-int(v)) for v in A_ub[t]] + [Fraction(1)])  # -A_ub x = 1 when tight
    # Gaussian elimination (exact)
    R = [r[:] for r in rows]; piv = []; r0 = 0
    for c in range(m):
        p = next((r for r in range(r0, len(R)) if R[r][c] != 0), None)
        if p is None: continue
        R[r0], R[p] = R[p], R[r0]
        inv = 1 / R[r0][c]; R[r0] = [v * inv for v in R[r0]]
        for r in range(len(R)):
            if r != r0 and R[r][c] != 0:
                f = R[r][c]; R[r] = [a - f * b for a, b in zip(R[r], R[r0])]
        piv.append(c); r0 += 1
    if len(piv) < m: return None
    if any(all(v == 0 for v in r[:m]) and r[m] != 0 for r in R): return None
    xs = [None] * m
    for r in range(len(piv)): xs[piv[r]] = R[r][m]
    ok = xs[0] > 0 and all(xs[t] < xs[t + 1] for t in range(m - 1)) and all(xs[i] + xs[j] == xs[l] for (i, j, l) in T)
    return xs if ok else None

def main():
    path = sys.argv[1]; nsamp = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    fails = 0
    # positive controls (hand-derived; see report)
    pc1 = ([(0, 1, 2), (0, 1, 3)], [1, -1])                          # x2 = x0+x1 = x3
    pc2 = ([(0, 1, 2), (0, 3, 4), (0, 4, 5), (2, 3, 5)], [1, -1, -1, 1])  # forces x1 = x0
    for T, y in (pc1, pc2):
        s = certify(M, T, y); print('positive control', T, y, '->', s); fails += (s == 0)
        s2 = certify(M, T, [-w for w in y]); print('  all signs flipped (still valid, other convention) ->', s2); fails += (s2 == 0)
    # structural negatives
    for T, y, why in [(pc2[0], [0, 0, 0, 0], 'all-zero weights'), ([(0, 1, 22)], [1], 'l = m out of range'),
                      ([(1, 1, 2), (0, 1, 2)], [1, -1], 'i = j'), ([(2, 1, 3)], [1], 'i > j'), ([], [], 'empty'),
                      ([(0, 1, 2)], [1], 'single realisable equality'), (pc2[0], [1, -1, -1], 'length mismatch')]:
        s = certify(M, T, y); print('negative control', why, '->', s); fails += (s != 0)
    # realisable configuration: every true sum relation of {1..22} (x_i = i+1) must admit no certificate
    T = [(i, j, l) for i in range(M) for j in range(i + 1, M) for l in range(j + 1, M) if (i + 1) + (j + 1) == l + 1]
    rng = random.Random(1126); acc = 0
    for _ in range(20000):
        sub = rng.sample(T, rng.randint(1, min(25, len(T)))); y = [rng.randint(-3, 3) for _ in sub]
        acc += certify(M, sub, y) != 0
    print(f'realisable {{1..22}}: {len(T)} true equalities, 20000 random (subset, weights) -> accepted {acc} (must be 0)'); fails += acc
    # sample archive certs
    recs = []
    with gzip.open(path, 'rt') as f:
        for ln, line in enumerate(f):
            recs.append(line)
    sample = [json.loads(recs[i]) for i in rng.sample(range(len(recs)), nsamp)]
    del recs
    drop_tested = drop_proved_feasible = drop_rejected = drop_not_minimal = 0
    flip_rej = flip_acc = plus_rej = plus_acc = 0
    for rec in sample:
        T = [tuple(t) for t in rec['triples']]; y = rec['weights']
        assert certify(M, T, y) != 0
        r = rng.randrange(len(T))
        T2 = T[:r] + T[r + 1:]; y2 = y[:r] + y[r + 1:]
        drop_tested += 1
        s = certify(M, T2, y2) if T2 else 0
        if s == 0: drop_rejected += 1
        pt = exact_point(M, T2)
        if pt is not None:
            drop_proved_feasible += 1
            if s != 0: print('CHECKER ERROR: accepted a certificate for a realisable system', T2, y2, pt); fails += 1
        else:
            drop_not_minimal += 1
        yf = y[:]; yf[r] = -yf[r]
        if certify(M, T, yf) == 0: flip_rej += 1
        else: flip_acc += 1
        yp = y[:]; yp[r] += 1
        if certify(M, T, yp) == 0: plus_rej += 1
        else: plus_acc += 1
    print(f'drop-one-term on {drop_tested} archive certs: rejected {drop_rejected}; remaining system PROVED realisable by an exact '
          f'rational point in {drop_proved_feasible} (checker must reject all of these: errors counted above); no exact point found in {drop_not_minimal}')
    print(f'flip sign of one weight: rejected {flip_rej}, accepted {flip_acc};  +1 on one weight: rejected {plus_rej}, accepted {plus_acc}')
    print('CONTROLS', 'PASS' if fails == 0 else f'FAIL ({fails})')
    sys.exit(0 if fails == 0 else 1)

if __name__ == '__main__':
    main()
