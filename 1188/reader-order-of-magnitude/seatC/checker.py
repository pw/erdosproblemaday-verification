"""Independent checker for distinct covering systems (seat C).
A system is a list of (a, n) pairs meaning the residue class a mod n.
covers(S): every integer mod L=lcm(n) lies in some class.
minimal_private(S): every class has a point (mod L) covered by no other class.
minimal_subfamily(S): no proper subfamily covers (brute force over all 2^k - 2 proper nonempty subfamilies + empty).
"""
from math import gcd
from itertools import combinations

def lcm(a, b):
    return a // gcd(a, b) * b

def L_of(S):
    L = 1
    for a, n in S:
        L = lcm(L, n)
    return L

def masks(S, L):
    out = []
    for a, n in S:
        m = 0
        for z in range(a % n, L, n):
            m |= 1 << z
        out.append(m)
    return out

def covers(S):
    if not S:
        return False
    L = L_of(S)
    full = (1 << L) - 1
    u = 0
    for m in masks(S, L):
        u |= m
    return u == full

def distinct(S):
    ns = [n for a, n in S]
    return len(ns) == len(set(ns)) and all(n >= 2 for n in ns)

def minimal_private(S):
    if not covers(S):
        return False
    L = L_of(S)
    ms = masks(S, L)
    for i, m in enumerate(ms):
        others = 0
        for j, mj in enumerate(ms):
            if j != i:
                others |= mj
        if m & ~others == 0:
            return False
    return True

def minimal_subfamily(S):
    if not covers(S):
        return False
    k = len(S)
    for r in range(0, k):
        for sub in combinations(S, r):
            if covers(list(sub)):
                return False
    return True

def accept(S):
    """minimal distinct covering system?"""
    return distinct(S) and covers(S) and minimal_private(S)

if __name__ == '__main__':
    pos = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
    neg_add = pos + [(3, 8)]
    print('positive control', pos)
    print('  covers', covers(pos), 'distinct', distinct(pos), 'minimal_private', minimal_private(pos), 'minimal_subfamily', minimal_subfamily(pos), '-> ACCEPT' if accept(pos) else '-> REJECT')
    print('negative control (+ 3 mod 8)', neg_add)
    print('  covers', covers(neg_add), 'distinct', distinct(neg_add), 'minimal_private', minimal_private(neg_add), 'minimal_subfamily', minimal_subfamily(neg_add), '-> ACCEPT' if accept(neg_add) else '-> REJECT')
    for i in range(len(pos)):
        neg = pos[:i] + pos[i+1:]
        print('negative control (minus %s)' % (pos[i],), 'covers', covers(neg), 'minimal_private', minimal_private(neg), '-> ACCEPT' if accept(neg) else '-> REJECT')
    # repeated modulus negative
    rep = [(0, 2), (1, 2)]
    print('negative control (0 mod 2, 1 mod 2: covers+minimal but moduli not distinct)', 'covers', covers(rep), 'minimal_private', minimal_private(rep), 'distinct', distinct(rep), '-> ACCEPT' if accept(rep) else '-> REJECT')
    # paper's 18-class example for x=48
    ex48 = [(2,3),(3,4),(4,5),(1,6),(5,8),(3,9),(2,10),(10,12),(1,15),(9,16),(6,18),(8,20),(12,24),(10,30),(18,36),(0,40),(36,45),(33,48)]
    print('paper 18-class example (x=48): n=%d distinct %s covers %s minimal_private %s max modulus %d' % (len(ex48), distinct(ex48), covers(ex48), minimal_private(ex48), max(n for a,n in ex48)))
    ex216 = [(2,3),(2,4),(1,6),(0,8),(3,9),(4,12),(15,18),(15,24),(9,27),(24,36),(45,54),(36,72),(81,108),(27,216)]
    print('paper 14-class example (divisors of 216): n=%d distinct %s covers %s minimal_private %s; moduli = all divisors of 216 except 1,2: %s' % (len(ex216), distinct(ex216), covers(ex216), minimal_private(ex216), sorted(n for a,n in ex216) == [d for d in range(3,217) if 216 % d == 0]))
