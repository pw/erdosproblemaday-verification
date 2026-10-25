#!/usr/bin/env python3
"""H1 by the e-pattern case split (2026-10-19 15Z seat). Independent of fs/ and of the authors.

Block form (README §reduction): H = graph on the (k+1)(k-2) far vertices, (k-1)-regular, C4-free; k+1 blocks of k-2
(block X = far neighbours of u_X in N(x)), paired (u_X ~ u_X'); no H-edges between paired blocks; every vertex has
<= 1 neighbour in each block (own block included).
LEMMA D (README §derived): with d = k-1, N[X][Y] = #edges between X != Y, N[X][X] = 2 e(X):
    N[X'][Y] + N[X][Y'] >= d-1 for all X != Y;   for Y = X':  e(X) + e(X') >= ceil((d-1)/2).
k = 7: e(X) <= 2 (5-vertex block induces a matching) so every pair has {e(X), e(X')} = {1,2} or {2,2}.
Swapping a pair (X <-> X', i.e. u_X <-> u_X') and permuting pairs are symmetries of the H1 setting, so WLOG
    case j (0..(k+1)/2): pairs 0..j-1 have e = (2,2), pairs j.. have e = (2,1) (first block of the pair has 2).
Inside a block the internal matching is unique up to the block's S_{k-2}: fix it to local edges (0,1),(2,3),...
Residual SB: lex-leader for the within-block transpositions that fix the internal matching (row-lex, fs/README).
Usage: h1cube.py k j cap solver [--no-derived] [--no-sb] [--drop-c4] [--emit path]
  --drop-c4: positive control (C4 clauses removed -> must be SAT; the model is re-checked against the fixed
             internal edges, degrees, block rules and the lex order).
General k: for k = 5 the lemma forces e = 1 everywhere (one case, j ignored)."""
import itertools, os, subprocess, sys, tempfile
from pysat.formula import CNF
from pysat.card import CardEnc, EncType

