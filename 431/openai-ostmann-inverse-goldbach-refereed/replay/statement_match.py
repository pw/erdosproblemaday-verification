#!/usr/bin/env python3
# Family 013 / Erdős #431 (06:00Z erdos seat 2026-10-23; copied from the family-21 matcher): comparators OstmannComplete (2 theorems + 5 defs) and OstmannPrimes (main) vs the solution envs OAI.NumberTheory.Ostmann.Complete / .Main.
# (ComparatorChallenges/ShortEgyptianFractions: main + 3 defs; ComparatorChallenges/EgyptianFractions: 9 theorems + 11 defs)
# vs the SOLUTION environments (OAI.NumberTheory.ShortEgyptian.Main / OAI.NumberTheory.EgyptianFractions.Main closures). Blocks delimited by '@@@ BEGIN <kind> <name>'
# markers the probes print themselves. Inside a block: whitespace collapsed, leading 'noncomputable '/'@[reducible] ' dropped, axiom lines
# removed and compared separately. Exit 0 = every block MATCH + solution theorems on exactly the 3 standard axioms + sorryAx seen on every
# comparator theorem; 1 otherwise; 2 = a block missing on either side (cannot see).
import re, sys
STD = {"propext", "Classical.choice", "Quot.sound"}
def blocks(t):
    out = {}
    parts = re.split(r"^@@@ (BEGIN \S+ \S+|END|EXTRA .*)$", t, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        tag, body = parts[i], parts[i + 1]
        if not tag.startswith("BEGIN"): continue
        name = tag.split()[2]
        ax = re.findall(r"'[^']+' depends on axioms: \[([^\]]*)\]", body, re.S)
        axs = None if not ax else set(x.strip().split('.{')[0] for x in ax[0].split(','))
        if re.search(r"does not depend on any axioms", body): axs = set()
        body = re.sub(r"'[^']+' (depends on axioms: \[[^\]]*\]|does not depend on any axioms)", "", body, flags=re.S)
        body = re.sub(r"(?m)^(@\[reducible\] )?(noncomputable )?", "", body)
        out[name] = (re.sub(r"\s+", " ", body).strip(), axs)
    return out
def axes(t, name):
    m = re.search(r"'%s' depends on axioms: \[([^\]]*)\]" % re.escape(name), t, re.S)
    return None if not m else set(x.strip().split('.{')[0] for x in m.group(1).split(','))
import json
P = json.load(open("probes.json"))
L = sys.argv[1] if len(sys.argv) > 1 else "logs"
missing = False; allok = True; out = []
for cmpname in P:
    axf, cmpf = f"ax_{cmpname}.log", f"cmp_{cmpname}.log"
    try:
        A, C = blocks(open(f"{L}/{axf}").read()), blocks(open(f"{L}/{cmpf}").read())
    except FileNotFoundError:
        missing = True; out.append(f"{cmpname}: LOG MISSING"); continue
    want = set(P[cmpname][1]) | set(P[cmpname][2])
    if not C or set(C) != want: missing = True; print(cmpname, "BLOCK SET", sorted(want - set(C)))
    nm = nmis = 0
    for k, y in C.items():
        x = A.get(k)
        if x is None or not x[0] or not y[0]: missing = True
        ok = x is not None and x[0] == y[0] and x[0] != ""
        allok &= ok; nm += ok; nmis += (not ok)
        print(cmpname, k, "MATCH" if ok else "MISMATCH", "| lens", None if x is None else len(x[0]), len(y[0]))
        if y[1] is not None:
            sax, cax = (x[1] if x else None), y[1]
            s_ok = sax == STD; c_ok = bool(cax) and "sorryAx" in cax
            allok &= s_ok and c_ok
            print("   solution axioms:", sorted(sax) if sax is not None else None, "| comparator axioms:", sorted(cax) if cax else cax)
    out.append(f"{cmpname}: {nm} MATCH / {nmis} MISMATCH")
out.insert(0, "ALL_MATCH_STD_SORRYSEEN" if allok and not missing else ("MISSING" if missing else "FAIL"))
if len(sys.argv) <= 1: open("statement_match.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(2 if missing else (0 if allok else 1))
