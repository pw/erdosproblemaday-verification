#!/usr/bin/env python3
"""#789 upper bounds on h(n) by exact search over a window: find the LARGEST A ⊆ [-N, N] (0 and negatives allowed)
with NO admissible k-subset. h(n) = min over n-sets of H(A) and is non-decreasing in n, so an m-set with no admissible
k-subset proves h(n) ≤ k-1 for every n ≤ m. Pure SAT: y_v per integer v in [-N,N]; one clause per ADMISSIBLE k-subset
of the window (not all chosen); cardinality ≥ m (totalizer); m increases until UNSAT. Admissibility = hcheck.admissible,
the literal page definition (all nonempty S,T ⊆ B, equal sums ⇒ equal sizes). Every witness is re-checked exhaustively:
H(A) ≤ k-1 by testing all C(|A|,k) subsets with hcheck.admissible. UNSAT at m says only "no m-set inside this window"."""
import sys, itertools, time
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195
from hcheck import admissible

def fast_admissible(B):
    seen = {}
    for r in range(1, len(B) + 1):
        for S in itertools.combinations(B, r):
            s = sum(S)
            if s in seen:
                if seen[s] != r: return False
            else: seen[s] = r
    return True

def search(N, k, m_start):
    vals = list(range(-N, N + 1)); var = {v: i + 1 for i, v in enumerate(vals)}
    t0 = time.time(); clauses = []; nsub = 0
    for A in itertools.combinations(vals, k):
        nsub += 1
        if fast_admissible(A): clauses.append([-var[v] for v in A])
    tc = time.time() - t0
    print(f"window [-{N},{N}] ({len(vals)} ints): admissible {k}-subsets {len(clauses)}/{nsub} classified in {tc:.0f}s", flush=True)
    best = None; m = m_start
    while m <= len(vals):
        cnf = CNF(from_clauses=clauses)
        cnf.extend(CardEnc.atleast(lits=list(var.values()), bound=m, top_id=len(vals), encoding=EncType.totalizer).clauses)
        t1 = time.time()
        with Cadical195(bootstrap_with=cnf.clauses) as s:
            r = s.solve(); model = set(s.get_model()) if r else None
        if not r:
            print(f"  m={m}: UNSAT in window ({time.time()-t1:.1f}s)", flush=True); break
        A = [v for v in vals if var[v] in model]
        best = A; print(f"  m={m}: SAT |A|={len(A)} A={A} ({time.time()-t1:.1f}s)", flush=True)
        m = len(A) + 1
    if best is not None:
        t2 = time.time(); bad = all(not admissible(S) for S in itertools.combinations(best, k))
        print(f"RESULT N={N} k={k} max|A|={len(best)} A={best} every_{k}_subset_inadmissible={bad} (exhaustive recheck {time.time()-t2:.0f}s)"
              f" => h(n) <= {k-1} for all n <= {len(best)}" if bad else "RECHECK FAILED", flush=True)
    return best

if __name__ == "__main__":
    N, k = int(sys.argv[1]), int(sys.argv[2]); m0 = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    search(N, k, m0)
