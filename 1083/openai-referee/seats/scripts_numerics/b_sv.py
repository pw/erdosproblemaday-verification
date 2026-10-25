# (b) Solymosi-Vu recurrences, applied by hand.  Source read: refs/solymosi-vu/sv_combinatorica2008.pdf
# (Combinatorica 28 (1) (2008) 113-125, journal PDF, 13 pp; not on arXiv -- arXiv title/author searches return nothing),
# text: refs/solymosi-vu/sv.txt (pdftotext -layout).  Statements used (verbatim in the report):
#  Thm 2.1: t(A) = Omega(max(n/m^{(d-1)/d}, t_{d-1}(m))), m = max |A cap hyperplane|
#  Thm 2.2: t(A) = Omega(max(n^{(d+1)/2d}/m^{(d-1)/2d}, t_{d-2}(m))), m = max |A cap codim-2 flat|
#  Cor 2.3: t_{d-1}(n)=Omega(n^a) => t_d(n)=Omega(n^{d a/(d a + d-1)});  Cor 2.6: t_{d-2}(n)=Omega(n^a) => t_d(n)=Omega(n^{(d+1)a/(2 d a + d-1)})
#  Fact 2.5 / 2.8 closed forms; sec. 2: "All theorems and corollaries in this section hold ... if we replace t_d(n) by g_d(n)."
from sympy import Rational as R, Symbol, solve, nsolve, log as slog, simplify
import math
def c23(d, a): return d*a/(d*a + d - 1)
def c26(d, a): return (d+1)*a/(2*d*a + d - 1)
def f25(d, d0, a0): return R(2*d)/((d+d0+1)*(d-d0) + 2*d0/a0)
def f28(d, d0, a0): return R(2*(d+1))/((d+d0+2)*(d-d0) + 2*(d0+1)/a0)

print("== consistency of SV's own statements ==")
a2 = 0.8635
print("  Thm 1.1(a): Cor 2.3 at d=3 with Tardos a2=.8635:  3a2/(3a2+2) =", round(3*a2/(3*a2+2), 6), " (SV: .5643)")
for d in range(4, 11):
    e = 2*(d+1)/(d*d + 2*d - 8 + 6/a2) if d % 2 == 0 else 2*(d+1)/(d*d + 2*d - 15 + 8/0.5643)
    print(f"  Cor 1.3 d={d}: {e:.5f} > 2/d-2/(d(d+2)) = {2/d-2/(d*(d+2)):.5f}: {e > 2/d-2/(d*(d+2))}")
print("  Fact 2.8 with d0=2 equals Cor 1.3(3):", all(simplify(f28(d, 2, Symbol('a')) - 2*(d+1)/(d*d+2*d-8+6/Symbol('a'))) == 0 for d in (4, 6, 8)),
      "; with d0=3 equals Cor 1.3(4):", all(simplify(f28(d, 3, Symbol('a')) - 2*(d+1)/(d*d+2*d-15+8/Symbol('a'))) == 0 for d in (5, 7, 9)))

print("== (i) Guth-Katz g_2(m) >= c m/log m into Thm 2.1 at d=3 (the log form; Cor 2.3 needs a pure power) ==")
print("  pure-power shadow: Cor 2.3 with a=1 at d=3:", c23(3, R(1)))
print("  exact asymptotics: minimise max(n m^(-2/3), m/ln m) over m; the minimum is at the crossing n = m^(5/3)/ln m,")
print("  value V = m/ln m;  ln m ~ (3/5) ln n  =>  V ~ n^(3/5) ((3/5) ln n)^(-2/5) = (5/3)^(2/5) n^(3/5)/(ln n)^(2/5); (5/3)^(2/5) =", round((5/3)**0.4, 6))
for k in (6, 12, 24, 50, 100, 200, 300):
    lnn = k*math.log(10)
    # solve (5/3) ln m - ln ln m = ln n for x = ln m by Newton
    x = 0.6*lnn
    for _ in range(100):
        F = (5/3)*x - math.log(x) - lnn; x -= F/((5/3) - 1/x)
    lnV = x - math.log(x)
    ratio = math.exp(lnV - (0.6*lnn - 0.4*math.log(lnn)))
    print(f"    n=1e{k}: min max(...) / (n^(3/5)/(ln n)^(2/5)) = {ratio:.5f}")
print("  => Theta(n^(3/5)/(log n)^(2/5)): exponent 3/5, log power 2/5 (paper Sec. 1.1: Omega(n^{3/5}/(log n)^{2/5}) [21, Theorem 2.1])")

print("== (ii) Tidor-Yu-Zakharov g_3(n) >= n^{2/3-o(1)} ==")
a3 = R(2, 3)
print("  d=4 via Cor 2.3 (from d=3):", c23(4, a3), " (paper: 8/17)   [Fact 2.5 d0=3:", f25(4, 3, a3), "]")
print("  d=4 via Cor 2.6 (from d=2, Guth-Katz a=1):", c26(4, R(1)), "= ", float(c26(4, R(1))), "< 8/17")
print("  d=5 via Cor 2.6 (from d=3):", c26(5, a3), " (paper: 3/8)   [Fact 2.8 d0=3:", f28(5, 3, a3), "]")
print("  d=5 via Cor 2.3 (from d=4 = 8/17):", c23(5, c23(4, a3)), "=", float(c23(5, c23(4, a3))), "< 3/8")
eps = R(1, 10**6)
print("  o(1) bookkeeping: inputs 2/3-eps give d=4:", float(c23(4, a3-eps)), " d=5:", float(c26(5, a3-eps)), "(continuous in a; -> 8/17, 3/8)")
print("== general d: best of the two recurrences from (Guth-Katz a2 = 1-o(1), TYZ a3 = 2/3-o(1)) vs SV's general 2/d - 2/(d(d+2)) ==")
best = {2: R(1), 3: R(2, 3)}
for d in range(4, 11):
    cand = [c23(d, best[d-1]), c26(d, best[d-2])]
    best[d] = max(cand)
    closed = f28(d, 2, R(1)) if d % 2 == 0 else f28(d, 3, R(2, 3))
    sv = R(2, d) - R(2, d*(d+2))
    print(f"  d={d}: via Cor2.3 {cand[0]} ({float(cand[0]):.4f}), via Cor2.6 {cand[1]} ({float(cand[1]):.4f}); Fact 2.8 closed form {closed} ({float(closed):.4f}); 2/d-2/(d(d+2)) = {sv} ({float(sv):.4f}); 2/d = {float(R(2,d)):.4f}")
print("  identity 2/d - 2/(d(d+2)) = 2(d+1)/(d(d+2)):", simplify(R(2,1)/Symbol('d') - 2/(Symbol('d')*(Symbol('d')+2)) - 2*(Symbol('d')+1)/(Symbol('d')*(Symbol('d')+2))) == 0)
