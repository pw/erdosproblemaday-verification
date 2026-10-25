# Discriminating mutation control: n=10 deg 4 is UNSAT with the C4 clauses (counting: 9 < 4*3);
# with the free-pair C4 clauses dropped it must be SAT and its model MUST fail the graph check.
import sys, subprocess
sys.path.insert(0, '.')
import c4cnf
for mutate in (False, True):
    cnf, var, F, adjS = c4cnf.build(10, [], [], {v: 4 for v in range(10)})
    if mutate:
        cnf.clauses = [c for c in cnf.clauses if len(c) != 4]
    cnf.to_file('/tmp/erdos85-1019/h9/mut_n10.cnf')
    for s in (['/home/exedev/MathDyad/tools/kissat/build/kissat', '-q'], ['/usr/bin/cadical', '-q']):
        out = subprocess.run(s + ['/tmp/erdos85-1019/h9/mut_n10.cnf'], capture_output=True, text=True).stdout
        v = 'UNSAT' if 's UNSATISFIABLE' in out else 'SAT' if 's SATISFIABLE' in out else 'UNKNOWN'
        note = ''
        if v == 'SAT':
            model = [int(t) for l in out.splitlines() if l.startswith('v ') for t in l[2:].split()]
            degs, mc = c4cnf.check_graph(10, c4cnf.decode(model, var))
            note = f'degrees {sorted(set(degs))} max codegree {mc} -> graph check {"FAILS (C4 present)" if mc >= 2 else "passes"}'
        print('mutated' if mutate else 'intact ', s[0].split('/')[-1], v, note)
