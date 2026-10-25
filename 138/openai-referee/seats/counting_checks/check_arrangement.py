"""Check Lemma count:arrangement (printed Lemma 3.1, p.7):
#realized ternary sign vectors of s affine hyperplanes in R^e
   <= B1 = sum_{d=0}^e C(s,d) sum_{j=0}^{e-d} C(s,j) <= B2 = (e+1)^2 (s+1)^e.
Oracle 1: exact Fourier-Motzkin feasibility (strict/non-strict/equality), DFS over sign vectors.
Oracle 2 (e=2): exact face enumeration in a large box (arr2d.face_points).
Oracle 3 (e=2): Zaslavsky count  V + sum_L (v_L+1) + (1 + n + sum_p (t_p - 1))  over distinct lines.
Oracle 4 (e=1): 2r+1 for r distinct roots.
Controls that MUST fail are at the bottom."""
import random, sys, time
from fractions import Fraction as Fr
from math import comb
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
from arr2d import face_points, sign_vector, norm_line

def B1(e, s): return sum(comb(s, d) * sum(comb(s, j) for j in range(e - d + 1)) for d in range(e + 1))
def B2(e, s): return (e + 1) ** 2 * (s + 1) ** e
def strict_only(e, s): return sum(comb(s, j) for j in range(e + 1))

# ---------- exact Fourier-Motzkin with strictness ----------
# constraint: (coef tuple, const, rel) meaning coef.x + const  rel 0, rel in '<','<=','=='
def feasible(cons, nvar):
    cons = [(list(c), Fr(d), r) for c, d, r in cons]
    # eliminate equalities
    while True:
        eq = next((k for k, (c, d, r) in enumerate(cons) if r == '=='), None)
        if eq is None:
            break
        c, d, r = cons.pop(eq)
        v = next((i for i in range(nvar) if c[i] != 0), None)
        if v is None:
            if d != 0:
                return False
            continue
        new = []
        for c2, d2, r2 in cons:
            if c2[v] != 0:
                f = c2[v] / c[v]
                c2 = [c2[i] - f * c[i] for i in range(nvar)]
                d2 = d2 - f * d
            new.append((c2, d2, r2))
        cons = new
    for v in range(nvar):
        pos = [x for x in cons if x[0][v] > 0]
        neg = [x for x in cons if x[0][v] < 0]
        zer = [x for x in cons if x[0][v] == 0]
        for cp, dp, rp in pos:
            for cn, dn, rn in neg:
                a, b = cp[v], -cn[v]
                c = [b * cp[i] + a * cn[i] for i in range(nvar)]
                zer.append((c, b * dp + a * dn, '<' if '<' in (rp, rn) else '<='))
        cons = zer
    for c, d, r in cons:
        if r == '<' and not d < 0: return False
        if r == '<=' and not d <= 0: return False
    return True

def count_signs_FM(H, e):
    """H: list of (normal tuple, const) for f(x)=n.x+c. Count realized sign vectors."""
    out = []
    def rec(i, cons, sig):
        if i == len(H):
            out.append(tuple(sig)); return
        n, c = H[i]
        for s in (-1, 0, 1):
            if s == -1: k = (n, c, '<')
            elif s == 0: k = (n, c, '==')
            else: k = (tuple(-x for x in n), -c, '<')
            if feasible(cons + [k], e):
                rec(i + 1, cons + [k], sig + [s])
    rec(0, [], [])
    return out

def rand_arr(e, s, rng, coef=2):
    H = []
    while len(H) < s:
        r = rng.random()
        if H and r < 0.15:                      # repeated hyperplane (possibly re-scaled / re-oriented)
            n, c = rng.choice(H); f = rng.choice([-2, -1, 2, 3])
            H.append((tuple(f * x for x in n), f * c)); continue
        n = tuple(Fr(rng.randint(-coef, coef)) for _ in range(e))
        if all(x == 0 for x in n): continue
        H.append((n, Fr(rng.randint(-coef, coef))))
    return H

def zaslavsky2(H):
    lines = sorted(set(norm_line(n[0], n[1], -c) for n, c in H))
    from itertools import combinations
    pts = {}
    for i, j in combinations(range(len(lines)), 2):
        A1, B1_, C1 = lines[i]; A2, B2_, C2 = lines[j]
        det = A1 * B2_ - A2 * B1_
        if det == 0: continue
        p = ((C1 * B2_ - C2 * B1_) / det, (A1 * C2 - A2 * C1) / det)
        pts.setdefault(p, set()).update((i, j))
    V = len(pts)
    E = sum(1 + sum(1 for p in pts if i in pts[p]) for i in range(len(lines)))
    R = 1 + len(lines) + sum(len(t) - 1 for t in pts.values())
    return V + E + R

