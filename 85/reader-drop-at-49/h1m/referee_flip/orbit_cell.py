#!/usr/bin/env python3
"""Orbit-representative test: JOINT soundness of all symmetry-breaking clauses in one H1 cell (referee_flip, 2026-10-28).

For a cell (j, M): emit with h1mcell.py itself
  base = --drop-c4 --slots --ph --no-sb            (C4 removed so models exist; no SB at all)
  full = --drop-c4 --slots --ph --pairsb --edgeswap (= campaign flags minus C4; within-block transposition SB on)
Sample models x of base (kissat, several seeds), push each through a random element of the cell group first, then ask
a SAT solver whether SOME g in Gamma_c = (within-block groups: D4 on an e=2 block's {0,1,2,3}, Z2 x S3 on an e=1 block)
x| Stab(M) maps x to an assignment satisfying EVERY clause of `full` simultaneously (pair SB + edge-swap SB +
transposition SB + base). g = beta o sigma; sigma looped over Stab(M) in random order, beta chosen by the solver via
one-hot selectors per block. Joint soundness (and Gamma_c-invariance of base) require YES for every x.
Also reports whether the RAW x already satisfies full (if always yes, the test would be vacuous).
Mutations (the test must then FAIL for some x):
  --mut pairflip : pair-level SB direction flipped (X >=lex X o pi) while transposition/edge-swap SB keep X <=lex;
                   injected by patching fsenc.add_perm_sb for block-moving perms only, h1mcell.py run verbatim via runpy.
  --mut invar    : append clauses forcing X = X o pi for one edge swap pi (orbits without a pi-invariant member die).
Usage: orbit_cell.py j M nmodels seed [--mut pairflip|invar] [--noph]"""
import sys, os, subprocess, random, itertools, tempfile, time, shutil
from pysat.formula import CNF
from pysat.solvers import Solver

H = os.path.expanduser("~/MathDyad/erdos85/h1m")
PY = os.path.expanduser("~/.venv/bin/python")
KIS = os.path.expanduser("~/MathDyad/tools/kissat/build/kissat")
j, Mstr, nmod, seed = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
MUT = sys.argv[sys.argv.index("--mut") + 1] if "--mut" in sys.argv else None
NOPH = "--noph" in sys.argv
rng = random.Random(seed)
td = tempfile.mkdtemp(prefix="orb-", dir="/tmp")
HERE = os.path.dirname(os.path.abspath(__file__))

WRAP = os.path.join(td, "wrap_pairflip.py")
open(WRAP, "w").write(f'''import sys, os, runpy
sys.path.insert(0, {os.path.join(H, "..", "fs")!r})
import fsenc
orig = fsenc.add_perm_sb
def patched(cnf, var, n, perms, top):
    moves = [pi for pi in perms if any(pi[v] // 5 != v // 5 for v in range(n))]
    keep = [pi for pi in perms if pi not in moves]
    top, a = orig(cnf, var, n, keep, top)
    negvar = {{k: -v for k, v in var.items()}}       # complemented literals => value order 1 < 0 => X >=lex X o pi
    top, b = orig(cnf, negvar, n, moves, top)
    return top, a + b
fsenc.add_perm_sb = patched
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
''')

def emit(flags, path, mut=False):
    cmd = ([PY, WRAP] if mut else [PY]) + [os.path.join(H, "h1mcell.py"), "7", str(j), "1", "kissat"] + flags + \
          ["--M", Mstr, "--emit", path]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=H)
    assert os.path.exists(path), r.stdout + r.stderr
    return r.stdout.strip().splitlines()

common = ["--drop-c4", "--slots"] + ([] if NOPH else ["--ph"])
basep, fullp = os.path.join(td, "base.cnf"), os.path.join(td, "full.cnf")
print("base:", emit(common + ["--no-sb"], basep)[-2])
fo = emit(common + ["--pairsb", "--edgeswap"], fullp, mut=(MUT == "pairflip"))
print("full:", [l for l in fo if l.startswith("pair-level")], fo[-2] if len(fo) > 1 else fo)
full = CNF(from_file=fullp)

