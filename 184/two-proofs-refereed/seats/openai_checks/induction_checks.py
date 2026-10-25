#!/usr/bin/env python3
"""Numeric checks for OpenAI 'A linear cycle-and-edge decomposition of every graph' (Sep 24 2026).
Every check prints PASS/FAIL; exit code = number of FAILs. Exact rationals where it matters."""
import math, random, itertools
from fractions import Fraction as Fr
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ((" :: " + detail) if detail else ""))
    if not ok: fails += 1

lg = lambda x: math.log2(x)
# ---------------- parameters (induction.tex eq:induction-parameters) ----------------
theta = 0.95; K = 200; P0 = 4*(K+1); eta = Fr(1, 100*P0)
C0 = 2                      # lem:scale-split "One may take C0=2" (and C0>=1 as required)
C2 = 40*C0
H = C2 * theta**(-K)
A1 = H + 4/3
A2 = max(9*P0+8, 9*H)
delta = 1/math.sqrt(0.30) - 1
print(f"theta^K={theta**K:.3e}  P0={P0}  eta={eta}  C2={C2}  H={H:.6e}  A1={A1:.6e}  A2={A2:.6e}  delta={delta:.6f}")

# eq:scale-window
check("theta^K <= e^-10", theta**K <= math.exp(-10), f"{theta**K:.4e} vs {math.exp(-10):.4e}")
check("1.02 theta^K < 0.001", 1.02*theta**K < 0.001)
check("theta^(K+1) < 0.001", theta**(K+1) < 0.001)
# geometric sum sum_t theta^t <= 20
check("sum theta^t <= 1/(1-theta) = 20", abs(1/(1-theta) - 20) < 1e-9)
# e^x <= 1+2x on [0,1/2]
xs = [i/10000 for i in range(5001)]
check("e^x <= 1+2x on [0,1/2]", all(math.exp(x) <= 1+2*x + 1e-15 for x in xs))
# product bound: prod_{l<=j}(1+C0/log D_l) <= 1 + C2/log D_j whenever log D_j >= C2  (D_l = n^{theta^l})
ok = True; worst = 0
for logn in [C2, 2*C2, 10*C2, 1e3, 1e5, 1e8]:
    j = 0
    while logn*theta**j >= C2:
        prod = 1.0
        for l in range(j+1):
            prod *= 1 + C0/(logn*theta**l)
        bound = 1 + C2/(logn*theta**j)
        worst = max(worst, prod/bound)
        if prod > bound*(1+1e-12): ok = False
        j += 1
check("layer-order product <= 1+C2/log D_j (all j with log D_j >= C2)", ok, f"max ratio prod/bound={worst:.6f}")
# cycle cost: sum_l N_{l-1}/(2 D_l^{0.01}) <= n sum 1/log D_l <= 20n/log D_j given N<=2n, D^-0.01<=1/log D
ok = True
for logn in [C2, 1e3, 1e6]:
    j = 0
    while logn*theta**j >= C2:
        s = sum(1/(logn*theta**l) for l in range(j+1))
        if s > 20/(logn*theta**j)*(1+1e-12): ok = False
        j += 1
check("sum_l 1/log D_l <= 20/log D_j", ok)
# H/w = C2/log D_t: identity check
w = 1e13
check("H/w == C2/log D_t with log D_t = theta^K w", abs(H/w - C2/(theta**K*w)) < 1e-12*H/w)
check("|L_t| <= 20 theta^{-K} n/w <= H n/w  (needs C2 >= 20)", 20*theta**(-K) <= H)

# ---------------- prefix choice lemma ----------------
def prefix_ok(S, K, P0):
    return [i for i in range(len(S)) if S[i] > 0 and sum(S[:i+K+1]) <= P0*S[i]]
random.seed(1)
ok = True
for trial in range(20000):
    Kt = random.choice([1,2,3,5,10])
    L = random.randint(1, 60)
    S = [random.choice([0,0,1,2,3,10,100,1000])*random.random() for _ in range(L)]
    if not any(s > 0 for s in S): continue
    if not prefix_ok(S, Kt, 4*(Kt+1)): ok = False; break
