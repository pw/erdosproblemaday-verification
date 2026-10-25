#!/usr/bin/env python3
# Family 191 / Erdős #507 (15:00Z erdos seat 2026-10-22). Second-level verdict over statement_match.py's blocks:
# a def block that differs ONLY by a leading '@[irreducible] ' is accepted as KERNEL-IDENTICAL iff the kernel-identity
# probes (probe/Kid_{Ax,Cmp}.lean -> logs/kid_{Ax,Cmp}.log) print identical kernel_hints, value_hash, type_hash and safety
# for that constant on both sides. Everything else must match textually, exactly as in statement_match.py.
# Exit 0 = all blocks MATCH or MATCH-UP-TO-ELAB-ATTRIBUTE (with kernel evidence) + std axioms + sorryAx seen; 1 = fail; 2 = missing.
import re, sys, json, importlib.util
L = sys.argv[1] if len(sys.argv) > 1 else "logs"
spec = importlib.util.spec_from_file_location("sm", "statement_match.py"); sm = importlib.util.module_from_spec(spec)
src = open("statement_match.py").read().split("import json")[0]  # reuse blocks()/STD only, not the main body
exec(src, sm.__dict__)
def kid(path):
    out = {}
    try: t = open(path).read()
    except FileNotFoundError: return None
    for m in re.finditer(r"@@KID (\S+) kernel_hints=(.+?) value_hash=(\d+) type_hash=(\d+) safety=(\S+) elab_status=(\S+)", t):
        out[m.group(1)] = (m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
    return out
P = json.load(open("probes.json"))
KA, KC = kid(f"{L}/kid_Ax.log"), kid(f"{L}/kid_Cmp.log")
missing = KA is None or KC is None; allok = True; rows = []
for cmpname in P:
    try:
        A = sm.blocks(open(f"{L}/ax_{cmpname}.log").read()); C = sm.blocks(open(f"{L}/cmp_{cmpname}.log").read())
    except FileNotFoundError:
        missing = True; continue
    want = set(P[cmpname][1]) | set(P[cmpname][2])
    if set(C) != want or not set(want) <= set(A): missing = True
    for k, y in C.items():
        x = A.get(k)
        if x is None or not x[0] or not y[0]: missing = True; continue
        if x[0] == y[0]: verdict = "MATCH"
        elif x[0].startswith("@[irreducible] ") and x[0][len("@[irreducible] "):] == y[0]:
            ka = (KA or {}).get(k); kc = (KC or {}).get(k)
            if ka and kc and ka[:4] == kc[:4]:
                verdict = f"MATCH-UP-TO-ELAB-ATTRIBUTE (kernel hints/value/type/safety identical: {ka[:4]}; elab status {ka[4]} vs {kc[4]})"
            else:
                verdict = "MISMATCH (attribute differs and no kernel evidence)"; allok = False
        else:
            verdict = "MISMATCH"; allok = False
        if y[1] is not None:
            s_ok = (x[1] == sm.STD); c_ok = bool(y[1]) and "sorryAx" in y[1]
            allok &= s_ok and c_ok
            verdict += f" | solution axioms {sorted(x[1]) if x[1] is not None else None} | comparator {sorted(y[1]) if y[1] else y[1]}"
        rows.append(f"{cmpname} {k} {verdict}")
head = "ALL_MATCH_KERNEL_STD_SORRYSEEN" if allok and not missing else ("MISSING" if missing else "FAIL")
print(head); print("\n".join(rows))
if len(sys.argv) <= 1: open("statement_match_v2.txt", "w").write(head + "\n" + "\n".join(rows) + "\n")
sys.exit(2 if missing else (0 if allok else 1))
