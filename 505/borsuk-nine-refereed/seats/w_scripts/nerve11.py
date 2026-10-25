# Enumerate Voronoi vertices (Delaunay tetrahedra) of a line configuration in RP^3 and report f-vector.
import numpy as np, sys, itertools
C=np.load(sys.argv[1]); K=len(C)
rng=np.random.default_rng(3)
X=rng.normal(size=(400000,4)); X/=np.linalg.norm(X,axis=1,keepdims=True)
A=np.abs(X@C.T); top=np.argsort(-A,axis=1)[:,:4]
# candidate quadruples: those appearing as top-4 near deep points; verify each exactly
cands=set(tuple(sorted(r)) for r in top[np.argsort(A.max(axis=1))[:40000]])
verts=[]
for Q in itertools.combinations(range(K),4):
    for sg in itertools.product([1,-1],repeat=3):
        sgn=np.array((1,)+sg,float); M=sgn[:,None]*C[list(Q)]
        try: y=np.linalg.solve(M,np.ones(4))
        except np.linalg.LinAlgError: continue
        s=1/np.linalg.norm(y); v=y*s
        a=np.abs(C@v)
        others=np.delete(a,list(Q))
        if others.max()<s-1e-9: verts.append((Q,tuple(sgn),np.degrees(np.arccos(s))))
print("lines",K,"Voronoi vertices (tetrahedra)",len(verts))
print("max vertex angle (covering radius) %.5f"%max(v[2] for v in verts))
E=set(); F=set()
for Q,_,_ in verts:
    for e in itertools.combinations(Q,2): E.add(e)
    for f in itertools.combinations(Q,3): F.add(f)
print("f-vector (f0,f1,f2,f3) =",(len(set(i for Q,_,_ in verts for i in Q)),len(E),len(F),len(verts)))
print("distinct quadruples",len(set(Q for Q,_,_ in verts)))
print("Euler char f0-f1+f2-f3 =",len(set(i for Q,_,_ in verts for i in Q))-len(E)-0+len(F)-len(verts))
