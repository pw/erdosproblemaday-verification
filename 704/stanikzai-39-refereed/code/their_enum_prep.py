"""Q5.2 cross-check on THEIR decomposition: map each of their 200 leaves to global 5-set ids, CHECK the leaf file equals
our complement-of-J induced on those 5-sets (and forced set + v1 is independent and inside the leaf's common
neighbourhood), then write leaves at threshold tau-1 (i.e. looking for 33-sets) for clq3."""
import json, csv
from itertools import combinations
root = '/home/exedev/MathDyad/erdos704/sub-vapywt/rel/'
V = [frozenset(c) for c in combinations(range(13), 5)]
row = {}
for r in csv.DictReader(open(root + 'R/out/dimacs/J_13_5_3_dimacs_vertex_map.csv')): row[int(r['dimacs_vertex'])] = int(r['original_row_id']) - 1
m = json.load(open(root + 'R/out/solve/cubes/J_13_5_3_s33/manifest.json'))
v1 = 0; assert V[v1] == frozenset(range(5))
lines = []; Fmap = {}
for c in m['cubes']:
    mp = {int(r['cube_vertex']): row[int(r['export_vertex'])] for r in csv.DictReader(open(root + c['cube_map_path']))}
    F = [row[x] for x in c['forced_vertices']]
    fam = [V[x] for x in F + [v1]]
    assert all(len(a & b) != 3 for a, b in combinations(fam, 2)), c['id']
    n = 0; E = set()
    for line in open(root + c['cube_dimacs_path']):
        if line.startswith('p'): n = int(line.split()[2])
        elif line.startswith('e'):
            a, b = map(int, line.split()[1:3]); E.add(frozenset((mp[a], mp[b])))
    vs = [mp[i] for i in range(1, n + 1)]
    assert len(set(vs)) == n
    exp = {frozenset((a, b)) for a, b in combinations(vs, 2) if len(V[a] & V[b]) != 3}
    assert E == exp, f'leaf {c["id"]} edges differ from complement of J'
    assert all(all(len(V[w] & V[f]) != 3 and w != f for f in F + [v1]) for w in vs)
    assert c['cube_threshold'] == 33 - len(F)
    lines.append(f"{c['id']} {c['cube_threshold'] - 1} {n} " + ' '.join(str(x + 1) for x in vs) + '\n')
    Fmap[c['id']] = F + [v1]
open('runs/theirs_s32/leaves.txt', 'w').write(''.join(lines))
json.dump(dict(F=Fmap), open('runs/theirs_s32/forced.json', 'w'))
print('their 200 leaves: files equal complement of J on the mapped 5-sets; forced+v1 independent; tau = 33-|F|: all OK')
