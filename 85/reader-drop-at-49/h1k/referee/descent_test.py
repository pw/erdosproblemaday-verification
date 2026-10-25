#!/usr/bin/env python3
"""End-to-end positive control of README §3 (case split + canonical internal matching + residual lex-leader) and of
h1cube.py's C4 / degree / block / SB code IN A REGIME WHERE SOLUTIONS EXIST (generalised block size s >= d).
Solutions come from the referee's own encoder (own_block_enc.py, internal edges FREE, no SB, no fixing). Each solution is
normalised by the referee's own code: orient every pair so e(first) >= e(second); sort pairs by (e_hi, e_lo) descending;
map each block's internal matching onto local (0,1),(2,3),...; then lex-DESCEND under every within-block transposition
that fixes the internal edge set (lex order computed directly, row-major over all vertex pairs). The normal form must be
ACCEPTED by the colleague's (patched-for-s) CNF for that e-pattern, C4 clauses ON. --exhaustive additionally
enumerates every labelled solution and every model of every case CNF and checks (a) case models are all genuine
solutions, (b) every solution's orbit under the FULL symmetry group meets the case models.
Usage: descent_test.py d s nsamples [--exhaustive] [--real k (C4 off, real parameters, their own h1cube.py)]"""
import itertools, os, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from own_block_enc import encode
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

