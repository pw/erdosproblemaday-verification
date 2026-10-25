#!/usr/bin/env python3
"""Check 7: Section 8 arithmetic, recomputed independently.

(a) symbolic: exponent of r in a_r = r*sqrt(N^3/tau) from the stated parameter bounds
    B ~ r^30 (L = r^10, B in (100k^2L^3, 200k^2L^3]), h=B^k, q in (h^100, 2h^100], N=(hq)^10,
    tau = floor(B^(k-1)/2).  Recompute beta, alpha, eta with k symbolic.
(b) exact big-int values d=41, M=C(4d-1,d)=C(163,41), T=C(M,3), k=T^2+1; digits; log10 eta;
    log10 of Lean exponent 1/(100000k); confirm 1/(100000k) < 2/(45435k+16).
(c) numeric toy of the two-sided bound (8.6) constants for small k with exact integers.
Mutation controls: (i) a deliberately wrong beta (drop the -(k-1)/2 tau term) must FAIL the
    two-sided bound on the toy; (ii) the wrong comparison 1/(10000k) vs eta must come out the
    other way round for the real k (it does not -- printed honestly), and the claim
    'eta < 1/(100000k)' must be REJECTED.
"""
import sympy as sp
from math import comb, log10
from fractions import Fraction

print("=== (a) symbolic exponents ===")
k = sp.symbols('k', positive=True, integer=True)
# exponents of r (leading order) for each parameter
eB = 30                      # B ~ k^2 L^3, L=r^10
eh = eB * k                  # h = B^k
eq = 100 * eh                # q ~ h^100
eN = 10 * (eh + eq)          # N = (hq)^10
etau = eB * (k - 1)          # tau ~ B^(k-1)
ea = 1 + sp.Rational(3, 2) * eN - sp.Rational(1, 2) * etau
alpha = sp.expand(ea)
beta_paper = 1515 * k - (k - 1) / sp.Integer(2)
print("alpha (recomputed) =", alpha)
print("beta_paper =", sp.simplify(beta_paper), " = (3029k+1)/2 ?", sp.simplify(beta_paper - (3029 * k + 1) / sp.Integer(2)) == 0)
print("1+30*beta_paper =", sp.expand(1 + 30 * beta_paper), " matches alpha:", sp.expand(1 + 30 * beta_paper - alpha) == 0)
print("paper alpha 45435k+16 matches:", sp.expand(alpha - (45435 * k + 16)) == 0)
# beta as exponent of B in N^{3/2}/sqrt(tau): N^{3/2} = (hq)^15, hq ~ h^101 = B^{101k}
beta_re = sp.Rational(15) * 101 * k - (k - 1) / sp.Integer(2)
print("beta recomputed from (hq)^15/sqrt(tau):", sp.simplify(beta_re), " equal paper:", sp.simplify(beta_re - beta_paper) == 0)
# check the o(1) claims' exponents: second term of (8.2) bounded by (log)^2 (h/tau) r^(2-d), h/tau <= 3B = O(r^30)
d = 41
print("second-term exponent of r: 30 + 2 - d =", 30 + 2 - d, "(paper says r^-9):", 30 + 2 - d == -9)
# n_r^2 Delta >= r^2/64 : (a_r/2)^2 * tau/(16N^3) = r^2/64 exactly
r_, N_, tau_ = sp.symbols('r N tau', positive=True)
a_r = r_ * sp.sqrt(N_**3 / tau_)
print("(a_r/2)^2 * tau/(16 N^3) =", sp.simplify((a_r / 2)**2 * tau_ / (16 * N_**3)))

print("\n=== (b) exact integers ===")
d = 41
M = comb(4 * d - 1, d)
T = comb(M, 3)
kk = T * T + 1
print("M = C(163,41) has", len(str(M)), "digits; M =", M)
print("T = C(M,3) has", len(str(T)), "digits")
print("k = T^2+1 has", len(str(kk)), "digits")
alpha_v = 45435 * kk + 16
eta = Fraction(2, alpha_v)
lean = Fraction(1, 100000 * kk)
def flog10(fr):
    # log10 of a positive Fraction with huge num/den
    n, dd = fr.numerator, fr.denominator
    def l(x):
        s = str(x); return len(s) - 1 + log10(int(s[:15]) / 10**14)
    return l(n) - l(dd)
print("log10(eta) = %.6f" % flog10(eta))
print("log10(1/(100000k)) = %.6f" % flog10(lean))
print("eta / leanexp =", float(eta / lean), "(should be 200000k/(45435k+16) ~ 4.4019)")
print("CLAIM 1/(100000k) < 2/(45435k+16):", lean < eta)
print("MUTATION claim 2/(45435k+16) < 1/(100000k) (must be False):", eta < lean)
print("M check: C(163,41) via sympy binomial equal:", sp.binomial(163, 41) == M)
# T = C(M,3) = M(M-1)(M-2)/6 sanity
print("T == M(M-1)(M-2)/6:", T == M * (M - 1) * (M - 2) // 6 and (M * (M - 1) * (M - 2)) % 6 == 0)

print("\n=== (c) toy two-sided bound (8.6) with exact integers, small k ===")
from math import isqrt
def check_bounds(kv, r, Bv, qv, beta_num, beta_den):
    """Return (lower_ok, upper_ok) for sqrt2 r B^beta < a_r <= 2^15 sqrt3 r B^beta,
    using exact squared comparisons; beta = beta_num/beta_den (half-integer allowed)."""
    h = Bv**kv
    N = (h * qv)**10
    tau = Bv**(kv - 1) // 2
    # a_r^2 = r^2 N^3 / tau ; compare a_r^2 with 2 r^2 B^(2beta) and 2^30*3 r^2 B^(2beta)
    two_beta = Fraction(2 * beta_num, beta_den)
    assert two_beta.denominator == 1
    tb = int(two_beta)
    lhs_num = r * r * N**3          # a_r^2 = lhs_num / tau
    low = 2 * r * r * Bv**tb if tb >= 0 else None
    up = (2**30) * 3 * r * r * Bv**tb
    lower_ok = lhs_num > low * tau
    upper_ok = lhs_num <= up * tau
    return lower_ok, upper_ok

import random
random.seed(7)
allok = True; mutfail = 0; trials = 0
for kv in (2, 3, 4):
    for r in (101, 1009):
        L = r**10
        for trial in range(3):
            Bv = random.randint(100 * kv * kv * L**3 + 1, 200 * kv * kv * L**3)
            h = Bv**kv
            qv = random.randint(h**100 + 1, 2 * h**100)
            lo, upo = check_bounds(kv, r, Bv, qv, 3029 * kv + 1, 2)
            allok &= lo and upo
            # mutation: beta' = 1515k (forgets the tau factor) -> bounds must fail
            lo2, up2 = check_bounds(kv, r, Bv, qv, 1515 * kv, 1)
            if not (lo2 and up2):
                mutfail += 1
            trials += 1
print(f"paper beta=(3029k+1)/2: two-sided bound held in all {trials} toy instances: {allok}")
print(f"MUTATION beta=1515k: bound violated in {mutfail}/{trials} instances (must be {trials})")
