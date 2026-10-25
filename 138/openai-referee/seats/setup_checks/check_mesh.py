# The V-mesh of 02-setup.tex, built LITERALLY from (mesh:definition)/(mesh:intervals) for small k, in 30-digit mpmath:
#   D=ceil(k^{1/10}), P = least prime > k, q = least power of P >= k^{ck/D} (c=1e-5), alpha = q^{-(D+1)},
#   R = log(1+1/(2alpha)), m = ceil(k^2 R), a_l = alpha(e^{lR/m}-1), H = k^{-2}, eta = 1/(1000 D).
# Verifies: partition of [-1/2,1/2) (a_0=0, a_m=1/2, strict monotonicity, where 0 and the cut sit);
#   Lemma mesh:width  (1/4)H(rho+alpha) <= |I| <= 2H(rho+alpha) <= 2H at BOTH closure endpoints of every I
#      (rho is affine on each closed interval, so endpoint checks cover all of I-bar), |V| = 2m vs k^3 log k;
#   Lemma mesh:neighbors: for every I, N(I) = {dist(Y, I-bar) <= w}: #mesh endpoints in N(I) <= 49 and min|J| >= w/16
#      over all J with J-bar meeting N(I) (circular, incl. wrap across the cut);
#   Lemma mesh:truncated: max #breakpoints of V_eta on a closed arc of length 4H  <= 16004 D
#      (breakpoints = mesh endpoints with rho >= eta, plus the two threshold points rho = eta; max is attained by
#       arcs starting at a breakpoint, so all such arcs are enumerated).
# CONTROLS (must FAIL the same checker): C1 wrong growth rate m' = ceil(k R) ; C2 uniform mesh of 2m equal cells ;
#   C3 the paper's mesh with 64 consecutive cells merged into one (abrupt scale change).
import math, bisect, sys, time
import mpmath
from sympy import nextprime
mpmath.mp.dps = 30
mpf = mpmath.mpf
HALF = mpf(1)/2

def iroot_ceil(k, r):
    D = max(1, int(round(k ** (1.0/r))))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def params(k):
    D = iroot_ceil(k, 10); P = nextprime(k)
    c = mpf(1)/10**5; lk = mpmath.log(k); lP = mpmath.log(P)
    e = 1
    while e*lP < c*k*lk/D: e += 1
    q = P**e
    alpha = mpf(1)/mpf(q)**(D+1)
    R = mpmath.log(1 + 1/(2*alpha))
    m = int(mpmath.ceil(mpf(k)**2 * R))
    H = mpf(1)/k**2; eta = mpf(1)/(1000*D)
    return dict(k=k, D=D, P=P, q=q, alpha=alpha, R=R, m=m, H=H, eta=eta)

def paper_endpoints(pr, m=None):
    m = pr['m'] if m is None else m
    al, R = pr['alpha'], pr['R']
    a = [al*(mpmath.exp(l*R/m) - 1) for l in range(m+1)]
    # identity a_m = alpha(e^R - 1) = alpha * 1/(2 alpha) = 1/2 is exact; check numerically, then store it exactly
    assert abs(a[m] - HALF) < mpf(10)**-25, a[m]
    a[m] = HALF
    return a

def mesh_from_a(a):
    # sorted endpoint list E (all in [-1/2,1/2)), intervals [E_i, E_{i+1}) with E_{len} := 1/2 (== -1/2 on circle)
    m = len(a) - 1
    E = [-HALF + a[l] for l in range(m)] + [HALF - a[l] for l in range(m, 0, -1)]
    return E

def rho(x):              # x in [-1/2, 1/2]
    return HALF - abs(x)

def check_partition(a, E):
    m = len(a) - 1
    ok = (a[0] == 0) and abs(a[m] - HALF) < mpf(10)**-25 and all(a[i] < a[i+1] for i in range(m))
    ok = ok and all(E[i] < E[i+1] for i in range(len(E)-1)) and E[0] == -HALF and E[-1] < HALF
    # zero is the LEFT endpoint of an interval (assigned to the interval on its right); the cut -1/2 is E[0]
    iz = bisect.bisect_right(E, mpf(0)) - 1          # index of the interval containing 0 (half-open [E_i,E_{i+1}))
    zero_ok = (E[iz] == 0) and (iz == m)              # 0 is the LEFT end of the interval right of it: [0, 1/2 - a_{m-1})
    return ok, zero_ok, iz

def widths(E):
    return [E[i+1] - E[i] for i in range(len(E)-1)] + [HALF - E[-1]]

def check_width(pr, E, W):
    H, al = pr['H'], pr['alpha']
    worst_lo = None; worst_hi = None; viol = 0; maxw = 0
    n = len(E)
    for i in range(n):
        l = E[i]; r = E[i+1] if i+1 < n else HALF
        for y in (l, r):
            s = rho(y) + al
            lo = W[i] / (H*s); 
            if worst_lo is None or lo < worst_lo: worst_lo = lo
            if worst_hi is None or lo > worst_hi: worst_hi = lo
            if not (H*s/4 <= W[i] <= 2*H*s <= 2*H): viol += 1
        maxw = max(maxw, W[i])
    return viol, worst_lo, worst_hi, maxw

