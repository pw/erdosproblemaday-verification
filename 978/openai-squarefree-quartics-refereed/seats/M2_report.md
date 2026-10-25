# Seat M2 — hostile referee report on printed Sections 5–9 and Section 12

**Paper.** OpenAI, "Squarefree values of quartics and power-free values of polynomials" (24 Sep 2026). I read the LaTeX
(`sections/05`–`09`, `13-cyclotomic`) and checked statement numbering against `paper.txt`.
**Scope.** §5 bihomogeneous determinant cuts · §6 lattice coordinates and exceptional fibres · §7 weighted Hilbert bounds ·
§8 quartic surface bound and the global quintic set · §9 curve alternatives · §12 the cyclotomic quartic, read as a
consistency check against §§4–11.
**Method.** I re-derived every load-bearing step by hand. I checked every Hilbert-function claim that can be made concrete
by computing evaluation ranks mod p = 2^61−1 at random points of the actual variety and comparing them with the claimed
complete-intersection series. I verified the quintic finiteness claim by an exact resultant count. I fetched and checked
the citations used in my sections (Stacks tags, EGHP (∗), Reuss 1307.2802). Brute-force arithmetic checks for x⁴+1 and
x⁴+2 up to 10⁶ were done with PARI/gp. Scratch files and scripts are in `/tmp/oaimath/020/seats/M2_work/`.

**Bottom line.** I could not break any step in §§5–9. Every place where the brief predicts a failure is argued explicitly:
the cut is nonzero on its component, the mixed/pure dichotomy is exhaustive, the Hilbert lower bounds are on the variety
actually present, the constants are uniform in moving equations, and the quintic set is global and small. The
computations agree with the paper wherever a statement is concrete. My findings are EXPOSITION-level or
ERROR-NONFATAL only.

---

## 1. Section 5 — bihomogeneous determinant cuts

### Lemma 5.1 (bicone, Hilbert polynomial (5.1)): HOLDS.
- **Strata dimensions.**
  - Open stratum, all a_i ≠ 0: d+2.
  - One a_i = 0 with nonzero product vector: this forces N₀ = θ_iL₀ and L₀ ≠ 0. Since the roots are distinct, every other
    a_j ≠ 0. Dimension d+1.
  - Zero-product locus: union of coordinate d-planes.
  - Hence codimension d−2 is attained, and the generators form a regular sequence (graded CM, Stacks 02JN).
- **Primeness.** There is one top component. It is generically smooth, so it is reduced (Stacks 031Q/031R, R₀+S₁), hence
  a domain. All six Stacks tags were fetched; each says what is used.
- **Leading term.** I re-derived it: (k∂_A+∂_B)^{d−2} A^{d−1}B^{d−1}/((d−1)!)² equals (5.1) exactly.
- **Derived polynomials.** H, H_a, H_b and their coefficient forms (10.7) match the certificate's `polynomials()`. The
  quartic values at t = 1/2 are (H,H_a,H_b) = (10,5,10), as the appendix asserts.
- **Computation.** I ranked the evaluation of all bidegree-(A,B) monomials at random points of the cone (θ = 1,2,3,5 / …).

  | d | (A,B) | evaluation rank = CI series |
  |---|---|---|
  | 4 | (2,1) | 38 |
  | 4 | (4,2) | 271 |
  | 4 | (6,3) | 1020 |
  | 4 | (3,3) | 320 |
  | 4 | (8,2) | 1013 |
  | 4 | (2,4) | 310 |
  | 5 | (3,1) | 172 |
  | 5 | (4,2) | 975 |
  | 5 | (3,3) | 1180 |
  | 5 | (5,1) | 585 |

  All ten match. The Hilbert function is that of the regular sequence, i.e. the prime ideal is the complete-intersection
  ideal.

### Prop. 5.2, first cut (§5.3).
- **Taylor estimate.** (5.3)/(5.4) correctly use the d small variables (u₁..u_{d−1}, z), weighted (w,…,w,1). The monomial
  count is T^d/(d!w^{d−1}) and S/ℓ = (d/(d+1))(w^{d−1}H)^{1/d}A.
