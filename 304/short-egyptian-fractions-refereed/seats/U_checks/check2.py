# Seat U numerical checks, part 2: pieces of Lemma 3.1
import random, math
from sympy import factorint, primerange
random.seed(7)

def logbinom(L, j):
    return math.lgamma(L+1) - math.lgamma(j+1) - math.lgamma(L-j+1)

def logsumexp(xs):
    m = max(xs); return m + math.log(sum(math.exp(x-m) for x in xs))

# (3.3): sum_{j<=v/log z} C(L,j) <= q^{-v/log z}(1+q)^L <= exp(B v/log z), L=floor(ES/log z), q=v/(ES), B=1+log(ES/v)
fails = 0; worst = -1e9; cnt = 0
for S in [50.0, 200.0, 1e3, 1e4, 1e5]:
    for D in [1.0, 3.0, 10.0, 100.0]:
        E = D + 1
        for _ in range(60):
            v = random.uniform(S/(2*math.log(S)), D*S)
            lz = random.choice([math.log(2), math.log(3), math.log(101), math.log(10007), random.uniform(1, v)])
            L = int(E*S/lz); J = v/lz
            q = v/(E*S); B = 1 + math.log(E*S/v)
            js = [j for j in range(0, min(L, int(J))+1)]
            lhs = logsumexp([logbinom(L, j) for j in js]) if js else -1e9
            mid = -J*math.log(q) + L*math.log1p(q)
            rhs = B*J
            cnt += 1
            if not (lhs <= mid + 1e-9 and mid <= rhs + 1e-9): fails += 1
            worst = max(worst, lhs - rhs)
print(f"(3.3) binomial bound: {cnt} cases, failures = {fails}, max(log lhs - log rhs) = {worst:.3f}")

# prefix lemma: for n > sqrt(Y), d = longest initial product (primes in nondecreasing order, with multiplicity) <= sqrt(Y),
# p = next prime; check d <= sqrt(Y) < d p, and d_X(n) <= tau(d) * d_X(n/d)
def divisors_from_fact(f):
    ds = [1]
    for p, e in f.items():
        ds = [x * p**k for x in ds for k in range(e+1)]
    return ds
def tau(f):
    r = 1
    for e in f.values(): r *= e+1
    return r
fails = 0; cnt = 0
for _ in range(3000):
    n = random.randint(2, 10**random.randint(3, 15))
    f = factorint(n)
    plist = sorted(p for p, e in f.items() for _ in range(e))
    X = random.uniform(2, n)
    Y = random.uniform(math.sqrt(X), X)
    if n <= math.sqrt(Y): continue
    d = 1; idx = 0
    while idx < len(plist) and d*plist[idx] <= math.sqrt(Y):
        d *= plist[idx]; idx += 1
    p = plist[idx]
    fd = factorint(d); fe = factorint(n//d)
    dX = sum(1 for a in divisors_from_fact(f) if a <= X)
    dXe = sum(1 for a in divisors_from_fact(fe) if a <= X)
    ok = (d <= math.sqrt(Y) < d*p) and all(q <= p for q in fd) and all(q >= p for q in fe) and dX <= tau(fd)*dXe
    cnt += 1
    if not ok: fails += 1
print(f"prefix inequality d_X(n) <= tau(d) d_X(n/d): {cnt} cases, failures = {fails}")

# (3.6): sum_{p<=T} 1/p <= e*log(1+log T)
N = 10**7
sieve = bytearray([1])*(N+1); sieve[0]=sieve[1]=0
for i in range(2, int(N**0.5)+1):
    if sieve[i]: sieve[i*i::i] = bytearray(len(range(i*i, N+1, i)))
s = 0.0; fails = 0; T_checks = set([2,3,10,100,1000,10**4,10**5,10**6,10**7])
worst = 0
for t in range(2, N+1):
    if sieve[t]: s += 1/t
    if t in T_checks or (t % 99991 == 0):
        rhs = math.e*math.log(1+math.log(t))
        if s > rhs: fails += 1
        worst = max(worst, s/rhs)
print(f"(3.6) sum 1/p <= e log(1+log T) up to 1e7: failures = {fails}, max ratio = {worst:.3f}")

# Hamming: P(Bin(m,1/2) < m/4) <= e^{-m/16}
fails = 0
for m in range(4, 3001):
    lp = [logbinom(m, k) - m*math.log(2) for k in range(0, m+1) if k < m/4]
    if lp and logsumexp(lp) > -m/16 + 1e-12: fails += 1
print(f"Hamming tail P(B<m/4) <= e^(-m/16), m=4..3000: failures = {fails}")

# toy moment, truncated divisor function in a short interval far from 0
def dX(n, X):
    return sum(1 for a in divisors_from_fact(factorint(n)) if a <= X)
X = 10**6; Y = 1000; r = 3
for N in [random.randint(10**12, 10**13) for _ in range(3)] + [math.lcm(*range(1, 30))]:
    mom = sum(dX(N+h, X)**r for h in range(1, Y+1))
    print(f"  toy: N={N:.3e}  X=1e6 Y=1e3 r=3: (1/Y) sum d_X(N+h)^3 = {mom/Y:.1f}  (log X)^7 = {math.log(X)**7:.2e}")
