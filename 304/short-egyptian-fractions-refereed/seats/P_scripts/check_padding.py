# Lemma 7.2 (marker-preserving padding) implemented exactly as written; also (6.2) padding injectivity.
import sys, pickle
from fractions import Fraction
from collections import Counter
res = pickle.load(open(sys.argv[1], 'rb'))
KMAX = max(res)

def smallest_factor(s):
    for a in range(2, int(s**0.5)+1):
        if s % a == 0: return a
    return None

def pad_keep(t, m):
    """Lemma 7.2 construction. t sorted distinct tuple, sum 1, len>=3, m in t."""
    t = list(t); r = len(t)
    if m != t[-1]:
        b = t[-1]; new = t[:-1] + [b+1, b*(b+1)]; return tuple(sorted(new)), 'split-largest'
    v = t[-1]; s = t[-2]
    if v != s+1 and v != s*(s+1):
        new = t[:-2] + [s+1, s*(s+1), v]; return tuple(sorted(new)), 'split-second'
    a = smallest_factor(s)
    if a is None:
        raise RuntimeError(f"prime exceptional case occurred: {t}, m={m}")  # lemma says impossible
    b = s // a
    new = t[:-2] + [s+a, b*(s+a), v]
    return tuple(sorted(new)), 'composite-alt'

stats = Counter(); fails = 0; examples = {}
for r in range(3, KMAX):
    for t in res[r]:
        for m in t:
            new, branch = pad_keep(t, m)
            stats[(r, branch)] += 1
            examples.setdefault(branch, (t, m, new))
            ok = (len(new) == r+1 and len(set(new)) == r+1 and m in new
                  and sum(Fraction(1, n) for n in new) == 1)
            if not ok: fails += 1; print("FAIL", t, m, new)
            if new not in set(res[r+1]) if False else False: pass
    # every output must be in res[r+1]
R = {r: set(res[r]) for r in res}
for r in range(3, KMAX):
    for t in res[r]:
        for m in t:
            new, _ = pad_keep(t, m)
            assert new in R[r+1]
print("Lemma 7.2 branch usage:", dict(stats))
print("examples:", examples)
print("Lemma 7.2 FAILS:", fails)

# Exceptional configuration counts: m = n_r and n_r in {n_{r-1}+1, n_{r-1}(n_{r-1}+1)}
exc = Counter()
for r in range(3, KMAX+1):
    for t in res[r]:
        s, v = t[-2], t[-1]
        if v == s+1: exc[(r, 'v=s+1', 'prime' if smallest_factor(s) is None else 'composite')] += 1
        if v == s*(s+1): exc[(r, 'v=s(s+1)', 'prime' if smallest_factor(s) is None else 'composite')] += 1
print("exceptional (v,s) configurations:", dict(exc))

# (6.2) padding: split largest; injectivity on all expansions of each length
for r in range(2, KMAX):
    imgs = {}
    for t in res[r]:
        v = t[-1]; new = tuple(sorted(list(t[:-1]) + [v+1, v*(v+1)]))
        assert sum(Fraction(1,n) for n in new) == 1 and len(set(new)) == r+1
        # inverse map as described: delete two largest, reinsert second largest minus one
        inv = tuple(sorted(list(new[:-2]) + [new[-2]-1]))
        assert inv == t
        assert new not in imgs; imgs[new] = t
    print(f"(6.2) padding injective on length {r}: {len(imgs)} images from {len(res[r])}")
