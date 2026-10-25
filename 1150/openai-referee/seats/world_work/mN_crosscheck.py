# Independent cross-check of mN_bruteforce.py: (a) N<=14: every one of the 2^N sign vectors (no symmetry reduction) on a direct
# polyval grid of 2^13 points on the FULL circle, min over vectors of the grid max (a lower bound on the true min sup, up to
# grid error); (b) re-evaluate each reported minimiser by direct summation on 2^20 points.
import sys, math, itertools
import numpy as np
rep = {}
for line in open(sys.argv[1]):
    if line.startswith('N='):
        parts = line.split()
        N = int(parts[0][2:]) if parts[0] != 'N=' else int(parts[1])
for line in open(sys.argv[1]):
    if 'example=' in line:
        N = int(line.split('N=')[1].split()[0]); ex = line.split('example=')[1].split()[0]
        lo = float(line.split('[')[1].split(',')[0]); rep[N] = (ex, lo)
th = 2*math.pi*np.arange(1<<20)/(1<<20)
for N,(ex,lo) in sorted(rep.items()):
    eps = np.array([1.0 if c=='+' else -1.0 for c in ex])
    z = np.exp(1j*th)
    v = np.zeros_like(z)
    for e in eps[::-1]: v = v*z + e
    print(f"N={N:2d} reported {lo:.9f}  direct 2^20-grid max {np.abs(v).max():.9f}", end='')
    if N <= 14:
        K = 1<<13; t = 2*math.pi*np.arange(K)/K
        W = np.exp(1j*np.outer(np.arange(N), t))          # N x K
        best = 1e9
        for bits in range(1<<N):
            pass
        E = np.array([[1.0 if (b>>k)&1 else -1.0 for k in range(N)] for b in range(1<<N)])
        best = np.abs(E @ W).max(axis=1).min()
        print(f"  | all 2^{N} vectors, 2^13 full-circle grid: min of grid-max = {best:.9f}", end='')
    print()