- **Integer lower bound and cut condition.** (5.5) needs only the upper bounds |x_i| ≪ X^{η₊/d} and |y_i| ≪ X^{b₊/d}.
  Comparing it with (5.4) gives exactly the first inequality of (5.2). I checked numerically that the quartic cell of
  Prop 12.2 satisfies it, with a thin margin (0.15270 vs 0.15268).
- **Demand 1 (nonvanishing).** The columns are a basis of the degree-(A,B) coordinate space of V. A kernel vector is
  therefore a form that vanishes at the points but not on V. ✓
- **Saturated equation (5.6).**
  - I re-derived the bidegree λ = l + ks₀ − Σe_i.
  - On the stratum a_i = 0 (nonzero products), the surviving terms are the Laurent monomials a_{−i}^{I_{−i}−e_{−i}}b_i^{ν_{i,I}}.
    They are distinct, and their coefficients g_I(θ_i,1) ≠ 0 because (N₀−θ_iL₀) ∤ g_I.
  - So C cuts that stratum to dimension ≤ d. The zero-product boundary already has dimension d < d+1.
  - Equidimensionality of the complete intersection then forces a unique component, and generic reducedness on the open
    C[a^{±1},N₀,L₀]/(F) gives primeness. ✓
- **Computation (saturation).** I took the concrete factor F = a₂³(N₀−θ₁L₀) + a₁³L₀ for d = 4. This has e = (2,0,0,0) and
  C = a₂³b₁ + a₁L₀ of bidegree (3,1). Evaluation ranks on V(F) at (A,B) = (3,1), (5,2), (6,3), (4,3), (8,2) are 71, 366,
  852, 464, 829. All equal the CI series with the saturated bidegree (3,1). The unsaturated bidegree (5,1) would predict
  400 and 980 at (5,2) and (6,3), which is wrong. So the saturation step is necessary, and it is correct.
- **Mixed vs pure (demand 1).** (λ,s₀) ∈ Z²_{≥0}∖{(0,0)}, so "both ≥ 1 / s₀ = 0 / λ = 0" is exhaustive. A factor F with
  s₀ ≥ 1 whose saturation has λ = 0 is routed correctly to the pure-b branch.

### §5.4, second cut on pure components: HOLDS, uniformly.
- **Rank estimate.** It is coefficient-free: multiplication by Q₀ gives rank ≤ D_e(q) per power of z. The sum is
  c₀T^r/(r!w^{r−1}) with r = d−1.
- **Exponent.** With ℓ = c₀H_aA^r/r!, the factor c₀ cancels and S/ℓ ≥ (r/d)(w^{r−1}H_a)^{1/r}A. This is exactly the
  second inequality of (5.2).
- **Pure-b case.** The pure-b branch is partitioned by the boundedly many reverse branches (Lemma 4.2(1)–(2)), so each
  determinant uses one analytic chart. ✓
- **Nonvanishing.** The second-cut form is again a kernel vector on a basis of W's coordinate space, so it is nonzero on
  W. The degrees depend only on the bounded set of bidegrees (c₀,0) and (0,s₀). ✓
- **Affine consequences.** F(a,n,1) is irreducible and has n-degree s₀. Its a-coefficients have codimension-2 common
  zeros. Lemma 6.3 needs exactly this. ✓

## 2. Section 6 — lattice coordinates and exceptional fibres
- **Lemma 6.1.** The proof (shortest vector, √3/2 projection bound, lift factor 2/√3, Cramer + Hadamard) is complete.
- **Prop. 6.2.**
  - Λ_c has covolume X^{−η₊}M^{d−1}, and U_* ≤ X^{η₊/d}.
  - With J ≥ X^j, the shortest unscaled vector has ‖q‖ ≤ T = X^{m/d−j}, and T/M ≪ X^{−w/d}. So q₀ ≠ 0 and
    c ≡ −q·q₀^{−1} (mod M) with |c_i| ≪ M.
  - This gives O(T^d) = O(X^{m−dj}) s-boxes, and the same count for t-boxes; partners are O(1) by Lemma 4.2(3).
  - The coordinate bound U = u+j+τ follows from J < X^{j+τ}. The polynomial-height claim (max‖b_i‖ ≪ X^{m−η₊/d}) is
    correct.
  - Linear changes within a block preserve the weight filtration, irrespective of their coefficients. ✓
