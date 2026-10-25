# Check 2: Lemma 5.5 (binary-centre separation) -- exact representation y+e^{it} = x+e^{i a+}+e^{i a-},
# the expansion (5.9) of F = a+ o a-^{-1} - 2kappa, and the six-map bounds (5.10).
# Controls: (i) flip the sign of the arccos in a+- (representation must fail);
#           (ii) a WRONG leading term t+(2d/sqrt3)cos(t-pi/6) (residual/d^2 must blow up).
import numpy as np
kap = np.pi/3
N = 200001
t = np.linspace(-4*np.pi, 4*np.pi, 4*N)          # wide range so every F(u - j*kappa) is evaluated by genuine interpolation
def lifts(d, t, sgn=1.0):
    w = d + np.exp(1j*t)
    Th = t + np.imag(np.log(1 + d*np.exp(-1j*t)))
    ac = np.arccos(np.abs(w)/2)
    return Th + sgn*ac, Th - sgn*ac, w
for d in (0.3, 0.1):
    ap, am, w = lifts(d, t)
    res = np.max(np.abs(np.exp(1j*ap) + np.exp(1j*am) - w))
    apb, amb, _ = lifts(d, t, sgn=-1.0); wrongsum = np.exp(1j*apb) + np.exp(1j*amb) - w   # same pair swapped: still fine
    # real control: use arcsin instead of arccos
    Th = t + np.imag(np.log(1 + d*np.exp(-1j*t))); acw = np.arcsin(np.abs(w)/2)
    resc = np.max(np.abs(np.exp(1j*(Th+acw)) + np.exp(1j*(Th-acw)) - w))
    nonpar = np.min(np.abs(np.sin(ap-am)))
    print(f"d={d}: max|e^ia+ + e^ia- - (d+e^it)| = {res:.1e}; CONTROL(arcsin) = {resc:.2f}; min|sin(a+ - a-)| = {nonpar:.3f}; "
          f"min/max a+' = {np.min(np.gradient(ap,t)):.3f}/{np.max(np.gradient(ap,t)):.3f}")

def sixmaps(d):
    ap, am, _ = lifts(d, t)
    # invert a- by monotone interpolation; evaluate F on s in [0, 2pi]
    s = np.linspace(0, 2*np.pi, 20001)
    am_inv = lambda u: np.interp(u, am, t)
    ap_f = lambda u: np.interp(u, t, ap)
    F = lambda u: ap_f(am_inv(u)) - 2*kap
    Fj = [ (lambda u, j=j: j*kap + F(u - j*kap)) for j in range(6) ]
    return s, F, Fj
print("\n d      max|F-t-(2d/v3)sin(t-pi/6)|/d^2   CONTROL cos-version/d^2   min_t max_j (Fj-t)/d   min_t max_j (Fj'-1)/d   max_j|Fj-t|/d  max_j|Fj'-1|/d  max_j|Fj''|/d")
for d in (0.08, 0.04, 0.02, 0.01, 0.005):
    s, F, Fj = sixmaps(d)
    lead = s + 2*d/np.sqrt(3)*np.sin(s - np.pi/6)
    r1 = np.max(np.abs(F(s) - lead))/d**2
    r2 = np.max(np.abs(F(s) - (s + 2*d/np.sqrt(3)*np.cos(s - np.pi/6))))/d**2
    V = np.stack([Fj[j](s) for j in range(6)])
    D1 = np.gradient(V, s, axis=1); D2 = np.gradient(D1, s, axis=1)
    disp = np.min(np.max(V - s, axis=0))/d
    der  = np.min(np.max(D1 - 1, axis=0))/d
    print(f"{d:<6} {r1:>14.4f} {r2:>30.2f} {disp:>22.4f} {der:>22.4f} {np.max(np.abs(V-s))/d:>16.4f} {np.max(np.abs(D1-1))/d:>14.4f} {np.max(np.abs(D2[:,5:-5]))/d:>14.4f}")
print("theory: leading coefficient 2/sqrt3 =", 2/np.sqrt(3), "; six-phase max of sine >= sqrt3/2 gives max_j(Fj-t)/d -> 1, max_j(Fj'-1)/d -> 1")
