#!/usr/bin/env python3
"""Referee's independent audit of a CNF emitted by h1cube.py (no code of theirs imported).
Spec rebuilt from the README alone:
  k in {5,7}; d=k-1, block size s=k-2, b=k+1 blocks (pairs 2p,2p+1); vertices 0..N-1, block of v = v // s.
  Edge variables = pairs (a<b) in different, non-paired blocks, numbered 1.. in lexicographic order.
  Case j (k=7): pairs p<j have e=(2,2), others (2,1); k=5: e=1 everywhere. Internal edges = local (0,1),(2,3) / (0,1).
  Residual group generators = ALL within-block transpositions that map the fixed internal edge set onto itself
  (found by brute force here, not copied from their list).
Checks:
  A. header/clause count sanity; variable count.
  B. every clause over edge variables only is all-negative and its edge set, together with the fixed internal edges,
     contains a forbidden configuration (vertex with 2 nbrs in one block, or a pair with 2 common nbrs) => implied.
  C. (C4 variants) the set of C4-type clauses equals the set of ALL potential 4-cycles (computed independently).
  D. semantic equivalence on a pool of full edge assignments: CNF(assumptions) SAT  <=>  my predicate
     (degrees, <=1 per block, [codegree<=1], [Lemma D cross constraints], [lex-leader X <=lex pi X computed DIRECTLY
     in row-major order over all vertex pairs, constants included]).
Usage: audit_cnf.py file.cnf k j c4(0/1) derived(0/1) sb(0/1) [pool_size] [--mutate-sb|--mutate-extra|--mutate-dropc4]"""
import itertools, random, sys
from pysat.solvers import Solver

