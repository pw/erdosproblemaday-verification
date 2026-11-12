# Exact (uncapped) recheck of the r=60 w_z-form counterexample found by barrier_wz.py.
from fractions import Fraction as Fr
def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]
PR = primes_upto(5000)
ps = [p for p in PR if 1049 <= p and p * p < 2 * 1049 * 1049]
r = len(ps); m = ps[-2] * ps[-1]
print("r =", r, "p_1..p_r =", ps[0], "..", ps[-1], " p_r/p_1 =", ps[-1] / ps[0], " m =", m)
assert ps[-1] ** 2 < 2 * ps[0] ** 2
c = Fr(19, 10)
P = 1
for p in ps: P *= p
x = P - (m + 1) // 2
# LHS: k <= m, exact valuations
w = {}
for p in ps:
    for k in range(p, m + 1, p):
        kk = k; v = 0
        while kk % p == 0: kk //= p; v += 1
        w[k] = w.get(k, 0) + v
LHS_W = sum((Fr(v) - c) for v in w.values() if v > c)
LHS_S = Fr(0)
cnt = {}
for p in ps:
    for k in range(p, m + 1, p): cnt[k] = cnt.get(k, 0) + 1
LHS_S = sum((Fr(s) - c) for s in cnt.values() if s > c)
# RHS: exact big-int valuations on the window
ww = {}; ss = {}
for p in ps:
    rr = (-x) % p
    i0 = rr if rr >= 1 else p
    for i in range(i0, m + 1, p):
        b = x + i; v = 0
        while b % p == 0: b //= p; v += 1
        ww[i] = ww.get(i, 0) + v; ss[i] = ss.get(i, 0) + 1
RHS_W = sum(v - 1 for v in ww.values() if v > 1)
RHS_S = sum(s - 1 for s in ss.values() if s > 1)
print("S-form  : LHS =", LHS_S, " RHS =", RHS_S, " fails:", LHS_S > RHS_S)
print("w_z-form: LHS =", LHS_W, "=", float(LHS_W), " RHS =", RHS_W, " fails:", LHS_W > RHS_W)
print("max window valuation seen:", max(ww.values()))
