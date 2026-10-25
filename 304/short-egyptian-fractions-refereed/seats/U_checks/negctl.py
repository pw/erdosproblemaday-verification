# negative controls: show the checks in check1/check2 can fail when the claimed bound is tightened
import math, random
random.seed(11)
def logbinom(L, j): return math.lgamma(L+1)-math.lgamma(j+1)-math.lgamma(L-j+1)
def lse(xs):
    m=max(xs); return m+math.log(sum(math.exp(x-m) for x in xs))
viol=0; n=0
for S in [50.0, 200.0, 1e3, 1e4]:
    for D in [1.0, 3.0, 10.0]:
        E=D+1
        for _ in range(60):
            v=random.uniform(S/(2*math.log(S)), D*S); lz=random.choice([math.log(2), math.log(3), random.uniform(1,v)])
            L=int(E*S/lz); J=v/lz; B=1+math.log(E*S/v)
            js=range(0, min(L,int(J))+1)
            if lse([logbinom(L,j) for j in js]) > 0.3*B*J: viol+=1
            n+=1
print("(3.3) with B replaced by 0.3B: violations", viol, "of", n, "(expect >0)")
# greedy: bound minus 1 should fail sometimes
viol=0
for _ in range(20000):
    b=random.randint(2,10**random.randint(1,30)); a=random.randint(1,b-1); T=b+random.random()*b**random.choice([1,2,3])
    if T<=b: T=b+0.5
    A,C=a,b; st=0
    while A and C<T:
        z=-(-C//A); A,C=A*z-C,C*z; st+=1
    if st > math.ceil(math.log2(math.log(T)/math.log(2))) - 1: viol+=1
print("Lemma 2.3 with step bound reduced by 2: violations", viol, "(expect >0)")
