#!/usr/bin/env python3
"""Cube-and-conquer for the #792 n=15 hard sign patterns (mixed792.py, k=4..7 time out at 12 h).
Cube = the weak interleaving of |negatives| among the positives. With x_0<..<x_{k-1}<0<x_k<..<x_{n-1} and a_i=-x_i,
each negative i gets a slot r_i in {k..n}: x_{r_i-1} <= a_i <= x_{r_i}  (x_{k-1}:=0 side is free, x_n:=+inf side is free).
a_0>a_1>..>a_{k-1} forces r_0>=r_1>=..>=r_{k-1}; the non-strict inequalities make the C(n,k) cubes COVER every real
assignment (ties sit in two cubes), so  all cubes UNSAT  =>  the pattern is UNSAT. A cube also prunes mixed atoms soundly:
r_i<=j  => a_i<=x_j => x_i+x_j>=0 => m in [k,j);   r_i>j => a_i>=x_j => x_i+x_j<=0 => m in (i,k).
Controls (--selftest): every cube count == C(n,k); a hand witness with alpha<=t-1 per k lands in a cube whose pruned atom
set still contains every Schur relation the witness uses, and that cube is SAT at t with a model that re-checks exactly."""
import sys, itertools, time, argparse, math, random
from fractions import Fraction
from mixed792 import largest_sum_free, every_subset_covered

def cubes(n, k):
    # non-increasing r_0>=...>=r_{k-1}, each in k..n
    return [tuple(c) for c in itertools.combinations_with_replacement(range(n, k - 1, -1), k)]

def partial_cubes(n, k, slots):
    slots = sorted(slots); out = []
    for c in itertools.combinations_with_replacement(range(n, k - 1, -1), len(slots)):
        cube = [None] * k
        for s_, r in zip(slots, c): cube[s_] = r
        out.append(tuple(cube))
    return out

def cube_of(vals, k):
    n = len(vals); vals = sorted(vals); a = [-v for v in vals[:k]]; pos = vals[k:]
    r = []
    for ai in a:
        # smallest slot r in k..n with ai <= x_r (x_n = inf); then x_{r-1} <= ai holds for the smallest such r
        slot = n
        for j in range(k, n):
            if ai <= pos[j - k]: slot = j; break
        r.append(slot)
    return tuple(r)

def atoms(n, k, cube):
    out = []
    for i in range(n):
        for j in range(i, n):
            for m in range(n):
                if m == i or m == j: continue
                ni, nj = i < k, j < k
                if not ni and not nj:
                    if not m > j: continue
                elif ni and nj:
                    if not m < i: continue
                else:
                    if cube[i] is None:
                        if not (i < m < j): continue
                    elif cube[i] <= j:
                        if not (k <= m < j): continue
                    else:
                        if not (i < m < k): continue
                out.append((i, j, m))
    return out

def solve(n, k, t, cube, timeout_ms=0, want_model=True):
    from z3 import Real, Bool, Solver, Or, Implies, sat, unsat
    x = [Real(f"x{i}") for i in range(n)]
    s = Solver()
    if timeout_ms: s.set("timeout", timeout_ms)
    for i in range(n - 1): s.add(x[i] < x[i + 1])
    s.add(x[k - 1] < 0); s.add(x[k] == 1)
    for i in range(k):
        r = cube[i]
        if r is None: continue
        if r > k: s.add(-x[i] >= x[r - 1])
        if r < n: s.add(-x[i] <= x[r])
    A = atoms(n, k, cube); b = {}
    for a in A:
        b[a] = Bool("b_%d_%d_%d" % a); s.add(Implies(b[a], x[a[0]] + x[a[1]] == x[a[2]]))
    for S in itertools.combinations(range(n), t):
        Ss = set(S); lits = [b[a] for a in A if a[0] in Ss and a[1] in Ss and a[2] in Ss]
        if not lits: return "unsat", 0.0, len(A), None
        s.add(Or(lits))
    t0 = time.time(); r = s.check(); secs = time.time() - t0
    status = "sat" if r == sat else "unsat" if r == unsat else "unknown"
    ints = None
    if status == "sat" and want_model:
        mdl = s.model(); vals = []
        for xi in x:
            v = mdl[xi]
            vals.append(Fraction(0) if v is None else Fraction(v.as_fraction()))
        L = 1
        for v in vals: L = L * v.denominator // math.gcd(L, v.denominator)
        ints = [int(v * L) for v in vals]
    return status, secs, len(A), ints

