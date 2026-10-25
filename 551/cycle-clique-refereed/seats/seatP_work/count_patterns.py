# Independent recount of Table 1 (pattern counts) with seatP's own generator (model_s8.patterns),
# plus a brute-force cross-check: canonical forms of ALL labelled weighted linear forests for small t.
import sys, itertools
sys.path.insert(0, '/tmp/oaimath/189/seats/seatP_work')
from model_s8 import patterns
paper = {5:[4,2,1],6:[6,5,2,1],7:[9,9,5,2,1],8:[16,10,5,2,1],9:[25,20,11,5,2],10:[35,24,11,5],11:[60,46,25,11],
         12:[87,51,26],13:[152,104,55],14:[197,118],15:[364,237],16:[468],17:[879]}
tot = 0; pairs = 0; ok = True
for k in range(5, 18):
    ts = [t for t in range(max(3, k//2), min(8, k)+1)]
    cnt = [len(patterns(t, k-t)) for t in ts]
    pairs += len(ts); tot += sum(cnt)
    if cnt != paper[k]: ok = False; print("MISMATCH k=%d" % k, ts, cnt, paper[k])
print("pairs:", pairs, "total patterns:", tot, "matches Table 1:", ok)
# brute force: all linear forests on t labelled vertices with positive amounts, total <= B, up to isomorphism,
# canonicalised independently (multiset of min(tuple, reversed tuple)) -> compare counts
def brute(t, B):
    # enumerate set partitions of {0..t-1} into ordered paths is expensive; instead enumerate edge subsets of K_t
    verts = range(t); E = list(itertools.combinations(verts, 2)); seen = set()
    for m in range(0, min(t-1, B) + 1):
        for es in itertools.combinations(E, m):
            deg = [0]*t
            for u, w in es: deg[u] += 1; deg[w] += 1
            if max(deg, default=0) > 2: continue
            # acyclic check + extract paths
            adj = {v: [] for v in verts}
            for u, w in es: adj[u].append(w); adj[w].append(u)
            seenv = set(); comps = []; cyc = False
            for v in verts:
                if v in seenv: continue
                # walk component
                stack = [v]; comp = set()
                while stack:
                    x = stack.pop()
                    if x in comp: continue
                    comp.add(x); stack.extend(adj[x])
                seenv |= comp
                ne = sum(len(adj[x]) for x in comp) // 2
                if ne != len(comp) - 1: cyc = True; break
                ends = [x for x in comp if len(adj[x]) <= 1]
                start = min(ends); order = [start]; prev = None
                while True:
                    nxt = [y for y in adj[order[-1]] if y != prev]
                    if not nxt: break
                    prev = order[-1]; order.append(nxt[0])
                comps.append(order)
            if cyc: continue
            # assign amounts to the m edges: all compositions with sum <= B
            elist = []
            for order in comps:
                elist.append([(order[i], order[i+1]) for i in range(len(order)-1)])
            nE = sum(len(x) for x in elist)
            for amts in itertools.product(range(1, B+1), repeat=nE):
                if sum(amts) > B: continue
                it = iter(amts); key = []
                for ch in elist:
                    tp = tuple(next(it) for _ in ch)
                    key.append(min(tp, tp[::-1]))
                seen.add(tuple(sorted(key)))
    return len(seen)
for (t, B) in [(3,2),(4,2),(5,2),(4,4),(5,3),(6,2),(5,5),(6,3)]:
    b = brute(t, B); g = len(patterns(t, B))
    print("brute vs generator t=%d B=%d: %d %d %s" % (t, B, b, g, "OK" if b == g else "MISMATCH"))
