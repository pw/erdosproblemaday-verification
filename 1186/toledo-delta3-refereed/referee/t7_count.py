import numpy as np
from fractions import Fraction as F
B = [28, 6, 28, 37, 59, 116, 116, 59, 37, 28, 6, 28]
for k in [1, 2, 4, 8]:
    n = 548*k
    col = np.concatenate([np.full(b*k, i % 2) for i, b in enumerate(B)])
    assert len(col) == n
    V = 0
    for d in range(1, (n-1)//2 + 1):
        a = col[:n-2*d]; b = col[d:n-d]; c = col[2*d:]
        V += int(((a == b) & (b == c)).sum())
    print(n, V, 'formula 117n^2/2192 - n/2 =', F(117*n*n, 2192) - F(n, 2), ' match' if V == F(117*n*n, 2192) - F(n, 2) else '')
