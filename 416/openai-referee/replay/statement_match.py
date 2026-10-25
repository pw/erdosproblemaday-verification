#!/usr/bin/env python3
# #416 / OpenAI family 24 (12:00Z erdos seat 2026-10-21): pp.all printouts of the COMPARATOR challenges
# (ComparatorChallenges/TotientAsymptotic: 4 theorems + 32 defs; ComparatorChallenges/TotientCompanionZero: companion_zero_case + 22 defs)
# vs the SOLUTION environment (OAI.NumberTheory.TotientAsymptotic.UnconditionalMain closure). Blocks delimited by '@@@ BEGIN <kind> <name>'
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
L = sys.argv[1] if len(sys.argv) > 1 else "logs"
a = open(f"{L}/ax.log").read(); c = open(f"{L}/cmp.log").read(); c2 = open(f"{L}/cmp2.log").read()
A, C, C2 = blocks(a), blocks(c), blocks(c2)
missing = False; allok = True; out = []
for cmpname, CB in (("TotientAsymptotic", C), ("TotientCompanionZero", C2)):
    nm = nmis = 0
    for k, y in CB.items():
        x = A.get(k)
        if x is None or not x[0] or not y[0]: missing = True
        ok = x is not None and x[0] == y[0] and x[0] != ""
        allok &= ok; nm += ok; nmis += (not ok)
        print(cmpname, k, "MATCH" if ok else "MISMATCH", "| lens", None if x is None else len(x[0]), len(y[0]))
        if k.split('.')[-1] in ("totient_asymptotic_formula","weighted_totient_asymptotic","weighted_totient_one_two","coefficient_nonnegative","companion_zero_case"):
            sax, cax = (x[1] if x else None), y[1]
            s_ok = sax == STD; c_ok = bool(cax) and "sorryAx" in cax
            allok &= s_ok and c_ok
            print("   solution axioms:", sorted(sax) if sax is not None else None, "| comparator axioms:", sorted(cax) if cax else cax)
    out.append(f"{cmpname}: {nm} MATCH / {nmis} MISMATCH")
for t in ["OAI.TotientAsymptotic.rho_mem", "OAI.TotientAsymptotic.seeds_one_two", "OAI.TotientAsymptotic.seed_least_preimage",
          "OAI.TotientAsymptotic.extractedStructureInput", "OAI.TotientAsymptotic.fordLemma26Input", "OAI.TotientAsymptotic.primeNumberTheoremInput",
          "OAI.TotientAsymptotic.ford_scale_lower", "OAI.TotientAsymptotic.ford_scale_upper", "OAI.TotientAsymptotic.fordScaleBounds"]:
    s = axes(a, t); out.append(f"{t} {'STD_AXIOMS' if s == STD else ('SUBSET_STD '+str(sorted(s)) if s is not None and s <= STD else 'NONSTD/MISSING '+str(s))}")
out.insert(0, "ALL_MATCH_STD_SORRYSEEN" if allok and not missing else ("MISSING" if missing else "FAIL"))
if len(sys.argv) <= 1: open("statement_match.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(2 if missing else (0 if allok else 1))
