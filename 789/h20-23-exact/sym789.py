#!/usr/bin/env python3
"""Symmetric obstruction search for Erdős #789 (page definition: integers, 0 allowed).
A = ±P (mode 'pm') or {0} ∪ ±P (mode 'zpm'), P = {p_1<...<p_m} positive reals. Every k-subset of A must be
BAD: exists disjoint S,T ⊆ subset, |S|<|T|, sum(S)=sum(T), with S=∅ allowed (then sum(T)=0, T nonempty).
SAT => explicit |A|-element set with H(A) <= k-1  (an exact-table upper bound h(|A|) <= k-1).
UNSAT => no SYMMETRIC obstruction of this shape (says nothing about asymmetric sets)."""
import sys, itertools, time
from fractions import Fraction
from z3 import Real, Solver, Or, Sum, sat, RealVal

def bad_eqs(idx):
    idx = list(idx); eqs = []
    for t in range(1, len(idx)):                          # S = ∅ : a PROPER nonempty zero-sum subset T (the whole
        for T in itertools.combinations(idx, t): eqs.append(((), T))   # set summing to 0 is NOT a violation: S must be nonempty)
    for r in range(1, len(idx)):
        for S in itertools.combinations(idx, r):
            rest = [i for i in idx if i not in S]
            for t in range(r + 1, len(rest) + 1):
                for T in itertools.combinations(rest, t): eqs.append((S, T))
    return eqs

def main():
    mode, m, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    p = [Real(f"p{i}") for i in range(m)]
    s = Solver()
    s.add(p[0] > 0)
    for i in range(m - 1): s.add(p[i] < p[i + 1])
    elems = [p[i] for i in range(m)] + [-p[i] for i in range(m)] + ([RealVal(0)] if mode == "zpm" else [])
    n = len(elems); nd = 0
    for K in itertools.combinations(range(n), k):
        d = [Sum([elems[i] for i in S]) == Sum([elems[i] for i in T]) if S else Sum([elems[i] for i in T]) == 0 for S, T in bad_eqs(K)]
        s.add(Or(d)); nd += len(d)
    print(f"mode={mode} m={m} k={k} n={n} clauses={sum(1 for _ in itertools.combinations(range(n), k))} disjuncts={nd}", flush=True)
    t0 = time.time(); r = s.check(); print(f"-> {r} in {time.time()-t0:.1f}s", flush=True)
    if r == sat:
        mdl = s.model(); vals = [Fraction(mdl.eval(x, model_completion=True).numerator_as_long(), mdl.eval(x, model_completion=True).denominator_as_long()) for x in p]
        import math
        L = 1
        for v in vals: L = L * v.denominator // math.gcd(L, v.denominator)
        P = [int(v * L) for v in vals]; g = 0
        for v in P: g = math.gcd(g, v)
        P = [v // g for v in P]
        A = sorted(set(P + [-x for x in P] + ([0] if mode == "zpm" else [])))
        print("P =", P); print("A =", A, "n =", len(A))
        # independent exact re-check of H(A) <= k-1 via literal definition
        def admissible(B):
            seen = {}
            for r_ in range(1, len(B) + 1):
                for S in itertools.combinations(B, r_):
                    sm = sum(S)
                    if sm in seen and seen[sm] != r_: return False
                    seen.setdefault(sm, r_)
            return True
        ok = not any(admissible(S) for S in itertools.combinations(A, k))
        print(f"RECHECK: no admissible {k}-subset in A: {ok}  (so H(A) <= {k-1}, h({len(A)}) <= {k-1})", flush=True)

if __name__ == "__main__": main()
