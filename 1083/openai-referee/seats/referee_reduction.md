# Referee report — scope `reduction`: §1.2–1.3 (pp. 2–5) and §2 (pp. 7–13), the formal assembly

Paper: /tmp/oaimath/166/paper.pdf (sha256 37f63553…). Every formula below was read off the rendered PDF pages (Read tool, pp. 1–19, 42–43, 61–62, 74–78, 90–92, 99–104), not off the text extraction.
Reviewer seat: Claude (Opus 5.5), 2026-10-11.

**Bottom line: in this scope I found no FATAL and no GAP.** The §2 assembly is a correct deduction of Theorem 1.1 from seven later results. Each of those results, *as stated on its own page*, has exactly the hypotheses §2 supplies and gives the conclusion §2 uses (interface table, §5 below). No step in §2 uses a rate for M/A → 0 or for δ → 0. Every constant that has to beat a divergent quantity is fixed before N → ∞. The objections below are all COSMETIC or UNCLEAR. Whether Theorem 1.1 is *true* therefore rests entirely on the consumed results: Thm 6.1 (§3–6), Thm 7.1 (§7), Thm A.1 (App. A), Thm B.2/B.12 (App. B). I did not check their proofs (§6 below). Those proofs are the other referees' scopes.

---

## 1. Objections

**R1 — Prop 2.2, p. 8: dyadic sum, hypothesis stated conditionally. COSMETIC (exposition).**
> "If L_max = o(N) is the maximum occupancy, a dyadic sum gives #{discarded pairs} ≤ CN²/H + CNL_max = O(N²/H) + o(N²)."

The text never says *why* L_max = o(N). It does hold: by Lemma 2.1's line row, L_max ≤ 2M ≤ 2A = 2N^{2/d} = o(N) once M ≤ A. I checked the dyadic sum: lines with occupancy in [t, 2t) number ≤ C(N²/t³ + N/t) (Thm B.2) and carry ≤ 2t² pairs each, so Σ_{t ≥ H dyadic} C(N²/t + Nt) ≤ C(N²/H + N·L_max). No rate is used. Fix: cite Lemma 2.1.

**R2 — Prop 2.2, p. 9, case 1: the constant changes silently. COSMETIC.**
> "#{q counted} L²/(2M) ≤ CL² deg(Y)A^{a−1}. This is (2.2), since M ≤ A."

This gives #counted ≤ 2C·M·deg(Y)A^{a−1} ≤ **2C**·deg(Y)A^a. So the constant doubles at each level of the induction on a. The last line of the proof acknowledges it: "Fixed increases in the constants at the finitely many dimensions are harmless." Since a ≤ d−1, the final constant is ≤ 2^{d−1}·max(H, K, Lemma 2.1 constants). That is finite and depends on the sequence only through H and K, which the proposition allows ("fixed along the subsequence").

**R3 — Prop 2.3, p. 10: an unstated monotonicity step, and a constant misnamed. COSMETIC.**
> "The component Hilbert lower bound in Lemma 3.6, applied at the defining degree D, gives H_S(D) = H_{Env_D(S)}(D) ≥ c_d a_j D^j."

Lemma 3.6 (3.7) bounds H_{V_j}(D), where V_j is the union of the group-j components. The step H_{Env_D(S)}(D) ≥ H_{V_j}(D) needs restriction-rank monotonicity under inclusion: the restriction Env → V_j is surjective on quotient spaces. The paper does not state this; it is immediate. The ambient space is ℙ^{d−1}, so the constant is Lemma 3.6's c_{n} with n = d−1, not "c_d". Naming only.

**R4 — Lemma 2.4 proof, p. 12: Lemma 3.1 applied to Q without comment. COSMETIC.**
> "Physical separators from Lemma 3.1, one in p and one in q, have a product of degree O(M)."

Lemma 3.1 is stated for a finite P ⊂ ℝⁿ. The q-separator needs it for Q = RP. This is valid because Δ(Q) = Δ(P), so M is the same and s_q^Q = s_{R⁻¹q}∘R⁻¹. The product has degree 4(M−1) ≤ 4A once M ≤ A. That is positive and ≤ C₀A with C₀ ≥ 4 (hypothesis (i) of Thm A.1).

**R5 — §2.3, p. 10 and p. 12: the genericity conditions on R are not listed. COSMETIC.**
> "Take Q = RP, where R is a sufficiently generic real rotation" … "The rotation R may be chosen to ensure u + w ≠ 0 simultaneously for the finite set of relevant displacement pairs."

