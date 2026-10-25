# (i) explicit numerical constants / exponent inequalities in Sections 5-6, recomputed.
# Exact (sympy) where symbolic; random profiles for the case analyses (seeded).
import math, random, itertools
from sympy import symbols, Rational as R, simplify, sqrt, log, exp, limit, oo, nsimplify, Sum, expand
random.seed(1662)

print("== 5.1 thresholds (5.3): a_K = s^(1/10), a_i = 10 a_{i+1}; claims sum_{r>i} a_r < a_i/9, (5.4) exponent -a_i/2+sum_{r>i}a_r <= -7a_i/18 ==")
worst = -1
for K in range(1, 40):
    a = [10**(K-1-i) for i in range(K)]            # exact integers; a_K normalised to 1, a[0] largest
    for i in range(K):
        tail = sum(a[i+1:])
        assert 9*tail < a[i], (K, i)                # exact: sum_{r>i} a_r < a_i/9
        worst = max(worst, R(-a[i], 2*a[i]) + R(tail, a[i]))
print(f"  max over K<=39, i of (-a_i/2 + sum_(r>i) a_r)/a_i = {worst} = {float(worst):.6f}  vs claimed <= -7/18 = {-7/18:.6f}: {worst <= R(-7,18)}")
print("  exact: sum_{r>i} a_r / a_i -> sum_{m>=1} 10^-m = 1/9 (strict for finite K); 1/2 - 1/9 =", R(1,2)-R(1,9), "= 7/18")
print("  sum_i a_i = s^(1/10) (10^K - 1)/9 with K = O(1+sqrt(log s)): log_s of 10^K factor -> 0, so sum = s^(1/10+o(1)):")
for s in (1e2, 1e4, 1e8, 1e16, 1e32, 1e64):
    K = 1 + math.ceil(math.sqrt(math.log(s)))   # one admissible choice of K = O(1+sqrt(log s))
    tot = s**0.1 * (10**K - 1)/9
    print(f"    s={s:.0e}: K={K}, sum a_i = {tot:.3e}, log(sum)/log(s) = {math.log(tot)/math.log(s):.3f}, sum/s^(1/3) = {tot/s**(1/3):.3e}")
print("  NOTE: o(s^(1/3)) holds asymptotically, but sum/s^(1/3) < 1 only for astronomically large s with this K (between 1e32 and 1e64 above) -- harmless: only the limit is used, no rate is claimed.")

print("== (5.5) summability over dyadic widths 2^m u, u >= s_*: claims 2^(m/10) >= 1+cm (c = log2/10) and sqrt(log(2^m u)) <= sqrt(log u)+sqrt(m log 2) ==")
c = math.log(2)/10; bad = 0
for m in range(0, 400):
    if 2**(m/10) < 1 + c*m - 1e-12: bad += 1
    for u in (2.0, 10.0, 1e3, 1e9):
        if math.sqrt(math.log(2**m*u)) > math.sqrt(math.log(u)) + math.sqrt(m*math.log(2)) + 1e-12: bad += 1
print(f"  violations over m<400, u in {{2,10,1e3,1e9}}: {bad}")
for u in (1e2, 1e4, 1e6, 1e10, 1e20):
    S = sum((1+math.sqrt(math.log(2**m*u)))*math.exp(-(2**m*u)**0.1/2) for m in range(0, 400))
    S3 = sum(math.exp(-(2**m*u)**(1/3)) for m in range(0, 400))
    print(f"    u={u:.0e}: sum_m (1+sqrt(log 2^m u)) exp(-(2^m u)^(1/10)/2) = {S:.3e};  sum_m exp(-(2^m u)^(1/3)) = {S3:.3e}  (both -> 0 as u -> oo)")

