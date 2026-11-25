"""Independent checker for M(A)=alpha(G_A), G_A: edge {u,v}, u!=v, u+v in A.
Two independent exact methods: OR-tools CP-SAT maximization, and pysat (cadical)
decision 'exists independent set of size t' with seqcounter cardinality."""
import sys, itertools
from ortools.sat.python import cp_model
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def graph(A):
    A = sorted(set(A)); S = set(A); idx = {a:i for i,a in enumerate(A)}
    E = [(i,j) for i in range(len(A)) for j in range(i+1,len(A)) if A[i]+A[j] in S]
    return A, E

def alpha_cpsat(A, timeout=600):
    A, E = graph(A)
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(len(A))]
    for i,j in E: m.AddBoolOr([x[i].Not(), x[j].Not()])
    m.Maximize(sum(x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = timeout; s.parameters.num_workers = 8
    r = s.Solve(m)
    if r != cp_model.OPTIMAL: return None, None
    B = [A[i] for i in range(len(A)) if s.Value(x[i])]
    return int(s.ObjectiveValue()), B

def has_indep(A, t):
    A, E = graph(A); n = len(A)
    if t > n: return False, None
    cnf = CardEnc.atleast(lits=list(range(1,n+1)), bound=t, top_id=n, encoding=EncType.seqcounter)
    with Solver(name='cadical153', bootstrap_with=cnf.clauses) as s:
        for i,j in E: s.add_clause([-(i+1), -(j+1)])
        ok = s.solve()
        B = [A[i] for i in range(n) if s.get_model()[i] > 0] if ok else None
    return ok, B

def check_indep(A, B):
    S = set(A)
    for b1, b2 in itertools.combinations(B, 2):
        if b1 + b2 in S: return False
    return set(B) <= S

def alpha_sat(A):
    # find alpha by decision: increasing t
    t = 1
    best = None
    while True:
        ok, B = has_indep(A, t)
        if not ok: return t-1, best
        assert check_indep(A, B); best = B; t = len(B)+1 if len(B) >= t else t+1
