import sys, time, resource, json
sys.path.insert(0, '/home/exedev/MathDyad/runs')
import erdos778_wavew014_verify as V
mode = sys.argv[1]  # clique | triangle
n = int(sys.argv[2])
t0 = time.time()
if mode == 'clique':
    s = V.Solver(n, 'clique', 1, 2, symmetry=True)
else:
    s = V.TriangleAvoidanceSolver(n, symmetry=True)
r = s.solve()
r['elapsed_s'] = round(time.time()-t0, 1)
r['maxrss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(json.dumps(r, default=str))
