import json, sys, time
from fractions import Fraction as F
sys.path.insert(0, '/home/exedev/MathDyad/subs-1127/36/mine')
from overlap_eval import *
import numpy as np

root = '/home/exedev/MathDyad/subs-1127/36/repo'
obj = json.load(open(root + '/construction.json'))
a, D = obj['numerators'], obj['denominator']
N = len(a)
print("N", N, "D", D, "D == 524287e8:", D == 524287 * 10**8)
print("side conditions:", side_conditions(a, D) or "all pass")
print("nonzero cells:", sum(1 for x in a if x), "first nonzero idx", next(i for i,x in enumerate(a) if x), "last nonzero", max(i for i,x in enumerate(a) if x))
print("cells == D:", sum(1 for x in a if x == D))
t = time.time()
T, mx, argmax, scale = scores(a, D)
print("exact convolution time %.1fs" % (time.time() - t))
U = mx * scale
Uclaim = F(2462273619527794579322422405079, 6465103708838880000000000000000)
print("max T_k =", mx, " argmax k:", argmax)
print("U =", U, " == claimed:", U == Uclaim, " float:", float(U))
print("peak shift s = k*w =", [F(2 * k, N) for k in argmax])
print("U < 0.38085601258978320592:", U < F('0.38085601258978320592'), " U >= 0.38085601258978320591:", U >= F('0.38085601258978320591'))
# definition-level cross-check of top lags
vals = sorted(T.items(), key=lambda kv: -kv[1])
print("top 8 vertices (k, H value, gap to max):")
for k, v in vals[:8]:
    print("  ", k, float(v * scale), float((mx - v) * scale))
for k, v in vals[:5] + [(0, T[0]), (1, T[1]), (-N + 1, T[-N + 1]), (N - 1, T[N - 1])]:
    assert T_direct(a, D, k) == v, k
print("pure-Python definition sums agree at top-5 + 4 other lags")
# full-length cross-check: sum identity
assert sum(T.values()) == sum(a) * (N * D - sum(a))
print("sum identity sum_k T_k = (sum a)(ND - sum a): OK")
# uniqueness over the reals: max vertex strictly above all others
second = vals[1][1]
print("strict uniqueness among 2N+1 =", len(T), "vertices:", mx > second, " relative gap (max-second)/max =", float(F(mx - second, mx)))
# off-grid direct exact integration
import random
rng = random.Random(1127)
k0 = argmax[0]
tests = [F(k0) * F(2, N), F(2*k0+1, N), F(2*k0-1, N), F(2 * k0, N) + F(1, 10**9)] + [F(rng.randint(-2 * N, 2 * N), N) + F(rng.randint(1, 999), 1000 * N) for _ in range(4)]
w = F(2, N)
for s in tests:
    hd = H_direct_exact(a, D, s)
    q = s / w; k = q.numerator // q.denominator; u = q - k
    hi = ((1 - u) * T.get(k, 0) + u * T.get(k + 1, 0)) * scale
    print("  s=%.12f direct=%.18f interp=%.18f equal=%s <=U=%s" % (float(s), float(hd), float(hi), hd == hi, hd <= U))
# float FFT third route
Hf = H_fft_float(a, D)
ex = np.array([float(T[k] * scale) for k in range(-N, N + 1)])
print("FFT vs exact: max abs diff %.3e ; FFT argmax k = %d ; FFT max %.15f" % (np.abs(Hf - ex).max(), int(np.argmax(Hf)) - N, Hf.max()))
json.dump({str(k): str(v) for k, v in T.items()}, open('/home/exedev/MathDyad/subs-1127/36/mine/T_child.json', 'w'))
