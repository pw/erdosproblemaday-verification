"""Independent count of Aut(W) = {pi in Sym(13): pi(W) = W} for the 33-set W, by backtracking over point images
(our own code; pynauty said 48). Also: cluster structure of W under 'meet in exactly 4'."""
from itertools import combinations
W0 = [{1,2,3,4,5},{1,2,3,4,6},{1,2,3,5,6},{1,2,4,5,6},{1,3,4,5,6},{2,3,4,5,6},{3,6,9,10,12},{3,6,9,10,13},{3,6,9,12,13},{3,6,10,12,13},{3,9,10,12,13},{6,9,10,12,13},{4,5,7,8,9},{4,5,7,8,10},{4,5,7,9,10},{4,5,8,9,10},{4,7,8,9,10},{5,7,8,9,10},{1,3,7,11,12},{1,4,7,11,12},{1,5,7,11,12},{1,6,7,11,12},{1,7,9,11,12},{1,7,10,11,12},{1,2,8,11,13},{2,3,8,11,13},{2,4,8,11,13},{2,5,8,11,13},{2,6,8,11,13},{2,7,8,11,13},{2,8,9,11,13},{2,8,10,11,13},{2,8,11,12,13}]
W = {frozenset(s) for s in W0}; pts = list(range(1, 14))
deg = {p: sum(p in S for S in W) for p in pts}
count = 0
def bt(i, img, used):
    global count
    if i == len(pts):
        if {frozenset(img[x] for x in S) for S in W} == W: count += 1
        return
    p = pts[i]
    for q in pts:
        if q in used or deg[q] != deg[p]: continue
        img[p] = q
        # prune: every set fully mapped so far must map into W
        ok = all(frozenset(img[x] for x in S) in W for S in W if all(x in img for x in S))
        if ok: bt(i + 1, img, used | {q})
        del img[p]
bt(0, {}, frozenset())
print('|Aut(W)| =', count, ' point degrees', sorted(deg.values()))
# clusters of the 'meet in 4' graph
adj = {S: [T for T in W if len(S & T) == 4] for S in W}
seen = set(); comps = []
for S in W:
    if S in seen: continue
    st = [S]; comp = set()
    while st:
        x = st.pop()
        if x in comp: continue
        comp.add(x); st += adj[x]
    seen |= comp; comps.append(comp)
for c in comps:
    core = frozenset.intersection(*c); union = frozenset.union(*c)
    print(len(c), 'sets; common core', sorted(core), '; union', sorted(union))
print('pairwise intersections:', sorted({len(a & b) for a, b in combinations(W, 2)}))
