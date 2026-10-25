import itertools, re
K = 2921
# optimal sets from the exact DFS table (lexicographically first optimal set for the smallest n achieving each size)
opt = {}
for line in open('r3table.txt'):
    n, s = map(int, line.split()[:2])
    elems = list(map(int, line.split(':')[1].split()))
    if s not in opt: opt[s] = elems
def bt(j):  # j-th element of the binary-ternary set
    v, p = 0, 1
    while j: v += (j & 1) * p; j >>= 1; p *= 3
    return v
class Leaf:
    def __init__(s, elems, name): s.e = elems; s.size = len(elems); s.M = max(elems); s.name = name
    def elem(s, j): return s.e[j]
class BTLeaf:  # binary-ternary words with t digits
    def __init__(s, t): s.t=t; s.size = 2**t; s.M = (3**t-1)//2; s.name = f"BT{t}"
    def elem(s, j): return bt(j)
class Prod:
    def __init__(s, top, low): s.top, s.low = top, low; s.b = 2*low.M + 1; s.size = top.size*low.size; s.M = top.M*s.b + low.M; s.name = f"({top.name}|{low.name})"
    def elem(s, j): return s.top.elem(j // s.low.size)*s.b + s.low.elem(j % s.low.size)
def prefix_max(T, K): return T.elem(K-1)
leaves = [Leaf(opt[s], f"O{s}") for s in sorted(opt) if s >= 2] + [BTLeaf(t) for t in range(1, 13)]
results = []
# top = a leaf used only as a prefix (needs size >= ceil(K/low.size)); lows = products of 0..2 full leaves
lows = [None] + leaves + [Prod(a, b) for a in leaves for b in leaves]
for low in lows:
    for top in leaves:
        if low is None:
            if top.size >= K: results.append((prefix_max(top, K), top.name)); continue
            continue
        if top.size * low.size < K: continue
        T = Prod(top, low)
        results.append((prefix_max(T, K), T.name))
# top can also be the binary-ternary set of unbounded length (prefix)
class BTinf:
    size = 10**9; M = None; name = "BTinf"
    def elem(s, j): return bt(j)
for low in lows[1:]:
    T = Prod.__new__(Prod); T.top, T.low = BTinf(), low; T.b = 2*low.M+1; T.size = 10**18; T.name = f"(BT*|{low.name})"
    results.append((T.top.elem((K-1)//low.size)*T.b + low.elem((K-1) % low.size), T.name))
results.sort()
for r in results[:15]: print(r)
print("baseline BT prefix:", bt(K-1))