print("== 5.1 lower boundary: N exp(-sqrt(2s)) / (N exp(-sqrt(s) - o(s^(1/3)))) = exp(-(sqrt2-1)sqrt(s)+o(s^(1/3))) ==")
s_ = symbols('s', positive=True)
print("  exponent difference -sqrt(2s)+sqrt(s) =", simplify(-sqrt(2*s_)+sqrt(s_)), "; coefficient sqrt2-1 =", float(sqrt(2)-1), "> 0, and s^(1/3) = o(sqrt s)")
print("== 5.1 core: on entry to the last width s_f in [s_*, 2 s_*], degree B exp((1+o(1)) s_f) <= B exp(3 s_*);  E L^2 = (delta N/A) B^2 exp(6 s_*) ==")
B_, N_, d_, delta, sst = symbols('B N d delta s_star', positive=True)
A_ = B_**2
print("  E*L^2 / N =", simplify((delta*N_/A_)*(B_*exp(3*sst))**2/N_), " -> 0 by the choice delta*exp(6 s_*) -> 0")
print("  width halving: batches <= exp(sqrt s); union degree exp(sqrt s)*O(B e^{s/2}) = B exp(s/2 + O(sqrt s)) = B exp((1+o(1)) s/2): relative error O(sqrt(s))/(s/2) -> 0")

print("== (5.6)-(5.7) profiles: sigma(b) = prod_i min(T,D_i) = e_j T^(d-j) on plateau j; b1+b2<0 from sum=0, b1<0<bd, d>=3 ==")
def rand_profile(d):
    while True:
        b = sorted(random.uniform(-1, 1) for _ in range(d - 1))
        last = -sum(b)
        if -1 <= last <= 1:
            b = sorted(b + [last])
            if max(abs(x) for x in b) >= 0.5 and abs(sum(b)) < 1e-12 and b[0] < 0 < b[-1]:
                return b
viol = 0; cnt = 0
for d in (3, 4, 5, 6):
    for _ in range(20000):
        b = rand_profile(d); cnt += 1
        if not (b[0] + b[1] < 0): viol += 1
        # sigma identity in log-scale (B = e^1, s = 1): log T = 1 + t, log D_i = 1 + b_i
        for j in range(d):
            lo = -1 if j == 0 else b[j-1]; hi = b[j] if j < d else 1
            if hi - lo < 1e-9: continue
            t = random.uniform(lo, hi)
            lhs = sum(min(1+t, 1+bi) for bi in b); rhs = sum(1+bi for bi in b[:j]) + (d-j)*(1+t)
            if abs(lhs-rhs) > 1e-9: viol += 1
print(f"  {cnt} random admissible profiles (d=3..6): violations of b1+b2<0 or of the sigma plateau identity: {viol}")
fig2 = [R(-8,10), R(-4,10), R(3,10), R(9,10)]
print("  Figure 2 profile (-0.8,-0.4,0.3,0.9): sum =", sum(fig2), ", b1+b2 =", fig2[0]+fig2[1], ", max|b| =", max(abs(x) for x in fig2))

print("== Prop 5.5: omitted nonreal-line fraction e_{d-1} exp(o(s))/n = exp(o(s))/D_d, D_d = B e^{b_d s} >= B since b_d > 0 ==")
print("  with s <= log B: exp(o(s))/B <= B^{-1+o(1)} -> 0  (exact: e_{d-1}/N = prod_{i<d} D_i / B^d = exp(s*sum_{i<d} b_i)/B = exp(-b_d s)/B)")

print("== (6.5)-(6.7) common window: initial interval rank T^(2d-1) vs sigma^2 * T/(D1 D2) with sigma = T^d and D1 D2 >= T^2 ==")
bad = 0
for d in (3, 4, 5):
    for _ in range(5000):
        b = rand_profile(d); t = random.uniform(-1, b[0])
        # log-scale with log B = 1/s normalisation: logs in units of s, B = e^{beta*s}; use beta = log B / s >= 1
        lhs = (2*d - 1)*t; rhs = 2*d*t + t - (b[0] + b[1])      # log(T^(2d-1)) vs log(sigma^2 T/(D1D2)) relative to B-powers (B-exponents cancel: (2d-1) vs 2d+1-2)
        if lhs < rhs - 1e-12: bad += 1
