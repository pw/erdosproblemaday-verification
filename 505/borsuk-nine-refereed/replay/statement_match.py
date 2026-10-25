#!/usr/bin/env python3
# #505: compare pp.all printouts of the COMPARATOR challenge (ComparatorChallenges/BorsukNine, statement with sorry) vs the SOLUTION
# module (OAI.Geometry.Borsuk.Main): theorem type + every definition it unfolds through. Heads normalised (leading @ dropped, '@[reducible] '
# dropped, .{u} dropped). Prints MATCH/MISMATCH per item, STD_AXIOMS/NONSTD (solution), CMP_SORRY_SEEN/NOT_SEEN (comparator).
import re, sys
STD = {"propext", "Classical.choice", "Quot.sound"}
P = "OAI.BorsukNine."
DEFS = ["projector", "projectorSet", "traceOneSymmetric", "HasTenSmallCover", "Vector4", "Matrix4"]
def blocks(t):
    t = re.sub(r"^@\[reducible\] ", "", t, flags=re.M)
    HEAD = re.compile(r"^(def \S+|@?%s\w+(?= :))" % re.escape(P), re.M)
    ms = list(HEAD.finditer(t)); out = {}
    for m, nxt in zip(ms, ms[1:] + [None]):
        seg = t[m.start(): nxt.start() if nxt else len(t)]
        h = m.group(1).lstrip('@')
        if h.startswith('def '): h = re.sub(r"\.\{[^}]*\}$", "", h)
        seg = re.split(r"\n'[^']+' depends on axioms", seg)[0]
        out[h] = re.sub(r"\s+", " ", seg.lstrip('@')).strip()
    return out
def axset(t, name):
    m = re.search(r"'%s' depends on axioms: \[([^\]]*)\]" % re.escape(name), t, re.S)
    return None if not m else set(x.strip().split('.{')[0] for x in m.group(1).split(','))
a = open(sys.argv[1] if len(sys.argv) > 1 else "logs/ax.log").read(); c = open(sys.argv[2] if len(sys.argv) > 2 else "logs/cmp.log").read()
A, C = blocks(a), blocks(c); res = []
for k in [P + "main_theorem"] + ["def " + P + d for d in DEFS]:
    x = A.get(k); y = C.get(k); ok = x is not None and x == y; res.append(ok)
    print(k, "MATCH" if ok else "MISMATCH", "| lens", None if x is None else len(x), None if y is None else len(y))
ax = axset(a, P + "main_theorem"); cax = axset(c, P + "main_theorem")
print("solution axioms:", ax, "comparator axioms:", cax)
out = ["MATCH" if all(res) else "MISMATCH", "STD_AXIOMS" if ax == STD else "NONSTD", "CMP_SORRY_SEEN" if cax and "sorryAx" in cax else "CMP_SORRY_NOT_SEEN"]
for t in ["euclidean_nine_counterexample", "no_admissible_ten", "cover_to_admissible", "FiniteObstruction.no_ten_system"]:
    s = axset(a, P + t); out.append(f"{t} {'STD_AXIOMS' if s == STD else ('SUBSET_STD' if s is not None and s <= STD else 'NONSTD/MISSING')}")
if len(sys.argv) <= 1: open("statement_match.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