# ---- the h1mcell variable map, rebuilt
N, bs, nb = 40, 5, 8
blk = [v // bs for v in range(N)]
var = {}
for a, b in itertools.combinations(range(N), 2):
    if blk[a] == blk[b] or blk[b] == blk[a] ^ 1:
        continue
    var[(a, b)] = len(var) + 1
assert len(var) == 600
E = []
for p in range(4):
    E += [2, 2] if p < j else [2, 1]
MM = [[0] * nb for _ in range(nb)]
for (X, Y), v in zip([(X, Y) for X in range(8) for Y in range(X + 1, 8) if Y != X ^ 1], map(int, Mstr.split(","))):
    MM[X][Y] = MM[Y][X] = v

def closure(gens):
    G = {tuple(range(5))}
    frontier = list(G)
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                c = tuple(h[g[i]] for i in range(5))
                if c not in G:
                    G.add(c); new.append(c)
        frontier = new
    return sorted(G)
def tp(*cyc):
    p = list(range(5))
    for c in cyc:
        for i in range(len(c)):
            p[c[i]] = c[(i + 1) % len(c)]
    return tuple(p)
B2 = closure([tp((0, 1)), tp((2, 3)), tp((0, 2), (1, 3))])
B1 = closure([tp((0, 1)), tp((2, 3)), tp((2, 4)), tp((3, 4))])
assert len(B2) == 8 and len(B1) == 12
Bg = [B2 if E[Z] == 2 else B1 for Z in range(nb)]

# Stab(M) in G_j, identity included
full_p = [p for p in range(4) if E[2 * p] == E[2 * p + 1]]
half_p = [p for p in range(4) if E[2 * p] != E[2 * p + 1]]
stab = []
for pf in itertools.permutations(full_p):
    for flips in itertools.product((0, 1), repeat=len(full_p)):
        for ph in itertools.permutations(half_p):
            b = [None] * 8
            for s, t, f in zip(full_p, pf, flips):
                b[2 * s] = 2 * t + f; b[2 * s + 1] = 2 * t + 1 - f
            for s, t in zip(half_p, ph):
                b[2 * s] = 2 * t; b[2 * s + 1] = 2 * t + 1
            if all(MM[b[X]][b[Y]] == MM[X][Y] for X in range(8) for Y in range(8)):
                stab.append(tuple(b))
print(f"j={j} M={Mstr} |Stab(M)|={len(stab)} |B|={'x'.join(str(len(g)) for g in Bg)} full clauses={len(full.clauses)} mut={MUT}")

def act(x, sigma, betas):
    """y = x o g, g(u) = 5*sigma(blk u) + beta_{sigma(blk u)}(u mod 5); y_{uv} = x_{g(u) g(v)}"""
    g = [5 * sigma[blk[u]] + betas[sigma[blk[u]]][u % 5] for u in range(N)]
    return {(a, b): x[(min(g[a], g[b]), max(g[a], g[b]))] for (a, b) in var}

def exists_rep(x):
    order = stab[:]; rng.shuffle(order)
    for n_tried, sigma in enumerate(order, 1):
        s = Solver(name="cadical153", bootstrap_with=full.clauses)
        top = full.nv
        sel = {}
        for Z in range(nb):
            sel[Z] = list(range(top + 1, top + 1 + len(Bg[Z]))); top += len(Bg[Z])
            s.add_clause(sel[Z])
            for p, q in itertools.combinations(sel[Z], 2):
                s.add_clause([-p, -q])
        for (u, v), i in var.items():
            Z1, Z2 = sigma[blk[u]], sigma[blk[v]]
            for gi, g1 in enumerate(Bg[Z1]):
                a = 5 * Z1 + g1[u % 5]
                for gj, g2 in enumerate(Bg[Z2]):
                    b = 5 * Z2 + g2[v % 5]
                    s.add_clause([-sel[Z1][gi], -sel[Z2][gj], i if x[(min(a, b), max(a, b))] else -i])
        if MUT == "invar":     # force X = X o pi for the edge swap of block 0
            pi = list(range(N)); pi[0], pi[2], pi[1], pi[3] = 2, 0, 3, 1
            for (a, b), i in var.items():
                k = var[(min(pi[a], pi[b]), max(pi[a], pi[b]))]
                if k != i:
                    s.add_clause([-i, k]); s.add_clause([i, -k])
        r = s.solve(); s.delete()
        if r:
            return True, n_tried
    return False, len(order)

def raw_ok(x):
    with Solver(name="cadical153", bootstrap_with=full.clauses) as s:
        return s.solve(assumptions=[i if x[q] else -i for q, i in var.items()])

ok = fail = raw = 0
t0 = time.time()
for m in range(nmod):
    r = subprocess.run(["bash", "-c", f'ulimit -v 4000000; exec nice -n 19 {KIS} -q --seed={seed + m} {basep}'],
                       capture_output=True, text=True)
    assert "s SATISFIABLE" in r.stdout, r.stdout[:200]
    vals = {int(t) for l in r.stdout.splitlines() if l.startswith("v ") for t in l[2:].split() if int(t) > 0}
    x0 = {q: (1 if i in vals else 0) for q, i in var.items()}
    sig = rng.choice(stab); bet = [rng.choice(Bg[Z]) for Z in range(nb)]
    x = act(x0, sig, bet)                                   # random start point in the orbit
    rw = raw_ok(x); raw += rw
    e, nt = exists_rep(x)
    ok += e; fail += (not e)
    print(f"model {m}: raw x satisfies full: {rw}; orbit has a member satisfying ALL SB+base: {e} (sigmas tried {nt}/{len(stab)})", flush=True)
print(f"RESULT j={j} |Stab|={len(stab)} mut={MUT}: models {nmod}, raw-already-ok {raw}, orbits WITH rep {ok}, orbits with NO rep {fail}  ({time.time() - t0:.0f} s)")
shutil.rmtree(td)
