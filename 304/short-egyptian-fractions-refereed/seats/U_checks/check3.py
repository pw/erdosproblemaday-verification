# Seat U numerical checks, part 3: recurrence (5.8)-(5.10), constant arithmetic, Lemma 4.3 toy, Lemma 4.5 toy
import math, random, cmath
random.seed(3)
print("=== (5.8)->(5.10) unrolling: worst case delta_j = min(1, eps + A delta_{j+1}^alpha) vs the unrolled sum ===")
fails = 0
for _ in range(20000):
    r = random.randint(2, 60); alpha = 1 - 1/r
    d = random.randint(1, 80)
    eps = 10**random.uniform(-300, -1); A = 10**random.uniform(0, 5)
    delta = 0.0
    for j in range(d): delta = min(1.0, eps + A*delta**alpha)
    # unrolled bound sum_{i=0}^{d-1} A^{(1-alpha^i)/(1-alpha)} eps^{alpha^i}  (in logs, may exceed 1)
    terms = [((1-alpha**i)/(1-alpha))*math.log(A) + (alpha**i)*math.log(eps) for i in range(d)]
    m_ = max(terms); bound = math.exp(m_)*sum(math.exp(t-m_) for t in terms) if m_ < 700 else float('inf')
    if delta > bound*(1+1e-9): fails += 1
print("unrolling failures:", fails)

print("=== constants ===")
K, R, D0, eta = 100, 1000, 100000, 1e-4
DM = (2*R+2)*(K+2); DX = DM+2; DC = 4*DX
print("D_M, D_X, D_C =", DM, DX, DC, "| (2R+1)K =", (2*R+1)*K, "< D_M:", (2*R+1)*K < DM)
Kd = 3*DX/eta; print("K_d = %.4g, minimal r = %d" % (Kd, math.ceil(8*Kd)))
print("Lemma 4.4: need 0.4*D_C >= K+2 for U^{3D_C} >= |Z|:", 0.4*DC >= K+2, "; U^4<=e^{4 D_X S}=e^{D_C S}<=|Z|:", 4*DX == DC)
print("middle-level exponent 10*eta - 0.01*(1-eta) =", 10*eta - 0.01*(1-eta))
print("4*eta <= 0.005*(1-eta):", 4*eta <= 0.005*(1-eta))
print("Hamming: (m/4)ln2 + m ln(3/4) per m =", 0.25*math.log(2)+math.log(0.75), "<= -1/16 =", -1/16)
print("(4.15) exponent 0.08(K-3)/(K+1) =", 0.08*(K-3)/(K+1), ">= 0.05")
print("fresh-product exponent 0.75(K+1)/K =", 0.75*(K+1)/K, "< 0.8; atom exponent 0.74(K-2)/K =", 0.74*(K-2)/K, ">= 0.7")
print("sqrt(q)*||a||*||b|| exponent: 1/2 - 0.7 =", 0.5-0.7, "(<= -0.2)")
print("terminal blocks: (u^-0.005)^R = u^", -0.005*R)
QB = math.ceil(3*DC)+1
log10_inv_deltaB = math.log10(10*QB) + QB*math.log10(2)
print("Lemma 4.3 with B=3D_C: Q_B =", QB, "; log10(1/delta_B) = %.1f" % log10_inv_deltaB)
print("  => e^{-0.8 delta_B S} <= e^{-0.01 m} needs log S >~ 0.0125/delta_B, i.e. log10 log S >~ %.0f (b_0 astronomically large but absolute)" % (log10_inv_deltaB + math.log10(0.0125)))
# recurrence threshold: need c* S^{3/4}/(2 log S) > 2 r S^{1/4} + log d + log 8
r = math.ceil(8*Kd); cs = 0.001
lo, hi = 1.0, 400.0  # log10 S
for _ in range(200):
    mid = (lo+hi)/2; S = 10**mid
    lhs = cs*S**0.75/(2*math.log(S)); rhs = 2*r*S**0.25 + math.log(Kd*math.log(S)) + math.log(8)
    if lhs > rhs: hi = mid
    else: lo = mid
print("  recurrence alone needs S >~ 10^%.1f (with r = ceil(8K_d) = %d)" % (hi, r))

print("=== Lemma 4.3 toy: |sum_{n in [U,2U]} e(Z/n)| / U for integer Z with U^4<=Z<=U^6 ===")
for U in [500, 2000, 8000]:
    worst = 0
    for _ in range(6):
        Z = random.randint(U**4, U**6)
        s = sum(cmath.exp(2j*math.pi*((Z % n)/n)) for n in range(U, 2*U+1))
        worst = max(worst, abs(s)/U)
    print(f"  U={U}: max |S|/U over 6 random Z = {worst:.4f}  (trivial bound 1; U^-1/2 = {U**-0.5:.4f})")

print("=== Lemma 4.5 mechanism toy (outside its parameter range): E|2^-m sum_I e(t_I/u)|^2, Monte Carlo ===")
def primes_in(a, b):
    out = []
    for n in range(a, b+1):
        if n > 1 and all(n % p for p in range(2, int(n**0.5)+1)): out.append(n)
    return out
P = primes_in(1000, 2000)
for (m, u) in [(10, 1000003), (12, 10**7+19), (12, 2**23)]:
    vals = []
    for _ in range(40):
        pr = [(random.choice(P), random.choice(P)) for _ in range(m)]
        # all 2^m subset products mod u
        prods = [1]
        for (p0, p1) in pr:
            prods = [x*p0 % u for x in prods] + [x*p1 % u for x in prods]
        s = sum(cmath.exp(2j*math.pi*x/u) for x in prods)/len(prods)
        vals.append(abs(s)**2)
    print(f"  m={m}, u={u}: mean |.|^2 = {sum(vals)/len(vals):.2e}  (2^-m = {2**-m:.2e})")
