#!/usr/bin/env python3
"""EXPERIMENT (not a result): restrict one M-cell to a subset S of blocks. Vertices of S, edges inside S only; degree
<= 6 (internal fixed + cross); <= 1 neighbour per block; exact #edges(X,Y) = 5 - M[X][Y] for non-paired X, Y in S;
C4-free inside S; within-block transposition SB. UNSAT would mean the cell's obstruction is local to S."""
import itertools, sys, subprocess, tempfile, os
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from menum import PAIRS, case_E
j = int(sys.argv[1]); flat = list(map(int, sys.argv[2].split(","))); S = list(map(int, sys.argv[3].split(","))); cap = int(sys.argv[4])
E = case_E(j); bs = 5
M = [[0]*8 for _ in range(8)]
for (X, Y), v in zip(PAIRS, flat): M[X][Y] = M[Y][X] = v
V = [X*bs + t for X in S for t in range(bs)]
blk = {v: v // bs for v in V}
internal = {(X*bs + 2*t, X*bs + 2*t + 1) for X in S for t in range(E[X])}
var = {}
for a, b in itertools.combinations(V, 2):
    if blk[a] == blk[b] or blk[b] == blk[a] ^ 1: continue
    var[(a, b)] = len(var) + 1
top = len(var); cnf = CNF()
x = lambda a, b: var.get((min(a, b), max(a, b)))
adjf = lambda a, b: (min(a, b), max(a, b)) in internal
for v in V:
    fd = sum(1 for w in V if blk[w] == blk[v] and w != v and adjf(v, w))
    lits = [x(v, w) for w in V if x(v, w)]
    c = CardEnc.atmost(lits=lits, bound=6 - fd, top_id=top, encoding=EncType.seqcounter); top = max(top, c.nv); cnf.extend(c.clauses)
    for Y in S:
        ls = [x(v, w) for w in V if blk[w] == Y and x(v, w)]
        for p, q in itertools.combinations(ls, 2): cnf.append([-p, -q])
for X, Y in itertools.combinations(S, 2):
    if Y == X ^ 1: continue
    ls = [x(a, b) for a in V if blk[a] == X for b in V if blk[b] == Y]
    c = CardEnc.equals(lits=ls, bound=5 - M[X][Y], top_id=top, encoding=EncType.seqcounter); top = max(top, c.nv); cnf.extend(c.clauses)
for a, b in itertools.combinations(V, 2):
    com = []
    for c in V:
        if c in (a, b): continue
        la = [] if adjf(a, c) else ([x(a, c)] if x(a, c) else None)
        lb = [] if adjf(b, c) else ([x(b, c)] if x(b, c) else None)
        if la is None or lb is None: continue
        com.append(la + lb)
    for C1, C2 in itertools.combinations(com, 2):
        cl = [-l for l in C1 + C2]
        if not cl: sys.exit("fixed C4")
        cnf.append(cl)
fd, path = tempfile.mkstemp(suffix=".cnf"); os.close(fd); cnf.to_file(path)
p = subprocess.run(["timeout", str(cap), "nice", "-n", "19", os.path.expanduser("~/MathDyad/tools/kissat/build/kissat"), "-q", path], capture_output=True, text=True)
os.unlink(path)
print("S=", S, "vars", len(var), "->", "SAT" if "s SATISFIABLE" in p.stdout else "UNSAT" if "s UNSAT" in p.stdout else "UNKNOWN")