k, j, cap, solver = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
DERIVED, SB, DROPC4 = "--no-derived" not in sys.argv, "--no-sb" not in sys.argv, "--drop-c4" in sys.argv
EMIT = sys.argv[sys.argv.index("--emit") + 1] if "--emit" in sys.argv else None
d, bs, nb = k - 1, k - 2, k + 1
N = nb * bs
blk = [v // bs for v in range(N)]
partner = lambda X: X ^ 1
blocks = [list(range(X * bs, (X + 1) * bs)) for X in range(nb)]
emax = bs // 2
need = -(-(d - 1) // 2)
if k == 7:
    assert 0 <= j <= nb // 2
    E = []
    for p in range(nb // 2):
        E += [2, 2] if p < j else [2, 1]
elif k == 5:
    E = [1] * nb
else:
    sys.exit("k must be 5 or 7")
for p in range(nb // 2):
    assert E[2 * p] + E[2 * p + 1] >= need and max(E) <= emax
internal = set()
for X in range(nb):
    for t in range(E[X]):
        a, b = blocks[X][2 * t], blocks[X][2 * t + 1]
        internal.add((a, b))
var = {}
for a, b in itertools.combinations(range(N), 2):
    if blk[a] == blk[b] or blk[b] == partner(blk[a]):
        continue
    var[(a, b)] = len(var) + 1
top = len(var)
def x(a, b):
    a, b = min(a, b), max(a, b)
    return var.get((a, b))
def adjfixed(a, b):
    return (min(a, b), max(a, b)) in internal
cnf = CNF()
# degrees: d = internal (fixed) + cross
for v in range(N):
    fixed_deg = sum(1 for w in blocks[blk[v]] if w != v and adjfixed(v, w))
    lits = [x(v, w) for w in range(N) if x(v, w)]
    c = CardEnc.equals(lits=lits, bound=d - fixed_deg, top_id=top, encoding=EncType.seqcounter)
    top = max(top, c.nv); cnf.extend(c.clauses)
    for Y in range(nb):            # <= 1 neighbour in every other block
        if Y in (blk[v], partner(blk[v])):
            continue
        ls = [x(v, w) for w in blocks[Y]]
        for p, q in itertools.combinations(ls, 2):
            cnf.append([-p, -q])
# codegree <= 1 (C4-free) over all pairs, fixed internal edges included as constants
nc4 = 0
if not DROPC4:
    for a, b in itertools.combinations(range(N), 2):
        commons = []   # each item: list of literals that must all be true for c to be a common neighbour
        ok_const = True
        for c in range(N):
            if c in (a, b):
                continue
            la = [] if adjfixed(a, c) else ([x(a, c)] if x(a, c) else None)
            lb = [] if adjfixed(b, c) else ([x(b, c)] if x(b, c) else None)
            if la is None or lb is None:
                continue
            commons.append(la + lb)
        for C1, C2 in itertools.combinations(commons, 2):
            cl = [-l for l in C1 + C2]
            if not cl:
                sys.exit(f"fixed internal edges already contain a C4 at {a},{b}")
            cnf.append(cl); nc4 += 1
# Lemma D cross constraints
def between(X, Y):
    if X == Y:
        return None
    return [x(a, b) for a in blocks[X] for b in blocks[Y] if x(a, b)]
nder = 0
if DERIVED:
    for X, Y in itertools.combinations(range(nb), 2):
        if Y == partner(X):
            continue           # within-pair part is fixed by the case
        lits = between(partner(X), Y) + between(X, partner(Y))
        c = CardEnc.atleast(lits=lits, bound=d - 1, top_id=top, encoding=EncType.seqcounter)
        top = max(top, c.nv); cnf.extend(c.clauses); nder += 1
# residual SB: transpositions inside a block that preserve the fixed internal matching
nsb = 0
trans = []
for X in range(nb):
    L = blocks[X]
    mt = [(L[2 * t], L[2 * t + 1]) for t in range(E[X])]
    single = L[2 * E[X]:]
    trans += [(a, b) for a, b in mt]                                # swap the ends of a matched edge
    trans += list(itertools.combinations(single, 2))                # swap two unmatched vertices
if SB:
    for i, jj in trans:
        cols = [c for c in range(N) if c not in (i, jj)]
        top += 1; eq = top; cnf.append([eq])
        for c in cols:
            a, b = x(i, c), x(jj, c)
            if a is None and b is None:
                # both fixed: must be equal under the transposition (it preserves the fixed edges)
                assert adjfixed(i, c) == adjfixed(jj, c) or (i, jj) in [(min(i, c), max(i, c))], (i, jj, c)
                continue
            assert a is not None and b is not None, (i, jj, c)
            cnf.append([-eq, -a, b])
            top += 1; nxt = top
            cnf.append([-eq, a, b, nxt]); cnf.append([-eq, -a, -b, nxt])
            eq = nxt
        nsb += 1
print(f"k={k} case j={j} e={E} vars={len(var)} clauses={len(cnf.clauses)} c4={nc4} derived={nder} sb={nsb}"
      f"{' DROP-C4 CONTROL' if DROPC4 else ''}", flush=True)
fd, path = tempfile.mkstemp(suffix=".cnf"); os.close(fd); cnf.to_file(path)
if EMIT:
    os.replace(path, EMIT); path = EMIT
BIN = {"kissat": [os.path.expanduser("~/MathDyad/tools/kissat/build/kissat"), "-q"], "cadical": ["/usr/bin/cadical", "-q"]}
p = subprocess.run(["timeout", str(cap), "nice", "-n", "19"] + BIN[solver] + [path], capture_output=True, text=True)
if not EMIT:
    os.unlink(path)
if "s SATISFIABLE" in p.stdout:
    vals = {int(t) for l in p.stdout.splitlines() if l.startswith("v ") for t in l[2:].split() if int(t) > 0}
    adj = {v: set() for v in range(N)}
    for (a, b), i in var.items():
        if i in vals:
            adj[a].add(b); adj[b].add(a)
    for a, b in internal:
        adj[a].add(b); adj[b].add(a)
    bad = []
    for v in range(N):
        if len(adj[v]) != d: bad.append(f"deg {v}={len(adj[v])}")
        for Y in range(nb):
            cnt = len(adj[v] & set(blocks[Y]))
            if Y == partner(blk[v]) and cnt: bad.append(f"partner edge {v}")
            if cnt > 1: bad.append(f"{v} has {cnt} in block {Y}")
    for X in range(nb):
        ie = sum(1 for a, b in itertools.combinations(blocks[X], 2) if b in adj[a])
        if ie != E[X]: bad.append(f"e({X})={ie}")
    cod = max(len(adj[a] & adj[b]) for a, b in itertools.combinations(range(N), 2))
    row = lambda v: [1 if w in adj[v] else 0 for w in range(N)]
    lexbad = 0
    for i, jj in trans:   # semantic lex check: row_i <=lex row_j over columns != i, j
        ri = [row(i)[c] for c in range(N) if c not in (i, jj)]; rj = [row(jj)[c] for c in range(N) if c not in (i, jj)]
        if ri > rj: lexbad += 1
    print(f"SAT  recheck: {len(bad)} structural violations {bad[:3]}, max codegree {cod}, lex violations {lexbad}")
elif "s UNSATISFIABLE" in p.stdout:
    print("UNSAT")
else:
    print(f"UNKNOWN (cap {cap})")
