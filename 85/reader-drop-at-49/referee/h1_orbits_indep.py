#!/usr/bin/env python3
"""Referee: independent (non-Lean, non-native_decide) recomputation of the H1 orbit inventory.
Admissible tables (OneHighFamilyV2Admissible): symmetric nonneg values on the 24 non-mate pairs of 8
branches, row c summing to 2*IE(profile,c), IE(a,i)=1 if i even and i//2<a else 2.
Group (OneHighProfilePerm): permutations of 8 commuting with i -> i^1 and preserving IE(profile,.).
Check: labelled counts vs Lean's enumerator lengths; #orbits vs inventory per profile; every
inventory row admissible; inventory rows hit every orbit exactly once."""
import itertools, sys, functools
print = functools.partial(print, flush=True)
from collections import Counter
PAIRS = [(c, j) for c in range(8) for j in range(8) if c < j and j != (c ^ 1)]
IDX = {p: k for k, p in enumerate(PAIRS)}
def IE(a, i): return 1 if (i % 2 == 0 and i // 2 < a) else 2
def group(a):
    G = []
    for perm in itertools.permutations(range(8)):
        if all(perm[i ^ 1] == perm[i] ^ 1 for i in range(8)) and all(IE(a, perm[i]) == IE(a, i) for i in range(8)):
            G.append(perm)
    return G
def act(perm, vals):
    out = [0] * 24
    for (c, j), k in IDX.items():
        x, y = perm[c], perm[j]
        out[IDX[(min(x, y), max(x, y))]] = vals[k]
    return tuple(out)
def enum(a):
    tgt = [2 * IE(a, i) for i in range(8)]
    res = []
    last = {}
    for k, (c, j) in enumerate(PAIRS): last[c] = k; last[j] = k
    done_at = [[i for i in range(8) if last[i] == k] for k in range(24)]
    def rec(k, deg, vals):
        if k == 24:
            if deg == tgt: res.append(tuple(vals))
            return
        if k > 0 and any(deg[i] != tgt[i] for i in done_at[k - 1]): return
        c, j = PAIRS[k]
        ub = min(tgt[c] - deg[c], tgt[j] - deg[j])
        for v in range(ub + 1):
            deg[c] += v; deg[j] += v; vals.append(v)
            rec(k + 1, deg, vals)
            vals.pop(); deg[c] -= v; deg[j] -= v
    rec(0, [0] * 8, [])
    return res
inv = Counter(); invrows = {a: [] for a in range(5)}
for line in open("/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/h1_orbit_inventory.compact"):
    v = [int(x) for x in line.split()]
    if len(v) == 25: invrows[v[0]].append(tuple(v[1:]))
lean_enum = {0: 449358, 1: 169668, 2: 70070, 3: 31512, 4: 16692}
lean_inv = {0: 1536, 1: 3662, 2: 4801, 3: 2700, 4: 842}
allok = True
for a in range(5):
    G = group(a)
    L = enum(a)
    Lset = set(L)
    canon = {}
    for t in L:
        if t in canon: continue
        orb = {act(g, t) for g in G}
        m = min(orb)
        for s in orb: canon[s] = m
    orbits = set(canon.values())
    rows = invrows[a]
    adm = all(r in Lset for r in rows)
    hit = Counter(canon[r] for r in rows if r in canon)
    ok = (len(L) == lean_enum[a] and len(orbits) == lean_inv[a] == len(rows) and adm
          and len(hit) == len(orbits) and max(hit.values()) == 1)
    allok &= ok
    print(f"profile {a}: |G|={len(G)} labelled={len(L)} (lean {lean_enum[a]}) orbits={len(orbits)} "
          f"inventory={len(rows)} (lean {lean_inv[a]}) inv_admissible={adm} orbits_hit={len(hit)} max_mult={max(hit.values())} OK={ok}")
print("ALL OK" if allok else "MISMATCH")
