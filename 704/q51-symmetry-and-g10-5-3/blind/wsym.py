import sys, itertools, collections, math
sys.path.insert(0,'/home/exedev/MathDyad/erdos704/q51')
from wstruct import WA
W=set(WA); N=13
assert len(W)==33
assert all(len(a&b)!=3 for a,b in itertools.combinations(W,2))
# brute-force automorphisms via backtracking
order=sorted(range(N), key=lambda x:-sum(x in s for s in W))
sets_by_last={}
pos={p:i for i,p in enumerate(order)}
for s in W:
    last=max(s,key=lambda x:pos[x]); sets_by_last.setdefault(last,[]).append(s)
auts=[]
def bt(i,img,used):
    if i==N: auts.append(tuple(img[x] for x in range(N))); return
    p=order[i]
    for q in range(N):
        if q in used: continue
        img[p]=q
        if all(frozenset(img[x] for x in s) in W for s in sets_by_last.get(p,[])):
            used.add(q); bt(i+1,img,used); used.discard(q)
        del img[p]
bt(0,{},set())
print('|Aut(W)| =',len(auts))
def cyc(g):
    seen=set(); t=[]
    for x in range(N):
        if x in seen: continue
        l=0;y=x
        while y not in seen: seen.add(y); y=g[y]; l+=1
        t.append(l)
    return tuple(sorted(t,reverse=True))
def order_(g): return math.lcm(*cyc(g))
print('orders:', collections.Counter(order_(g) for g in auts))
print('cycle types:', collections.Counter(cyc(g) for g in auts))
# point degrees
deg=collections.Counter(x for s in W for x in s); print('point degrees', sorted(deg.items()))
# order-2: involutions with k transpositions; fixed 5-sets of 13 and fixed sets in W
from itertools import combinations
allV=[frozenset(c) for c in combinations(range(N),5)]
inv=[g for g in auts if order_(g)==2]
byk=collections.defaultdict(set)
for g in inv:
    k=sum(1 for x in range(N) if g[x]>x)
    fw=sum(1 for s in W if frozenset(g[x] for x in s)==s)
    byk[k].add(fw)
print('involutions in Aut(W): k -> fixed sets in W:', dict(byk))
def fixed_total(k):
    g=list(range(N))
    for i in range(k): g[2*i],g[2*i+1]=2*i+1,2*i
    return sum(1 for s in allV if frozenset(g[x] for x in s)==s)
print('fixed 5-sets of 13 for k=1..6:', [fixed_total(k) for k in range(1,7)])
o3=[g for g in auts if order_(g)==3]
print('order-3 cycle types:', collections.Counter(cyc(g) for g in o3))
import json; json.dump(auts,open('/tmp/blind704/auts.json','w'))