R is fixed on p. 10, but the condition is only stated on p. 12, and "the finite set" is never written down. The only genericity §2 needs is R(x′−x) ≠ −(p′−p) for all ordered pairs x ≠ x′ and p ≠ p′ in P. That is finitely many conditions. Each one excludes {R : Ra = b}, which is a proper real-algebraic subset of SO(d) for d ≥ 2. So the conditions can be imposed up front, over all pairs of P, before S is transported. The condition is load-bearing in two places:
- Thm A.1 requires v = u+w ≠ 0 for the local parameters.
- F ∩ F′ ≠ ∅ in (2.8): if u+w = 0, the equation reads 0 = 2u.

Nothing else in §2 uses genericity of R. Thm 7.1 holds for *every* congruent copy (p. 61: "The same estimate holds … for any rigidly congruent copy Q of P").

**R6 — Prop 2.6, p. 13: one step relies on Appendix A without saying so. COSMETIC.**
> "These neighbor flats are distinct by the local parameter check above."

The "check above" (Lemma 2.5) proves the *parameters* [u+w : u−w] are distinct. That distinct parameters give distinct flats is Appendix A, p. 74 ("Distinct parameters give distinct flats"). That fact needs e ≥ 3: for e = 2, K_v = {z : zv = 0} = 0 and the flat does not recover [v]. The local e is d ≥ 3, so it holds.

**R7 — §1.3, p. 4 and §2 preamble, p. 7: the effectivity of the constant is overstated. COSMETIC (misdescription; Theorem 1.1 itself is unaffected).**
> "The sample uses one fixed probability, and all concentration constants are uniform; this is where the preceding quantitative estimates produce the positive constant in Theorem 1.1."
> "We include the selection and sampling arguments here, since keeping their constants uniform is essential."

c_d is not "produced" by any estimate. It is the infimum of |Δ(P)|/|P|^{2/d}, shown positive by contradiction (last paragraph, p. 13). The selection constants are *not* uniform: H, K, the density c and the constant C in (2.2), and hence c₁, c′, c₂, c₃, all depend on the contradiction sequence. That is legitimate, because each is fixed along the subsequence before N → ∞. What genuinely must be uniform is uniform:
- θ < c₄/C₄;
- c₄, which depends only on d through Lemma 3.6 and the Lemma 2.4 constant C(d+1, C₀);
- the Lemma 2.5 constant C(d, C₀).

The proof yields no value or bound for c_d.

**R8 — p. 13: "three ingredients" undercounts the inputs. COSMETIC.**
> "Proposition 2.6, together with the three ingredients proved below, rules out (2.1) in the least possible failing dimension."

§2 actually consumes eight later results: Thm 6.1, Thm 7.1, Thm A.1(a)/(b), Lemma 3.1, Lemma 3.6/Cor 3.7, Thm B.2, Thm B.12/Cor B.13 (the interface table counts A.1(a) and A.1(b) as two rows). Lemma 3.6 is the engine of both (2.3) and (2.9).

**R9 — Lemma 2.1 vs Cor B.13: different normalisations of M. COSMETIC.**
Cor B.13 (p. 101): "If a finite set in Euclidean space determines at most M ≥ 1 positive distances, then any affine two-plane contains at most CM log(2M) of its points."
In Cor B.13, M = |Δ|. In Lemma 2.1, M = 1 + |Δ|. Since x ↦ Cx log 2x is increasing, the u = 2 row follows.

**R10 — Prop 2.6, p. 13: two meanings of "≫". UNCLEAR wording, correct content.**
> "There are at most N² vertices, and δ(H) ≫ A^{d−1}, a fixed positive power of N."

Here "≫" means δ(H)/A^{d−1} → ∞, which is (2.5). What the union bound needs is weaker: δ(H) ≥ A^{d−1} = N^{2(d−1)/d} ≥ N^{4/3} eventually. Then N²·exp(−cθδ(H)) ≤ N²·exp(−cθN^{4/3}) → 0. Sufficient.

**Observation for brief item (vi) — not an objection.** §2 itself consumes far less than the planar Ω(n/log n):
- **c₀ > 0 for d = 3** (p. 8) needs plane occupancy ≤ B^{3−c₀}. That holds for any planar exponent α > 2/3 (n ≤ M^{1/α} ≤ B^{2/α}).
- **Prop 2.2, ℓ ≤ 3, a ≥ 2** (p. 9) needs plane ≤ O(A²) = O(B⁴), i.e. α ≥ 1/2.
- **The fibre case d−ℓ = 2** uses the elementary circle bound 2M, not the planar row.
- **"Planes have the more precise bound B^{2+o(1)}"** is consumed only later (§4–6, e.g. p. 31: "CNB^{2+o(1)}(1+log N)² = o(N²), using the plane cap and d ≥ 3"). Even that line, for d = 3, needs only plane cap = o(B³/log²B).

Whether any *later* use needs the full planar strength is the incidence/secants referees' question.

