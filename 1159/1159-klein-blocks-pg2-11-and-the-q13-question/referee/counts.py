"""Referee: C1 (no blocking set with all intersections in {1,2,3} for q>=5) and C4 (21q-98) by sympy,
plus a brute-force cross-check of C1 over integer (s, n1, n2, n3) for small q."""
import sympy as sp
q, s, n1, n2, n3, n4 = sp.symbols('q s n1 n2 n3 n4')
v = q**2 + q + 1
sol = sp.solve([n1 + n2 + n3 - v, n1 + 2*n2 + 3*n3 - s*(q + 1), n2 + 3*n3 - s*(s - 1)/2], [n1, n2, n3], dict=True)[0]
t2 = sp.expand(sol[n2]); print("C1: n2 =", t2, "| entry formula matches:", sp.simplify(t2 - (-s**2 + (3*q + 4)*s - 3*v)) == 0)
disc = sp.expand(sp.discriminant(t2, s)); print("    discriminant in s:", disc, "| roots in q:", sp.solve(disc, q))
print("    disc<0 at q=5..12:", [int(disc.subs(q, k)) for k in range(2, 13)], "(q=2..12)")
print("    n1 =", sp.factor(sol[n1]), "; n3 =", sp.factor(sol[n3]))
# brute force: for q in 2..13, any nonnegative integer solution with s in [1, v]?
for Q in range(2, 14):
    V = Q*Q + Q + 1; feas = []
    for S in range(1, V + 1):
        N2 = -S*S + (3*Q + 4)*S - 3*V; N3 = sp.Rational(S*(S - 1), 2) - S*(Q + 1) + V
        N1 = V - N2 - N3
        if N1 >= 0 and N2 >= 0 and N3 >= 0: feas.append(S)
    print(f"    q={Q}: sizes s with nonneg real (n1,n2,n3) for type (1,2,3): {feas}")
# C4
m = sp.solve([n1 + 3*28 + 4*21 - 21*(q + 1)], [n1], dict=True)[0][n1]
met = sp.expand(m + 28 + 21)
print("C4: n1 =", m, "; lines met =", met, "; pair check 3*28+6*21 =", 3*28 + 6*21, "= C(21,2) =", 21*20//2)
print("    met = q^2+q+1  <=>", sp.factor(met - v), "=0 ->", sp.solve(met - v, q))
print("    at q=11:", met.subs(q, 11), "=", v.subs(q, 11), "; n1 at q=11:", m.subs(q, 11))
# is (n3, n4) = (28, 21) forced for a 21-set of type (0?,1,3,4) with n2 = 0?  pairs: 3 n3 + 6 n4 = 210 -> one free parameter
print("    NB pair count alone: 3 n3 + 6 n4 = 210 leaves (n3,n4) in", [(k, (210 - 3*k)//6) for k in range(0, 71) if (210 - 3*k) % 6 == 0])
# with blocking (n0 = 0): three equations determine (n1,n3,n4) for given q
sol4 = sp.solve([n1 + n3 + n4 - v, n1 + 3*n3 + 4*n4 - 21*(q + 1), 3*n3 + 6*n4 - 210], [n1, n3, n4], dict=True)[0]
print("    blocking 21-set of type (1,3,4):", {k: sp.factor(vv) for k, vv in sol4.items()})
for Q in range(2, 30):
    vals = {k: vv.subs(q, Q) for k, vv in sol4.items()}
    if all(x >= 0 and x == int(x) for x in vals.values()): print(f"      q={Q}: nonneg solution {vals}")
