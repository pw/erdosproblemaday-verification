"""Referee-2 harness: exec the REAL h1cube2.py source (verbatim, up to the solver call) with section markers
inserted, so tests can address the clauses each option adds.  Nothing in h1cube2.py is modified on disk."""
import os, sys, re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "h1cube2.py")


def build(argv, mutate=None):
    src = open(SRC).read()
    cut = src.index("fd, path = tempfile.mkstemp")
    src = src[:cut]
    marks = [
        ("# degrees: d = internal", "deg"),
        ("# codegree <= 1 (C4-free)", "c4"),
        ("# Lemma D cross constraints", "lemD"),
        ("# residual SB: transpositions", "tsb"),
        ("# SLOTS (implied", "slots"),
        ("# PH (implied", "ph"),
        ("npair = 0\nif PAIRSB:", "pairsb"),
        ("print(f\"k={k} case j={j} e={E}", "end"),
    ]
    for needle, name in marks:
        assert src.count(needle) == 1, needle
        src = src.replace(needle, f"_MARK({name!r})\n" + needle)
    # per-(w,Y) PH clause bookkeeping: record which clauses belong to which (w,Y) OR-clause
    needle = "            ors = [o for o in ors if o is not None]\n            cnf.append(ors); nph += 1\n"
    assert src.count(needle) == 1
    src = src.replace(needle, needle + "            _PHC[(w, Y)] = (_phstart, len(cnf.clauses))\n")
    needle2 = "            if Y == blk[w]:\n                continue\n            ors = []\n"
    assert src.count(needle2) == 1
    src = src.replace(needle2, needle2 + "            _phstart = len(cnf.clauses)\n")
    if mutate:
        for old, new in mutate:
            assert src.count(old) == 1, ("mutation anchor not unique/absent", old)
            src = src.replace(old, new)
    ns = {"__name__": "h1cube2_exec", "__file__": SRC}
    M = {}
    ns["_PHC"] = {}

    def _MARK(name):
        M[name] = len(ns["cnf"].clauses) if "cnf" in ns else 0
    ns["_MARK"] = _MARK
    old = sys.argv
    sys.argv = ["h1cube2.py"] + list(argv)
    try:
        exec(compile(src, SRC, "exec"), ns)
    finally:
        sys.argv = old
    ns["_M"] = M
    return ns


def section(ns, a, b):
    M = ns["_M"]
    return ns["cnf"].clauses[M[a]:M[b]]