---

## 2. Line-by-line findings

**Lemma 2.1 (p. 7–8).**
- u = 0 row: trivial.
- u = 1 and circle rows: from a sample point x on the line or circle, each value in Δ(P) is realised ≤ 2 times. For the circle: a sphere about x meets the circle's plane in a circle centred at x, distinct from the given circle, so ≤ 2 points. Hence ≤ 1 + 2(M−1) ≤ 2M. ✓
- u = 2 row: Cor B.13 (R9). ✓
- u ≥ 3 rows: Theorem 1.1 in dimension u < d (minimality) gives n ≤ (M/c_u)^{u/2}. ✓
- c₀ = 1/2, with N·B^{−1/2} = B^{d−1/2} (I checked each row):
  - line: 2M ≤ 2B²;
  - plane: CB² log(2B²);
  - u-flat: C_u B^u ≤ C_u B^{d−1}.

  All are ≤ B^{d−1/2} for large B, using only M ≤ B². ✓
- Complex-flat sentence: W ∩ ℝ^d is a real affine subspace whose complexification lies in W. So its real dimension is ≤ the complex dimension of W, and it is proper if W is. ✓

**Theorem 6.1 as used (p. 8) vs as stated (p. 42).** The two statements match:
- p. 8: "In the regime (2.1), one cannot assign to each p ∈ P a union C_p of irreducible projective curves, each spanning a projective space of dimension at most two, with deg C_p ≤ δN/A, δ → 0, such that all but o(N²) unordered pairs {p,q} satisfy π_p(q) ∈ C_p or π_q(p) ∈ C_q."
- p. 42: "Along a sequence with M = o(A), there cannot be families C_p, one for each p ∈ P, of irreducible projective curves, each spanning projective dimension at most two, such that deg C_p ≤ E = δN/A, δ → 0, and 1 − o(1) of the unordered pairs {p,q} satisfy π_p(q) ∈ C_p or π_q(p) ∈ C_q."
- The §6 preamble adds "We retain the contradiction hypotheses, including the lower-dimensional induction bounds".
- "All but o(N²)" and "1 − o(1) of the C(N,2) pairs" are the same thing. ✓

**Negation vs Prop 2.2's diagonal argument (p. 9).** Let f_n(H,K) be the surviving fraction after the line discard at threshold H and the greedy at threshold KA. The negation of "∃ H, K and a subsequence with liminf f_n > 0" is "∀ H, K: f_n(H,K) → 0". Blocks with H_n = K_n = j for n_j ≤ n < n_{j+1} then give f_n(H_n,K_n) → 0. The pairs not covered are the line-discarded ones, at most O(N²/H_n) + O(N·M) = o(N²), plus the survivors, o(N²). Every other pair was removed by the greedy at p (so π_p(q) ∈ C_p) or at q (so π_q(p) ∈ C_q). That is the either-endpoint alternative, exactly.

For the degree: each greedy curve Γ is charged > K_nA·deg Γ partners, and the charged sets are disjoint. Hence Σ deg < N/(K_nA) = δ_nN/A with δ_n = 1/K_n → 0, at a rate set only by the sequence. A curve emptied by the greedy cannot be chosen again, so deg C_p is a sum over distinct curves. Every curve spans at most ℙ². The output is **exactly** the forbidden configuration. ✓

**Prop 2.2, (2.2) by induction on a (p. 9).**
- **a = 0:** a direction carries ≤ H partners (light lines). ✓
- **Case 1** (some radius class about p has L ≥ 2M distinct projections to U):
  - For each counted q the |q − z_i| take ≤ M values. Cauchy–Schwarz gives Σ n_r² − L ≥ L²/M − L ≥ L²/(2M) ordered equal pairs, using L ≥ 2M.
  - Expanding |q−z_i|² = |q−p|² − 2(q−p)·(z_i−p) + |z_i−p|² with |z_i−p| = |z_j−p| gives (q−p)·(z_i−z_j) = 0. ✓
  - The section is proper on Y: if Y ⊂ H_{ij}, every counted displacement, hence U, is orthogonal to proj_U(z_i−z_j) ≠ 0. ✓
  - Bézout: the components have pure dimension a−1 and total degree ≤ deg Y. ✓
  - Double counting then gives ≤ 2CM·deg(Y)A^{a−1} (R2). ✓
