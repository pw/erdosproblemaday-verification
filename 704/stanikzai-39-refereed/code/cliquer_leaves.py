"""Second leaf solver on OUR tree: cliquer 1.21 (Niskanen-Ostergard, Debian package /usr/bin/cliquer) decides each leaf
of <out>/leaves.txt at its tau: 'cliquer -u -q -m tau' searches for a clique of size >= tau (unweighted).
Leaf graphs rebuilt here from the 5-sets (Gbar adjacency = intersection != 3). Usage: cliquer_leaves.py out P"""
import sys, subprocess, time, json, os
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor
out, P = sys.argv[1], int(sys.argv[2])
V = [frozenset(c) for c in combinations(range(13), 5)]
jobs = []
for l in open(out + '/leaves.txt').read().splitlines():
    t = list(map(int, l.split())); jobs.append((t[0], t[1], [x - 1 for x in t[3:]]))
jobs.sort(key=lambda j: -len(j[2]))
os.makedirs(out + '/cliquer', exist_ok=True)
logf = open(out + '/cliquer/log.jsonl', 'a')
def run(j):
    lid, tau, vs = j; k = len(vs)
    E = [(a + 1, b + 1) for a in range(k) for b in range(a + 1, k) if len(V[vs[a]] & V[vs[b]]) != 3]
    p = f'{out}/cliquer/L{lid}.col'
    with open(p, 'w') as f:
        f.write(f'p edge {k} {len(E)}\n'); f.writelines(f'e {a} {b}\n' for a, b in E)
    t0 = time.time()
    o = subprocess.run(['nice', '-n', '19', 'cliquer', '-u', '-q', '-m', str(tau), p], capture_output=True, text=True)
    so = o.stdout + o.stderr
    if 'size=' in o.stdout:
        C = [vs[int(x) - 1] for x in o.stdout.split(':')[1].split()]
        ok = len(C) >= tau and all(len(V[a] & V[b]) != 3 for a, b in combinations(C, 2))
        st = 'SAT' if ok else 'BAD_SAT'
    elif o.returncode == 0 and 'No such clique' in so: st = 'UNSAT'
    else: st = f'ERR rc={o.returncode}'
    os.remove(p)
    r = dict(id=lid, tau=tau, k=k, status=st, secs=round(time.time() - t0, 1), out=so.strip()[:120])
    logf.write(json.dumps(r) + '\n'); logf.flush()
    return r
with ThreadPoolExecutor(P) as ex:
    res = list(ex.map(run, jobs))
from collections import Counter
print('cliquer', dict(Counter(r['status'] for r in res)), 'cpu', round(sum(r['secs'] for r in res)), 'max', max(r['secs'] for r in res))
