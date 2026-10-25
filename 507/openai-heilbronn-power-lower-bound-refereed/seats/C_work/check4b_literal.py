#!/usr/bin/env python3
"""Check 4 literal small case from the brief: H = 1, q = 2003 (first prime >= 2000H^2), w = floor(q/1000) = 2.
Every shift b in F_q^3 is enumerated through its intersection count (exact maximum of |S| over all q^3 shifts),
then Lemma 5.2's conclusions are checked for one allowed a and random G."""
import numpy as np, random
from check4_cap import gamma_points, collinear_lines, count_A1, random_gl, relation_check, nonsquare
q, H = 2003, 1
w = q // (1000 * H * H)
nu = nonsquare(q)
G = gamma_points(q, nu)                      # q^2 points
box = np.array([(x, y, z) for x in range(w) for y in range(w) for z in range(w)], dtype=np.int64)
# shifts b with p in b + Gamma  <=>  b = p - gamma ; count multiplicities over all p in box
keys = []
for p in box:
    s = (p - G) % q
    keys.append(s[:, 0] * q * q + s[:, 1] * q + s[:, 2])
keys = np.concatenate(keys)
u, c = np.unique(keys, return_counts=True)
print(f"q={q} w={w}: exact average |S| over all q^3 shifts = {c.sum()/q**3:.6f} (= w^3/q = {w**3/q:.6f}); "
      f"max |S| = {c.max()}; #shifts with |S|>=1: {len(u)}")
best = u[c.argmax()]; b = np.array([best // (q*q), (best // q) % q, best % q])
S = np.array([p for p in box if any(((p - b) % q == g).all() for g in G[(G[:,0] == (p[0]-b[0]) % q) & (G[:,1] == (p[1]-b[1]) % q)])])
print(f"   S for the best shift: {S.tolist()}  lines>=3: {collinear_lines(S, q)[0] if len(S)>=3 else 0}")
okA = count_A1(q, H, w)
print(f"   |A|/q^3 = {okA.mean():.5f} >= 1/2: {okA.mean() >= 0.5}")
rng = random.Random(1)
a1 = rng.randrange(q)
while not okA[a1]: a1 = rng.randrange(q)
a = np.array([a1, rng.randrange(q), rng.randrange(q)]); Gm = random_gl(q, rng)
V = ((S + a) % q) @ Gm.T % q
print(f"   V: 0 in V: {any((v==0).all() for v in V)}; short-relation violations: {len(relation_check(V, q, H))}")
