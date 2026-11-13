import sys
from itertools import combinations
n=13
V=[frozenset(c) for c in combinations(range(n),5)]; I={x:i for i,x in enumerate(V)}
W=[{1,2,3,4,5},{1,2,3,4,6},{1,2,3,5,6},{1,2,4,5,6},{1,3,4,5,6},{2,3,4,5,6},{3,6,9,10,12},{3,6,9,10,13},{3,6,9,12,13},{3,6,10,12,13},{3,9,10,12,13},{6,9,10,12,13},{4,5,7,8,9},{4,5,7,8,10},{4,5,7,9,10},{4,5,8,9,10},{4,7,8,9,10},{5,7,8,9,10},{1,3,7,11,12},{1,4,7,11,12},{1,5,7,11,12},{1,6,7,11,12},{1,7,9,11,12},{1,7,10,11,12},{1,2,8,11,13},{2,3,8,11,13},{2,4,8,11,13},{2,5,8,11,13},{2,6,8,11,13},{2,7,8,11,13},{2,8,9,11,13},{2,8,10,11,13},{2,8,11,12,13}]
W=[frozenset(x-1 for x in s) for s in W]
assert len(set(W))==33 and all(len(a&b)!=3 for a,b in combinations(W,2))
k=int(sys.argv[1]); pick=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else list(range(6,6+k))
F=[I[W[0]],I[W[1]]]+[I[W[i]] for i in pick[:k]]
R=[w for w in range(len(V)) if w not in F and all(len(V[w]&V[f])!=3 for f in F)]
for tau in (33-len(F)+1, 33-len(F)):   # 34-|F| -> UNSAT expected ; 33-|F| -> SAT expected
    print(f"{tau} {tau} {len(R)} "+' '.join(str(x+1) for x in R))
