# Exhaustive check of |dE S| >= |S| log2(2^r/|S|) for nonempty S in {0,1}^r, r<=4
import math, itertools
for r in range(1,5):
    N=1<<r; worst=None
    for mask in range(1,1<<N):
        S=[v for v in range(N) if mask>>v&1]; s=len(S)
        bd=sum(1 for v in S for j in range(r) if not (mask>>(v^(1<<j))&1))
        rhs=s*math.log2(N/s)
        slack=bd-rhs
        if worst is None or slack<worst[0]: worst=(slack,S,bd,rhs)
        assert bd >= rhs-1e-9, (r,S,bd,rhs)
    print('r=%d all %d subsets ok; min slack %.4f at |S|=%d'%(r,(1<<N)-1,worst[0],len(worst[1])))
