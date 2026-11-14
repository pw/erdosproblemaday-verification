# Referee: lift the author's 101-column rational solution to an explicit weighting of copies (spread over Aut(W)),
# then check cover equalities and the three cut families directly on 5-, 4-, 6-sets and points, in exact Fractions.
import json
from fractions import Fraction
from itertools import combinations
from collections import defaultdict
auts = [tuple(p) for p in json.load(open('refauts.json'))['auts']]
sol = json.load(open('../lp_cuts_exact.json')); z = [Fraction(x) for x in sol['z']]
reps = [list(map(int, l.split())) for l in open('lp_reps.txt')]
assert all(r[0] == 1 for r in reps) and len(reps) == len(z) == 101
reps = [r[1:] for r in reps]
def struct(R):
    inf, a, b = R[0], R[1:4], R[4:7]; S12, S13, S23 = set(R[7:9]), set(R[9:11]), set(R[11:13])
    B = [frozenset({a[0], b[0]} | S12 | S13), frozenset({a[1], b[1]} | S12 | S23), frozenset({a[2], b[2]} | S13 | S23)]
    c6 = frozenset({inf, *a}); c9 = frozenset({inf, *b}); sh = S12 | S13 | S23
    sets = {Bk - {x} for Bk in B for x in Bk} | {c6 | {s} for s in sh} | {c9 | {y} for y in range(13) if y not in c9}
    assert len(sets) == 33
    return dict(inf=inf, B=B, c6=c6, c9=c9, sh=sh, sets=sets)
Wr = [10, 0, 11, 6, 1, 12, 7, 2, 5, 3, 4, 8, 9]; Ws = struct(Wr)
wt = defaultdict(Fraction)   # copy (as frozenset of sets) -> weight, and keep a role record
rec = {}
print('min z', min(z), 'sum z', sum(z))
for R, zt in zip(reps, z):
    for g in auts:
        R2 = [g[x] for x in R]; s = struct(R2); key = frozenset(s['sets'])
        assert not (key & Ws['sets']), 'copy meets W'
        wt[key] += zt / 48; rec[key] = s
print('distinct copies in support:', len(wt), '| total weight', sum(wt.values()), '(expect 38 = 1254/33)')
V5 = [frozenset(c) for c in combinations(range(13), 5)]
cov = defaultdict(Fraction)
for key, w in wt.items():
    for s in key: cov[s] += w
print('cover: every 5-set outside W exactly 1:', all(cov[s] == 1 for s in V5 if s not in Ws['sets']), '| sets of W covered 0:', all(cov[s] == 0 for s in Ws['sets']))
def add4(acc, s, w):
    for Bk in s['B']:
        for U in combinations(sorted(Bk), 4): acc[frozenset(U)] += w
    acc[s['c9']] += 4*w; acc[s['c6']] += 3*w
def add6(acc, s, w):
    for Bk in s['B']: acc[Bk] += 3*w
    for x, y in combinations(sorted(s['sh']), 2): acc[s['c6'] | {x, y}] += w
    for x, y in combinations([t for t in range(13) if t not in s['c9']], 2): acc[s['c9'] | {x, y}] += w
a4 = defaultdict(Fraction); a6 = defaultdict(Fraction); ap = defaultdict(Fraction)
add4(a4, Ws, Fraction(1)); add6(a6, Ws, Fraction(1)); ap[Ws['inf']] += 1
for k, w in wt.items(): add4(a4, rec[k], w); add6(a6, rec[k], w); ap[rec[k]['inf']] += w
print('4-set cut: max LHS =', max(a4.values()), '(must be <= 4); 6-set cut: max LHS =', max(a6.values()), '(must be <= 3)')
print('point rule: min over points =', min(ap[x] for x in range(13)), '(must be >= 1)')
# negative control: the same check on an infeasible perturbation (scale weights by 1.01) must fail the cover test
