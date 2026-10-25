#!/usr/bin/env python3
"""From-scratch encoding v2 for #85's order-49 strata (our own; extends ../h9/c4cnf.py without modifying it).

Adds to c4cnf.build (exact low degrees + codegree <= 1 everywhere):
 R1 (redundant, hand-proved): for every high vertex x (degree 8), N(x) induces a PERFECT matching.
    Proof: x has 8 neighbours, each of degree 7 (highs are pairwise non-adjacent), and C4-freeness makes the
    sets N(u) \\ N[x] (u in N(x)) pairwise disjoint and disjoint from N[x]; so 49 >= 1 + 8 + sum_u (6 - m_u)
    = 57 - 2|M| where M is the matching N(x) induces (C4-free => induced subgraph on N(x) has max degree 1).
    Hence |M| >= 4 = 8/2.  c4cnf already has "at most one"; R1 adds "at least one" per u in N(x).
 SB (symmetry breaking, lex-leader): free vertices i<j with identical fixed neighbourhood and target degree are
    interchangeable (the transposition (i j) maps the formula, incl. R1, to itself).  Under the row-major order of
    the upper-triangle edge variables, the lex-leader constraint X <=lex (i j)X is exactly
    row_i <=lex row_j over columns k not in {i,j} in increasing k (0 < 1).  Lex-leader constraints for any set of
    group elements under one variable order are jointly sound (the lex-least member of each orbit satisfies all).
"""
import itertools, sys
from pathlib import Path
sys.path.insert(0, "/home/exedev/MathDyad/erdos85/h9")
import c4cnf
DEGH = 8


def classes_of(n, F, adjS, target):
    key = {}
    for v in F:
        key.setdefault((frozenset(adjS[v]), target[v]), []).append(v)
    return [sorted(c) for c in key.values() if len(c) > 1]


def build(n, S, fixed, target, highs=(), sb="all", r1=True, r1b=True, hdeg=8):
    cnf, var, F, adjS = c4cnf.build(n, S, fixed, target)
    def x(a, b):
        return var[(a, b) if a < b else (b, a)]
    top = max([cnf.nv] + [abs(l) for c in cnf.clauses for l in c])
    stats = {"base_clauses": len(cnf.clauses)}
    if r1:
        nr = 0
        for h in highs:
            N = sorted(adjS[h])
            assert len(N) == hdeg and all(u in set(F) for u in N), (h, N)
            for u in N:
                cnf.append([x(u, w) for w in N if w != u]); nr += 1
        stats["r1_clauses"] = nr
    if r1b:
        # R1b (redundant, hand-proved): for high x, EVERY vertex v != x has exactly one neighbour in N(x).
        # Proof: the 2-walks x-u-v (u in N(x), v != x) number sum_u (deg u - 1) = 8*6 = 48 = |V \ {x}|, and
        # C4-freeness makes their endpoints distinct, so each v != x is the endpoint of exactly one.
        # (v in N(x): that is R1.)  Here: v outside N[x]; free v gets a clause, fixed v is asserted.
        nb = 0
        Fs = set(F)
        for h in highs:
            N = sorted(adjS[h])
            for v in range(n):
                if v == h or v in adjS[h]:
                    continue
                fixedhits = [u for u in N if u in adjS[v]]   # fixed edges v-u (v in S)
                if v in Fs:
                    cnf.append([x(v, u) for u in N if u != v]); nb += 1
                else:
                    assert len(fixedhits) == 1, ("R1b fixed", h, v, fixedhits)
        stats["r1b_clauses"] = nb
    cls = classes_of(n, F, adjS, target) if sb else []
    nsb = 0
    for C in cls:
        pairs = list(zip(C, C[1:])) if sb == "consecutive" else list(itertools.combinations(C, 2))
        for i, j in pairs:
            cols = [k for k in range(n) if k not in (i, j) and k in set(F)]
            e_prev = None
            for p, k in enumerate(cols):
                a, b = x(i, k), x(j, k)
                pre = [] if e_prev is None else [-e_prev]
                cnf.append(pre + [-a, b]); nsb += 1
                if p < len(cols) - 1:
                    top += 1; e = top
                    cnf.append(pre + [a, b, e]); cnf.append(pre + [-a, -b, e]); nsb += 2
                    e_prev = e
    stats["sb_classes"] = [len(C) for C in cls]; stats["sb_clauses"] = nsb
    return cnf, var, F, adjS, stats, cls


