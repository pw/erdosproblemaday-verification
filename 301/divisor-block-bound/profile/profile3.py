#!/usr/bin/env python3
"""Exact divisor-block profile for Erdos #301.

For M and D = divisors of M (sorted), F(t) = max size of a subset of D∩[1,t] containing no
solution of 1/a = 1/b_1 + ... + 1/b_k (distinct elements, k >= 2). h(t) = |D∩[1,t]| - F(t).
F increases by 0 or 1 at each new divisor d; h 'jumps' at d iff F does not increase.
W = sum over jump divisors of 1/d  ( = integral of h(t)/t^2 dt ).

Incremental lazy-constraint search with CP-SAT: at divisor d ask whether a solution-free
subset of the prefix of size F_old+1 exists (it must contain d). Every constraint added is a
genuine solution set (re-checked with Fractions at the end); 'no' is the load-bearing verdict
and is re-checked by a second solver (check_infeasible.py) from the dumped constraint sets.
Usage: profile.py M [tmax] [workers]
"""
import sys, json, time
from fractions import Fraction
from itertools import combinations
from ortools.sat.python import cp_model

M = int(sys.argv[1]); TMAX = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != '0' else M
WORKERS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
D = sorted(d for d in range(1, M + 1) if M % d == 0)
D = [d for d in D if d <= TMAX]
idx = {d: i for i, d in enumerate(D)}
L = M  # all reciprocals 1/d = (M/d)/M

def find_solutions(A, per_a=1):
    """For each a in A, look for B subset of {b in A, b>a} with sum M/b = M/a. Return list of frozensets."""
    A = sorted(A); out = []
    for i, a in enumerate(A):
        target = L // a
        items = [L // b for b in A[i + 1:]]
        if sum(items) < target: continue
        mask = (1 << (target + 1)) - 1
        reach = 1; hist = [reach]
        for v in items:
            reach = (reach | (reach << v)) & mask
            hist.append(reach)
        if not (reach >> target) & 1: continue
        # backtrack
        s = target; B = []
        for j in range(len(items) - 1, -1, -1):
            if (hist[j] >> s) & 1: continue  # reachable without item j
            s -= items[j]; B.append(A[i + 1 + j])
        assert s == 0
        out.append(frozenset([a] + B))
    return out

def is_solution(T):
    T = sorted(T); a = T[0]
    return len(T) >= 3 and Fraction(1, a) == sum(Fraction(1, b) for b in T[1:])

# seed: all k=2 and k=3 solutions inside D
cons = set()
Dset = set(D)
for a in D:
    for b in D:
        if b <= a: continue
        num, den = a * b, b - a   # 1/c = 1/a - 1/b
        if num % den == 0:
            c = num // den
            if c in Dset and c > b: cons.add(frozenset((a, b, c)))
for a in D:
    for b in D:
        if b <= a: continue
        r = Fraction(1, a) - Fraction(1, b)
        for c in D:
            if c <= b: continue
            r2 = r - Fraction(1, c)
            if r2 <= 0: break
            if r2.numerator == 1 and r2.denominator in Dset and r2.denominator > c:
                cons.add(frozenset((a, b, c, r2.denominator)))
import os
SEED = os.environ.get("SEED_JSON")
if SEED:
    for c in json.load(open(SEED))["constraints"]:
        if all(x in Dset for x in c) and is_solution(c): cons.add(frozenset(c))
print(f"M={M} |D|={len(D)} seed constraints={len(cons)} (seeded from {SEED})", flush=True)

F = 0; jumps = []; W = Fraction(0); log = []; wits = {}
t0 = time.time()
for step, d in enumerate(D):
    prefix = D[:step + 1]
    iters = 0
    while True:
        iters += 1
        m = cp_model.CpModel()
        x = {e: m.NewBoolVar(f"x{e}") for e in prefix}
        m.Add(x[d] == 1)
        m.Add(sum(x.values()) >= F + 1)
        pset = set(prefix)
        for T in cons:
            if max(T) <= d and T <= pset:
                m.Add(sum(x[e] for e in T) <= len(T) - 1)
        s = cp_model.CpSolver(); s.parameters.num_workers = WORKERS
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE:
            jumps.append(d); W += Fraction(1, d); verdict = 'jump'; break
        assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE), s.StatusName(st)
        A = [e for e in prefix if s.Value(x[e])]
        new = [T for T in find_solutions(A) if T not in cons]
        if not new:
            F += 1; verdict = 'grow'; witness = A; break
        cons.update(new)
    log.append((d, verdict, F, iters, len(cons)))
    if verdict == 'grow': wits[d] = A
    json.dump({"M": M, "tmax": TMAX, "jumps": jumps, "W": [W.numerator, W.denominator], "F": F, "log": log,
               "witnesses": wits, "constraints": sorted(sorted(T) for T in cons)}, open(f"partial_{M}_{TMAX}.json", "w"))
    print(f"d={d:>7} {verdict:4} F={F:>3} h={step+1-F:>3} iters={iters:>4} cons={len(cons):>7} W={float(W):.6f} t={time.time()-t0:.0f}s", flush=True)

# re-check every constraint with Fractions
bad = [sorted(T) for T in cons if not is_solution(T)]
print("constraints genuine:", len(bad) == 0, "bad:", bad[:3])
json.dump({"M": M, "tmax": TMAX, "D": D, "jumps": jumps, "W": [W.numerator, W.denominator], "F_final": F,
           "witness_final": witness if 'witness' in dir() else None, "log": log,
           "constraints": sorted(sorted(T) for T in cons)}, open(f"profile_{M}_{TMAX}.json", "w"))
print("W =", W, "=", float(W))
