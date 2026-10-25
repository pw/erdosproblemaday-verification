"""Check Lemma count:global (printed Lemma 3.2, p.7), scalar step: for a circle partition with F endpoints
(half-open arcs [tau_i, tau_{i+1}) in increasing direction), the words (label((a+jb) mod 1))_{0<=j<k},
(a,b) in [0,1)^2, are determined by the ternary signs of a+jb-(tau+z), -1<=z<=k  (<= 3k^2F lines), hence
#words <= #realized sign vectors <= 9(3k^2F+1)^2.  Exact: every face of the arrangement (incl. box lines)
gets a rational sample point, so the realized word set is computed exactly.
Control (must FAIL): comparisons against tau only (z=0, no integer lifts) do NOT determine the word."""
import sys, time, random
from fractions import Fraction as Fr
from math import comb
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
from arr2d import face_points, sign_vector

def label(x, taus):            # taus sorted in [0,1); arcs [tau_i, tau_{i+1}), last arc wraps
    f = x - (x.numerator // x.denominator)
    idx = -1
    for i, t in enumerate(taus):
        if f >= t: idx = i
    return idx % len(taus)     # f < taus[0] lies in the wrapping arc [tau_F, tau_1 + 1)

def B1(e, s): return sum(comb(s, d) * sum(comb(s, j) for j in range(e - d + 1)) for d in range(e + 1))

t0 = time.time()
rng = random.Random(3)
cases = [(2, [Fr(0)]), (3, [Fr(0), Fr(2, 5)]), (4, [Fr(0), Fr(1, 3), Fr(3, 4)]),
         (5, [Fr(0), Fr(1, 2)]), (4, [Fr(1, 7), Fr(5, 7)]), (6, [Fr(0), Fr(2, 3)])]
for k, taus in cases:
    F = len(taus)
    full = [(Fr(1), Fr(j), t + z) for j in range(k) for t in taus for z in range(-1, k + 1)]
    assert len(full) <= 3 * k * k * F
    pts = [p for p in face_points(full, (0, 1, 0, 1)) if 0 <= p[0] < 1 and 0 <= p[1] < 1]
    # add random rational points as extra probes of the determination claim
    pts += [(Fr(rng.randrange(10**6), 10**6), Fr(rng.randrange(10**6), 10**6)) for _ in range(3000)]
    words, sv2w, ok = set(), {}, True
    for p in pts:
        w = tuple(label(p[0] + j * p[1], taus) for j in range(k))
        words.add(w)
        sv = sign_vector(full, p)
        if sv2w.setdefault(sv, w) != w: ok = False
    nsv = len(sv2w)
    # control: no integer lifts (z = 0 only)
    nolift = [(Fr(1), Fr(j), t) for j in range(k) for t in taus]
    m, clash = {}, 0
    for p in pts:
        w = tuple(label(p[0] + j * p[1], taus) for j in range(k))
        sv = sign_vector(nolift, p)
        if m.setdefault(sv, w) != w: clash += 1
    s = len(full)
    print(f"k={k} F={F} taus={[str(t) for t in taus]}: lines={s} (3k^2F={3*k*k*F}) words={len(words)} "
          f"signvecs={nsv} B1(2,s)={B1(2,s)} 9(3k^2F+1)^2={9*(3*k*k*F+1)**2} "
          f"determined={ok}  CONTROL(no lifts) clashes={clash} -> determination fails={clash>0}")
    assert ok and len(words) <= nsv <= B1(2, s) <= 9 * (3 * k * k * F + 1) ** 2
print("time %.1fs" % (time.time() - t0))
