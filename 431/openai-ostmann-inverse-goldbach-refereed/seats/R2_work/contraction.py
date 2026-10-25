# Numerical check of Lemma 5.2 (local contraction) on an explicit sparse-spectrum S_p,
# plus negative controls (overlapping supports; non-sparse random S).
import numpy as np, sys
def isprime(n):
    return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def analyse(p, S, T, t0=0.85, label=''):
    S=np.array(sorted(S)); T=np.array(sorted(T))
    sig=len(S)/p
    ind=np.zeros(p); ind[S]=1
    F=(ind-sig)/np.sqrt(sig*(1-sig))
    g=np.sqrt(p)*np.fft.fft(F)/p          # g(v)=sqrt p * E_x F(x) e(-vx)
    gamma=np.mean(np.abs(g))
    E=np.where(np.abs(g)>1)[0]
    eps_card=len(E)/p; tail=np.sum(np.abs(g[np.abs(g)<=1])**2)/p
    x=np.arange(p)
    b=(t0/p)*np.cos(2*np.pi*np.outer(x,E)/p).sum(axis=1) if len(E) else np.zeros(p)
    def kernel(u,v):
        h=(1+u*b)*(1+v*b)
        return h[(x[:,None]-x[None,:])%p]      # H[x,y]=h(x-y)
    H=kernel(1,1)
    uS=np.zeros(p); uS[S]=1/len(S); uT=np.zeros(p); uT[T]=1/len(T)
    QS=np.eye(len(S))-1/len(S); QT=np.eye(len(T))-1/len(T)
    M=np.zeros((1+len(S),1+len(T)))
    M[0,0]=uS@H@uT
    M[0,1:]=(uS@H[:,T])@QT
    M[1:,0]=QS@(H[S,:]@uT)
    M[1:,1:]=QS@H[np.ix_(S,T)]@QT
    nrm=np.linalg.norm(M,2)
    U=np.mean([(1+b[i])**2 for i in range(1,p)])
    print(f'{label} p={p} sigma={sig:.3f} gamma={gamma:.3f} |E|/p={eps_card:.4f} tail={tail:.4f}  '
          f'||L||={nrm:.7f}  U={U:.7f}  U(1-1.6/p)={U*(1-1.6/p):.7f}  '
          f'(||L||-1)*p={(nrm-1)*p:+.3f}  holds={nrm<=U*(1-1.6/p)}')
    return nrm, U

for p in (1009, 2003):
    assert isprime(p)
    half=p//2
    S=list(range(0,half)); T=list(range(half,p))       # interval: sparse spectrum
    analyse(p,S,T,label='interval   ')
    # negative control 1: same sparse kernel but "overlapping" supports (T:=S) -> no contraction expected
    analyse(p,S,S,label='CONTROL S=T')
    # negative control 2: random balanced S (non-sparse spectrum): lemma's hypothesis gamma<delta0 fails
    rng=np.random.default_rng(p); perm=rng.permutation(p)
    analyse(p,sorted(perm[:half]),sorted(perm[half:]),label='CONTROL rnd')
