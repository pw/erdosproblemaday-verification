# Exponent bookkeeping for Prop 2.4 / Lemma 2.7 of "A power saving for planar unit distances".
# Every quantity is t^{exponent}; exponents are linear in the small parameters
#   a  (a -> 0, a log t -> oo),  b = o(a) (b log t -> oo),  e = generic o(b) error  (e << b << a << 1).
# A claim "X <= Y" (or "X = o(Y)") holds asymptotically iff exp(X) - exp(Y) is eventually negative,
# i.e. iff its most dominant nonzero coefficient, in the order  1 >> a >> b >> e, is negative.
# ("eventually" uses a log t -> oo and b log t -> oo so t^{-c a}, t^{-c b} -> 0.)
import sympy as sp
a, b, e = sp.symbols('a b e', positive=True)
R = sp.Rational
gamma = R(27, 50); eta = gamma - R(1, 2)

def lead_sign(expr):
    expr = sp.expand(expr)
    poly = sp.Poly(expr, a, b, e)
    const = poly.coeff_monomial(1)
    if const != 0: return sp.sign(const), '1'
    for v in (a, b, e):
        c = poly.coeff_monomial(v)
        if c != 0: return sp.sign(c), str(v)
    # higher-order monomials only (e.g. a*b): check by substitution regime
    return 0, 'zero'

checks = []
def claim(name, lhs, rhs, strict=True, equality=False):
    d = sp.expand(lhs - rhs)
    s, by = lead_sign(d)
    if equality:
        ok = (d == 0)
    else:
        ok = (s < 0) if strict else (s <= 0)
    checks.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name}:  exp(LHS)-exp(RHS) = {d}   [sign {s} via {by}]")
    return ok

def run(gamma, eta, label):
    print(f"--- {label}: gamma={gamma}, eta={eta}")
    # e_err : any o(a) error; b chosen to dominate them; we model o(a) errors as +-e.
    s_exp = 1 - a + e          # s = O(t^{1-a} log t), log t = t^{o(a)}
    claim("deletion cost s*t^3 = o(t^{4-o(a)})", s_exp + 3, 4 - e)
    claim("pieces: s^2 + t^3/t^{1+2a} <= t^{2-2a+o(a)}", 2*s_exp, 2 - 2*a + 2*e, strict=False)
    claim("  second term t^{3-(1+2a)} equals t^{2-2a}", 3 - (1 + 2*a), 2 - 2*a, equality=True)
    e0_low = (4 - e) - (2 - 2*a + 2*e)
    claim("pigeonhole e0 >= t^{2+2a-o(a)}", 2 + 2*a - 3*e, e0_low, equality=True)
    claim("Szekely upper: (|P0||Q0|)^{2/3} = t^{2+2a}", R(2,3)*(1+2*a) + R(2,3)*(2+a), 2 + 2*a, equality=True)
    claim("  linear |Q0| = t^{2+a} below t^{2+2a}", 2 + a, 2 + 2*a)
    e0_up = 2 + 2*a + e
    claim("#points deg>t^{1+b} <= t^{1+2a-b/2}", e0_up - (1 + b), 1 + 2*a - b/2)
    claim("#centers deg>t^{a+b} <= t^{2+a-b/2}", e0_up - (a + b), 2 + a - b/2)
    mixed1 = R(2,3)*(1 + 2*a - b/2) + R(2,3)*(2 + a)
    mixed2 = R(2,3)*(1 + 2*a) + R(2,3)*(2 + a - b/2)
    claim("mixed term (excess points) = t^{2+2a-b/3}", mixed1, 2 + 2*a - b/3, equality=True)
    claim("mixed term (excess centers) = t^{2+2a-b/3}", mixed2, 2 + 2*a - b/3, equality=True)
    claim("mixed term o(e0)", 2 + 2*a - b/3 + e, 2 + 2*a - 3*e)
    claim("linear t^{2+a+o(b)} = o(e0)", 2 + a + e, 2 + 2*a - 3*e)
    claim("linear t^{1+2a+o(b)} = o(e0)", 1 + 2*a + e, 2 + 2*a - 3*e)
    claim("retained |P0| >= e/maxdeg = t^{1+2a-o(a)}  [encoded as t^{1+2a-2b} <= e0/t^{1+b}]", 1 + 2*a - 2*b, (2 + 2*a - 3*e) - (1 + b), strict=False)
    claim("retained |Q0| >= t^{2+a-o(a)}  [encoded as t^{2+a-2b} <= e0/t^{a+b}]", 2 + a - 2*b, (2 + 2*a - 3*e) - (a + b), strict=False)
    # (2.6) normalisations relative to |E0| = t^{2+2a}
    claim("(2.6) (|F||G|)^{2/3}/|E0| -> (uv)^{2/3} t^0", R(2,3)*(1+2*a) + R(2,3)*(2+a) - (2+2*a), 0, equality=True)
    claim("(2.6) |G|/|E0| -> t^{-a} v", (2 + a) - (2 + 2*a), -a, equality=True)
    claim("(2.6) |F|/|E0| -> t^{-1} u", (1 + 2*a) - (2 + 2*a), -1, equality=True)
    claim("(2.7) t^{-1/2} <= t^{-a/2}", -R(1,2), -a/2)
    # (2.8): second term exponent with UV >= t^{-a/4}
    claim("(2.8) 2nd term exponent -a/2 + eta*a/4 = -49a/100", -a/2 + eta*a/4, -R(49,100)*a, equality=(gamma==R(27,50)))
    claim("(2.8) 2nd term -> 0", -a/2 + eta*a/4 + e, 0)
    claim("(2.8) first-term power 2/3-gamma > 0  [UV<=t^{-ca} => T_t (UV)^{2/3-gamma} -> 0]", -(R(2,3) - gamma)*a + e, 0)
    claim("eta = gamma - 1/2 > 0 (needed for (2.5) to beat sqrt(uv))", -eta, 0)
    # infeasible subsets: uv <= tau/min(U,V) = t^{-a/8+o(a)}
    claim("xi_t: (uv)^{1/6} <= t^{-a/48+o(a)}", (-a/8 + e)/6, -a/48 + e, strict=False)
    claim("xi_t -> 0", -a/48 + e, 0)
    claim("2 t^{-a/2} <= t^{-a/48}", -a/2, -a/48)
    claim("tau = t^{-a/8} below U = t^{-o(a)} (single-vertex removal stays feasible)", -a/8, -e)
    # (2.3)
    claim("d(p) >= gamma|E|/|P| = t^{1+o(a)}", (2 + 2*a) - (1 + 2*a), 1, equality=True)
    claim("d(q) >= gamma|E|/|Q| = t^{a+o(a)}", (2 + 2*a) - (2 + a), a, equality=True)
    claim("max mu(p) = t^{-1-2a+o(a)}", (1) - (2 + 2*a), -1 - 2*a, equality=True)
    # Lemma 2.7
    claim("(2.16) 2/(|E| d_min) = t^{-2-3a}", -(2 + 2*a) - a, -2 - 3*a, equality=True)
    claim("(2.17) |Q|/|E| = t^{-a} -> 0", (2 + a) - (2 + 2*a) + e, 0)

