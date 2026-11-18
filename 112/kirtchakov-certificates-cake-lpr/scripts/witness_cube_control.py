# Positive control on the cube CNFs (witness-type cubes at N=20 must be SAT).
import sys, os; sys.path.insert(0, os.getcwd())
# classes isomorphic to N+(v), N-(v), I(v) by brute-force isomorphism (our code), write the N=20 cube with
# his make_structured.py, and solve it. Each must be SAT (the witness itself, relabelled, is a model).
import json, itertools, subprocess, sys, os
from verify_chain import I3L3, TT4F
w = json.load(open('witness_sat_3_4_20.json')); N = w['N']
arcs = set(map(tuple, w['arcs']))
def induced(vs):
    idx = {v: i for i, v in enumerate(vs)}
    return frozenset((idx[a], idx[b]) for (a, b) in arcs if a in idx and b in idx)
def iso(A, n, B):
    if len(A) != len(B): return False
    for p in itertools.permutations(range(n)):
        if all((p[a], p[b]) in B for (a, b) in A): return True
    return False
def load(f):
    d = json.load(open(f)); return d['N'], frozenset(map(tuple, d['arcs']))
def find(vs, fam):
    G = induced(vs); n = len(vs)
    for i, f in enumerate(fam.get(n, [])):
        m, B = load(f)
        if m == n and iso(G, n, B): return i, f
    return None, None
C = os.path.expanduser('~/MathDyad/tools/cadical-3.0.1/build/cadical')
done = 0
for v in range(N):
    out = [b for (a, b) in arcs if a == v]; inn = [a for (a, b) in arcs if b == v]
    non = [u for u in range(N) if u != v and u not in out and u not in inn]
    p, q, s = len(out), len(inn), len(non)
    if p > q:  # use reversal symmetry the same way the chain does: reverse every arc
        continue
    i, pf = find(out, I3L3); j, qf = find(inn, I3L3); k, sf = find(non, TT4F)
    if None in (i, j, k):
        print('v', v, (p, q, s), 'NO CLASS FOUND', i, j, k); continue
    fn = f'/tmp/wc20_{v}.cnf'
    subprocess.run([sys.executable, 'make_structured.py', str(N), str(p), str(q), str(s), pf, qf, sf, fn], check=True, capture_output=True)
    r = subprocess.run([C, '-q', fn], capture_output=True, text=True)
    st = [l for l in r.stdout.splitlines() if l.startswith('s ')]
    print('v', v, (p, q, s), 'classes', (i, j, k), 'rc', r.returncode, st[0] if st else '')
    os.remove(fn); done += 1
    if done >= 3: break
