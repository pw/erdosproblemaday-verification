#!/usr/bin/env python3
"""Independent check of the h = 9 stratum of #85's order-49 case split (submission jhpvtq).

Normalisation (proved in the README, not taken from the authors): in a C4-free 49-vertex graph with
min degree >= 7 and exactly 9 vertices of degree 8 (H), the high-neighbourhoods of the 40 low vertices
are: the triples of a linear triple system T on H (t <= 4), every H-pair not covered by T exactly once,
r3(x) private singletons {x} for each x in H, and 4 - t empty sets.  So the H-L incidence is fixed by the
isomorphism class of T; only the low-low edges are unknown.  20 classes (lts9.py: 1,1,2,5,11 for t=0..4).

Controls through the same encoder: Petersen n=10 deg 3 (SAT, model re-checked), n=10 deg 4 (UNSAT:
n-1 >= d(d-1) fails), Hoffman-Singleton with a closed neighbourhood fixed (SAT, model re-checked),
and a mutation (C4 clauses on free pairs dropped) whose model must FAIL the independent graph check.
"""
import itertools, json, os, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import c4cnf

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1800
KISSAT = str(Path.home() / "MathDyad/tools/kissat/build/kissat")
CADICAL = "/usr/bin/cadical"


def run(solver, path, extra=()):
    t0 = time.time()
    cmd = [KISSAT, "-q"] if solver == "kissat" else [CADICAL, "-q"]
    p = subprocess.run(["timeout", str(CAP), "nice", "-n", "19"] + cmd + list(extra) + [str(path)],
                       capture_output=True, text=True)
    v = "UNSAT" if "s UNSATISFIABLE" in p.stdout else ("SAT" if "s SATISFIABLE" in p.stdout else "UNKNOWN")
    model = [int(t) for line in p.stdout.splitlines() if line.startswith("v ") for t in line[2:].split()]
    return v, round(time.time() - t0, 2), model


def solve_check(name, n, S, fixed, target, expect, mutate=False):
    cnf, var, F, adjS = c4cnf.build(n, S, fixed, target)
    if mutate:   # drop all 4-literal clauses (the free-pair C4 constraints)
        cnf.clauses = [c for c in cnf.clauses if len(c) != 4]
    path = OUT / f"{name}.cnf"; cnf.to_file(str(path))
    rows = []
    for solver in ("kissat", "cadical"):
        v, el, model = run(solver, path)
        note = ""
        if v == "SAT":
            edges = list(fixed) + c4cnf.decode(model, var)
            degs, mc = c4cnf.check_graph(n, edges)
            okdeg = all(degs[u] == target[u] for u in F)
            note = f"model: free degrees ok={okdeg}, max codegree={mc}"
        rows.append((name, solver, v, el, len(var), len(cnf.clauses), expect, note))
        print("\t".join(map(str, rows[-1])), flush=True)
    return rows


def petersen():
    E = [(i, (i + 1) % 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)] + [(i, 5 + i) for i in range(5)]
    return E


def hoffman_singleton():
    # Robertson's construction: pentagons P_h and pentagrams Q_i, vertex (P,h,j)~(Q,i,(h*i+j) mod 5)
    V = [("P", h, j) for h in range(5) for j in range(5)] + [("Q", i, j) for i in range(5) for j in range(5)]
    idx = {v: k for k, v in enumerate(V)}
    E = set()
    for h in range(5):
        for j in range(5):
            E.add(tuple(sorted((idx[("P", h, j)], idx[("P", h, (j + 1) % 5)]))))
            E.add(tuple(sorted((idx[("Q", h, j)], idx[("Q", h, (j + 2) % 5)]))))
    for h in range(5):
        for j in range(5):
            for i in range(5):
                E.add(tuple(sorted((idx[("P", h, j)], idx[("Q", i, (h * i + j) % 5)]))))
    return sorted(E)


rows = []
# --- controls
P = petersen(); degs, mc = c4cnf.check_graph(10, P); assert degs == [3] * 10 and mc <= 1
rows += solve_check("ctl_petersen_free_deg3", 10, [], [], {v: 3 for v in range(10)}, "SAT")
rows += solve_check("ctl_n10_deg4", 10, [], [], {v: 4 for v in range(10)}, "UNSAT")
HS = hoffman_singleton(); degs, mc = c4cnf.check_graph(50, HS); assert degs == [7] * 50 and mc <= 1, (set(degs), mc)
S = list(range(30))   # fix every edge at vertices 0..29; the 20-vertex free part must be re-completed
fixedHS = [e for e in HS if e[0] in S or e[1] in S]
rows += solve_check("ctl_hs_30fixed", 50, S, fixedHS, {v: 7 for v in range(50)}, "SAT")
rows += solve_check("mut_hs30_no_free_c4", 50, S, fixedHS, {v: 7 for v in range(50)}, "SAT-but-model-must-fail", mutate=True)

# --- H9 instances
reps = json.load(open(Path(__file__).parent / "reps.json"))
H = list(range(9))
for t in sorted(reps, key=int):
    for k, T in enumerate(reps[t]):
        T = [tuple(b) for b in T]
        covered = {frozenset(p) for b in T for p in itertools.combinations(b, 2)}
        Pairs = [p for p in itertools.combinations(H, 2) if frozenset(p) not in covered]
        r3 = {x: sum(x in b for b in T) for x in H}
        blocks = [tuple(b) for b in T] + Pairs + [(x,) for x in H for _ in range(r3[x])] + [()] * (4 - int(t))
        assert len(blocks) == 40, (t, k, len(blocks))
        fixed = [(h, 9 + i) for i, b in enumerate(blocks) for h in b]
        degH = {h: sum(1 for a, b in fixed if a == h) for h in H}
        assert all(d == 8 for d in degH.values()), degH
        # every H-pair covered exactly once
        for a, b in itertools.combinations(H, 2):
            assert sum(1 for blk in blocks if a in blk and b in blk) == 1
        rows += solve_check(f"h9_t{t}_rep{k}", 49, H, fixed, {v: 7 for v in range(9, 49)}, "UNSAT")
json.dump(rows, open(OUT / "results.json", "w"), indent=1)