def witness(n, k):
    # k negatives -1..-k and n-k positives spread out: alpha small by construction? we just need alpha <= t-1 = (n-1)//2 roughly;
    # use negatives -1..-k, positives 1..(n-k) (a block); alpha of {-k..-1} U {1..n-k} is computed exactly below.
    return sorted([-i for i in range(1, k + 1)] + list(range(1, n - k + 1)))

def selftest(n, t):
    for k in range(1, (n + 1) // 2 + 1):
        C = cubes(n, k); assert len(C) == math.comb(n, k), (k, len(C))
        assert len(set(C)) == len(C)
        w = witness(n, k); al = largest_sum_free(w)
        cb = cube_of(w, k); assert cb in set(C), (k, cb)
        # every Schur relation the witness realises must survive pruning in its own cube
        A = set(atoms(n, k, cb)); idx = {v: i for i, v in enumerate(w)}
        missing = [(w[i], w[j], w[i] + w[j]) for i in range(n) for j in range(i, n)
                   if w[i] + w[j] in idx and idx[w[i] + w[j]] not in (i, j) and (i, j, idx[w[i] + w[j]]) not in A]
        tt = al + 1  # witness proves every (al+1)-subset covered => cube must be SAT at t=al+1
        st, secs, na, ints = solve(n, k, tt, cb, timeout_ms=600000)
        ok = st == "sat" and ints is not None and every_subset_covered(ints, tt) and largest_sum_free(ints) <= al
        print(f"selftest k={k} cubes={len(C)} witness_alpha={al} cube={cb} missing_atoms={len(missing)} "
              f"sat_at_t={tt}:{st} secs={secs:.1f} recheck={'OK' if ok else 'FAIL'}", flush=True)
        assert not missing and ok, "SELFTEST FAILED"
    print("SELFTEST OK")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("k", type=int, nargs="?"); ap.add_argument("--n", type=int, default=15); ap.add_argument("--t", type=int, default=7)
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--seed", type=int, default=1); ap.add_argument("--timeout-ms", type=int, default=0)
    ap.add_argument("--cube", type=str, default=None); ap.add_argument("--list", action="store_true")
    ap.add_argument("--slots", type=str, default=None, help="partial cubes: fix only these negatives' slots, e.g. 0,6")
    a = ap.parse_args()
    if a.selftest: selftest(a.n, a.t); sys.exit(0)
    C = partial_cubes(a.n, a.k, [int(v) for v in a.slots.split(",")]) if a.slots else cubes(a.n, a.k)
    if a.list:
        for c in C: print(",".join(map(str, c)))
        sys.exit(0)
    if a.cube: todo = [tuple(None if v in ("_", "x") else int(v) for v in a.cube.split(","))]
    elif a.sample: random.seed(a.seed); todo = random.sample(C, a.sample)
    else: todo = C
    worst = "unsat"
    for cb in todo:
        st, secs, na, ints = solve(a.n, a.k, a.t, cb, a.timeout_ms)
        line = f"CUBE n={a.n} k={a.k} t={a.t} cube={','.join('_' if v is None else str(v) for v in cb)} atoms={na} status={st} secs={secs:.1f}"
        if st == "sat":
            cov = every_subset_covered(ints, a.t); al = largest_sum_free(ints)
            line += f" WITNESS ints={ints} covered={cov} alpha={al} => {'VALID COUNTEREXAMPLE' if cov and al <= a.t-1 else 'MODEL FAILS EXACT RECHECK'}"
        print(line, flush=True)
        if st == "sat": worst = "sat"
        elif st == "unknown" and worst != "sat": worst = "unknown"
    sys.exit({"sat": 10, "unsat": 20}.get(worst, 1))
