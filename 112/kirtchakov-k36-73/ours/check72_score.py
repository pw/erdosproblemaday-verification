# Route 2 (erdos seat 2026-11-26), decorrelated from check72.py: reads the reader's ARC LIST from the JSON (not S),
# checks it equals the Cayley graph, then
#  (a) independence: trace((J-I-A-A^T)^3)/6 = number of independent triples (numpy matrix route),
#  (b) TT6: by translation (checked: the arc set is invariant under every group translation) a TT6 has its source
#      at vertex 0 WLOG, so TT6 exists iff the 25 out-neighbours of 0 contain a TT5. Brute force: every 5-subset of
#      N+(0); a 5-subset is a transitive tournament iff all 10 pairs are arcs and the out-degree sequence is {0,1,2,3,4}.
#  Control: the same brute force on 4-subsets must find TT4s; and on the transitive tournament TT_7 it finds C(6,5)=6 TT5s below its source.
import json, sys, itertools, numpy as np
d=json.load(open(sys.argv[1])); N=d['N']; arcs={tuple(a) for a in d['arcs']}
A=np.zeros((N,N),dtype=np.int64)
for u,v in arcs: A[u,v]=1
sys.path.insert(0,'.'); from check72 import S, build
_,out=build(S); print('json arcs == Cayley(S):', arcs=={(u,v) for u in range(N) for v in range(N) if out[u]>>v&1})
def tr(v,h): x,y=divmod(v,3); a,b=divmod(h,3); return 3*((x+a)%24)+(y+b)%3
print('translation-invariant:', all((tr(u,h),tr(v,h)) in arcs for h in range(N) for (u,v) in arcs))
U=A+A.T; print('2-cycles:',int((U==2).sum())//2,'loops:',int(np.trace(A)))
C=np.ones((N,N),dtype=np.int64)-np.eye(N,dtype=np.int64)-U
print('independent triples:', int(np.trace(C@C@C))//6)
def count_tt(verts,k):
    c=0
    for sub in itertools.combinations(verts,k):
        if any(U[a,b]!=1 for a,b in itertools.combinations(sub,2)): continue
        if sorted(int(A[a,list(sub)].sum()) for a in sub)==list(range(k)): c+=1
    return c
nb=[v for v in range(N) if A[0,v]]
print('|N+(0)|',len(nb))
print('TT5 inside N+(0) (=> TT6 in G iff >0):', count_tt(nb,5))
print('TT4 inside N+(0) (control, expect >0):', count_tt(nb,4))
B=np.zeros((7,7),dtype=np.int64)
for i in range(7):
    for j in range(i+1,7): B[i,j]=1
A,U=B,B+B.T; print('control TT7: TT5 below source =',count_tt([1,2,3,4,5,6],5),'(expect 6)')