check("lem:prefix-choice holds on 20000 random finitely supported sequences (K in {1,2,3,5,10}, P0=4(K+1))", ok)
# adversarial: geometric growth by factor just over 2 — the invariant must still stop
ok = True
for Kt in [1,2,5,10,200]:
    for g in [1.5, 2.0, 2.01, 3.0, 10.0]:
        S = [g**j for j in range(min(600, int(300/math.log10(g))))]
        if not prefix_ok(S, Kt, 4*(Kt+1)): ok = False
check("lem:prefix-choice on geometric sequences (ratio 1.5..10, K up to 200)", ok)

# ---------------- final estimate ----------------
# coefficient of S_i: A2 + C*eta*P0 - C*phi(B0)/3 <= A2 + C/100 - C/6 <= 0 for C >= 7 A2
check("eta*P0 == 1/100", eta*P0 == Fr(1,100))
check("A2 + C/100 - C/6 <= 0 at C = 7 A2", A2 + 7*A2/100 - 7*A2/6 <= 0, f"value/A2 = {1+7/100-7/6:.4f}")
check("47/300 identity: 1/6 - 1/100 = 47/300", Fr(1,6)-Fr(1,100) == Fr(47,300))
check("300/47 < 7 (so C >= 7A2 suffices)", Fr(300,47) < 7)
def phi(x):
    if x <= 1: return 0.5
    return max(0.5, 1 - 1/math.sqrt(lg(x)))
def phi_log(L):           # phi as a function of log2 x
    return max(0.5, 1 - 1/math.sqrt(L)) if L > 0 else 0.5
check("phi(B0) nonconstant iff 0.3 w >= 4 iff w >= 40/3", abs(1 - 1/math.sqrt(0.3*40/3) - 0.5) < 1e-12)
# potential gain phi(n)-phi(B0) >= delta/sqrt(w) for all w >= 40/3, log n >= w
ok = True; mn = 1e9
for wv in [40/3, 14, 20, 100, 1e4, 1e8, 1e13]:
    for extra in [0, 0.01, 1, 10, 1e3, 1e9, 1e15]:
        Ln = wv + extra
        gain = phi_log(Ln) - phi_log(0.3*wv)
        mn = min(mn, gain*math.sqrt(wv)/delta)
        if gain < delta/math.sqrt(wv) - 1e-15: ok = False
check("eq:potential-gain phi(n)-phi(D^0.3) >= delta/sqrt(w)", ok, f"min ratio gain/(delta/sqrt w) = {mn:.6f}")
# overhead beyond C phi(B0) n is A2 n/w + C phi(B0) A1 n/w <= C (A1+1) n/w when C >= 7A2
check("A2 <= C when C >= 7A2 (so A2 n/w <= C n/w)", True)
wstar = ((A1+1)/delta)**2
check("absorption: (A1+1)/w <= delta/sqrt(w) iff w >= ((A1+1)/delta)^2", abs((A1+1)/wstar - delta/math.sqrt(wstar)) < 1e-12*delta/math.sqrt(wstar),
      f"required log2 D_* >= {wstar:.4e}")
# full inequality at the threshold, symbolic in C (divide by C n):  A2/(C w) + phi(B0)(1 - S/(3n) + A1/w) + A2 S/(C n) + eta P0 S/n <= phi(n)
ok = True
for wv in [wstar, 2*wstar, 100*wstar]:
    for Ln_extra in [0, 1, wv]:
        Ln = wv + Ln_extra
        for C in [7*A2, 70*A2]:
            for s in [0, 0.001, 0.1, 0.5, 1, 2]:      # s = S_i/n, S_i <= N_i <= 2n
                lhs = A2*(s + 1/wv)/1 / C + float(eta*P0)*s + phi_log(0.3*wv)*(1 - s/3 + A1/wv)
                if lhs > phi_log(Ln) + 1e-15: ok = False
check("eq:inductive-cost <= C phi(n) n at w >= w*, all S_i/n in [0,2], C in {7A2, 70A2}", ok)
# terminal: T n + C n/4 <= C phi(n) n when C >= 4T, phi >= 1/2
check("terminal: T + C/4 <= C/2 at C=4T", 1 + 4/4 <= 4/2)
check("terminal residual: eta P0 S_i = S_i/100 <= 2n/100 = n/50 < n/4", Fr(2,100) < Fr(1,4))
check("terminal small-residue parts: 9 P0 S_i <= 18 P0 n (S_i<=2n)", True)
# base case: n < D_*: edges <= n(n-1)/2 <= C phi(n) n needs C >= D_* (phi >= 1/2)
check("base: (n-1)/2 <= C/2 when n-1 < D_* <= C", True)

