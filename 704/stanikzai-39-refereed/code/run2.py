"""Decide every leaf in <out>/leaves.txt with ./clq2 in P parallel chunks; verify every SAT witness against J
rebuilt here from the definition (frozensets, no shared code with tree.py's bitmask build)."""
import sys, json, subprocess, os, time
from itertools import combinations
out, P = sys.argv[1], int(sys.argv[2])
here = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(out + '/manifest.json'))
n, s = man['n'], man['s']
V = [frozenset(c) for c in combinations(range(n), 5)]
lines = open(out + '/leaves.txt').read().splitlines()
F = {L['id']: L['F'] for L in man['leaves']}
os.makedirs(out + '/chunks', exist_ok=True)
for i in range(P):
    open(f'{out}/chunks/c{i:02d}.txt', 'w').write(''.join(l + '\n' for l in lines[i::P]))
t0 = time.time()
procs = [subprocess.Popen(['nice', '-n', '19', here + '/clq2', out + '/gbar.col', f'{out}/chunks/c{i:02d}.txt'],
                          stdout=open(f'{out}/chunks/r{i:02d}.txt', 'w')) for i in range(P)]
rcs = [p.wait() for p in procs]
res = [l.split() for i in range(P) for l in open(f'{out}/chunks/r{i:02d}.txt')]
nsat = nuns = bad = 0; wits = []
for r in res:
    lid = int(r[0])
    if r[1] == 'SAT':
        g = [int(x) - 1 for x in r[2:]] + F[lid] + [man['v'], man['u']]
        fam = [V[x] for x in g]
        ok = len(set(g)) == s + 1 and all(len(a & b) != 3 for a, b in combinations(fam, 2))
        nsat += 1; bad += (not ok); wits.append(dict(leaf=lid, ok=ok, family=[sorted(x) for x in fam]))
    elif r[1] == 'UNSAT': nuns += 1
    else: bad += 1
missing = len(lines) - len(res)
summary = dict(leaves=len(lines), answered=len(res), missing=missing, UNSAT=nuns, SAT=nsat, bad=bad, rcs=rcs,
               wall=round(time.time() - t0, 1), nodes_total=sum(int(r[2].split('=')[1]) for r in res if r[1] == 'UNSAT'))
json.dump(dict(summary=summary, witnesses=wits[:20]), open(out + '/results_clq2.json', 'w'))
print('clq2', summary)
