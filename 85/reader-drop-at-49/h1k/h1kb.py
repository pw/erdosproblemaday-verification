#!/usr/bin/env python3
"""H1 analogue, BLOCK form (equivalent to h1k.py by the hand reduction in README.md): H on (k+1)(k-2) vertices,
(k-1)-regular, k+1 blocks of k-2 in (k+1)/2 pairs; no edges between paired blocks; every vertex has <= 1 neighbour in
each block (own block included); codegree <= 1 in H.  Usage: h1kb.py k [cap] [solver] -> SAT(+recheck as full G)/UNSAT/UNKNOWN"""
import itertools, sys, subprocess, tempfile, os
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
k = int(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 600
solver = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else "kissat"
SB = "--sb" in sys.argv
RELAX = "--relax-pairs" in sys.argv
DERIVED = "--derived" in sys.argv
NEG = next((a.split("=")[1] for a in sys.argv if a.startswith("--negate=")), None)  # implication check: base + NOT(one derived constraint)   # positive control: allow edges between paired blocks
nb, bs = k + 1, k - 2; N = nb * bs
blk = [v // bs for v in range(N)]; partner = lambda b: b ^ 1
var = {}
for a, b in itertools.combinations(range(N), 2):
    if RELAX or blk[b] != partner(blk[a]):
        var[(a, b)] = len(var) + 1
def e(a, b): return var.get((a, b) if a < b else (b, a))
cnf = CNF(); top = len(var)
for v in range(N):
    lits = [e(v, w) for w in range(N) if w != v and e(v, w)]
    c = CardEnc.equals(lits=lits, bound=k - 1, top_id=top, encoding=EncType.seqcounter); top = max(top, c.nv)
    cnf.extend(c.clauses)
    for Y in range(nb):
        ls = [e(v, w) for w in range(Y * bs, (Y + 1) * bs) if w != v and e(v, w)]
        for p, q in itertools.combinations(ls, 2): cnf.append([-p, -q])
for a, b in itertools.combinations(range(N), 2):
    cs = [c for c in range(N) if c not in (a, b) and e(a, c) and e(b, c)]
    for c, d in itertools.combinations(cs, 2):
        cnf.append([-e(a, c), -e(b, c), -e(a, d), -e(b, d)])
# DERIVED (hand lemma, README "derived block constraints"): with N[X][Y] = #H-edges between blocks X != Y and
# N[X][X] = 2 e(X), every pair X != Y satisfies N[X'][Y] + N[X][Y'] >= d-1 (d = k-1): the left side minus (d-1) is the
# number of codegree-0 pairs between X and Y.  For Y = X' this is 2e(X) + 2e(X') >= d-1.
d = k - 1
blocks = [list(range(Y * bs, (Y + 1) * bs)) for Y in range(nb)]
def between(X, Y):
    if X == Y:
        return [e(a, b) for a, b in itertools.combinations(blocks[X], 2) if e(a, b)]
    return [e(a, b) for a in blocks[X] for b in blocks[Y] if e(a, b)]
dcons = []
for X, Y in itertools.combinations(range(nb), 2):
    if Y == partner(X):
        lits = between(X, X) + between(Y, Y); bound = -(-(d - 1) // 2)    # e(X)+e(X') >= ceil((d-1)/2)
    else:
        lits = between(partner(X), Y) + between(X, partner(Y)); bound = d - 1
    dcons.append((X, Y, lits, bound))
if DERIVED:
    for X, Y, lits, bound in dcons:
        c = CardEnc.atleast(lits=lits, bound=bound, top_id=top, encoding=EncType.seqcounter); top = max(top, c.nv)
        cnf.extend(c.clauses)
if NEG is not None:
    X, Y, lits, bound = dcons[int(NEG)]
    c = CardEnc.atmost(lits=lits, bound=bound - 1, top_id=top, encoding=EncType.seqcounter); top = max(top, c.nv)
    cnf.extend(c.clauses)
    print(f"NEGATE constraint #{NEG}: blocks {X},{Y}: at most {bound-1} of {len(lits)}", flush=True)
nsb = 0
if SB:   # lex-leader for every transposition of two vertices in the same block (fs/README.md derivation, row-major)
    F = lambda: None
    def x(a, b):
        return e(a, b)
    for i, j in itertools.combinations(range(N), 2):
        if blk[i] != blk[j]: continue
        cols = [c for c in range(N) if c not in (i, j) and (x(i, c) or x(j, c))]
        top += 1; eq = top; cnf.append([eq])
        for c in cols:
            a, b = x(i, c), x(j, c)          # both exist: same block => same allowed columns
            cnf.append([-eq, -a, b])
            top += 1; nxt = top
            cnf.append([-eq, a, b, nxt]); cnf.append([-eq, -a, -b, nxt])
            eq = nxt
        nsb += 1
fd, path = tempfile.mkstemp(suffix='.cnf'); os.close(fd); cnf.to_file(path)
BIN = {"kissat": [os.path.expanduser("~/MathDyad/tools/kissat/build/kissat"), "-q"], "cadical": ["/usr/bin/cadical", "-q"]}
p = subprocess.run(["timeout", str(cap)] + BIN[solver] + [path], capture_output=True, text=True)
os.unlink(path)
if "s SATISFIABLE" in p.stdout:
    vals = {int(t) for l in p.stdout.splitlines() if l.startswith("v ") for t in l[2:].split() if int(t) > 0}
    EH = [ab for ab, i in var.items() if i in vals]
    # rebuild the full G on k^2 vertices: x=0, N(x)=1..k+1 (matched 1-2,3-4,..), block b hangs off vertex 1+b
    n = k * k; off = k + 2
    E = [(0, i) for i in range(1, k + 2)] + [(1 + 2 * j, 2 + 2 * j) for j in range(nb // 2)]
    E += [(1 + blk[v], off + v) for v in range(N)] + [(off + a, off + b) for a, b in EH]
    adj = {v: set() for v in range(n)}
    for a, b in E: adj[a].add(b); adj[b].add(a)
    degs = [len(adj[v]) for v in range(n)]
    cod = max(len(adj[a] & adj[b]) for a, b in itertools.combinations(range(n), 2))
    ok = degs[0] == k + 1 and all(d == k for d in degs[1:]) and cod <= 1
    print(f"k={k}: SAT  H edges={len(EH)}  full G n={n}: deg(x)={degs[0]} others {min(degs[1:])}..{max(degs[1:])} "
          f"max codegree={cod}  RECHECK {'PASS' if ok else 'FAIL'}")
    print("H_EDGES", EH)
elif "s UNSATISFIABLE" in p.stdout:
    print(f"k={k}: UNSAT ({solver}{', sb' if SB else ''}{', derived' if DERIVED else ''}{', RELAXED' if RELAX else ''}{', negated #'+NEG if NEG else ''})")
else:
    print(f"k={k}: UNKNOWN (cap {cap}s, {solver}{', sb' if SB else ''}{', derived' if DERIVED else ''})")
