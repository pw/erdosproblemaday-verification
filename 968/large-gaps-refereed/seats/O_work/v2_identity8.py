# Exact integer check of the deletion identity (8): for m with m+a prime (a in I),
#   Z(m) = sum_j sum_{S subset I, |S|=j} D_{F_j}(m;S)  ==  sum_j sum_{U subset I\{a}, |U|=j} D_{Ftilde_j}(m;U),
# Ftilde_j = F_j + F_{j+1}(.,0), for arbitrary real symmetric F_j on [0,inf)^j vanishing when sum v >= tau.
# Also checks a NEGATIVE control: the identity must FAIL when m+a is composite (so the test can fail).
import itertools, math, random
from sympy import divisors, isprime, factorint
from sympy.ntheory import mobius
random.seed(7)
def run(X,lam,k,tau,nm=6):
    L=math.log(X); h=int(lam*L); I=list(range(h+1,2*h+1))
    co=[random.uniform(-1,1) for _ in range(k+2)]
    def F(j,v):   # symmetric, vanishes iff sum v >= tau (on the orthant)
        if j==0: return co[0]
        s=sum(v); 
        if s>=tau: return 0.0
        return co[j]*(tau-s)**2*(1+sum(x*x for x in v))
    def DF(Ffun,j,m,S):
        if j==0: return Ffun(0,())
        lists=[[(d,mobius(d),math.log(d)/L) for d in divisors(m+b) if math.log(d)/L<tau or d==m+b] for b in S]
        tot=0.0
        for combo in itertools.product(*lists):
            mu=1
            for c in combo: mu*=c[1]
            if mu==0: continue
            tot+=mu*Ffun(j,tuple(c[2] for c in combo))
        return tot
    Ft=lambda j,v: F(j,v)+(F(j+1,tuple(v)+(0.0,)) if j+1<=k else 0.0)
    out=[]; m=X+1; found=0; neg=0
    while found<nm or neg<2:
        a=random.choice(I)
        Zl=sum(DF(F,j,m,S) for j in range(k+1) for S in itertools.combinations(I,j))
        Zr=sum(DF(Ft,j,m,U) for j in range(k+1) for U in itertools.combinations([b for b in I if b!=a],j))
        if isprime(m+a) and found<nm: out.append(('prime',m,a,Zl,Zr,abs(Zl-Zr))); found+=1
        elif not isprime(m+a) and neg<2 and abs(Zl-Zr)>1e-9: out.append(('COMPOSITE(neg ctrl)',m,a,Zl,Zr,abs(Zl-Zr))); neg+=1
        m+=random.randint(1,50)
    return h,out
for X,lam,k,tau in [(10**9,0.4,3,0.125),(10**7,0.5,3,0.45)]:
    h,out=run(X,lam,k,tau)
    print(f"X={X} lam={lam} h={h} k={k} tau={tau}")
    for o in out: print("  %-20s m=%d a=%d  lhs=%.10f rhs=%.10f |diff|=%.2e"%o)
