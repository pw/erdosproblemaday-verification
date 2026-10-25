# Exhaustive check: Shi-Dong k=4 colouring of Z/p^4Z has no nontrivial symmetrically
# coloured 4-AP (c(a)=c(a+3d), c(a+d)=c(a+2d), d != 0 mod p^4), plus negative controls.
import sys, numpy as np
def irreducible_cubic(p):
    for a in range(p):
        for b in range(1,p):
            if all((x*x*x + a*x + b) % p for x in range(p)): return a,b
def mul(u,v,p,a,b):
    # elements c0+c1 T+c2 T^2 mod T^3 + a T + b
    r=[0]*5
    for i in range(3):
        for j in range(3): r[i+j]+=u[i]*v[j]
    # T^3 = -aT - b ; T^4 = -aT^2 - bT
    c4=r[4]; r[2]-=a*c4; r[1]-=b*c4
    c3=r[3]; r[1]-=a*c3; r[0]-=b*c3
    return (r[0]%p,r[1]%p,r[2]%p)
def power(u,e,p,a,b):
    res=(1,0,0)
    while e:
        if e&1: res=mul(res,u,p,a,b)
        u=mul(u,u,p,a,b); e>>=1
    return res
def build(p, variant):
    a,b=irreducible_cubic(p)
    norm={}
    for x1 in range(p):
        for x2 in range(p):
            for x3 in range(p):
                n=power((x1,x2,x3),1+p+p*p,p,a,b)
                assert n[1]==0 and n[2]==0
                norm[(x1,x2,x3)]=n[0]
    # sanity: norm has no nontrivial zero
    assert sum(1 for k,v in norm.items() if v==0)==1
    M=p**4; C=np.zeros(M,dtype=np.int64)
    tau=lambda x:(3*x)//p
    for n in range(M):
        x0=n%p; x1=(n//p)%p; x2=(n//p**2)%p; x3=n//p**3
        Nv=norm[(x1,x2,x3)]
        if variant=='full':   key=(tau(x0),tau(x1),tau(x2),(x0+Nv)%p)
        elif variant=='nolin': key=(tau(x0),tau(x1),tau(x2),Nv)          # drop linear layer
        elif variant=='notau0': key=(0,tau(x1),tau(x2),(x0+Nv)%p)       # drop carry control on digit 0
        C[n]=((key[0]*3+key[1])*3+key[2])*p+key[3]
    return M,C
def count_violations(M,C):
    idx=np.arange(M); bad=0; ex=None
    for d in range(1,M):
        m=(C==C[(idx+3*d)%M])&(C[(idx+d)%M]==C[(idx+2*d)%M])
        c=int(m.sum())
        if c and ex is None: ex=(int(np.argmax(m)),d)
        bad+=c
    return bad,ex
if __name__=="__main__":
 for p in [int(x) for x in sys.argv[1:]]:
    for variant in ['full','nolin','notau0']:
        M,C=build(p,variant)
        bad,ex=count_violations(M,C)
        print(f"p={p} M={M} variant={variant} colours_used={len(set(C.tolist()))} (bound 27p={27*p}) violations={bad} example(a,d)={ex}",flush=True)
