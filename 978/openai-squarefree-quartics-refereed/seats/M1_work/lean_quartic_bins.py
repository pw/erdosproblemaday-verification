# Recompute the Lean quartic bins (QuarticComponents.lean) and compare with the paper's certificate.
from fractions import Fraction as F
rows = []
for j in range(100):
    A = 101 + j; B = 200 - 2*j
    U = F(A, 400); V = F(B, 400)
    etaL, etaH = 1 + F(j, 100), 1 + F(j+1, 100)
    assert U == etaH/4 and V == 1 - etaL/2
    num = (lambda h: (206 if h <= 2 else 200 if h == 3 else 191)) if j < 60 else \
          (lambda h: 252 if h == 1 else 206 if h == 2 else 175)
    env = {h: F(num(h), 1000) for h in range(1, 6)}
    # thresholds as encoded by the Lean `decide` lemmas
    d5 = float((U**4*V**4/(2*U+V)**3)**F(1,1)) ** (1/5)
    d4 = float(U**4*V**4/(min(U,V)*(2*U+V)**3)) ** (1/4)
    d3 = float(U**3*V**3/(min(U,V)*(2*U+V)**2)) ** (1/3)
    d2a = float(U**2*V**2/(min(2*U,V)*(2*U+V))) ** 0.5
    d2p = float(U*V**2/(V+4*U)) ** 0.5
    d1 = float(max(U/2, min(U, V/3)))
    ok = (d5 <= env[5] and d4 <= env[4] and d3 <= env[3] and max(d2a, d2p) <= env[2] and d1 <= env[1])
    S = sum(env.values())
    rows.append((j, float(etaL), float(etaH), float(U), float(V), round(d5,4), round(d4,4), round(d3,4), round(d2a,4), round(d2p,4), round(d1,4), float(S), ok))
bad = [r for r in rows if not r[-1]]
print("bins:", len(rows), "envelope violations:", len(bad))
print("max envelope sum:", max(r[11] for r in rows), " (Lean asserts sum + 1/1000 <= 997/1000)")
for r in rows[:2] + rows[58:62] + rows[-2:]:
    print(r)
