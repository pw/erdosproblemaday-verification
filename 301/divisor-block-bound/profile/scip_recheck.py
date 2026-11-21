#!/usr/bin/env python3
"""Second-solver re-check (SCIP via pyscipopt) of the CP-SAT 'infeasible' verdicts, from the dumped cut sets.
Every cut is first re-checked to be a genuine solution set (Fractions). Then:
  profile dump (partial_M_T.json): for each jump at d with F_before, SCIP must find
     {x_d = 1, sum_{prefix} x >= F_before + 1, all cuts inside the prefix} infeasible.
  maxfree dump: {sum x >= K, all cuts} infeasible.
Exit 0 = every verdict re-confirmed; 1 = a disagreement; 2 = cannot read.
Usage: ~/.venv/bin/python scip_recheck.py FILE.json [maxd]"""
import sys, json
from fractions import Fraction
from pyscipopt import Model, quicksum
try: J = json.load(open(sys.argv[1]))
except Exception as e: print("CANNOT READ", e); sys.exit(2)
maxd = int(sys.argv[2]) if len(sys.argv) > 2 else 10**12
mind = int(sys.argv[3]) if len(sys.argv) > 3 else 0
M = J["M"]; cuts = [tuple(c) for c in J["constraints"]]
def genuine(T): return len(T) >= 3 and Fraction(1, T[0]) == sum(Fraction(1, b) for b in T[1:])
badc = [c for c in cuts if not genuine(sorted(c))]
print("cuts", len(cuts), "non-genuine", len(badc))
if badc: sys.exit(1)
def infeasible(elems, cutset, K, force=None):
    m = Model(); m.hideOutput(); m.setParam("limits/time", 3600)
    x = {e: m.addVar(vtype="B") for e in elems}
    m.addCons(quicksum(x.values()) >= K)
    if force: m.addCons(x[force] == 1)
    S = set(elems)
    for c in cutset:
        if set(c) <= S: m.addCons(quicksum(x[e] for e in c) <= len(c) - 1)
    m.optimize(); return m.getStatus()
fails = 0
if "log" in J:  # profile dump
    D = [d for d in range(1, J["tmax"] + 1) if M % d == 0]
    Fb = 0; n = 0
    for (d, verdict, F, iters, nc) in J["log"]:
        if d > maxd: break
        if verdict == "jump" and d > mind:
            st = infeasible([e for e in D if e <= d], cuts, Fb + 1, force=d); n += 1
            ok = st == "infeasible"; fails += not ok
            print(f"jump d={d} F_before={Fb}: SCIP {st} {'OK' if ok else 'DISAGREE'}", flush=True)
        Fb = F
    print("jumps re-checked", n, "disagreements", fails)
else:
    D = [d for d in range(1, J["T"] + 1) if M % d == 0]
    st = infeasible(D, cuts, J["K"]); ok = (st == "infeasible") == (J["status"] == "INFEASIBLE"); fails += not ok
    print(f"maxfree M={M} T={J['T']} K={J['K']}: CP-SAT {J['status']}, SCIP {st} {'OK' if ok else 'DISAGREE'}")
sys.exit(1 if fails else 0)
