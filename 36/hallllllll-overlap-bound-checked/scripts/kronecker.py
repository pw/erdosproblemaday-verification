# Main seat's own exact check (27 Nov): all lags T_k = sum_i a_i (D - a_{i-k}) by Kronecker substitution in Python big ints.
# Different implementation from the referee seat (20-bit int64 split) and from the reader (base-2^128 packed certificate).
import json, sys
from fractions import Fraction as F
obj = json.load(open(sys.argv[1])); a = obj['numerators']; D = obj['denominator']; N = len(a)
assert all(0 <= x <= D for x in a) and 2 * sum(a) == N * D          # 0<=h<=1, integral of h over [0,2) = 1
b = [D - x for x in a]                                              # g = 1 - h on [0,2)
B = 1 << 140                                                        # slot width: each T_k < N*D^2 < 2^104
A = sum(x << (140 * i) for i, x in enumerate(a))
Rb = sum(x << (140 * (N - 1 - j)) for j, x in enumerate(b))         # reversed b
P = A * Rb; mask = B - 1
# coefficient at index i + (N-1-j) = (N-1) + (i-j) collects a_i b_j with i - j = k
T = {}
for idx in range(2 * N - 1):
    T[idx - (N - 1)] = (P >> (140 * idx)) & mask
mx = max(T.values()); arg = [k for k, v in T.items() if v == mx]
# H at s = k*w (w = 2/N): sum over cell pairs with offset k of the overlap integral w*h_i*g_j  -> H(kw) = w * T_k / D^2
U = F(2, N) * F(mx, D * D)
print("N", N, "max T", mx, "argmax", arg, "U", U, float(U))
print("U == claimed:", U == F(2462273619527794579322422405079, 6465103708838880000000000000000))
s2 = sorted(T.values(), reverse=True)[1]; print("second-best gap", float(F(2, N) * F(mx - s2, D * D)))
print("sum check:", sum(T.values()) == sum(a) * sum(b))
