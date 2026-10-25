#!/usr/bin/env python3
"""Extract a minimal unsatisfiable core (MUS, deletion-based) of a config188 CNF, with pysat
(cadical153 incremental, clause selectors), and dump the core as points/pairs/runs JSON."""
import sys, json
from pysat.formula import CNF
from pysat.solvers import Solver

def mus(clauses, solver='cadical153'):
    n = max(abs(l) for c in clauses for l in c)
    sel = list(range(n+1, n+1+len(clauses)))
    with Solver(name=solver, bootstrap_with=[c + [-s] for c, s in zip(clauses, sel)]) as S:
        assert S.solve(assumptions=sel) is False, "instance is SAT"
        core = set(S.get_core())
        keep = [s for s in sel if s in core]
        # deletion-based minimisation
        i = 0
        while i < len(keep):
            trial = keep[:i] + keep[i+1:]
            if S.solve(assumptions=trial) is False:
                keep = [s for s in trial if s in set(S.get_core())]
            else:
                i += 1
        assert S.solve(assumptions=keep) is False
    idx = [s - n - 1 for s in keep]
    return [clauses[i] for i in idx], idx

if __name__ == "__main__":
    base = sys.argv[1]  # runs/xxx  (expects xxx.cnf + xxx.json)
    cnf = CNF(from_file=base + ".cnf")
    core, idx = mus(cnf.clauses)
    meta = json.load(open(base + ".json"))
    pts = meta["points"]
    used = sorted({abs(l) - 1 for c in core for l in c})
    pairs = [tuple(abs(l)-1 for l in c) for c in core if len(c) == 2 and all(l < 0 for l in c)]
    runs_ = [tuple(l-1 for l in c) for c in core if len(c) >= 2 and all(l > 0 for l in c)]
    units = [tuple((l-1 if l > 0 else l) for l in c) for c in core if len(c) == 1]   # positive: index; negative: -(index+1)
    print(f"core: {len(core)} clauses ({len(pairs)} unit-distance pairs, {len(runs_)} runs, {len(units)} units) over {len(used)} points")
    json.dump({"source": base, "core_clauses": core, "points_used": used,
               "pairs": pairs, "runs": runs_, "units": units,
               "points": {i: pts[i] for i in used}, "tags": {i: meta["tags"][i] for i in used},
               "isos": meta["isos"], "iso_words": meta.get("iso_words"), "gen_desc": meta.get("gen_desc"),
               "k": meta["k"], "ds": meta["ds"]}, open(base + ".core.json", "w"), indent=0)
    print("->", base + ".core.json")
