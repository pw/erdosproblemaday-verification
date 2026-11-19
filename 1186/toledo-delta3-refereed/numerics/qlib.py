import ctypes, numpy as np, os
_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libqmin.so"))
_dp = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
_lib.cd_box.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_int, ctypes.c_double, ctypes.c_ulonglong]
_lib.cd_box.restype = ctypes.c_int
_lib.sa_pm1.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_ulonglong]
_lib.sa_pm1.restype = ctypes.c_double
_lib.tabu_pm1.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong]
_lib.tabu_pm1.restype = ctypes.c_double
_lib.qval.argtypes = [ctypes.c_int, _dp, _dp]
_lib.qval.restype = ctypes.c_double

def cd(M, x, seed, maxsweeps=5000, tol=1e-12):
    x = np.ascontiguousarray(x, dtype=np.float64).copy()
    sw = _lib.cd_box(len(x), M, x, maxsweeps, tol, seed)
    return x, sw
def sa(M, x, seed, steps, T0, T1, pblock=0.1, maxblock=48):
    x = np.ascontiguousarray(np.sign(x) + (x == 0), dtype=np.float64).copy()
    f = _lib.sa_pm1(len(x), M, x, steps, T0, T1, pblock, maxblock, seed)
    return x, f
def tabu(M, x, seed, iters, tenure, tenrand):
    x = np.ascontiguousarray(np.sign(x) + (x == 0), dtype=np.float64).copy()
    f = _lib.tabu_pm1(len(x), M, x, iters, tenure, tenrand, seed)
    return x, f
def qv(M, x):
    return _lib.qval(len(x), M, np.ascontiguousarray(x, dtype=np.float64))
