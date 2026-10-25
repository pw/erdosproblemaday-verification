#!/usr/bin/env python3
"""Erdős #792, the finite residual left by our wave-7m report (§5): is F_*(13) = 5 or 6?
F_*(n) = min over nonzero integer n-sets A of alpha(A), alpha = largest sum-free subset (a+b=c forbidden, a=b allowed).
Known: Bourgain gives F_*(13) >= 5; the positive witness {1,...,300} gives <= 6; and the POSITIVE case is settled
(every positive 13-set has a sum-free 6-subset: QF_LRA unsat, report §4). Negation preserves Schur relations, so a
13-set with alpha <= 5 may be assumed to have k in {0,...,6} negative elements. For each k this script asks z3/cvc5:
  do reals x_0 < ... < x_12, exactly k of them negative (x_{k-1} < 0 < x_k = 1 after scaling), exist such that EVERY
  t-subset (t=6) contains a Schur relation x_i + x_j = x_m (i<=j, m not in {i,j})?
UNSAT over the reals => no integer counterexample with that sign pattern (integers are reals; scaling is a symmetry).
SAT => the rational model is scaled to integers and RE-CHECKED exactly (alpha by brute force) before being believed.
Atoms are pruned by the order+sign constraints (--prune): positives sum above both, negatives below both, a negative
plus a positive lands strictly between them. --no-prune keeps every (i<=j, m) as a second, decorrelated encoding.
Controls: (k=0,t=6) must be UNSAT (report §4, independent re-derivation); (k,t=7) must be SAT for every k (alpha<=6 is
attainable with any sign split, e.g. negatives {-1..-k} plus a positive block) and the model must re-check.
"""
import sys, itertools, time, argparse, math
from fractions import Fraction

def atoms(n, k, prune):
    out = []
    for i in range(n):
        for j in range(i, n):
            for m in range(n):
                if m == i or m == j: continue
                if prune:
                    ni, nj = i < k, j < k
                    if not ni and not nj:
                        if not m > j: continue
                    elif ni and nj:
                        if not m < i: continue
                    else:
                        if not (i < m < j): continue
                out.append((i, j, m))
    return out

def largest_sum_free(vals):
    vals = list(vals); n = len(vals); best = 0
    S = set(vals)
    for mask in range(1, 1 << n):
        B = [vals[i] for i in range(n) if mask >> i & 1]
        if len(B) <= best: continue
        Bs = set(B); ok = True
        for a in B:
            for b in B:
                if a + b in Bs: ok = False; break
            if not ok: break
        if ok: best = len(B)
    return best

def every_subset_covered(vals, t):
    for S in itertools.combinations(vals, t):
        Ss = set(S)
        if not any(a + b in Ss for a in S for b in S): return False
    return True

def run(n, k, t, engine, prune, timeout_ms):
    if engine == "z3":
        from z3 import Real, Bool, Solver, Or, Implies, sat, unsat
    else:
        from cvc5.pythonic import Real, Bool, Solver, Or, Implies, sat, unsat
    x = [Real(f"x{i}") for i in range(n)]
    s = Solver()
    if timeout_ms and engine == "z3": s.set("timeout", timeout_ms)
    for i in range(n - 1): s.add(x[i] < x[i + 1])
    if k > 0: s.add(x[k - 1] < 0)
    if k < n: s.add(x[k] == 1)
    else: s.add(x[n - 1] == -1)
    A = atoms(n, k, prune); b = {}
    for (i, j, m) in A:
        b[(i, j, m)] = Bool(f"b_{i}_{j}_{m}"); s.add(Implies(b[(i, j, m)], x[i] + x[j] == x[m]))
    by_subset = 0
    for S in itertools.combinations(range(n), t):
        Ss = set(S); lits = [b[a] for a in A if a[0] in Ss and a[1] in Ss and a[2] in Ss]
        if not lits:
            print(f"RESULT n={n} k={k} t={t} engine={engine} prune={int(prune)} status=trivially-unsat (subset {S} admits no atom)"); return "unsat"
        s.add(Or(lits)); by_subset += 1
    t0 = time.time(); r = s.check(); secs = time.time() - t0
    status = "sat" if r == sat else "unsat" if r == unsat else "unknown"
    print(f"RESULT n={n} k={k} t={t} engine={engine} prune={int(prune)} atoms={len(A)} clauses={by_subset} status={status} secs={secs:.1f}", flush=True)
    if status == "sat":
        mdl = s.model(); vals = []
        for xi in x:
            v = mdl[xi]
            if v is None: vals.append(Fraction(0)); continue
            try: vals.append(Fraction(v.as_fraction()))
            except Exception:
                try: vals.append(Fraction(v.numerator_as_long(), v.denominator_as_long()))
                except Exception: vals.append(Fraction(str(v)))
        L = 1
        for v in vals: L = L * v.denominator // math.gcd(L, v.denominator)
        ints = [int(v * L) for v in vals]
        ok_sorted = all(ints[i] < ints[i + 1] for i in range(n - 1)) and all(v != 0 for v in ints) and sum(1 for v in ints if v < 0) == k
        cov = every_subset_covered(ints, t); alpha = largest_sum_free(ints)
        print(f"WITNESS k={k} ints={ints} sorted_nonzero_k_ok={ok_sorted} every_{t}_subset_covered={cov} alpha={alpha} "
              f"=> {'VALID COUNTEREXAMPLE (alpha<=%d)' % (t-1) if (ok_sorted and cov and alpha <= t-1) else 'MODEL FAILS EXACT RECHECK'}", flush=True)
    return status

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("k", type=int); ap.add_argument("--n", type=int, default=13); ap.add_argument("--t", type=int, default=6)
    ap.add_argument("--engine", choices=["z3", "cvc5"], default="z3"); ap.add_argument("--no-prune", action="store_true")
    ap.add_argument("--timeout-ms", type=int, default=0)
    a = ap.parse_args()
    st = run(a.n, a.k, a.t, a.engine, not a.no_prune, a.timeout_ms)
    sys.exit({"sat": 10, "unsat": 20}.get(st, 1))
