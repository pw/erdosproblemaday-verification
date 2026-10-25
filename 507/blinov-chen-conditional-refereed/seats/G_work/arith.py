"""Seat G: exact arithmetic for the geometric transfer (Blinov e29a291 patch, Chen 18 Oct 2026).

Every check is an assertion on exact integers / Fractions.  Run with MUTATE=<name> in argv to
replace one input by a wrong value; each mutation must make at least one assertion fail.
"""
import sys
from fractions import Fraction as F

MUT = sys.argv[1] if len(sys.argv) > 1 else None

k = 408781
if MUT == "k":
    k = 408782
d = 5
# ---------------- Blinov: exponent bookkeeping (patch 08-alteration) ----------------
beta = F(42) * k - F(k - 1, 2)          # (hq)^6 = h^42 (q ~ h^6), tau ~ B^{k-1}
if MUT == "beta":
    beta = F(42) * k - F(k, 2)
assert beta == F(83 * k + 1, 2), "beta"
rho = 249 * k + 3
if MUT == "rho":
    rho = 249 * k + 4
assert 6 * beta == rho, "6 beta == rho"
gamma = F(rho, rho + 1)
alpha = gamma + 6 * beta
assert alpha == rho + gamma
eta = 2 * gamma / alpha
assert eta == F(2, rho + 2), "eta = 2/(rho+2)"
assert eta == F(2, 249 * k + 5)
assert eta == F(1, 50893237), "eta = 1/50,893,237"
assert 2 * gamma - 2 == F(-2, rho + 1) and 2 * gamma - 2 < 0
# B interval: 100k^2 P < B <= 200k^2 P, P = 400 k^2 r^6
assert 100 * 400 == 40000 and 200 * 400 == 80000
# theta = B/M^2 <= 1/2 with M = 400 k^2 r^3:  80000 k^4 r^6 / (160000 k^4 r^6) = 1/2
assert F(80000, 400 ** 2) == F(1, 2)
# deletion exponents in r (B ~ r^6):
first_term_exp = gamma - 3 * (k - 1)            # r^gamma tau^{-1/2}
second_term_exp = 2 * gamma - 8 + 6              # r^{2gamma-8} * h/tau, h/tau <= 3B ~ r^6
third_term_exp = 2 * gamma - 10 + 6              # all-three-equal labels
assert first_term_exp < 0 and second_term_exp < 0 and third_term_exp < 0
# §7 losses with H = 2h, q > h^6, q^3/s <= 2000 q H^2 = 8000 q h^2
# (zero:equal-additional): h^2 q^-3 (q^3/s)^2 <= h^2 q^-3 (8000 q h^2)^2 = 8000^2 h^6/q
# exponents of h in the three losses must be <= 0 when q = h^6:
for num_h, q_pow in ((2 + 4, -1), (2 + 2, -1), (2 + 4, -2)):
    assert num_h + 6 * q_pow <= 0
# h >= 10 makes q > h^6 >= 2000 H^2 = 8000 h^2
assert 10 ** 6 >= 8000 * 10 ** 2
assert 9 ** 6 < 8000 * 9 ** 2  # (control: h = 9 would NOT suffice) -- boundary is real

# ---------------- Chen: s0, rho, eta, constants ----------------
s0 = 102195
if MUT == "s0":
    s0 = 102196
rhoC = 249 * k + 3 - 9 * s0
assert rhoC == 100866717, "rho_Chen"
gC = F(rhoC, rhoC + 1)
etaC = 2 * gC / (rhoC + gC)
assert etaC == F(2, rhoC + 2) == F(2, 100866719), "eta_Chen"
assert etaC > F(1, 50893237)
assert 100866719 < 2 * 50893237 == 101786474
assert 100 * rhoC == 10086671700, "c exponent"
assert rhoC + 1 == 100866718, "N0 exponent"
betaC = F(83 * k - 3 * s0 + 1, 2)
assert 6 * betaC == rhoC
assert 3 * s0 - k + 1 == -102195 == -s0, "Chen chose 4 s0 = k-1"
assert 4 * s0 == k - 1
# first term exponent in r: gamma + 6*(3 s0 - k + 1)/2
assert gC + 3 * (3 * s0 - k + 1) == gC - 306585
# delta = 2/(rho+1) > 2^-26
assert F(2, rhoC + 1) > F(1, 2 ** 26)
assert k < 2 ** 19 and 80000 * k ** 4 < 2 ** 93
assert 28 * 93 + 5 <= (701 - 28 * 6) * 5   # 5 + 28k(93+6x) < 701 k x for x >= log2(37) > 5.2
assert 701 * k < 2 ** 29
# denominators: 64 D0 C0^2 = 2^{6+20rho+2(21rho+1)} = 2^{62 rho + 8} < 2^{100 rho}
assert 6 + 20 * rhoC + 2 * (21 * rhoC + 1) == 62 * rhoC + 8 < 100 * rhoC
# hq | N needs s0 <= 3k
assert s0 <= 3 * k

