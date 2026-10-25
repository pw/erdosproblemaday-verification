# Simulate the marking scan of Paper B §4 (mark:marking) on greedy-consistent flag tuples in PG(d,q).
import random, itertools, sys, math
q=int(sys.argv[1]); d=int(sys.argv[2]); N=int(sys.argv[3]); seed=int(sys.argv[4])
random.seed(seed)
n=d+1
def normalize(v):
    for x in v:
        if x%q:
            inv=pow(x,q-2,q); return tuple((y*inv)%q for y in v)
    return None
pts=sorted({normalize(v) for v in itertools.product(range(q),repeat=n)}-{None})
idx={p:i for i,p in enumerate(pts)}
dot=lambda a,b: sum(x*y for x,y in zip(a,b))%q
inc=[[dot(a,b)==0 for b in pts] for a in pts]   # inc[a][b]: a ⊥ b
flags=[(a,b) for a in range(len(pts)) for b in range(len(pts)) if inc[a][b]]
# rank / span utilities over F_q
def reduce(basis,v):
    v=list(v)
    for (piv,row) in basis:
        if v[piv]%q:
            c=v[piv]
            v=[(x-c*y)%q for x,y in zip(v,row)]
    return v
def add(basis,v):
    v=reduce(basis,v)
    for i,x in enumerate(v):
        if x%q:
            inv=pow(x,q-2,q); v=[(y*inv)%q for y in v]
            nb=[]
            for (piv,row) in basis:
                if row[i]%q:
                    c=row[i]; row=[(a-c*b)%q for a,b in zip(row,v)]
                nb.append((piv,row))
            nb.append((i,v)); return nb,True
    return basis,False
def contains(basis,v): return not any(x%q for x in reduce(basis,v))
stream=[random.choice(flags) for _ in range(N)]
tup=[]
for f in stream:
    a,b=f
    if all((not inc[a2][b]) or inc[a][b2] for (a2,b2) in tup): tup.append(f)
def scan(tup):
    V=[[] for _ in pts]
    stats={'pop':0,'poor':0,'exp':0,'viol':0,'maxpopdom':0,'maxpoordom':0}
    for (a,b) in tup:
        r=len(V[b])
        # consistency => a ⊥ V(b)
        for (piv,row) in V[b]:
            if dot(pts[a],row): stats['viol']+=1; break
        dims=[len(V[y]) for y in range(len(pts))]
        Z=[[y for y in range(len(pts)) if dims[y]==j] for j in range(n+1)]
        l=max(range(r+1),key=lambda j:(len(Z[j]),-j))
        Zl=Z[l]
        popcnt=sum(1 for y in Zl if contains(V[y],pts[b]))
        if popcnt>=len(Zl)/(16*q):
            stats['pop']+=1
            # popular-domain size: # b' with dim V(b')==r and popular, times #a' ⊥ V(b') and ⊥ b'
            popB=[bb for bb in range(len(pts)) if dims[bb]==r and sum(1 for y in Zl if contains(V[y],pts[bb]))>=len(Zl)/(16*q)]
            assert len(popB)<=32*q**l, (len(popB),q,l)
            dom=0
            for bb in popB:
                dom+=sum(1 for aa in range(len(pts)) if inc[aa][bb] and all(dot(pts[aa],row)==0 for (_,row) in V[bb]))
            stats['maxpopdom']=max(stats['maxpopdom'],dom/q**d)
            continue
        poorcnt=sum(1 for y in Zl if inc[a][y])
        if poorcnt<=len(Zl)/(8*q):
            stats['poor']+=1
            poorA=[aa for aa in range(len(pts)) if sum(1 for y in Zl if inc[aa][y])<=len(Zl)/(8*q)]
            dom=sum(1 for aa in poorA for bb in Z[r] if inc[aa][bb])
            stats['maxpoordom']=max(stats['maxpoordom'],dom/q**d)
            continue
        stats['exp']+=1
        for y in range(len(pts)):
            if inc[a][y]:
                V[y],_=add(V[y],pts[b])
    return stats
fw=scan(tup)
rev=[(b,a) for (a,b) in reversed(tup)]
bw=scan(rev)
print(f"q={q} d={d} N={N} |PG|={len(pts)} flags={len(flags)} tuple={len(tup)} q*log q={q*math.log(q):.1f}")
print("forward",fw); print("reverse",bw)