- **Case 2** (every radius class has < 2M projections):
  - At most M radius classes (counting p itself) times < 2M projections gives < 2M² fibres covering **all of P**.
  - A fibre lies on a sphere inside the (d−ℓ)-flat p + u + U^⊥. The paper bounds it by the **flat** row u = d−ℓ, which is legitimate because the sphere lies in the flat and 3 ≤ d−ℓ < d. For d−ℓ = 2 it uses the circle row; for d−ℓ ≤ 1, two points.
  - Exponents: 2 + (d−ℓ)/2 ≤ d/2 ⟺ ℓ ≥ 4. For d−ℓ = 2 the total is M³ ≤ M^{d/2} since d = ℓ+2 ≥ 6. For d−ℓ ≤ 1 the total is M² ≤ M^{d/2} since d ≥ 4.
  - The contradiction N ≤ C·M^{d/2} holds for all p and U at once, eventually, because (M/A)^{d/2} → 0. No rate is needed.
- **ℓ ≤ 3:**
  - a ≥ 2: Lemma 2.1 gives at most CM log 2M or C₃M^{3/2} (when 3 < d), both ≤ A². If ℓ = d = 3, the bound is N = A^{3/2} ≤ A². ✓
  - a = 1 with Y ⊂ ℙ(U_ℂ), which has dimension ℓ−1 ≤ 2: the greedy left ≤ KA·deg Y unremoved partners on any curve spanning ≤ ℙ², and the partners in G are a subset of these. ✓
  - a = 1 with Y ⊄ ℙ(U_ℂ): Y ∩ ℙ(U_ℂ) lies in Y ∩ H for some hyperplane H ⊃ ℙ(U_ℂ) not containing Y, so it has ≤ deg Y points. That gives ≤ H·deg Y partners. ✓

**Prop 2.3 (p. 10).**
- What (2.3) needs from Lemma 3.6: for any finite T ⊂ ℙ^{d−1}, any D ≥ 1 and any j, H_T(D) ≥ c(d)·a_j·D^j, where a_j is the total degree of (any subfamily of) the j-dimensional components of Env_D(T).
- What Lemma 3.6 and Cor 3.7 state (pp. 18–19): (3.7) H_V(L) ≥ c_n·a·L^k for V a union of k-dimensional irreducible components of a locus of equations of degree ≤ L, L ≥ 1. The statement continues: "The same assertions hold for projective varieties, with homogeneous restriction rank", and "In particular these statements apply to the components of Env_L(T)". **MATCH**, with L = D = ⌊A⌋ ≥ 1, (3.1), and monotonicity (R3).
- I also read the (3.6)/(3.7) proof. The generic fibre of V gives a = deg V points, isolated in the generic fibre of the whole locus. Lemma 3.3 separates them in degree q ≤ C_nL, independently of a. Multiplying by base monomials of degree ≤ D−q, then (3.8) H(bL) ≤ bⁿH(L), gives the bound. I found no flaw. This is the step that makes the bound uniform in component degree, which brief item (ii) worries about; it is the algebra referee's scope.
- Assembly: |S| ≤ Σ_j C·a_j·A^j ≤ Σ_j (C/c)(A/D)^j·H_S(D) ≤ d·2^{d−1}(C/c)·H_S(D), with A ≤ 2D. ✓
- Charging argument: an omitted edge is blocked at an endpoint, where its evaluation vector lies in the span of the selected vectors there. The charged set at p has rank ≤ s_p, so by (2.3) it has size ≤ s_p/c₁. Summing, omitted ≤ Σ s_p/c₁ = 2|E′|/c₁, hence |E′| ≥ cN²/(1+2/c₁). ✓
- Separators: surjectivity of the evaluation map gives them. At most one partner per projective direction. ✓

**§2.3 (pp. 10–11).**
- (2.4): each length-ρ pair in S and each in RS give 2 edges (two bijections), and these are distinct. There are ≤ M−1 lengths, so 2Σs_ρ² ≥ 2|S|²/M. ✓
- d = 3 deletion: every edge inside V_g with k_g ≥ C_richA is removed, at cost ≤ Σ C(k_g,2) ≤ K_richN⁴/(2A). Since K_richM/A → 0, this is o(N⁴/M), with no rate.
- Survivor property: if (p,q) kept r neighbours matched (with it) by one isometry g, then k_g ≥ r+1. So either k_g ≥ C_richA (all those edges were deleted) or r < C_richA. Later pruning only removes edges. ✓
- Pruning: fewer than N² deletions of fewer than E₀/(2N²) edges each, so δ(H) ≥ E₀/(2N²) ≥ c₃N²/M and δ/A^{d−1} ≥ c₃A/M → ∞. ✓
- (2.6): dimension s₀ = d(d−1)/2. Distinct pairs give distinct flats: the flat recovers y₀ at Z = 0, then v₀ via Zv₀ for all skew Z (d ≥ 2). ✓
- (2.7): the matrix identity holds. The last coordinate is −c·v₀ = −(y₀ − Zv₀)·v₀ = −v₀·y₀, using v₀·Zv₀ = 0. Also y(v) = 0 and v ≠ 0. ✓
- (2.8): v₀′ − v₀ = (u+w)/2 and y₀′ − y₀ = (u−w)/2. ✓
- Numerical checks with random data, d = 3…6 (`/tmp/ref_reduction_scripts/chk.py`, `chk2.py`; the second uses unequal-distance controls):
  - the (2.7) identity holds;
  - the (2.8) intersection holds;
  - Z ↦ Z(u+w) on skew d×d matrices has rank d−1, so the neighbour flat has codimension d−1 in F_{p,q};
  - the global evaluation flat has dimension s₀;
  - the global form satisfies B((v,y),(v′,y′)) = −(v₀−v₀′)·(y₀−y₀′) = −(|p−p′|² − |q−q′|²)/4. The sign is opposite to the paper's display but irrelevant, since the paper sets it to 0;
  - the local form satisfies B = 2(u_i·u_j − w_i·w_j).

