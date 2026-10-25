# Enumerate ALL additive relations a+b=c+d ({a,b}!={c,d}, a=b allowed) in S_K and test each lies inside one copy phi^j(O).
import sys, itertools
from fractions import Fraction as F
from collections import defaultdict
O=[0,49,75,83,98,101,117,119,121,159,269]
def phi(x): return F(101)+F(18)*x/269
def copies(K):
    cs=[]; cur=[F(x) for x in O]
    for j in range(K+1):
        cs.append(set(cur)); cur=[phi(x) for x in cur]
    return cs
def relations(pts):
    pts=sorted(pts); sums=defaultdict(list); n=len(pts)
    for i in range(n):
        for j in range(i,n): sums[pts[i]+pts[j]].append((pts[i],pts[j]))
    R=set()
    for v,ps in sums.items():
        for p,q in itertools.combinations(ps,2): R.add(frozenset(p)|frozenset(q))
    return R
if __name__=='__main__':
    K=int(sys.argv[1])
    cs=copies(K); allp=set().union(*cs)
    assert len(allp)==11+9*K
    # copy overlaps: consecutive share exactly {phi^j(101),phi^j(119)}, others disjoint
    for i in range(K+1):
        for j in range(i+1,K+1):
            inter=cs[i]&cs[j]
            if j==i+1: assert len(inter)==2
            else: assert not inter,(i,j)
    R=relations(allp)
    cross=[r for r in R if not any(r<=c for c in cs)]
    print('K',K,'points',len(allp),'relations',len(R),'expected',9*(K+1),'cross-copy',len(cross))
    if K==0:
        for r in sorted(R,key=lambda r:sorted(r)): print('  ',sorted(int(x) for x in r))
    # negative control: inject a point that creates a cross-copy relation and confirm it is detected
    if K>=1:
        a=sorted(cs[0]-cs[1])[0]; b=sorted(cs[1]-cs[0])[0]; c=sorted(cs[0]-cs[1])[1]
        extra=b+c-a
        R2=relations(allp|{extra}); cs2=cs+[{extra}]
        cross2=[r for r in R2 if not any(r<=c_ for c_ in cs)]
        assert cross2, 'control failed'
        print('  control: injected point creates',len(cross2),'cross-copy relations (detected)')
