#!/usr/bin/env python3
"""Independent recount of OpenAI family 189's pattern table (paper §9.1, Table 1).
Route: brute force. A pattern = isomorphism class of a linear forest on t vertices whose edges carry positive integer
amounts with total <= B = k - t. Each nontrivial component = a path with r >= 1 edges = an amount tuple up to reversal;
singletons = isolated vertices. We enumerate canonical chain types directly (min(tuple, reversed)), then multisets of them
with vertex budget <= t (remaining vertices = singletons) and amount budget <= B. No code shared with the paper's checkers."""
import itertools, sys
from functools import lru_cache

def compositions(m, r):
    # all r-tuples of positive ints summing to m
    if r == 0:
        if m == 0: yield ()
        return
    for c in itertools.combinations(range(1, m), r - 1):
        parts = []; prev = 0
        for x in c + (m,):
            parts.append(x - prev); prev = x
        yield tuple(parts)

def chain_types(tmax, B):
    types = set()
    for r in range(1, tmax):            # r edges use r+1 vertices <= tmax
        for m in range(r, B + 1):
            for p in compositions(m, r):
                types.add(min(p, p[::-1]))
    return sorted(types, key=lambda p: (len(p), sum(p), p))

def count(t, B):
    T = chain_types(t, B)
    # count multisets of types with sum(len+1) <= t and sum(amount) <= B (the rest of the t vertices are singletons)
    @lru_cache(maxsize=None)
    def f(i, verts, budget):
        if i == len(T): return 1
        p = T[i]; vc = len(p) + 1; ac = sum(p); total = 0; j = 0
        while j * vc <= verts and j * ac <= budget:
            total += f(i + 1, verts - j * vc, budget - j * ac); j += 1
        return total
    return f(0, t, B)

paper = {5:[4,2,1],6:[6,5,2,1],7:[9,9,5,2,1],8:[16,10,5,2,1],9:[25,20,11,5,2],10:[35,24,11,5],11:[60,46,25,11],
         12:[87,51,26],13:[152,104,55],14:[197,118],15:[364,237],16:[468],17:[879]}
pairs = 0; total = 0; bad = 0
for k in range(5, 18):
    ts = list(range(max(3, k // 2), min(8, k) + 1))
    ours = [count(t, k - t) for t in ts]
    pairs += len(ts); total += sum(ours)
    flag = 'OK' if ours == paper[k] else 'MISMATCH'
    if flag != 'OK': bad += 1
    print(k, ts, ours, flag)
print('pairs', pairs, 'patterns', total, 'mismatched rows', bad)
# negative control: the same code with B = k - t + 1 must NOT reproduce the table
neg = sum(count(t, k - t + 1) for k in range(5, 18) for t in range(max(3, k // 2), min(8, k) + 1))
print('negative control (budget+1):', neg, '(must differ from 3099)')
sys.exit(0 if (bad == 0 and total == 3099 and pairs == 42 and neg != 3099) else 1)
