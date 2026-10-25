#!/usr/bin/env python3
"""Brute-force + exact checks of Theorem transfer:large-r (07-transfers.tex, printed Thm 7.2).
(1) For r in a list: b = floor(r^{1/4}), s = floor(log r / (4 log 2)); colour n in [0, b^s) by
    (h(x_0),...,h(x_{s-1}), sum x_i^2); check #colours used <= 2^s(1+s(b-1)^2) <= r and that NO
    colour class contains a 3-AP n, n+d, n+2d (d >= 1).
CONTROL 1 (must FAIL): halves H_0 = {0..ceil(b/2)} (diameter one larger) -> mono 3-AP expected.
CONTROL 2 (must FAIL): drop the squared-norm entry -> mono 3-AP expected.
(2) Exact arithmetic of (transfer:color-count), s >= L/(8 log 2), log b >= L/8 and
    b^s > exp(L^2/(64 log 2)) for EVERY integer r in [256, 2*10^6] and for r = 2^j, 2^j - 1,
    j <= 400 (where floors jump)."""
import math

def iroot_floor(n, e):
    if n < 2: return n
    x = 1 << ((n.bit_length() + e - 1) // e)
    while True:
        y = ((e - 1) * x + n // x ** (e - 1)) // e
        if y >= x: break
        x = y
    while x ** e > n: x -= 1
    while (x + 1) ** e <= n: x += 1
    return x

def params(r):
    b = iroot_floor(r, 4)
    s = (r.bit_length() - 1) // 4          # floor(floor(log2 r)/4) = floor(log r/(4 log 2))
    return b, s

def colouring(b, s, half_cut, with_norm=True):
    cols = []
    for n in range(b ** s):
        x, t = [], n
        for _ in range(s):
            x.append(t % b); t //= b
        hv = tuple(int(xi >= half_cut) for xi in x)
        cols.append(hv + ((sum(xi * xi for xi in x),) if with_norm else ()))
    return cols

def mono_3ap(cols):
    classes = {}
    for n, c in enumerate(cols): classes.setdefault(c, []).append(n)
    for c, mem in classes.items():
        S = set(mem)
        for i in range(len(mem)):
            for j in range(i + 1, len(mem)):
                a, z = mem[i], mem[j]
                if (a + z) % 2 == 0 and (a + z) // 2 in S:
                    return (a, (a + z) // 2, z), len(classes)
    return None, len(classes)

for r in [256, 400, 625, 1296, 2401, 4096, 6561, 10000, 65536, 100000]:
    b, s = params(r)
    hc = (b + 1) // 2                      # ceil(b/2): H_0 = {0..ceil(b/2)-1}
    bound = 2 ** s * (1 + s * (b - 1) ** 2)
    if b ** s > 300000:
        print(f"r={r}: b={b}, s={s}, b^s={b**s} too large to brute force here"); continue
    w, ncol = mono_3ap(colouring(b, s, hc))
    w1, _ = mono_3ap(colouring(b, s, hc + 1))
    w2, _ = mono_3ap(colouring(b, s, hc, with_norm=False))
    lb = math.exp(math.log(r) ** 2 / (64 * math.log(2)))
    print(f"r={r}: b={b}, s={s}, interval [0,{b**s}), colours used {ncol} <= {bound} <= r: {ncol <= bound <= r}; "
          f"mono 3-AP: {w}; claimed bound exp(L^2/64log2)={lb:.3f} < b^s: {lb < b**s} | "
          f"CONTROL1 wide halves -> {w1} | CONTROL2 no norm -> {w2}")

# (2) exact arithmetic over all r in a range and at the jump points
bad = []
def check(r):
    b, s = params(r)
    L = math.log(r)
    ok = (2 ** s * (1 + s * b * b) <= r and s >= L / (8 * math.log(2)) - 1e-12
          and math.log(b) >= L / 8 - 1e-12 and s * math.log(b) >= L * L / (64 * math.log(2)) - 1e-9
          and b >= 2 and s >= 1)
    if not ok: bad.append(r)
for r in range(256, 2_000_001):
    check(r)
for j in range(8, 401):
    for r in (2 ** j - 1, 2 ** j, 2 ** j + 1):
        if r >= 256: check(r)
for t in range(4, 10 ** 4):
    for r in (t ** 4 - 1, t ** 4):
        if r >= 256: check(r)
print(f"\nexact-arithmetic sweep r in [256, 2e6] plus jump points: failures = {bad[:10]} (count {len(bad)})")
# CONTROL 3a (must FAIL): claim the stronger constant 16 log 2 instead of 64 log 2
f3a = [r for r in range(256, 200001) if params(r)[1] * math.log(params(r)[0]) < math.log(r) ** 2 / (16 * math.log(2))]
print(f"CONTROL3a (b^s >= exp(L^2/(16 log 2)) claimed): fails at {len(f3a)} r in [256,2e5], first {f3a[:3]}")
# CONTROL 3b (must FAIL): b = floor(r^{1/3}) instead of r^{1/4} breaks (transfer:color-count)
f3b = [r for r in range(256, 200001) if 2 ** ((r.bit_length()-1)//4) * (1 + ((r.bit_length()-1)//4) * iroot_floor(r, 3) ** 2) > r]
print(f"CONTROL3b (b = floor(r^(1/3))): colour count exceeds r at {len(f3b)} r in [256,2e5], first {f3b[:3]}")
