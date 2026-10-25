#!/usr/bin/env python3
"""Cross-check: the pattern lists hard-coded in OpenAI's Lean (route A: CycleClique/Patterns{k}x{t}.lean, defs patterns_k_t_i)
equal, as SETS with no duplicates, the patterns produced by OUR brute-force enumerator (count_patterns.py logic, B = k - t).
Our canonical form: each chain = min(tuple, reversed); components sorted lexicographically (Python tuple order on lists of ints,
singletons = empty tuple first). Exit 0 iff all 42 pairs agree."""
import re, glob, itertools, sys, ast
D = '/tmp/oaimath/189/repo/lean/OAI/Combinatorics/Ramsey/CycleClique'
def compositions(m, r):
    for c in itertools.combinations(range(1, m), r - 1):
        parts = []; prev = 0
        for x in c + (m,):
            parts.append(x - prev); prev = x
        yield tuple(parts)
def our_patterns(t, B):
    types = sorted({min(p, p[::-1]) for r in range(1, t) for m in range(r, B + 1) for p in compositions(m, r)})
    out = set()
    def rec(i, verts, budget, chosen):
        if i == len(types):
            out.add(tuple(sorted(chosen + [()] * verts))); return
        p = types[i]; vc = len(p) + 1; ac = sum(p); j = 0
        while j * vc <= verts and j * ac <= budget:
            rec(i + 1, verts - j * vc, budget - j * ac, chosen + [p] * j); j += 1
    rec(0, t, B, []); return out
bad = 0; tot = 0
for f in sorted(glob.glob(D + '/Patterns*x*.lean')):
    k, t = map(int, re.search(r'Patterns(\d+)x(\d+)\.lean', f).group(1, 2))
    src = open(f).read()
    lists = []
    for m in re.finditer(r'noncomputable def patterns_%d_%d_\d+ : List \(List \(List ℕ\)\) := (\[.*\])\s*$' % (k, t), src, re.M):
        lists += ast.literal_eval(m.group(1))
    lean = [tuple(sorted(tuple(c) for c in P)) for P in lists]
    lean_set = set(lean)
    ours = our_patterns(t, max(0, k - t - 1))
    dup = len(lean) - len(lean_set)
    ok = (lean_set == ours and dup == 0)
    # also check each Lean pattern is already in canonical form (chains reversal-normalised, components sorted)
    canon = all(tuple(tuple(c) for c in P) == tuple(sorted(min(tuple(c), tuple(c)[::-1]) for c in P)) for P in lists)
    tot += len(lean)
    if not (ok and canon): bad += 1
    print(f'k={k} t={t} lean={len(lean)} ours={len(ours)} dup={dup} canonical={canon} {"OK" if ok and canon else "MISMATCH"}')
print('pairs', len(glob.glob(D + '/Patterns*x*.lean')), 'lean patterns total', tot, 'bad pairs', bad)
sys.exit(0 if bad == 0 and tot == 3099 else 1)
