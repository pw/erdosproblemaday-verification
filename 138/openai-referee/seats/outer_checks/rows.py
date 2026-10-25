# Brute-force check of the first-family row construction in Prop outer:coloring:
# light labels = multiplicity <= k/M in the word; if L0 >= delta*k light positions,
# order light positions grouping equal labels, deal cyclically into w_max rows.
# Claims: (1) a label occurs at most once per row; (2) every row has >= floor(L0/w_max)
# >= delta*M - 1 positions; (3) rows partition the light positions; (4) if every row has
# each bit on >= 1/4 of its positions then each bit is on >= 1/4 of the light positions.
import random, sys
from fractions import Fraction as Fr
from collections import Counter

def make_rows(word, k, M, nrows=None, grouped=True, rng=None):
    mult = Counter(word)
    light = [j for j in range(k) if mult[word[j]]*M <= k]      # multiplicity <= k/M
    if not light: return None
    wmax = max(mult[word[j]] for j in light)
    if grouped: order = sorted(light, key=lambda j: (word[j], j))
    else: order = light[:]; rng.shuffle(order)
    R = wmax if nrows is None else nrows
    rows = [order[i::R] for i in range(R)]
    return light, wmax, rows

def check(word, k, M, delta, **kw):
    out = make_rows(word, k, M, **kw)
    if out is None: return 'nolight'
    light, wmax, rows = out
    L0 = len(light)
    if L0 < delta*k: return 'few'
    if any(len({word[j] for j in r}) != len(r) for r in rows): return 'REPEAT'
    if min(len(r) for r in rows) < L0 // wmax: return 'SHORT'
    if not (L0 // wmax >= delta*M - 1): return 'ROWSIZE'
    if sorted(j for r in rows for j in r) != sorted(light): return 'PARTITION'
    return 'ok'

def main():
    rng = random.Random(7)
    delta = Fr(1, 10)
    stats = Counter()
    for it in range(4000):
        k = rng.randint(100, 900); M = max(2, int(k**0.5) + rng.randint(0, 3))
        nl = rng.randint(2, k)
        word = [rng.randint(0, nl) if rng.random() < 0.7 else rng.randint(0, 5) for _ in range(k)]
        stats[check(word, k, M, delta)] += 1
    print('correct construction:', dict(stats))
    assert all(s in ('ok', 'few', 'nolight') for s in stats)
    # (4) summing balanced rows: random bits, keep only colorings where every row balanced
    good = bad = 0
    for it in range(3000):
        k = 200; M = 15
        word = [rng.randint(0, 120) for _ in range(k)]
        out = make_rows(word, k, M)
        light, wmax, rows = out
        if len(light) < k/10: continue
        bits = {b: rng.randint(0, 1) for b in set(word)}
        if all(4*sum(bits[word[j]] == v for j in r) >= len(r) for r in rows for v in (0, 1)):
            for v in (0, 1):
                if 4*sum(bits[word[j]] == v for j in light) < len(light): bad += 1
            good += 1
    print('row-balanced colorings tested:', good, '; overall-unbalanced among them:', bad)
    assert bad == 0
    print('--- CONTROLS (each must FAIL) ---')
    stats = Counter()
    for it in range(2000):
        k = rng.randint(100, 900); M = max(2, int(k**0.5))
        word = [rng.randint(0, k//3) for _ in range(k)]
        out = make_rows(word, k, M)
        if out is None or out[1] < 2: continue
        stats[check(word, k, M, delta, nrows=out[1]-1)] += 1
    print('CONTROL deal into w_max-1 rows:', dict(stats))
    stats = Counter()
    for it in range(2000):
        k = rng.randint(100, 900); M = max(2, int(k**0.5))
        word = [rng.randint(0, k//3) for _ in range(k)]
        stats[check(word, k, M, delta, grouped=False, rng=rng)] += 1
    print('CONTROL ungrouped (random) order:', dict(stats))
    return 0
sys.exit(main())
