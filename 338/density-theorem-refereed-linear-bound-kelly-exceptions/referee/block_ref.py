"""Referee's independent test of Theorem 2 (README): l*(C,3) <= 4 for finite C in (1, inf).
Own code: sorted sweep for the component of 0 (not the fixed-point loop of block338.py); l* = least l >= 1
(definition in the README) rather than starting from l = h; exact Fractions throughout.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
import random, sys

def comp0(ivs):
    """right end of the connected component containing 0 of a union of closed intervals [a,b]"""
    ivs = sorted(ivs)
    assert any(a <= 0 <= b for a, b in ivs)
    end = None
    for a, b in ivs:
        if a <= 0 <= b and end is None:
            end = b
    # sweep from the start: everything with a <= end extends
    end = F(0)
    for a, b in ivs:
        if a > end: break
        if b > end: end = b
    return end

def rho(C, h):
    ivs = []
    for k in range(h + 1):
        for S in combinations_with_replacement(C, k):
            s = sum(S, F(0)); ivs.append((s, s + h - k))
    return comp0(ivs)

def rl(C, l):
    ivs = []
    for k in range(min(l, len(C)) + 1):
        for T in combinations(C, k):
            s = sum(T, F(0)); ivs.append((s, s + l - k))
    return comp0(ivs)

def lstar(C, h=3):
    R = rho(C, h); l = 1
    while rl(C, l) < R: l += 1
    return l, R

def rand_C(rnd):
    k = rnd.randint(1, 7)
    C = set()
    mode = rnd.random()
    while len(C) < k:
        u = rnd.random()
        if u < 0.25:
            c = F(rnd.randint(3, 40), 2)                      # halves
        elif u < 0.45:
            c = F(rnd.randint(4, 60), 3)                      # thirds
        elif u < 0.65:
            q = rnd.randint(10 ** 3, 10 ** 6); c = 1 + F(rnd.randint(1, 15 * q), q)   # large denominators
        elif u < 0.75:
            q = rnd.randint(2, 10 ** 6); c = 1 + F(1, q)      # just above 1
        else:
            if C:                                            # near-ties with an existing element
                base = rnd.choice(sorted(C))
                eps = F(1, rnd.randint(2, 10 ** 6)) * rnd.choice([-1, 1])
                c = rnd.choice([base - F(1, 2), base - F(1, 2) + eps, base + F(1, 2), base + 1, base + eps,
                                2 * base, 2 * base + 1, base + 2, (base + 1) / 2, base - 1])
            else:
                c = F(rnd.randint(11, 200), 10)
        if c > 1: C.add(c)
    return sorted(C)

def main():
    rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 338)
    # controls: known values
    for C, exp in (([F(2)], 4), ([F(2), F(4)], None)):
        print("control", [str(c) for c in C], "h=3 l*,rho =", lstar(C, 3), "expected", exp)
    print("control HHP h=4 C={2,4}:", lstar([F(2), F(4)], 4), "(README: reach 11, l* 7)")
    print("control h=4 C={4,5}:", lstar([F(4), F(5)], 4), "(README: reach 16, l* 9)")
    hist = {}
    worst = None
    T = 20000
    for i in range(T):
        C = rand_C(rnd)
        l, R = lstar(C)
        hist[l] = hist.get(l, 0) + 1
        if worst is None or l > worst[0]: worst = (l, [str(c) for c in C], str(R))
    print(f"random h=3, {T} sets (|C|<=7): l* histogram {dict(sorted(hist.items()))}; max {worst}")
    # hill-climb: try to push l* above 4
    best = (0, None)
    for trial in range(300):
        C = rand_C(rnd)
        l, _ = lstar(C)
        for it in range(60):
            D = list(C)
            op = rnd.random()
            if op < 0.4 and D:
                j = rnd.randrange(len(D)); D[j] = D[j] + F(rnd.randint(-20, 20), rnd.choice([2, 4, 8, 1000]))
            elif op < 0.7 and len(D) < 7:
                D.append(rnd.choice(D) - F(1, 2) if D else F(2))
            elif D and len(D) > 1:
                D.pop(rnd.randrange(len(D)))
            D = sorted(set(d for d in D if d > 1))
            if not D: continue
            l2, _ = lstar(D)
            if l2 >= l: C, l = D, l2
        if l > best[0]: best = (l, [str(c) for c in C])
    print("hill-climb max l*(C,3):", best)
    # exhaustive grid: all C subset of {k/4 : 5<=k<=40} with |C|<=3
    grid = [F(k, 4) for k in range(5, 41)]
    mx = 0; arg = None; cnt = 0
    for m in (1, 2, 3):
        for C in combinations(grid, m):
            l, _ = lstar(list(C)); cnt += 1
            if l > mx: mx, arg = l, [str(c) for c in C]
    print(f"exhaustive grid quarters (1,10], |C|<=3, {cnt} sets: max l* = {mx} at {arg}")

main()
