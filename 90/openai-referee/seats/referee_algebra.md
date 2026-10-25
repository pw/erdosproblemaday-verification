# Referee report: seat "algebra" (Section 8, PDF pp. 42–51, plus brief item (vii))

Paper: OpenAI, "A power saving for planar unit distances", 23 Sep 2026. I read /tmp/oaimath/167/paper/paper.pdf, and every formula in scope was checked against the rendered PDF (pp. 42–51 read as images; p. 44 re-rendered at 300 dpi). paper.txt was used only for search.

STATUS: COMPLETE.

## 0. Headline: brief item (vii) is based on a text-extraction artifact. The paper uses the correct involution.

The brief says §8.2 writes the symmetry as "(z,w) ↦ (w,z)" and the circle condition as "v = u". That is what **paper.txt** says. The **PDF** says something else. Rendered at 300 dpi (crop saved as /tmp/oaimath/167/checks/algebra_render/p44_sym.png), p. 44 reads:

> "Each finite curve contains t_n^{1−o(1)} retained real points: divide the full edge count by the upper bound for the other vertex set. Its image under (z, w) ↦ (w̄, z̄) shares all these points. The bounded intersection fact forces the two curves to be equal on a large set. The limiting curve has the same symmetry. Neither coordinate projection is constant, since a curve with constant z would be a line z = c, whose symmetric image w = c̄ is a different line."

> "The symmetry gives v = ū, again an exact coordinatewise identity on a large set. Hence the finite loci there are the same real unit circle."

So the paper's map is (z,w) ↦ (w̄, z̄). That map fixes real points, and **v = ū** is exactly the real unit circle |p − u| = 1. pdftotext dropped the overlines: paper.txt contains **zero** combining-macron characters (`grep -c $'̄' paper.txt` → 0). **Warning for the coordinator: every other seat working from paper.txt loses every overline (complex conjugate) silently.**

I re-checked each use of the symmetry with the correct map B:(z,w) ↦ (w̄,z̄) and, for comparison, with the wrong map A:(z,w) ↦ (w,z) (check 3 below).
- **"its image shares all these points."** True for B: a real point has (z,w) = (x+iy, x−iy), and B sends it to (x+iy, x−iy), so it is fixed. False for A, which sends it to the point (x, −y). On the explicit circle (z−u)(w−ū) = 1 with u = 1+2i, all 12 sampled real points are B-fixed and 0 of 12 stay on the circle under A. The A-image meets the circle in only 2 points, so the Bézout step needs B, and the paper has B.
- **"symmetric image w = c̄ is a different line."** Holds under B. It would also hold under A, since w = c is a different line too.
- **(8.4) "v = ū."** The B-symmetry of (z−u)(w−v) = 1 forces v = ū (sympy: solution {v: conjugate(u)}). For real points, (z−u)(w−ū) = |p−u|², so this is the real unit circle of radius exactly 1, as the paper says. There is no second slip.
- **§8.4 "the symmetry of this curve shows that the other projection has degree one as well."** The B-image of {f = 0} is {f̄(w,z) = 0}, where f̄ conjugates the coefficients. Equality of the curves gives f̄(w,z) = c·f(z,w), so deg_z f = deg_w f. (Under A the same degree equality would also follow.)
- **Is the symmetric curve defined over B_0? Must B_0 be closed under conjugation?** Nothing in §8 needs it, and it holds automatically anyway. Normalise a_{j0k0} = 1 in f = Σ a_{jk} z^j w^k. Then ā_{jk} = c·a_{kj}. At (j0,k0) this gives c = 1/a_{k0j0} ∈ B_0, so every ā_{jk} ∈ B_0, and i ∈ B_0 gives ī = −i ∈ B_0. The exact definition of B_0 is used in only three places: countability (Lemma 8.3), containing the locus coefficients (generic evaluation, Lemma 8.6 "coefficient of w recovers −a"), and containing i (so that x = (z+w)/2 and y = (z−w)/(2i) lie in K_0 and M, and so that the direction vector v ∈ K_0²). All three hold.

**Verdict on (vii): no defect. The symmetry step is correct as printed.**

## 1. Objections (numbered)

**O1. COSMETIC (citation over-attribution).** §8.3, Lemma 8.4 proof, p. 46: "For an infinite algebraic extension, take the compatible extensions to its finite subextensions; uniqueness makes them agree on overlaps [7, Section 5]."
- Conrad §5 does not prove this. It says: "It is left to the reader to check for an infinite algebraic extension L/K that the conditions of Theorems 1.2 and 1.5 match Definition 5.1."
- The statement is true, and the paper's one-line argument is correct once one fact is added: for finite subextensions E ⊂ E′ of F/k_0(T), the extension to E′ maps E into E. This is Conrad Lemma 4.4: "every derivation F → L that sends K to K has values in F." Equivalently, for α ∈ E with minimal polynomial g, D(α) = −g^D(α)/g′(α) ∈ E.
- Type: exposition gap. Fix: cite Conrad Lemma 4.4 together with Thm 1.5/4.1.

