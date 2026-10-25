import cmath, math, random, sys
from itertools import product
def e(x): return cmath.exp(2j*math.pi*x)
random.seed(3)
fac = float(sys.argv[1])  # 1.0 = paper's claim; >1 control should FAIL
# (A) Lemma 2.1 eq (2.2): sum_{(h,u)=1} |E_U e_u(hn)|^2 >= prod j/(p-j); test claim*fac
worstA = 1e9; failsA=0
for t in range(300):
    ps = random.sample([5,7,11,13],2); u = ps[0]*ps[1]; j = random.randint(1,2)
    forb = {p: set(random.sample(range(p),j)) for p in ps}
    allowed = [n for n in range(u) if all(n%p not in forb[p] for p in ps)]
    if t%3==0: U = allowed                      # equality case
    else: U = random.sample(allowed, random.randint(1,len(allowed))) + [n+u*random.randint(1,5) for n in random.sample(allowed,2)]
    lhs = sum(abs(sum(e(h*n/u) for n in U)/len(U))**2 for h in range(u) if math.gcd(h,u)==1)
    rhs = fac*math.prod(j/(p-j) for p in ps)
    worstA=min(worstA,lhs/rhs); failsA += lhs < rhs*(1-1e-9)
print(f"(A) fac={fac}: min lhs/rhs={worstA:.6f} fails={failsA}")
# (B) eq (3.?) src12 ingredient: F(s)=g_d(cs) conj g_d'(c's) on period q=[d,d'], every normalized Fourier coeff <= A=((dd')/(d,d')^2)^(-1/2)
worstB=0; failsB=0
for t in range(200):
    pool=[3,5,7]; Lp=pool
    S={l:set(random.sample(range(l),random.randint(1,l-1))) for l in Lp}
    def f(l,x): return (1.0 if x%l in S[l] else 0.0)-len(S[l])/l
    dp=random.sample(Lp,random.randint(1,2)); dq=random.sample(Lp,random.randint(1,2))
    d=math.prod(dp); dd=math.prod(dq); q=d*dd//math.gcd(d,dd)
    def g(dpr,dm,b):
        return math.sqrt(dm)*sum(math.prod(f(l,x) for l in dpr)*e(-b*x/dm) for x in range(dm))/dm
    c=random.choice([x for x in range(1,d) if math.gcd(x,d)==1]); cp=random.choice([x for x in range(1,dd) if math.gcd(x,dd)==1])
    F=[g(dp,d,c*s)*g(dq,dd,cp*s).conjugate() for s in range(q)]
    A=(d*dd/math.gcd(d,dd)**2)**-0.5
    mx=max(abs(sum(F[s]*e(-h*s/q) for s in range(q))/q) for h in range(q))
    worstB=max(worstB,mx/(A/fac)); failsB += mx > (A/fac)*(1+1e-9)
print(f"(B) fac={fac}: max coeff/(A/fac)={worstB:.4f} fails={failsB}")
