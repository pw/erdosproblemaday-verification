#!/usr/bin/env python3
"""Test (B) illustration on a REAL proper colouring: the standard hexagonal 7-colouring (side s=0.45).
At a triple point x the three hexagon-boundary segments are compact connected exclusion continua (Prop 7.1's data,
with k=7). Check (i) properness by sampling, (ii) Lemma 8.1's one-sided strip conclusion on this colouring, and
(iii) what replaces the binary outsider state s of Sec. 8.4 when there are four outsiders instead of two."""
import numpy as np, sys
s = 0.45; SQ3 = np.sqrt(3)
def colour(p):
    x, y = p[..., 0], p[..., 1]
    q = (SQ3/3*x - y/3)/s; r = (2/3*y)/s                     # pointy-top axial coordinates
    cx, cz = q, r; cy = -cx - cz
    rx, ry, rz = np.round(cx), np.round(cy), np.round(cz)
    dx, dy, dz = abs(rx-cx), abs(ry-cy), abs(rz-cz)
    m1 = (dx > dy) & (dx > dz); m2 = (~m1) & (dy > dz)
    rx = np.where(m1, -ry-rz, rx); rz = np.where(~m1 & ~m2, -rx-ry, rz)
    return ((rx + 3*rz) % 7).astype(int)
rng = np.random.default_rng(7)
fails = []
# (i) properness on random unit pairs (skip pairs within 1e-6 of a boundary by resampling noise: measure-zero)
P = rng.uniform(-20, 20, (400000, 2)); th = rng.uniform(0, 2*np.pi, 400000)
Qp = P + np.stack([np.cos(th), np.sin(th)], 1)
mono = np.sum(colour(P) == colour(Qp))
print(f"(i) monochromatic unit pairs among 400000 random pairs: {mono}")
if mono: fails.append("hex colouring not proper")
# control: side s=0.55 (diameter 1.1 > 1) must produce monochromatic unit pairs
s_save = s; s = 0.55; mono_bad = np.sum(colour(P) == colour(Qp)); s = s_save
print(f"    control s=0.55 (hexagon diameter > 1): monochromatic unit pairs = {mono_bad} (must be > 0)")
if mono_bad == 0: fails.append("control failed")
# (ii) triple point x = top vertex of hexagon (0,0): x = (0, s); edge directions from x: 90, 210, 330 degrees
x = np.array([0.0, s]); vdeg = [90.0, 210.0, 330.0]
eps = 1e-3
def side_colours(vd):
    v = np.array([np.cos(np.radians(vd)), np.sin(np.radians(vd))]); n = np.array([-v[1], v[0]])
    p = x + 0.1*v
    return int(colour(p + eps*n)), int(colour(p - eps*n))
edges = [side_colours(vd) for vd in vdeg]
tri = sorted({c for e in edges for c in e})
print(f"(ii) edges (label pairs) at x: {edges}; triangle labels {tri}; outsiders {sorted(set(range(7)) - set(tri))}")
B = sorted({(vd + 90) % 360 for vd in vdeg} | {(vd - 90) % 360 for vd in vdeg})
viol = 0; outer_cols = set(); inner_cols = set()
for ed in np.arange(0.25, 360, 0.5):
    if min(abs(((ed - b + 180) % 360) - 180) for b in B) < 1.0: continue
    e = np.array([np.cos(np.radians(ed)), np.sin(np.radians(ed))])
    sg = [np.sign(e @ np.array([np.cos(np.radians(vd)), np.sin(np.radians(vd))])) for vd in vdeg]
    O = set(range(7)) - {c for (pair, g) in zip(edges, sg) if g > 0 for c in pair}
    I = set(range(7)) - {c for (pair, g) in zip(edges, sg) if g < 0 for c in pair}
    for rho in (1.0005, 1.002, 1.005):
        c = int(colour(x + rho*e)); outer_cols.add(c); viol += c not in O
    for rho in (0.995, 0.998, 0.9995):
        c = int(colour(x + rho*e)); inner_cols.add(c); viol += c not in I
print(f"    Lemma 8.1 strip conclusion on this colouring: violations = {viol} (expect 0)")
if viol: fails.append("Lemma 8.1 conclusion violated on hex colouring")
print(f"(iii) colours met just outside / inside the unit circle about x: {sorted(outer_cols)} / {sorted(inner_cols)}")
print("     With k=7 the two-of-three-edges strip uses the FOUR outsiders, not two: the binary state s(e) of Sec. 8.4,")
print("     the two-colour alternation of Lemma 8.6, and the 3-label region of Lemma 8.8 all depend on k=5 (two outsiders).")
print("RESULT:", "OK" if not fails else fails)
sys.exit(1 if fails else 0)