- **Lemma 6.3 (quartic infinite fibres).** The base has dimension ≤ 2 in both cases:
  - if dim Z ≤ 3, by fibre dimension;
  - if Z is mixed, because F has codimension-2 common zeros of its n-coefficients (shown in §5.4).
  
  The integer-point bound O(B²) on a bounded-degree surface is uniform in the coefficients. The final claim (on every
  irreducible Y ⊆ Z meeting the surviving set, n is algebraic over C(a)) is correct as argued. The per-box cost X^{2U} is
  charged in (10.10).

## 3. Section 7 — weighted Hilbert bounds (demand 2)
- **Prop 7.1 construction.**
  - Choosing h−1 a's independent over C(n), plus one more index, gives an h-dimensional image. Its field equals that of
    Y_pair.
  - C₁ (7.3) is the saturation of F₁, and every term has weight ≤ D.
  - The top-weight part restricted to {a_i^kb_i = q} is a^{−e}·in_{(U,kU+V)}F₁(a,q) ≠ 0, so D is exact. D ≥ min(U,V)
    because C₁ is nonconstant.
  - I re-derived the boundary stratum a_i = 0: n = θ_i, all other a_j ≠ 0, and C₁ restricts to distinct Laurent
    monomials.
- **Weighted infinity (§7.2).**
  - At t = 0 with all a ≠ 0, the locus is a hypersurface in (a,q)-space, of dimension h. With some a_i = 0 it is a union of
    coordinate h-planes. So the homogenized system has the expected dimension h+1.
  - It is therefore a complete intersection with a unique top component, hence prime and t-saturated. The graded pieces
    are exactly the filtered pieces.
  - In series (7.7), at a nontrivial root of unity dividing both A and B, it also divides Q = kA+B and E (E is a monomial
    weight of C₁). So the pole order is ≤ h, and the leading term is Q^{h−1}E/(A^hB^h)·N^h/h!. ✓
- **Lower bound on the variety present.** H_Y ≥ H_{Y_pair} by injective, weight-preserving pullback. The doubling clause
  (7.8) is a correct linear-independence argument over K_pair.
- **Uniformity.** deg F₁ is bounded by deg Y, so for each of the finitely many (U,V) only finitely many E occur, hence
  finitely many series. ✓
- **Computation.** I compared the filtered evaluation rank on Y_pair with the cumulative coefficient of (7.7) for every
  N up to Nmax, in three examples. In each, the naive weight of F₁ would give the wrong count.

  | Example | h | D (naive) | Result |
  |---|---|---|---|
  | E1: F₁ = a₂(n−θ₁)+a₁³ | 2 | U+V (3U+V) | 0 mismatches for N ≤ 12 at (U,V) = (1,1): 434 = 434, naive predicts 736 |
  | E2: F₁ = a₁a₂−n | 2 | 2U+V | 0 mismatches at (1,1): 600 = 600 |
  | E3: F₁ = a₃(n−θ₁)(n−θ₂)+a₁²a₂ | 3 | 2U+2V (5U+2V) | 0 mismatches for N ≤ 7 at (1,1): 1221 = 1221, naive predicts 1302 |

  Unequal weights: for (U,V) ∈ {(1,2),(2,1),(2,3),(3,2)} (N ≤ 18 for h = 2, N ≤ 10 for h = 3), all 12 runs give **0
  mismatches**. Examples at the largest N:
  - E1, (2,1): 580 = 580, naive predicts 1076.
  - E3, (2,1): 1456 = 1456, naive predicts 1527.
  - E1, (3,2): 166 = 166, naive predicts 258.
  
  This tests the saturation/extraction step (D ≠ naive weight), the complete intersection at weighted infinity, and the
  root-of-unity (quasi-polynomial) analysis: the series is exact for every N, not just asymptotically. Scripts are
  `M2_work/whilb.gp`, `hilb.gp`; outputs are `whilb2.out`, `checks.out`.
