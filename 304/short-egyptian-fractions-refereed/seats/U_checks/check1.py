# Seat U numerical checks, part 1: identities, greedy (Lemma 2.3), Takenouchi (Lemma 2.2)
import random, math
from fractions import Fraction as F
random.seed(20261021)

# --- (4.1)/(5.4)/intro identity ---
bad = 0
for trial in range(200000):
    M_t = random.randint(1, 10**6)          # M/t
    t = random.randint(1, 10**9)
    M = M_t * t
    Q = random.choice([1, random.randint(1, 10**12)])
    u = random.randint(1, 10**9)
    z = -(-Q*t // u)                        # ceil(Qt/u)
    h = u*z - Q*t
    assert z >= 1 and 0 <= h < u
    lhs = F(u, M*Q)
    rhs = F(1, (M//t)*z) + F(1, z) * F(h, M*Q)
    if lhs != rhs: bad += 1
    # (5.4) with C_j = Q * c1, C_{j+1} = c1 (C_{j+1} | C_j)
    c1 = random.choice([1, random.randint(1, 1000)])
    Cj, Cj1 = Q*c1, c1
    z2 = -(-Cj*t // u); h2 = u*z2 - Cj*t
    rhs2 = F(1, (M//t)*z2) + F(1, z2*(Cj//Cj1)) * F(h2, M*Cj1)
    if F(u, M*Cj) != rhs2: bad += 1
    # h is least nonneg residue of -Qt mod u
    if h != (-Q*t) % u: bad += 1
print("identity checks: failures =", bad)

# --- Lemma 2.3 greedy ---
fails = 0; maxratio = 0
for trial in range(20000):
    b = random.randint(2, 10**random.randint(1, 30))
    a = random.randint(1, b-1)
    T = b + random.random() * b**random.choice([1, 2, 3])  # real T > b
    if T <= b: T = b + 0.5
    A, C = a, b
    steps = 0
    bound = 1 + math.ceil(math.log2(math.log(T)/math.log(2)))
    zs = []
    while True:
        if A == 0: break
        if C >= T: break
        z = -(-C // A)
        zs.append(z)
        A, C = A*z - C, C*z
        steps += 1
    ok = steps <= bound and all(z >= 2 for z in zs)
    if A > 0:
        ok = ok and (1 <= A <= a) and (T <= C < T*T)
        ok = ok and (F(a, b) == sum((F(1, z) for z in zs), F(0)) + F(A, C))
    else:
        ok = ok and F(a, b) == sum((F(1, z) for z in zs), F(0))
    if not ok: fails += 1
print("Lemma 2.3 greedy: failures =", fails)

# --- Lemma 2.2 Takenouchi ---
def takenouchi(lst):
    lst = sorted(lst)
    it = 0
    while True:
        it += 1
        dup = None
        for i in range(len(lst)-1):
            if lst[i] == lst[i+1]:
                dup = lst[i]; break
        if dup is None: return lst, it
        lst.remove(dup); lst.remove(dup)
        if dup % 2 == 0:
            p = dup // 2
            assert p >= 2
            new = [p+1, p*(p+1)]
            inc = (p-1)**2
        else:
            p = (dup-1)//2
            assert p >= 1
            new = [p+1, (p+1)*(2*p+1)]
            inc = 2*p*p
        assert sum(new) - 2*dup == inc
        lst = sorted(lst + new)
fails = 0; tried = 0
while tried < 5000:
    k = random.randint(1, 12)
    lst = [random.randint(2, 30) for _ in range(k)]
    # force repeats
    if k >= 2 and random.random() < 0.7:
        lst[1] = lst[0]
    s = sum(F(1, d) for d in lst)
    if s >= 1: continue
    tried += 1
    out, it = takenouchi(lst)
    if not (len(out) == k and len(set(out)) == k and min(out) >= 2 and sum(F(1, d) for d in out) == s):
        fails += 1
print("Lemma 2.2 Takenouchi: tried", tried, "failures =", fails)

# --- step bound sanity in Lemma 2.3 proof: x - 1/ceil(1/x) <= x^2/(1+x)
fails = 0
for trial in range(100000):
    C = random.randint(2, 10**8); A = random.randint(1, C-1)
    x = F(A, C); r = x - F(1, -(-C//A))
    if not (0 <= r <= x*x/(1+x)): fails += 1
print("x - 1/ceil(1/x) <= x^2/(1+x): failures =", fails)
