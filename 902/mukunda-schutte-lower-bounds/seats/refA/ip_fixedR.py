"""Local model of Theorem 7.1 with T[R] FIXED: integer program in the multiplicities n_S
(S subset R, |S|>=5; n_S = #{y in O : Q_y = S}).  For each sampled 5-regular tournament T[R]
on 11 vertices: is there a family with all j_r >= 0, J <= Jmax, every triple of R >= 5 dominators?
Paper: impossible for Jmax = 2.  Positive control: Jmax = 8 / smallest feasible J reported.
T[R] samples: the circulant(s) + random walks by reversing directed 3-cycles (preserves scores).
Usage: ip_fixedR.py n_samples Jmax time_limit_per_ip seed
"""
import sys, itertools, random, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

nsamp = int(sys.argv[1]); Jmax = int(sys.argv[2]); tl = float(sys.argv[3]); seed = int(sys.argv[4])
n = 11
subsets = [S for k in range(5, n + 1) for S in itertools.combinations(range(n), k)]
triples = list(itertools.combinations(range(n), 3))
inS = np.array([[1 if r in S else 0 for r in range(n)] for S in subsets])
disj = np.array([[1 if not (set(S) & set(U)) else 0 for S in subsets] for U in triples])


def solve(A):
    dom = np.array([sum(1 for w in range(n) if w not in U and all(A[w, u] for u in U)) for U in triples])
    rows, lb, ub = [], [], []
    rows.append(np.ones(len(subsets))); lb.append(38); ub.append(38)
    for r in range(n):
        rows.append(1 - inS[:, r]); lb.append(20); ub.append(np.inf)
    rows.append((1 - inS).sum(1)); lb.append(-np.inf); ub.append(220 + Jmax)
    for t in range(len(triples)):
        rows.append(disj[t]); lb.append(5 - dom[t]); ub.append(np.inf)
    res = milp(np.zeros(len(subsets)), constraints=LinearConstraint(np.array(rows), lb, ub),
               integrality=np.ones(len(subsets)), bounds=Bounds(0, 38), options={'time_limit': tl})
    return res


def circulant(conn):
    A = np.zeros((n, n), int)
    for i in range(n):
        for d in conn:
            A[i, (i + d) % n] = 1
    return A


def walk(A, steps, rng):
    A = A.copy()
    for _ in range(steps):
        while True:
            a, b, c = rng.sample(range(n), 3)
            if A[a, b] and A[b, c] and A[c, a]:
                A[a, b] = A[b, c] = A[c, a] = 0
                A[b, a] = A[c, b] = A[a, c] = 1
                break
    return A


rng = random.Random(seed)
samples = [circulant([1, 2, 3, 4, 5]), circulant([1, 3, 4, 5, 9]), circulant([1, 2, 4, 5, 8])]
for c in samples:
    assert all(c[i].sum() == 5 for i in range(n)) and np.all(c + c.T + np.eye(n, dtype=int) == 1)
base = samples[0]
while len(samples) < nsamp:
    samples.append(walk(base, 200, rng))
tally = {}
t0 = time.time()
for k, A in enumerate(samples):
    res = solve(A)
    tally[res.status] = tally.get(res.status, 0) + 1
    if res.status == 0:
        x = np.round(res.x).astype(int)
        j = [int(sum(x[i] for i, S in enumerate(subsets) if r not in S)) - 20 for r in range(n)]
        # re-verify from scratch
        dom = [sum(1 for w in range(n) if w not in U and all(A[w, u] for u in U)) +
               sum(x[i] for i, S in enumerate(subsets) if not set(S) & set(U)) for U in triples]
        print(f"sample {k}: FEASIBLE j={j} J={sum(j)} min triple dominators={min(dom)} sum n={x.sum()}", flush=True)
    elif k < 5 or res.status != 2:
        print(f"sample {k}: status {res.status} {res.message}", flush=True)
print(f"Jmax={Jmax}: samples={len(samples)} status tally (0=feasible,2=infeasible,1=timeout) {tally} in {time.time()-t0:.0f}s")
