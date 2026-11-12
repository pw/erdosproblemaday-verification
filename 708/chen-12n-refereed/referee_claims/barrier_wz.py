# Does the barrier survive for the completely additive w_z (z_p=1) form, which is what
# the proof of Thm chain19 actually consumes (sum_a w_z(a) <= cn + sum_{k<=m}(w_z(k)-c)^+ ...)?
# Search clusters of consecutive primes p_1..p_r with p_r < sqrt2 * p_1, m = p_{r-1} p_r,
# window centred at P = prod p_i; compute both sides exactly by sieve (k<=m) and residues (window).
from fractions import Fraction as Fr
import sys

def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]

PR = primes_upto(20000)
c = Fr(19, 10)

def both_sides(ps):
    m = ps[-2] * ps[-1]
    w = bytearray(m + 1)  # w_z on [1,m] restricted to cluster (z_p = 1)
    for p in ps:
        q = p
        while q <= m:
            for k in range(q, m + 1, q): w[k] += 1
            q *= p
    LHS_S = Fr(0); LHS_W = Fr(0)
    sv = bytearray(m + 1)
    for p in ps:
        for k in range(p, m + 1, p): sv[k] += 1
    for k in range(1, m + 1):
        if w[k] >= 2: LHS_W += w[k] - c
        if sv[k] >= 2: LHS_S += sv[k] - c
    P = 1
    for p in ps: P *= p
    x = P - (m + 1) // 2
    assert x + 1 <= P <= x + m
    info = {}
    for p in ps:
        r = (-x) % p
        i0 = r if r >= 1 else p
        for i in range(i0, m + 1, p):
            t = (x + i) % (p ** 8); v = 0
            if t == 0: v = 8
            else:
                while t % p == 0: t //= p; v += 1
            s, ww = info.get(i, (0, 0)); info[i] = (s + 1, ww + v)
    RHS_S = sum(s - 1 for s, ww in info.values() if s > 1)
    RHS_W = sum(ww - 1 for s, ww in info.values() if ww > 1)
    return m, LHS_S, RHS_S, LHS_W, RHS_W

# 1) the paper's instance
ps = [p for p in PR if 503 <= p <= 641]
print("paper instance r=21:", both_sides(ps))
# 2) longest clusters of consecutive primes p_1..p_r with p_r^2 < 2 p_1^2, scanning p_1
found = None
for idx in range(len(PR)):
    p1 = PR[idx]
    if p1 < 1000: continue
    j = idx
    while j + 1 < len(PR) and PR[j + 1] ** 2 < 2 * p1 * p1: j += 1
    ps = PR[idx:j + 1]
    r = len(ps)
    if r < 60: continue
    m, LS, RS, LW, RW = both_sides(ps)
    print("p1=%d r=%d m=%d  S-form: %s vs %s   w-form: %s vs %s  w-fails=%s" % (p1, r, m, LS, RS, LW, RW, LW > RW), flush=True)
    if LW > RW:
        found = (p1, r); break
print("first w-form failure at c=19/10:", found)
