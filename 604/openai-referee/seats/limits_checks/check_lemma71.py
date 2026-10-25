# Finite illustration of Lemma 7.1 / (7.7) / (7.8) of the OpenAI #604 preprint.
# J_w(X) = \int w(Pr(X >= u)) du, computed EXACTLY for the empirical law of a sample:
# for u in (X_(i), X_(i+1)], Pr(X>=u) = (N-i)/N  (0-indexed sorted, i = 1..N-1 gaps).
import numpy as np
rng = np.random.default_rng(604)

def w_l(t, l):
    # continuous, compactly supported in (0,1), =1 on [1/l, 1-1/l]
    lo, hi = 1.0/(2*l), 1.0/l
    t = np.asarray(t, float)
    out = np.zeros_like(t)
    up = (t > lo) & (t < hi); out[up] = (t[up]-lo)/(hi-lo)
    mid = (t >= hi) & (t <= 1-hi); out[mid] = 1.0
    dn = (t > 1-hi) & (t < 1-lo); out[dn] = ((1-lo)-t[dn])/(hi-lo)
    return out

def J(x, l, U=None):
    """exact J_{w_l} of the empirical law of finite sample x; +inf entries allowed,
    then the u-integral is truncated to [-U, U] (needs U)."""
    x = np.sort(np.asarray(x, float)); N = len(x)
    fin = np.isfinite(x)
    if not fin.all():
        assert U is not None
        x = np.where(np.isposinf(x), U, x); x = np.clip(x, -U, U)
    gaps = np.diff(x)                         # length of (x_(i), x_(i+1)]
    tail = (N - np.arange(1, N)) / N          # Pr(X >= u) on that gap
    return float(np.sum(w_l(tail, l) * gaps))

def unif_disk(N, c=0j, rad=1.0):
    r = rad*np.sqrt(rng.random(N)); th = 2*np.pi*rng.random(N)
    return c + r*np.exp(1j*th)

N = 400_000; l = 10
Z = unif_disk(N)                                   # beta_1 = uniform on unit disk (nonatomic)
ap = 0.3+0.2j                                      # a' in supp beta_1

print("== (A) algebra: -log|Phi(z)-b'| = log(|z-a|/|z-a'|) - log|b'-b| ==")
a, b, bp = -0.4+0.1j, 2.0-1.0j, 1.5+0.5j
t = (ap-a)*(bp-b)
Phi = lambda z: b + t/(z-a)
lhs = -np.log(np.abs(Phi(Z)-bp))
rhs = np.log(np.abs(Z-a)/np.abs(Z-ap)) - np.log(abs(bp-b))
print("  max |lhs-rhs| =", np.max(np.abs(lhs-rhs)))
wrong = np.log(np.abs(Z-a)*np.abs(Z-ap)) - np.log(abs(bp-b))   # CONTROL: product instead of ratio
print("  CONTROL (product kernel) max |lhs-wrong| =", np.max(np.abs(lhs-wrong)))

print("== (B) (7.8) as an identity of J-values for one Mobius map (beta_2 := Phi_* beta_1) ==")
W = Phi(Z)
J_left = J(np.log(np.abs(Z-a)/np.abs(Z-ap)), l)
J_right = J(-np.log(np.abs(W-bp)), l)
print("  J_left =", J_left, " J_right =", J_right, " diff =", J_left-J_right)
J_ctrl = J(np.log(np.abs(Z-a)*np.abs(Z-ap)), l)
print("  CONTROL J(product kernel) =", J_ctrl, " (differs from J_right by", J_ctrl-J_right, ")")

print("== (C) Lemma 7.1 mechanism: LHS of (7.8) -> 0 as a_k -> a' (beta_1 nonatomic, a' in supp) ==")
for k in range(0, 13, 2):
    ak = ap + 0.5*2.0**(-k)*np.exp(1j*0.7*k)
    X = np.log(np.abs(Z-ak)/np.abs(Z-ap))
    print(f"  k={k:2d} |a_k-a'|={abs(ak-ap):.2e}  J_l(X_k)={J(X,l):.5f}")
beta2 = unif_disk(N, c=1.0+0j, rad=2.0)            # some nonatomic beta_2, b' in its support
bp2 = 1.5+0.5j
print("  RHS of (7.8) for beta_2=Unif(disk(1,2)), b'=1.5+0.5i: J_l(-log|W-b'|) =", J(-np.log(np.abs(beta2-bp2)), l))

print("== (D) CONTROL 1: beta_1 with an ATOM at a' (mass 0.3): X_k = +inf on the atom ==")
Za = Z.copy(); Za[:int(0.3*N)] = ap               # atom at a'
with np.errstate(divide='ignore'):
    for k in (0, 6, 12):
        ak = ap + 0.5*2.0**(-k)*np.exp(1j*0.7*k)
        X = np.log(np.abs(Za-ak)) - np.log(np.abs(Za-ap))   # +inf on the atom
        print(f"  k={k:2d}  J truncated to |u|<=U:", {U: round(J(X, l, U=U),3) for U in (10, 100, 1000)})
print("  (grows linearly in U: J = +inf, does NOT tend to 0)")

print("== (E) CONTROL 2: near-atom (mass 0.3 uniform on disk radius 1e-9 about a') ==")
Zn = Z.copy(); Zn[:int(0.3*N)] = unif_disk(int(0.3*N), c=ap, rad=1e-9)
for k in range(0, 25, 4):
    ak = ap + 0.5*2.0**(-k)*np.exp(1j*0.7*k)
    X = np.log(np.abs(Zn-ak)/np.abs(Zn-ap))
    print(f"  k={k:2d} |a_k-a'|={abs(ak-ap):.2e}  J_l(X_k)={J(X,l):.4f}")

print("== (F) CONTROL 3: a' NOT in supp beta_1 (a'=2.0, beta_1=Unif(unit disk)) ==")
ap_out = 2.0+0j
grid = [x+1j*y for x in np.linspace(-1,1,21) for y in np.linspace(-1,1,21) if x*x+y*y<=1]
vals = [J(np.log(np.abs(Z[:100000]-g)/np.abs(Z[:100000]-ap_out)), l) for g in grid]
print("  min over a in supp of J_l(log|Z-a|/|Z-a'|) =", min(vals), " (bounded away from 0: no a_k -> a')")
