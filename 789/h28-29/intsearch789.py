#!/usr/bin/env python3
"""Integer witness search for the #789 lemma (m,k): is there an m-subset of {1..N} with NO admissible k-subset?
Pure SAT: y_v = "v is chosen"; for every ADMISSIBLE k-subset A of {1..N} add the clause (not all of A chosen);
cardinality: at least m chosen (pysat totalizer). SAT => an explicit integer m-set every k-subset of which is bad
(re-checked from the definition) = the real-arithmetic lemma is FALSE for (m,k). UNSAT at N only says no witness
inside {1..N} (coverage, not a proof of the lemma). Admissibility per lemma789.is_admissible."""
import sys, itertools, time
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195
from lemma789 import is_admissible

def search(N, m, k):
    t0 = time.time()
    cnf = CNF(); nadm = 0; nsub = 0
    for A in itertools.combinations(range(1, N + 1), k):
        nsub += 1
        if is_admissible(A):
            nadm += 1; cnf.append([-v for v in A])
    card = CardEnc.atleast(lits=list(range(1, N + 1)), bound=m, top_id=N, encoding=EncType.totalizer)
    cnf.extend(card.clauses)
    with Cadical195(bootstrap_with=cnf.clauses) as s:
        r = s.solve(); model = s.get_model() if r else None
    secs = time.time() - t0
    if r:
        chosen = [v for v in range(1, N + 1) if v in set(model)]
        ok = len(chosen) >= m and all(not is_admissible(K) for K in itertools.combinations(chosen, k))
        print(f"INTSEARCH N={N} m={m} k={k} admissible_subsets={nadm}/{nsub} SAT witness={chosen} every_{k}_subset_bad={ok} secs={secs:.1f}", flush=True)
        return "sat", chosen
    print(f"INTSEARCH N={N} m={m} k={k} admissible_subsets={nadm}/{nsub} UNSAT secs={secs:.1f}", flush=True)
    return "unsat", None

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        assert search(17, 12, 6)[0] == "sat"      # the known (12,6) witness lives in [1,17]
        assert search(17, 13, 6)[0] == "sat"      # P = {1,2,3,4,5,6,8,9,10,12,14,15,17} has no admissible 6-subset (h(27) <= 5 bundle)
        assert search(10, 9, 5)[0] == "sat"       # {1,...,8,10}
        assert search(22, 10, 5)[0] == "unsat"    # the proved lemma: no 10-set anywhere, so none in [1,22]
        print("SELFTEST OK"); sys.exit(0)
    N, m, k = map(int, sys.argv[1:4])
    st, w = search(N, m, k); sys.exit(10 if st == "sat" else 20)
