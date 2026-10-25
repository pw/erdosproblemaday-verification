#!/usr/bin/env python3
"""Independent SAT encoding of the finite obstruction (paper §6 / Lean TenSystem) on labels 0..9.
Variables: q[S] for each 4-subset S (tetrahedra), t[U] for each 3-subset U (triangles).
Conditions (Lean TenSystem field names; paper's version in brackets):
  down          : q[S] -> t[U] for U ⊂ S, |U|=3
  pure          : t[U] -> OR_{v∉U} q[U+v]
  no_boundary   : q[S] -> OR_{v∉S} q[(S-{x})+v]  for each x in S        [paper: 'parity': each triangle in an EVEN number of tetrahedra]
  complementary : q[S] -> (t[U] xor t[C\\U]) for U ⊂ C=Sᶜ, |U|=3
  pair_count    : q[S] -> exactly two of t[P+w], w ∈ C\\P, for P ⊂ C, |P|=2
  nonempty      : q[{0,1,2,3}]   (WLOG by relabelling, as the Lean's no_ten_system does)
Usage: tensystem_cnf.py OUT.cnf [--variant lean|paper|both] [--drop field,...]"""
import sys, itertools as it
L = range(10)
S4 = [frozenset(s) for s in it.combinations(L, 4)]
S3 = [frozenset(s) for s in it.combinations(L, 3)]
var = {}
for s in S4: var[('q', s)] = len(var) + 1
for u in S3: var[('t', u)] = len(var) + 1
q = lambda s: var[('q', frozenset(s))]
t = lambda u: var[('t', frozenset(u))]
def build(variant='lean', drop=()):
    cl = []
    if 'down' not in drop:
        for s in S4:
            for u in it.combinations(sorted(s), 3): cl.append([-q(s), t(u)])
    if 'pure' not in drop:
        for u in S3: cl.append([-t(u)] + [q(u | {v}) for v in L if v not in u])
    if variant in ('lean', 'both') and 'no_boundary' not in drop:
        for s in S4:
            for x in s:
                u = s - {x}
                cl.append([-q(s)] + [q(u | {v}) for v in L if v not in s])
    if variant in ('paper', 'both') and 'parity' not in drop:
        # XOR over the 7 tetrahedra containing u is 0: forbid every odd assignment (2^6 = 64 clauses per triangle)
        for u in S3:
            xs = [q(u | {v}) for v in L if v not in u]
            for bits in it.product([0, 1], repeat=len(xs)):
                if sum(bits) % 2 == 1:
                    cl.append([(-x if b else x) for x, b in zip(xs, bits)])
    for s in S4:
        C = [v for v in L if v not in s]
        if 'complementary' not in drop:
            for u in it.combinations(C, 3):
                w = frozenset(C) - frozenset(u)
                if min(u) < min(w):  # each complementary pair once
                    cl.append([-q(s), t(u), t(w)]); cl.append([-q(s), -t(u), -t(w)])
        if 'pair_count' not in drop:
            for p in it.combinations(C, 2):
                xs = [t(set(p) | {w}) for w in C if w not in p]   # 4 candidates; exactly two true
                for a in it.combinations(xs, 3): cl.append([-q(s)] + [-x for x in a])   # at most 2
                for a in it.combinations(xs, 3): cl.append([-q(s)] + list(a))           # at least 2 (no 3 false)
    if 'nonempty' not in drop: cl.append([q({0, 1, 2, 3})])
    return cl
def check(model_true, variant='lean'):
    """Independent semantic checker (plain set logic, no clause reuse). model_true: set of positive var ids."""
    Q = {s for s in S4 if q(s) in model_true}; T = {u for u in S3 if t(u) in model_true}
    ok = {}
    ok['down'] = all(frozenset(u) in T for s in Q for u in it.combinations(s, 3))
    ok['pure'] = all(any(u <= s for s in Q) for u in T)
    ok['no_boundary'] = all(sum(1 for s2 in Q if (s - {x}) <= s2) >= 2 for s in Q for x in s)
    ok['parity'] = all(sum(1 for s in Q if u <= s) % 2 == 0 for u in S3)
    ok['complementary'] = all((frozenset(u) in T) != ((frozenset(L) - s - frozenset(u)) in T)
                              for s in Q for u in it.combinations(sorted(frozenset(L) - s), 3))
    ok['pair_count'] = all(sum(1 for w in (frozenset(L) - s - frozenset(p)) if (frozenset(p) | {w}) in T) == 2
                           for s in Q for p in it.combinations(sorted(frozenset(L) - s), 2))
    ok['nonempty'] = frozenset({0, 1, 2, 3}) in Q
    return ok, len(Q), len(T)
if __name__ == '__main__':
    out = sys.argv[1]; variant = 'lean'; drop = ()
    if '--variant' in sys.argv: variant = sys.argv[sys.argv.index('--variant') + 1]
    if '--drop' in sys.argv: drop = tuple(sys.argv[sys.argv.index('--drop') + 1].split(','))
    cl = build(variant, drop)
    with open(out, 'w') as f:
        f.write(f'c TenSystem variant={variant} drop={",".join(drop) or "-"}\np cnf {len(var)} {len(cl)}\n')
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    print(out, 'vars', len(var), 'clauses', len(cl))