def lex_ok(adj, cls, n):
    """Independent check that a graph (adjacency sets) satisfies every SB constraint."""
    for C in cls:
        for i, j in itertools.combinations(C, 2):
            ri = [1 if k in adj[i] else 0 for k in range(n) if k not in (i, j)]
            rj = [1 if k in adj[j] else 0 for k in range(n) if k not in (i, j)]
            if ri > rj:
                return False
    return True


def stratum(h, T):
    """hrun.py's normalisation (README): blocks = triples of T, uncovered H-pairs, s(x)=9-h+r3(x) singles, empties."""
    H = list(range(h))
    T = [tuple(b) for b in T]
    covered = {frozenset(p) for b in T for p in itertools.combinations(b, 2)}
    Pairs = [p for p in itertools.combinations(H, 2) if frozenset(p) not in covered]
    r3 = {x: sum(x in b for b in T) for x in H}
    sing = [(x,) for x in H for _ in range(9 - h + r3[x])]
    n0 = 49 - h - len(T) - len(Pairs) - len(sing)
    assert n0 >= 0
    blocks = T + Pairs + sing + [()] * n0
    fixed = [(x, h + i) for i, b in enumerate(blocks) for x in b]
    assert all(sum(1 for a, _ in fixed if a == x) == 8 for x in H)
    for a, b in itertools.combinations(H, 2):
        assert sum(1 for blk in blocks if a in blk and b in blk) == 1
    return H, fixed, {v: 7 for v in range(h, 49)}, n0, len(Pairs), len(sing)


def add_perm_sb(cnf, var, n, perms, top):
    """Generic lex-leader for vertex permutations pi that are automorphisms of the formula:
    X <=lex Y with Y_p = X_{pi(p)} over the free edge variables in row-major upper-triangle order (0 < 1).
    Sound jointly with the class transpositions above (same group, same variable order)."""
    def x(a, b):
        return var.get((a, b) if a < b else (b, a))
    order = sorted(var)                       # row-major upper triangle
    nc = 0
    for pi in perms:
        pos = []
        for (a, b) in order:
            u, w = x(a, b), x(pi[a], pi[b])
            assert w is not None, ("perm maps a free pair to a fixed pair", a, b)
            if u != w:
                pos.append((u, w))
        e_prev = None
        for p, (a_, b_) in enumerate(pos):
            pre = [] if e_prev is None else [-e_prev]
            cnf.append(pre + [-a_, b_]); nc += 1
            if p < len(pos) - 1:
                top += 1; e = top
                cnf.append(pre + [a_, b_, e]); cnf.append(pre + [-a_, -b_, e]); nc += 2
                e_prev = e
    return top, nc


def high_perm(h, blocks_lowstart, blocks, sigma):
    """Vertex permutation induced by a permutation sigma of the highs that preserves the block multiset.
    Lows with block B go to lows with block sigma(B), matched in order of appearance."""
    n = h + len(blocks)
    pi = list(range(n))
    for a in range(h):
        pi[a] = sigma[a]
    slots = {}
    for i, b in enumerate(blocks):
        slots.setdefault(tuple(sorted(b)), []).append(h + i)
    used = {k: 0 for k in slots}
    for i, b in enumerate(blocks):
        img = tuple(sorted(sigma[x] for x in b))
        assert img in slots and used[img] < len(slots[img]), ("sigma does not preserve the blocks", b, img)
        pi[h + i] = slots[img][used[img]]; used[img] += 1
    assert sorted(pi) == list(range(n))
    return pi


def stratum_gen(n, d, h, T):
    """Generalisation of stratum() to n = d^2, low degree d, high degree d+1 (used ONLY by the small-d control).
    s(x) = d + 2 - h + r3(x)."""
    assert n == d * d
    H = list(range(h)); T = [tuple(b) for b in T]
    covered = {frozenset(p) for b in T for p in itertools.combinations(b, 2)}
    Pairs = [p for p in itertools.combinations(H, 2) if frozenset(p) not in covered]
    r3 = {x: sum(x in b for b in T) for x in H}
    if any(d + 2 - h + r3[x] < 0 for x in H):
        return None
    sing = [(x,) for x in H for _ in range(d + 2 - h + r3[x])]
    n0 = n - h - len(T) - len(Pairs) - len(sing)
    if n0 < 0:
        return None
    blocks = T + Pairs + sing + [()] * n0
    fixed = [(x, h + i) for i, b in enumerate(blocks) for x in b]
    assert all(sum(1 for a, _ in fixed if a == x) == d + 1 for x in H)
    return H, fixed, {v: d for v in range(h, n)}, blocks
