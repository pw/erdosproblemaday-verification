# Elementary real inequalities used in Lemma mesh:width (02-setup.tex l.194-197) and the explicit k-thresholds of
# every "for large k" assumption made inside 02-setup.tex.
# (i)  e^t - 1 <= 2t  on [0,1]   (convexity: e^t - 1 <= (e-1) t on [0,1], and e - 1 < 2)
# (ii) 1 - e^{-t} >= t/2 on [0,1] (concavity: 1 - e^{-t} >= (1 - 1/e) t on [0,1], and 1 - 1/e > 1/2)
# CONTROLS (must FAIL): (i) at t = 1.3, (ii) at t = 1.6 -- the hypothesis t <= 1 (i.e. theta <= 1) is genuinely used.
import mpmath, math
mpmath.mp.dps = 40
N = 200000
g1 = min(2*mpmath.mpf(i)/N - mpmath.expm1(mpmath.mpf(i)/N) for i in range(0, N+1, 7)) 
g2 = min(-mpmath.expm1(-mpmath.mpf(i)/N) - mpmath.mpf(i)/(2*N) for i in range(0, N+1, 7))
print("min over grid of 2t-(e^t-1) on [0,1] =", mpmath.nstr(g1, 6), " | chord slope e-1 =", mpmath.nstr(mpmath.e - 1, 8), "< 2")
print("min over grid of (1-e^-t)-t/2 on [0,1] =", mpmath.nstr(g2, 6), " | chord slope 1-1/e =", mpmath.nstr(1 - 1/mpmath.e, 8), "> 1/2")
print("CONTROL t=1.3: e^t-1 <= 2t ?", mpmath.expm1(1.3) <= 2.6, "(e^1.3-1 = %s)" % mpmath.nstr(mpmath.expm1(1.3), 6))
print("CONTROL t=1.6: 1-e^-t >= t/2 ?", -mpmath.expm1(-1.6) >= 0.8, "(1-e^-1.6 = %s)" % mpmath.nstr(-mpmath.expm1(-1.6), 6))
# the largest t for which each holds (where the hypothesis really bites)
t1 = mpmath.findroot(lambda t: mpmath.expm1(t) - 2*t, 1.25); t2 = mpmath.findroot(lambda t: -mpmath.expm1(-t) - t/2, 1.6)
print("e^t-1<=2t holds exactly on [0, %s];  1-e^-t >= t/2 holds exactly on [0, %s]" % (mpmath.nstr(t1, 8), mpmath.nstr(t2, 8)))

def iroot_ceil(k, r):
    D = max(1, int(round(k ** (1.0/r))))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D
print("\nexplicit thresholds for the in-section 'large k' assumptions (checked k = 1..10^5 exactly; each is monotone after):")
conds = {
  "h0 < 2M < k (l.21)": lambda k: iroot_ceil(k,10)**2 < 2*iroot_ceil(k,2) < k,
  "H = k^-2 <= 1/8 (mesh:neighbors)": lambda k: 8 <= k*k,
  "4H < 1 and 3*(2H) < 1 (arcs)": lambda k: 4 < k*k and 6 < k*k,
  "alpha <= 1/4, R >= 1 given q >= P >= k+1 (mesh:width)": lambda k: (k+1)**2 >= 4 and (k+1)**2 >= 2*(math.e - 1) ,
  "prime lemma 4^(k^2)>(2k^2+1)(2k^2)^k [exact k<60 here; 3..400+tail in check_prime.py]": lambda k: 4**(k*k) > (2*k*k+1)*(2*k*k)**k if k < 60 else True,
  "h0 < k (so h0 < k < P, gcd(lambda,q)=1)": lambda k: iroot_ceil(k,10)**2 < k,
}
for name, f in conds.items():
    bad = [k for k in range(1, 10**5 + 1) if not f(k)]
    print("  %-58s fails for k in %s -> holds for all k >= %d" % (name, bad if len(bad) < 12 else str(bad[:12]) + "...", (max(bad) + 1) if bad else 1))
