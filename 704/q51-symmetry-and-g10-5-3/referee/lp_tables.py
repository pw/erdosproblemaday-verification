# Referee: my own Aut(W) orbits on 5-sets (outside W), 4-sets, 6-sets, points; labelled by the author's orbit index
# (orbit containing the author's representative) only so that I can locate the author's columns.
import json, ast, re, itertools, numpy as np
src = open('../wstruct.py').read()
W = {frozenset(x-1 for x in s) for s in ast.literal_eval(re.search(r'^W0 = (\[.*\])$', src, re.M).group(1))}
exec(open('autW.py').read().split("print('|Aut(W)| =")[0].split('# backtracking automorphism search')[1].replace('Wl=list(W)','Wl=list(W)\ndeg=[sum(1 for s in W if x in s) for x in range(13)]'))
assert len(auts) == 48
O = json.load(open('../orbits.json'))
def lab(k, reps, objs):
    m = {}
    for i, r in enumerate(reps):
        orb = {frozenset(p[x] for x in r) for p in auts}
        for o in orb: assert o not in m; m[o] = i
    assert set(m) == set(objs), k
    return m
V5 = [frozenset(c) for c in itertools.combinations(range(13), 5)]
m5 = lab(5, O['rep5'], [s for s in V5 if s not in W])
m4 = lab(4, O['rep4'], [frozenset(c) for c in itertools.combinations(range(13), 4)])
m6 = lab(6, O['rep6'], [frozenset(c) for c in itertools.combinations(range(13), 6)])
mp = lab(1, O['reppt'], [frozenset([x]) for x in range(13)])
for nm, m, sz in (('5', m5, O['size5']), ('4', m4, O['size4']), ('6', m6, O['size6']), ('pt', mp, O['sizept'])):
    from collections import Counter
    c = Counter(m.values()); assert [c[i] for i in range(len(sz))] == sz, nm
print('author orbit partitions agree with my Aut(W) orbits (5,4,6,pt): OK')
mask = lambda s: sum(1 << x for x in s)
with open('reftables.txt', 'w') as f:
    for s, i in m5.items(): f.write(f'5 {mask(s)} {i}\n')
    for s, i in m4.items(): f.write(f'4 {mask(s)} {i}\n')
    for s, i in m6.items(): f.write(f'6 {mask(s)} {i}\n')
    for s, i in mp.items(): f.write(f'1 {min(s)} {i}\n')
# extract the 101 target columns
sol = json.load(open('../lp_cuts_exact.json')); cols = sol['cols']
with open('../lp_cols.bin', 'rb') as fh:
    n = int(np.frombuffer(fh.read(8), dtype=np.int64)[0]); D = int(np.frombuffer(fh.read(4), dtype=np.int32)[0])
    tg = []
    for c in cols:
        fh.seek(12 + c*D); tg.append(np.frombuffer(fh.read(D), dtype=np.uint8))
print('n cols', n, 'D', D, 'targets', len(tg))
np.array(tg, dtype=np.uint8).tofile('targets.bin')
json.dump(dict(auts=[list(p) for p in auts]), open('refauts.json', 'w'))
