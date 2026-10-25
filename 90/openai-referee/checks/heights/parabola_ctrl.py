# CONTROL for Lemma 4.5: replace the reciprocal w-jump 1/d (Euclidean, zw=1) by d^2 (parabola Y=X^2, Valtr-type arc).
# With 1/d the per-edge inconsistency integral is O(1) uniformly in n_e; with d^2 it grows linearly in |n_e|.
import random, math, cmath
random.seed(7)
def cell(z, side, phi): return (math.floor(z.real/side - phi[0]), math.floor(z.imag/side - phi[1]))
def incons(delta, wjump, s, phiA, phiB):
    Aagree = cell(delta, math.exp(-s), phiA) == cell(0j, math.exp(-s), phiA)
    Bagree = cell(wjump, math.exp(s), phiB) == cell(0j, math.exp(s), phiB)
    n = -math.log(abs(delta))
    return (not (Aagree and not Bagree)) if n > s else (not (Bagree and not Aagree))
S = [x/20 for x in range(-1000, 1001)]
for n in (0.0, 1.0, 2.0, 4.0, 8.0, -4.0, -8.0):
    Ir, Ip = 0.0, 0.0
    for _ in range(40):
        delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi))
        phiA = (random.random(), random.random()); phiB = (random.random(), random.random())
        Ir += sum(incons(delta, 1/delta, s, phiA, phiB) for s in S)*0.05
        Ip += sum(incons(delta, delta**2, s, phiA, phiB) for s in S)*0.05
    print(f"n_e={n:+.0f}: int inconsistency  reciprocal(1/d)={Ir/40:.2f}   parabola(d^2)={Ip/40:.2f}")
