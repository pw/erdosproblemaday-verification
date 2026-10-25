"""T4: clause-level PH == semantic PH, per (w,Y), on random edge assignments (all branches incl. partner block,
own-block z, fixed internal edges).  Usage: test_ph.py k j [--relax-pairs] [--mut NAME] [trials]"""
import sys, random, itertools
sys.path.insert(0, __import__("os").path.dirname(__file__))
import lib
from pysat.solvers import Solver

MUTS = {
    # m <-> "z HAS a neighbour in Y" instead of "has none" (direction of the m definition flipped)
    "mflip": [("            for l in ls: cnf.append([-m, -l])\n            cnf.append([m] + ls)\n",
               "            for l in ls: cnf.append([-m, l])\n            cnf.append([-m] + [l for l in ls[:1]])\n")],
    # forget the inside-Y neighbours of w (drop the second loop's contribution)
    "noinY": [("                ors.append(ew)\n            ors = [o for o in ors",
               "                pass\n            ors = [o for o in ors")],
    # treat inside-Y z as missing Y even when matched (wrong: a matched z touches Y via its internal edge)
    "inYall": [("                if any(adjfixed(z, b) for b in blocks[Y] if b != z):\n                    continue\n",
                "")],
}

k, j = int(sys.argv[1]), int(sys.argv[2])
args = [str(k), str(j), "1", "kissat", "--ph"]
if "--relax-pairs" in sys.argv: args.append("--relax-pairs")
mut = sys.argv[sys.argv.index("--mut") + 1] if "--mut" in sys.argv else None
trials = int(sys.argv[-1]) if sys.argv[-1].isdigit() and len(sys.argv) > 3 else 40
ns = lib.build(args, MUTS[mut] if mut else None)
var, N, nb, blocks, blk, internal = ns["var"], ns["N"], ns["nb"], ns["blocks"], ns["blk"], ns["internal"]
PHC = ns["_PHC"]
cl = ns["cnf"].clauses
first = min(a for a, b in PHC.values())
mdefs = cl[ns["_M"]["ph"]:first]
assert len(PHC) == N * (nb - 1), len(PHC)
rng = random.Random(12345)
mism = 0; tot = 0; holds = 0
for tr in range(trials):
    p = [0.03, 0.08, 0.15, 0.25, 0.4][tr % 5]
    X = {q: rng.random() < p for q in var}
    adj = {v: set() for v in range(N)}
    for (a, b), on in X.items():
        if on: adj[a].add(b); adj[b].add(a)
    for a, b in internal:
        adj[a].add(b); adj[b].add(a)
    assum = [var[q] if on else -var[q] for q, on in X.items()]
    for (w, Y), (a, b) in PHC.items():
        sem = any(not (adj[z] & set(blocks[Y])) for z in adj[w])
        with Solver(name="minisat22", bootstrap_with=mdefs + cl[a:b]) as s:
            got = s.solve(assumptions=assum)
        tot += 1; holds += sem
        if got != sem:
            mism += 1
            if mism <= 3: print("MISMATCH", (w, Y), "semantic", sem, "clause", got, "p", p)
print(f"k={k} j={j} relax={'--relax-pairs' in sys.argv} mut={mut}: {tot} (w,Y,assignment) checks, "
      f"semantic PH true in {holds}, mismatches {mism}")