- **§7.4 thresholds.**
  - For dimension d, D = λU + s₀V ≥ U+V. I checked that F(a,n,1) has n-degree exactly s₀ because L₀ ∤ F.
  - For 2 ≤ h ≤ d−1, D ≥ min(U,V).
  - With h independent a's, D ≥ V: a C₁ with no b would be a relation among independent a's.
  
  The three thresholds are exactly the Ψ_h used in (10.3).
- **Exhaustiveness (cross-check with Thm 3.1).** I enumerated which subvarieties can occur.
  - Mixed components (h = d).
  - Subvarieties with n constant: the ≤ 1-point alternative.
  - Subvarieties with n nonconstant: Prop 7.1.
  - Mode Q, h = 3: n is algebraic by Lemma 6.3.
  - Surfaces: Prop 8.1.
  - Curves: Prop 9.2.
  
  No class of subvariety escapes.

## 4. Section 8 — quartic geometry

### Prop 8.1 (surface bound): HOLDS. The case analysis on deg S is exhaustive (demand 3).
S is a surface because n is algebraic over C(a). Its degree is ≥ 3, = 2 or = 1.
- **deg ≥ 3.** A general projection plus a primitive linear form r gives 1, r, r² independent over C(s,t). This yields
  3T²/(2U²); it is the U/√3 branch of δ₂.
- **Quadric.**
  - EGHP (∗) is correctly cited: arXiv math/0404517, (∗) deg X ≥ 1 + codim(X, span X).
  - The span is Q-rational, and the trace form gives Σσ_i(γ)ℓ_i = 0 with all coefficients nonzero. So no three of the four
    lines are concurrent, and they have 6 distinct pairwise intersections. Q₂ cannot vanish at all six.
  - A pair (i,j) with Q₂(v) ≠ 0 makes S of degree 2 over the (a_i,a_j)-plane. If D < D₀, then K_pair = C(a_i,a_j), the
    degree is ≥ 2, the coefficient doubles, and 2D ≥ 2V ≥ D₀. ✓
- **Plane.** If D < D₀, relation (8.2) is forced: monomials of weight < D₀ = min(3U,2V,U+V) are only 1, quadratics in a,
  and single b's. Then:
  - *n polynomial.* deg n ≤ 4.
    - Galois transport makes every index occur with c_i ≠ 0. The transport is correct: τ ∈ Aut(C) maps the edge relation
      to a relation on edge (πi, πj), valid on τ(Y) = Y. Independence is preserved because the plane is Q-rational.
    - Hence a_i² | n−θ_i. On a general line this gives a polynomial of degree ≤ 4 with four distinct critical points:
      impossible.
  - *n not polynomial.* Both c's are nonzero. A denominator factor is a common line ℓ through every edge point
    {a_i = a_j = 0}. Connectivity of the complete multipartite graph gives concurrency.
    - The t → 0 limit gives one degree-2 map (8.4) on the line of directions. It is ramified at all four zero-directions
      with values θ_i.
    - Coincident directions contradict distinct values, and four distinct ramification points contradict degree two.
  - The introduction's paraphrase of this dichotomy is accurate.

### Prop 8.2 (one global set of quintic values): HOLDS (demand 4).
- **(a) Finiteness.**
  - The derivation argument is correct: ∂Φ vanishes at the 4 simple roots of Φ′, so ∂Φ = AΦ′ with deg A ≤ 1. Then
    ∂z_i = −A(z_i), and the normalisations z₁ = 0, z₂ = 1 kill A.
  - *Concrete count.* I eliminated c and solved for (z₃,z₄) by resultant in gp, keeping solutions with distinct critical
    points and G(1) ≠ 0.
    - Critical values (1,i,−1,−i): exactly **25** normalised polynomials. These values are θ for x⁴+1 after division by
      ζ₈; θ for x⁴+2 after division by 2^{1/4}. The problem is invariant under Φ ↦ αΦ+β.
    - Reordered (1,−1,i,−i): 25.
    - Generic (0,1,3,7): 25.
    - This is the Hurwitz/Cayley count n^{n−3} = 5² for n = 5 (labelled critical values, normalised source). It also
      meets the Bézout bound of the elimination.
  - The critical values are the roots θ_i of f, fixed independently of the box, curve or prime. The curve's τ_i are
    σ_i(−q/r) ∈ L, so Φ ∈ L[t]. ✓