print(f"  violations of T^(2d-1) >= T^(2d+1)/(D1 D2) on t < b1 (5000 profiles x d=3..5): {bad}")
print("  k = d-1 plateau: D1^2 T^(2d-2) min(1, T/(D1 D2)) <= D1 T^(2d-2)  <=>  min(D1, T/D2) <= 1 (true as T <= D2): checked symbolically below")
D1, D2, T = symbols('D1 D2 T', positive=True)
print("   D1^2 T^(2d-2) * T/(D1 D2) / (D1 T^(2d-2)) =", simplify(D1**2*T/(D1*D2)/D1), " <= 1 iff T <= D2")
print("  (6.7) margins at T = D_d, sigma = N: log(A/D_d)/s = (log B)/s - b_d; log(A/(D1 D2))/s = -(b1+b2)")
for d in (3, 4, 5, 6):
    mins = []
    for _ in range(20000):
        b = rand_profile(d)
        for ratio in (1.0, 2.0, 4.0):         # (log B)/s : 1 = outermost, >= 2 otherwise (dyadic widths)
            m1 = ratio - b[-1]; m2 = -(b[0] + b[1])
            if ratio >= 2: mins.append(min(m1, m2))
    print(f"    d={d}: non-outermost windows, min over 20000 profiles of min(margin1, margin2) = {min(mins):.4f} (> 0 required; margin1 >= 1 always, margin2 = -(b1+b2) > 0)")
print("  outermost s = log B: margin1 = 1 - b_d, zero iff b_d = 1 (the Sec. 6.2 case)")

print("== (6.9) outermost endpoint: s = log B, b_d = 1, final open plateau of dim k after j = d-k cuts, cuts j+1..d at time 1 ==")
for d in range(3, 9):
    feas = []
    for k in range(0, d+1):
        j = d - k
        # need j values in [-1, 1) summing to -k (cuts at time 1 contribute k), and b1 + b2 < 0, plateau positive-dim (k >= 1)
        if k == 0: continue
        if j == 0: continue
        if -j <= -k < j: feas.append(k)   # sum of j values in [-1,1) can be -k iff -j <= -k < j
    print(f"  d={d}: feasible k = {feas}; paper's range 1 <= k < d-1 = {list(range(1, d-1))}; e_j = B^(d-2k) >= 1 forces k <= d/2: {[k for k in feas if 2*k <= d]}")
print("  identities: e_j * (B^2)^k = B^d  =>  e_j = B^(d-2k), N/e_j = B^(2k) = A^k")
print("== (6.10)-(6.11), Lemma 6.4 at the outermost endpoint ==")
print("  t0 > 1+b1+b2 is possible below 1 since b1+b2 < 0; normalized logs of T0/T_s(beta) and T0/(D1 D2): t0-beta and t0-(1+b1+b2):")
t0, beta, b1, b2 = symbols('t0 beta b1 b2', real=True)
Bs = symbols('Bs', positive=True)   # B = e^{s} at s = log B
print("    log(T0/(D1 D2))/s =", simplify((1 + t0) - (1 + b1) - (1 + b2)), "= t0 - (1+b1+b2)")
for d in (4, 5, 6, 7, 8):
    for k in range(2, d-1):
        print(f"    d={d}, k={k}: deletion mass exponent (d-2k)+(k+1) = {d-k+1} < d: {d-k+1 < d}", end=";")
    print()
print("  test degrees T_s(t2) = B^(1+t2) = B^(2-(1-t2)) with t2 < 1: c = (1-t2)/2 works after constants")
print("  Bezout direction count: C E B^(2-c+o(1))/n with E = delta N/A, n >= N sqrt(delta): =", simplify((delta*N_/B_**2)*B_**2/(N_*sqrt(delta))), "* B^(-c+o(1))")
print("  final row count: E M / n <=", simplify((delta*N_/B_**2)/(N_*sqrt(delta))), "* M  = sqrt(delta) M / A -> 0 (no rate needed)")
print("  lift degree: deg(gamma)deg(C->gamma) = deg C - mult_p C >= deg C/2 and sum deg(C->gamma) <= 1  =>  sum deg C <= 2 deg(gamma)")

