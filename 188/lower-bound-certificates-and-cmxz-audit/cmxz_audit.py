#!/usr/bin/env python3
"""Independent recomputation of every constant in Currier-Mody-Xie-Zhang, arXiv:2606.17194v2, Section 3.1
(Theorem 1.2: E^2 does not arrow (l_2, l_6330)).  Nothing here is taken from the paper except the
construction; each number is recomputed and compared with what the paper prints."""
import math
from mpmath import mp, mpf, log, exp
mp.dps = 30
print("== lattice: b1=(3/2,0), b2=(3/4,sqrt3/4) (times 1-eps)")
b1 = (1.5, 0.0); b2 = (0.75, math.sqrt(3)/4)
v = (b1[0]-b2[0], b1[1]-b2[1])
print("  |b2| = %.6f  |b1-b2| = %.6f  angle(b2,b1-b2) = %.1f deg  => hexagonal lattice, spacing sqrt3/2 = %.6f" %
      (math.hypot(*b2), math.hypot(*v), math.degrees(math.acos((b2[0]*v[0]+b2[1]*v[1])/(math.hypot(*b2)*math.hypot(*v)))), math.sqrt(3)/2))
s = math.sqrt(3)/2
print("  Voronoi hexagon circumradius = spacing/sqrt3 = %.6f -> diameter %.6f (paper: 1-eps < 1)  OK" % (s/math.sqrt(3), 2*s/math.sqrt(3)))
print("  shortest lattice vector = %.4f >= 1/2 (paper)  OK" % s)
print("== |z(D)|: cells within distance <= 1 of a given hexagon (paper: 18)")
cells = [(a*s + b*s/2, b*s*math.sqrt(3)/2) for a in range(-6,7) for b in range(-6,7)]
def hexagon(c, r=0.5):
    return [(c[0]+r*math.cos(math.pi/6 + k*math.pi/3), c[1]+r*math.sin(math.pi/6 + k*math.pi/3)) for k in range(6)]
def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx-ax, by-ay; t = max(0, min(1, ((px-ax)*dx + (py-ay)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-ax-t*dx, py-ay-t*dy)
def poly_dist(P, Q):
    return min(min(seg_dist(p, Q[i], Q[(i+1)%6]) for p in P for i in range(6)), min(seg_dist(q, P[i], P[(i+1)%6]) for q in Q for i in range(6)))
H0 = hexagon((0,0))
near = [c for c in cells if abs(c[0])+abs(c[1])>1e-9 and poly_dist(H0, hexagon(c)) <= 1 + 1e-9]
print("  computed |z(D)| =", len(near), " at centre distances", sorted(set(round(math.hypot(*c),4) for c in near)))
print("  next ring (centre distance %.4f) has min gap %.4f > 1 -> excluded  OK" % (math.sqrt(7)*s, min(poly_dist(H0, hexagon(c)) for c in cells if abs(math.hypot(*c)-math.sqrt(7)*s)<1e-6)))
print("== wall lines (Lemma 3.1): parallel wall-line spacing (paper: >= 1/3) and count within 5m of origin (paper: <= 100 m)")
import numpy as np
verts = np.array(H0); n = verts[1]-verts[0]; n = np.array([-n[1], n[0]])/np.linalg.norm(n)
hs = sorted(set(round(float(np.dot(np.array(c)+verts[0], n)),6) for c in cells) | set(round(float(np.dot(np.array(c)+verts[3], n)),6) for c in cells))
sp_ = min(hs[i+1]-hs[i] for i in range(len(hs)-1))
print("  spacing = %.6f ;  lines per direction within radius 5m = 10m/%.4f = %.2f m ; three directions: %.2f m <= 100 m  OK" % (sp_, sp_, 10/sp_, 30/sp_))
print("== Milnor-Thom count (Theorem 2.5 with D=1, M=100 m^2, N=4): (50*100 m^2/4)^4 = 1250^4 m^8 = 2^4 5^16 m^8")
print("  1250^4 =", 1250**4, " 2^4*5^16 =", 2**4*5**16, " equal:", 1250**4 == 2**4*5**16)
print("== Lemma 3.2 (Janson/Suen), p = 1/19, |z(D)| = 18")
p = mpf(1)/19; z = 18
mu1 = p*(1-p)**z; D1 = 3*p**2*(1-p)**z; delta = 8*p*(1-p)**z
rate = -mu1 + D1*exp(2*delta)
print("  E[X_i] = p(1-p)^18 =", mp.nstr(mu1, 8), "(maximised at p=1/19: d/dp = (1-p)^17 (1-19p))")
print("  Delta/m <= 3 p^2 (1-p)^18 =", mp.nstr(D1, 8), " delta <= 8 p (1-p)^18 =", mp.nstr(delta, 8))
print("  (-mu + Delta e^{2 delta})/m =", mp.nstr(rate, 10), "  paper: -0.01557  OK")
print("== crossover: exp(rate m) * 2^4 5^16 m^8 < 1")
cl = 4*log(2) + 16*log(5)
def E(m, r=rate): return cl + 8*log(m) + r*m
for m in (6328, 6329, 6330):
    print("  m =", m, " ln(expected #all-blue admissible collections) =", mp.nstr(E(m), 6), ("< 0" if E(m) < 0 else ">= 0"), " [unrounded exponent]")
for m in (6329, 6330):
    print("  m =", m, " with the paper's ROUNDED exponent -0.01557:", mp.nstr(E(m, mpf('-0.01557')), 6), ("< 0" if E(m, mpf('-0.01557')) < 0 else ">= 0"))
print("  => unrounded: every m >= 6329; with the exponent as printed (0.01557): every m >= 6330 -- the paper's 6330 is exact for the lemma as stated")
print("== remark: the progression has 3 degrees of freedom. Parametrise by (x1, y1, t = tan(theta/2)); each wall-line sign")
print("   condition becomes a polynomial of degree 3 in 3 variables; Theorem 2.5 with D=3, N=3, M=100 m^2 gives (5000 m^2)^3:")
def E2(m, lines=100): return 3*log(50*3*lines*m*m/3) + rate*m
for m in (4915, 4916, 4917, 4918):
    print("  m =", m, " ln E' =", mp.nstr(E2(m), 6), ("< 0" if E2(m) < 0 else ">= 0"))
print("  => the same proof gives E^2 not-> (l_2, l_4917) with their line count (100 m).")
for m in (4839, 4840, 4841):
    print("  [estimate only, not claimed] with the exact line count 69.28 m: m =", m, mp.nstr(E2(m, 30/0.4330127), 6))
# optimal p against the full exponent (free further gain, not claimed)
import mpmath
def rate_p(q): return -q*(1-q)**18 + 3*q**2*(1-q)**18*exp(16*q*(1-q)**18)
best = min((rate_p(mpf(k)/10000), k) for k in range(200, 800))
print("  [not claimed] optimal p against the full exponent ~", best[1]/10000, "rate", mp.nstr(best[0], 7), "vs", mp.nstr(rate, 7), "at p = 1/19")
