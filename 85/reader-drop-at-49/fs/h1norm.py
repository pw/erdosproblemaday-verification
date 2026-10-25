#!/usr/bin/env python3
"""H1 (one high vertex) under the anchor normalisation (WLOG, proved in README):
x = 0; its 8 neighbours 1..8 (all degree 7) induce a perfect matching (R1) -> relabel so it is 1-2, 3-4, 5-6, 7-8;
every other vertex has exactly one neighbour among 1..8 (R1b) and each of 1..8 has exactly 5 such (degree 7 = x +
partner + 5) -> relabel the 40 others so B_i = {9+5(i-1) .. 13+5(i-1)}.  All edges at 0..8 fixed; unknowns = the
780 edges among the 40; targets 7.  SB: class transpositions inside each B_i (same fixed nbhd) + lex-leader for
every non-identity permutation of 1..8 preserving the matching (384-element group), induced on the B_i in order.
Usage: h1norm.py <outdir> <cap> <solver> [--no-perm]"""
import itertools, subprocess, sys, time, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fsenc, c4cnf
OUT = Path(sys.argv[1]); CAP = int(sys.argv[2]); solver = sys.argv[3]; noperm = "--no-perm" in sys.argv
slots = "--slots" in sys.argv
OUT.mkdir(parents=True, exist_ok=True)
n = 49; S = list(range(9))
B = {i: list(range(9 + 5 * (i - 1), 14 + 5 * (i - 1))) for i in range(1, 9)}
fixed = [(0, i) for i in range(1, 9)] + [(1, 2), (3, 4), (5, 6), (7, 8)] + [(i, v) for i in B for v in B[i]]
target = {v: 7 for v in range(9, 49)}
cnf, var, F, adjS, st, cls = fsenc.build(n, S, fixed, target, highs=(), sb="all", r1=False, r1b=False)
assert sorted(len(c) for c in cls) == [5] * 8, cls
for v in range(n): assert len(adjS[v] & set(range(1, 9))) == (1 if v >= 9 or v == 0 and False else len(adjS[v] & set(range(1, 9))))
perms = []
if not noperm:
    pairs = [(1, 2), (3, 4), (5, 6), (7, 8)]
    for order in itertools.permutations(range(4)):
        for flips in itertools.product((0, 1), repeat=4):
            sig = {}
            for a, b_ in enumerate(order):
                p, q = pairs[a]; P, Q = pairs[b_]
                if flips[a]: P, Q = Q, P
                sig[p], sig[q] = P, Q
            if all(sig[i] == i for i in range(1, 9)): continue
            pi = list(range(n))
            for i in range(1, 9):
                pi[i] = sig[i]
                for k in range(5): pi[B[i][k]] = B[sig[i]][k]
            perms.append(pi)
    assert len(perms) == 383
    top = max([abs(l) for c in cnf.clauses for l in c] + [len(var)])
    top, nc = fsenc.add_perm_sb(cnf, var, n, perms, top)
nslot = 0
if slots:
    # Implied (sound, README): v in B_i has 6 neighbours among 40, at most one in its own B_i (B_i induces a matching:
    # it lies in N(u_i)), none in the partner's block, at most one in each of the 6 other blocks (common nbr u_j).
    # 6 neighbours over 7 slots of capacity 1 => it misses at most one slot => of any two slots at least one is hit.
    def x(a, b): return var[(a, b) if a < b else (b, a)]
    partner = {1: 2, 2: 1, 3: 4, 4: 3, 5: 6, 6: 5, 7: 8, 8: 7}
    for i in B:
        for v in B[i]:
            sl = [[x(v, w) for w in B[i] if w != v]] + [[x(v, w) for w in B[j]] for j in B if j not in (i, partner[i])]
            assert len(sl) == 7
            for a_, b_ in itertools.combinations(sl, 2):
                cnf.append(a_ + b_); nslot += 1
tag = f"h1norm_{'noperm' if noperm else 'perm383'}{'_slots' if slots else ''}"
path = OUT / f"{tag}.cnf"; cnf.to_file(str(path))
sha = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
BIN = {"kissat": [str(Path.home() / "MathDyad/tools/kissat/build/kissat"), "-q"], "cadical": ["/usr/bin/cadical", "-q"]}
t0 = time.time()
p = subprocess.run(["timeout", str(CAP), "nice", "-n", "19"] + BIN[solver] + [str(path)], capture_output=True, text=True)
v = "UNSAT" if "s UNSATISFIABLE" in p.stdout else ("SAT" if "s SATISFIABLE" in p.stdout else "UNKNOWN")
note = ""
if v == "SAT":
    model = [int(x) for line in p.stdout.splitlines() if line.startswith("v ") for x in line[2:].split()]
    degs, mc = c4cnf.check_graph(49, fixed + c4cnf.decode(model, var))
    note = f"MODEL degrees {sorted(set(degs))} max codegree {mc}"
    (OUT / f"{tag}.{solver}.model").write_text(p.stdout)
print("\t".join(map(str, [tag, solver, v, round(time.time() - t0, 1), sha, len(var), len(cnf.clauses), f"classes={[len(c) for c in cls]} perms={len(perms)} slot_clauses={nslot}", note])), flush=True)