HERE = os.path.dirname(os.path.abspath(__file__))
d, s, ns = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
EXH = "--exhaustive" in sys.argv
REAL = int(sys.argv[sys.argv.index("--real") + 1]) if "--real" in sys.argv else None
rng = random.Random(11)
b = d + 2; N = b * s; blk = [v // s for v in range(N)]; P = lambda X: X ^ 1
order = list(itertools.combinations(range(N), 2))
free = [(u, v) for u, v in order if blk[u] != blk[v] and blk[v] != P(blk[u])]
vid = {p: i + 1 for i, p in enumerate(free)}

def canonE(E):
    return E
def fixed_of(E):
    return {(X * s + 2 * t, X * s + 2 * t + 1) for X in range(b) for t in range(E[X])}
def trans_of(fx):
    out = []
    for X in range(b):
        for u, v in itertools.combinations(range(X * s, X * s + s), 2):
            pi = list(range(N)); pi[u], pi[v] = v, u
            if {(min(pi[a], pi[c]), max(pi[a], pi[c])) for a, c in fx} == fx: out.append(pi)
    return out
def relabel(H, g): return frozenset((min(g[u], g[v]), max(g[u], g[v])) for u, v in H)
def lexless(H1, H2):        # H1 <lex H2 in row-major over all pairs, 0 < 1
    for p in order:
        a, c = p in H1, p in H2
        if a != c: return (not a) and c
    return False

def normalise(H):
    e = [sum(1 for u, v in H if blk[u] == blk[v] == X) for X in range(b)]
    pairs = []
    for p in range(b // 2):
        A, B = 2 * p, 2 * p + 1
        if e[A] < e[B]: A, B = B, A
        pairs.append(((e[A], e[B]), A, B))
    pairs.sort(key=lambda t: t[0], reverse=True) if REAL is None else pairs.sort(key=lambda t: t[0] != (2, 2))
    newblock = {}; E = []
    for i, (_, A, B) in enumerate(pairs):
        newblock[A], newblock[B] = 2 * i, 2 * i + 1; E += [e[A], e[B]]
    g = [None] * N
    for X in range(b):
        L = list(range(X * s, X * s + s))
        M = [(u, v) for u, v in H if blk[u] == blk[v] == X]
        rng.shuffle(M)
        seq = []
        for u, v in M: seq += [u, v] if rng.random() < .5 else [v, u]
        rest = [w for w in L if w not in seq]; rng.shuffle(rest)
        for t, w in enumerate(seq + rest): g[w] = newblock[X] * s + t
    H2 = relabel(H, g)
    fx = fixed_of(E); assert fx <= H2 and all(not (blk[u] == blk[v] and (u, v) not in fx) for u, v in H2)
    TR = trans_of(fx); steps = 0
    while True:
        for pi in TR:
            H3 = relabel(H2, pi)
            if (lexless(H2, H3) if os.environ.get('DESCENT_MUTATE') else lexless(H3, H2)): H2 = H3; steps += 1; break
        else: break
    return H2, tuple(E), fx, TR, steps

cnf_cache = {}
def their_cnf(E):
    if E in cnf_cache: return cnf_cache[E]
    out = os.path.join(HERE, "cnf", f"gen_d{d}_s{s}_E{''.join(map(str, E))}.cnf") if REAL is None else \
          os.path.join(HERE, "cnf", f"k7_j{list(E).count(2) - 4}_noc4.cnf")
    if REAL is None:
        env = dict(os.environ, GEN_D=str(d), GEN_S=str(s), GEN_E=",".join(map(str, E)))
        r = subprocess.run([sys.executable, os.path.join(HERE, "h1cube_gen.py"), "7", "0", "1", "kissat", "--no-derived",
                            "--emit", out], env=env, capture_output=True, text=True, cwd=HERE)
        assert "vars=" in r.stdout, r.stdout + r.stderr
    cl = []; cur = []
    for line in open(out):
        if line[0] in "pc" or not line.strip(): continue
        for t in map(int, line.split()):
            if t == 0: cl.append(cur); cur = []
            else: cur.append(t)
    S = Solver(name="cadical153", bootstrap_with=cl); cnf_cache[E] = (S, cl); return cnf_cache[E]
def accepts(E, H):
    S, _ = their_cnf(E)
    return S.solve(assumptions=[vid[p] if p in H else -vid[p] for p in free])

def gen_solutions(n, allsol=False):
    if REAL is None:
        cl, v2, fx, NN, bl = encode(d, s, E=None, c4=True)
    else:     # real parameters, C4 OFF, with the within-pair e-sum and Lemma D cross constraints (both symmetric)
        cl, v2, fx, NN, bl = encode(d, s, E=None, c4=False)
        top = max(abs(l) for c in cl for l in c)
        for p in range(b // 2):
            ls = [v2[(u, w)] for u, w in v2 if bl[u] == bl[w] and bl[u] in (2 * p, 2 * p + 1)]
            enc = CardEnc.atleast(lits=ls, bound=3, top_id=top, encoding=EncType.totalizer); top = max(top, enc.nv); cl += enc.clauses
        for X, Y in itertools.combinations(range(b), 2):
            if Y == P(X): continue
            ls = [v2[(min(u, w), max(u, w))] for u in range(P(X) * s, P(X) * s + s) for w in range(Y * s, Y * s + s)] + \
                 [v2[(min(u, w), max(u, w))] for u in range(X * s, X * s + s) for w in range(P(Y) * s, P(Y) * s + s)]
            enc = CardEnc.atleast(lits=ls, bound=d - 1, top_id=top, encoding=EncType.totalizer); top = max(top, enc.nv); cl += enc.clauses
    nv = len(v2); out = []
    with Solver(name="glucose4", bootstrap_with=cl) as T:
        while allsol or len(out) < n:
            if not allsol: T.set_phases([x if rng.random() < .25 else -x for x in range(1, nv + 1)])
            if not T.solve(): break
            m = set(T.get_model()); H = frozenset(p for p, i in v2.items() if i in m); out.append(H)
            T.add_clause([-v2[p] for p in H])
    return out

def valid(H, c4=True):
    adj = [set() for _ in range(N)]
    for u, v in H: adj[u].add(v); adj[v].add(u)
    if any(len(adj[v]) != d for v in range(N)): return False
    if any(blk[v] == P(blk[w]) for v in range(N) for w in adj[v]): return False
    if any(sum(1 for w in adj[v] if blk[w] == Y) > 1 for v in range(N) for Y in range(b)): return False
    if c4 and any(len(adj[x] & adj[y]) > 1 for x, y in order): return False
    return True

sols = gen_solutions(ns, allsol=EXH)
print(f"d={d} s={s} N={N} {'REAL k='+str(REAL)+' C4 OFF' if REAL else 'C4 ON'}: {len(sols)} solutions from referee encoder", flush=True)
rej = 0; pats = {}; steps_tot = 0
for H in sols:
    assert valid(H, c4=REAL is None)
    Hn, E, fx, TR, st = normalise(H); steps_tot += st
    assert valid(Hn, c4=REAL is None)
    ok = accepts(E, Hn); pats[E] = pats.get(E, 0) + 1
    if not ok: rej += 1
print(f"  normal forms REJECTED by colleague CNF: {rej} / {len(sols)}   (lex-descent steps total {steps_tot}); patterns {pats}")
if EXH:
    allset = set(sols); U = set(); bad = 0
    for E in pats:
        S, cl = their_cnf(E); fx = fixed_of(E)
        with Solver(name="glucose4", bootstrap_with=cl) as T:
            while T.solve():
                m = set(T.get_model()); H = frozenset([p for p in free if vid[p] in m]) | frozenset(fx)
                if H not in allset: bad += 1
                U.add(H); T.add_clause([-vid[p] for p in free if vid[p] in m])
    print(f"  case-CNF models: {len(U)}; not genuine solutions: {bad}")
    # full group: block perms preserving the pairing x within-block perms
    pairperms = list(itertools.permutations(range(b // 2)))
    blockmaps = []
    for pp in pairperms:
        for sw in itertools.product([0, 1], repeat=b // 2):
            blockmaps.append([2 * pp[X // 2] + ((X % 2) ^ sw[X // 2]) for X in range(b)])
    within = list(itertools.permutations(range(s)))
    miss = 0; orbit_reps = set()
    for H in sols:
        found = False
        for bm in blockmaps:
            for ws in itertools.product(within, repeat=b):
                g = [bm[blk[v]] * s + ws[blk[v]][v % s] for v in range(N)]
                if relabel(H, g) in U: found = True; break
            if found: break
        if not found: miss += 1
    print(f"  solutions whose full-group orbit misses every case model: {miss} / {len(sols)} "
          f"(group order {len(blockmaps) * len(within) ** b})")