**O2. COSMETIC (cross-reference labels).** §8 cites lemmas and propositions by the label "Theorem": "Theorem 4.2" (= Lemma 4.2), "Theorem 7.6" (= Prop 7.6), "Theorem 8.1/8.2/8.3/8.4/8.6" (= Prop 8.1 and Lemmas 8.2/8.3/8.4/8.6), "Theorem 4.4" (= Prop 4.4). Every one points at the intended result. Harmless.

**O3. COSMETIC (superfluous sentence).** §8.5, p. 50: "The line has nonconstant projections, as established above; in the form (8.13) its direction has nonzero squared length proportional to e ≠ 0."
- Nothing in the collinear-case argument uses the direction's squared length. Only v ≠ 0 and s_ℓ ≠ 0 are used, and the determinant 2(s_2R_1 − s_1R_2) does not involve v·v. Harmless.

**O4. COSMETIC (implicit step).** §8.2, p. 44: "The limiting curve has the same symmetry."
- What is meant is the coordinatewise identity f̄(w,z) = c_n f(z,w) on a large set, with c ∈ B_0 by the computation in §0.
- This is used only for the projection-degree statements and for (8.4), both of which also go through at the finite indices. Not a gap.

**O5. COSMETIC (constant bookkeeping, no effect).** §8.2 pruning: "both vertex sets have size t_n^{1+o(1)}".
- What (8.6) actually needs is the two-sided bound t^{1±o(1)}. The lower bound follows from the full edge count divided by the other side's size, which the paper says in the symmetry paragraph. Fine.

**I found no FATAL item and no mathematical GAP in §8.**

## 2. Status of each result in scope

