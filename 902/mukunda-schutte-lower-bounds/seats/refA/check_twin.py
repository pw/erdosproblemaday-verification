"""Remark 9.4: DRT(51) + twin vertex -> 52 vertices, in-degrees 25/26, pairs >= 12, min triple count.
Uses own DRT(51) and the repo's drt_twin52.npy (loaded with allow_pickle=False)."""
import sys, itertools
import numpy as np
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refA')
from tlib import *
def report(A, name):
    check_tournament(A)
    ind = A.sum(0)
    print(f"{name}: n={A.shape[0]} in-degree values {sorted(set(ind.tolist()))} counts {np.bincount(ind)[25:27].tolist()}"
          f" nu2={min_dom(A,2)} nu3={min_dom(A,3)}")
for i in range(2):
    D = np.load(f'own_drt51_{i}.npy', allow_pickle=False).astype(np.int8)
    n = 51
    A = np.zeros((52, 52), dtype=np.int8)
    A[:51, :51] = D
    v = 0
    A[51, :51] = D[v]; A[:51, 51] = D[:, v]
    A[51, v] = 0; A[v, 51] = 1   # v -> twin
    report(A, f"own_drt51_{i}+twin")
B = np.load('/home/exedev/MathDyad/subs-1126/902/repo/proof/search/r10/drt_twin52.npy', allow_pickle=False).astype(np.int8)
report(B, "repo drt_twin52.npy")