**Lemma 2.4 (p. 12).**
- e = d+1, r = d; Appendix A's s₀ = C(e−1, 2) = d(d−1)/2 agrees with §2.
- (i): product of Lemma 3.1 separators, homogenised with v_{d+1}. Degree 4(M−1) ≤ 4A, and at the representative ((v₀,1),(y₀,−v₀·y₀)) it evaluates to s_p(p)s_q(q) = 1. ✓
- (ii): a parameter set in one ℙ^r ⊂ Q has pairwise isotropic real representatives, so |p−p′| = |q−q′|. Hence p determines q, giving ≤ N = A^{d/2} ≤ A^{d−1}. ✓
- (a): |𝒫| ≤ N² = A^d = A^r. ✓
- Endpoints: h = 0 is the equal-dimension case; h = d uses the cardinality. ✓

**Lemma 2.5 (pp. 12–13).**
- e = d, r = d−1; local n = C(d,2) = C(d−1,2) + (d−1). ✓
- Parameters [u+w : u−w] lie on the quadric ((u−w)·(u+w) = |u|² − |w|² = 0), with v ≠ 0 (R5).
- Distinctness: λ is real; uniqueness per direction gives u′ = u, hence λ = 1. ✓
- (i): σ_u(u)σ_w(w) with u = (v+y)/2, w = (v−y)/2, homogeneous of degree 2D ≤ 2A. It vanishes at other neighbours because either p′ differs (σ_u = 0) or p′ agrees and q′ differs (σ_w = 0). It equals 1 at the parameter itself. ✓
- (ii), Gram step: the parameters in one ℙ^r ⊂ Q satisfy u_i·u_j = w_i·w_j for all i, j, including i = j. So u_i ↦ w_i is a well-defined real isometry of spans; it extends to S ∈ O(d), and g(x) = q + S(x−p) matches the centre and those neighbours.
  - d ≥ 4: g is a function, so the neighbours number ≤ N = A^{d/2} ≤ A^{d−2}.
  - d = 3: the survivor property gives < C_richA. Both orientations are included, as are Thm 7.1 and the deletion. ✓
  - **The survivor property is exactly what (ii) needs.**
- (b): a hypersurface component has dimension n−1, i.e. h = r−1 = d−2 ∈ [1, r) for d ≥ 3. It lies in the zero set of a polynomial of degree ≤ A ≤ C₀A. Summing over components of total degree ≤ A gives ≤ C·A·A^{d−2}. This is literally Thm A.1's "useful consequence of (b)". ✓