| Item | Status |
|---|---|
| Prop 8.1 statement (hypotheses, quantifiers, "uniformly") | VERIFIED. (8.2) holds at every index for every edge; (8.3) is a sup over complete rectangles = o(J_n), which implies the u-sense o(J_n). Interface with Prop 7.6: c = 1/3 from (7.14); ω_t J with ω_t → 0 from (7.15); |P| = t^{1+2a+o(a)} = t^{1+o(1)}; t^{2−o(1)} edges; popular-circle deletion is verbatim. All match. |
| §8.1 ultraproduct | VERIFIED. F is a field by Łoś. F ⊂ U with F_n ⊂ C (coordinates are given as complex numbers). U is algebraically closed because a fixed-degree polynomial keeps its degree on a large set, so rootwise choice gives a root. Conjugation acts coordinatewise. Note that U is an ultraPRODUCT, not an ultralimit, so unbounded coefficient sequences cause no trouble. |
| Lemma 8.2 | VERIFIED LINE BY LINE. Nonarchimedean place: if \|u\|_v > max(1, max\|a_r\|_v), then \|u^m\| exceeds every \|a_r u^r\|, so the ultrametric inequality forbids the sum being 0. Archimedean place: if \|u\| > 1, then \|u\|^m ≤ Σ\|a_r\|\|u\|^r ≤ \|u\|^{m−1}Σ\|a_r\|, so \|u\| ≤ m·max(1, max\|a_r\|). Then log⁺\|u\|_v ≤ max_r log⁺\|a_r\|_v + [v arch]·log m ≤ Σ_r log⁺\|a_r\|_v + [v arch]·log m. Summing with total archimedean weight 1 (Lemma 4.1: ordinary modulus, weight 1/d_N per embedding) gives h(u) ≤ Σh(a_r) + log m. An element algebraic over k_0 has a fixed-degree monic relation, holding on a large set, so unbounded degree never arises. Field closure: h(−u) = h(u), Q ⊂ k_0, i ∈ k_0. "Edge ratio transcendental over k_0" follows from (8.2) plus relative algebraic closedness. χ ∈ k_0^× follows from (8.3) plus λ ≠ 0. |
| §8.2 standard facts | VERIFIED; citations MATCH (table below). Gauss's lemma as stated is correct: an irreducible polynomial of positive W-degree in K[Z][W] is primitive (else a factor in K[Z] splits off), hence irreducible over K(Z). |
| §8.2 loci, minimal total dimension, normalisation, B_0, irreducibility over U | VERIFIED. A minimum exists over {2,3,4}. A factorisation over U with fixed-degree factors transfers to a large set by Łoś. B_0 is countable. |
| §8.2 symmetry, nonconstant projections, (8.4), unit-circle exclusion | VERIFIED. See §0. Popular-circle contradiction: on a large set the finite loci coincide with one real circle of radius exactly 1, it contains ≥ t^{1−o(1)} > t^{9/10} points of P_n, and the full set of retained edges have both endpoints on it, contradicting the hypothesis. |
| §8.2 pruning | VERIFIED. Removing vertices of degree < e/(2v) deletes fewer than v·e/(2v) = e/2 edges. The minimum degree is then ≥ e/(2v) = t^{1−o(1)}. |
| Lemma 8.3 | VERIFIED LINE BY LINE (details in §3). |
| Function-field evaluation remark | VERIFIED. A common root z_0 of the w-coefficients would give (z−z_0) \| f over U. Then z is transcendental; f is irreducible over B(z) by Gauss; the kernel of B[z,w] → U is (f); evaluation embeds B(V). |
| §8.3 definitions, (8.8) | VERIFIED (symbolic identity). χ_{iℓ} is the rectangle product for (p_i, p_1; r_ℓ, r_1); for i = 1 or ℓ = 1 it equals 1 ∈ k_0. |
| Lemma 8.4 | VERIFIED. Citation partially over-attributed (O1). The linear-forms argument: the form for edge e′ has coefficient ∂_{e′}λ_{e′} ≠ 0 on c_{e′}, so it is nonzero; a product of 100 nonzero forms is a nonzero polynomial over the infinite field F. |
| (8.9)–(8.11) | VERIFIED by sympy (check 1). The identity holds as an identity of rational functions, not only on the variety. It needs ∂i = 0 (true: 2i∂i = ∂(−1) = 0) and ∂χ = 0. The control with ∂χ ≠ 0 leaves the residual dchi(χg−h)(χg+h)/(χ²gh). |
| K_0 | VERIFIED. The algebraic closure in U of a subfield is algebraically closed because U is. ∂ is never applied to K_0, B_0 or U \ F. |
| Lemma 8.5 | VERIFIED LINE BY LINE. trdeg_{B0(r)} B0(r,p) = Nd_1 by (8.5). Adjoining 3j elements (U_ℓ: 2 each, A′_ℓ: 1 each) drops trdeg by at most 3j, and algebraic closure does not change it, giving (8.12). Each p_i has trdeg ≤ d_1 over K_0 (on a curve, w is algebraic over K_0(z) since f(z_0,W) ≢ 0 by irreducibility over U). Subadditivity then gives a contradiction because N d_1 − 3j > N(d_1−1) ⇔ N > 3j: 20 > 15. Correlation of A′_ℓ with p_1 (h_ℓ involves λ_{1ℓ}) is allowed by the count. If i = 1 survives, A_1 − A′_ℓ = ∂λ_{1ℓ}/λ_{1ℓ} ≠ 0. |
| §8.4 Lemma 8.6, plane case | VERIFIED. Q_ℓ is linear in w and primitive: gcd(z−a, −(z−a)w_r − 4) = gcd(z−a, −4) = 1. The Q_ℓ are monic in zw and pairwise non-associate (the z and w coefficients recover the centre). Q_ℓ ∤ L_m since L_m is reducible. So v_{Q_ℓ}(D_ℓ) = 0+1 and v_{Q_ℓ}(D_m) = 0+0. |
| Lemma 8.6, curve case (V_2 ≠ V_1, or projection degree ≥ 2) | VERIFIED. a transcendental over B_0. Leading coefficient ≠ 0 at a. Simple roots via αf + βf_w = δ(z) ≠ 0 at a. r_ℓ ∉ V_1 when V_2 ≠ V_1 (generic evaluation gives f_2 \| f). b ∈ K_0. r_m stays generic over B_0(s_ℓ) ⊂ alg. closure of B_0(r_ℓ). Coordinates differ, since w_{r_m} = b would force V_2 = {w = b}, excluded. L_m(s_ℓ) ≠ 4, since otherwise f_2 ∝ (z−a)(w−b) − 4 and the w-coefficient puts a in B_0. Hensel in K_0[[T]] with f_w(a,b) ≠ 0. Kernel (f), so K_0(V_1) ↪ K_0((T)). Orders: L_ℓ has order 1, the rest order 0. |
| Lemma 8.6, same curve of projection degree one | VERIFIED. Classification azw + cz + dw + e_0: a = 0 gives a line with c, d ≠ 0; a ≠ 0 gives (8.14) with nonzero constant. b ≠ 1 by (8.4). Line case L_ℓ = e(z−a_ℓ)² (sympy). (8.15), the quadratic, discriminant 16(1−b), nonzero roots (product 1), and the squared-distance formula all checked in sympy (check 2). Non-coincidence: L_m(s_ℓ) ∈ {0,4} would make a_m algebraic over B_0(s_ℓ), contradicting genericity. Poles: only at z = u, and z_{s_ℓ} ≠ u. |
| Exhaustiveness of the three cases | VERIFIED. V_1 plane / V_1 curve with V_2 ≠ V_1 / V_1 = V_2 with deg_w ≥ 2 / V_1 = V_2 with deg_w = 1. These cover everything. |
| Remark b = 1 | VERIFIED. L(L−4) = ((ζ²−1)/ζ)² (sympy), so the radicand is a square on a common unit circle; this is exactly why the popular-circle deletion is needed. |
| §8.5 Kummer | VERIFIED; citation MATCHES (table below). Independence of square classes in M from Lemma 8.6; μ_2 ⊂ M, char 0. |
| §8.5 rank-two Cramer / R_4 flip | VERIFIED LINE BY LINE. det = −4(R_1m_23 − R_2m_13 + R_3m_12), where m_ab are the 2×2 minors of the position rows (sympy). Single radicals are independent over M: from Σc_ℓR_ℓ = 0, flipping R_1 gives 2c_1R_1 = 0, and R_1 ≠ 0 since v(D_1) = 1. Cramer puts (H_x,H_y,A) in M(R_1,R_2,R_3), which σ_4 fixes. Applying σ_4 to the 4th equation and subtracting gives 2R_4(A − A′_4) = 0, so A = A′_4, contradicting (8.11). Needs j ≥ 4; j = 5. |
| §8.5 rank failure / collinear case | VERIFIED. Anchors are non-collinear unless V_2 is a line (generic evaluation). If V_2 is a line, rank < 2 only if p is on it, which needs V_1 = V_2 = that line. Collinear determinant 2(s_2R_1 − s_1R_2) (sympy), nonzero by radical independence. Flip R_3 to conclude. |
| Proof of Thm 1.1 (assembly) | VERIFIED. Sequence reduction (§2 opening): failure at exponent 4/3 − 1/j with C large gives n ≥ j and 2u(n) ≥ u(n) > n^{4/3−1/j} = t^{4−3/j}. Ordered vs unordered changes the constant only. Dichotomy on S. The interfaces Prop 4.4 / Prop 7.6 → Prop 8.1 match as stated. (The correctness of Props 4.4 and 7.6 is outside this seat.) |

