"""Check Lemma count:local (printed Lemma 3.4, pp.8-9) on a surrogate V-mesh built with the paper's literal
formulas (mesh:definition): R = log(1+1/(2 alpha)), m = ceil(k^2 R), a_l = alpha(e^{lR/m}-1), H = k^{-2},
eta = 1/(1000 D).  Surrogate: k = 4 (H = 1/16), D = 1, alpha in {2^-20, 2^-30, 2^-45}.  Endpoints are exact
rationals (60-digit decimal values of the formulas).
(a) mesh:neighbors: endpoints in N(I) <= 49, |J| >= |I|/16 for J meeting N(I)           [used by stationary case]
(b) mesh:truncated: V_eta breakpoints on any arc of length 4H <= 16004 D                  [used by rotating case]
(c) stationary case, exact 2D: a in I (half-open lift), |b| <= |I|, targets a + tau_z + (z-z0)/h * b with
    INTEGER tau_z: #distinct output sequences <= 9(49h+1)^2, and the output is a function of the signs
    against the lifted endpoints of N(I).  CONTROL: endpoints of I's closure only -> determination fails.
(d) width-independence: one target, max over ALL anchors I of #labels reachable, |b| <= |I| (clause (iii))
    vs CONTROL |b| <= H (absolute drift): the latter grows with log(1/alpha), i.e. with q.
(e) rotating case: one target, |b| <= H, truncated output V_eta: max #outputs is alpha-independent;
    CONTROL without truncation grows with log(1/alpha).
(f) rotating case, exact 2D for anchors with rho >= eta, h = 3."""
import sys, time, bisect, random
from fractions import Fraction as Fr
import mpmath
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
from arr2d import face_points, sign_vector
mpmath.mp.dps = 60
HALF = Fr(1, 2)

def build_mesh(kk, alpha_exp):
    alpha = mpmath.mpf(2) ** (-alpha_exp)
    R = mpmath.log(1 + 1 / (2 * alpha))
    m = int(mpmath.ceil(kk * kk * R))
    a = [Fr(0)] + [Fr(mpmath.nstr(alpha * (mpmath.exp(l * R / m) - 1), 55)) for l in range(1, m)] + [HALF]
    assert all(x < y for x, y in zip(a, a[1:]))
    pts = set()
    for al in a:
        pts.add((-HALF + al) % 1); pts.add((HALF - al) % 1)
    E = sorted(pts)
    assert len(E) == 2 * m
    return E, Fr(mpmath.nstr(alpha, 55)), m

def arcs(E):   # list of (left, right) real lifts with left in [0,1), right = next endpoint (wrap +1)
    return [(E[i], E[i + 1] if i + 1 < len(E) else E[0] + 1) for i in range(len(E))]

