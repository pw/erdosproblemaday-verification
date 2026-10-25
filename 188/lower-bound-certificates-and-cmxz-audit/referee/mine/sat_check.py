import sys, json, itertools, subprocess
core = json.load(open(sys.argv[1])); cnf = sys.argv[2]
cl = [tuple(sorted(c)) for c in core['core_clauses']]
inst = set()
for line in open(cnf):
    if line[0] in 'pc': continue
    lits = [int(t) for t in line.split()][:-1]
    inst.add(tuple(sorted(lits)))
print('core clauses in instance:', sum(c in inst for c in cl), '/', len(cl))
# renumber and write DIMACS for cadical
vs = sorted({abs(l) for c in cl for l in c}); m = {v: i+1 for i, v in enumerate(vs)}
path = sys.argv[1] + '.dimacs'
with open(path, 'w') as f:
    f.write(f'p cnf {len(vs)} {len(cl)}\n')
    for c in cl: f.write(' '.join(str((1 if l > 0 else -1)*m[abs(l)]) for l in c) + ' 0\n')
r = subprocess.run(['cadical', '-q', path], capture_output=True, text=True); print('cadical:', [l for l in r.stdout.splitlines() if l.startswith('s ')])
if len(vs) <= 20:
    sat = 0
    for bits in itertools.product([False, True], repeat=len(vs)):
        val = dict(zip(range(1, len(vs)+1), bits))
        if all(any((val[m[abs(l)]] if l > 0 else not val[m[abs(l)]]) for l in c) for c in cl): sat += 1
    print('brute force satisfying assignments:', sat, 'of', 2**len(vs))
