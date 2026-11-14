"""Structure of W and a generator of its copies (our own description; checked against Appendix A in selftest)."""
from itertools import combinations, permutations
import random
N = 13
V = [frozenset(c) for c in combinations(range(N), 5)]
IDX = {s: i for i, s in enumerate(V)}

def copy_from_roles(inf, a, b, S12, S13, S23):
    """a=(a1,a2,a3), b=(b1,b2,b3), S_ij = shared pair of blocks i,j. Returns list of 33 frozensets."""
    B1 = {a[0], b[0]} | set(S12) | set(S13)
    B2 = {a[1], b[1]} | set(S12) | set(S23)
    B3 = {a[2], b[2]} | set(S13) | set(S23)
    out = []
    for B in (B1, B2, B3):
        assert len(B) == 6
        out += [frozenset(B - {x}) for x in B]
    core6 = {inf, *a}; core9 = {inf, *b}
    shared = set(S12) | set(S13) | set(S23)
    out += [frozenset(core6 | {x}) for x in shared]
    out += [frozenset(core9 | {y}) for y in range(N) if y not in core9]
    return out

def random_copy(rng=random):
    p = list(range(N)); rng.shuffle(p)
    return copy_from_roles(p[0], p[1:4], p[4:7], p[7:9], p[9:11], p[11:13])

# Appendix A family (1-based) as printed in the submission
W0 = [{1,2,3,4,5},{1,2,3,4,6},{1,2,3,5,6},{1,2,4,5,6},{1,3,4,5,6},{2,3,4,5,6},{3,6,9,10,12},{3,6,9,10,13},{3,6,9,12,13},{3,6,10,12,13},{3,9,10,12,13},{6,9,10,12,13},{4,5,7,8,9},{4,5,7,8,10},{4,5,7,9,10},{4,5,8,9,10},{4,7,8,9,10},{5,7,8,9,10},{1,3,7,11,12},{1,4,7,11,12},{1,5,7,11,12},{1,6,7,11,12},{1,7,9,11,12},{1,7,10,11,12},{1,2,8,11,13},{2,3,8,11,13},{2,4,8,11,13},{2,5,8,11,13},{2,6,8,11,13},{2,7,8,11,13},{2,8,9,11,13},{2,8,10,11,13},{2,8,11,12,13}]
WA = {frozenset(x - 1 for x in s) for s in W0}

def independent(F):
    return all(len(x & y) != 3 for x, y in combinations(F, 2))

if __name__ == '__main__':
    # Appendix A in role form (0-based: subtract 1): INF=11->10; a=(1,12,7)->(0,11,6); b=(2,13,8)->(1,12,7);
    # S12={3,6}->{2,5}; S13={4,5}->{3,4}; S23={9,10}->{8,9}
    C = copy_from_roles(10, (0, 11, 6), (1, 12, 7), (2, 5), (3, 4), (8, 9))
    assert set(C) == WA and len(set(C)) == 33, 'role description does not reproduce Appendix A'
    random.seed(1)
    for _ in range(2000):
        C = random_copy(); assert len(set(C)) == 33 and independent(C)
    # negative control: a broken role map (shared pair assigned to the wrong block) is NOT independent
    bad = copy_from_roles(10, (0, 11, 6), (1, 12, 7), (2, 3), (5, 4), (8, 9))
    print('role form reproduces Appendix A: OK; 2000 random copies independent, size 33: OK;',
          'relabelled-but-still-a-copy control independent:', independent(bad))
    # true negative: swap one a_i with a shared point inside the 6-core only
    C2 = list(WA); C2[0] = frozenset({0, 1, 2, 3, 6})
    print('planted non-independent family detected:', not independent(C2))
