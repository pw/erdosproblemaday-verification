# Lemma 7.1, per-place upper bound at an ARCHIMEDEAN entry, simulated with the actual grid labels of §4.4.
# Point star p with neighbours q, q' (jumps d, d' arbitrary distinct nonzero complex numbers, as at a
# non-identity embedding where sigma(w) is not conj(sigma(z))):  z_q = z_p - d, w_q = w_p - 1/d.
# A-label at level s: cell of side e^{-s} containing z, fixed fractional shift; B1-label: side e^{s}.
# Worst case: every level is good rare, p exceptional, minority bit 0 below a cut s*, 1 above (any
# monotone pattern).  Score_v = int 2*1{Y1=Y2=minority}*N ds - int |Y1-Y2| ds.
# Claim (Lemma 7.1 proof): Score_v <= 2T_v - (b'-b) with T_v = alpha + log 2, alpha = u - b,
# u = -log|d-d'|; and 2T_v-(b'-b) = -log|(d-d')(1/d-1/d')| + 2log2  [(5.14)].
import numpy as np, math
rng = np.random.default_rng(7)
def cells(x, side, sh):
    return np.floor(x.real/side + sh[0]).astype(np.int64), np.floor(x.imag/side + sh[1]).astype(np.int64)
def trial(cv, nscan=60, ds=2e-4):
    zp = complex(*rng.normal(size=2))*rng.uniform(0.1,10); wp = complex(*rng.normal(size=2))*rng.uniform(0.1,10)
    d  = complex(*rng.normal(size=2))*math.exp(rng.uniform(-3,3))
    dd = d*(1 + complex(*rng.normal(size=2))*math.exp(rng.uniform(-4,1)))   # d' near or far from d
    zq, wq, zqq, wqq = zp-d, wp-1/d, zp-dd, wp-1/dd
    n1, n2 = -math.log(abs(d)), -math.log(abs(dd)); b, bp = min(n1,n2), max(n1,n2)
    u = -math.log(abs(d-dd)); alpha = u-b; T = alpha + cv
    x = (d-dd)*(1/d-1/dd); assert abs(-math.log(abs(x)) - (2*alpha-(bp-b))) < 1e-9     # (5.14)
    lo, hi = b - abs(T) - 3, bp + abs(T) + 3
    s = np.arange(lo, hi, ds)
    shA, shB = rng.uniform(0,1,2), rng.uniform(0,1,2)
    sideA, sideB = np.exp(-s), np.exp(s)
    Aq, Aqq = cells(zq*np.ones_like(s), sideA, shA), cells(zqq*np.ones_like(s), sideA, shA)
    Bq, Bqq = cells(wq*np.ones_like(s), sideB, shB), cells(wqq*np.ones_like(s), sideB, shB)
    Amatch = (Aq[0]==Aqq[0]) & (Aq[1]==Aqq[1]); Bmatch = (Bq[0]==Bqq[0]) & (Bq[1]==Bqq[1])
    Y1, Y2 = (n1 > s), (n2 > s)
    neg = np.sum(Y1 != Y2)*ds
    both1 = Y1 & Y2 & Bmatch           # candidate positives with minority bit 1
    both0 = (~Y1) & (~Y2) & Amatch     # candidate positives with minority bit 0
    worst = -1e9
    for cut in np.linspace(lo, hi, nscan):
        pos = 2*ds*(np.sum(both0 & (s < cut)) + np.sum(both1 & (s >= cut)))
        worst = max(worst, pos - neg)
    bound = 2*T - (bp - b)
    # interval claims: bit-1 positives inside [b-T_v, b], bit-0 positives inside [b', b'+T_v] (T_v with log 2)
    T2 = alpha + math.log(2)
    out1 = np.any(both1 & ((s < b - T2 - 2*ds) | (s >= b)))
    out0 = np.any(both0 & ((s < bp) | (s > bp + T2 + 2*ds)))
    return worst - bound, out1 or out0, T2
viol = 0; maxexc = -1e9; intervals_bad = 0; N = 400
for _ in range(N):
    e, ib, T2 = trial(math.log(2)); maxexc = max(maxexc, e); viol += e > 1e-3; intervals_bad += ib
print("paper's bound (c_v = log 2): trials=%d violations=%d max(score-bound)=%.4f interval-claim failures=%d"
      %(N, viol, maxexc, intervals_bad))
viol0 = 0; maxexc0 = -1e9
for _ in range(N):
    e, _, _ = trial(0.0); maxexc0 = max(maxexc0, e); viol0 += e > 1e-3
print("CONTROL c_v = 0 at the archimedean entry: violations=%d max(score-bound)=%.4f (expect >0)"%(viol0, maxexc0))
