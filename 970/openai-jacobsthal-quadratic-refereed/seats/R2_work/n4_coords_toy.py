# N4: faithful toy of Section 9.1 / Prop 9.2.
# (a) Exact check of the arithmetic coordinates (9.2)-(9.9): for every prime p in a bin, impose the aligned class
#     a_p = A/D mod p, enumerate the actual hit progression n = b + q_f(k+pj), and compare the direct survivor count on
#     the common interval with the count computed from (m0, k) via the avoidance rules (9.9). Control: shifted m0 must fail.
# (b) Dichotomy: large T (C0/R large) -> empirical second moment over p of (S-JV0)/JV0 close to the independent model;
#     small T (C0=1, H=1, small classes aligned to A/D) -> a constant bias of the size Prop 9.2 cannot exclude
#     (these are the "hard endpoints" passed to Section 10). This is a sanity check of mechanism, not of asymptotics.
import math, random
from math import gcd
def primes(n):
    return [p for p in range(2,n+1) if all(p%q for q in range(2,int(p**.5)+1))]
def isp(n): return n>1 and all(n%q for q in range(2,int(n**.5)+1))
def inv(a,m): return pow(a%m,-1,m)
def crt(rs,ms):
    x,M=0,1
    for r,m in zip(rs,ms):
        t=((r-x)*inv(M,m))%m; x+=M*t; M*=m
    return x%M, M
small=primes(13); V0=1.0
for t in small: V0*=1-1/t
def instance(D,qA_primes,qE_primes,C0,small_aligned,R,xi,Jtarget,seed):
    rnd=random.Random(seed)
    qf_primes=qA_primes+qE_primes; qf=1
    for l in qf_primes: qf*=l
    qfA=1
    for l in qA_primes: qfA*=l
    qfE=qf//qfA; H=D*qfE
    # choose b (CRT rep) first with prescribed non-aligned classes random, then A = D b - qfA*C0
    # need classes a_l for l in qA aligned: automatic from A definition; choose b mod qE random nonzero patterns
    a={}
    for l in qf_primes: a[l]=rnd.randrange(l)
    b,_=crt([a[l] for l in qf_primes],qf_primes)
    if b==0: b=qf
    # force alignment at qA primes: we instead define A from b and C0:
    A=D*b-qfA*C0
    assert gcd(A,D)==1 and gcd(C0,H)==1
    for l in qA_primes: assert (D*a[l]-A)%l==0
    for l in qE_primes: assert (D*a[l]-A)%l!=0
    for t in small:
        if small_aligned and D%t: a[t]=(A*inv(D,t))%t
        else: a[t]=rnd.randrange(t)
    J=Jtarget; Y=int(J*(1+xi)*R*qf)+qf*R  # so that floor(Y/((1+xi)R qf)) >= J
    Jc=Y//(int((1+xi)*R)*qf+1)  # conservative common interval length (as in Section 9, using p<=(1+xi)R)
    Jc=min(Jc,J)
    out=[]
    for p in range(R,int((1+xi)*R)+1):
        if not isp(p) or H%p==0 or p in qf_primes: continue
        ap=(A*inv(D,p))%p
        n0,_=crt([b,ap],[qf,p])
        if n0==0: n0=qf*p
        # direct count on common interval
        Sd=sum(1 for j in range(Jc) if all((n0+qf*p*j-a[t])%t for t in small))
        # coordinates: k with C0+H k = 0 mod p, k in [0,p)
        k=((-C0)*inv(H,p))%p
        assert n0==b+qf*k, (n0,b,qf,k)
        m0=(C0+H*k)//p; assert (C0+H*k)%p==0
        assert C0/p<=m0<C0/p+H and (p*m0-C0)%H==0
        def Sform(mm,kk):
            c=0
            for j in range(Jc):
                ok=True
                for t in small:
                    if H%t: ok = (p*qfA*(mm+H*j)-(D*a[t]-A))%t!=0
                    else:   ok = (kk+p*j-(a[t]-b)*inv(qf,t))%t!=0
                    if not ok: break
                c+=ok
            return c
        Sf=Sform(m0,k); Sctrl=Sform(m0+1,k)
        out.append((p,Sd,Sf,Sctrl))
    return out,Jc,H,abs(C0)/R
def model_relvar(J):
    odd=[t for t in small if t>2]; c=1.0
    for t in odd: c*=1-1/(t-1)**2
    off=0.0
    for h in range(1,J):
        G=0.0 if h%2 else 2*c*math.prod(1+1/(t-2) for t in odd if h%t==0)
        off+=2*(J-h)*(G-1)
    return (J*V0*(1-V0)+V0*V0*off)/(J*V0)**2
for label,args in [
  ("large T, H=3*23, small classes random", dict(D=3,qA_primes=[17,19],qE_primes=[23],C0=10**9+7,small_aligned=False,R=3000,xi=0.2,Jtarget=60,seed=1)),
  ("large T, H=1, small classes ALIGNED  ", dict(D=1,qA_primes=[17,19,23],qE_primes=[],C0=10**9+7,small_aligned=True,R=3000,xi=0.2,Jtarget=10,seed=2)),
  ("SMALL T: C0=1,H=1, small aligned     ", dict(D=1,qA_primes=[17,19,23],qE_primes=[],C0=1,small_aligned=True,R=3000,xi=0.2,Jtarget=10,seed=3)),
  ("SMALL T: C0=1,H=3*23, small aligned  ", dict(D=3,qA_primes=[17,19],qE_primes=[23],C0=1,small_aligned=True,R=3000,xi=0.2,Jtarget=10,seed=4)),
]:
    out,Jc,H,c=instance(**args)
    agree=all(Sd==Sf for _,Sd,Sf,_ in out); ctrl_bad=sum(Sd!=Sc for _,Sd,_,Sc in out)
    m=Jc*V0
    mean=sum(Sd for _,Sd,_,_ in out)/len(out)
    mom2=sum(((Sd-m)/m)**2 for _,Sd,_,_ in out)/len(out)
    print("%s n_p=%d J=%d H=%d |C0|/R=%.3g | coords exact:%s ctrl mismatches:%d/%d | mean S/JV0=%.3f  E((S-JV0)/JV0)^2=%.4f  model=%.4f"%(
        label,len(out),Jc,H,c,agree,ctrl_bad,len(out),mean/m,mom2,model_relvar(Jc)))
