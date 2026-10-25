#!/usr/bin/env python3
# #968 / OpenAI family 26 (06:00Z erdos seat 2026-10-21): compare pp.all printouts of the COMPARATOR challenge
# (ComparatorChallenges/PrimeGaps, statement with sorry) vs the SOLUTION module (OAI.NumberTheory.PrimeGaps.RatioCorollary):
# the theorem type + all six definitions it unfolds through. Blocks are delimited by explicit '@@@ BEGIN <kind> <name>' markers
# printed by the probes themselves (no regex guessing at heads). Inside a block: whitespace collapsed, a leading 'noncomputable '
# and '@[reducible] ' dropped (compiler/elaborator annotations, not kernel terms), axiom lines removed and compared separately.
# Exit 0 = all MATCH + STD_AXIOMS + CMP_SORRY_SEEN; 1 otherwise; 2 = a block missing on either side (cannot see).
import re, sys
STD = {"propext", "Classical.choice", "Quot.sound"}
T = "OAI.Problem344.large_gaps_and_ratio_density"
DEFS = ["OAI.LargePrimeGaps.prime", "OAI.LargePrimeGaps.largeGapIndices", "OAI.Problem344.primeAt",
        "OAI.Problem344.initialCount", "OAI.Problem344.lowerAsymptoticDensity", "OAI.Problem344.ratioIncreaseIndices"]
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
a = open(sys.argv[1] if len(sys.argv) > 1 else "logs/ax.log").read()
c = open(sys.argv[2] if len(sys.argv) > 2 else "logs/cmp.log").read()
A, C = blocks(a), blocks(c)
res, missing = [], False
for k in [T] + DEFS:
    x, y = A.get(k), C.get(k)
    if x is None or y is None or not x[0] or not y[0]: missing = True
    ok = x is not None and y is not None and x[0] == y[0] and x[0] != ""
    res.append(ok)
    print(k, "MATCH" if ok else "MISMATCH", "| lens", None if x is None else len(x[0]), None if y is None else len(y[0]))
sax, cax = A.get(T, (None, None))[1], C.get(T, (None, None))[1]
print("solution axioms:", sax, "| comparator axioms:", cax)
out = ["MATCH" if all(res) else "MISMATCH", "STD_AXIOMS" if sax == STD else "NONSTD",
       "CMP_SORRY_SEEN" if cax and "sorryAx" in cax else "CMP_SORRY_NOT_SEEN"]
for t in ["OAI.LargePrimeGaps.main", "OAI.LargePrimeGaps.bombieriVinogradov", "OAI.LargePrimeGaps.siegelWalfisz",
          "OAI.Problem344.positive_lower_density_prime_ratio_increases"]:
    s = axes(a, t); out.append(f"{t} {'STD_AXIOMS' if s == STD else ('SUBSET_STD' if s is not None and s <= STD else 'NONSTD/MISSING')}")
if len(sys.argv) <= 1: open("statement_match.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(2 if missing else (0 if out[:3] == ["MATCH", "STD_AXIOMS", "CMP_SORRY_SEEN"] else 1))
