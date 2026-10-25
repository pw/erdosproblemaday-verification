# Covering radius (in RP^3, angle metric) of the 11 lines through Walkup's 1970 polytope P0 (Acta Math 125, sec. 8).
import numpy as np, itertools
b=np.sqrt(2)/2; a=1/np.sqrt(3)
L=[(0,0,0,1)]
for i in range(3):
    for s in (1,-1):
        v=[0,0,0,0]; v[i]=b; v[3]=s*b; L.append(tuple(v))
for s2,s3 in itertools.product((1,-1),repeat=2):
    L.append((a,s2*a,s3*a,0))
C=np.array(L,float); C/=np.linalg.norm(C,axis=1,keepdims=True)
print("lines",len(C)); G=np.abs(C@C.T); np.fill_diagonal(G,0); print("max |cos| between lines",G.max().round(6))
verts=[]
for Q in itertools.combinations(range(len(C)),4):
    for sg in itertools.product([1,-1],repeat=3):
        sgn=np.array((1,)+sg,float); M=sgn[:,None]*C[list(Q)]
        if abs(np.linalg.det(M))<1e-12: continue
        y=np.linalg.solve(M,np.ones(4)); s=1/np.linalg.norm(y); v=y*s
        if np.delete(np.abs(C@v),list(Q)).max()<=s+1e-9: verts.append((Q,np.degrees(np.arccos(min(1,s)))))
angs=sorted(set(round(t,6) for _,t in verts))
print("Voronoi-vertex circumradii (deg):",angs)
print("covering radius (deg) = %.6f"%max(t for _,t in verts))
# independent dense check
rng=np.random.default_rng(0); X=rng.normal(size=(2000000,4)); X/=np.linalg.norm(X,axis=1,keepdims=True)
print("sampled max-min angle (deg) = %.6f"%np.degrees(np.arccos(np.abs(X@C.T).max(axis=1).min())))