- **(b) X^{1/5}.**
  - The monic rescaling (8.5) puts z in A₅^{−1}O_L. The embedding sizes are O(X^{1/5}).
  - The rational-value locus is the inverse image of the diagonal under a product of finite maps (free of rank 5^{r_L}
    over C[v]), so it is one-dimensional.
  - A bounded-degree curve has O(R) integer points in a box of radius R. Total: O_f(X^{1/5}) values. ✓
- **(c) Removed once.** E_f depends only on f (via the θ_i and L), and Section 11 removes it once per dyadic X.
  - On a polynomial line curve with deg n = 5, every selected integer s gives z = (s−τ₁)/(τ₂−τ₁) ∈ L and n = Φ(z) ∈ E_f.
    Such curves have no surviving points.
  - For d = 4 all remaining polynomial line curves therefore have deg b_i ≥ 4 = g. ✓

## 5. Section 9 — curve alternatives: HOLDS.
- **Lemma 9.1.**
  - Interpolation with a+b+1 points has a one-dimensional solution space. Proof: A₁B₀ − A₀B₁ has degree ≤ a+b and a+b+1
    zeros, and coprimality plus the degree bounds force proportionality.
  - The integer solution has polynomial height. The resultant is a nonzero integer of polynomial height, B₁(s) | R₀, and
    the divisor bound finishes. The count is uniform in the coefficients.
- **Prop 9.2 case analysis.** It is exhaustive:
  - n constant;
  - a-image a point;
  - a-image a nonlinear curve, or a line with extension degree ≥ 2: two families give 2T/U;
  - a line with extension degree 1 and some y′ non-polynomial: Lemma 9.1, each s fixes x′;
  - a line with all y′ polynomial: (s−τ_i)^k | n−θ_i gives deg n ≥ 1+d(k−1) and deg b_i ≥ (d−1)(k−1). The d = 4
    equality case is the quintic of Prop 8.2.
  
  The independence of s^j b_i^a (0 ≤ j < g ≤ ℓ) by distinct degrees is correct. Threshold: δ₁ = max{U/2, min(U, V/g)}.
  The constants are uniform for the finitely many (U,V) with bounded ratio.

## 6. Uniformity (demand 5) — where each uniform constant is argued
| Constant | Must be uniform over | Where argued | OK? |
|---|---|---|---|
| Cut degrees A,B; number of components | boxes, X | §5.3 (fixed bidegrees, factor count ≤ degree) | ✓ |
| Taylor coefficients / remainder | boxes | §5.2 (fixed-radius polydisc, Cauchy; Lemma 4.2(2)) | ✓ |
| Second-cut rank N(T) | moving Q₀ | §5.4 (D_e(q) depends only on e ≤ c₀) | ✓ |
| Lattice basis constants; box counts | boxes, X | Lemma 6.1 (C_d), Prop 6.2 | ✓ |
| Fibre-deletion count | moving base | Lemma 6.3 (bounded degree, coefficient-free) | ✓ |
| Hilbert error O(T^{h−1}+1) | moving Y, coordinate changes | §7.3 (finitely many series for bounded deg Y and finitely many (U,V)) | ✓ |
| Surface bound | moving Y | Prop 8.1 (explicit counts or Prop 7.1) | ✓ |
| Curve small-count X^ε | moving rational function | Lemma 9.1 (resultant/divisor; coefficient-free) | ✓ |
| Quintic set | boxes, curves, primes | Prop 8.2 (depends on f only) | ✓ |

