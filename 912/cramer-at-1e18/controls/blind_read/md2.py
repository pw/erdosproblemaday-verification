import numpy as np, math
for e in (7, 8, 9):
    n = 10**e; s = math.isqrt(n); k = np.arange(2, s + 1, dtype=np.int64)
    # Poisson form exactly as move_density.py
    lam = lambda kk: (n / (kk * (kk + 1.0))) / np.log(n / kk)
    p0k = np.exp(-lam(k.astype(float))); p0km = np.exp(-lam(k.astype(float) - 1))
    w = 1 / (k * np.log(n / k))
    pois = np.sum(w * (p0k + p0km - 2 * p0k * p0km))
    # Bernoulli Cramér with integer lengths and the sqrt(n) truncation (interval below Q = I_k, above Q = I_{k-1} minus Q)
    Q = n // k + 1  # representative Q at the left edge of I_{k-1}
    loA = np.maximum(n // (k + 1), s); lenA = np.maximum(n // k - loA, 0)
    loB = np.maximum(n // k, s); lenB = np.maximum(n // (k - 1) - loB - 1, 0)
    q = 1 / np.log(n / k.astype(float))
    pA = np.exp(lenA * np.log1p(-q)); pB = np.exp(lenB * np.log1p(-q))
    bern = np.sum(w * (pA + pB - 2 * pA * pB))
    print(f"1e{e}: Poisson form {pois:.4f}   Bernoulli Cramér (integer lengths, sqrt-n cut) {bern:.4f}")
