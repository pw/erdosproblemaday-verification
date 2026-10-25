import itertools, random
from fractions import Fraction as Fr
# 1) mixed-radix embedding of Theorem A.7: Phi(Q) in [L], and two-face identities reflected
random.seed(1)
for trial in range(200):
    n=random.randint(1,3); T=[random.randint(1,5) for _ in range(n)]
    b=[4*t for t in T]; a=[1]
    for i in range(1,n): a.append(a[-1]*b[i-1])
    L=1
    for x in b: L*=x
    Q=list(itertools.product(*[range(t) for t in T]))
    Phi=lambda x: 1+sum(ai*xi for ai,xi in zip(a,x))
    assert all(1<=Phi(x)<=L for x in Q)
    pts={}
    for u in Q:
        for v in Q:
            pts.setdefault(Phi(u)+Phi(v),set()).add(tuple(ui+vi for ui,vi in zip(u,v)))
    assert all(len(s)==1 for s in pts.values())
print("A.7 box embedding ok")
# 2) cyclic partition: diameter < N/3, length >= N/8
for N in range(1,400):
    k=min(4,N); sizes=[N//k+(1 if i<N%k else 0) for i in range(k)]
    assert all(s-1 < N/3 and s >= N/8 for s in sizes), N
print("A.7 cyclic partition ok")
# 3) D.2 kernels
import math
for b in [Fr(1),Fr(1,4),Fr(1,3)]:
    r=b*(1-b)
    # E over e1=+-1 of nu1(u) nu2(v), symbolic check at random rational u,v
    for _ in range(20):
        u=Fr(random.randint(0,20),random.randint(1,5)); v=Fr(random.randint(0,20),random.randint(1,5))
        # C1=b+s e1, C2=b-s e1, s^2=r ; E[C1]=b, E[C2]=b, E[C1C2]=b^2-r, E[C1^2]=b^2+r
        EC1C2=b*b-r; EC2=b*b+r
        B=1+b*(u-1)+b*(v-1)+EC1C2*(u-1)*(v-1)
        assert B==1+b*(u+v-2)+(2*b*b-b)*(u-1)*(v-1)
        K=1+2*b*(u+v-2)/2*1  # placeholder
        Ksame=1+b*(u-1)+b*(v-1)+EC2*(u-1)*(v-1)
        assert Ksame==1-b+b*u*v
    if b==Fr(1,4):
        u,v=Fr(7),Fr(3); assert 1+b*(u+v-2)+(2*b*b-b)*(u-1)*(v-1)==Fr(3,8)+Fr(3,8)*u+Fr(3,8)*v-Fr(1,8)*u*v
tau=Fr(1,10); val=Fr(9,8)*(1-tau/18)-Fr(1,8)*(1-tau); assert val==1+tau/16
print("D.2 kernels and deficit ok")
# 4) C.4(2) numeric spot check
for _ in range(2000):
    M=random.uniform(1,50); xs=[random.uniform(0,M) for _ in range(5)]
    m=sum(xs)/5
    if m>1: xs=[x/m for x in xs]
    EX=sum(xs)/5; EX2=sum(x*x for x in xs)/5; c=EX2-1
    if c>0: assert sum(math.sqrt(x) for x in xs)/5 <= 1-c/(2*(1+math.sqrt(M))**2)+1e-12
print("C.4 ok")
