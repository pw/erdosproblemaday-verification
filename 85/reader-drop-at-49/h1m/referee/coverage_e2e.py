#!/usr/bin/env python3
"""Referee (h1m) objection-hunt (e)+(f): END-TO-END coverage chain on graphs produced OUTSIDE the cell machinery.

For case j:
 1. emit the CASE-level CNF (h1mcell.py without --M) with --drop-c4 --no-sb --slots --ph (Lemma D cross constraints on,
    no SB at all) and solve it with Kissat under several seeds -> several H's (C4 dropped, everything else genuine).
 2. for each H: compute M FROM THE GRAPH by the definition (M[X][Y] = #z in X with no H-neighbour in Y), check
    symmetry, row sums, M4; canonicalise under the brute-force case group (min over the orbit of the flat tuple, as
    menum does) and look the canonical form up in classes_all.tsv; take a g achieving it and relabel H by g.
 3. emit the CELL CNF of that class rep (--M rep, --drop-c4 --no-sb --slots --ph, no pair SB / edgeswap) and check
    that the relabelled H, given as unit clauses on all 600 edge variables, is SAT  (=> H lies in the rep's cell).
 4. negative control: the same relabelled H against the cell of a DIFFERENT class of the same case must be UNSAT.
Usage: coverage_e2e.py j nseeds
"""
import itertools, os, subprocess, sys, tempfile
H1M = "/home/exedev/MathDyad/erdos85/h1m"
KISSAT = os.path.expanduser("~/MathDyad/tools/kissat/build/kissat")
PY = os.path.expanduser("~/.venv/bin/python")
j, nseeds = int(sys.argv[1]), int(sys.argv[2])
N, bs = 40, 5
blk = [v // bs for v in range(N)]
E = []
for p in range(4):
    E += [2, 2] if p < j else [2, 1]
internal = {(X * bs + 2 * t, X * bs + 2 * t + 1) for X in range(8) for t in range(E[X])}
var = {}
for a, b in itertools.combinations(range(N), 2):
    if blk[a] == blk[b] or blk[b] == blk[a] ^ 1:
        continue
    var[(a, b)] = len(var) + 1
PAIRS = [(X, Y) for X in range(8) for Y in range(X + 1, 8) if Y != X ^ 1]
G = [g for g in itertools.permutations(range(8))
     if all(g[X ^ 1] == g[X] ^ 1 for X in range(8)) and all(E[g[X]] == E[X] for X in range(8))]
reps = [tuple(map(int, l.split("\t")[1].split(","))) for l in open(f"{H1M}/classes_all.tsv") if int(l.split("\t")[0]) == j]
repset = set(reps)

def emit(extra, path):
    cmd = f"ulimit -v 4000000; nice -n 19 {PY} {H1M}/h1mcell.py 7 {j} 1 kissat --drop-c4 --no-sb --slots --ph {extra} --emit {path}"
    subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=600)
    assert os.path.exists(path), cmd

def solve(path, units=(), seed=0, cap=600):
    if units:
        txt = open(path).read().split("\n")
        hdr = [i for i, l in enumerate(txt) if l.startswith("p cnf")][0]
        nv, nc = map(int, txt[hdr].split()[2:4])
        txt[hdr] = f"p cnf {nv} {nc + len(units)}"
        fd, p2 = tempfile.mkstemp(suffix=".cnf", dir="/tmp"); os.close(fd)
        with open(p2, "w") as f:
            f.write("\n".join(txt).rstrip("\n") + "\n" + "".join(f"{u} 0\n" for u in units))
        path = p2
    r = subprocess.run(["timeout", str(cap), "nice", "-n", "19", KISSAT, "-q", f"--seed={seed}", path],
                       capture_output=True, text=True)
    if units:
        os.unlink(path)
    if "s SATISFIABLE" in r.stdout:
        return {int(t) for l in r.stdout.splitlines() if l.startswith("v ") for t in l[2:].split() if int(t) > 0}
    return "UNSAT" if "s UNSATISFIABLE" in r.stdout else "UNKNOWN"

def mmat(adj):
    M = [[0] * 8 for _ in range(8)]
    for X in range(8):
        for Y in range(8):
            if X == Y or Y == X ^ 1: continue
            M[X][Y] = sum(1 for z in range(X * bs, X * bs + bs) if not any(w in adj[z] for w in range(Y * bs, Y * bs + bs)))
    return M

def act(g, flat):
    M = [[0] * 8 for _ in range(8)]
    for (X, Y), v in zip(PAIRS, flat): M[X][Y] = M[Y][X] = v
    Nn = [[0] * 8 for _ in range(8)]
    for X in range(8):
        for Y in range(8): Nn[g[X]][g[Y]] = M[X][Y]
    return tuple(Nn[X][Y] for X, Y in PAIRS)

tmp = tempfile.mkdtemp(prefix="h1mref-")
case_cnf = f"{tmp}/case.cnf"; emit("", case_cnf)
ok = bad = 0
seen = set()
for seed in range(nseeds):
    vals = solve(case_cnf, seed=seed, cap=600)
    if not isinstance(vals, set):
        print(f"seed {seed}: case CNF {vals}"); continue
    adj = {v: set() for v in range(N)}
    for (a, b), i in var.items():
        if i in vals: adj[a].add(b); adj[b].add(a)
    for a, b in internal: adj[a].add(b); adj[b].add(a)
    assert all(len(adj[v]) == 6 for v in range(N))
    M = mmat(adj)
    sym = all(M[X][Y] == M[Y][X] for X in range(8) for Y in range(8))
    rows = all(sum(M[X]) == 2 * E[X] for X in range(8))
    m4 = all(M[X ^ 1][Y] + M[X][Y ^ 1] <= 5 for X, Y in PAIRS)
    flat = tuple(M[X][Y] for X, Y in PAIRS)
    can = min(act(g, flat) for g in G)
    g = next(g for g in G if act(g, flat) == can)
    pi = [g[blk[v]] * bs + v % bs for v in range(N)]
    adj2 = {pi[v]: {pi[w] for w in adj[v]} for v in range(N)}
    assert tuple(mmat(adj2)[X][Y] for X, Y in PAIRS) == can
    units = [var[(a, b)] if b in adj2[a] else -var[(a, b)] for (a, b) in var]
    cell = f"{tmp}/cell.cnf"; emit("--M " + ",".join(map(str, can)), cell)
    r_in = solve(cell, units)
    other = next(r for r in reps if r != can)
    cell2 = f"{tmp}/cell2.cnf"; emit("--M " + ",".join(map(str, other)), cell2)
    r_out = solve(cell2, units)
    good = sym and rows and m4 and can in repset and isinstance(r_in, set) and r_out == "UNSAT"
    ok += good; bad += not good
    seen.add(can)
    print(f"j={j} seed {seed}: M sym {sym} rowsums {rows} M4 {m4} class-in-tsv {can in repset} "
          f"rep-cell {'SAT' if isinstance(r_in, set) else r_in} other-cell {'SAT' if isinstance(r_out, set) else r_out} -> {'OK' if good else 'FAIL'}",
          flush=True)
print(f"j={j}: {ok} OK, {bad} FAIL, distinct classes hit {len(seen)}")