def count_closed(E, A, B):
    # number of points of E in closed real interval [A,B] (A,B possibly outside [-1/2,1/2): wrap)
    def cnt(lo, hi):
        if hi < lo: return 0
        return bisect.bisect_right(E, hi) - bisect.bisect_left(E, lo)
    total = cnt(max(A, -HALF), min(B, HALF))
    if A < -HALF: total += cnt(A + 1, HALF)
    if B >= HALF: total += cnt(-HALF, B - 1)
    # the point 1/2 == -1/2 = E[0]: counted once via -HALF if B>=HALF wrap or A<=-1/2; guard double count
    if A <= -HALF and B >= HALF: total -= 1
    return total

def intervals_meeting(E, A, B):
    # indices i of intervals [E_i, E_{i+1}] (closure) meeting closed real interval [A,B], A,B in [-1/2,1/2]
    n = len(E)
    Ext = E + [HALF]
    i_lo = max(0, bisect.bisect_left(Ext, A) - 1)     # first i with E_{i+1} >= A
    i_hi = min(n-1, bisect.bisect_right(Ext, B) - 1)  # last i with E_i <= B
    return i_lo, i_hi

def check_neighbors(E, W):
    n = len(E); maxcnt = 0; minratio = None; viol = 0
    for i in range(n):
        w = W[i]; l = E[i]; r = E[i+1] if i+1 < n else HALF
        A, B = l - w, r + w
        c = count_closed(E, A, B)
        maxcnt = max(maxcnt, c)
        # closures meeting N(I): pieces of [A,B] reduced into [-1/2,1/2]
        pieces = []
        pieces.append((max(A, -HALF), min(B, HALF)))
        if A < -HALF: pieces.append((A + 1, HALF))
        if B > HALF: pieces.append((-HALF, B - 1))
        mn = None
        for (x, y) in pieces:
            i0, i1 = intervals_meeting(E, x, y)
            rng = range(i0, i1+1)
            cand = [W[j] for j in rng]
            mm = min(cand)
            mn = mm if mn is None else min(mn, mm)
        rt = mn / w
        if minratio is None or rt < minratio: minratio = rt
        if c > 49 or rt < mpf(1)/16: viol += 1
    return viol, maxcnt, minratio

def check_truncated(pr, E):
    eta, H, D = pr['eta'], pr['H'], pr['D']
    B = [x for x in E if rho(x) >= eta]
    B += [-HALF + eta, HALF - eta]
    B = sorted(set(B))
    L = 4*H; mx = 0
    for b in B:
        mx = max(mx, count_closed(B, b, b + L) if b + L < HALF else count_closed(B, b, b + L))
    return mx, 16004*D

def report(tag, pr, a, E, do_trunc=True):
    t0 = time.time()
    W = widths(E)
    okp, zero_ok, iz = check_partition(a, E)
    vw, lo, hi, maxw = check_width(pr, E, W)
    vn, maxcnt, minratio = check_neighbors(E, W)
    line = ("%s k=%d D=%d P=%d q=%d m=%d |V|=%d |V|/(k^3 log k)=%.3f | partition=%s 0 in [0,1/2-a_{m-1}):%s cut=E[0]=%s | "
            "width viol=%d ratio |I|/(H(rho+a)) in [%s, %s] (claim [1/4,2]) max|I|/2H=%s | neighbors viol=%d max#endpoints(N(I))=%d (claim<=49) min|J|/w=%s (claim>=1/16)"
            % (tag, pr['k'], pr['D'], pr['P'], pr['q'], len(a)-1, len(E), len(E)/(pr['k']**3*math.log(pr['k'])), okp, zero_ok, E[0] == -HALF,
               vw, mpmath.nstr(lo, 5), mpmath.nstr(hi, 5), mpmath.nstr(maxw/(2*pr['H']), 5), vn, maxcnt, mpmath.nstr(minratio, 5)))
    if do_trunc:
        mx, bound = check_truncated(pr, E)
        line += " | trunc max#breakpoints on 4H-arc=%d (claim<=%d)" % (mx, bound)
    print(line + "  [%.1fs]" % (time.time() - t0)); sys.stdout.flush()
    return vw, vn

print("== PAPER MESH (literal formulas) ==")
for k in [3, 4, 5, 7, 10, 16, 24, 32]:
    pr = params(k)
    th = pr['R']/pr['m']
    assert pr['alpha'] <= mpf(1)/4 and pr['R'] >= 1 and pr['H']/2 <= th <= pr['H']
    assert pr['k']**2*pr['R'] <= pr['m'] <= 2*pr['k']**2*pr['R'] and pr['R'] <= (pr['D']+1)*mpmath.log(pr['q'])
    a = paper_endpoints(pr); E = mesh_from_a(a)
    report("PAPER", pr, a, E)

print("\n== CONTROLS (each must report violations) ==")
for k in [10, 24]:
    pr = params(k)
    # C1 wrong growth rate
    m1 = int(mpmath.ceil(k*pr['R']))
    a1 = paper_endpoints(pr, m=m1); E1 = mesh_from_a(a1)
    report("C1 m'=ceil(kR)", pr, a1, E1, do_trunc=False)
    # C2 uniform mesh, same number of cells
    m = pr['m']; a2 = [mpf(l)/(2*m) for l in range(m+1)]; E2 = mesh_from_a(a2)
    report("C2 uniform    ", pr, a2, E2, do_trunc=False)
    # C3 merged cells
    a = paper_endpoints(pr); mid = m//2
    a3 = a[:mid] + a[mid+64:]
    E3 = mesh_from_a(a3)
    report("C3 merge-64   ", pr, a3, E3, do_trunc=False)
