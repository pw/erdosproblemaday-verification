#!/usr/bin/env python3
"""Lossless symmetry breaking for one order-N case: every automorphism σ of the FIXED out-type (acting on the
out-part's vertices), of the fixed in-type, and of the fixed non-tournament extends to an automorphism of the whole
case CNF (the definition-level constraints are vertex-symmetric, arcs to the root are uniform within a part, other
parts untouched). So the solution set is invariant under the group G = Aut(N+) x Aut(N-) x Aut(N0), and adding the
lex-leader constraints  x <=_lex σ(x)  for every σ ∈ G over the vector x of cross-part pair-state variables keeps at
least one solution per orbit (Crawford–Ginsberg–Luks–Roy 1996). Hence: sb-CNF UNSAT ⇒ case UNSAT; sb-CNF SAT ⇒ a
genuine witness (checked by check_witness.py as usual). The script VERIFIES each σ preserves the fixed arcs before
using it. Usage: symbreak_case.py <case_name> [cases_dir]   -> writes <case>_sb.cnf and <case>.sb.json"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases_any import PROFILES, T, V, ORDER   # same generator; honours ORDER env
name = sys.argv[1]; d = sys.argv[2] if len(sys.argv) > 2 else "cases"
p, q, r = int(name[1]), int(name[2]), int(name[3])
ti, tj, tk = [int(x[1:]) for x in name.split("_")[1:4]]
out = list(range(1, 1 + p)); inn = list(range(1 + p, 1 + p + q)); non = list(range(1 + p + q, ORDER))
var = V()
for u, v in itertools.combinations(range(ORDER), 2): var.fwd(u, v); var.fwd(v, u); var.none(u, v)
def arcs_of(verts, typ): return set((verts[a], verts[b]) for a, b in typ["arcs"])
parts = [(out, T["N"][str(p)][ti]), (inn, T["N"][str(q)][tj]), (non, T["T"][str(r)][tk])]
def automorphisms(verts, A):
    auts = []
    for perm in itertools.permutations(verts):
        m = dict(zip(verts, perm))
        if all((m[a], m[b]) in A for a, b in A): auts.append(m)
    return auts
groups = []
for verts, typ in parts:
    A = arcs_of(verts, typ); auts = automorphisms(verts, A)
    assert any(all(m[v] == v for v in verts) for m in auts), "identity missing?!"
    groups.append(auts)
sizes = [len(g) for g in groups]
# cross-part pair-state variable vector (fixed order)
cross = []
for Pa, Pb in ((out, inn), (out, non), (inn, non)):
    for u in Pa:
        for v in Pb: cross += [("f", u, v), ("f", v, u), ("n", u, v)]
def lit(t):
    return var.fwd(t[1], t[2]) if t[0] == "f" else var.none(t[1], t[2])
x = [lit(t) for t in cross]
index = {t: i for i, t in enumerate(cross)}
def apply(m, t):  # m: vertex map (identity outside its part)
    a, b = m.get(t[1], t[1]), m.get(t[2], t[2])
    if t[0] == "n": return ("n", min(a, b), max(a, b))
    return ("f", a, b)
src = open(os.path.join(d, name + ".cnf")).read().splitlines()
hdr = [l for l in src if l.startswith("p cnf")][0]; nv, nc = map(int, hdr.split()[2:4])
body = [l for l in src if not l.startswith("p") and not l.startswith("c")]
extra = []; top = nv
nelem = 0
for g1 in groups[0]:
    for g2 in groups[1]:
        for g3 in groups[2]:
            m = {**g1, **g2, **g3}
            if all(m[v] == v for v in m): continue
            nelem += 1
            # σ(x)_i = variable of the image of cross[i]
            sx = [lit(apply(m, t)) for t in cross]
            # lex-leader: x <=_lex sx with prefix-equality vars e_i
            e_prev = None
            for i in range(len(x)):
                xi, si = x[i], sx[i]
                if xi == si: continue   # fixed point: no constraint, equality holds; keep e_prev
                top += 1; e = top
                # (e_prev ∧ xi) → si   [x_i <= σ(x)_i given prefix equal]
                extra.append(([-e_prev] if e_prev else []) + [-xi, si])
                # e ↔ e_prev ∧ (xi ↔ si)
                extra.append([-e] + ([e_prev] if e_prev else [] and []))  if False else None
                if e_prev: extra.append([-e, e_prev])
                extra.append([-e, -xi, si]); extra.append([-e, xi, -si])
                extra.append(([-e_prev] if e_prev else []) + [xi, si, e])      # prefix equal ∧ both false → e
                extra.append(([-e_prev] if e_prev else []) + [-xi, -si, e])    # prefix equal ∧ both true  → e
                e_prev = e
extra = [c for c in extra if c]
with open(os.path.join(d, name + "_sb.cnf"), "w") as f:
    f.write(f"p cnf {top} {nc + len(extra)}\n" + "\n".join(body) + "\n" + "\n".join(" ".join(map(str, c)) + " 0" for c in extra) + "\n")
json.dump({"case": name, "aut_sizes": sizes, "group_order": sizes[0] * sizes[1] * sizes[2], "nonidentity_elems": nelem, "cross_vars": len(x), "extra_clauses": len(extra), "aux_vars": top - nv}, open(os.path.join(d, name + ".sb.json"), "w"))
print(f"{name}: |Aut| = {sizes} (group order {sizes[0]*sizes[1]*sizes[2]}), {nelem} lex-leader constraints over {len(x)} cross vars, +{len(extra)} clauses, +{top-nv} aux vars -> {name}_sb.cnf")
