#!/usr/bin/env python3
"""Independent from-scratch check of one stratum H_h of #85's order-49 split, for the cells given by a file of
linear triple systems (lts.py output).  Normalisation (README): high set H = {0..h-1}, every H-pair covered exactly
once by a low vertex; low high-neighbourhoods = the triples of T, the H-pairs T leaves uncovered, s(x) = 9 - h + r3(x)
private singletons per x, and n0 = 49 - h - t - |P| - sum s(x) empty sets.  Unknown: the low-low edges.
Usage: hrun.py <h> <reps.json> <tmin> <tmax> <outdir> <cap_s> <solvers comma-separated>
"""
import itertools, json, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import c4cnf

h, repsf, tmin, tmax, OUT, CAP = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]), int(sys.argv[6])
SOLVERS = [] if sys.argv[7] == "none" else sys.argv[7].split(",")
OUT.mkdir(parents=True, exist_ok=True)
BIN = {"kissat": [str(Path.home() / "MathDyad/tools/kissat/build/kissat"), "-q"], "cadical": ["/usr/bin/cadical", "-q"]}
H = list(range(h))
reps = json.load(open(repsf))
for t in sorted((int(k) for k in reps), key=int):
    if not (tmin <= t <= tmax):
        continue
    for k, T in enumerate(reps[str(t)]):
        T = [tuple(b) for b in T]
        covered = {frozenset(p) for b in T for p in itertools.combinations(b, 2)}
        Pairs = [p for p in itertools.combinations(H, 2) if frozenset(p) not in covered]
        r3 = {x: sum(x in b for b in T) for x in H}
        sing = [(x,) for x in H for _ in range(9 - h + r3[x])]
        n0 = 49 - h - len(T) - len(Pairs) - len(sing)
        assert n0 >= 0, (t, k, n0)
        blocks = T + Pairs + sing + [()] * n0
        assert len(blocks) == 49 - h
        fixed = [(x, h + i) for i, b in enumerate(blocks) for x in b]
        assert all(sum(1 for a, _ in fixed if a == x) == 8 for x in H)
        for a, b in itertools.combinations(H, 2):
            assert sum(1 for blk in blocks if a in blk and b in blk) == 1
        cnf, var, F, adjS = c4cnf.build(49, H, fixed, {v: 7 for v in range(h, 49)})
        name = f"h{h}_t{t}_rep{k}"
        path = OUT / f"{name}.cnf"; cnf.to_file(str(path))
        for s in SOLVERS:
            t0 = time.time()
            p = subprocess.run(["timeout", str(CAP), "nice", "-n", "19"] + BIN[s] + [str(path)], capture_output=True, text=True)
            v = "UNSAT" if "s UNSATISFIABLE" in p.stdout else ("SAT" if "s SATISFIABLE" in p.stdout else "UNKNOWN")
            note = ""
            if v == "SAT":
                model = [int(x) for line in p.stdout.splitlines() if line.startswith("v ") for x in line[2:].split()]
                degs, mc = c4cnf.check_graph(49, fixed + c4cnf.decode(model, var))
                note = f"MODEL degrees {sorted(set(degs))} max codegree {mc}"
                (OUT / f"{name}.{s}.model").write_text(p.stdout)
            print(f"{name}\t{s}\t{v}\t{round(time.time() - t0, 2)}\tn0={n0} pairs={len(Pairs)} singles={len(sing)}\t{note}", flush=True)
