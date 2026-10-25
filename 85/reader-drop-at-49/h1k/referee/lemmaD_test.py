#!/usr/bin/env python3
"""Referee's own test of README §1 (reduction) and §2 (Lemma D). Written from scratch; imports nothing of the colleague's.

Generalised family: b = d+2 blocks of size s, paired (2p, 2p+1); H on F = b*s vertices, d-regular,
  (ii) no edge between paired blocks, (iii) every vertex <= 1 neighbour in every block (own block included),
  optionally (i) H C4-free.
G is built explicitly: x, U = {u_0..u_{b-1}} matched u_{2p}-u_{2p+1}, u_X adjacent to every vertex of block X, plus H.
Lemma D's proof never uses s = d-1 except in arithmetic; the general identity it proves is
  q(X,Y) = s^2 - d*s + N[Y'][X] + N[X'][Y]      (s = d-1  ->  N + N - (d-1), the README statement)
and, WITHOUT C4-freeness, steps 1,2,4,5 give
  m(X,Y) := #{z in F with an H-neighbour in X and one in Y} = d*s - N[Y'][X] - N[X'][Y].
Checks per instance: step 1 (each z misses exactly one available block), step 2 (each block missed by exactly s),
m-identity, step 3 counting form sum_{a in X, b in Y} codeg_G(a,b) == m (always) and, when C4-free, the full q identity
with q computed from common neighbours in the FULL G (so step 3's 'common neighbours are far' is tested, not assumed).
§1 check: G C4-free  <=>  (i) and (ii) and (iii), on valid instances and on mutated ones (2-switches / edge flips).
Usage: lemmaD_test.py d s count [--c4] [--seed n]"""
import itertools, random, sys
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def gen(d, s, c4, rng, count, timeout_note=""):
    b = d + 2; N = b * s
    blk = [v // s for v in range(N)]
    perm = list(range(N)); rng.shuffle(perm)            # random relabelling for diversity (blocks preserved below)
    pairs = [(u, v) for u, v in itertools.combinations(range(N), 2) if blk[v] != (blk[u] ^ 1)]
    rng.shuffle(pairs)
    vid = {p: i + 1 for i, p in enumerate(pairs)}
    def X(u, v): return vid.get((min(u, v), max(u, v)))
    cls = []; top = len(vid)
    for v in range(N):
        lits = [X(v, w) for w in range(N) if w != v and X(v, w)]
        e = CardEnc.equals(lits=lits, bound=d, top_id=top, encoding=EncType.kmtotalizer); top = max(top, e.nv); cls += e.clauses
        for Y in range(b):
            ls = [X(v, w) for w in range(Y * s, (Y + 1) * s) if w != v and X(v, w)]
            for p, q in itertools.combinations(ls, 2): cls.append([-p, -q])
    if c4:
        for a, bb in itertools.combinations(range(N), 2):
            ws = []
            for c in range(N):
                if c in (a, bb) or not X(a, c) or not X(bb, c): continue
                top += 1; w = top; ws.append(w)
                cls.append([-X(a, c), -X(bb, c), w])        # w <- (ac & bc)
            if len(ws) > 1:
                e = CardEnc.atmost(lits=ws, bound=1, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cls += e.clauses
    out = []
    with Solver(name="glucose4", bootstrap_with=cls) as S:
        for _ in range(count):
            S.set_phases([v if rng.random() < 0.3 else -v for v in range(1, len(vid) + 1)])
            if not S.solve(): break
            m = set(S.get_model())
            E = {p for p, i in vid.items() if i in m}
            out.append(E)
            S.add_clause([-vid[p] for p in E])               # block this exact graph
    return out, N, blk, b

def build_G(E, N, blk, b, s):
    # vertices: 'x', ('u',X), ('f',v)
    adj = {"x": set()}
    for X in range(b): adj[("u", X)] = set()
    for v in range(N): adj[("f", v)] = set()
    def add(p, q): adj[p].add(q); adj[q].add(p)
    for X in range(b): add("x", ("u", X))
    for p in range(b // 2): add(("u", 2 * p), ("u", 2 * p + 1))
    for v in range(N): add(("u", blk[v]), ("f", v))
    for u, v in E: add(("f", u), ("f", v))
    return adj

def has_c4(adj):
    V = list(adj)
    for a, c in itertools.combinations(V, 2):
        if len(adj[a] & adj[c]) >= 2: return True
    return False

def conds(E, N, blk, b):
    adj = {v: set() for v in range(N)}
    for u, v in E: adj[u].add(v); adj[v].add(u)
    i_ = all(len(adj[a] & adj[c]) <= 1 for a, c in itertools.combinations(range(N), 2))
    ii = all(blk[v] != (blk[u] ^ 1) for u, v in E)
    iii = all(sum(1 for w in adj[v] if blk[w] == Y) <= 1 for v in range(N) for Y in range(b))
    return i_, ii, iii, adj

MUTATE = False
def check_lemma(E, N, blk, b, d, s, c4):
    i_, ii, iii, adj = conds(E, N, blk, b)
    assert ii and iii and all(len(adj[v]) == d for v in range(N)), "generator broke hypotheses"
    if c4: assert i_
    blocks = [[v for v in range(N) if blk[v] == X] for X in range(b)]
    nb = lambda v, Y: sum(1 for w in adj[v] if blk[w] == Y)
    Nm = [[0] * b for _ in range(b)]
    for u, v in E: Nm[blk[u]][blk[v]] += 1; Nm[blk[v]][blk[u]] += 1   # N[X][X] = 2 e(X)
    fails = []
    # step 1
    for z in range(N):
        avail = [Y for Y in range(b) if Y != (blk[z] ^ 1)]
        miss = [Y for Y in avail if nb(z, Y) == 0]
        if len(miss) != 1: fails.append(("step1", z, miss))
    # step 2
    for Y in range(b):
        missers = [z for z in range(N) if blk[z] != (Y ^ 1) and nb(z, Y) == 0]
        if len(missers) != s: fails.append(("step2", Y, len(missers)))
    G = build_G(E, N, blk, b, s)
    for Xb, Yb in itertools.permutations(range(b), 2):
        m = sum(1 for z in range(N) if nb(z, Xb) and nb(z, Yb))
        pred_m = d * s - Nm[Yb ^ 1][Xb] - Nm[Xb ^ 1][Yb]
        if MUTATE: pred_m = d * s - Nm[Yb][Xb] - Nm[Xb ^ 1][Yb ^ 1]          # wrong pairing (negative control)
        if m != pred_m: fails.append(("m-identity", Xb, Yb, m, pred_m))
        cod = [len(G[("f", a)] & G[("f", c)]) for a in blocks[Xb] for c in blocks[Yb]]
        if sum(cod) != m: fails.append(("step3-count", Xb, Yb, sum(cod), m))
        # common neighbours in G are far vertices (step 3's first sentence)
        for a in blocks[Xb]:
            for c in blocks[Yb]:
                if any(not (isinstance(w, tuple) and w[0] == "f") for w in G[("f", a)] & G[("f", c)]):
                    fails.append(("non-far common nbr", a, c))
        if c4:
            q = sum(1 for t in cod if t == 0)
            pred = s * s - d * s + Nm[Yb ^ 1][Xb] + Nm[Xb ^ 1][Yb]
            if MUTATE: pred = s * s - d * s + Nm[Yb][Xb] + Nm[Xb ^ 1][Yb ^ 1]
            if q != pred: fails.append(("q-identity", Xb, Yb, q, pred))
    return fails

def reduction_check(E, N, blk, b, s, rng, trials):
    """§1: G C4-free <=> (i)&(ii)&(iii). Tested on E and on mutations of E (degree of H irrelevant to the equivalence)."""
    bad = 0; seen = {"both": 0, "neither": 0}
    cur = set(E)
    allpairs = list(itertools.combinations(range(N), 2))
    for t in range(trials):
        Et = set(cur)
        for _ in range(rng.randint(0, 3)):
            p = rng.choice(allpairs)
            Et ^= {p}
        i_, ii, iii, _ = conds(Et, N, blk, b)
        g = not has_c4(build_G(Et, N, blk, b, s))
        if g != (i_ and ii and iii): bad += 1
        seen["both" if g else "neither"] += 1
    return bad, seen

if __name__ == "__main__":
    d, s, count = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    c4 = "--c4" in sys.argv
    MUTATE = "--mutate" in sys.argv
    globals()["MUTATE"] = MUTATE
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 1
    rng = random.Random(seed)
    Es, N, blk, b = gen(d, s, c4, rng, count)
    print(f"d={d} s={s} b={b} N={N} c4={'ON' if c4 else 'off'}: {len(Es)} instance(s)", flush=True)
    tot = 0; nonzero_q = set(); Nvals = set()
    ie = []; qs = set()
    for E in Es:
        ie.append(sum(1 for u, v in E if blk[u] == blk[v]))
        f = check_lemma(E, N, blk, b, d, s, c4)
        tot += len(f)
        if f: print("  FAIL", f[:4])
    rb, seen = (0, {})
    if c4 and Es:
        rb, seen = reduction_check(Es[0], N, blk, b, s, rng, 300)
    print(f"  internal edges per instance: min {min(ie) if ie else '-'} max {max(ie) if ie else '-'}")
    print(f"  lemma failures: {tot}   reduction-equivalence mismatches: {rb} {seen}")
