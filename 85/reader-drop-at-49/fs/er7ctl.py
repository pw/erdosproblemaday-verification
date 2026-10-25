#!/usr/bin/env python3
"""End-to-end positive control for fsenc (R1 + SB) on a graph where R1's conclusion is TRUE:
ER(7), the polarity graph of PG(2,7): 57 vertices, C4-free, absolute points degree 7, others degree 8.
For a non-absolute x whose polar line x^perp is a passant (no absolute point), N(x) induces a perfect matching.
Instance: S = everything except a free set Fr (N(x) + 12 more), all S-edges fixed, x in S, R1 for x, SB on.
ER(7) restricted is a solution => must be SAT; every model is re-checked independently (degrees, codegree,
R1 for x, lex order).  Mutation: R1 demanded for a SECANT vertex y whose two absolute neighbours have no partner
in N(y) in ER(7) -- its models (if any) must differ from ER(7) there; reported, not asserted."""
import itertools, random, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fsenc, c4cnf
q = 7
pts = []
for a in range(q):
    for b in range(q):
        for c in range(q):
            v = (a, b, c)
            if v == (0, 0, 0): continue
            # normalise: first nonzero coordinate = 1
            f = next(z for z in v if z)
            inv = pow(f, q - 2, q)
            w = tuple(z * inv % q for z in v)
            if w not in pts: pts.append(w)
assert len(pts) == 57
dot = lambda u, v: sum(x * y for x, y in zip(u, v)) % q
E = [(i, j) for i, j in itertools.combinations(range(57), 2) if dot(pts[i], pts[j]) == 0]
degs, mc = c4cnf.check_graph(57, E); assert mc <= 1 and sorted(set(degs)) == [7, 8]
adj = {v: set() for v in range(57)}
for i, j in E: adj[i].add(j); adj[j].add(i)
absolute = {i for i in range(57) if dot(pts[i], pts[i]) == 0}
def pm(x):  # does N(x) induce a perfect matching?
    return all(len(adj[u] & adj[x]) == 1 for u in adj[x])
passant = [x for x in range(57) if x not in absolute and not (adj[x] & absolute)]
secant = [x for x in range(57) if x not in absolute and len(adj[x] & absolute) == 2]
assert passant and all(pm(x) for x in passant) and not any(pm(y) for y in secant)
KISSAT = str(Path.home() / "MathDyad/tools/kissat/build/kissat")
def run(name, x, Fr, highs):
    S = [v for v in range(57) if v not in Fr]
    fixed = [e for e in E if e[0] in S or e[1] in S]
    target = {v: degs[v] for v in Fr}
    cnf, var, F, adjS, st, cls = fsenc.build(57, S, fixed, target, highs=highs, sb="all", r1=True)
    path = f"/tmp/erdos85-fs/{name}.cnf"; cnf.to_file(path)
    for s in ([KISSAT, "-q"], ["/usr/bin/cadical", "-q"]):
        out = subprocess.run(["timeout", "1800"] + s + [path], capture_output=True, text=True).stdout
        v = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "UNKNOWN"
        note = ""
        if v == "SAT":
            model = [int(t) for l in out.splitlines() if l.startswith("v ") for t in l[2:].split()]
            ed = fixed + c4cnf.decode(model, var)
            d2, mc2 = c4cnf.check_graph(57, ed)
            a2 = {u: set() for u in range(57)}
            for i, j in ed: a2[i].add(j); a2[j].add(i)
            r1ok = all(all(len(a2[v] & a2[h]) == 1 for v in range(57) if v != h) for h in highs)  # R1 + R1b
            note = (f"degrees_ok={all(d2[u]==degs[u] for u in range(57))} maxcodeg={mc2} R1_R1b_ok={r1ok} "
                    f"lex_ok={fsenc.lex_ok(a2, cls, 57)} same_as_ER7={sorted(ed)==sorted(E)}")
        print(name, s[0].split('/')[-1], v, f"free={len(Fr)} classes={st['sb_classes']} r1={st['r1_clauses']}", note, flush=True)
random.seed(20261019)
x = passant[0]
others = [v for v in range(57) if v != x and v not in adj[x]]
for trial in range(3):
    Fr = sorted(adj[x] | set(random.sample(others, 12)))
    run(f"er7_pass_{trial}", x, Fr, [x])
y = secant[0]
others = [v for v in range(57) if v != y and v not in adj[y]]
Fr = sorted(adj[y] | set(random.sample(others, 12)))
run("er7_MUT_secant_r1", y, Fr, [y])
