import math, random, itertools, cmath
random.seed(1)
# 1. sum_{j=1}^k r_j log r_j = r log r - 2 r log 2 + 2 log 2, r=2^k ; control: perturbed formula must fail
for k in range(1,15):
    r=2**k
    lhs=sum(2**(j-1)*math.log(2**(j-1)) for j in range(1,k+1))
    rhs=r*math.log(r)-2*r*math.log(2)+2*math.log(2)
    bad=r*math.log(r)-2*r*math.log(2)+math.log(2)
    assert abs(lhs-rhs)<1e-6*max(1,lhs), (k,lhs,rhs)
    if k>1: assert abs(lhs-bad)>1e-3
print("sum r_j log r_j identity OK (control fails as expected)")
# 2. a log a <= (a-1)(log r + 1) for 1<=a<=r ; control: (a-1)log r alone fails somewhere
viol=0
for r in range(1,300):
    for a in range(1,r+1):
        assert a*math.log(a) <= (a-1)*(math.log(r)+1)+1e-12
        if a*math.log(a) > (a-1)*math.log(r)+1e-12: viol+=1
print("a log a bound OK; control violations of weaker bound:",viol)
# 3. (am)! <= (m!)^a a^{am}; control (am)! <= (m!)^a fails
for a in range(1,8):
    for m in range(1,15):
        assert math.lgamma(a*m+1) <= a*math.lgamma(m+1)+a*m*math.log(a)+1e-9
        if a>1: assert math.lgamma(a*m+1) > a*math.lgamma(m+1)
print("multinomial bound OK; control fails")
# 4. (9.7) and (9.21) coefficient arithmetic
from fractions import Fraction as Fr
# exponent/(r_j m) = -Delta_j/(r_j m) + Delta0/m + log z + 1/4 log r_j + C
# Delta_j/(r_j m) = B_D + B_z log z + 0.4 log r_j ; Delta0/m = B_s + 8 log z
print("(9.7) log r_j coeff:", Fr(-2,5)+Fr(1,4), " log z coeff: -B_z + 8 + 1 = 9-B_z")
print("(9.21) log r coeff:", Fr(-3,4)+Fr(2,5), " log z coeff: B_z+8 (E_k) + 8 (Delta0) = B_z+16 ; B_s coeff 2")
# 5. bad-arrangement count, brute force small r,m: count second arrangements with > 3r/4 components vs bound
def components(r,assign1,assign2):
    # vertices: left leaves 0..r-1, right leaves r..2r-1, edge per variable
    parent=list(range(2*r))
    def f(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for v in range(len(assign1)):
        a=f(assign1[v]); b=f(r+assign2[v])
        if a!=b: parent[a]=b
    return len({f(x) for x in range(2*r)})
for r,m in [(4,1),(4,2),(8,1)]:
    n=r*m
    first=[i//m for i in range(n)]  # leaf of variable i in first arrangement (slot order)
    bad=0; tot=0
    for perm in itertools.permutations(range(n)):
        second=[0]*n
        for slot,var in enumerate(perm): second[var]=slot//m
        t=components(r,first,second)
        tot+=1
        if t>3*r/4: bad+=1
    bound_main=math.factorial(m)**r*math.exp(0.25*(math.log(r)+1)*r*m)
    print(f"r={r} m={m}: bad={bad} total={tot}  (m!)^r e^(1/4(log r+1) rm)={bound_main:.1f}  ratio bad/(m!)^r = {bad/math.factorial(m)**r:.1f}")
# 6. CRT identity sum_{a in U_C} F(a) = C with g(0)=0, mean |g|^2 = 1 ; control with g(0)!=0 fails
def make_g(l, zero=True):
    S=set(random.sample(range(l), l//2))
    sigma=len(S)/l
    F=[((1 if x in S else 0)-sigma)/math.sqrt(sigma*(1-sigma)) for x in range(l)]
    g=[math.sqrt(l)*sum(F[x]*cmath.exp(-2j*math.pi*b*x/l) for x in range(l))/l for b in range(l)]
    if not zero: g[0]=0.7
    return g
for zero in (True,False):
    ls=[5,7,11]; C=5*7*11
    gs={l:make_g(l,zero) for l in ls}
    s,d,q=3,2,13
    tot=0
    for a in range(C):
        if math.gcd(a,C)!=1: continue
        val=1
        for l in ls:
            al=(s*pow(d*q*(C//l),-1,l))%l
            arg=(al*pow(a,-1,l))%l
            val*=abs(gs[l][arg])**2
        tot+=val
    print("CRT sum", "normalized" if zero else "control g(0)!=0", round(tot,6), "C=",C)
