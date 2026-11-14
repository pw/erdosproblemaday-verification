sets=[]
for line in open('/tmp/blind704/mis12.txt'):
    sets.append(frozenset(int(x) for x in line.split()))
idx={s:i for i,s in enumerate(sets)}
par=list(range(len(sets)))
def find(x):
    while par[x]!=x: par[x]=par[par[x]]; x=par[x]
    return x
def app(perm,m): return sum(1<<perm[i] for i in range(10) if m>>i&1)
gens=[[1,0,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9,0]]
for i,s in enumerate(sets):
    for g in gens:
        t=frozenset(app(g,m) for m in s); j=idx[t]
        a,b=find(i),find(j)
        if a!=b: par[a]=b
roots={}
for i in range(len(sets)): r=find(i); roots[r]=roots.get(r,0)+1
print('orbits under S10 (shapes):', len(roots), 'orbit sizes:', sorted(roots.values()))
import math; print('stabiliser orders:', sorted(math.factorial(10)//v for v in roots.values()))
