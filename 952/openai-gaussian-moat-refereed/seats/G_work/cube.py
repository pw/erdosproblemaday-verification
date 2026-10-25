# Exhaustive check of (4.x): |boundary_E S| >= |S| log2(2^r/|S|) for all nonempty S in {0,1}^r, r<=4,
# plus the outside-vertex-boundary corollary and the inequality h2(a) >= 1-|1-2a| used in the induction.
import math, itertools
worst_overall=None
for r in range(0,5):
    N=1<<r
    edges=[(u,u^(1<<i)) for u in range(N) for i in range(r) if u< (u^(1<<i))]
    minslack=1e9; minslack_v=1e9; cnt=0
    for mask in range(1,1<<N):
        S=[u for u in range(N) if mask>>u&1]
        s=len(S)
        eb=sum(1 for (u,v) in edges if ((mask>>u)&1)!=((mask>>v)&1))
        rhs=s*math.log2(N/s)
        minslack=min(minslack, eb-rhs)
        # outside vertex boundary
        out=set()
        for u in S:
            for i in range(r):
                v=u^(1<<i)
                if not (mask>>v)&1: out.add(v)
        if r>0:
            minslack_v=min(minslack_v, len(out)-rhs/r)
        cnt+=1
    print(f"r={r}: {cnt} nonempty subsets; min(|dE S| - |S|log2(2^r/|S|)) = {minslack:.6f}; min(|dV S| - |S|log2(2^r/|S|)/r) = {minslack_v if r>0 else 'n/a'}")
# h2(a) >= 1-|1-2a|
def h2(a):
    if a in (0,1): return 0.0
    return -a*math.log2(a)-(1-a)*math.log2(1-a)
m=min(h2(i/100000)-(1-abs(1-2*i/100000)) for i in range(100001))
print("min over grid of h2(a) - (1-|1-2a|) =", m)
