# Seat F own enumerator: brute force over ORDERED lists of ORIENTED chains, canonicalised afterwards.
import json, sys, itertools
from collections import Counter
from math import comb

def oriented_chains(maxv, B):
    # all tuples of positive ints with len <= maxv-1 and sum <= B  (chain with len+1 vertices)
    out = [()]
    frontier = [()]
    while frontier:
        nf = []
        for c in frontier:
            if len(c) + 1 >= maxv:  # can't add an edge (would need len+2 <= maxv)
                continue
            for q in range(1, B - sum(c) + 1):
                nc = c + (q,)
                out.append(nc); nf.append(nc)
        frontier = nf
    return out

def ordered_lists(t, B, chains):
    # all ordered sequences of oriented chains with total vertices t, total amount <= B
    if t == 0:
        yield ()
        return
    for c in chains:
        v = len(c) + 1
        s = sum(c)
        if v <= t and s <= B:
            for rest in ordered_lists(t - v, B - s, chains):
                yield (c,) + rest

def canon(lst):
    return tuple(sorted(min(c, c[::-1]) for c in lst))

def count(t, B):
    chains = oriented_chains(t, B)
    S = set()
    for lst in ordered_lists(t, B, chains):
        S.add(canon(lst))
    return S

# generating-function count, (9.5), done by direct polynomial arithmetic (independent code)
def gf_count(t, B):
    def a(r, m):
        tot = comb(m - 1, r - 1)
        if r % 2 == 0:
            s = r // 2
            pal = comb(m // 2 - 1, s - 1) if m % 2 == 0 else 0
        else:
            s = (r - 1) // 2
            pal = comb((m - 1) // 2, s)
        assert (tot + pal) % 2 == 0
        return (tot + pal) // 2
    # poly as dict (x,y)->coef truncated x<=t, y<=B
    poly = Counter({(0, 0): 1})
    def mul_inv_power(poly, dx, dy, e):
        # multiply by (1 - x^dx y^dy)^(-e) = sum_j C(e+j-1, j) x^{dx j} y^{dy j}
        new = Counter()
        for (i, j), c in poly.items():
            jj = 0
            while i + dx * jj <= t and j + dy * jj <= B:
                new[(i + dx * jj, j + dy * jj)] += c * comb(e + jj - 1, jj)
                jj += 1
        return new
    poly = mul_inv_power(poly, 1, 0, 1)
    for r in range(1, t):
        for m in range(r, B + 1):
            e = a(r, m)
            if e:
                poly = mul_inv_power(poly, r + 1, m, e)
    return sum(c for (i, j), c in poly.items() if i == t and j <= B)

summ = json.load(open(sys.argv[1]))
cov = {(r['k'], r['t']): r for r in summ['coverage']}
dom = [(k, t) for k in range(5, 18) for t in range(max(3, k // 2), min(8, k) + 1)]
# re-derive the domain from first principles: t in [max(3,floor(k/2)), k] (clq:bound) and t<=8 (finite stage), k>=5 (sec 4)
dom2 = sorted((k, t) for k in range(5, 40) for t in range(3, 9) if max(3, k // 2) <= t <= k)
print('domain pairs', len(dom), 'first-principles pairs', len(dom2), 'equal', sorted(dom) == dom2)
tot = 0; bad = 0
perk = Counter()
for k, t in dom:
    S = count(t, k - t)
    n1 = len(S); n2 = gf_count(t, k - t)
    by = Counter(sum(map(sum, p)) for p in S)
    c = cov[(k, t)]
    ok = (n1 == n2 == c['patterns']) and {str(a): b for a, b in by.items()} == {str(a): b for a, b in c['by_amount'].items()}
    tot += n1; perk[k] += n1
    if not ok: bad += 1
    print(k, t, 'brute', n1, 'gf', n2, 'summary', c['patterns'], 'by_amount_ok', ok)
print('TOTAL', tot, 'mismatching pairs', bad)
print('per k', dict(perk))
