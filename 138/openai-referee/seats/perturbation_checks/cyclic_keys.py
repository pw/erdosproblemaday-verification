#!/usr/bin/env python3
"""Cyclic-model check of Lemma perturb:multiplicity and (perturb:separation).

G = Z/q^D, y_i(n) = lambda*n/q^i mod 1, centered representative
ytilde_i(n) in [-1/2,1/2) (exact rational r'/q^i), key(n) = (V-box of ytilde(n),
floor(||q ytilde(n)||^2)).  For every progression n0 + j d (d != 0, 0<=j<k)
we compute the largest multiplicity of a key, and for every pair n != n' we
check ||q ytilde(n) - q ytilde(n')||^2 >= 1 exactly (integer arithmetic).

MODE literal : the paper's literal parameters at k = 10 (D = 2, M = 4,
               h_0 = 4, lambda = 24, P prime in (10,200], q = P, H = 1/k^2,
               adaptive mesh (mesh:definition) with alpha = q^-(D+1)).
MODE stress  : hypotheses of the lemma kept (box widths <= 2H, 2kH < 1,
               lambda a unit mod q^D, P > k) but boxes made as WIDE as allowed
               (uniform mesh of width 1/ceil(1/(2H)) <= 2H, H = 0.49/k), q a higher prime
               power, so boxes contain whole progressions and only the norm
               band limits multiplicity.
MODE stress_adaptive : as stress but with the paper's adaptive mesh formula
               (geometric toward the cut) at scale H = 0.49/k.
Controls (must FAIL): ctl_nonunit (lambda = P, not a unit mod q^D),
               ctl_noband (key = box only), ctl_widebox (one interval, 2kH>=1).
Usage: cyclic_keys.py MODE k P e D
"""
import sys, math
import numpy as np
from fractions import Fraction as F
import mpmath
mpmath.mp.dps = 50

MODE = sys.argv[1]; k = int(sys.argv[2]); P = int(sys.argv[3]); e = int(sys.argv[4]); D = int(sys.argv[5])
q = P ** e; N = q ** D
assert all(P % r for r in range(2, int(P ** 0.5) + 1)) and P > k, "need prime P > k"

def paper_lambda(k, D):
    M = next(M for M in range(1, k + 1) if M * M >= k)
    h0 = D * D
    lam = 1
    for l in range(2, h0 + 1):
        if all(l % r for r in range(2, int(l ** 0.5) + 1)):
            a = 0
            while l ** (a + 1) <= 2 * M: a += 1      # = floor(log(2M)/log l)
            lam *= l ** a
    return lam, M, h0

if MODE == "literal":
    Dk = next(d for d in range(1, 100) if d ** 10 >= k)
    assert Dk == D, f"literal mode needs D = ceil(k^(1/10)) = {Dk}"
    lam, M, h0 = paper_lambda(k, D)
    assert h0 < 2 * M < k, (h0, M, k)
    # q = least power of P that is >= k^{ck/D}, c = 1e-5
    target = mpmath.power(k, mpmath.mpf(1) / 100000 * k / D)
    qq = 1
    while qq < target: qq *= P
    assert qq == q, f"literal q should be {qq}"
    H = F(1, k * k)
elif MODE == "ctl_nonunit":
    lam, H = P, F(49, 100 * k)
else:
    lam, H = 24, F(49, 100 * k)
assert math.gcd(lam, q) == 1 or MODE == "ctl_nonunit"
print(f"MODE={MODE} k={k} P={P} q={q} D={D} N={N} lambda={lam} H={H} 2kH={float(2*k*H):.3f}")

# centered numerators r'_i(n): ytilde_i(n) = r'_i(n) / q^i
n = np.arange(N, dtype=np.int64)
R = np.zeros((N, D), dtype=np.int64)
for i in range(1, D + 1):
    Q = q ** i
    r = (lam * n) % Q
    R[:, i - 1] = np.where(2 * r >= Q, r - Q, r)          # [-1/2,1/2): r/Q >= 1/2 -> subtract 1