## 7. Section 12 consistency check: CONSISTENT.
- **Cor 12.1.** ρ(4) = 0 and ρ(p²) = 4·1[p≡1 mod 8]. The bound c₈ > 3/4 holds.
  - Euler product computed to p ≤ 2·10⁷: **c(x⁴+1) ≈ 0.980817**. The observed squarefree proportion for n ≤ 10⁶ is
    **0.980831**.
  - **c(x⁴+2) ≈ 0.756684** vs observed **0.756674**. Both agree within sampling noise (~10⁻⁴).
- **Prop 12.2 (enlarged cell).** I ran the appendix "enlarged first quartic cell" code exactly (rational arithmetic). It
  passes: P = (4729/10⁵, 5097/10⁵, 6899/10⁵, 76819/1200000) and gap − 4τ = 1941/10⁵.
  - u = 76819/1200000 and v = 313933/10⁶ agree with my hand computation. v/u ≈ 4.90 ≤ 5.
  - The claim that Lemma 4.1 uses p > X only through the bad primes and p^k > interval length is correct; p² ≥ N^{2−2ε₀}
    suffices.
- **§12.2.**
  - Z[ζ₈] norm-Euclidean: the rounding argument and the equality case are correct.
  - (A)² = ker φ₂ by index, which gives A²B = n−ζ. The unit 1+√2 with √2 = ζ−ζ³ balances the two complex places.
  - Primitivity of the coefficient vectors holds.
- **Lemma 12.3 (Pell).** The norm-(−1) ratio argument gives γ ≥ 2+√3 and O(1+log N) solutions. D ≤ 17N^{1−2ε}. ✓
- **§12.3.**
  - [V₈] = (2H+J)² gives intersection numbers (0,1,4,4,0). This reproduces R(A,B) = (4A³B+24A²B²+16AB³)/24 of Lemma 5.1
    at d = 4.
  - The level-saving integral and the threshold (2h+g)/(2a₁+b₁) at (k,l) = (2,1) recompute correctly.
  - q_Z = D Z³/(6ω³) + O(Z²) is correct, via strips. The conditional analytic estimate is internally consistent and is
    labelled conditional.
- **Large-prime tail, brute force.** I factored every f(n), 1 ≤ n ≤ 10⁶.
  - x⁴+1: **zero** n with p² | f(n) for a prime p > n.
  - x⁴+2: exactly **two**, n = 2 (p = 3) and n = 97 (p = 179, 97⁴+2 = 179²·2763).
  - Primes √n < p ≤ n with p² | f(n), per block of 2.5·10⁵: 132/55/44/33 for x⁴+1 and 139/63/46/36 for x⁴+2.
  - This is consistent with Prop 1.4's smallness (heuristically the p > n count grows like log log N).

## 8. Objections (all minor)
1. **EXPOSITION — §5, Lemma 5.1.** "its bihomogeneous coordinate space in degree (A,B) has dimension R(A,B)+O(A^{d−1})".
   For a regular sequence the dimension is the exact finite difference for all large A,B, so the error statement is
   weaker than what is proved. Harmless.
2. **EXPOSITION — Prop 8.2.** "There are finitely many polynomials Φ ∈ L[t] of degree five …". The number over C is 25
   (verified). Stating it, or citing the Hurwitz count, would let a reader check the claim without the derivation
   argument. Not an error.
3. **EXPOSITION — Lemma 9.1.** It reuses the letters A, B (and later D) for exponents, while §5 uses A, B for bidegrees
   and §7 uses D for the extracted weight. Notational clash only.
4. **EXPOSITION — §7.4 "If instead we can select h algebraically independent a-coordinates, the same pair-image
   construction applies."** Prop 7.1's preamble selects h−1 a's independent over C(n). The alternative selection (h a's
   independent over C, n algebraic over them) also gives an h-dimensional image. The boundary and weighted-infinity
   arguments never use which selection was made, so the reuse is valid. The text should say so.
5. **ERROR-NONFATAL / none found.** I found no false mathematical statement in §§5–9 or §12.

No FATAL objection and no GAP within this scope. The paper's §§5–9 prove what they say, at the level of uniformity that
Theorem 3.1 requires.

VERDICT: HOLDS AS READ
