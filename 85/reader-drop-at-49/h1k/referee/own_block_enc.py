#!/usr/bin/env python3
"""Referee's own block-form encoder (k=5/7 or general d,s), independent of h1cube.py. No SB.
Options: fixed e-pattern + canonical internal matching (as README §3) or free internal edges; C4 on/off.
Used to (1) cross-check which Lemma-D sums are feasible without C4, (2) cross-check h1cube verdicts at k=5."""
import itertools
from pysat.card import CardEnc, EncType
def encode(d, s, E=None, c4=True, extra_pairsum=None):
    b = d + 2; N = b * s; blk = [v // s for v in range(N)]; P = lambda X: X ^ 1
    fixed = set()
    if E is not None:
        for X in range(b):
            for t in range(E[X]): fixed.add((X * s + 2 * t, X * s + 2 * t + 1))
    free = [(u, v) for u, v in itertools.combinations(range(N), 2)
            if blk[v] != P(blk[u]) and (E is None or blk[u] != blk[v])]
    vid = {p: i + 1 for i, p in enumerate(free)}; top = len(vid); cl = []
    def lit(u, v):
        p = (min(u, v), max(u, v))
        return "T" if p in fixed else vid.get(p)
    for v in range(N):
        fd = sum(1 for w in range(N) if w != v and lit(v, w) == "T")
        ls = [lit(v, w) for w in range(N) if w != v and isinstance(lit(v, w), int)]
        e = CardEnc.equals(lits=ls, bound=d - fd, top_id=top, encoding=EncType.cardnetwrk); top = max(top, e.nv); cl += e.clauses
        for Y in range(b):
            ls = [lit(v, w) for w in range(Y * s, Y * s + s) if w != v and lit(v, w) is not None]
            for p, q in itertools.combinations(ls, 2):
                c = [-x for x in (p, q) if x != "T"]
                assert c, "fixed edges violate block rule"
                cl.append(c)
    if c4:
        for a, bb in itertools.combinations(range(N), 2):
            cs = []
            for c in range(N):
                if c in (a, bb): continue
                la, lb = lit(a, c), lit(bb, c)
                if la is None or lb is None: continue
                cs.append([x for x in (la, lb) if x != "T"])
            for C1, C2 in itertools.combinations(cs, 2):
                cl.append([-x for x in C1 + C2])
    if extra_pairsum is not None:
        (X, Y), op, bound = extra_pairsum
        ls = [lit(u, v) for u in range(P(X) * s, P(X) * s + s) for v in range(Y * s, Y * s + s)] + \
             [lit(u, v) for u in range(X * s, X * s + s) for v in range(P(Y) * s, P(Y) * s + s)]
        f = CardEnc.atmost if op == "le" else CardEnc.atleast
        e = f(lits=ls, bound=bound, top_id=top, encoding=EncType.totalizer); top = max(top, e.nv); cl += e.clauses
    return cl, vid, fixed, N, blk