# f(n) = ||q ytilde||^2 = sum_i r'_i^2 / q^{2(i-1)}; floor exactly via common denominator
den = q ** (2 * (D - 1))
num = sum((R[:, i - 1].astype(object) ** 2) * q ** (2 * (D - i)) for i in range(1, D + 1))
fl = np.array([x // den for x in num], dtype=np.int64)
assert all(0 <= x <= F(D * q * q, 4) * den for x in num), "0 <= f <= D q^2/4 violated"

# V labels
def adaptive_endpoints(Hs):
    alpha = mpmath.mpf(1) / mpmath.mpf(q) ** (D + 1)
    Rr = mpmath.log(1 + 1 / (2 * alpha))
    m = int(mpmath.ceil(Rr / Hs))                         # literal: m = ceil(k^2 R) when Hs = 1/k^2
    a = [alpha * (mpmath.e ** (l * Rr / m) - 1) for l in range(m + 1)]
    a[0] = mpmath.mpf(0); a[m] = mpmath.mpf(1) / 2          # exact by construction
    return a, m

if MODE in ("literal", "stress_adaptive"):
    a, m = adaptive_endpoints(mpmath.mpf(H.numerator) / H.denominator)
    widths = [a[l + 1] - a[l] for l in range(m)]
    assert max(widths) <= 2 * mpmath.mpf(H.numerator) / H.denominator, "mesh:width |I| <= 2H fails"
    lab = np.zeros((N, D), dtype=np.int64); margin = mpmath.mpf(1)
    import bisect
    af = a
    for idx in range(N):
        for i in range(D):
            Q = q ** (i + 1); y = mpmath.mpf(int(R[idx, i])) / Q
            if y < 0:                      # left family: x = y + 1/2 in [a_l, a_{l+1})
                x = y + mpmath.mpf(1) / 2
                l = bisect.bisect_right(af, x) - 1
                lab[idx, i] = l
            else:                          # right family: [1/2 - a_{l+1}, 1/2 - a_l), x' = 1/2 - y in (a_l, a_{l+1}]
                x = mpmath.mpf(1) / 2 - y
                l = bisect.bisect_left(af, x) - 1
                lab[idx, i] = m + l
            for ep in (af[max(l, 0)], af[min(l + 1, m)]):
                d_ = abs(ep - x)
                if d_ > 0: margin = min(margin, d_)
    print(f"adaptive mesh: m={m} intervals per family, max width={float(max(widths)):.3e} <= 2H={float(2*H):.3e}, "
          f"min nonzero point-endpoint gap={mpmath.nstr(margin, 5)}")
elif MODE in ("stress", "ctl_nonunit", "ctl_noband"):
    Wden = math.ceil(1 / (2 * H)); W = F(1, Wden); assert W <= 2 * H
    print(f"uniform mesh: {Wden} intervals of width {W} <= 2H")
    # interval index floor((y + 1/2)/W), exact
    lab = np.zeros((N, D), dtype=np.int64)
    for i in range(D):
        Q = q ** (i + 1)
        lab[:, i] = ((2 * R[:, i] + Q) * Wden) // (2 * Q)
elif MODE == "ctl_widebox":
    lab = np.zeros((N, D), dtype=np.int64)      # one interval [-1/2,1/2): width 1 > 2H, 2kH >= 1
else:
    raise SystemExit("bad mode")

keys = {}
kid = np.zeros(N, dtype=np.int64)
for idx in range(N):
    t = tuple(lab[idx]) + ((int(fl[idx]),) if MODE != "ctl_noband" else ())
    kid[idx] = keys.setdefault(t, len(keys))
print(f"distinct keys={len(keys)}, max elements of G per key={np.bincount(kid).max()}")

# separation over all pairs n != n' (exact integers)
sep_fail = 0
w = np.array([q ** (2 * (D - i)) for i in range(1, D + 1)], dtype=object)
Ri = R.astype(np.int64)
for s0 in range(0, N, 256):
    blk = Ri[s0:s0 + 256]
    diff = blk[:, None, :] - Ri[None, :, :]                  # (b, N, D)
    acc = np.zeros(diff.shape[:2], dtype=np.float64)
    tot = np.zeros(diff.shape[:2], dtype=object) if q ** (2 * D) > 2 ** 52 else None
    if tot is None:
        val = sum((diff[:, :, i - 1].astype(np.int64) ** 2) * int(q ** (2 * (D - i))) for i in range(1, D + 1))
        bad = (val < q ** (2 * (D - 1)))
    else:
        val = sum((diff[:, :, i - 1].astype(object) ** 2) * q ** (2 * (D - i)) for i in range(1, D + 1))
        bad = (val < q ** (2 * (D - 1)))
    for b in range(bad.shape[0]):
        bad[b, s0 + b] = False                              # skip n == n'
    sep_fail += int(np.count_nonzero(bad))
print(f"separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all {N*(N-1)} ordered pairs: failures={sep_fail}")

# key multiplicity over every progression (n0, d), d != 0
J = np.arange(k, dtype=np.int64)
dist = np.zeros(k + 1, dtype=np.int64)
worst = 0; witness = None
d_all = np.arange(1, N, dtype=np.int64)
for s0 in range(0, N, 64):
    n0 = np.arange(s0, min(N, s0 + 64), dtype=np.int64)
    idx = (n0[:, None, None] + J[None, None, :] * d_all[None, :, None]) % N
    kk = kid[idx]                                             # (b, N-1, k)
    eq = (kk[:, :, :, None] == kk[:, :, None, :]).sum(axis=3) # multiplicity of each position's key
    mx = eq.max(axis=2)
    dist += np.bincount(mx.ravel(), minlength=k + 1)
    if mx.max() > worst:
        worst = int(mx.max()); b, dd = np.argwhere(mx == worst)[0]
        witness = (int(n0[b]), int(d_all[dd]))
print(f"progressions checked={int(dist.sum())}; max key multiplicity={worst} (witness n0,d={witness}); "
      f"distribution of per-progression max: { {i:int(c) for i,c in enumerate(dist) if c} }")
ok = worst <= 4 and sep_fail == 0
print("Lemma perturb:multiplicity (<=4) and (perturb:separation):", "HOLD" if ok else "FAIL")
sys.exit(0 if ok else 1)
