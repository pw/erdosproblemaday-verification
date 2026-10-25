#!/usr/bin/env python3
"""lemma789.py with ORDER-PRUNED disjunctions. For a k-subset with positions p_0<...<p_{k-1} (values increasing), a bad
equation sum(S)=sum(T), |S|<|T|, is kept only if some strictly increasing positive k-vector satisfies it (checked once per
position pattern with z3; e.g. x_1 = x_2 + x_3 can never hold, x_6 = x_1 + x_2 can). Dropping an equation that can never
hold is sound: the remaining disjunction is equivalent under the order constraints. Same exact re-check path as lemma789.
  python3 lemma789p.py m k [--engine z3|cvc5] [--timeout-ms N] [--selftest]
Selftest: (6,4) unsat, (5,4) sat+recheck, (9,5) sat+recheck, plus: every pattern dropped is refuted on the known witnesses
(no witness of (5,4)/(9,5)/(12,6) satisfies a dropped equation on any of its k-subsets)."""
import sys, itertools, time, math, argparse
from fractions import Fraction
from lemma789 import bad_equations, is_admissible

def feasible_patterns(k):
    from z3 import Real, Solver, Sum, unsat
    x = [Real(f"p{i}") for i in range(k)]; keep = []
    for S, T in bad_equations(range(k)):
        s = Solver(); s.add(x[0] > 0)
        for i in range(k - 1): s.add(x[i] < x[i + 1])
        s.add(Sum([x[i] for i in S]) == Sum([x[i] for i in T]))
        if s.check() != unsat: keep.append((S, T))
    return keep

def run(m, k, engine="z3", timeout_ms=0, quiet=False):
    if engine == "z3": from z3 import Real, Solver, Or, Sum, sat, unsat
    else: from cvc5.pythonic import Real, Solver, Or, Sum, sat, unsat
    pats = feasible_patterns(k); total = len(bad_equations(range(k)))
    x = [Real(f"x{i}") for i in range(m)]; s = Solver()
    if timeout_ms and engine == "z3": s.set("timeout", timeout_ms)
    s.add(x[0] > 0)
    for i in range(m - 1): s.add(x[i] < x[i + 1])
    nd = 0
    for K in itertools.combinations(range(m), k):
        disj = [Sum([x[K[i]] for i in S]) == Sum([x[K[i]] for i in T]) for S, T in pats]
        s.add(Or(disj)); nd += len(disj)
    t0 = time.time(); r = s.check(); dt = time.time() - t0
    st = "sat" if r == sat else "unsat" if r == unsat else "unknown"
    print(f"(m={m},k={k}) engine={engine} patterns={len(pats)}/{total} clauses={math.comb(m,k)} disjuncts={nd} -> {st} in {dt:.1f}s", flush=True)
    ints = None
    if st == "sat":
        mdl = s.model(); vals = []
        for xi in x:
            v = mdl.eval(xi, model_completion=True)
            try: vals.append(Fraction(v.numerator_as_long(), v.denominator_as_long()))
            except Exception: vals.append(Fraction(str(v)))
        L = 1
        for v in vals: L = L * v.denominator // math.gcd(L, v.denominator)
        ints = [int(v * L) for v in vals]; g = 0
        for v in ints: g = math.gcd(g, v)
        ints = [v // g for v in ints]
        allbad = all(not is_admissible([ints[i] for i in K]) for K in itertools.combinations(range(m), k))
        print(f"  counterexample candidate {ints}; every {k}-subset bad: {allbad}", flush=True)
    return st, ints

def selftest():
    k5 = feasible_patterns(5); k6 = feasible_patterns(6)
    print(f"feasible patterns: k=5 {len(k5)}/65, k=6 {len(k6)}/231")
    # a dropped pattern must never be the equation a real witness satisfies
    wit = {(9, 5): [1, 2, 3, 4, 5, 6, 7, 8, 10], (12, 6): [1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 17], (14, 6): [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16]}
    for (m, k), w in wit.items():
        pats = set(feasible_patterns(k)); dropped = [e for e in bad_equations(range(k)) if e not in pats]
        viol = 0; covered = 0
        for K in itertools.combinations(range(m), k):
            vals = [w[i] for i in K]
            if any(sum(vals[i] for i in S) == sum(vals[i] for i in T) for S, T in dropped): viol += 1
            if any(sum(vals[i] for i in S) == sum(vals[i] for i in T) for S, T in pats): covered += 1
        print(f"witness ({m},{k}): dropped-equation hits={viol} (must be 0), subsets covered by kept patterns={covered}/{math.comb(m,k)} (must be all)")
        assert viol == 0 and covered == math.comb(m, k)
    assert run(6, 4)[0] == "unsat"; assert run(5, 4)[0] == "sat"; assert run(9, 5)[0] == "sat"
    print("SELFTEST OK")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("m", type=int, nargs="?"); ap.add_argument("k", type=int, nargs="?")
    ap.add_argument("--engine", default="z3"); ap.add_argument("--timeout-ms", type=int, default=0); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest(); sys.exit(0)
    st, _ = run(a.m, a.k, a.engine, a.timeout_ms); sys.exit({"sat": 10, "unsat": 20}.get(st, 1))
