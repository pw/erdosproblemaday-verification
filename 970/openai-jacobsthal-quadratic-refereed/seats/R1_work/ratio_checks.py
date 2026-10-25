# sanity: a/c0, c/c0 in a compact subinterval of (0,1) (Lemma 4.1 (4.3)); phi_e, phi_o positive & nonincreasing (Lemma 4.2);
# Dickman ratio bounds (4.4).
import numpy as np
from sieve_fns import build, A
s, hs, f, F, rho = build(40, 20000)
N = int(round(1/hs)); a = 1-f; c = F-1
i1 = N; c0 = np.full_like(s, np.nan); c0[i1:] = A*rho[:len(s)-i1]/s[i1:]
sel = (s >= 1) & (s <= 8)
ra, rc = a[sel]/c0[sel], c[sel]/c0[sel]
print(f"a/c0 in [{ra.min():.4f},{ra.max():.4f}], c/c0 in [{rc.min():.4f},{rc.max():.4f}] on s in [1,8]")
pe = s*(a + np.interp(s-1, s, c)); po = s*(c + np.where(s-1 <= 2, 1.0, np.interp(np.maximum(s-1,0), s, a)))
se = (s >= 2) & (s <= 8); so = (s >= 1) & (s <= 8)
print("phi_e min", pe[se].min(), "max increase step", np.max(np.diff(pe[se])), "| phi_o min", po[so].min(), "max increase step", np.max(np.diff(po[so])))
u = s[(s >= 2) & (s <= 8)]; r = np.interp(u, s, rho)/np.interp(u-1, s, rho)
print("rho(u)/rho(u-1) * u in", (r*u).min(), (r*u).max(), " ; *4u^2 min", (r*4*u*u).min())
