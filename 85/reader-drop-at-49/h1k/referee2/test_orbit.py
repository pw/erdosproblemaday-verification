"""T2/T3: lex-leader soundness of --pairsb COMBINED with the within-block transposition SB, at the CLAUSE level.
Sample models X of a SAT relative of the case formula (default: --drop-c4, Lemma D on, no SB); compute the orbit of X
under a group H that contains P (the pair-level group --pairsb enumerates) and the selected within-block transpositions;
take the lex-least member X* (order = sorted(var) = row-major, X <=lex X o g, (X o g)_q = X_{g(q)}); require
  (a) X* satisfies the base CNF (automorphism check, clause level) and
  (b) X* satisfies the emitted transposition-SB clauses for the transpositions in H AND all emitted pairsb clauses.
--exists: instead of X*, ask whether ANY orbit member satisfies (b) (used for mutation sensitivity).
--mut flip|revorder: mutate fsenc.add_perm_sb (direction flipped / reversed variable order) to show the test can fail.
Usage: test_orbit.py k j nsamples [--relax-pairs] [--sub01] [--exists] [--mut M]"""
import sys, os, random, itertools, types
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from pysat.solvers import Solver

k, j, ns_ = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
RELAX = "--relax-pairs" in sys.argv
SUB01 = "--sub01" in sys.argv          # H uses only the (0 1) swap in every block (keeps |H| small at k = 7)
EXISTS = "--exists" in sys.argv
mut = sys.argv[sys.argv.index("--mut") + 1] if "--mut" in sys.argv else None
extra = ["--relax-pairs"] if RELAX else []

if mut:   # install a mutated fsenc before h1cube2's `import fsenc`
    sys.path.insert(0, os.path.join(os.path.dirname(lib.SRC), "..", "fs"))
    import fsenc
    orig = fsenc.add_perm_sb
    def mutated(cnf, var, n, perms, top):
        if mut == "flip":     # X >=lex X o pi  (opposite direction to the transpositions)
            inv = []
            for pi in perms:
                q = [0] * n
                for a, b in enumerate(pi): q[b] = a
                inv.append(q)
            # X >= X o pi  <=>  X o pi^{-1}... encode directly: swap roles by complementing literals
            class Neg(dict):
                pass
            negvar = {kk: -vv for kk, vv in var.items()}
            return orig(cnf, negvar, n, perms, top)       # literals complemented => 1 < 0 value order
        if mut == "revorder":
            rv = dict(sorted(var.items(), key=lambda t: t[0], reverse=True))
            def add(cnf, var_, n, perms, top):
                x = lambda a, b: var_.get((a, b) if a < b else (b, a))
                order = sorted(var_, reverse=True); nc = 0
                for pi in perms:
                    pos = [(x(a, b), x(pi[a], pi[b])) for (a, b) in order if x(a, b) != x(pi[a], pi[b])]
                    e_prev = None
                    for p, (a_, b_) in enumerate(pos):
                        pre = [] if e_prev is None else [-e_prev]
                        cnf.append(pre + [-a_, b_]); nc += 1
                        if p < len(pos) - 1:
                            top += 1; e = top; cnf.append(pre + [a_, b_, e]); cnf.append(pre + [-a_, -b_, e]); nc += 2
                            e_prev = e
                return top, nc
            return add(cnf, var, n, perms, top)
    fsenc.add_perm_sb = mutated
    sys.modules["fsenc"] = fsenc

sb = lib.build([str(k), str(j), "1", "kissat", "--pairsb"] + extra)          # SB formula (trans SB + pairsb)
base = lib.build([str(k), str(j), "1", "kissat", "--no-sb", "--drop-c4"] + extra)   # SAT relative for samples
var, N, nb, bs, blk, trans, perms = sb["var"], sb["N"], sb["nb"], sb["bs"], sb["blk"], sb["trans"], sb["perms"]
assert base["var"] == var
order = sorted(var)
A = np.array([a for a, b in order]); B = np.array([b for a, b in order])
pidx = -np.ones((N, N), dtype=np.int16)
for i, (a, b) in enumerate(order): pidx[a, b] = i
# split the transposition-SB section into one chain per transposition (each chain starts with the unit [eq])
tsb = lib.section(sb, "tsb", "slots"); chains = []
for c in tsb:
    if len(c) == 1: chains.append([])
    chains[-1].append(c)
