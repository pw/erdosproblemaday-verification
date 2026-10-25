# Lemma 4.3 grid mismatch bound and Lemma 4.5 archimedean inconsistency bound (same fractional shift at every level).
import random, math, cmath
random.seed(45)
SQ2 = math.sqrt(2)
def cell(z, side, phi):
    return (math.floor(z.real/side - phi[0]), math.floor(z.imag/side - phi[1]))

# Lemma 4.3: P(different cells) <= min(1, sqrt2 * a / side); exact value 1-(1-|dx|/l)+(1-|dy|/l)+
worst = 0.0
for _ in range(2000):
    a = 10**random.uniform(-2, 1); th = random.uniform(0, 2*math.pi); side = 1.0
    d = cmath.rect(a, th)
    exact = 1 - max(0, 1 - abs(d.real)/side)*max(0, 1 - abs(d.imag)/side)
    worst = max(worst, exact/min(1, SQ2*a/side))
print(f"L4.3: max exact P(diff cell)/min(1,sqrt2 a e^-s) = {worst:.4f} (<=1 required)")
# integral over s>=0 of min(1, sqrt2 a e^-s) vs C(1+log+ a) with C = 1+log sqrt2
for a in (0.01, 0.5, 1/SQ2, 1.0, 10.0, 1e6):
    I = SQ2*a if SQ2*a <= 1 else 1 + math.log(SQ2*a)
    print(f"  a={a:g}: int = {I:.4f} <= (1+log sqrt2)(1+log+ a) = {(1+math.log(SQ2))*(1+max(0,math.log(a))):.4f}")
# point-pair side: log+ a <= int_0^inf 1{a > sqrt2 e^s} ds + log sqrt2  (equality for a >= sqrt2)
for a in (0.3, 1.0, SQ2, 5.0, 1e5):
    lhs = max(0, math.log(a)); rhs = max(0, math.log(a/SQ2)) + math.log(SQ2)
    print(f"  point pair a={a:g}: log+a={lhs:.4f} <= {rhs:.4f}: {lhs <= rhs + 1e-12}")

# Lemma 4.5 at infinity. Edge: z-jump delta, w-jump 1/delta ; n_e = -log|delta|.
def inconsistent(zq, wq, delta, s, phiA, phiB):
    zp, wp = zq + delta, wq + 1/delta
    Aagree = cell(zp, math.exp(-s), phiA) == cell(zq, math.exp(-s), phiA)
    Bagree = cell(wp, math.exp(s), phiB) == cell(wq, math.exp(s), phiB)
    n = -math.log(abs(delta))
    if n > s:  return not (Aagree and not Bagree)
    else:      return not (Bagree and not Aagree)
viol = 0; tot = 0; Iacc = 0.0; ntr = 300
grid = [x/20 for x in range(-200, 201)]  # s in [-10,10], ds = 0.05
for tr in range(ntr):
    n = random.uniform(-3, 3); delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi))
    zq = complex(random.uniform(-50, 50), random.uniform(-50, 50)); wq = complex(random.uniform(-50, 50), random.uniform(-50, 50))
    phiA = (random.random(), random.random()); phiB = (random.random(), random.random())   # ONE shift per grid, all levels
    for s in grid:
        tot += 1
        Iacc += inconsistent(zq, wq, delta, s, phiA, phiB) * 0.05
I_avg = Iacc/ntr
# pointwise bound check: average over shifts at fixed (delta, s)
worst = 0.0
for _ in range(60):
    n = random.uniform(-2, 2); delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi)); s = n + random.uniform(-3, 3)
    m = sum(inconsistent(0j, 0j, delta, s, (random.random(), random.random()), (random.random(), random.random())) for _ in range(3000))/3000
    b = (1 if abs(s-n) <= math.log(SQ2) else 0) + SQ2*math.exp(-abs(s-n))
    worst = max(worst, m - b)
print(f"L4.5: mean over edges/shifts of int_R inconsistency = {I_avg:.3f} <= log2 + 2sqrt2 = {math.log(2)+2*SQ2:.3f}; "
      f"max(MC P(incons) - pointwise bound) = {worst:.4f} (<= ~0 up to MC noise)")
# CONTROL: replace the w-jump 1/delta by delta^2 (parabola-type 'unit circle' Y = X^2): consistency integral is NOT bounded
def inconsistent_par(zq, wq, delta, s, phiA, phiB):
    zp, wp = zq + delta, wq + delta**2
    Aagree = cell(zp, math.exp(-s), phiA) == cell(zq, math.exp(-s), phiA)
    Bagree = cell(wp, math.exp(s), phiB) == cell(wq, math.exp(s), phiB)
    n = -math.log(abs(delta))
    return (not (Aagree and not Bagree)) if n > s else (not (Bagree and not Aagree))
Iacc = 0.0; big = [x/20 for x in range(-400, 401)]
for tr in range(100):
    n = random.uniform(-3, 3); delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi))
    phiA = (random.random(), random.random()); phiB = (random.random(), random.random())
    Iacc += sum(inconsistent_par(0j, 0j, delta, s, phiA, phiB) for s in big)*0.05
print(f"CONTROL (jumps d, d^2 instead of d, 1/d): mean int over s in [-20,20] of inconsistency = {Iacc/100:.2f} (per-edge value grows linearly in |n_e|, see parabola_ctrl.py; random n_e in [-3,3] here)")
