#!/usr/bin/env python3
"""Orbit control for the lex-leader symmetry-breaking clauses, per case, INDEPENDENT of the problem constraints.
For each symmetry-broken case: recompute G = Aut(N+) x Aut(N-) x Aut(N0) by brute force, draw random assignments of
the cross-part pair-state vector (one state per pair), enumerate each assignment's orbit under G (image = relabel
by the vertex permutation), take the lex-MIN member, and ask cadical whether the case's SB clauses (the clauses
appended to the plain CNF) are satisfiable with the cross vector pinned to it:
  (a) lex-min member            -> must be SAT   (the SB clauses keep one member of every orbit = losslessness)
  (b) lex-max / random non-min  -> must be UNSAT (otherwise the clauses are vacuous and prove nothing about losslessness)
Any (a) failure is a soundness bug (k(3,4)=21 would rest on an over-constrained CNF). Exit 1 on failure, 2 if nothing ran."""
import os, sys, json, random, itertools, subprocess, tempfile
os.environ.setdefault("ORDER", "21")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases_any import T, V, ORDER
assert ORDER == 21, ORDER
CADICAL = "/bin/cadical"
def solve(nv, clauses):
    with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
        f.write(f"p cnf {nv} {len(clauses)}\n" + "\n".join(" ".join(map(str, c)) + " 0" for c in clauses) + "\n"); path = f.name
    rc = subprocess.run([CADICAL, "-q", path], capture_output=True).returncode; os.unlink(path)
    return {10: "SAT", 20: "UNSAT"}.get(rc, f"rc{rc}")
def check_case(name, d="cases", draws=3, rng=random.Random(112)):
    p, q, r = int(name[1]), int(name[2]), int(name[3]); ti, tj, tk = [int(x[1:]) for x in name.split("_")[1:4]]
    out = list(range(1, 1 + p)); inn = list(range(1 + p, 1 + p + q)); non = list(range(1 + p + q, ORDER))
    var = V()
    for u, v in itertools.combinations(range(ORDER), 2): var.fwd(u, v); var.fwd(v, u); var.none(u, v)
    parts = [(out, T["N"][str(p)][ti]), (inn, T["N"][str(q)][tj]), (non, T["T"][str(r)][tk])]
    groups = []
    for verts, typ in parts:
        A = set((verts[a], verts[b]) for a, b in typ["arcs"])
        groups.append([dict(zip(verts, perm)) for perm in itertools.permutations(verts) if all((m[a], m[b]) in A for a, b in A for m in [dict(zip(verts, perm))])])
    G = [{**g1, **g2, **g3} for g1 in groups[0] for g2 in groups[1] for g3 in groups[2]]
    sb = json.load(open(os.path.join(d, name + ".sb.json")))
    assert [len(g) for g in groups] == sb["aut_sizes"], (name, [len(g) for g in groups], sb["aut_sizes"])
    pairs = [(u, v) for Pa, Pb in ((out, inn), (out, non), (inn, non)) for u in Pa for v in Pb]
    cross = [t for u, v in pairs for t in (("f", u, v), ("f", v, u), ("n", u, v))]
    def lit(t): return var.fwd(t[1], t[2]) if t[0] == "f" else var.none(t[1], t[2])
    assert len(cross) == sb["cross_vars"]
    # SB clauses = the clause lines appended after the plain CNF's own clauses
    plain_nc = int([l for l in open(os.path.join(d, name + ".cnf")) if l.startswith("p cnf")][0].split()[3])
    sbl = open(os.path.join(d, name + "_sb.cnf")).read().splitlines()
    hdr = [l for l in sbl if l.startswith("p cnf")][0]; nv_sb, nc_sb = map(int, hdr.split()[2:4])
    body = [l for l in sbl if l and not l.startswith("p") and not l.startswith("c")]
    assert len(body) == nc_sb and nc_sb - plain_nc == sb["extra_clauses"], (name, len(body), nc_sb, plain_nc, sb["extra_clauses"])
    extra = [list(map(int, l.split()[:-1])) for l in body[plain_nc:]]
    def image(x, m):  # relabel: the pair (u,v) in state s goes to the pair (m[u],m[v]) in state s
        y = {}
        for (u, v), s in x.items():
            a, b = m[u], m[v]
            if s == "n": y[(min(a, b), max(a, b))] = "n"
            elif s == "fwd": y[(min(a, b), max(a, b))] = "fwd" if a < b else "bwd"
            else: y[(min(a, b), max(a, b))] = "bwd" if a < b else "fwd"
        return y
    def vec(x):  # the cross vector of an assignment, as a 0/1 tuple in symbreak's variable order
        bits = []
        for u, v in pairs:
            s = x[(u, v)]; bits += [1 if s == "fwd" else 0, 1 if s == "bwd" else 0, 1 if s == "n" else 0]
        return tuple(bits)
    def units(x): return [[l if b else -l] for l, b in zip([lit(t) for t in cross], vec(x))]
    results = []
    for k in range(draws):
        x = {pr: rng.choice(["fwd", "bwd", "n"]) for pr in pairs}
        orbit = {}
        for m in G:
            y = image(x, m); orbit[vec(y)] = y
        vmin = min(orbit); vmax = max(orbit)
        ra = solve(nv_sb, extra + units(orbit[vmin]))
        rb = solve(nv_sb, extra + units(orbit[vmax])) if vmax != vmin else "n/a"
        others = [v for v in orbit if v != vmin]
        rc = solve(nv_sb, extra + units(orbit[rng.choice(others)])) if others else "n/a"
        ok = ra == "SAT" and rb in ("UNSAT", "n/a") and rc in ("UNSAT", "n/a")
        results.append((len(orbit), ra, rb, rc, ok))
    return results
if __name__ == "__main__":
    d = "cases"; names = sorted(f[:-len(".sb.json")] for f in os.listdir(d) if f.endswith(".sb.json") and f.startswith("p"))
    bad = 0; ran = 0
    for name in names:
        try:
            res = check_case(name, d)
        except Exception as e:
            print(f"{name}: ERROR {e!r}"); bad += 1; continue
        ran += len(res)
        for orb, ra, rb, rc, ok in res:
            if not ok: bad += 1
        flag = "ok" if all(r[4] for r in res) else "FAIL"
        print(f"{name}: |orbit|={[r[0] for r in res]} lexmin={[r[1] for r in res]} lexmax={[r[2] for r in res]} other={[r[3] for r in res]} {flag}")
    print(f"\ncases {len(names)}  draws {ran}  failures {bad}")
    sys.exit(2 if ran == 0 else (1 if bad else 0))