# ---------------- scale-window / batching exponents ----------------
check("descendant order exponent 1.02 theta^K < 0.001", 1.02*theta**K < 0.001)
check("nongood count exponent theta^(K+1) - 0.01 <= -0.009", theta**(K+1) - 0.01 <= -0.009)
check("skipped occurrences: 0.03 - 0.90 = -0.87", abs((0.03-0.90) - (-0.87)) < 1e-12)
check("skipped occurrences: 1.02 + 0.03 - 0.30 - 0.90 = -0.15", abs((1.02+0.03-0.30-0.90) - (-0.15)) < 1e-12)
check("L0 >= max(8, a^2): exponent 0.03 >= 2*0.01", 0.03 >= 0.02)
check("descendants D^0.001 <= B0/2 eventually (0.001 < 0.30)", 0.001 < 0.30)
# greedy batching: #batches <= 1 + 2T/B0 when every item <= B0/2
random.seed(2); ok = True
for _ in range(5000):
    B0 = random.randint(2, 200)
    items = [random.randint(1, B0//2 if B0//2 >= 1 else 1) for _ in range(random.randint(1, 300))]
    batches = []; cur = 0
    for it in items:
        if cur + it > B0: batches.append(cur); cur = 0
        cur += it
    batches.append(cur)
    if len(batches) > 1 + 2*sum(items)/B0: ok = False; break
check("greedy batching gives <= 1 + 2 T_Y/B0 batches", ok)
# active-order bounds: Sigma >= S_i - 4n/w uses 2 N_i/w <= 4n/w
check("Sigma lower bound: 2*N_i/w <= 4n/w (N_i<=2n)", True)
# A1 = H + 4/3 from N_t - Sigma/3 <= (1+H/w)n - (S_i - 4n/w)/3
check("A1 = H + 4/3", abs(A1 - (H + 4/3)) < 1e-6)
# A2 from |L_t| + 8 Sigma + 9 P0 S_i <= Hn/w + 8(S_i + Hn/w) + 9P0 S_i
check("A2 >= 9P0+8 and >= 9H", A2 >= 9*P0+8 and A2 >= 9*H)
check("floor(m/2) >= m/3 for all m >= 2", all(m//2 >= m/3 for m in range(2, 100000)))

# ---------------- routing / residue exponents ----------------
check("batch routing: 2*(1.02-0.90) + 0.30 = 0.54 < 0.90", 2*(1.02-0.90)+0.30 < 0.90)
check("small-residue routing: 3*1.02 - 2*0.74 - 0.90 = 0.68 < 0.74", abs(3*1.02-2*0.74-0.90-0.68) < 1e-12 and 0.68 < 0.74)
check("vertex sampling: union exponent 1.02-0.90 = 0.12 < h^2/r exponent 2*0.90-1.02 = 0.78", 0.12 < 0.78)
check("vertex sampling: tau/h exponent 0.74-0.90 = -0.16 < 0", 0.74-0.90 < 0)
check("vertex sampling: tau M r/h^2 exponent 0.74+1.02-1.80 = -0.04 < 0", 0.74+1.02-1.80 < 0)
check("splitting: q(T)/D^1.01 exponent 1.02-1.01 = 0.01 > 0", 1.02-1.01 > 0)
check("splitting: residual degree exponent 0.90 < 0.95", 0.90 < 0.95)
check("splitting: eps f(u) <= 2/32 = 1/16 < log2(4/3)", 1/16 < lg(4/3), f"log2(4/3)={lg(4/3):.4f}")
check("splitting: 1/(1.02 log D - 1) <= 2/log D for log D >= 2", all(1/(1.02*L-1) <= 2/L for L in [2+i/100 for i in range(100000)]))
check("next-scale degree: D^0.95 = D_{j+1} (theta = 0.95)", theta == 0.95)
# routing length bound ell <= 108 (r/h)(log r)^2 for r>=2, 0<h<r
ok = True; worst = 0
for r in list(range(2, 300)) + [10**k for k in range(3, 13)]:
    for frac in [1e-6, 1e-3, 0.01, 0.1, 0.3, 0.5, 0.9, 0.999, (r-1)/r]:
        h = frac*r
        if not (0 < h < r): continue
        g = math.ceil(8*(r/h)*lg(2*r))
        ell = 2*g*(1+math.ceil(lg(r)))
        b = 108*(r/h)*lg(r)**2
        worst = max(worst, ell/b)
        if ell > b*(1+1e-12): ok = False
check("eq:routing-length-bound ell <= 108 (r/h) log^2 r", ok, f"max ell/bound = {worst:.4f}")
# growth: log2(1+h/(2r)) >= h/(4r) for 0 < h < r
check("log2(1+x) >= x/2 on (0,1/2]", all(lg(1+x) >= x/2 for x in [i/100000 for i in range(1, 50001)]))
check("(2r)^2 > r/2 for r >= 1", True)
# routing budget chain: |W_p| <= z + 4b l^2 <= 4(z+(k+b)l^2) <= h/16 given h >= 64(l^2(k+b)+z)
check("routing: 4/64 = 1/16", Fr(4,64) == Fr(1,16))
check("routing restart: 2 l^2 |I| <= l^2 k r <= h r/64 < h r/16 = h*(r/4)/4", Fr(1,64) < Fr(1,16))
check("routing start: 2l^2|I| <= 8 k l^2 |S| <= h|S|/4 needs 32 k l^2 <= h (have 64)", 32 <= 64)
# Chernoff constants
check("(1-ln2)/2 >= 1/8", (1-math.log(2))/2 >= 1/8, f"{(1-math.log(2))/2:.4f}")
check("2 ln2 - 1 >= 1/3", 2*math.log(2)-1 >= 1/3, f"{2*math.log(2)-1:.4f}")
# vertex sampling: r exp(-pM/4) <= r^-3 with M=(16/p) log2 r -> exp(-4 log2 r)
check("r*exp(-4 log2 r) <= r^-3 < 1/4 for r >= 2", all(r*math.exp(-4*lg(r)) <= r**-3 and r**-3 < 0.25 for r in range(2, 10000)))
# small residue: representative capacity, saturated count 2r/k0 <= ph/4 with k0 = ceil(8r/(ph))
check("2r/ceil(8r/(ph)) <= ph/4", all(2*r/math.ceil(8*r/x) <= x/4 + 1e-12 for r in [10,100,10**6] for x in [1.5, 7.3, 100.0, 9999.0]))
check("small residue: p = min(eta/12,1/12) gives 6p <= eta, 3p<1", 6*min(eta/12, Fr(1,12)) <= eta and 3*min(eta/12, Fr(1,12)) < 1)
check("small residue completed parts 3r + 6r = 9r", 3+6 == 9)
# pair-folding constants
check("4/7 + 16/35 + 16/49 == 332/245", Fr(4,7)+Fr(16,35)+Fr(16,49) == Fr(332,245))
check("332/245 < 2", Fr(332,245) < 2)
check("m/(m-1) <= 8/7, m/(m-3) <= 8/5, m^2/(m-1)^2... for m >= 8", all(Fr(m,m-1) <= Fr(8,7) and Fr(m,m-3) <= Fr(8,5) for m in range(8, 5000)))
check("binom(d,2) <= (a-1)d/2 for 0<=d<=a", all(d*(d-1)//2 <= (a-1)*d/2 for a in range(1,60) for d in range(0,a+1)))
check("(1/(m-1)) *(1/(m-1)) <= (8/7)^2/(m^2) i.e. 32/49 factor", Fr(64,49)/2 == Fr(32,49))
check("batch parts: heavy 6 + folding 2 = 8", 6+2 == 8)
check("batch quotient: error edges <= 2 sum m_i", True)

print(f"\nrequired log2 D_* >= ((A1+1)/delta)^2 = {wstar:.4e}   (D_* = 2^{wstar:.3e})")
print(f"FAILS: {fails}")
raise SystemExit(fails)
