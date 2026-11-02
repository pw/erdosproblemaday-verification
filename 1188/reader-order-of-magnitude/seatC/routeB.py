"""Route B (seat C): point-driven canonical DFS, decorrelated from Route A (modulus-driven, C).
At each node take the least uncovered point z of Z/L and branch on WHICH modulus m covers it
(class z mod m), with the canonical rule that m is the smallest modulus of the final system
whose class contains z: on choosing m, residue z mod m' is forbidden for every still-unused m' < m.
Each minimal covering system is generated exactly once; a leaf (nothing uncovered) is counted
iff every chosen class still has a private point. No translation/reflection normalisation and
no number-theoretic lemma: the moduli list is whatever is passed in.
usage: python3 routeB.py [--dump] m1 m2 ...
"""
import sys
from math import gcd
from collections import Counter

def run(moduli, dump=False):
    moduli = sorted(set(moduli))
    L = 1
    for n in moduli:
        L = L // gcd(L, n) * n
    FULL = (1 << L) - 1
    # base mask for 0 mod n, then shifted copies
    cls = {}
    for n in moduli:
        base = 0
        for z in range(0, L, n):
            base |= 1 << z
        cls[n] = [((base << a) & FULL) | (base >> (L - a)) if a else base for a in range(n)]
        # sanity: each class mask has exactly L/n bits and lowest bit a
        for a in range(n):
            m = cls[n][a]
            assert bin(m).count('1') == L // n and (m & -m).bit_length() - 1 == a
    K = len(moduli)
    found = []
    stats = Counter()
    nodes = [0]

    def dfs(U, chosen, privs, used, forb):
        nodes[0] += 1
        if U == 0:
            # all privs nonempty is an invariant (checked on insertion)
            found.append(tuple(sorted((n, a) for (n, a) in chosen)))
            return
        z = (U & -U).bit_length() - 1
        newforb_list = []
        for idx, m in enumerate(moduli):
            if used >> idx & 1:
                continue
            r = z % m
            if r in forb[idx]:
                # this modulus cannot cover z; it still forbids nothing new for larger m (it stays unused-or-other)
                newforb_list.append(None)
                continue
            C = cls[m][r]
            # new private sets
            ok = True
            nprivs = []
            for p in privs:
                q = p & ~C
                if q == 0:
                    ok = False
                    break
                nprivs.append(q)
            if ok:
                nprivs.append(U & C)  # nonempty: contains z
                # forbid z mod m' for unused m' < m (indices < idx)
                nforb = forb
                changed = []
                for j in range(idx):
                    if not (used >> j & 1):
                        changed.append(j)
                if changed:
                    nforb = list(forb)
                    for j in changed:
                        nforb[j] = forb[j] | {z % moduli[j]}
                dfs(U & ~C, chosen + [(m, r)], nprivs, used | (1 << idx), nforb)
            newforb_list.append(m)
    dfs(FULL, [], [], 0, [frozenset()] * K)
    return L, found, nodes[0]

if __name__ == '__main__':
    args = sys.argv[1:]
    dump = False
    if args and args[0] == '--dump':
        dump = True
        args = args[1:]
    mods = [int(a) for a in args]
    L, found, nodes = run(mods, dump)
    assert len(found) == len(set(found)), 'duplicate system generated!'
    print('MODULI', ' '.join(map(str, sorted(set(mods)))))
    print('L', L, 'nodes', nodes)
    print('TOTAL', len(found))
    byk = Counter(len(s) for s in found)
    for k in sorted(byk):
        print('CLASSES', k, 'count', byk[k])
    bys = Counter(tuple(n for n, a in s) for s in found)
    for s in sorted(bys):
        print('SET', ' '.join(map(str, s)), ':', bys[s])
    if dump:
        for s in sorted(found):
            print('SYS', ' '.join('%d/%d' % (a, n) for n, a in s))