**Prop 2.6 (p. 13).**
- (2.9): groups h = 0…d. Lemma 2.4 gives assigned ≤ C·a_h·A^h. Cor 3.7 at L = D, applied to the components of the affine envelope in ℂ^{s₀+d}, gives H ≥ c·a_h·D^{s₀+h}. Hence m ≤ (d+1)·C·2^{s₀+d}·H/(c·A^{s₀}). The case "envelope = ambient space" is covered (zero equation, or H = C(D+s₀+d, s₀+d) directly). ✓
- Sample rank: subadditive over the union, ≤ #sampled·C(D+s₀, s₀) ≤ C₄·θ·m·A^{s₀}. ✓
- Markov: P(#sampled ≤ 2θm) ≥ 1/2. ✓
- Chernoff: P(X < μ/2) ≤ e^{−μ/8} with μ ≥ θδ(H) ≥ θA^{d−1}, so the union bound → 0 (R10). ✓
- Existence of f: rank(sample) < rank(all), so some f vanishes on every sampled flat and not on some F. ✓
- Endgame: f|_F has degree ≤ D ≤ A and vanishes on ≥ θδ(H)/2 distinct neighbour flats (R6). This exceeds C·A^{d−1} eventually because θc₃A/(2M) → ∞. Contradiction with Lemma 2.5. ✓
- Last paragraph: an infimum of 0 forces a sequence with ratio → 0. Then N → ∞ (bounded N gives ratio ≥ N^{−2/d}), and M/A ≤ 2|Δ|/N^{2/d} → 0. ✓

**Hidden-rate audit of every "eventually / sufficiently large / o(·)" in §2:**

| Location | What the step needs | Rate on M/A or δ used? |
|---|---|---|
| Lemma 2.1, c₀ | M ≤ B², B ≥ B₀(d) | No |
| L_max = o(N) | 2M ≤ 2A | No |
| Prop 2.2, case 2 impossible | (M/A)^{d/2} < 1/C | No |
| d = 3 deletion | K_richM/A < c₂/2 | No |
| (2.5) | c₃A/M → ∞ | No |
| Union bound | δ(H) ≥ A^{d−1}, eventually | No |
| Final contradiction | θc₃A/(2M) > C_{2.5} | No |
| Diagonal H_n, K_n → ∞ | rate dictated by the sequence and handed to Thm 6.1, which claims to accept any δ → 0 | No (in §2) |

**No rate is used anywhere in §2.**

**Hand-wave words in pp. 2–13: 14 instances (grep), plus "after advancing along the sequence" (p. 8). All checked.**
- "sufficiently large" / "eventually" (pp. 7, 8, 10): each needs only N ≥ N₀ with no rate.
- "After passing to a subsequence" (p. 8) and "sufficiently slowly" (p. 9): the diagonal argument; checked.
- "generic" (p. 4, rotated copy; p. 8, planar projection, fine and duplicated in B.2's proof): checked.
- "sufficiently generic" (p. 10): R5.
- "generic section" (p. 11): BES citation, decorative.
- "uniformly" (p. 10): c₁ fixed along the subsequence.
- "trivial" (p. 9): N = A^{3/2} ≤ A².
- "harmless" (p. 9): R2.
- "sufficiently small" (p. 3, §1.3 overview): §5's, not in this scope.

---

## 3. Citation table (scope §1.2–1.3, §2)

| Cited | Paper claims | Source says (quote) | Verdict |
|---|---|---|---|
| [2] Aksoy Yazici, arXiv:2002.01248 (v1 fetched; v3 = withdrawal notice; abstract via arXiv API, current version) | Footnote 1, p. 2: "An earlier manuscript of Aksoy Yazici claimed the constant-factor bound in all dimensions d ≥ 3, but was withdrawn by the author because the proof of its Theorem 1.2 is not correct." Ref. [2]: "Withdrawn by the author on February 12, 2020." | v1 Theorem 1.1: "Let E be a set of points R^d with \|E\| = n. Then the number of distinct distances determined by E is Ω(n^{2/d})." Current abstract: "…for d≥3, a set of n points in R^d determines Ω(n^{2/d}) distinct distances." arXiv comment: "The paper is withdrawn as the proof of Theorem 1.2 is not correct"; last update 2020-02-12T17:17:05Z. | MATCH |
| [4] Bardwell-Evans–Sheffer, arXiv:1705.10963v2 (6 Apr 2019; current) | p. 11: "Each F_{p,q} is the complexification of the corresponding real point-pair flat in the construction of Bardwell-Evans and Sheffer before their generic section [4, Theorem 6.1]." | Thm 6.1: "Given a, p ∈ R^d, the flat η_d(T_ap ∩ Spun(d)^+) is defined by the following system of d equations … a_1 − p_1 = (a_2+p_2)x_{1,2} + … + (a_d+p_d)x_{1,d} + 2x_{1,d+1}, a_2 − p_2 = −(a_1+p_1)x_{1,2} + …". In matrix form: a − p = X(a+p) + 2c with X skew. Halving gives the paper's Z(p+q)/2 + c = (p−q)/2 under (a,p) ↦ (p,q). BES §1: "intersect L with a generic (2d − 1)-flat". | MATCH (non-load-bearing) |
| Theorem B.12 / Cor B.13 (internal) | Lemma 2.1 u = 2 row: CM log(2M) | Cor B.13 (p. 101), quoted in R9. Thm B.12: "Every finite set Q ⊂ ℝ² of n ≥ 2 points determines at least cn/log(2n) distinct positive distances." | MATCH (R9 normalisation) |
| Theorem B.2 (internal) | p. 8: lines with ≥ t points ≤ C(N²/t³ + N/t), via a generic planar projection | p. 91: "the number of lines containing at least k ≥ 2 points of an n-point set is at most C(n²/k³ + n/k). The same assertions apply to finite point–line configurations in ℝ^s and in real projective space." | MATCH |

§1.2–1.3 cite no other external source; §1.1 belongs to the `citations` referee.

---

## 4. Constant-dependency table

| Constant | Fixed where | Depends on | Used where | Claimed independent of | OK? |
|---|---|---|---|---|---|
| c₀ = 1/2 | Lemma 2.1 | nothing (needs B ≥ B₀(d, C_u, planar C)) | later sections | sequence | ✓ |
| C_u (u ≥ 3), planar C | Lemma 2.1 (via c_u, Cor B.13) | u (non-effective, from minimality) | Lemma 2.1 rows, Prop 2.2 | sequence | ✓ |
| H, K | Prop 2.2 (existence by contradiction with Thm 6.1) | **the sequence** | light-line and greedy bounds | — ("fixed along the subsequence") | ✓ |
| c (density), C in (2.2) | Prop 2.2 | sequence (through H, K), d, C_u; C grows ≤ 2^{d−1} (R2) | Prop 2.3 | N | ✓ |
| c_n (Lemma 3.6) | Lemma 3.6 | n only (n = d−1, and n = d(d+1)/2 in Prop 2.6) | (2.3), (2.9) | everything else | ✓ (statement; proof algebra scope) |
| c₁ | (2.3) | C, c_{d−1}, d | Prop 2.3 charging | subset S, star, N | ✓ |
| c′ = c/(1+2/c₁); c₂ = 2c′² | Prop 2.3; (2.4) | sequence | (2.4), pruning | N | ✓ |
| C_rich, K_rich | Thm 7.1 | absolute | d = 3 deletion, Lemma 2.5 cap | rate of M/A (p. 61 says so) | ✓ (as stated) |
| c₃ = c₂/4 (d = 3) or c₂/2 | (2.5) | sequence | Prop 2.6 endgame | N | ✓ |
| C₀ | Lemmas 2.4–2.5 (implicit) | max(4, C_rich), absolute | Thm A.1 hypotheses | sequence | ✓ |
| C(Lemma 2.4) = C(d+1, C₀); C(Lemma 2.5) = C(d, C₀) | Thm A.1 | d only | (2.9), endgame | A, sequence, sample | ✓ |
| c₄, C₄ | (2.9), sample bound | d only (via C(Lemma 2.4), c_n, binomial) | choice of θ | sequence (in fact) | ✓ |
| θ < c₄/C₄ | Prop 2.6 | d only | Markov/Chernoff | N, δ(H) | ✓ |
| D = ⌊A⌋ | Props 2.3, 2.6 | N | everywhere | — | ✓ (uses only A ≥ 1, A ≤ 2D) |

There is no cycle. θ is chosen from c₄ and C₄, which precede the sample and do not depend on δ(H). Every comparison is of the form "fixed constant vs A/M → ∞".

---

## 5. Interface table — every later result §2 consumes

| Result (page) | Hypotheses as stated | Supplied by §2 | Conclusion as stated | Used by §2 | Verdict |
|---|---|---|---|---|---|
| **Thm 6.1** (p. 42) | contradiction hypotheses; sequence with M = o(A); C_p finite families of irreducible curves each spanning ≤ ℙ²; deg C_p ≤ δN/A, δ → 0; 1−o(1) of unordered pairs covered at either endpoint | (2.1) sequence in least failing d; greedy curves; δ_n = 1/K_n; uncovered ≤ line-discarded + survivors = o(N²) | such families cannot exist | negation gives fixed H, K | MATCH, exactly |
| **Thm 7.1** (p. 61) | P ⊂ ℝ³, N ≥ 2, A = N^{2/3}, M ≤ A; also any rigidly congruent copy Q | d = 3, M ≤ A eventually, Q = RP | motions (both orientations) with k_g ≥ C_richA finite; Σk_g² ≤ K_richN⁴/A; absolute constants | deletion cost ≤ K_richN⁴/(2A) = o(N⁴/M) | MATCH |
| **Thm A.1 (a)** (p. 75) | e ≥ 3; C₀ ≥ 1, A ≥ 1; 𝒫 finite distinct, v ≠ 0; (i) separators of positive degree ≤ C₀A; (ii) ≤ C₀A^{r−1} per ℙ^r ⊂ Q; \|𝒫\| ≤ C₀A^r | e = d+1, r = d; (2.7) parameters; Lemma 3.1 product, degree 4(M−1) ≤ 4A; injectivity of p gives ≤ N ≤ A^{d−1}; \|𝒫\| ≤ A^d | ≤ C(e, C₀)·deg(V)·A^h for 1 ≤ h < r | Lemma 2.4 for 0 ≤ h ≤ d (endpoints separately) | MATCH |
| **Thm A.1 (b)** (p. 75) | as above but V ⊂ zero set of a nonzero polynomial of degree ≤ C₀A; no \|𝒫\| bound | e = d, r = d−1; neighbour parameters [u+w : u−w]; σ_uσ_w of degree 2D ≤ 2A; cap N ≤ A^{d−2} (d ≥ 4) or < C_richA (d = 3); hypersurface components of a degree ≤ A polynomial, h = d−2 | same, plus "a nonzero polynomial of degree D ≤ C₀A contains at most CDA^{r−1} of the flats" | Lemma 2.5: ≤ CA^{d−1} | MATCH |
| **Lemma 3.1** (p. 15) | finite P ⊂ ℝⁿ, M = 1+\|Δ(P)\| | P and Q = RP (R4) | s_p of degree ≤ 2(M−1), s_p(p) = 1, s_p(q) = 0 | Lemma 2.4 separators | MATCH |
| **Lemma 3.6 (3.7) / Cor 3.7** (pp. 18–19) | V a union of k-dimensional irreducible components of a locus of equations of degree ≤ L, L ≥ 1; projective version stated | components of Env_D(S) ⊂ ℙ^{d−1} and of Env_D(∪𝓕) ⊂ ℂ^{s₀+d}, L = D | H_V(L) ≥ c_n·a·L^k | (2.3), (2.9), plus (3.1) and monotonicity | MATCH (R3) |
| **Thm B.2** (p. 91) | n-point set, k ≥ 2; ℝ^s allowed | P ⊂ ℝ^d, t ≥ 2 | ≤ C(n²/k³ + n/k) rich lines | dyadic discard | MATCH |
| **Thm B.12 / Cor B.13** (p. 101) | M ≥ 1 positive distances | M = 1+\|Δ\| (monotone) | plane ≤ CM log(2M) | Lemma 2.1 u = 2 | MATCH (R9) |
| **Thm 1.1 in dims 3 ≤ u < d** | minimality of d | flat occupancy | n ≤ (M/c_u)^{u/2} | Lemma 2.1 rows | MATCH |

Cycle check: I grepped pp. 14–103 for references to §2 results. Only Lemma 2.1 and (2.1) are used later (pp. 27, 51), plus Lemma 2.5 in Remark 7.8, which is a forward explanation. Lemma 2.1 depends only on minimality and Cor B.13. Thm 7.1 uses M ≤ A only through the line cap (7.2). **No circularity.**

---

## 6. Verified line by line vs skimmed

**Verified line by line, PDF-rendered:**
- §1.2; §1.3 (each step checked against §2 for consistency); Figure 1.
- §2.1 including the Lemma 2.1 proof.
- The Theorem 6.1 statements on p. 8 and p. 42.
- Prop 2.2 (every sentence, both cases, the ℓ ≤ 3 cases, the diagonal argument).
- Prop 2.3; §2.3 including (2.4), the d = 3 deletion, pruning, (2.5)–(2.8) (numerics as listed in §2).
- Lemma 2.4; Lemma 2.5; Prop 2.6; the closing paragraph.
- Interface statements read verbatim: Thm 6.1, Thm 7.1 (plus the p. 62 line-cap remark), Thm A.1 (plus the p. 74 setup), Lemma 3.1 with its proof, Lemma 3.6 with its full proof and Cor 3.7, Thm B.2, Thm B.12, Cor B.13 with its proof.
- Citations [2] and [4] fetched and compared.

**Read but not audited:**
- Lemma 3.3 (the isolated-point separator via Lemma 3.2's determinant), on which Lemma 3.6 rests. I followed the argument and it looks correct (Bezoutian / divided-difference construction, degree ≤ c(L−1) independent of the number of points). It belongs to the algebra scope.
- The proof of Thm B.2: crossing-number argument and the projection paragraph.
- The proof of Thm B.12: it depends on B.5, B.10 and B.11, which I did not check.

**Not checked (other scopes):**
- the proof of Thm 6.1 (§3–6);
- the proof of Thm 7.1 (§7);
- the proof of Thm A.1 (App. A);
- the proofs of B.5 and B.10.

---

## 7. Verdict for this scope

**HOLDS AS READ.** §2 is a correct, rate-free deduction of Theorem 1.1 from the consumed results, and the statement of each consumed result matches its use. In particular:
- Theorem 6.1's either-endpoint, any-δ → 0 form is exactly what Prop 2.2's diagonal argument produces.
- The d = 3 survivor property is exactly the local isotropic cap required by Thm A.1(ii).
- Lemma 3.6 at the defining degree is stated in the form (2.3) and (2.9) need, and its proof (which I read) is uniform in component degree.

**COULD NOT CHECK (outside scope):** the truth of Thm 6.1, Thm 7.1, Thm A.1, Lemma 3.3, and Thms B.5/B.10/B.12. The correctness of Theorem 1.1 reduces to these.
