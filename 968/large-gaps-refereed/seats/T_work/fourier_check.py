# Seat T numeric 3: conventions of printed eq. (25) and the kernel/derivative formula (14) (end of printed 5.2);
# numeric 4: P_p(0), B_p(0), H_p(0) vs the local factor of S(H), by brute-force enumeration of allowed subsets.
import numpy as np, math, itertools, random

def psi1(v):  # smooth, compact support (-1,1); extension of F on the orthant
    out = np.zeros_like(v); m = np.abs(v) < 1
    out[m] = np.exp(-1.0 / (1 - v[m]**2)) * (1 + 0.3 * v[m])
    return out
def psi2(v):
    out = np.zeros_like(v); m = (v > -0.8) & (v < 0.9)
    t = (v[m] + 0.8) / 1.7
    out[m] = np.exp(-1.0 / (t * (1 - t))) * np.cos(2 * v[m])
    return out
vg = np.linspace(-1, 1, 40001); dv = vg[1] - vg[0]
ug = np.linspace(-80, 80, 3201); du = ug[1] - ug[0]
def Phi(psi):  # (2pi)^{-1} int e^{v} psi(v) e^{iuv} dv
    g = np.exp(vg) * psi(vg)
    return np.array([np.sum(g * np.exp(1j * u * vg)) * dv for u in ug]) / (2 * math.pi)
P1, P2 = Phi(psi1), Phi(psi2)
w = 1 + 1j * ug
print("inversion (25): F(v) vs int Phi(u) e^{-(1+iu)v} du")
for v0 in [0.0, 0.2, 0.5, 0.8]:
    rec = np.sum(P1 * np.exp(-w * v0)) * du
    print(f"  v={v0}: psi1={psi1(np.array([v0]))[0]:.10f}  rec={rec.real:.10f}{rec.imag:+.1e}i")
def dpsi(psi, y, h=1e-5):
    return (psi(y + h) - psi(y - h)) / (2 * h)
# singleton fibre: int Phi(u) w du  should equal (-1)dF(0) = -psi'(0)
s1 = np.sum(P1 * w) * du
print(f"singleton fibre: int Phi*w = {s1.real:.8f}{s1.imag:+.1e}i ; -psi1'(0) = {-dpsi(psi1, np.array([0.0]))[0]:.8f}")
# double fibre: int int Phi1 Phi2 w1 w2/(w1+w2) = int_0^inf psi1'(y) psi2'(y) dy
W1, W2 = np.meshgrid(w, w, indexing='ij')
K = W1 * W2 / (W1 + W2)
dbl = np.sum(np.outer(P1, P2) * K) * du * du
yg = np.linspace(0, 1, 20001)
rhs = np.sum(dpsi(psi1, yg) * dpsi(psi2, yg)) * (yg[1] - yg[0])
print(f"double fibre: int Phi1 Phi2 w1w2/(w1+w2) = {dbl.real:.8f}{dbl.imag:+.1e}i ; int_0^inf psi1' psi2' = {rhs:.8f}")

# numeric 4: local factors
def local_check(p, shifts, kappa_sizes, a0=None, trials=1):
    # coordinates: fibre i has kappa_sizes[i] coordinates, all with shift shifts[i]
    coords = [i for i, m in enumerate(kappa_sizes) for _ in range(m)]
    M = len(coords); delta = 0 if a0 is None else 1
    P0 = 1.0
    for r in range(1, M + 1):
        for S in itertools.combinations(range(M), r):
            res = {shifts[coords[g]] % p for g in S}
            if len(res) != 1:
                continue
            if delta and (next(iter(res)) - a0) % p == 0:
                continue
            P0 += (-1)**r / (p - delta)
    t = len(shifts)
    B0 = (1 - 1 / p)**t
    H = set(shifts) | ({a0} if delta else set())
    nu = len({x % p for x in H})
    loc = (1 - nu / p) * (1 - 1 / p)**(-len(H))
    return P0 / B0, loc
random.seed(1)
worst = 0
for _ in range(400):
    p = random.choice([2, 3, 5, 7])
    t = random.randint(1, 4)
    sh = random.sample(range(-20, 20), t + 1)
    a0 = sh[-1] if random.random() < 0.5 else None
    sizes = [random.randint(1, 3) for _ in range(t)]
    Hp, loc = local_check(p, sh[:t], sizes, a0)
    worst = max(worst, abs(Hp - loc))
print(f"H_p(0) vs local factor of S(H): max abs diff over 400 random patterns (p<=7, fibres<=3, marked/unmarked) = {worst:.2e}")
