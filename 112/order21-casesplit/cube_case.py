#!/usr/bin/env python3
"""Split one stubborn case CNF 3 ways on the state of one cross-part pair (the lexicographically first free pair
between the out- and in-parts of the root profile), writing <name>_c0/_c1/_c2.cnf. Each child adds one unit clause;
the three children are exhaustive (exactly-one state per pair is already in the CNF), so UNSAT on all three = UNSAT
of the parent. Verify each child's DRAT separately; record which pair was split in <name>.cube.json."""
import sys, json, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases112 import PROFILES, T, V, ORDER
name = sys.argv[1]; d = sys.argv[2] if len(sys.argv) > 2 else "cases"
# recover the profile + variable numbering (deterministic: same pool construction order as cases112.build)
p, q, r = int(name[1]), int(name[2]), int(name[3])
var = V()
for u, v in itertools.combinations(range(ORDER), 2): var.fwd(u, v); var.fwd(v, u); var.none(u, v)   # same creation order as base()
out = list(range(1, 1 + p)); inn = list(range(1 + p, 1 + p + q))
u, v = out[0], inn[0]
lits = [var.fwd(u, v), var.fwd(v, u), var.none(u, v)]
src = open(os.path.join(d, name + ".cnf")).read().splitlines()
hdr = [l for l in src if l.startswith("p cnf")][0]; nv, nc = map(int, hdr.split()[2:4])
body = [l for l in src if not l.startswith("p") and not l.startswith("c")]
for i, lit in enumerate(lits):
    with open(os.path.join(d, f"{name}_c{i}.cnf"), "w") as f:
        f.write(f"p cnf {nv} {nc + 1}\n" + "\n".join(body) + f"\n{lit} 0\n")
json.dump({"parent": name, "split_pair": [u, v], "unit_lits": lits}, open(os.path.join(d, name + ".cube.json"), "w"))
print("wrote 3 children for", name, "split on pair", (u, v), "lits", lits)