path, k, j, C4, DER, SB = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), *[sys.argv[i] == "1" for i in (4, 5, 6)]
POOL = int(sys.argv[7]) if len(sys.argv) > 7 and not sys.argv[7].startswith("--") else 200
MUT = [a for a in sys.argv if a.startswith("--mutate")]
rng = random.Random(7)
d, s, b = k - 1, k - 2, k + 1; N = b * s
blk = [v // s for v in range(N)]
P = lambda X: X ^ 1
if k == 7: E = sum(([2, 2] if p < j else [2, 1] for p in range(b // 2)), [])
else: E = [1] * b
fixed = set()
for X in range(b):
    for t in range(E[X]): fixed.add((X * s + 2 * t, X * s + 2 * t + 1))
free = [(u, v) for u, v in itertools.combinations(range(N), 2) if blk[u] != blk[v] and blk[v] != P(blk[u])]
vid = {p: i + 1 for i, p in enumerate(free)}; nvar = len(free)
edge_of = {i: p for p, i in vid.items()}

# ---- parse
hdr = None; clauses = []; cur = []
for line in open(path):
    if line.startswith("p cnf"): hdr = tuple(map(int, line.split()[2:4])); continue
    if line.startswith("c") or not line.strip(): continue
    for t in line.split():
        t = int(t)
        if t == 0: clauses.append(cur); cur = []
        else: cur.append(t)
assert not cur
report = []
report.append(f"A. header {hdr}, parsed {len(clauses)} clauses, edge vars {nvar}")
if hdr[1] != len(clauses): report.append("   !! clause count mismatch")

if "--mutate-sb" in MUT:          # flip one lex clause (-eq,-a,b) -> (-eq,a,-b): audit must notice
    for c in clauses:
        if len(c) == 3 and sum(1 for l in c if abs(l) <= nvar) == 2 and c[0] < 0 and abs(c[0]) > nvar:
            c[1], c[2] = -c[1], -c[2]; report.append(f"   MUTATION: flipped lex clause -> {c}"); break
if "--mutate-extra" in MUT:       # add a pure-edge clause that is NOT implied
    a, bb = vid[free[0]], vid[free[-1]]
    clauses.append([-a, -bb]); report.append(f"   MUTATION: added [-{a},-{bb}]")
if "--mutate-dropc4" in MUT:      # drop one C4 clause
    for i, c in enumerate(clauses):
        if len(c) >= 3 and all(l < 0 and -l <= nvar for l in c):
            tgt = frozenset(c); n0 = len(clauses)
            clauses[:] = [cc for cc in clauses if frozenset(cc) != tgt]
            report.append(f"   MUTATION: dropped all {n0 - len(clauses)} copies of {c}"); break

def adjacency(edges):
    adj = [set() for _ in range(N)]
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    return adj

# ---- B: pure edge clauses
pure = [c for c in clauses if all(abs(l) <= nvar for l in c)]
nonneg = [c for c in pure if any(l > 0 for l in c)]
c4like = []; blockpairs = 0; bad = []
for c in pure:
    if any(l > 0 for l in c): continue
    S = [edge_of[-l] for l in c]
    adj = adjacency(list(fixed) + S)
    VS = {u for e in S for u in e}
    VS |= {w for u in list(VS) for w in adj[u]}      # a C4 in S+fixed lives on V(S) + fixed partners (fixed = matching)
    two_in_block = any(sum(1 for w in adj[v] if blk[w] == Y) >= 2 for v in VS for Y in range(b))
    cod2 = any(len(adj[x] & adj[y]) >= 2 for x, y in itertools.combinations(sorted(VS), 2)) if len(S) >= 2 else False
    if len(S) == 2 and two_in_block: blockpairs += 1
    elif cod2: c4like.append(frozenset(c))
    elif two_in_block: blockpairs += 1
    else: bad.append(c)
report.append(f"B. pure-edge clauses {len(pure)}: block(<=1/block) {blockpairs}, C4 {len(c4like)}, with positive lits {len(nonneg)}, NOT IMPLIED {len(bad)} {bad[:3]}")

# ---- C: C4 clause set vs all potential 4-cycles
if C4:
    pot = lambda u, v: (min(u, v), max(u, v)) in fixed or (min(u, v), max(u, v)) in vid
    lit = lambda u, v: None if (min(u, v), max(u, v)) in fixed else -vid[(min(u, v), max(u, v))]
    expect = set()
    for a, bb in itertools.combinations(range(N), 2):
        cs = [c for c in range(N) if c not in (a, bb) and pot(a, c) and pot(bb, c)]
        for c1, c2 in itertools.combinations(cs, 2):
            ls = [lit(a, c1), lit(bb, c1), lit(a, c2), lit(bb, c2)]
            expect.add(frozenset(l for l in ls if l is not None))
    got = set(c4like)
    # a C4 clause may legitimately be dominated (subsumed) by a block clause; report exact-set differences
    report.append(f"C. potential 4-cycles {len(expect)}; C4 clauses (distinct) {len(got)}; missing {len(expect - got)}; extra {len(got - expect)}")

# ---- D: semantic equivalence on a pool
def trans_list():
    out = []
    for X in range(b):
        L = range(X * s, (X + 1) * s)
        for u, v in itertools.combinations(L, 2):
            pi = list(range(N)); pi[u], pi[v] = v, u
            img = {(min(pi[a], pi[c]), max(pi[a], pi[c])) for a, c in fixed}
            if img == fixed: out.append(pi)
    return out
TR = trans_list()
order = list(itertools.combinations(range(N), 2))         # row-major over the upper triangle, ALL pairs
def pred(edges, why=False):
    adj = adjacency(list(fixed) + list(edges))
    if any(len(adj[v]) != d for v in range(N)): return "deg"
    if any(sum(1 for w in adj[v] if blk[w] == Y) > 1 for v in range(N) for Y in range(b)): return "block"
    if C4 and any(len(adj[x] & adj[y]) > 1 for x, y in itertools.combinations(range(N), 2)): return "c4"
    if DER:
        Nm = [[0] * b for _ in range(b)]
        for u, v in edges: Nm[blk[u]][blk[v]] += 1; Nm[blk[v]][blk[u]] += 1
        for X, Y in itertools.combinations(range(b), 2):
            if Y != P(X) and Nm[P(X)][Y] + Nm[X][P(Y)] < d - 1: return "lemmaD"
    if SB:
        A = lambda u, v: v in adj[u]
        for pi in TR:
            for (u, v) in order:
                x0, x1 = A(u, v), A(pi[u], pi[v])
                if x0 != x1:
                    if x0 > x1: return "lex"
                    break
    return "ok"

S = Solver(name="cadical153", bootstrap_with=clauses)
def cnf_accepts(edges):
    es = set(edges)
    return S.solve(assumptions=[vid[p] if p in es else -vid[p] for p in free])
def sample_models(cl, n):
    out = []
    with Solver(name="glucose4", bootstrap_with=cl) as T:
        for _ in range(n):
            T.set_phases([v if rng.random() < 0.2 else -v for v in range(1, nvar + 1)])
            if not T.solve(): break
            m = set(T.get_model()); es = [p for p in free if vid[p] in m]; out.append(es)
            T.add_clause([-vid[p] for p in es])
    return out
# seed models: from THIS cnf minus C4 clauses (C4-on has no models), and from the same cnf with SB / LemmaD
# aux-clauses removed is not possible syntactically, so instead the caller supplies sibling CNFs via env.
import os
seeds = []; seeds_ld = []
for sib in os.environ.get("SIBLINGS", "").split(":"):
    if not sib: continue
    cl = []; cur = []
    for line in open(sib):
        if line[0] in "pc" or not line.strip(): continue
        for t in map(int, line.split()):
            if t == 0: cl.append(cur); cur = []
            else: cur.append(t)
    seeds += sample_models(cl, max(4, POOL // 20))
# targeted Lemma D boundary assignments: models of a no-derived sibling + (sum <= d-2) or (sum == d-1) on ONE pair
from pysat.card import CardEnc, EncType
if os.environ.get("TARGET_LD"):
    cl0 = []; cur = []
    for line in open(os.environ["TARGET_LD"]):
        if line[0] in "pc" or not line.strip(): continue
        for t in map(int, line.split()):
            if t == 0: cl0.append(cur); cur = []
            else: cur.append(t)
    top0 = max(abs(l) for c in cl0 for l in c)
    for X, Y in itertools.combinations(range(b), 2):
        if Y == P(X): continue
        lits = [vid[(min(u, v), max(u, v))] for u in range(P(X) * s, P(X) * s + s) for v in range(Y * s, Y * s + s)] + \
               [vid[(min(u, v), max(u, v))] for u in range(X * s, X * s + s) for v in range(P(Y) * s, P(Y) * s + s)]
        for kind in ("below", "at"):
            enc = CardEnc.atmost(lits=lits, bound=d - 2, top_id=top0, encoding=EncType.totalizer) if kind == "below" else \
                  CardEnc.equals(lits=lits, bound=d - 1, top_id=top0, encoding=EncType.totalizer)
            got = sample_models(cl0 + enc.clauses, 1)
            for es in got: seeds_ld.append((kind, es))
pool = [("LD-" + kind, es) for kind, es in seeds_ld]
for es in seeds:
    pool.append(("model", es))
    es_set = set(es)
    for pi in rng.sample(TR, min(4, len(TR))):        # transposed model (tests lex)
        pool.append(("pi", [tuple(sorted((pi[u], pi[v]))) for u, v in es]))
    for _ in range(6):                                 # degree-preserving 2-switches (tests block/LemmaD/lex)
        e1, e2 = rng.sample(es, 2); (a, bb), (c, dd) = e1, e2
        if rng.random() < 0.5: c, dd = dd, c
        n1, n2 = tuple(sorted((a, c))), tuple(sorted((bb, dd)))
        if n1 in vid and n2 in vid and n1 not in es_set and n2 not in es_set and len({a, bb, c, dd}) == 4:
            pool.append(("2sw", [e for e in es if e not in (e1, e2)] + [n1, n2]))
    e = rng.choice(free); pool.append(("flip", list(es_set ^ {e})))
    for _ in range(3):                                 # random element of the residual group (mixed lex verdicts)
        g = list(range(N))
        for _ in range(rng.randint(1, 6)):
            pi = rng.choice(TR); g = [pi[g[v]] for v in range(N)]
        pool.append(("rand-g", [tuple(sorted((g[u], g[v]))) for u, v in es]))
cnt = {}; mism = []
for tag, es in pool[:POOL * 3 + 100]:
    p = pred(es); c = cnf_accepts(es)
    cnt[(tag, p, c)] = cnt.get((tag, p, c), 0) + 1
    if c != (p == "ok"): mism.append((tag, p, c))
report.append(f"D. pool {min(len(pool), POOL*3+100)} assignments; mismatches {len(mism)} {mism[:5]}")
report.append("   (tag, my-verdict, cnf-accepts): " + ", ".join(f"{k_}={v}" for k_, v in sorted(cnt.items())))
report.append(f"   residual transpositions (mine, brute force): {len(TR)}")
if os.environ.get("DIFF_NOC4"):
    from collections import Counter
    sib = []; cur = []
    for line in open(os.environ["DIFF_NOC4"]):
        if line[0] in "pc" or not line.strip(): continue
        for t in map(int, line.split()):
            if t == 0: sib.append(tuple(cur)); cur = []
            else: cur.append(t)
    A_, B_ = Counter(tuple(c) for c in clauses), Counter(sib)
    only_full = A_ - B_; only_sib = B_ - A_
    c4set = set(c4like)
    nonc4 = [c for c in only_full.elements() if frozenset(c) not in c4set]
    report.append(f"E. full minus drop-C4 sibling: {sum(only_full.values())} clauses, of which NOT a verified C4 clause: {len(nonc4)}; "
                  f"sibling clauses absent from full: {sum(only_sib.values())}")
print(f"== {os.path.basename(path)} k={k} j={j} c4={int(C4)} der={int(DER)} sb={int(SB)} {' '.join(MUT)}")
print("\n".join(report), flush=True)