def vlabel(x, E):
    f = x - (x.numerator // x.denominator)
    i = bisect.bisect_right(E, f) - 1
    return i % len(E)

def rho(x):
    f = x - (x.numerator // x.denominator)
    d = abs(f - HALF)
    return min(d, 1 - d)

def lifts_in(E, lo, hi):     # all reals e + n (e in sorted E, n integer) with lo <= e+n <= hi
    out = []
    n0 = lo.numerator // lo.denominator - 1
    for n in range(n0, n0 + int(hi - lo) + 3):
        i = bisect.bisect_left(E, lo - n)
        j = bisect.bisect_right(E, hi - n)
        out.extend(e + n for e in E[i:j])
    return sorted(out)

def count_in_closed_arc(E, lo, hi):   # endpoints (circle points) lying in closed real interval [lo,hi], length<1
    return len(lifts_in(E, lo, hi))

t0 = time.time()
KK, D = 4, 1
H = Fr(1, KK * KK); eta = Fr(1, 1000 * D)
meshes = {ae: build_mesh(KK, ae) for ae in (20, 30, 45)}
for ae, (E, alpha, m) in meshes.items():
    A = arcs(E)
    # (a)
    worstN, worstratio = 0, Fr(10**9)
    for (L, Rr) in A:
        w = Rr - L
        cnt = count_in_closed_arc(E, L - w, Rr + w)
        worstN = max(worstN, cnt)
    # |J| >= w/16 for J whose closure meets N(I): J ranges over arcs overlapping [L-w, R+w] (closed)
    widths = [r - l for l, r in A]
    n = len(A)
    for i, (L, Rr) in enumerate(A):
        w = Rr - L
        for di in range(-8, 9):
            j = (i + di) % n
            l2, r2 = A[j]
            for sh in (-1, 0, 1):
                if l2 + sh <= Rr + w and r2 + sh >= L - w:
                    worstratio = min(worstratio, (r2 - l2) / w)
    # (b) breakpoints of V_eta on arcs of length 4H, arcs starting at every breakpoint
    thr = [(HALF - eta), (HALF + eta) % 1]
    bps = sorted({e for e in E if rho(e) >= eta} | set(thr))
    worstB = 0
    ext = bps + [b + 1 for b in bps]
    for t_i, s0 in enumerate(bps):
        worstB = max(worstB, bisect.bisect_right(ext, s0 + 4 * H) - t_i)
    print(f"alpha=2^-{ae}: 2m={2*m} intervals; (a) max endpoints in N(I)={worstN} (<=49: {worstN<=49}), "
          f"min |J|/|I| over J meeting N(I)={float(worstratio):.4f} (>=1/16: {worstratio>=Fr(1,16)}); "
          f"(b) max V_eta breakpoints on a 4H arc={worstB} (<=16004D: {worstB<=16004*D})")
    assert worstN <= 49 and worstratio >= Fr(1, 16) and worstB <= 16004 * D

# (d) and (e): one target, z0 = 0, z = 1, h = 2 -> c = 1/2
print("(d)/(e) one target c=1/2, max over all anchor intervals of #distinct outputs reachable:")
for ae, (E, alpha, m) in meshes.items():
    A = arcs(E)
    rel = absd = rot_trunc = rot_full = 0
    for (L, Rr) in A:
        w = Rr - L
        # stationary, clause (iii): |b| <= w  -> target range [L - w/2, R + w/2] (R excluded only for b=0, harmless)
        rel = max(rel, count_in_closed_arc(E, L - w / 2, Rr + w / 2) + 1)
        # control: absolute drift |b| <= H
        absd = max(absd, count_in_closed_arc(E, L - H / 2, Rr + H / 2) + 1)
        # rotating: |b| <= H, truncated output (count breakpoints of V_eta in range, +1)
        lo, hi = L - H / 2, Rr + H / 2
        bp = [v for v in lifts_in(E, lo, hi) if rho(v) >= eta] + [v for v in lifts_in([HALF - eta, (HALF + eta) % 1], lo, hi)]
        rot_trunc = max(rot_trunc, len(set(bp)) + 1)
        rot_full = max(rot_full, count_in_closed_arc(E, lo, hi) + 1)
    print(f"  alpha=2^-{ae}: stationary |b|<=|I|: {rel:3d} (<=50: {rel<=50}) | CONTROL stationary |b|<=H: {absd:3d}"
          f" | rotating truncated: {rot_trunc:3d} | CONTROL rotating untruncated: {rot_full:3d}")
print("  (CONTROL columns must grow with log(1/alpha); the clause-(iii) and truncated columns must not)")

# (c) stationary exact 2D
E, alpha, m = meshes[30]
A = arcs(E)
rng = random.Random(11)
idx_cut = [i for i, (l, r) in enumerate(A) if l <= HALF + 0 and r > HALF or (l <= Fr(3, 2) and r > Fr(3, 2))]
picks = sorted(set(idx_cut + [0, len(A) // 4] + [rng.randrange(len(A)) for _ in range(2)]))
h = 4
for i in picks:
    L, Rr = A[i]; w = Rr - L
    for z0 in (0, 2):
        cz = {z: Fr(z - z0, h) for z in range(h)}
        tau = {z: 3 * (z - z0) for z in range(h)}          # integral translations (stationary case)
        lines, lines_ctl = [], []
        maxrel = 0
        for z in range(h):
            if z == z0: continue
            lo, hi = L + tau[z] - abs(cz[z]) * w, Rr + tau[z] + abs(cz[z]) * w
            rel = lifts_in(E, lo, hi)
            maxrel = max(maxrel, len(rel))
            lines += [(Fr(1), cz[z], e - tau[z]) for e in rel]   # a + tau_z + c_z b = e
            # control: the same circle endpoints but NOT lifted into the target range (representatives in [0,1))
            lines_ctl += [(Fr(1), cz[z], (e % 1) - tau[z]) for e in rel]
        pts = [p for p in face_points(lines, (L, Rr, -w, w)) if L <= p[0] < Rr]
        pts += [(L + w * Fr(rng.randrange(10**6), 10**6), w * Fr(rng.randrange(-10**6, 10**6 + 1), 10**6)) for _ in range(600)]
        outs, m1, ok, m2, clash = set(), {}, True, {}, 0
        for p in pts:
            o = tuple(vlabel(p[0] + tau[z] + cz[z] * p[1], E) for z in range(h))
            outs.add(o)
            if m1.setdefault(sign_vector(lines, p), o) != o: ok = False
            if m2.setdefault(sign_vector(lines_ctl, p), o) != o: clash += 1
        bound = 9 * (49 * h + 1) ** 2
        print(f"(c) anchor arc #{i} width={float(w):.3e} rho(left)={float(rho(L)):.3e} z0={z0}: relevant endpoints/target<= {maxrel}"
              f" lines={len(lines)} outputs={len(outs)} <= 9(49h+1)^2={bound}: {len(outs)<=bound}; determined={ok};"
              f" CONTROL(unlifted endpoints) clashes={clash}")
        assert ok and maxrel <= 49 and len(outs) <= bound and clash > 0

# (f) rotating exact 2D, h = 3, anchors with rho >= eta, |b| <= H, truncated outputs
h = 3
cnt = 0
for i in [0, len(A) // 3, 5, len(A) - 40]:
    L, Rr = A[i]
    if rho(L) < eta: continue
    for z0 in (0, 1):
        cz = {z: Fr(z - z0, h) for z in range(h)}
        tau = {z: Fr(7 * (z - z0), 3) for z in range(h)}   # arbitrary non-integral translation (lambda t_i/h)
        lines = []
        for z in range(h):
            if z == z0: continue
            lo, hi = L + tau[z] - abs(cz[z]) * H, Rr + tau[z] + abs(cz[z]) * H
            bp = [v for v in lifts_in(E, lo, hi) if rho(v) >= eta] + lifts_in([HALF - eta, HALF + eta], lo, hi)
            assert len(set(bp)) <= 16004 * D
            lines += [(Fr(1), cz[z], v - tau[z]) for v in sorted(set(bp))]
        if len(lines) > 90: continue
        pts = [p for p in face_points(lines, (L, Rr, -H, H)) if L <= p[0] < Rr]
        def out(p):
            r = []
            for z in range(h):
                x = p[0] + tau[z] + cz[z] * p[1]
                r.append('*' if rho(x) < eta else vlabel(x, E))
            return tuple(r)
        pts += [(L + (Rr - L) * Fr(rng.randrange(10**6), 10**6), H * Fr(rng.randrange(-10**6, 10**6 + 1), 10**6)) for _ in range(400)]
        m1, ok, outs = {}, True, set()
        for p in pts:
            o = out(p); outs.add(o)
            if m1.setdefault(sign_vector(lines, p), o) != o: ok = False
        cnt += 1
        print(f"(f) rotating anchor arc #{i} rho={float(rho(L)):.3f} z0={z0}: lines={len(lines)} outputs={len(outs)}"
              f" <= 9(16004Dh+1)^2: {len(outs) <= 9*(16004*D*h+1)**2}; determined={ok}")
        assert ok
print("time %.1fs" % (time.time() - t0))
