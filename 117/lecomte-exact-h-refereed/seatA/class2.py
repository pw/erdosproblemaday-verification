"""Seat A: class-2 p-groups from alternating maps beta: V x V -> W = F_p^e (radical 0), beyond the SmallGroups range.
For odd p the group V x W with (v,w)(v',w') = (v+v', w+w'+beta(v,v')/2) has G/Z = V and commutator beta, so
omega and a depend only on beta.  Work projectively (one vertex per line of V).
  omega = max set of points pairwise beta != 0;  a = min cover by maximal totally-isotropic subspaces.
Checks: a <= T(omega), strict when omega >= 9 (paper, Thm 1.1 / Prop 4.1), and for the anisotropic-pencil case
(dim V = 4, e = 2, every nonzero scalarization nondegenerate) the printed claims a <= p^2+1 and omega >= p^2+1.
"""
import itertools, random, sys, collections
import networkx as nx
from ortools.sat.python import cp_model
sys.path.insert(0, "/home/exedev/MathDyad/subs-1116/117/seatA")
from analyze import T

def rank_mod(M, p):
    A = [r[:] for r in M]; n = len(A); m = len(A[0]); rk = 0
    for col in range(m):
        piv = next((i for i in range(rk, n) if A[i][col] % p), None)
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        iv = pow(A[rk][col], p - 2, p)
        A[rk] = [(v * iv) % p for v in A[rk]]
        for i in range(n):
            if i != rk and A[i][col] % p:
                f = A[i][col]; A[i] = [(a - f * b) % p for a, b in zip(A[i], A[rk])]
        rk += 1
    return rk

def rand_alt(p, n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            a = random.randrange(p); M[i][j] = a; M[j][i] = (-a) % p
    return M

def points(p, n):
    return [v for v in itertools.product(range(p), repeat=n) if any(v) and next(x for x in v if x) == 1]

def solve(p, n, mats, limit=600):
    pts = points(p, n)
    def bvals(u, v):
        return tuple(sum(u[i] * M[i][j] * v[j] for i in range(n) for j in range(n)) % p for M in mats)
    G = nx.Graph(); G.add_nodes_from(range(len(pts)))
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if not any(bvals(pts[i], pts[j])):
                G.add_edge(i, j)
    cl = list(nx.find_cliques(G))
    m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in pts]
    for c in cl:
        if len(c) >= 2: m.Add(sum(x[v] for v in c) <= 1)
    m.Maximize(sum(x)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = limit; s.parameters.num_workers = 8
    st = s.Solve(m); om = int(round(s.ObjectiveValue())); omb = int(round(s.BestObjectiveBound()))
    m2 = cp_model.CpModel(); y = [m2.NewBoolVar("") for _ in cl]
    inc = collections.defaultdict(list)
    for k, c in enumerate(cl):
        for v in c: inc[v].append(k)
    for v in range(len(pts)): m2.AddBoolOr([y[k] for k in inc[v]])
    m2.Minimize(sum(y)); s2 = cp_model.CpSolver(); s2.parameters.max_time_in_seconds = limit; s2.parameters.num_workers = 8
    st2 = s2.Solve(m2); a = int(round(s2.ObjectiveValue())); ab = int(round(s2.BestObjectiveBound()))
    return om, omb, a, ab, st == cp_model.OPTIMAL and st2 == cp_model.OPTIMAL

def all_scalarizations_nondeg(p, n, mats):
    e = len(mats)
    for lam in itertools.product(range(p), repeat=e):
        if not any(lam): continue
        M = [[sum(l * Mk[i][j] for l, Mk in zip(lam, mats)) % p for j in range(n)] for i in range(n)]
        if rank_mod(M, p) < n: return False
    return True

def sample(p, n, e, want_aniso=None, tries=20000):
    for _ in range(tries):
        mats = [rand_alt(p, n) for _ in range(e)]
        # independence of the e forms
        flat = [[M[i][j] for i in range(n) for j in range(i + 1, n)] for M in mats]
        if rank_mod(flat, p) < e: continue
        # radical zero
        stacked = [row for M in mats for row in M]
        # radical = common kernel: v with M v = 0 for all M  <=> rank of stacked (en x n) == n
        if rank_mod(stacked, p) < n: continue
        if want_aniso is not None and all_scalarizations_nondeg(p, n, mats) != want_aniso: continue
        return mats
    return None

if __name__ == "__main__":
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 117)
    configs = [  # (p, n, e, want_aniso, count)
        (3, 4, 1, None, 2), (3, 4, 2, True, 8), (3, 4, 2, False, 6), (3, 4, 3, None, 6), (3, 4, 4, None, 3),
        (5, 4, 2, True, 3), (5, 4, 2, False, 2), (5, 4, 3, None, 2),
        (3, 5, 2, None, 4), (3, 5, 3, None, 4),
        (3, 6, 2, None, 2), (3, 6, 3, None, 2), (3, 6, 4, None, 2),
        (7, 4, 2, True, 1),
        (2, 6, 2, None, 4), (2, 6, 3, None, 4), (2, 8, 2, None, 2), (2, 8, 3, None, 2),
    ]
    viol = []; done = 0
    for p, n, e, an, cnt in configs:
        for _ in range(cnt):
            mats = sample(p, n, e, an)
            if mats is None:
                print(f"p={p} n={n} e={e} aniso={an}: no sample"); break
            om, omb, a, ab, opt = solve(p, n, mats)
            aniso = all_scalarizations_nondeg(p, n, mats) if n == 4 else None
            flag = ""
            if a > T(om) or (om >= 9 and a >= T(om)): flag = "VIOLATION"; viol.append((p, n, e, om, a))
            if aniso and (a > p * p + 1 or om < p * p + 1): flag += " ANISO-CLAIM-FAILS"; viol.append(("aniso", p, om, a))
            if not opt: flag += f" (nonoptimal: omega in [{om},{omb}], a in [{ab},{a}])"
            print(f"p={p} dimV={n} e={e} aniso={aniso}: omega={om} a={a} T(omega)={T(om)} {flag}", flush=True)
            done += 1
    print("instances", done, "violations", viol)
