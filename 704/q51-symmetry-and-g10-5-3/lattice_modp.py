"""S1: rank of the copies' indicator vectors mod p, and membership of the all-ones vector in their span mod p.
Rows = random copies of W (1287 columns)."""
import sys, random, numpy as np
from wstruct import V, IDX, random_copy
R = int(sys.argv[1]) if len(sys.argv) > 1 else 3200
random.seed(20261114)
M = np.zeros((R, 1287), dtype=np.int64)
for r in range(R):
    for s in random_copy(): M[r, IDX[s]] = 1
np.save('copies_rows.npy', M.astype(np.int8))

def rank_and_member(M, t, p):
    A = np.concatenate([M % p, (t % p)[None, :]], axis=0)  # last row = target, never used as a pivot
    n_rows = A.shape[0] - 1; r = 0; piv_cols = []
    for c in range(A.shape[1]):
        nz = np.nonzero(A[r:n_rows, c])[0]
        if len(nz) == 0: continue
        i = r + nz[0]
        if i != r: A[[r, i]] = A[[i, r]]
        inv = pow(int(A[r, c]), -1, p)
        A[r] = (A[r] * inv) % p
        rows = np.nonzero(A[:, c])[0]; rows = rows[rows != r]
        A[rows] = (A[rows] - np.outer(A[rows, c], A[r])) % p
        piv_cols.append(c); r += 1
        if r == n_rows: break
    return r, not A[-1].any()

ones = np.ones(1287, dtype=np.int64)
planted = ones.copy(); planted[0] = 0   # coordinate sum 1286, not divisible by 3 or 11: must be rejected mod 3 and 11
for p in (2, 3, 5, 7, 11, 13, 17):
    rk, mem = rank_and_member(M, ones, p)
    _, mem_bad = rank_and_member(M, planted, p)
    print(f'p={p}: rank {rk}/1287, all-ones in span: {mem}; planted (sum 1286) in span: {mem_bad}', flush=True)
