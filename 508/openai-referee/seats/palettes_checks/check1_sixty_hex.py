# Check 1: sixty-degree exclusion (Cor 5.4) geometry + empirical palettes of hexagonal colourings,
# and the constants of Lemma 6.4.  Control: a non-60-degree rotation and an IMPROPER hexagon colouring.
import numpy as np, sys
from fractions import Fraction
rng = np.random.default_rng(1)

def rot(th): return np.exp(1j*th)
# (a) identity used in Cor 5.4:  f = R f + R^{-1} f, |Rf - f| = 1, endpoints nonparallel
for name, th in [("kappa=pi/3 (paper)", np.pi/3), ("CONTROL kappa=50deg", np.deg2rad(50))]:
    f = rot(rng.uniform(0, 2*np.pi, 1000))
    res = np.max(np.abs(rot(th)*f + rot(-th)*f - f))
    unit = np.max(np.abs(np.abs(rot(th)*f - f) - 1))
    nonpar = abs(np.sin(2*th))          # sin of angle between Rf and R^{-1}f
    print(f"{name}: max|Rf+R^-1f-f|={res:.2e}  max||Rf-f|-1|={unit:.2e}  |sin(angle(Rf,R^-1f))|={nonpar:.3f}")

# (b) empirical palettes for the Hadwiger hexagon colouring: Voronoi cells of the triangular lattice
#     with spacing sqrt(3) r, colour = (m + 2n) mod 7  (Z[w]/(2-w) = Z/7, w = e^{2 pi i/3}).
w = np.exp(2j*np.pi/3)
def colour(z, r):
    a = np.sqrt(3)*r
    # lattice coordinates z = a(m + n w)
    n = (z.imag/a)/np.sin(2*np.pi/3); m = z.real/a - n*np.cos(2*np.pi/3)
    m0, n0 = np.floor(m), np.floor(n)
    best = None; bestd = None
    for dm in (-1, 0, 1, 2):
        for dn in (-1, 0, 1, 2):
            mm, nn = m0+dm, n0+dn
            d = np.abs(z - a*(mm + nn*w))
            if best is None:
                best = (mm + 2*nn) % 7; bestd = d
            else:
                upd = d < bestd
                best = np.where(upd, (mm + 2*nn) % 7, best); bestd = np.where(upd, d, bestd)
    return best.astype(int)

def palettes(x, angles, r, eps, K=12):
    # colours of points within eps of x+e^{i t}: sample centre + K points on circles eps, eps/2
    pts = [x + rot(angles)]
    for rad in (eps, eps/2):
        for k in range(K):
            pts.append(x + rot(angles) + rad*rot(2*np.pi*k/K + 0.1))
    cols = np.stack([colour(p, r) for p in pts])          # (samples, angles)
    M = np.zeros((7, len(angles)), bool)
    for c in range(7): M[c] = (cols == c).any(axis=0)
    return M

T = 4096
ang = 2*np.pi*np.arange(T)/T
shift = T//6                       # R = rotation by 60 deg = T/6 grid steps
for r, label in [(0.4, "proper  r=2/5"), (0.6, "CONTROL r=0.6 (hexagon diameter 1.2>1, improper)")]:
    for eps in (1e-2, 1e-3):
        viol = 0; big = 0; tot = 0
        for _ in range(40):
            x = complex(*rng.uniform(-5, 5, 2))
            M = palettes(x, ang, r, eps)
            MR = np.roll(M, -shift, axis=1)             # palette at R f
            viol += (M & MR).any(axis=0).sum()
            big  += (M.sum(axis=0) >= 3).sum()
            tot += T
        print(f"{label} eps={eps:g}: frac f with P(f)∩P(Rf)≠∅ = {viol/tot:.5f};  frac |P(f)|>=3 = {big/tot:.5f}")

# (c) Lemma 6.4 constants, exact
cosg = Fraction(5, 6)
print("Lemma 6.4: 1-2*sin^2(g/2) with sin(g/2)=1/(2sqrt3):", 1 - 2*Fraction(1, 12), "== 5/6:", 1-2*Fraction(1,12) == cosg)
print("|1-e^{ig}|^2 = 2-2cos g =", 2-2*cosg, "(need 1/3);  triangle side^2 = 3*(1/3) =", 3*(2-2*cosg))
print("2cos g =", 2*cosg, "not an integer -> g/pi irrational (Niven-type argument)")
g = np.arccos(5/6)
for t in rng.uniform(0, 2*np.pi, 3):
    z = [rot(t + 2*j*np.pi/3)*(1 - rot(g)) for j in range(3)]
    print("  side lengths:", [round(abs(z[i]-z[(i+1)%3]), 12) for i in range(3)], " |sin(pi+g)|=", round(abs(np.sin(np.pi+g)), 4))
