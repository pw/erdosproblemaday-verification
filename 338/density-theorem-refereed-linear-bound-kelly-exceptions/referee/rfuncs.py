"""r(n) routines shared by the referee tests (copied from test_thmA.py)."""
import numpy as np

def r_fft(ind):
    n = len(ind)
    L = 1 << (2 * n).bit_length()
    f = np.fft.rfft(ind.astype(np.float64), L)
    conv = np.rint(np.fft.irfft(f * f, L)[: 2 * n - 1]).astype(np.int64)
    # ordered pairs incl. a=b ; remove diagonal, halve
    diag = np.zeros(2 * n - 1, dtype=np.int64)
    diag[0::2] = ind.astype(np.int64)
    r = (conv - diag)
    assert np.all(r % 2 == 0)
    return r // 2

def r_exact(ind):
    v = ind.astype(np.int64)
    conv = np.convolve(v, v)
    diag = np.zeros(len(conv), dtype=np.int64)
    diag[0::2] = v
    return (conv - diag) // 2

