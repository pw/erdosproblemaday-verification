import sys, time
from pysat.formula import CNF
from pysat.solvers import Solver
cnf = CNF(from_file=sys.argv[1])
for name in ['minisat22', 'glucose4']:
    t = time.time()
    with Solver(name=name, bootstrap_with=cnf.clauses) as S:
        r = S.solve()
    print(name, 'UNSAT' if r is False else 'SAT', '%.1fs' % (time.time() - t), flush=True)
