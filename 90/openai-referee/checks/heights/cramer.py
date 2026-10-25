# Numerical check of the Cramer step in Prop 4.4 and of |ab-1| <= 8*B*tau, with failing controls.
import random, cmath, math
random.seed(167)

def solve_dZ(D, E):
    D1, D2, D3 = D; E1, E2, E3 = E
    a11, a12, b1 = 1/D2 - 1/D1, D2 - D1, E2 - E1
    a21, a22, b2 = 1/D3 - 1/D1, D3 - D1, E3 - E1
    det = a11*a22 - a12*a21
    dZ = (b1*a22 - a12*b2)/det
    dW = (a11*b2 - b1*a21)/det
    return dZ, dW, det

def rand_D(B, r):
    while True:
        D = [cmath.rect(math.exp(random.uniform(-math.log(B), math.log(B))), random.uniform(0, 2*math.pi)) for _ in range(3)]
        if all(abs(D[i]-D[j]) >= r for i in range(3) for j in range(i+1, 3)):
            return D

def worst_E(D, eps):
    # |dZ| is linear in E: dZ = (E1(D2-D3)+E2(D3-D1)+E3(D1-D2))/det ; align phases to maximise
    D1, D2, D3 = D
    co = [D2 - D3, D3 - D1, D1 - D2]
    return [eps*cmath.exp(-1j*cmath.phase(c)) for c in co]

worst_ratio = 0.0; n = 0; viol = 0
for B in (2.0, 3.0, 5.0):
    for r in (0.9, 0.5, 0.2, 0.05):
        tau = 0.999*min(1.0, r**4/(128*B**5))
        eps = 8*B*tau
        for _ in range(4000):
            D = rand_D(B, r)
            for E in (worst_E(D, eps), [eps*cmath.exp(1j*random.uniform(0, 6.3))*random.random() for _ in range(3)]):
                dZ, dW, det = solve_dZ(D, E)
                n += 1
                assert abs(det) >= r**3/B**3 - 1e-12
                bound = 64*B**5*tau/r**3
                worst_ratio = max(worst_ratio, abs(dZ)/bound)
                if not (abs(dZ) <= bound + 1e-12 and abs(dZ) < r/2):
                    viol += 1
print(f"Cramer: {n} systems, violations={viol}, max |dZ|/(64B^5tau/r^3) = {worst_ratio:.4f}")

# full three-equation check: random (dZ,dW,D), E_j computed exactly; ratio |dZ| r^3 / (B^4 max|E|) must be <= 8
worst = 0.0
for _ in range(200000):
    B = random.choice([2.0, 3.0, 5.0])
    D = [cmath.rect(math.exp(random.uniform(-math.log(B), math.log(B))), random.uniform(0, 2*math.pi)) for _ in range(3)]
    r = min(abs(D[i]-D[j]) for i in range(3) for j in range(i+1, 3))
    dZ = cmath.rect(10**random.uniform(-6, 0), random.uniform(0, 6.3)); dW = cmath.rect(10**random.uniform(-6, 0), random.uniform(0, 6.3))
    E = [dZ/d + d*dW + dZ*dW for d in D]
    worst = max(worst, abs(dZ)*r**3/(B**4*max(abs(e) for e in E)))
print(f"three-equation: max |dZ| r^3/(B^4 max|E_j|) = {worst:.4f}  (paper's implication needs <= 8)")

# 8 B tau: |a|,|b| <= 2B, a'b'=1, |a-a'|,|b-b'| <= sqrt2*tau  =>  |ab-1| <= 8 B tau   (B>=2, tau<1)
worst8 = 0.0
for _ in range(300000):
    B = random.uniform(2, 6); tau = random.uniform(0, 1)
    a = cmath.rect(random.uniform(0, 2*B), random.uniform(0, 6.3))
    d1 = cmath.rect(math.sqrt(2)*tau*random.random()**0.1, random.uniform(0, 6.3))
    ap = a + d1
    if ap == 0: continue
    bp = 1/ap
    d2 = cmath.rect(math.sqrt(2)*tau*random.random()**0.1, random.uniform(0, 6.3))
    b = bp + d2
    if abs(b) > 2*B: continue
    worst8 = max(worst8, abs(a*b - 1)/(B*tau))
print(f"8B*tau: max |ab-1|/(B tau) = {worst8:.4f} (needs <= 8; analytic sup 4*sqrt2 + 2tau/B <= 6.66)")

# ---- CONTROLS (must FAIL) ----
# (a) violate (4.12): tau = 50 * r^4/(128 B^5); worst-case E gives |dZ| > r/2
B, r = 2.0, 0.5
tau_bad = 50*r**4/(128*B**5); eps = 8*B*tau_bad
best = 0.0
for _ in range(20000):
    D = rand_D(B, r)
    dZ, dW, det = solve_dZ(D, worst_E(D, eps))
    best = max(best, abs(dZ))
print(f"CONTROL (4.12) violated (tau=50x limit): max |dZ| = {best:.4f}  vs r/2 = {r/2}  -> exceeds: {best > r/2}")
# (b) violate (4.14): D's almost collide; exact solution with |dZ| = r and tiny E_j
B, r = 2.0, 0.5
Dc = [1.0, 1.0 + 1e-4, 1.0 + 2e-4j]
dZ = r
# choose dW minimising max|E_j| (approximately) : make E_1 = 0
dW = -(dZ/Dc[0])/(Dc[0] + dZ)
E = [dZ/d + d*dW + dZ*dW for d in Dc]
print(f"CONTROL (4.14) violated (|D_j-D_l|~1e-4): |dZ| = {dZ}, max|E_j| = {max(abs(e) for e in E):.3e}"
      f" -> an |E|<=8B*tau configuration with |dZ|>=r exists for tau = {max(abs(e) for e in E)/(8*B):.2e}"
      f" < r^4/(128B^5) = {r**4/(128*B**5):.2e}: {max(abs(e) for e in E)/(8*B) < r**4/(128*B**5)}")
