import subprocess, itertools, sys, time
def g6(s):
    b=[ord(c)-63 for c in s]; n=b[0]; bits=''.join(format(x,'06b') for x in b[1:]); E=[]; k=0
    for j in range(1,n):
        for i in range(j):
            if bits[k]=='1': E.append((i,j))
            k+=1
    return n,E
def adjs(n,E):
    A=[set() for _ in range(n)]
    for a,b in E: A[a].add(b); A[b].add(a)
    return A
def colourable(n,A,k):
    col=[-1]*n; order=sorted(range(n),key=lambda v:-len(A[v]))
    def bt(i):
        if i==n: return True
        v=order[i]; used={col[u] for u in A[v] if col[u]>=0}
        for c in range(k):
            if c not in used:
                col[v]=c
                if bt(i+1): return True
        col[v]=-1; return False
    return bt(0)
def triangles(n,E,A):
    return [(a,b,c) for a,b in E for c in A[a]&A[b] if c>b]
def arrows(n,E):
    A=adjs(n,E); T=triangles(n,E,A)
    if not T: return False
    idx={e:i for i,e in enumerate(E)}
    key=lambda a,b: idx[(a,b) if a<b else (b,a)]
    tri_of=[[] for _ in E]
    TE=[(key(a,b),key(a,c),key(b,c)) for a,b,c in T]
    for t in TE:
        for e in t: tri_of[e].append(t)
    col=[-1]*len(E)
    # order edges by triangle count desc
    order=sorted(range(len(E)),key=lambda e:-len(tri_of[e]))
    def ok(e):
        for t in tri_of[e]:
            cs=[col[x] for x in t]
            if -1 not in cs and cs[0]==cs[1]==cs[2]: return False
        return True
    def bt(i):
        if i==len(order): return True
        e=order[i]
        for c in (0,1):
            if i==0 and c==1: break   # colour symmetry
            col[e]=c
            if ok(e) and bt(i+1): return True
        col[e]=-1; return False
    return not bt(0)
# controls
K6=[(a,b) for a,b in itertools.combinations(range(6),2)]
assert arrows(6,K6) and not arrows(5,[(a,b) for a,b in itertools.combinations(range(5),2)])
G35=[(a,b) for a,b in itertools.combinations(range(3),2)]+[(3+i,3+(i+1)%5) if 3+i<3+(i+1)%5 else (3+(i+1)%5,3+i) for i in range(5)]+[(a,b) for a in range(3) for b in range(3,8)]
assert arrows(8,G35)
def minimal(n,E):
    return arrows(n,E) and all(not arrows(n,[f for f in E if f!=e]) for e in E)
assert minimal(6,K6) and minimal(8,G35)
assert not minimal(7,K6+[(0,6)])
t0=time.time()
for n in range(6,10):
    gs=subprocess.run(['nice','-n','19','nauty-geng','-q','-c','-d4',str(n)],capture_output=True,text=True).stdout.split()
    stage=[]
    for s in gs:
        nn,E=g6(s); A=adjs(nn,E)
        if any(u!=v and A[u]<=A[v] for u in range(nn) for v in range(nn)): continue   # Sperner (Prop 2.3)
        if colourable(nn,A,5): continue                                               # chi>=6 (Thm 2.5)
        stage.append((s,nn,E))
    mins=[(s,nn,E) for s,nn,E in stage if minimal(nn,E)]
    print(f"n={n}: connected delta>=4 {len(gs)}; non-Sperner & chi>=6 {len(stage)}; minimal (3,3)-Ramsey {len(mins)}  ({time.time()-t0:.0f}s)")
    for s,nn,E in mins:
        A=adjs(nn,E); nt=len(triangles(nn,E,A))
        print(f"   {s}: edges={len(E)} triangles={nt}  #tri>=#edges: {nt>=len(E)}")
