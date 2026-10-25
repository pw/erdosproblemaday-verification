"""T6: every --slots clause is implied: base (drop-c4 relative, degrees + block rules + fixed matching) AND NOT clause
must be UNSAT.  Control: the STRONGER (false) clause "a matched vertex hits every one of its 6 blocks" must be refutable,
i.e. base AND NOT(that) SAT for some vertex.  Usage: test_slots.py k j"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from pysat.solvers import Solver
k, j = sys.argv[1], sys.argv[2]
base = lib.build([k, j, "1", "kissat", "--drop-c4", "--no-sb"])
sl = lib.build([k, j, "1", "kissat", "--drop-c4", "--no-sb", "--slots"])
assert base["var"] == sl["var"]
slots = lib.section(sl, "slots", "ph")
nv = len(base["var"])
assert all(abs(l) <= nv for c in slots for l in c), "slot clause uses a non-edge variable"
bad = 0
with Solver(name="cadical153", bootstrap_with=base["cnf"].clauses) as s:
    assert s.solve(), "base relative must be SAT"
    for c in slots:
        if s.solve(assumptions=[-l for l in c]): bad += 1
    # control: false strengthening for matched vertices
    x, N, nb, blocks, blk, internal = sl["x"], sl["N"], sl["nb"], sl["blocks"], sl["blk"], sl["internal"]
    refuted = 0; tried = 0
    for v in range(N):
        X = blk[v]
        if not any((min(v, w), max(v, w)) in internal for w in blocks[X]): continue
        for Y in range(nb):
            if Y in (X, X ^ 1): continue
            tried += 1
            if s.solve(assumptions=[-x(v, w) for w in blocks[Y]]): refuted += 1
print(f"k={k} j={j}: {len(slots)} slot clauses, base AND NOT clause SAT for {bad} (must be 0); "
      f"control 'matched vertex hits block Y': refutable in {refuted}/{tried} (must be > 0)")
