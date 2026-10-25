import numpy as np, importlib.util, sys
spec=importlib.util.spec_from_file_location("cf","/tmp/motions_scripts/check_flats.py")
src=open("/tmp/motions_scripts/check_flats.py").read().split("res=[]")[0]
ns={}; exec(src,ns)
rng=ns['rng']; motion_flat=ns['motion_flat']; pair_flat=ns['pair_flat']; inter_dim=ns['inter_dim']; rand_rot=ns['rand_rot']
ok=0; trip=0
for t in range(200):
    S=rand_rot()@np.diag([1,1,-1.0]); h=rng.normal(size=3)
    E1,r1=motion_flat(S,h); E2,r2=motion_flat(S,h)   # different random e1 each call
    # same affine flat iff stacked system has rank 3 and consistent
    A=np.vstack([E1,E2]); b=np.concatenate([r1,r2])
    if np.linalg.matrix_rank(A,1e-9)==3 and np.linalg.matrix_rank(np.column_stack([A,b]),1e-9)==3: ok+=1
    # also flip axis orientation: emulate by negating S's eigvec choice -> motion_flat picks via eig; force by -a frame
    # triple intersection: three matched points -> planes H meet in a point
    xs=rng.normal(size=(3,3)); Hs=[]
    M=[E1]; rr=[r1]
    for x in xs:
        A_,b_=pair_flat(x,S@x+h); M.append(A_); rr.append(b_)
    d=inter_dim(np.vstack(M),np.concatenate(rr),np.zeros((0,6)),np.zeros(0))
    if d==0: trip+=1
print("frame-independent:",ok,"/200; transverse triple -> point:",trip,"/200")
