"""T5: PH is IMPLIED by its stated premises only -- deg(w) = d, every vertex <= 1 neighbour in Y (own block via the
fixed matching; partner block: none, or <= 1 under --relax-pairs), codegree(w,y) <= 1 for y in Y.  For every (w,Y):
premises AND NOT PH(w,Y) must be UNSAT; dropping the codegree premise (the injectivity) must make some (w,Y) SAT.
NOT PH is written two ways: (i) independently from the edge variables, (ii) through h1cube2's own m[z,Y] variables.
Usage: test_ph_implied.py k j [--relax-pairs]"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

k, j = int(sys.argv[1]), int(sys.argv[2])
RELAX = "--relax-pairs" in sys.argv
SOLVER = sys.argv[sys.argv.index("--solver") + 1] if "--solver" in sys.argv else "minisat22"
FIXNB = "--fixnb" in sys.argv   # fix N(w) to a random admissible 6-set (keeps CDCL out of the C(29,6) choice)
import random; RNG = random.Random(99)
ONLY = int(sys.argv[sys.argv.index("--only") + 1]) if "--only" in sys.argv else None
ns = lib.build([str(k), str(j), "1", "kissat", "--ph", "--drop-c4", "--no-derived", "--no-sb"] + (["--relax-pairs"] if RELAX else []))
var, N, nb, blocks, blk, internal, d = ns["var"], ns["N"], ns["nb"], ns["blocks"], ns["blk"], ns["internal"], ns["d"]
mvar = ns["mvar"]
fixed = lambda a, b: (min(a, b), max(a, b)) in internal
x = lambda a, b: var.get((min(a, b), max(a, b)))
mdefs = ns["cnf"].clauses[ns["_M"]["ph"]:min(a for a, b in ns["_PHC"].values())]
top0 = max(abs(l) for c in ns["cnf"].clauses for l in c)
res = {}
for withcod in (True, False):
    for neg in ("indep", "theirs"):
        nsat = 0
        for w in range(N):
            for Y in range(nb):
                if Y == blk[w]: continue
                if ONLY is not None and w >= ONLY: continue
                cl = []; top = top0
                fd = sum(1 for u in range(N) if u != w and fixed(w, u))
                lits = [x(w, u) for u in range(N) if x(w, u)]
                c = CardEnc.equals(lits=lits, bound=d - fd, top_id=top, encoding=EncType.seqcounter); top = max(top, c.nv); cl += c.clauses
                if FIXNB:
                    RNG.seed(1000 * w + Y); pool = [u for u in range(N) if x(w, u)]
                    while True:
                        S = RNG.sample(pool, d - fd)
                        if all(sum(1 for u in S if blk[u] == Z) <= 1 for Z in range(nb)): break
                    cl += [[x(w, u)] if u in S else [-x(w, u)] for u in pool]
                for z in range(N):          # premise used: every z has <= 1 neighbour in Y (own block: fixed matching)
                    ls = [x(z, b) for b in blocks[Y] if x(z, b)]
                    cl += [[-p, -q] for p, q in itertools.combinations(ls, 2)]
                if withcod:
                    for y in blocks[Y]:
                        com = []
                        for z in range(N):
                            if z in (w, y): continue
                            a = [] if fixed(w, z) else ([x(w, z)] if x(w, z) else None)
                            b = [] if fixed(y, z) else ([x(y, z)] if x(y, z) else None)
                            if a is None or b is None: continue
                            com.append(a + b)
                        cl += [[-l for l in C1 + C2] for C1, C2 in itertools.combinations(com, 2)]
                if neg == "indep":
                    for z in range(N):
                        if z == w: continue
                        ew = True if fixed(w, z) else x(w, z)
                        if ew is None: continue
                        hit = [True if fixed(z, y) else x(z, y) for y in blocks[Y] if y != z]
                        if any(h is True for h in hit): continue
                        hit = [h for h in hit if h]
                        cl.append(([] if ew is True else [-ew]) + hit)
                else:
                    cl += mdefs
                    for z in range(N):
                        if z == w: continue
                        ew = True if fixed(w, z) else x(w, z)
                        if ew is None: continue
                        if blk[z] == Y:
                            if any(fixed(z, b) for b in blocks[Y] if b != z): continue
                            cl.append([-ew]); continue
                        m = mvar[(z, Y)]
                        cl.append(([] if ew is True else [-ew]) + [-m])
                with Solver(name=SOLVER, bootstrap_with=cl) as s:
                    r = s.solve()
                nsat += r
        res[(withcod, neg)] = nsat
        print(f"k={k} j={j} relax={RELAX} codegree-premise={withcod} negation={neg}: SAT in {nsat} of {(N if ONLY is None else ONLY)*(nb-1)} (w,Y) [{SOLVER}]", flush=True)
