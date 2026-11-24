"""Step 1: the order-7 graph basis from nauty-geng, our own graph6 decoder and canonical labelling,
orbit-count completeness, and a bijection to model['graph_slack_flags'].

Canonical form = minimum mask over all 7! relabellings (brute force, vectorised over graphs with numpy).
Output: basis.json = list of {mine: canonical mask, rep: decoded geng mask, model_index: h, aut: |Aut|}.
"""
import os
import itertools
import json
import math
import subprocess
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import PIDX, pairs, load_model

N = 7
NP = N * (N - 1) // 2


def decode_graph6(s):
    s = s.strip()
    n = ord(s[0]) - 63
    assert 0 <= n <= 62
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        assert 0 <= v < 64, s
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    # graph6 upper triangle in COLUMN order: x(0,1), x(0,2), x(1,2), x(0,3), ...
    mask = 0
    t = 0
    for j in range(1, n):
        for i in range(j):
            if bits[t]:
                mask |= 1 << PIDX[n][(i, j)]
            t += 1
    # padding bits must be zero
    assert not any(bits[t:]), s
    return n, mask


def perm_tables(n):
    """for each permutation, the destination bit of each source bit"""
    P = list(itertools.permutations(range(n)))
    dest = np.zeros((len(P), n * (n - 1) // 2), dtype=np.int64)
    for pi, perm in enumerate(P):
        for b, (i, j) in enumerate(pairs(n)):
            a, c = perm[i], perm[j]
            if a > c:
                a, c = c, a
            dest[pi, b] = PIDX[n][(a, c)]
    return P, dest


def canon_all(masks, dest):
    """vectorised: canonical (min) form and automorphism count for each mask"""
    masks = np.asarray(masks, dtype=np.int64)
    best = np.full(masks.shape, np.iinfo(np.int64).max, dtype=np.int64)
    aut = np.zeros(masks.shape, dtype=np.int64)
    bitsrc = [(masks >> b) & 1 for b in range(dest.shape[1])]
    for pi in range(dest.shape[0]):
        img = np.zeros(masks.shape, dtype=np.int64)
        for b in range(dest.shape[1]):
            img |= bitsrc[b] << dest[pi, b]
        best = np.minimum(best, img)
        aut += (img == masks)
    return best, aut


def main():
    t0 = time.time()
    out = subprocess.run(['nauty-geng', '-q', str(N)], capture_output=True, text=True, check=True).stdout.split()
    reps = []
    for s in out:
        n, m = decode_graph6(s)
        assert n == N
        reps.append(m)
    print(f'geng lines: {len(reps)}')
    P, dest = perm_tables(N)
    can, aut = canon_all(reps, dest)
    can = [int(x) for x in can]
    aut = [int(x) for x in aut]
    assert len(set(can)) == len(can), 'geng output has isomorphic duplicates under our canonical form'
    orbit_total = sum(math.factorial(N) // a for a in aut)
    assert all(math.factorial(N) % a == 0 for a in aut)
    print(f'distinct canonical forms: {len(set(can))}; sum 7!/|Aut| = {orbit_total}; 2^21 = {2 ** NP}')
    assert orbit_total == 2 ** NP, 'basis not complete'

    model = load_model()
    gs = model['graph_slack_flags']
    assert all(isinstance(x, int) and 0 <= x < 2 ** NP for x in gs)
    mcan, _ = canon_all(gs, dest)
    mcan = [int(x) for x in mcan]
    assert len(set(mcan)) == len(gs) == 1044, 'model list has isomorphic duplicates'
    where = {c: h for h, c in enumerate(mcan)}
    assert set(where) == set(can), 'model list != geng list up to isomorphism'
    rows = [{'mine': c, 'rep': r, 'model_index': where[c], 'aut': a, 'model_mask': gs[where[c]]}
            for c, r, a in zip(can, reps, aut)]
    assert sorted(r['model_index'] for r in rows) == list(range(1044))
    # edges are an invariant: sanity
    for r in rows:
        assert bin(r['rep']).count('1') == bin(r['model_mask']).count('1')
    json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basis.json'), 'w'))
    print(f'bijection to model graph_slack_flags: OK (1044/1044, no duplicates). {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
