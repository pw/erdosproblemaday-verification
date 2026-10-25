# Second instrument for the lower sides: adjacency matrix A, check A symmetric 0/1 zero-diagonal,
# off-diagonal entries of A^2 <= 1 (no C4), row sums = degrees. Different parser (regex over the whole file).
import re, sys
import numpy as np
def load(path, n):
    s = open(path).read()
    m = re.search(r'def (\w+) : List \(Nat × Nat\) :=\s*\[(.*?)\]', s, re.S)
    E = [(int(a), int(b)) for a, b in re.findall(r'\((\d+)\s*,\s*(\d+)\)', m.group(2))]
    A = np.zeros((n, n), dtype=np.int64)
    for a, b in E:
        A[a, b] += 1; A[b, a] += 1
    return m.group(1), E, A
for path, n in [("Erdos85Boza48Witness.lean", 48), ("Erdos85OrderFortyNineDegreeSixWitness.lean", 49)]:
    name, E, A = load(path, n)
    A2 = A @ A; np.fill_diagonal(A2, 0)
    print(path, name, "edges", len(E), "sym", (A == A.T).all(), "0/1", A.max() <= 1, "diag0", (np.diag(A) == 0).all(),
          "mindeg", A.sum(1).min(), "maxdeg", A.sum(1).max(), "max codegree", A2.max())
    B = A.copy(); i, j = np.argwhere((A2 == 1) & (A == 0))[0]; B[i, j] = B[j, i] = 1
    B2 = B @ B; np.fill_diagonal(B2, 0)
    print("  control: add non-edge", (int(i), int(j)), "at distance 2 -> max codegree", B2.max())
