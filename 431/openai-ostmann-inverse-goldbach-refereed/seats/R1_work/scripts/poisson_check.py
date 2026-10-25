# Check the complete-sum identity behind eq. (3.?) "src6" (Poisson modulo Md), p. 9-10:
# sum_{r mod Md} f_d(r) chi_M(r - t_M) e(u r/(Md))
#   = sqrt(d) g_d(-u Mbar) * tau(chi_M) chi_M(u) chi_M(d) e((theta+h0) u / d)
# theta = t_M/M, h0 = -t_M Mbar mod L, d | L, g_d(b) = sqrt(d) E_{x mod d} f_d(x) e_d(-b x).
import cmath, random, math, sys
def e(x): return cmath.exp(2j*math.pi*x)
def legendre(a,p):
    a%=p
    if a==0: return 0
    return 1 if pow(a,(p-1)//2,p)==1 else -1
def jac(a,M,primes): 
    r=1
    for p in primes: r*=legendre(a,p)
    return r
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
mode = sys.argv[2] if len(sys.argv)>2 else "paper"
maxerr=0
for trial in range(40):
    Mpr = random.sample([11,13,17,19,23,29],2)
    Lpr = random.sample([3,5,7],2)
    M = Mpr[0]*Mpr[1]; L = Lpr[0]*Lpr[1]
    dpr = random.choice([[],[Lpr[0]],[Lpr[1]],Lpr])
    d = 1
    for l in dpr: d*=l
    # random partitions S_l and f_l = 1_S - sigma
    S = {}
    for l in Lpr:
        k = random.randint(1,l-1); S[l]=set(random.sample(range(l),k))
    def f(l,x): return (1.0 if x%l in S[l] else 0.0) - len(S[l])/l
    def fd(x):
        v=1.0
        for l in dpr: v*=f(l,x)
        return v
    tp = {p: random.randrange(p) for p in Mpr}
    # CRT t_M
    tM = next(t for t in range(M) if all(t%p==tp[p] for p in Mpr))
    Mbar_L = pow(M,-1,L)
    h0 = (-tM*Mbar_L) % L
    if mode=="perturb": h0 = (tM*Mbar_L) % L   # wrong sign: should FAIL
    theta = tM/M
    tau = sum(jac(z,M,Mpr)*e(z/M) for z in range(M))
    def gd(b):
        if d==1: return 1.0
        Mb=b%d
        return math.sqrt(d)*sum(fd(x)*e(-Mb*x/d) for x in range(d))/d
    Mbar_d = pow(M,-1,d) if d>1 else 0
    for u in [1,2,5,7,-3,12,30]:
        lhs = sum(fd(r)*jac(r-tM,M,Mpr)*e(u*r/(M*d)) for r in range(M*d))
        rhs = math.sqrt(d)*gd(-u*Mbar_d)*tau*jac(u,M,Mpr)*jac(d,M,Mpr)*e((theta+h0)*u/d)
        maxerr=max(maxerr,abs(lhs-rhs))
print(mode, "max |lhs-rhs| =", maxerr)