## 3. Lemma 8.3 in detail (brief item vii, second half)

**Uniform avoidance from minimality.** Suppose it fails at degree D. Then for every b > 0 the set {n : some degree-≤D polynomial has > t^{1−b} zeros among the pruned vertices} is large. Take a maximiser at each n; its zero count is t^{1−o(1)} along u. Some irreducible factor (at most D of them, degree ≤ D, fixed on a large set by partition) contains ≥ (zeros)/D = t^{1−o(1)} pruned vertices. Each has pruned degree ≥ e/(2v) = t^{1−o(1)}, so the pair (that curve, other locus) retains ≥ t^{2−o(1)} edges of the original graph. It is a legitimate locus sequence: irreducible, degree ≤ D fixed. Its total dimension is one less, contradicting the minimal choice.

**Brief's question** ("is 'restricting this side to a bounded-degree curve' with min degree t^{1−o(1)} really a full-count locus pair of smaller total dimension?"): yes, exactly as above.

**Curve side.** Distinct real points have distinct z = x+iy, so a nonzero polynomial in z of degree ≤ D has ≤ D vertex zeros.

**(8.6).** X = (1/n′)Σ_r Π_i 1{p_i ~ r}. Then EX = (1/n′)Σ_r (d(r)/m)^N ≥ δ^N (power mean). EX^j ≥ (EX)^j. The number of ordered complete grids is m^N(n′)^j E X^j ≥ t^{N+j−o(1)}, since δ ≥ t^{−o(1)} and m, n′ ≥ t^{1−o(1)}.

**(8.7) induction.**
- Write T = Σ_α c_α(earlier) X_last^α and pick c_α ≠ 0 over B_0. Its representatives are nonzero on a large set.
- Bad tuples are bounded by (zeros of c_α among earlier tuples) · t^{1+o(1)} plus (all earlier tuples) · (t^{1−b_D} or D).
- The uniform plane estimate is explicitly for coefficients depending on n and on the earlier tuple, so moving coefficients are legitimate.
- Saving: min(b′, b_D) − o(1).

**Diagonal choice.** B_0 is countable, so there are countably many tests. For fixed s, a finite union bound gives t^{N+j−min b} ≪ t^{N+j−o(1)}, so the first s tests are feasible on a large set. With s_n the largest feasible prefix ≤ n, we get s_n ≥ s on {n ≥ s} ∩ {feasible}, which is large. Hence every fixed test is nonzero in U at the limiting grid. Only finite intersections of large sets are used.

## 4. Finite checks (all run with ~/.venv/bin/python -I, nice -n 19; scripts in /tmp/oaimath/167/checks/algebra/)