print("== 6.3 (6.18)-(6.20) and the depth denominators ==")
print("  (6.19): groups of depth <= R e^{eta s}, t_p deg pi_p Y >= deg Y/2  =>  sum_Z deg Z >= a/(2R e^{eta s})")
print("  (6.20)/|P_x|: e_j B^(l+1)/N with e_j = B^j exp(s sum_{i<=j} b_i), l = d-j:")
for d in (3, 4, 5, 6):
    for j in range(1, d):
        l = d - j
        expo_B = j + (l + 1) - d
        print(f"    d={d} j={j}: B-exponent j+(l+1)-d = {expo_B} (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0", end="\n" if j == d-1 else ";")
for B in (1e6, 1e12, 1e30, 1e100):
    for frac in (0.05, 0.01):
        s = frac*math.log(B); q = B**0.5; r = math.ceil(B*math.exp(-2*s))
        print(f"    wider window: B={B:.0e}, s={frac}*log B: q=B^(1/2)={q:.3e}, r=ceil(B e^(-2s))={r:.3e}, q/r={q/r:.3e}, r >= ... B^{math.log(r)/math.log(B):.3f}")
print("  r - q - O(1) >= r/2 for large B since q = o(r) (q/r = B^(-1/2+o(1)))")
print("  multiplicity compression degree O(L^2/r) with L = B e^{O(s)}, r = B^(1+o(1)): = B e^{O(s)}")

print("== (6.26) strict margins on target plateaux (separated windows), all plateaux j=1..d-1 of random profiles ==")
fails = {}
for d in (3, 4, 5, 6, 7):
    for _ in range(20000):
        b = rand_profile(d)
        for j in range(1, d):           # plateau after j cuts, l = d - j, next cut b_{j+1} = b[j]
            l = d - j; bn = b[j]
            m1 = b[0] + bn                      # R = D1 (always)
            m2 = -sum(b[j+1:])                  # R = B exp(-s sum_{i>j} b_i) (narrower centres)
            m3 = bn - 2                         # R = B exp(-2s) (wider centres, b_{j+1} > 0, l < d-1)
            for side in ("narrow", "wide"):
                opts = [m1]
                if side == "narrow": opts.append(m2)
                if side == "wide" and bn > 0 and l < d - 1: opts.append(m3)
                best = min(opts)
                key = (d, side, "l=1,b_{j+1}>0" if (l == 1 and bn > 0) else "other")
                if best >= -1e-12:
                    fails.setdefault(key, 0); fails[key] += 1
for key in sorted(fails):
    print(f"  NO strict negative margin: d={key[0]} {key[1]:6s} case {key[2]:14s}: {fails[key]} plateau instances")
print("  (paper: the only zero-margin case is narrower centres, final one-dimensional plateau l = 1 with b_{j+1} = b_d > 0, handled in 6.5)")
print("  initial interval ratio A/T^2 = exp(-2 b s): positive margin near b1 < 0")
print("  (6.25)/(6.27) at the last endpoint: sigma T e^{cs}/A / (C E T) = sigma e^{cs}/(C delta N) >= e^{cs/2 - o(s)}/(C delta) >= delta^-1 e^{cs/3}")

print("== 6.5: identities on the final narrow curve plateau (j = d-1, R = B exp(-b_d s)) ==")
bd, s = symbols('b_d s', real=True)
Dd = B_*exp(bd*s); Rr = B_*exp(-bd*s); e_dm1 = B_**d_/Dd   # prod_{i<d} D_i = N/D_d with N = B^d (sum b = 0)
print("  R*D_d =", simplify(Rr*Dd), "= A ;  e_{d-1}/R =", simplify(e_dm1/Rr), "= N/A")
eta, eps = symbols('eta epsilon', positive=True)
print("  exceptional degree / projected degree: (delta (N/A) e^{-eta s}) / ((N/A) e^{-eps s}) =", simplify((delta*exp(-eta*s))/exp(-eps*s)), " -> 0 for 0 < eps < eta")
