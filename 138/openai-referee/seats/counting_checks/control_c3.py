"""Control C3 at a size where the misapplied bound is actually exceeded.
C3: 10 generic planes in R^3 (exact FM count incl. zero signs) vs the e=2 bound 9(s+1)^2.
"""
import sys, time, random
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
# same exact Fourier-Motzkin oracle as check_arrangement.py, plus de-duplication of derived constraints
from math import comb
def feasible(cons, nvar):
    cons = [(list(c), Fr(d), r) for c, d, r in cons]
    while True:
        eq = next((k for k, (c, d, r) in enumerate(cons) if r == '=='), None)
        if eq is None: break
        c, d, r = cons.pop(eq)
        v = next((i for i in range(nvar) if c[i] != 0), None)
        if v is None:
            if d != 0: return False
            continue
        new = []
        for c2, d2, r2 in cons:
            if c2[v] != 0:
                f = c2[v] / c[v]; c2 = [c2[i] - f * c[i] for i in range(nvar)]; d2 = d2 - f * d
            new.append((c2, d2, r2))
        cons = new
    for v in range(nvar):
        pos = [x for x in cons if x[0][v] > 0]; neg = [x for x in cons if x[0][v] < 0]
        zer = [x for x in cons if x[0][v] == 0]
        for cp, dp, rp in pos:
            for cn, dn, rn in neg:
                a, b = cp[v], -cn[v]
                c = [b * cp[i] + a * cn[i] for i in range(nvar)]
                # normalise to cut duplicates
                zer.append((c, b * dp + a * dn, '<' if '<' in (rp, rn) else '<='))
        # dedupe after normalisation by max |coef|
        seen = {}
        for c, d, r in zer:
            m = max([abs(x) for x in c] + [Fr(0)])
            if m == 0:
                key = (tuple(c), d, r)
            else:
                key = (tuple(x / m for x in c), d / m, r)
            if key in seen and seen[key] == '<': continue
            seen[key] = r
        zer = [(list(k[0]), k[1], k[2]) for k in seen]
        cons = zer
    for c, d, r in cons:
        if r == '<' and not d < 0: return False
        if r == '<=' and not d <= 0: return False
    return True

def count_FM(H, e):
    n = [0]
    def rec(i, cons):
        if i == len(H): n[0] += 1; return
        nn, c = H[i]
        for s in (-1, 0, 1):
            k = (nn, c, '<') if s == -1 else ((nn, c, '==') if s == 0 else (tuple(-x for x in nn), -c, '<'))
            if feasible(cons + [k], e): rec(i + 1, cons + [k])
    rec(0, [])
    return n[0]

t0 = time.time()
rng = random.Random(7)
s = 10
H = [(tuple(Fr(rng.randint(-60, 60)) for _ in range(3)), Fr(rng.randint(-60, 60))) for _ in range(s)]
c3 = count_FM(H, 3)
gen = sum(comb(s, d) * sum(comb(s - d, j) for j in range(3 - d + 1)) for d in range(4))
print(f"C3: s={s} planes in R^3: exact realized={c3} (generic-position formula {gen});"
      f" misapplied e=2 bound 9(s+1)^2={9*(s+1)**2} -> violated={c3 > 9*(s+1)**2};"
      f" correct e=3 bound (e+1)^2(s+1)^e={16*(s+1)**3} holds={c3 <= 16*(s+1)**3}   [{time.time()-t0:.1f}s]")