### Check 1: (8.9)–(8.10) by an abstract derivation (z = x+iy, w = x−iy, ∂i = 0, ∂χ = 0)
```python
import sympy as sp
xp,yp,xr,yr,g,h,chi = sp.symbols('xp yp xr yr g h chi', nonzero=True)
Hx,Hy,Ux,Uy,A,Ap,dchi = sp.symbols('Hx Hy Ux Uy A Ap dchi')
I = sp.I
base = [xp,yp,xr,yr,g,h,chi]
def D(expr, dchi_val=0):
    rules = {xp:Hx, yp:Hy, xr:Ux, yr:Uy, g:A*g, h:Ap*h, chi:dchi_val}
    return sum(sp.diff(expr, v)*rules[v] for v in base)   # D(i)=0: I is a constant
zp, wp = xp+I*yp, xp-I*yp
zr, wr = xr+I*yr, xr-I*yr
lam = g/h*chi                       # (8.8)
L = (zp-zr)*(wp-wr)                 # L_l(p_i)
R = 1/lam - lam                     # R_il
F = L - (2 - lam - 1/lam)
dF = sp.simplify(sp.expand(D(F)))
claim = 2*((xp-xr)*(Hx-Ux) + (yp-yr)*(Hy-Uy)) - R*(A-Ap)   # (8.9) as LHS-RHS
print("D(8.1) - [(8.9) LHS-RHS] =", sp.simplify(dF - claim))
bad = 2*((xp-xr)*(Hx-Ux) + (yp-yr)*(Hy-Uy)) - R*(A+Ap)
print("control (A+A'):", sp.simplify(dF - bad))
dF2 = sp.expand(D(F, dchi))
print("control (D chi != 0): residual =", sp.factor(sp.simplify(dF2 - claim)))
lamS = sp.symbols('lamS', nonzero=True)
LS = 2 - lamS - 1/lamS
RS = 1/lamS - lamS
print("(8.10) R^2 - L(L-4) =", sp.simplify(RS**2 - LS*(LS-4)))
print("control: R^2 - L(L+4) =", sp.simplify(RS**2 - LS*(LS+4)))
print("L - [(dx)^2+(dy)^2] =", sp.expand(L - ((xp-xr)**2+(yp-yr)**2)))
```
Output:
```
D(8.1) - [(8.9) LHS-RHS] = 0
control (A+A'): -2*Ap*chi*g/h + 2*Ap*h/(chi*g)
control (D chi != 0): residual = dchi*(chi*g - h)*(chi*g + h)/(chi**2*g*h)
(8.10) R^2 - L(L-4) = 0
control: R^2 - L(L+4) = 8*lamS - 16 + 8/lamS
L - [(dx)^2+(dy)^2] = 0
```
Confirms 2(p−r)·(H−U) = R(A−A′) and R² = L(L−4). The controls fail: a wrong sign, a non-constant χ, and a wrong (8.10).

### Check 2: §8.5 determinant, collinear determinant, (8.15), discriminant, b = 1, squared distance, line case
```python
import sympy as sp
px,py = sp.symbols('px py')
rx = sp.symbols('rx1:4'); ry = sp.symbols('ry1:4'); R = sp.symbols('R1:4')
Mx = sp.Matrix([[2*(px-rx[l]), 2*(py-ry[l]), -R[l]] for l in range(3)])
det = sp.expand(Mx.det())
m = lambda a,b: (px-rx[a])*(py-ry[b]) - (py-ry[a])*(px-rx[b])
pred = -4*(R[0]*m(1,2) - R[1]*m(0,2) + R[2]*m(0,1))
print("det - (-4)(R1 m23 - R2 m13 + R3 m12) =", sp.expand(det - pred))
print("control (wrong sign on R2 term):", sp.expand(det - (-4)*(R[0]*m(1,2) + R[1]*m(0,2) + R[2]*m(0,1))) != 0)
s1,s2 = sp.symbols('s1 s2'); 
print("collinear det =", sp.factor(sp.Matrix([[2*s1,-R[0]],[2*s2,-R[1]]]).det()), " (paper: 2(s2 R1 - s1 R2))")
z,u,v,b,a,zeta,am = sp.symbols('z u v b a zeta a_m')
w_of = lambda zz: v + b/(zz-u)
L = (z-a)*(w_of(z)-w_of(a))
L_zeta = sp.simplify(L.subs(z, u + zeta*(a-u)))
print("L_l in zeta:", sp.factor(L_zeta), "| minus paper's -b(zeta-1)^2/zeta:", sp.simplify(L_zeta + b*(zeta-1)**2/zeta))
num = sp.numer(sp.together(L_zeta - 4))
print("numerator of L-4 (up to sign):", sp.factor(num), "| paper: b z^2+(4-2b)z+b ->", sp.expand(-num - (b*zeta**2+(4-2*b)*zeta+b)))
print("discriminant:", sp.factor(sp.discriminant(b*zeta**2+(4-2*b)*zeta+b, zeta)))
print("control discriminant of b z^2+(4+2b)z+b:", sp.factor(sp.discriminant(b*zeta**2+(4+2*b)*zeta+b, zeta)))
Lb1 = L_zeta.subs(b,1)
print("b=1: L(L-4) - ((zeta^2-1)/zeta)^2 =", sp.simplify(Lb1*(Lb1-4) - ((zeta**2-1)/zeta)**2))
print("b=2: is L(L-4) a square in Q(zeta)?  sqf:", sp.factor(sp.together(L_zeta.subs(b,2)*(L_zeta.subs(b,2)-4))))
zs = sp.symbols('z_s')
Lm = (zs-am)*(w_of(zs)-w_of(am))
print("L_m(s_l) - paper formula:", sp.simplify(Lm - (-b*(zs-am)**2/((zs-u)*(am-u)))))
e,ep,al = sp.symbols('e ep a_l')
Lline = (z-al)*((e*z+ep)-(e*al+ep))
print("line case L_l - e(z-a_l)^2 =", sp.expand(Lline - e*(z-al)**2))
```
Output:
```
det - (-4)(R1 m23 - R2 m13 + R3 m12) = 0
control (wrong sign on R2 term): True
collinear det = -2*(-R1*s2 + R2*s1)  (paper: 2(s2 R1 - s1 R2))
L_l in zeta: -b*(zeta - 1)**2/zeta | minus paper's -b(zeta-1)^2/zeta: 0
numerator of L-4 (up to sign): -b*zeta**2 + 2*b*zeta - b - 4*zeta | paper: b z^2+(4-2b)z+b -> 0
discriminant: -16*(b - 1)
control discriminant of b z^2+(4+2b)z+b: 16*(b + 1)
b=1: L(L-4) - ((zeta^2-1)/zeta)^2 = 0
b=2: is L(L-4) a square in Q(zeta)?  sqf: 4*(zeta - 1)**2*(zeta**2 + 1)/zeta**2
L_m(s_l) - paper formula: 0
line case L_l - e(z-a_l)^2 = 0
```
Every claimed formula matches. The control discriminant differs. With b = 2, L(L−4) is a non-square (the ζ²+1 factor appears once).

