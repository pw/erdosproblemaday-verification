"""One-step form of the (4.8) induction with arbitrary S and theta:
 for a = K^i(v,.) (so a(z) <= x w_z), S+ = S cup {y: w(N(y) cap S) >= theta}:
 (aQ)(N(u) minus S+) <= a(N(u) minus S) + x^2 theta s_u / 2   (paper uses the weaker  + x^2 theta L).
Also the conditioning bound behind H_R on arbitrary splits D of N(u)."""
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, sys
rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 4)
def Hw(a,w):
    m=a>0; return float(np.sum(a[m]*np.log(w[m]/a[m])))
worst=-np.inf; nontriv=0; tot=0; worstH=-np.inf; nH=0
for t in range(3000):
    n=int(rng.integers(6,18))
    A=(rng.random((n,n))<rng.uniform(0.5,1.0)).astype(float); A=np.triu(A,1); A=A+A.T
    w=np.exp(rng.normal(0,rng.uniform(0.1,1.5),n))
    C=(A*w)@A
    A=A*(C>0); C=(A*w)@A; A=A*(C>0); C=(A*w)@A
    if A.sum()==0 or (C[A>0]<=0).any(): continue
    x=1/C[A>0].min(); s=A@w
    u=rng.choice(np.where(A.sum(1)>0)[0]); N=np.where(A[u]>0)[0]
    P=A[np.ix_(N,N)]*w[N][None,:]/C[u,N][:,None]; Q=0.5*(np.eye(len(N))+P)
    K=P@np.linalg.matrix_power(Q,int(rng.integers(0,4)))
    a=K[rng.integers(len(N))]
    assert np.all(a<=x*w[N]+1e-12)
    S=rng.random(n)<rng.uniform(0.1,0.7)
    reach=A@(w*S)
    theta=np.quantile(reach[reach>0],rng.uniform(0.2,0.95)) if (reach>0).any() else 1.0
    Sp=S|(reach>=theta)
    lhs=(a@Q)[~Sp[N]].sum(); rhs=a[~S[N]].sum()+x*x*theta*s[u]/2
    tot+=1; worst=max(worst,lhs-rhs)
    if lhs>0.5*rhs and lhs>a[~S[N]].sum()+1e-12: nontriv+=1
    D=rng.random(len(N))<0.5; d=a[~D].sum()
    if 0<d<1 and D.any() and (~D).any() and a[D].sum()>0:
        nH+=1; worstH=max(worstH,Hw(a,w[N])-(np.log(2)+(1-d)*np.log(w[N][D].sum())+d*np.log(w[N][~D].sum())))
print('instances',tot,'nontrivial (lhs>rhs/2 and some fresh leak)',nontriv,'max lhs-rhs',worst)
print('H_R conditioning instances',nH,'max violation',worstH)
