# Brute-force ALL additive relations a+b=c+d (a=b allowed) in S_K via integer scaling; test single-copy containment.
import sys, itertools, time; sys.path.insert(0,'/tmp/ref757')
from core import *
from collections import defaultdict
def rels(pts):
    pts=sorted(pts); n=len(pts); sums=defaultdict(list)
    for i in range(n):
        a=pts[i]
        for j in range(i,n): sums[a+pts[j]].append((i,j))
    R=set(); n4=0
    for v,ps in sums.items():
        if len(ps)>1:
            for p,q in itertools.combinations(ps,2):
                s=frozenset(p)|frozenset(q); R.add(s)
                if len(s)==4: n4+=1
    return R,n4,pts
for K in [int(a) for a in sys.argv[1:]]:
    t=time.time()
    cs=copies(K); sc=269**K
    S=sorted(set().union(*cs)); P=[int(x*sc) for x in S]
    assert all((x*sc).denominator==1 for x in S)
    idx={p:i for i,p in enumerate(P)}
    csI=[frozenset(idx[int(x*sc)] for x in c) for c in cs]
    R,n4,_=rels(P)
    cross=[r for r in R if not any(r<=c for c in csI)]
    # spans in level terms: level = index of copy whose 'new' points ... compute via canonical: min/max copy index containing
    print(f'K={K} n={len(P)} relations={len(R)} expect={9*(K+1)} 4pt={n4} cross-copy={len(cross)} t={time.time()-t:.1f}s',flush=True)
    if K==3:
        # negative control: add a point making a cross-copy 3-AP between copy0 point and copy3 point
        a=P[0]; b=P[-1]
        if (a+b)%2==0:
            R2,_,_=rels(P+[(a+b)//2])
        else:
            R2,_,_=rels(P+[2*b-a])
        print('  control (injected cross-copy AP) relations',len(R2),'(should exceed',len(R),')')
