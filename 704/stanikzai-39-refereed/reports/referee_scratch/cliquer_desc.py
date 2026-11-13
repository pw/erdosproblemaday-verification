"""Second, decorrelated leaf solver: cliquer (Ostergard) on every leaf of the s=33 tree at its tau, induced graphs
rebuilt here from the 5-sets; plus positive controls at tau-1 on the 16 leaves the 33-set images land in."""
import sys, subprocess, time, json
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor
D = '/home/exedev/MathDyad/erdos704/indep/runs/n13_s33_lg350'
V = [frozenset(c) for c in combinations(range(13), 5)]
L = open(D + '/leaves.txt').read().splitlines()
hit = {18,22,24,30,34,42,52,66,116,148,156,157,186,187,188,192}
jobs = []
for l in L:
    t = list(map(int, l.split())); jobs.append((t[0], t[1], [x - 1 for x in t[3:]]))
    if t[0] in hit: jobs.append((-t[0], t[1] - 1, [x - 1 for x in t[3:]]))
done = {163,146,162,188,186,200,-188}
jobs = [j for j in jobs if j[0] not in done]
jobs.sort(key=lambda j: -len(j[2]))
def run(j):
    lid, tau, vs = j; k = len(vs)
    E = [(a + 1, b + 1) for a in range(k) for b in range(a + 1, k) if len(V[vs[a]] & V[vs[b]]) != 3]
    p = f'/tmp/ref704/cl/desc_{lid}.col'
    with open(p, 'w') as f:
        f.write(f'p edge {k} {len(E)}\n'); f.writelines(f'e {a} {b}\n' for a, b in E)
    t0 = time.time()
    try:
        o = subprocess.run(['nice', '-n', '19', 'cliquer', '-u', '-q', '-m', str(tau), p], capture_output=True, text=True, timeout=1500); so, se = o.stdout, o.stderr; o = so
    except subprocess.TimeoutExpired:
        return dict(id=lid, tau=tau, k=k, status='TIMEOUT', secs=round(time.time() - t0))
    if 'No such clique' in so + se and 'size=' not in so: st = 'UNSAT'
    elif 'size=' in o:
        C = [vs[int(x) - 1] for x in o.split(':')[1].split()]
        ok = len(C) >= tau and all(len(V[a] & V[b]) != 3 for a, b in combinations(C, 2))
        st = 'SAT' if ok else 'BADWITNESS'
    else: st = 'ERR:' + o[:80]
    r = dict(id=lid, tau=tau, k=k, status=st, secs=round(time.time() - t0, 1))
    print(json.dumps(r), flush=True); return r
with ThreadPoolExecutor(int(sys.argv[1])) as ex:
    res = list(ex.map(run, jobs))
from collections import Counter
print('SUMMARY at-tau:', Counter(r['status'] for r in res if r['id'] > 0), ' controls tau-1:', Counter(r['status'] for r in res if r['id'] < 0))
