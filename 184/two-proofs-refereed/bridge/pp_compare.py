#!/usr/bin/env python3
"""Compare the pp.all elaboration of Formal Conjectures' erdos_184 / IsCycleOrEdge / IsDecomposition
(printed in Coffey's environment from FC's own module: Lean 4.33.1, Mathlib 0df444a3, FC 2424bb48)
with our verbatim copies Bridge184.* (printed in OpenAI's environment: Lean 4.34.1, Mathlib d13f23b7).
Usage: pp_compare.py <coffey ourcheck.log> <BridgePP.log>.  Exit 0 iff statement + IsCycleOrEdge are identical
after namespace renaming AND IsDecomposition differs only by the known instance-path tokens (checked separately by
InstDefeq.lean in both environments). Exit 2 if a block cannot be found (cannot see)."""
import re, sys, difflib
c = open(sys.argv[1]).read(); o = open(sys.argv[2]).read()
def grab(t, pat):
    m = re.search(pat, t, re.M)
    if not m: print("CANNOT SEE: no block for", pat); sys.exit(2)
    rest = t[m.start():]
    stop = re.search(r"\n(?=/tmp|'|@\[|def |theorem |Note:|warning|maxrss_kb=)", rest[1:])
    return rest[: (stop.start() + 1) if stop else len(rest)]
def norm(s):
    s = (s.replace("Bridge184.IsCycleOrEdge", "Erdos184.IsCycleOrEdge")
          .replace("Bridge184.IsDecomposition", "SimpleGraph.IsDecomposition")
          .replace("Bridge184.erdos_184", "Erdos184.erdos_184"))
    return re.sub(r"\s+", " ", s).strip()
pairs = [("erdos_184 statement", r"^Erdos184\.erdos_184\.\{u_1\} :", r"^Bridge184\.erdos_184\.\{u_1\} :"),
         ("IsCycleOrEdge", r"^(@\[[^\]]*\]\s*)?def Erdos184\.IsCycleOrEdge", r"^(@\[[^\]]*\]\s*)?def Bridge184\.IsCycleOrEdge"),
         ("IsDecomposition", r"^(@\[[^\]]*\]\s*)?def SimpleGraph\.IsDecomposition", r"^(@\[[^\]]*\]\s*)?def Bridge184\.IsDecomposition")]
ALLOWED = {"@CompleteSemilatticeInf.toPartialOrder.{u_1}", "@CompletePartialOrder.toPartialOrder.{u_1}",
           "@CompleteLattice.toCompleteSemilatticeInf.{u_1}", "@CompleteLattice.toCompletePartialOrder.{u_1}",
           "@HeytingAlgebra.toOrderBot.{u_1}", "@CompletePartialOrder.toOrderBot.{u_1}", "@Order.Frame.toHeytingAlgebra.{u_1}",
           "@CompleteDistribLattice.toFrame.{u_1}", "@CompleteBooleanAlgebra.toCompleteDistribLattice.{u_1}",
           "@CompleteBooleanAlgebra.toCompleteLattice.{u_1}", "@CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra.{u_1}",
           "@Set.instCompleteAtomicBooleanAlgebra.{u_1}", "Set.{u_1}", "Sym2.{u_1}", "V", "(", ")"}
ok = True
for name, pc, po in pairs:
    a, b = norm(grab(c, pc)), norm(grab(o, po))
    if len(a) < 200 or len(b) < 200: print("CANNOT SEE: block too short", name); sys.exit(2)
    if a == b:
        print(f"IDENTICAL  {name}  ({len(a)} chars)"); continue
    ta = re.findall(r"[@\w.{}]+|[()]", a); tb = re.findall(r"[@\w.{}]+|[()]", b)
    diffs = [op for op in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes() if op[0] != "equal"]
    toks = set(ta[i] for op in diffs for i in range(op[1], op[2])) | set(tb[j] for op in diffs for j in range(op[3], op[4]))
    bad = toks - ALLOWED
    print(f"DIFFERS    {name}  ({len(a)} vs {len(b)} chars); differing tokens: {sorted(toks)}")
    for op in diffs: print("   ", op[0], " ".join(ta[op[1]:op[2]]), " ==> ", " ".join(tb[op[3]:op[4]]))
    if name != "IsDecomposition" or bad:
        ok = False; print("   NOT ALLOWED:", sorted(bad))
    else:
        print("   only Set (Sym2 V) PartialOrder/OrderBot instance paths differ -> see InstDefeq.lean (Iff.rfl in both environments)")
print("RESULT", "MATCH_MODULO_INSTANCE_PATHS" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
