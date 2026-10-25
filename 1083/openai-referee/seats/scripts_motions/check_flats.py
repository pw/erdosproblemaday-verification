import numpy as np
rng=np.random.default_rng(1)
def cross_mat(v):  # matrix of w -> w x v
    # w x v = -v x w = -[v]_x w
    vx=np.array([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    return -vx
def pair_flat(x,y):
    v=(x+y)/2; b=(x-y)/2
    # equations: w x v + c = b  ->  [cross_mat(v) | I] (w,c) = b
    A=np.hstack([cross_mat(v),np.eye(3)]); return A,b
def rand_rot():
    q,_=np.linalg.qr(rng.normal(size=(3,3)))
    if np.linalg.det(q)<0: q[:,0]*=-1
    return q
def motion_flat(S,h):
    # S reversing. axis a: S a = -a
    w_,V=np.linalg.eig(S); i=np.argmin(abs(w_+1)); a=np.real(V[:,i]); a/=np.linalg.norm(a)
    # positively oriented frame U=[e1 e2 a]
    e1=np.cross(a,rng.normal(size=3)); e1/=np.linalg.norm(e1); e2=np.cross(a,e1)
    U=np.column_stack([e1,e2,a]); assert np.linalg.det(U)>0
    Sp=U.T@S@U; hp=U.T@h
    Sperp=Sp[:2,:2]; J=np.array([[0,-1],[1,0]])
    W=(np.eye(2)-Sperp)@np.linalg.inv(np.eye(2)+Sperp)
    om=W[1,0]; assert np.allclose(W,om*J)
    v0=hp[2]/2; d=-(np.eye(2)+om*J)@hp[:2]/2
    # in frame coords (w',c'): w3'=om, c1'+v0 w2'=d1, c2'-v0 w1'=d2 ; w'=U^T w, c'=U^T c
    E=np.zeros((3,6)); r=np.zeros(3)
    E[0,:3]=U[:,2]; r[0]=om
    E[1,3:]=U[:,0]; E[1,:3]+=v0*U[:,1]; r[1]=d[0]
    E[2,3:]=U[:,1]; E[2,:3]+=-v0*U[:,0]; r[2]=d[1]
    return E,r
def inter_dim(A1,b1,A2,b2):
    A=np.vstack([A1,A2]); b=np.concatenate([b1,b2])
    rk=np.linalg.matrix_rank(A,1e-9); rka=np.linalg.matrix_rank(np.column_stack([A,b]),1e-9)
    return None if rka>rk else 6-rk
Q=np.diag([1,1,1,-1,-1,-1]); Bm=np.block([[np.zeros((3,3)),np.eye(3)],[np.eye(3),np.zeros((3,3))]])
def null_dir(A):
    _,s,vt=np.linalg.svd(A); return vt[np.sum(s>1e-9):].T
res=[]
for trial in range(200):
    R=rand_rot(); refl=np.diag([1,1,-1.0]); S=R@refl; h=rng.normal(size=3)
    E,r=motion_flat(S,h)
    x=rng.normal(size=3); y=S@x+h
    A,b=pair_flat(x,y)
    dG=null_dir(E); dF=null_dir(A)
    assert np.allclose(dG.T@Bm@dG,0,atol=1e-9) and np.allclose(dF.T@Bm@dF,0,atol=1e-9)
    k1=inter_dim(A,b,E,r)
    y2=rng.normal(size=3); A2,b2=pair_flat(x,y2); k2=inter_dim(A2,b2,E,r)
    # planes from two different reversing motions both mapping x->y : distinct?
    R2=rand_rot(); S2=R2@refl; h2=y-S2@x; E2,r2=motion_flat(S2,h2)
    k3=inter_dim(np.vstack([A,E]),np.concatenate([b,r]),E2,r2)  # dim of (F∩G)∩G2
    res.append((k1,k2,k3))
from collections import Counter
print(Counter(res))
