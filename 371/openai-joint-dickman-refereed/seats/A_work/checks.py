import math, random, itertools
import numpy as np
from scipy import integrate

random.seed(1)
# 1. elementary progression count
worst = 0
for _ in range(20000):
    x = random.uniform(10, 1e6); a_ = random.uniform(0.1, 3); b_ = a_ + random.uniform(0.01, 3)
    q = random.randint(1, 50); d = random.randint(1, 200)
    if math.gcd(q, d) != 1: continue
    a = random.randint(0, q-1)
    lo, hi = a_*x, b_*x
    # count n in (lo,hi], n = a mod q, d | n  <=> n = n0 mod qd
    # find residue n0 mod qd by CRT
    n0 = next(n for n in range(q*d) if n % q == a and n % d == 0)
    M = q*d
    cnt = math.floor((hi - n0)/M) - math.floor((lo - n0)/M)
    err = cnt - (b_-a_)*x/M
    worst = max(worst, abs(err))
print("1. max |count - (beta-alpha)x/(qd)| =", worst, "(<=1 expected)")

# 2. constants
h0 = (1-math.log(2))/2
print("2. alpha0=1.6log2=", 1.6*math.log(2), " 2h0=", 2*h0, " 1-6h0=", 1-6*h0, " 1-5h0=", 1-5*h0)
for name, val, lim, k in [("2(h0+t)<.32", 2*h0, .32, 2), ("1-6(..)>.07", 1-6*h0, .07, 6), ("1-5(..)>.229", 1-5*h0, .229, 5)]:
    print("   tau bound for", name, ": tau <", abs(val-lim)/(k*math.log(2)))
print("   4h0 + 2(1)log2 - 1 (exponent of crude D_B sup) =", 4*h0 + 2*math.log(2) - 1)
print("   T exponent .32 vs Q_B exponent 2h0 =", 2*h0)
print("   B*R^{-alpha0} at B=1e6:", 1e6**(1-1.6*math.log(2))*(1000*math.log(1e6))**(1.6*math.log(2)))

# 3. |1-z^m| <= m|1-z| => 1-Re z^m <= m^2 (1-Re z)
worst = 0
for _ in range(200000):
    m = random.randint(1, 12); th = random.uniform(-math.pi, math.pi)
    z = complex(math.cos(th), math.sin(th))
    lhs = 1 - (z**m).real; rhs = m*m*(1 - z.real)
    worst = max(worst, lhs - rhs)
print("3. max (1-Re z^m) - m^2(1-Re z) =", worst, "(<=0 expected)")

# 4. tensor Vandermonde interpolation for J=3
J = 3
nodes = [1.0, 0.8, 0.6, 0.4][:J+1]
zeta = [complex(math.cos(1.1), math.sin(1.1)), complex(math.cos(2.3), math.sin(2.3))]
mu = 0.37+0.11j
V = np.array([[z**b for z in nodes] for b in range(J+1)])  # rows b, cols node
pts = list(itertools.product(range(J+1), repeat=J-1))
target = np.array([zeta[0]**b1*zeta[1]**b2 - mu for (b1,b2) in pts])
basis = np.array([[nodes[i]**b1*nodes[k]**b2 for (i,k) in itertools.product(range(J+1), repeat=2)] for (b1,b2) in pts])
c = np.linalg.solve(basis.astype(complex), target)
print("4. interpolation residual:", np.max(np.abs(basis@c - target)), " sum|c_l| =", np.sum(np.abs(c)))

# 5. Mertens-type: sum over P0<p<=e^{cB}... skip; fair split identity
S = [random.choice([101,103,107,109,113,127,131]) for _ in range(5)]
S = sorted(set(S)); B = 50.0; v = 0.7
exp_split = 0.0
for mask in range(1 << len(S)):
    b = 1
    for i,p in enumerate(S):
        if mask >> i & 1: b *= p
    exp_split += math.exp(-v*math.log(b)/B) / (1 << len(S))
prod = 1.0
for p in S: prod *= (1 + p**(-v/B))/2
print("5. fair-split identity:", exp_split, prod)