### Check 3: symmetric curve under both involutions on (z−u)(w−ū) = 1, u = 1+2i ∉ R; toy Kummer independence with a failing control
```python
import sympy as sp
z,w,X = sp.symbols('z w X')
u = 1 + 2*sp.I
ubar = sp.conjugate(u)
f = sp.expand((z-u)*(w-ubar) - 1)
fbar = lambda P: sp.expand(sp.conjugate(P).subs({sp.conjugate(z):z, sp.conjugate(w):w}))
imgA = sp.expand(f.subs({z:w, w:z}, simultaneous=True))
imgB = sp.expand(fbar(f).subs({z:w, w:z}, simultaneous=True))
print("eq of image under A:", imgA, "| equals f?", sp.expand(imgA - f) == 0)
print("eq of image under B:", imgB, "| equals f?", sp.expand(imgB - f) == 0)
ok_A = ok_B = 0
for k in range(12):
    th = sp.Rational(k,12)*2*sp.pi
    x, y = 1+sp.cos(th), 2+sp.sin(th)
    zp, wp = x+sp.I*y, x-sp.I*y
    assert sp.simplify(f.subs({z:zp, w:wp})) == 0
    zA, wA = wp, zp
    zB, wB = sp.conjugate(wp), sp.conjugate(zp)
    ok_A += sp.simplify(f.subs({z:zA, w:wA})) == 0
    ok_B += sp.simplify(f.subs({z:zB, w:wB})) == 0
    if k == 1: print("  sample real point p=(%s,%s): A-image = %s point (x,-y); B-image fixes p: %s" % (sp.nsimplify(x), sp.nsimplify(y), (sp.simplify(zA), sp.simplify(wA)), sp.simplify(zB-zp)==0 and sp.simplify(wB-wp)==0))
print("real points (of 12) whose A-image stays on the circle:", ok_A, "; B-image:", ok_B)
sol = sp.solve([f, imgA], [z, w], dict=True)
print("common points of the circle and its A-image:", len(sol), "(bounded, so the A-version of the Bezout step would NOT force equality)")
uu, vv = sp.symbols('u v')
g = sp.expand((z-uu)*(w-vv) - 1)
gB = sp.expand(g.subs({z:w, w:z}, simultaneous=True).subs({uu:sp.conjugate(uu), vv:sp.conjugate(vv)}))
print("B-symmetry of (z-u)(w-v)=1 requires coefficient equality:", sp.solve(sp.Poly(g-gB, z, w).coeffs(), [vv], dict=True))
c = sp.Symbol('c')
print("line z-c: B-image equation", sp.expand((z-c).subs({z:w}).subs(c, sp.conjugate(c))))
def kummer_poly(Ds, var):
    y1,y2,y3 = sp.symbols('y1 y2 y3')
    e = X - y1 - 2*y2 - 3*y3
    e = sp.resultant(y3**2 - Ds[2], e, y3)
    e = sp.resultant(y2**2 - Ds[1], e, y2)
    e = sp.resultant(y1**2 - Ds[0], e, y1)
    return sp.Poly(sp.expand(e), X)
anchors = [0, 7, 19]
Dl = [sp.expand((z-a)**2*((z-a)**2-4)) for a in anchors]
for S in [[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]:
    prod = sp.Mul(*[Dl[i] for i in S])
    _, fl = sp.factor_list(prod)
    odd = [str(fa) for fa,ex in fl if ex % 2 == 1]
    print("subset", S, "odd-exponent factors:", odd)
P = kummer_poly(Dl, z)
fac = sp.factor_list(P.as_expr(), X, z)
print("line case: deg_X of min-poly candidate =", P.degree(), "; irreducible factors' X-degrees:", [sp.degree(fa, X) for fa,ex in fac[1]])
zeta = sp.symbols('zeta')
def Lcirc(a, b):
    a, b = sp.Integer(a), sp.Integer(b)
    return sp.together((z-a)*(b/z - b/a))
for b in [1, 2]:
    Dc = [sp.together(Lcirc(a, b)*(Lcirc(a, b)-4)) for a in [2, 3, 5]]
    Dc = [sp.expand(sp.numer(d)*sp.denom(d)) for d in Dc]
    Pc = kummer_poly(Dc, z)
    fc = sp.factor_list(Pc.as_expr(), X, z)
    print("circle b=%d: irreducible factors' X-degrees:" % b, sorted(sp.degree(fa, X) for fa,ex in fc[1]))
```
Output:
```
eq of image under A: w*z - w + 2*I*w - z - 2*I*z + 4 | equals f? False
eq of image under B: w*z - w - 2*I*w - z + 2*I*z + 4 | equals f? True
  sample real point p=(sqrt(3)/2 + 1,5/2): A-image = (sqrt(3)/2 + 1 - 5*I/2, sqrt(3)/2 + 1 + 5*I/2) point (x,-y); B-image fixes p: True
real points (of 12) whose A-image stays on the circle: 0 ; B-image: 12
common points of the circle and its A-image: 2 (bounded, so the A-version of the Bezout step would NOT force equality)
B-symmetry of (z-u)(w-v)=1 requires coefficient equality: [{v: conjugate(u)}]
line z-c: B-image equation w - conjugate(c)
subset [0] odd-exponent factors: ['z - 2', 'z + 2']
subset [1] odd-exponent factors: ['z - 9', 'z - 5']
subset [2] odd-exponent factors: ['z - 21', 'z - 17']
subset [0, 1] odd-exponent factors: ['z - 9', 'z - 5', 'z - 2', 'z + 2']
subset [0, 2] odd-exponent factors: ['z - 21', 'z - 17', 'z - 2', 'z + 2']
subset [1, 2] odd-exponent factors: ['z - 21', 'z - 17', 'z - 9', 'z - 5']
subset [0, 1, 2] odd-exponent factors: ['z - 21', 'z - 17', 'z - 9', 'z - 5', 'z - 2', 'z + 2']
line case: deg_X of min-poly candidate = 8 ; irreducible factors' X-degrees: [8]
circle b=1: irreducible factors' X-degrees: [1, 1, 1, 1, 1, 1, 1, 1]
circle b=2: irreducible factors' X-degrees: [8]
```
- The map A (the brief's reading) is the wrong map. The map B (the PDF's reading) fixes every real point and preserves the curve. B-symmetry forces v = ū.
- Toy Kummer, line case: every nonempty product of radicands keeps odd-exponent factors, and √D1 + 2√D2 + 3√D3 has an irreducible degree-8 polynomial, so [M(R):M] = 8.
- **Failing control:** on a common unit circle (b = 1) the same construction collapses to 8 linear factors (the radicands are squares, as in the paper's remark). The radius-√2 circle (b = 2) has degree 8.

### Check 4: Lemma 8.2 root-height bound (Mahler-measure computation of h)
```python
import sympy as sp, random, math
x = sp.symbols('x')
def h_rational(q):
    q = sp.Rational(q)
    return 0.0 if q == 0 else math.log(max(abs(q.p), abs(q.q)))
def h_alg_from_minpoly(P):
    P = sp.Poly(P, x)
    _, Pp = P.clear_denoms(); Pp = Pp.primitive()[1]
    lead = abs(Pp.LC()); d = Pp.degree()
    roots = sp.Poly(Pp, x).nroots(n=30)
    return (math.log(lead) + sum((max(0.0, math.log(abs(complex(r)))) if abs(complex(r)) > 0 else 0.0) for r in roots)) / d
random.seed(1)
worst = -1e9; ntest = 0; viol_nolog = 0
for trial in range(60):
    m = random.randint(1, 5)
    coeffs = [sp.Rational(random.randint(-9, 9), random.randint(1, 6)) for _ in range(m)]
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
```
Output:
```
tests: 62  max of h(u) - [sum h(a_r) + log m] = 0.0 (must be <= 0)
control: bound WITHOUT the log m term is violated in 0 tests
control x^2-x-1: h(phi)=0.2406, sum h(a_r)=0, +log 2 = 0.6931
```
The bound holds in all 62 cases; equality occurs at m = 1. **Failing control:** the golden ratio has h = 0.2406 > 0 = Σh(a_r), so the bound without + log m is false. The random sample was too high-height to show this, which is why the explicit control is included.

## 5. Citation table (scope §8)

| Cited | Paper's claim | Source says (quote) | Verdict |
|---|---|---|---|
| [27] Stacks Lemma 10.120.10, Tag 0BC1 (fetched from stacks.math.columbia.edu/tag/0BC1, 14 Oct 2026) | K[Z,W] is a UFD | "Lemma 10.120.10. A polynomial ring over a UFD is a UFD. In particular, if k is a field, then k[x_1, …, x_n] is a UFD." | MATCH (Gauss's lemma itself is not cited, but is standard and stated correctly) |
| [11] Fulton, Algebraic Curves, §5.3 (2008 electronic ed., Wayback copy of www.math.lsa.umich.edu/~wfulton/CurveBook.pdf; the live URL refused the connection) | Distinct irreducible curves of degree ≤ D meet in ≤ D² points | §5.3: "BÉZOUT'S THEOREM. Let F and G be projective plane curves of degree m and n respectively. Assume F and G have no common component. Then Σ_P I(P, F∩G) = mn". §3.3 (2): "I(P, F∩G) = 0 if and only if P ∉ F∩G". k is a fixed algebraically closed field throughout. | MATCH (applies over U, any algebraically closed field) |
| [7] Conrad, Separability II, Thms 1.5, 4.1 (fetched 14 Oct 2026) | A derivation extends uniquely over a separable algebraic extension | Thm 1.5: "Let L/K be a finite extension. Then L is separable over K if and only if each derivation of K has a unique extension to a derivation of L." Thm 4.1: "α is separable over K if and only if every derivation on K has a unique extension to a derivation on K(α)." | MATCH |
| [7] Conrad §5 | Infinite algebraic extension case | "It is left to the reader to check for an infinite algebraic extension L/K that the conditions of Theorems 1.2 and 1.5 match Definition 5.1." | PARTIAL / over-attributed (O1). The claim is true via the paper's own argument plus Conrad Lemma 4.4. |
| [20] Milne FT v5.10, Thm 5.30 and Rem 5.32 (fetched; PDF says "Version 5.10", Sept 2022) | Independent square classes give [M(R_1..R_j):M] = 2^j and every sign pattern is an automorphism over M | Thm 5.30 (with ζ a primitive n-th root of 1 in F): "The map E ↦ F^× ∩ E^{×n} defines a one-to-one correspondence between … finite abelian extensions of F of exponent n … and subgroups B of F^× containing F^{×n} as a subgroup of finite index. The extension corresponding to B is F[B^{1/n}] … If E ↔ B, then [E : F] = (B : F^{×n})." Rem 5.32: "There is a perfect pairing (a, σ) ↦ σa^{1/n}/a^{1/n} : B(E)/F^{×n} × Gal(E/F) → μ_n." | MATCH. With n = 2, F = M (−1 is a primitive square root of 1, char 0), and B = ⟨M^{×2}, D_1..D_j⟩ of index 2^j: degree 2^j, and the perfect pairing makes Gal ≅ Hom(B/M^{×2}, μ_2), so every sign vector is realised. Ω = the algebraic closure of M in U. |

## 6. Valtr / Euclidean-specific content inside §8 (brief items i and viii-d, for this scope)

§8 is not metric-agnostic. It uses the Euclidean structure in three places:
- (8.1): the squared distance is a function of the edge ratio alone, (d − d′)(1/d − 1/d′) = 2 − λ − λ^{-1}. This is what makes the derivative identity (8.9) close up with a single scalar A_i − A′_ℓ.
- (8.10): R² = L(L−4).
- The b = 1 dichotomy: on a common unit circle L(L−4) is a perfect square and the argument genuinely fails (check 2 and the b = 1 control in check 3). The hypothesis deleting popular unit circles is exactly what excludes it.

For a non-Euclidean unit curve there is no analogue of (8.1), so §8 cannot be run.

Realness is used in four places:
- The involution B, which gives nonconstant projections, equal projection degrees, and v = ū.
- Distinct real points have distinct z (curve-side root count in Lemma 8.3).
- The meaning of "unit circle" in (8.4).
- (In §7, outside scope) two real points lie on at most two unit circles.

A complex configuration on the hyperbola graph would lose the involution and the injectivity of z; for example, curve loci of the form z = c become possible.

§8 adds no effective δ (ultrafilter plus contradiction). Nothing in §8 contradicts the n^{1+c} lower bounds, because Prop 8.1 needs a graph of density t^{2−o(1)} on t^{1+o(1)} points with the height structure (8.2)–(8.3), which is a near-4/3 regime object produced by §2–§7.

## 7. Verdict for this scope

**HOLDS AS READ.** Every result in §8 (Prop 8.1 proof, Lemmas 8.2–8.6, §8.5, and the proof of Thm 1.1 as an assembly) was verified line by line, the symbolic identities by sympy with failing controls.
- Brief item (vii)'s "wrong involution / v = u" comes from pdftotext dropping overlines. The PDF has (z,w) ↦ (w̄, z̄), w = c̄, v = ū, all correct, and every downstream use survives (in fact is exactly right).
- The only objections are COSMETIC: O1 (Conrad §5 over-cited for the infinite case; the true statement follows from Conrad Lemma 4.4) and O2–O5 (labels, a superfluous sentence, implicit steps).
- **Not checked by this seat:** whether Props 4.4 and 7.6 actually deliver their outputs. §8 is a correct reduction from the hypotheses of Prop 8.1; the paper stands or falls on §2–§7.
