# Referee: Aut(W) from W alone (W0 literal parsed from wstruct.py source text, not imported), by backtracking.
import ast, re, itertools
from math import comb
src = open('../wstruct.py').read()
W0 = ast.literal_eval(re.search(r'^W0 = (\[.*\])$', src, re.M).group(1))
W = {frozenset(x-1 for x in s) for s in W0}
assert len(W) == 33 and all(len(s)==5 for s in W)
assert all(len(a&b)!=3 for a,b in itertools.combinations(W,2)), 'W not independent'
# my own role description from CLAIMS.md (1-based): INF=11; a=(1,12,7); b=(2,13,8); S12={3,6}, S13={4,5}, S23={9,10}
INF=11; a=(1,12,7); b=(2,13,8); S={(1,2):{3,6},(1,3):{4,5},(2,3):{9,10}}
blocks=[{a[0],b[0]}|S[(1,2)]|S[(1,3)], {a[1],b[1]}|S[(1,2)]|S[(2,3)], {a[2],b[2]}|S[(1,3)]|S[(2,3)]]
R=set()
for B in blocks: R|={frozenset(B-{x}) for x in B}
sh=S[(1,2)]|S[(1,3)]|S[(2,3)]
R|={frozenset({INF,*a,s}) for s in sh}
R|={frozenset({INF,*b,y}) for y in range(1,14) if y not in {INF,*b}}
assert len(blocks[0]|blocks[1]|blocks[2]|{INF}|set(a)|set(b))==13
R={frozenset(x-1 for x in s) for s in R}
print('B1 role description reproduces Appendix A:', R==W)
deg=[sum(1 for s in W if x in s) for x in range(13)]
print('point degrees in W:', deg)
# backtracking automorphism search
Wl=list(W)
auts=[]
def ok(img):
    k=len(img)
    for s in Wl:
        if max(s)<k and frozenset(img[x] for x in s) not in W: return False
    return True
def bt(img, used):
    if len(img)==13: auts.append(tuple(img)); return
    x=len(img)
    for y in range(13):
        if y in used or deg[y]!=deg[x]: continue
        img.append(y)
        if ok(img): bt(img, used|{y})
        img.pop()
bt([], frozenset())
print('|Aut(W)| =', len(auts))
def ctype(p):
    seen=set(); L=[]
    for x in range(13):
        if x in seen: continue
        c=0; y=x
        while y not in seen: seen.add(y); y=p[y]; c+=1
        L.append(c)
    return tuple(sorted(L, reverse=True))
def order(p):
    from math import lcm
    o=1
    for c in ctype(p): o=lcm(o,c)
    return o
V=[frozenset(c) for c in itertools.combinations(range(13),5)]
rows={}
for p in auts:
    ty=ctype(p); o=order(p)
    phi=sum(1 for s in W if frozenset(p[x] for x in s)==s)
    fixall=sum(1 for s in V if frozenset(p[x] for x in s)==s)
    rows.setdefault((o,ty,phi,fixall),0); rows[(o,ty,phi,fixall)]+=1
for k,v in sorted(rows.items()): print('order',k[0],'type',k[1],'phi',k[2],'fixed5sets',k[3],'count',v)
# fixed 5-sets by any involution of type 2^k (all k), computed by brute force
for k in range(1,7):
    p=list(range(13))
    for i in range(k): p[2*i],p[2*i+1]=2*i+1,2*i
    N=sum(1 for s in V if frozenset(p[x] for x in s)==s)
    print('type 2^%d: N=%d'%(k,N), ' phi values in Aut(W):', sorted({kk[2] for kk in rows if kk[0]==2 and kk[1].count(2)==k}))
# preservation of INF, a-triple, b-triple
inf=10; at={0,11,6}; btp={1,12,7}
print('all auts fix INF, preserve {a},{b}:', all(p[inf]==inf and {p[x] for x in at}==at and {p[x] for x in btp}==btp for p in auts))
# order-3 elements: fixed 5-sets
print('type 3^k fixed 5-sets: ', {k: sum(1 for s in V if frozenset(((x//3)*3+(x%3+1)%3 if x<3*k else x) for x in s)==s) for k in range(1,5)})
