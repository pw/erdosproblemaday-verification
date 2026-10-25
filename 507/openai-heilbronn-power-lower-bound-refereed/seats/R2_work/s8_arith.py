# Section 8 exponent bookkeeping, symbolic in k (and d), in log-scale.
import sympy as sp
k, d, r = sp.symbols('k d r', positive=True)
# log_r of the leading powers (ignoring k-dependent constants): B ~ r^30, h = B^k, q ~ h^100, N = (hq)^10, tau ~ B^(k-1)
lB = 30
lh = k*lB
lq = 100*lh
lN = 10*(lh + lq)
ltau = (k-1)*lB
la = 1 + sp.Rational(3, 2)*lN - ltau/2          # a_r = r*sqrt(N^3/tau)
beta = 1515*k - (k-1)/sp.Integer(2)
print("beta =", sp.simplify(beta), " == (3029k+1)/2 :", sp.simplify(beta - (3029*k+1)/sp.Integer(2)) == 0)
alpha = 1 + 30*beta
print("log_r a_r =", sp.expand(la), "; alpha = 1+30beta =", sp.expand(alpha), "; match:", sp.simplify(la - alpha) == 0)
print("alpha == 45435k+16 :", sp.simplify(alpha - (45435*k + 16)) == 0)
eta = 2/alpha
print("eta =", sp.simplify(eta))
# term 1: n_r (hq)^6 N^-3 <= r tau^(-1/2) (hq)^(-9)
t1 = la + 6*(lh+lq) - 3*lN
print("log_r term1 =", sp.expand(t1), "(should be 1 - ltau/2 - 9(lh+lq) <0 for k>=1)")
print("  check equals 1 - ltau/2 - 9*(lh+lq):", sp.simplify(t1 - (1 - ltau/2 - 9*(lh+lq))) == 0)
# term 2: n_r^2 (log)^2 h / (N^3 r^d) <= (log)^2 (h/tau) r^(2-d); h/tau <= 3B
t2 = 2*la + lh - 3*lN - d
print("log_r term2 (ignoring logs) =", sp.expand(t2), " -> negative iff d >", sp.solve(sp.Eq(t2, 0), d))
print("  at d=41:", sp.expand(t2.subs(d, 41)))
# a_r > r h^(29/2): log a_r - (1 + 29/2 lh) > 0 ?
print("log_r a_r - (1 + 29/2*lh) =", sp.expand(la - (1 + sp.Rational(29, 2)*lh)))
# numeric with the paper's actual k
M = sp.binomial(163, 41); T = sp.binomial(M, 3); K = T**2 + 1
print("M digits:", len(str(M)), " T digits:", len(str(T)), " k digits:", len(str(K)))
print("eta = 2/(45435k+16) ~ 10^-%d" % (len(str(45435*K+16))-1))
# exact constants A_k, D_k check on a sample: a_r bounds sqrt2 r B^beta < a_r <= 2^15 sqrt3 r B^beta
import math, random
def check_bounds(kk, trials=2000):
    bad = 0
    for _ in range(trials):
        Bv = sp.Integer(random.randrange(3, 10**4)) # any odd/even B >= 3
        h = Bv**kk
        q = h**100 + random.randrange(0, int(min(h**100, 10**30))) + 1   # in (h^100, 2h^100]
        N = (h*q)**10
        tau = sp.floor(Bv**(kk-1) / 2)
        a = sp.sqrt(N**3 / tau)   # divided by r
        lo = sp.sqrt(2) * Bv**sp.Rational(3029*kk+1, 2)
        hi = 2**15 * sp.sqrt(3) * Bv**sp.Rational(3029*kk+1, 2)
        if not (lo < a <= hi): bad += 1
    return bad
random.seed(3)
for kk in [2, 3]:
    print("k =", kk, ": a_r/r bound failures over random B,q:", check_bounds(kk, 200))
