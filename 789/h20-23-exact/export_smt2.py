import sys, itertools
from z3 import Real, Solver, Or, Sum
sys.path.insert(0, "/home/exedev/MathDyad/erdos789")
from lemma789 import bad_equations
m, k = int(sys.argv[1]), int(sys.argv[2])
x = [Real(f"x{i}") for i in range(m)]
s = Solver(); s.add(x[0] > 0)
for i in range(m - 1): s.add(x[i] < x[i + 1])
for K in itertools.combinations(range(m), k):
    s.add(Or([Sum([x[i] for i in S]) == Sum([x[i] for i in T]) for S, T in bad_equations(K)]))
open(f"lemma_{m}_{k}.smt2", "w").write("(set-logic QF_LRA)\n" + s.to_smt2())
print("wrote", f"lemma_{m}_{k}.smt2")
