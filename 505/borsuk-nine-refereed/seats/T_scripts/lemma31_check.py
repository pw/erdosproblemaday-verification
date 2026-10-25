# Numerical sanity checks for Lemma 2.1, Remark 2.2, Lemma 3.1 (identities that do not need admissibility).
import numpy as np
rng = np.random.default_rng(1)

def proj(u):
    u = u/np.linalg.norm(u); return np.outer(u,u)

# ---- Lemma 2.1 (2.1) and Remark 2.2 isometry, k=4
def coords9(A):
    a=A
    return np.array([(a[0,0]-a[1,1])/np.sqrt(2),(a[0,0]+a[1,1]-2*a[2,2])/np.sqrt(6),
        (a[0,0]+a[1,1]+a[2,2]-3*a[3,3])/np.sqrt(12),
        np.sqrt(2)*a[0,1],np.sqrt(2)*a[0,2],np.sqrt(2)*a[0,3],np.sqrt(2)*a[1,2],np.sqrt(2)*a[1,3],np.sqrt(2)*a[2,3]])
err21=0; err22=0
for _ in range(2000):
    u=rng.normal(size=4); v=rng.normal(size=4); u/=np.linalg.norm(u); v/=np.linalg.norm(v)
    Px,Py=proj(u),proj(v)
    d2=np.sum((Px-Py)**2)
    err21=max(err21,abs(d2-(2-2*np.dot(u,v)**2)))
    # random trace-one symmetric pair
    S=rng.normal(size=(4,4)); S=(S+S.T)/2; S+= (1-np.trace(S))/4*np.eye(4)
    T=rng.normal(size=(4,4)); T=(T+T.T)/2; T+= (1-np.trace(T))/4*np.eye(4)
    err22=max(err22,abs(np.linalg.norm(coords9(S)-coords9(T))-np.linalg.norm(S-T)))
print("(2.1) max err",err21," (2.2) isometry max err",err22)

# ---- generic smooth (NOT admissible) f on RP^{k-1}: softmax of <M_i, P_x>
k=4; m=10
Ms=[ (lambda X:(X+X.T))(rng.normal(size=(k,k))) for _ in range(m)]
def f_of_vecs(V):  # V: (N,k) nonzero vectors -> (N,m) f([v])
    n=np.linalg.norm(V,axis=1,keepdims=True); U=V/n
    logits=np.stack([np.einsum('ni,ij,nj->n',U,M,U) for M in Ms],axis=1)
    logits-=logits.max(1,keepdims=True); e=np.exp(logits); return e/e.sum(1,keepdims=True)
def H(V):
    n2=np.sum(V**2,axis=1,keepdims=True); out=np.zeros((V.shape[0],m)); nz=n2[:,0]>1e-300
    out[nz]=n2[nz]*f_of_vecs(V[nz]); return out
def psd_sqrt(Q):
    w,U=np.linalg.eigh(Q); w=np.clip(w,0,None); return (U*np.sqrt(w))@U.T
def sphere(N,d):
    X=rng.normal(size=(N,d)); return X/np.linalg.norm(X,axis=1,keepdims=True)
NS=2_000_000
SV=sphere(NS,k)
def E_V(Q):  # factor k, mu_V on S^{k-1}
    R=psd_sqrt(Q); return k*H(SV@R.T).mean(0)

# (a) E_V(P_x)=f(x)
u=rng.normal(size=k); u/=np.linalg.norm(u)
print("E_V(P_x)-f(x) max abs:",np.abs(E_V(proj(u))-f_of_vecs(u[None,:])[0]).max())
# (b) sum E = tr Q
Bm=rng.normal(size=(k,k)); Q=Bm@Bm.T
print("sum E - trQ:",E_V(Q).sum()-np.trace(Q))
# (c) subspace identity for r=1,2,3: Q supported on W (random r-dim subspace)
for r in (1,2,3):
    Wb,_=np.linalg.qr(rng.normal(size=(k,r)))  # k x r orthonormal frame
    C=rng.normal(size=(r,r)); C=C@C.T+0.3*np.eye(r)
    Qw=Wb@C@Wb.T
    lhs=E_V(Qw)
    SW=sphere(NS,r)
    Csq=psd_sqrt(C)
    rhs=r*H((SW@Csq.T)@Wb.T).mean(0)   # E_W(Q|W), factor r, mu_W, f restricted to P(W)
    print(f"r={r}: max|E_V(Q)-E_W(Q|W)| = {np.abs(lhs-rhs).max():.2e}  (scale {lhs.max():.3f})  trQ={np.trace(Qw):.3f} sums {lhs.sum():.4f} {rhs.sum():.4f}")
# (d) total mass of the pushed measure: E|pi_W u|^2 = r/k
for r in (1,2,3):
    print(f"r={r}: mean |pi_W u|^2 = {np.mean(np.sum(SV[:,:r]**2,1)):.5f}  vs r/k={r/k}")
