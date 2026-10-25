#!/usr/bin/env python3
"""Run one from-scratch stratum cell with fsenc (R1 + lex-leader SB).
Usage: fsrun.py <h> <reps.json|-> <t> <rep> <outdir> <cap_s> <solver> [--no-r1] [--no-sb] [--sb consecutive]
For h=5 / h=3 the triple systems are enumerated here (trivial): h=5 t=0 [], t=1 [012], t=2 [012,034]; h=3 t=0 [], t=1 [012]."""
import json, subprocess, sys, time, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fsenc, c4cnf
a = sys.argv
h, repsf, t, k, OUT, CAP, solver = int(a[1]), a[2], int(a[3]), int(a[4]), Path(a[5]), int(a[6]), a[7]
r1 = "--no-r1" not in a
r1b = "--no-r1b" not in a
sb = False if "--no-sb" in a else ("consecutive" if "consecutive" in a else "all")
SMALL = {5: {0: [[]], 1: [[(0, 1, 2)]], 2: [[(0, 1, 2), (0, 3, 4)]]}, 3: {0: [[]], 1: [[(0, 1, 2)]]}, 1: {0: [[]]}}
T = SMALL[h][t][k] if repsf == "-" else json.load(open(repsf))[str(t)][k]
OUT.mkdir(parents=True, exist_ok=True)
H, fixed, target, n0, npairs, nsing = fsenc.stratum(h, T)
cnf, var, F, adjS, st, cls = fsenc.build(49, H, fixed, target, highs=H, sb=sb, r1=r1, r1b=r1b)
hsb = "--hsb" in a
nperm = 0
if hsb:
    import itertools as _it
    blocks = [tuple(sorted(x for x in H if (x, v) in set(fixed))) for v in range(h, 49)]
    perms = []
    for p_, q_ in _it.combinations(range(h), 2):
        sig = list(range(h)); sig[p_], sig[q_] = q_, p_
        try:
            perms.append(fsenc.high_perm(h, h, blocks, sig))
        except AssertionError:
            pass
    top = max([abs(l) for c in cnf.clauses for l in c] + [len(var)])
    top, nperm = fsenc.add_perm_sb(cnf, var, 49, perms, top)
    nperm = len(perms)
tag = f"h{h}_t{t}_rep{k}_{'hsb' if hsb else ''}{'r1' if r1 else 'nor1'}{'b' if r1b else ''}_{sb or 'nosb'}"
path = OUT / f"{tag}.cnf"; cnf.to_file(str(path))
sha = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
BIN = {"kissat": [str(Path.home() / "MathDyad/tools/kissat/build/kissat"), "-q"], "cadical": ["/usr/bin/cadical", "-q"]}
t0 = time.time()
p = subprocess.run(["timeout", str(CAP), "nice", "-n", "19"] + BIN[solver] + [str(path)], capture_output=True, text=True)
v = "UNSAT" if "s UNSATISFIABLE" in p.stdout else ("SAT" if "s SATISFIABLE" in p.stdout else "UNKNOWN")
note = ""
if v == "SAT":
    model = [int(x) for line in p.stdout.splitlines() if line.startswith("v ") for x in line[2:].split()]
    edges = fixed + c4cnf.decode(model, var)
    degs, mc = c4cnf.check_graph(49, edges)
    note = f"MODEL degrees {sorted(set(degs))} max codegree {mc}"
    (OUT / f"{tag}.{solver}.model").write_text(p.stdout)
print("\t".join(map(str, [tag, solver, v, round(time.time() - t0, 1), sha, len(var), len(cnf.clauses),
      f"n0={n0} pairs={npairs} singles={nsing} classes={st['sb_classes']} highperms={nperm}", note])), flush=True)