# ---------------- Item 8: slack in Chen's s0 ----------------
# first term of (B17): 2^22 r^gamma B^{(3 s0 - k + 1)/2} with B > r^6: need 3(3 s0 - k + 1) + gamma < 0,
# and for the explicit 1/8 bound at r >= 37 a margin; the exponent condition is 3 s0 < k - 1.
smax = max(s for s in range(0, 3 * k + 1) if 3 * s < k - 1) if MUT != "smax" else (k - 1) // 3
assert smax == 136259, smax
assert 3 * (3 * smax - k + 1) + 1 < 0                 # works for every gamma < 1
assert not (3 * (3 * (smax + 1) - k + 1) + F(1, 2) < 0)  # s0 = 136260 fails (exponent = gamma > 0)
# explicit check of Chen's own inequality at s0 = smax, r >= 37:  2^22 r^{gamma-9} < 1/8  <=  r^{9-gamma} > 2^25
assert 37 ** 8 > 2 ** 25
rho_best = 249 * k + 3 - 9 * smax
eta_best = F(2, rho_best + 2)
assert rho_best + 2 == 246 * k + 17 == 100560143
assert eta_best > etaC

# ---------------- Item 8: coordinator ceiling (printed lemmas, N free) ----------------
# Work in exponents of r: log_r h = 6k, log_r tau = 6(k-1), log_r (hq) = 42k (q ~ h^6, B ~ r^6).
# x = log_r a_r, Y = 3 log_r N.  Constraints (strict, up to logs):
#   (i)  x + 6*42k - Y <= 0                (proportional pairs, Lemma sam:proportional as printed)
#   (ii) 2x + 6k - Y - 8 <= 0              (bad triples, E[D 1_J] ~ r^-8)
#   objective: eta = (2x + 6(k-1) - Y)/x   (n^2 Delta = a_r^2 tau / N^3)
def lp_sup(c1, kk=k):
    """max over x>0, Y of (2x + 6(kk-1) - Y)/x s.t. Y >= x + c1, Y >= 2x + 6kk - 8.  Vertex + brute check."""
    xv = c1 - 6 * kk + 8              # intersection of the two constraints
    Yv = xv + c1
    val = F(2 * xv + 6 * (kk - 1) - Yv, xv)
    # brute: sample x on both sides of the vertex; objective with the binding constraint
    for dx in (-5000, -17, -1, F(-1, 3), 0, F(1, 7), 1, 23, 10 ** 6):
        x = xv + dx
        if x <= 0:
            continue
        Y = max(x + c1, 2 * x + 6 * kk - 8)
        assert F(2 * x + 6 * (kk - 1) - Y, x) <= val
    return xv, val

xv, ceil = lp_sup(252 * k)
if MUT == "ceiling":
    ceil = F(2, 246 * k + 9)
assert xv == 246 * k + 8
assert ceil == F(2, 246 * k + 8) == F(1, 123 * k + 4) == F(1, 50280067), ceil
# Blinov (N=(hq)^4, Y = 3*168k) and Chen sit strictly below the ceiling
assert eta < ceil and etaC < ceil and eta_best < ceil
# Varying L3 = r^{1+mu} (mu >= 3 forced by theta <= 1/2): B ~ r^{3+mu}, triple saving r^{-(5+mu)}
for mu in range(3, 9):
    b = 3 + mu
    c = min(5 + mu, 10)
    # (i) Y >= x + 42 b k ; (ii) Y >= 2x + b k - c ; objective (2x + b(k-1) - Y)/x
    xv2 = 42 * b * k - b * k + c
    val2 = F(c - b, xv2)
    if mu == 3:
        assert val2 == ceil
    else:
        assert val2 < ceil

# ---------------- Item 8: sharper proportional-pair lemma (see report) ----------------
# Pr(pi(u)=pi(v)) <= M^{-k} * (2/s) * C (hq)^6 N^{-3}; log_r M^k = 3k, log_r s = 2*36k - 2*6k = 60k
c1_improved = 252 * k - 3 * k - 60 * k
xv3, ceil3 = lp_sup(c1_improved)
assert xv3 == 183 * k + 8 and ceil3 == F(2, 183 * k + 8) == F(2, 74806931)
assert ceil3 > ceil
# at that vertex N = r^{Y/3} must still exceed hq = r^{42k} and h
assert F(xv3 + c1_improved, 3) > 42 * k

print("ALL ASSERTIONS PASSED" + (f" (mutation {MUT} NOT detected!)" if MUT else ""))
print("Blinov eta =", eta, " Chen eta =", etaC, " best s0 =", smax, "-> eta =", eta_best)
print("coordinator ceiling =", ceil, "  with sharpened Lemma sam:proportional ->", ceil3)