run(gamma, eta, "paper's constants")
D_over_logt = 2*(1 + 2*a) - (2 + 3*a)   # leading part of D/log t, ignoring the (2+3a) t^{-a} diagonal term
print("Lemma 2.7: D/log t <= 2(1+2a) - (1 - t^{-a+o(a)})(2+3a) - o(a) =", sp.simplify(D_over_logt), "+ (2+3a) t^{-a+o(a)} + o(a)")
ok_all = all(c[1] for c in checks)
print("ALL PAPER CLAIMS PASS:", ok_all)

print("\n===== CONTROLS (must FAIL) =====")
checks.clear()
print("[control 1] gamma = 7/10 > 2/3: the 'first term -> 0' step of (2.8) must fail")
g2 = R(7,10); claim("(2.8) first-term power 2/3-gamma > 0", -(R(2,3) - g2)*a + e, 0)
print("[control 2] gamma = 1/2 (eta=0): expansion (2.5) gives nothing beyond sqrt(uv)")
claim("eta > 0", -(R(1,2)-R(1,2)), 0)
print("[control 3] no cutting (R = 1, i.e. a = 1 'balanced' piece |P|=|Q|=t^3, |E|=t^4, d(q)=t): D/log t bound")
Dbal = 2*3 - (4 + 1)
print("   balanced D/log t <=", Dbal, "-> not o(1):", 'FAIL (as expected)' if Dbal > 0 else 'unexpected')
print("[control 4] mis-claimed excess count t^{1+2a-2b} (Markov only gives t^{1+2a-b+o})")
claim("#points deg>t^{1+b} <= t^{1+2a-2b}", (2 + 2*a + e) - (1 + b), 1 + 2*a - 2*b)
print("[control 5] density deficit: configuration with t^{4-c} pairs, fixed c=1/10: d(q) exponent a - c stays negative as a->0")
c = R(1,10); claim("d(q) -> oo with deficit c", -(a - c), 0)
print("CONTROLS that passed (should be none):", [n for n,o in checks if o])
