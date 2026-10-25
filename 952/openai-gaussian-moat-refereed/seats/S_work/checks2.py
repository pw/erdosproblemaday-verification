# Exact toy test of Lemma 5.1's inequality in the Gaussian setting:
#   E_S H(F_S(Y)) - H(H) <= s * av_c H(phi_c(Y) | H)
import math, random, itertools
from collections import defaultdict
random.seed(7)
primes=[29,37,41,53]  # p = 1 mod 4 in [29,58]
def sqrtm1(p):
    for x in range(p):
        if (x*x+1)%p==0: return x
roots={p:sqrtm1(p) for p in primes}
coords=[(p,s) for p in primes for s in (+1,-1)]
def phi(c,z):
    p,s=c; a,b=z; return (a+s*roots[p]*b)%p
def H(dist):
    return -sum(v*math.log(v) for v in dist.values() if v>0)
def ent_of(joint, f):
    d=defaultdict(float)
    for w,pr in joint.items(): d[f(w)]+=pr
    return H(d)
def cond(joint,f,g):  # H(f|g)
    return ent_of(joint,lambda w:(f(w),g(w)))-ent_of(joint,g)
worst=-1e9
for trial in range(200):
    # random joint law of (Y,Hdata): Y in a small box of Z^2, H in {0..3}
    pts=[(random.randint(-40,40),random.randint(-40,40)) for _ in range(random.randint(2,25))]
    joint={}
    for y in pts:
        for hh in range(random.randint(1,4)):
            joint[(y,hh)]=random.random()
    tot=sum(joint.values()); joint={k:v/tot for k,v in joint.items()}
    k=len(primes)
    for s in range(1,k+1):
        # E_S over s-subsets of primes and signs
        vals=[]
        for sub in itertools.combinations(primes,s):
            for signs in itertools.product((+1,-1),repeat=s):
                S=list(zip(sub,signs))
                vals.append(ent_of(joint,lambda w:tuple(phi(c,w[0]) for c in S)))
        lhs=sum(vals)/len(vals)-ent_of(joint,lambda w:w[1])
        rhs=s*sum(cond(joint,lambda w,c=c:phi(c,w[0]),lambda w:w[1]) for c in coords)/len(coords)
        worst=max(worst,lhs-rhs)
print("max of LHS-RHS (should be <= 0):",worst)
