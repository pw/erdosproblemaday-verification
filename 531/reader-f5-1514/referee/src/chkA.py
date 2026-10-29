#!/usr/bin/env python3
"""Referee checker A (independent; Python big-int bitsets, ASCENDING order).
For colour c let M_c = bitmask of integers in [1..N] with colour c (bit i <-> integer i).
Given a chosen set with subset-sum multiset S (incl. 0) and total T, the admissible next
elements x (> last, and x+T <= N) are exactly the set bits of  AND_{s in S} (M_c >> s).
Counts all k-sets of distinct positive integers whose 2^k-1 nonempty subset sums are all <= N
and all of colour c.
usage: chkA.py FILE K [--flip p ...] [--print m]   |   chkA.py --zero N K
"""
import sys
def load(path):
    raw = open(path, 'rb').read()
    line = raw.split(b'\n')[0]
    assert all(ch in b'01' for ch in line), 'bad char'
    return [None] + [ch - 48 for ch in line]

def count(colour, N, K, maxprint=0):
    masks = [0, 0]
    for i in range(1, N + 1):
        masks[colour[i]] |= (1 << i)
    full = (1 << (N + 1)) - 1
    total_cnt = [0, 0]
    examples = []
    def rec(c, chosen, sums, T, last):
        if len(chosen) == K:
            total_cnt[c] += 1
            if len(examples) < maxprint:
                examples.append((c, tuple(chosen)))
            return
        allowed = full
        for s in sums:
            allowed &= (masks[c] >> s)
            if not allowed:
                return
        # x > last and x + T <= N
        lo = last + 1
        hi = N - T
        if hi < lo:
            return
        allowed &= ((1 << (hi + 1)) - 1) & ~((1 << lo) - 1)
        while allowed:
            low = allowed & -allowed
            x = low.bit_length() - 1
            allowed ^= low
            rec(c, chosen + [x], sums + [s + x for s in sums], T + x, x)
    for c in (0, 1):
        rec(c, [], [0], 0, 0)
    return total_cnt, examples

if __name__ == '__main__':
    a = sys.argv[1:]
    maxprint = 0
    if '--print' in a:
        i = a.index('--print'); maxprint = int(a[i + 1]); del a[i:i + 2]
    if a[0] == '--zero':
        N, K = int(a[1]), int(a[2]); colour = [None] + [0] * N
    else:
        colour = load(a[0]); N = len(colour) - 1; K = int(a[1])
        if '--flip' in a:
            for p in a[a.index('--flip') + 1:]:
                colour[int(p)] ^= 1
    cnt, ex = count(colour, N, K, maxprint)
    for c, s in ex:
        print('MONO colour', c, *s)
    print(f'N={N} K={K} mono_total={sum(cnt)} (colour0={cnt[0]} colour1={cnt[1]})')
