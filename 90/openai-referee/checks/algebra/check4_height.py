# Lemma 8.2 toy check: for u a root of a monic u^m + a_{m-1}u^{m-1}+...+a_0 with rational a_r,
# h(u) <= sum_r h(a_r) + log m, with h = absolute logarithmic Weil height (Mahler-measure formula).
import sympy as sp, random, math
x = sp.symbols('x')
def h_rational(q):
    q = sp.Rational(q)
    return 0.0 if q == 0 else math.log(max(abs(q.p), abs(q.q)))
def h_alg_from_minpoly(P):           # P irreducible in Q[x]; h = log M(P_prim)/deg
    P = sp.Poly(P, x)
    _, Pp = P.clear_denoms(); Pp = Pp.primitive()[1]
    lead = abs(Pp.LC()); d = Pp.degree()
    roots = sp.Poly(Pp, x).nroots(n=30)
    return (math.log(lead) + sum((max(0.0, math.log(abs(complex(r)))) if abs(complex(r)) > 0 else 0.0) for r in roots)) / d
random.seed(1)
worst = -1e9; ntest = 0; viol_nolog = 0
for trial in range(60):
    m = random.randint(1, 5)
    coeffs = [sp.Rational(random.randint(-9, 9), random.randint(1, 6)) for _ in range(m)]   # a_0..a_{m-1}
    P = x**m + sum(coeffs[r]*x**r for r in range(m))
    rhs = sum(h_rational(a) for a in coeffs) + math.log(m)
    rhs_nolog = sum(h_rational(a) for a in coeffs)
    for fac, _ in sp.factor_list(P)[1]:
        hu = h_alg_from_minpoly(fac)
        ntest += 1
        worst = max(worst, hu - rhs)
        if hu > rhs_nolog + 1e-12: viol_nolog += 1
print("tests:", ntest, " max of h(u) - [sum h(a_r) + log m] =", round(worst, 6), "(must be <= 0)")
print("control: bound WITHOUT the log m term is violated in", viol_nolog, "tests")
golden = h_alg_from_minpoly(x**2 - x - 1)
print("control x^2-x-1: h(phi)=%.4f, sum h(a_r)=0, +log 2 = %.4f" % (golden, math.log(2)))
