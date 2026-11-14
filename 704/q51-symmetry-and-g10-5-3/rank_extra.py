import numpy as np
M = np.load('copies_rows.npy')[:1800].astype(np.int64)
def rank(M, p):
    A = M % p; r = 0
    for c in range(A.shape[1]):
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0: continue
        i = r + nz[0]
        if i != r: A[[r, i]] = A[[i, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        rows = np.nonzero(A[:, c])[0]; rows = rows[rows > r]
        A[rows] = (A[rows] - np.outer(A[rows, c], A[r])) % p
        r += 1
        if r == A.shape[0]: break
    return r
for p in (23, 47): print(f'p={p}: rank {rank(M, p)}/1287', flush=True)
