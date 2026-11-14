"""All maximum independent sets (size 12) of J(10,5,3) = G(10,5,3): vertices 5-subsets of {0..9}, adjacent iff they share exactly 3.
Enumerate those containing v0 = {0,1,2,3,4} (the graph is vertex-transitive), by plain backtracking on bitsets; then all of them by
applying Sym(10) orbit bookkeeping: total = (#containing v0) * 252 / 12."""
import sys, json
from itertools import combinations, permutations
N, K, T, A = 10, 5, 3, 12
V = [frozenset(c) for c in combinations(range(N), K)]; IDX = {s: i for i, s in enumerate(V)}; n = len(V)
adj = [0] * n
for i in range(n):
    for j in range(n):
        if i != j and len(V[i] & V[j]) == T: adj[i] |= 1 << j
found = []
def ext(cur, cand, last):
    if len(cur) == A: found.append(tuple(cur)); return
    if len(cur) + bin(cand).count('1') < A: return
    c = cand
    while c:
        low = c & -c; v = low.bit_length() - 1; c ^= low
        if len(cur) + 1 + bin(c & ~adj[v]).count('1') < A: continue
        ext(cur + [v], c & ~adj[v], v)
full = (1 << n) - 1
ext([0], full & ~adj[0] & ~1, 0)
print('independent 12-sets containing {0,1,2,3,4}:', len(found), '=> total', len(found) * n // A, flush=True)
# is there any independent 13-set? (alpha check, same code)
A = 13; f12 = found; found = []; ext([0], full & ~adj[0] & ~1, 0); print('independent 13-sets containing v0:', len(found)); found = f12
# classify under Sym(10): invariant = sorted point degrees + cluster structure
def clusters(F):
    F = [V[i] for i in F]; seen = set(); out = []
    for s in F:
        if s in seen: continue
        comp = set(); st = [s]
        while st:
            x = st.pop()
            if x in comp: continue
            comp.add(x); st += [t for t in F if len(t & x) == 4 and t not in comp]
        seen |= comp
        core = frozenset.intersection(*comp); uni = frozenset.union(*comp)
        out.append((len(comp), len(core), len(uni)))
    return tuple(sorted(out))
types = {}
for F in found:
    deg = tuple(sorted(sum(1 for i in F if p in V[i]) for p in range(N)))
    types.setdefault((deg, clusters(F)), []).append(F)
for k, lst in sorted(types.items(), key=lambda kv: -len(kv[1])):
    print('type: point degrees', k[0], '| clusters (size, |core|, |union|):', k[1], '| count containing v0:', len(lst), '| total', len(lst) * n // A if False else len(lst) * 252 // 12)
    print('   example:', [sorted(V[i]) for i in lst[0]])
json.dump([list(F) for F in found], open('mis10_v0.json', 'w'))
