# Negative control for THEIR solver: run their run_suite on m=15,k=5 (satisfiable: positive part of A31 has 15 elements, alpha<=5).
# Executed as a separate process with cwd = their code dir; their source is exec'd, not imported into my checker.
import sys
src = open('/tmp/e1125/dl787/repo/code/solve_k6_pos.py').read()
g = {'__name__': 'negctl', '__file__': '/tmp/e1125/dl787/repo/code/solve_k6_pos.py'}
exec(compile(src, 'solve_k6_pos.py', 'exec'), g)
r = g['run_suite'](int(sys.argv[1]), int(sys.argv[2]), [None] + list(range(int(sys.argv[1]) - 2)), wave_mode=False)
print('RESULT', r)
