#!/usr/bin/env python3
"""Enumerate six-label triangle systems (paper Def 5.1) and check Lemma 5.3 (1)-(4) on every one.
Def 5.1: T subset of C(C,3), |C|=6, (1) exactly one of T, C\\T in T for each triple; (2) every pair in exactly two members.
Independent of the paper's proofs: brute force over all 2^10 choices of one triple per complementary pair."""
from itertools import combinations, permutations
C = range(6)
triples = [frozenset(t) for t in combinations(C, 3)]
pairs = [frozenset(p) for p in combinations(C, 2)]
comp = {t: frozenset(C) - t for t in triples}
reps = []
for t in triples:
    if t not in reps and comp[t] not in reps: reps.append(t)
assert len(reps) == 10
systems = []
for mask in range(1 << 10):
    T = set(reps[i] if (mask >> i) & 1 else comp[reps[i]] for i in range(10))
    if all(sum(p <= t for t in T) == 2 for p in pairs):
        systems.append(frozenset(T))
print('six-label triangle systems:', len(systems))
def link(T, a):
    return {frozenset(t - {a}) for t in T if a in t}
def is_5cycle(E, V):
    deg = {v: sum(v in e for e in E) for v in V}
    if any(d != 2 for d in deg.values()) or len(E) != 5: return False
    # connected
    seen = {next(iter(V))}; stack = list(seen)
    while stack:
        v = stack.pop()
        for e in E:
            if v in e:
                for w in e:
                    if w not in seen: seen.add(w); stack.append(w)
    return seen == set(V)
bad = 0
for T in systems:
    # (1) every vertex link is a 5-cycle
    for a in C:
        if not is_5cycle(link(T, a), set(C) - {a}): bad += 1; print('(1) fails', sorted(map(sorted, T)), a)
    # (2) every 4-set contains a triangle but not all four
    for A in combinations(C, 4):
        k = sum(frozenset(t) in T for t in combinations(A, 3))
        if not (1 <= k <= 3): bad += 1; print('(2) fails')
    # (3) for a != b and R subset of C\{a,b}, |R|=3: links at a and b restricted to R differ
    for a, b in permutations(C, 2):
        for R in combinations(sorted(set(C) - {a, b}), 3):
            R = set(R)
            la = {e for e in link(T, a) if e <= R}; lb = {e for e in link(T, b) if e <= R}
            if la == lb: bad += 1; print('(3) fails', a, b, R)
    # (4) triangles in any 5-subset determine T
    for z in C:
        sub = {t for t in T if z not in t}
        cands = [S for S in systems if {t for t in S if z not in t} == sub]
        if cands != [T]: bad += 1; print('(4) fails')
# automorphism groups
for T in systems[:1]:
    aut = [p for p in permutations(C) if {frozenset(p[x] for x in t) for t in T} == T]
    trans = [p for p in aut if sum(p[i] != i for i in C) == 2]
    print('|Aut| of first system:', len(aut), ' transpositions in Aut:', len(trans))
orbit = {frozenset(frozenset(p[x] for x in t) for t in systems[0]) for p in permutations(C)}
print('orbit of first system under S6:', len(orbit), ' == all systems:', orbit == set(systems))
print('Lemma 5.3 (1)-(4) violations:', bad)
# hemi-icosahedron: 6 axes of the icosahedron, triangles = faces modulo antipode -> one such system (sanity)
import math
phi = (1 + 5 ** 0.5) / 2
V = [(0, 1, phi), (0, -1, phi), (1, phi, 0), (-1, phi, 0), (phi, 0, 1), (phi, 0, -1)]  # one vertex per antipodal pair
full = V + [tuple(-x for x in v) for v in V]
def d(u, v): return sum((a - b) ** 2 for a, b in zip(u, v))
faces = set()
for i, j, k in combinations(range(12), 3):
    if abs(d(full[i], full[j]) - 4) < 1e-9 and abs(d(full[j], full[k]) - 4) < 1e-9 and abs(d(full[i], full[k]) - 4) < 1e-9:
        faces.add(frozenset(x % 6 for x in (i, j, k)))
print('hemi-icosahedron triangles:', len(faces), ' is a triangle system:', frozenset(faces) in set(systems))
raise SystemExit(0 if (len(systems) == 12 and bad == 0 and frozenset(faces) in set(systems)) else 1)