assert len(chains) == len(trans), (len(chains), len(trans))
pairsb = lib.section(sb, "pairsb", "end")
# group H = W' x| P
E = sb["E"]
gens_by_block = []
for X in range(nb):
    L = sb["blocks"][X]
    ts = [(a, b) for (a, b) in trans if blk[a] == X]
    if SUB01: ts = [t for t in ts if (t == (L[0], L[1]) and "--no01" not in sys.argv) or ("--sub0123" in sys.argv and E[X] == 2 and t == (L[2], L[3]))
                    or ("--subsingle" in sys.argv and t[0] >= L[2 * E[X]])]     # --subsingle: swaps of two unmatched vertices
    gens_by_block.append(ts)
used = [i for i, t in enumerate(trans) if t in {tt for g in gens_by_block for tt in g}]
def closure(gens, n):
    idp = tuple(range(n)); S = {idp}; frontier = [idp]
    while frontier:
        nxt = []
        for g in frontier:
            for (a, b) in gens:
                h = list(g); h[a], h[b] = h[b], h[a]; h = tuple(h)   # left-multiply by (a b)
                if h not in S: S.add(h); nxt.append(h)
        frontier = nxt
    return S
Wb = [closure(gs, N) for gs in gens_by_block]
# W' = product of per-block groups (they commute; compose by taking each block's action)
Wlist = [np.arange(N)]
for X in range(nb):
    new = []
    for w in Wlist:
        for g in Wb[X]:
            h = w.copy(); idxs = sb["blocks"][X]; h[idxs] = np.array(g)[idxs]; new.append(h)
    Wlist = new
P = [np.arange(N)] + [np.array(p) for p in perms]
G = np.array([w[p] for w in Wlist for p in P], dtype=np.int16)         # g = w o p as vertex maps: v -> w[p[v]]
print(f"k={k} j={j} relax={RELAX} sub01={SUB01} |W'|={len(Wlist)} |P|={len(P)} |H|={len(G)} trans-in-H={len(used)}/{len(trans)} "
      f"pairsb clauses={len(pairsb)} mut={mut}", flush=True)
GA, GB = G[:, A], G[:, B]
IDX = pidx[np.minimum(GA, GB), np.maximum(GA, GB)]
assert (IDX >= 0).all(), "some g maps a free pair to a constant pair"
sbcl = [c for i in used for c in chains[i]] + pairsb
rng = random.Random(7)
fails_a = fails_b = 0; nsamp = 0; raw_viol = 0
with Solver(name="cadical153", bootstrap_with=base["cnf"].clauses) as sbase, \
     Solver(name="cadical153", bootstrap_with=sbcl) as ssb, \
     Solver(name="cadical153", bootstrap_with=base["cnf"].clauses) as sgen:
    for t in range(ns_):
        assum = [rng.choice((1, -1)) * var[q] for q in rng.sample(order, 6)]
        if not sgen.solve(assumptions=assum):
            continue
        mdl = set(l for l in sgen.get_model() if l > 0)
        Xv = np.array([1 if var[q] in mdl else 0 for q in order], dtype=np.uint8); nsamp += 1
        raw_viol += not ssb.solve(assumptions=[var[q] if Xv[i] else -var[q] for i, q in enumerate(order)])
        M = Xv[IDX]                                      # row g = X o g
        if EXISTS:
            ok = 0
            for row in M:
                if ssb.solve(assumptions=[var[q] if row[i] else -var[q] for i, q in enumerate(order)]): ok += 1
            if ok == 0: fails_b += 1
            print(f"  sample {t}: members satisfying SB clauses {ok}/{len(M)}", flush=True)
            continue
        o = np.lexsort(M.T[::-1]); Xs = M[o[0]]
        lits = [var[q] if Xs[i] else -var[q] for i, q in enumerate(order)]
        a_ok = sbase.solve(assumptions=lits); b_ok = ssb.solve(assumptions=lits)
        fails_a += not a_ok; fails_b += not b_ok
    print(f"RESULT: samples {nsamp} (raw sample violating SB: {raw_viol}), lexmin-not-a-base-model {fails_a}, "
          f"{'orbits with NO member passing SB' if EXISTS else 'lexmin violating emitted SB clauses'} {fails_b}")