def faces2(H):
    lines = [(n[0], n[1], -c) for n, c in H]
    # big box containing every vertex and the foot point of every line strictly inside
    from itertools import combinations
    big = Fr(1)
    for (A1, B1_, C1), (A2, B2_, C2) in combinations(lines, 2):
        det = A1 * B2_ - A2 * B1_
        if det != 0:
            big = max(big, abs((C1 * B2_ - C2 * B1_) / det), abs((A1 * C2 - A2 * C1) / det))
    for A, B, C in lines:
        nn = A * A + B * B
        big = max(big, abs(C * A / nn), abs(C * B / nn))
    big = 4 * big + 1
    pts = face_points(lines, (-big, big, -big, big))
    return len({sign_vector(lines, p) for p in pts if -big < p[0] < big and -big < p[1] < big})

rng = random.Random(20261015)
t0 = time.time()
worst = {}
ntests = 0
for e, s_list, reps in [(1, range(1, 9), 40), (2, range(1, 8), 40), (3, range(1, 7), 15)]:
    for s in s_list:
        for _ in range(reps):
            H = rand_arr(e, s, rng)
            cnt = len(count_signs_FM(H, e))
            assert cnt <= B1(e, s) <= B2(e, s), (e, s, cnt, H)
            if e == 1:
                roots = {-c / n[0] for n, c in H}
                assert cnt == 2 * len(roots) + 1, (cnt, roots)
            if e == 2:
                z = zaslavsky2(H); f = faces2(H)
                assert cnt == z == f, (cnt, z, f, H)
            ntests += 1
            worst[(e, s)] = max(worst.get((e, s), 0), cnt)
# general position extremes (maximal counts)
gp = {}
for e, s in [(2, 4), (2, 6), (3, 4), (3, 5)]:
    while True:
        H = [(tuple(Fr(rng.randint(-50, 50)) for _ in range(e)), Fr(rng.randint(-50, 50))) for _ in range(s)]
        if all(any(x != 0 for x in n) for n, c in H): break
    gp[(e, s)] = len(count_signs_FM(H, e))
    assert gp[(e, s)] <= B1(e, s)
print("random arrangements tested:", ntests, " (FM oracle; e=2 also vs face-enumeration and Zaslavsky; e=1 vs 2r+1)")
for (e, s), w in sorted(worst.items()):
    print(f"  e={e} s={s}: max realized={w:4d}  B1={B1(e,s):5d}  B2=(e+1)^2(s+1)^e={B2(e,s):6d}")
print("general position:", {k: (v, B1(*k), B2(*k)) for k, v in gp.items()})

# restriction to a subset: e=2, half-open box [0,1)^2 -- must be <= unrestricted count
for _ in range(20):
    H = rand_arr(2, 6, rng, coef=3)
    lines = [(n[0], n[1], -c) for n, c in H]
    pts = face_points(lines, (0, 1, 0, 1))
    rcnt = len({sign_vector(lines, p) for p in pts if 0 <= p[0] < 1 and 0 <= p[1] < 1})
    assert rcnt <= len(count_signs_FM(H, 2)) <= B1(2, 6)
print("restriction to [0,1)^2: 20 cases, restricted <= unrestricted <= B1: OK")

# ---------------- CONTROLS (each must report a violation) ----------------
print("\nCONTROLS (each line must show a VIOLATION):")
# C1: strict-region bound misapplied to ternary sign vectors
e, s = 2, 6; c = gp[(2, 6)]
print(f" C1 strict-only bound sum_j<=e C(s,j)={strict_only(e,s)} vs ternary count {c}: violated={c > strict_only(e,s)}")
# C2: dropping the (e+1)^2 factor
print(f" C2 (s+1)^e={(s+1)**e} vs ternary count {c}: violated={c > (s+1)**e}")
# C3: the e=2 count misapplied to a 3-parameter family (8 generic planes); see control_c3.py for s=10 vs 9(s+1)^2
H = [(tuple(Fr(rng.randint(-60, 60)) for _ in range(3)), Fr(rng.randint(-60, 60))) for _ in range(8)]
c3 = len(count_signs_FM(H, 3))
print(f" C3 e=2 count B1(2,8)={B1(2,8)} vs 8 generic planes in R^3: {c3}: violated={c3 > B1(2,8)};  correct e=3 bound B1(3,8)={B1(3,8)}: holds={c3 <= B1(3,8)}")
print("time %.1fs" % (time.time() - t0))
