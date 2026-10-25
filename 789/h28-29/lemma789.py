#!/usr/bin/env python3
"""Erdős #789 lemma: do every m distinct positive integers contain an ADMISSIBLE k-subset?
Admissible (per the live-page definition, re-derived in our wave-w015 report): for all nonempty
S,T ⊆ B, sum(S)=sum(T) ⇒ |S|=|T|. For positive reals, cancelling the common part shows this is
equivalent to: no two DISJOINT nonempty subsets of DIFFERENT sizes have equal sums.
Negation of the lemma: exist 0 < x_1 < ... < x_m (reals; by homogeneity + rational solvability of
linear systems, integers iff reals) such that EVERY k-subset is bad, i.e. satisfies at least one
"bad equation" sum(S) = sum(T), S,T disjoint nonempty, |S|≠|T|, S,T ⊆ that k-subset.
This is quantifier-free linear real arithmetic; z3 decides it exactly.
  UNSAT  => the lemma holds for all positive reals (hence integers).
  SAT    => an explicit counterexample m-set (we scale the rational model to integers and re-check).
Controls: (m,k)=(6,4) must be UNSAT (our report proved it symbolically); (5,4) must be SAT (e.g. {1,2,3,4,5}).
"""
import sys, itertools, time
from fractions import Fraction
from z3 import Real, Solver, And, Or, Sum, sat, unsat, RealVal

def bad_equations(idx):
    """All (S,T) disjoint nonempty subsets of idx with |S|<|T| (unordered pairs, so S the smaller)."""
    idx = list(idx); eqs = []
    for r in range(1, len(idx)):
        for S in itertools.combinations(idx, r):
            rest = [i for i in idx if i not in S]
            for t in range(r + 1, len(rest) + 1):
                for T in itertools.combinations(rest, t):
                    eqs.append((S, T))
    return eqs

def is_admissible(vals):
    vals = list(vals)
    for S, T in bad_equations(range(len(vals))):
        if sum(vals[i] for i in S) == sum(vals[i] for i in T): return False
    return True

def run(m, k, timeout_ms=None):
    x = [Real(f"x{i}") for i in range(m)]
    s = Solver()
    if timeout_ms: s.set("timeout", timeout_ms)
    s.add(x[0] > 0)
    for i in range(m - 1): s.add(x[i] < x[i + 1])
    nclauses = 0; ndisj = 0
    for K in itertools.combinations(range(m), k):
        disj = [Sum([x[i] for i in S]) == Sum([x[i] for i in T]) for S, T in bad_equations(K)]
        s.add(Or(disj)); nclauses += 1; ndisj += len(disj)
    t0 = time.time(); r = s.check(); dt = time.time() - t0
    print(f"(m={m},k={k}) clauses={nclauses} disjuncts={ndisj} -> {r} in {dt:.1f}s", flush=True)
    if r == sat:
        mdl = s.model()
        vals = []
        for xi in x:
            v = mdl.eval(xi, model_completion=True)
            vals.append(Fraction(v.numerator_as_long(), v.denominator_as_long()))
        import math
        L = 1
        for v in vals: L = L * v.denominator // math.gcd(L, v.denominator)
        ints = [int(v * L) for v in vals]
        g = 0
        for v in ints: g = math.gcd(g, v)
        ints = [v // g for v in ints]
        # independent re-check: every k-subset bad?
        allbad = all(not is_admissible([ints[i] for i in K]) for K in itertools.combinations(range(m), k))
        print(f"  counterexample candidate {ints}; every {k}-subset bad: {allbad}")
        return "SAT", ints, allbad
    return str(r), None, None

if __name__ == "__main__":
    m, k = int(sys.argv[1]), int(sys.argv[2])
    run(m, k, int(sys.argv[3]) if len(sys.argv) > 3 else None)
