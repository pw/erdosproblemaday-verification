"""Independent machine check of Theorem 7.1 in the LOCAL model that its proof uses.
Unknowns: a 5-regular tournament on R (11 vertices) and the multiset of 38 sets
Q_y subset R (|Q_y| >= 5), y in O.  j_r := #{y: r notin Q_y} - 20.
Hypotheses (exactly those used in the proof of Theorem 7.1):
  j_r >= 0 (Lemma 6.1);  every triple U subset R has >= 5 dominators, where by (6)
  |D(U)| = #{w in R\\U: w beats U} + #{y in O : Q_y cap U = empty}.
Question: can J = sum_r j_r be <= Jmax?  The paper claims impossible for Jmax = 2.
Encoding: multiplicities n_S (S subset R, |S|>=5); arc binaries; z_{w,U} <= [w beats U].
The feasible set contains every real configuration, so INFEASIBLE => theorem (local form).
"""
import sys, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

jvec = [int(t) for t in sys.argv[1].split(',')] + [0] * 11
jvec = jvec[:11]
Jmax = sum(jvec)
tl = float(sys.argv[2]) if len(sys.argv) > 2 else 1800
n = 11
pairs = list(itertools.combinations(range(n), 2))
pidx = {p: i for i, p in enumerate(pairs)}
subsets = [S for k in range(5, n + 1) for S in itertools.combinations(range(n), k)]
triples = list(itertools.combinations(range(n), 3))
nx = len(pairs)
nS = len(subsets)
zlist = [(w, U) for U in triples for w in range(n) if w not in U]
nz = len(zlist)
NV = nx + nS + nz
ox, oS, oz = 0, nx, nx + nS
rows = []  # (coeff dict, lb, ub)


def beats(w, u):
    # returns (const, coeff, varindex): indicator w->u = const + coeff*x
    if w < u:
        return 0, 1, ox + pidx[(w, u)]
    return 1, -1, ox + pidx[(u, w)]


# regularity: out-degree 5
for u in range(n):
    c = {}
    const = 0
    for v in range(n):
        if v == u:
            continue
        k0, k1, vi = beats(u, v)
        const += k0
        c[vi] = c.get(vi, 0) + k1
    rows.append((c, 5 - const, 5 - const))
# sum n_S = 38
rows.append(({oS + i: 1 for i in range(nS)}, 38, 38))
# j_r >= 0 ; J <= Jmax
Jrow = {}
for r in range(n):
    c = {oS + i: 1 for i, S in enumerate(subsets) if r not in S}
    rows.append((c, 20 + jvec[r], 20 + jvec[r]))
    for k, v in c.items():
        Jrow[k] = Jrow.get(k, 0) + v
rows.append((Jrow, -np.inf, 220 + Jmax))
# z_{w,U} <= [w beats u] for u in U
for zi, (w, U) in enumerate(zlist):
    for u in U:
        k0, k1, vi = beats(w, u)
        # z - k1*x <= k0
        rows.append(({oz + zi: 1, vi: -k1}, -np.inf, k0))
# triple constraint
zby = {}
for zi, (w, U) in enumerate(zlist):
    zby.setdefault(U, []).append(zi)
for U in triples:
    c = {oz + zi: 1 for zi in zby[U]}
    for i, S in enumerate(subsets):
        if not (set(S) & set(U)):
            c[oS + i] = c.get(oS + i, 0) + 1
    rows.append((c, 5, np.inf))
M = lil_matrix((len(rows), NV))
lb = np.zeros(len(rows)); ub = np.zeros(len(rows))
for i, (c, l, u) in enumerate(rows):
    for k, v in c.items():
        M[i, k] = v
    lb[i] = l; ub[i] = u
integrality = np.ones(NV)
bounds = Bounds(np.zeros(NV), np.concatenate([np.ones(nx), 38 * np.ones(nS), np.ones(nz)]))
print(f"j-vector={jvec} J={Jmax}: vars={NV} (arcs {nx}, sets {nS}, z {nz}), rows={len(rows)}", flush=True)
t0 = time.time()
res = milp(c=np.zeros(NV), constraints=LinearConstraint(M.tocsr(), lb, ub), integrality=integrality,
           bounds=bounds, options={'time_limit': tl, 'disp': False})
print(f"status={res.status} ({res.message}) in {time.time()-t0:.1f}s", flush=True)
if res.status == 0:
    x = np.round(res.x).astype(int)
    nsv = x[oS:oS + nS]
    Q = [(subsets[i], nsv[i]) for i in range(nS) if nsv[i]]
    j = [sum(m for S, m in Q if r not in S) - 20 for r in range(n)]
    print("FEASIBLE witness: j =", j, "J =", sum(j))
    print("Q multiset sizes:", sorted([len(S) for S, m in Q for _ in range(m)]))
    # re-verify witness from scratch
    A = np.zeros((n, n), int)
    for (u, v), i in pidx.items():
        if x[ox + i]: A[u, v] = 1
        else: A[v, u] = 1
    ok = all(A[u].sum() == 5 for u in range(n))
    mind = min(sum(1 for w in range(n) if w not in U and all(A[w, u] for u in U)) +
               sum(m for S, m in Q if not set(S) & set(U)) for U in triples)
    print("witness re-check: regular", ok, "min triple dominators", mind)
