# Seat S numerical sanity checks: section 5 inner inequalities + small exact tests
import math, random, itertools
from fractions import Fraction as Fr
random.seed(1)

print("== band arithmetic ==")
print("0.05 - 1.3/100 =", 0.05 - 1.3/100)
print("top->mid gap 0.8-0.30 =", 0.8-0.30, " mid->bottom 0.20-0.10 =", 0.20-0.10)

print("== (tau+4d)(1-d) >= tau+2d on grid ==")
worst = 1e9
for i in range(0, 376):
    tau = i/1000
    if tau<=0: continue
    for j in range(1, 157):
        d = j/10000
        lhs = (tau+4*d)*(1-d) - (tau+2*d)
        worst = min(worst, lhs/d)
print("min of [(tau+4d)(1-d)-(tau+2d)]/d over tau<=3/8, d<=1/64:", worst, "(should be >= 2-3/8-4/64 =", 2-3/8-4/64, ")")

print("== v+(1-v)log(1-v) >= v^2/2 ==")
print(min(v+(1-v)*math.log(1-v)-v*v/2 for v in [k/10000 for k in range(1,10000)]))

print("== exact binomial lower tail vs claimed bound ==")
def binom_cdf(n, lam, x):
    # P(Bin(n,lam) <= x), x real
    m = math.floor(x+1e-12)
    if m < 0: return 0.0
    s = 0.0
    for k in range(0, min(m,n)+1):
        s += math.comb(n,k)*lam**k*(1-lam)**(n-k)
    return s
viol = 0; tests=0
for _ in range(3000):
    n = random.randint(1,400)
    tau = random.uniform(0.001, 3/8)
    d = random.uniform(1e-4, 1/64)
    up_over_p = random.uniform(1e-3,1)
    lam = (tau+2*d)*up_over_p
    thr = n*(lam - d*up_over_p)
    pr = binom_cdf(n, lam, thr)
    bnd = math.exp(-n*(d*up_over_p)**2/(2*lam))
    tests += 1
    if pr > bnd*(1+1e-9): viol += 1
print("binomial lower-tail violations:", viol, "of", tests)

print("== identity sum_x |(K-x) cap E| = |K||E| in Z/p ==")
bad=0
for _ in range(500):
    p = random.choice([5,13,17,29,37,41,53,61])
    K = set(random.sample(range(p), random.randint(1,p)))
    E = set(random.sample(range(p), random.randint(0,p)))
    s = sum(len({(k-x)%p for k in K} & E) for x in range(p))
    if s != len(K)*len(E): bad+=1
print("identity failures:", bad)

print("== h(u) <= u log(e/u) ==")
h=lambda u: -u*math.log(u)-(1-u)*math.log(1-u)
print(max(h(u)-u*math.log(math.e/u) for u in [k/10000 for k in range(1,10000)]))
