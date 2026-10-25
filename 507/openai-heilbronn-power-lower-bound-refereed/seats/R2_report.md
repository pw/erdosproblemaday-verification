# Seat R2: hostile referee report on §5, the t = 0 hand-off in Prop 6.3, §7, §8 and Appendix A

Paper: OpenAI, "A power improvement in the Heilbronn triangle lower bound" (25 Sep 2026). I read it from the LaTeX in `paper/src/build/sections/05–09*.tex` and checked it against the printed numbering in `paper/paper.txt`. In print, (5.1)–(5.8) are: parameters, cap size, allowed shifts, V, short relation, the definition of W, the weight bounds, and the normalization identity. (7.1)–(7.11) and (8.1)–(8.8) are as listed in the PDF text.

Scratch work and scripts are in `/tmp/oaimath/191/seats/R2_work/`. Every script ran under `ulimit -v 4000000; timeout 900`. I compiled nothing and did not touch Lean.

**Bottom line.** I found no FATAL issue and no GAP in my sections. Every step I was asked to press on holds as written: the union bound, the uniform affine map, transitivity, the support statement, g | E, J_x, surjectivity, the B^j | g equivalence, the density, R ≥ h, the exhaustive case split, every power-of-h-over-q estimate, the §8 exponents, the every-n interpolation, and Bertrand. I re-derived each step by hand. Where the statement allows it, I also checked it numerically, and each check came with a control that could fail. The objections below are EXPOSITION only.

---

## §5: auxiliary cap, Lemmas 5.1 and 5.2, Prop 5.3, (5.8)

**(5.1)/(5.2).** From q > h^100 ≥ 2000 h^4 = 2000H² we get w = ⌊q/(1000H²)⌋ ≥ q/(1000H²) − 1 ≥ q/(2000H²). Then s ≥ w³/q ≥ q²/(2000³H⁶), so q³/s ≤ 8·10⁹ q h¹². This is the bound §7 uses as "q³/s ≪ qh¹²". **Holds.**

**Lemma 5.1.** On a line p + tv with (v₁,v₂) ≠ 0, the third-coordinate equation is p₃ + tv₃ = Q(p₁,p₂) + 2tB(p,v) + t²Q(v₁,v₂). Its leading coefficient Q(v₁,v₂) is nonzero because Q is anisotropic, so the line meets Γ at most twice. A vertical line meets Γ once. The averaging argument is exact: each point lies in b + Γ with probability q²/q³.
- *Check (`s51_cap.py`).* For q = 3, 5, 7, 11, 13: Γ has q² points and **0** collinear triples among all C(q²,3), and Q vanishes only at (0,0).
- For (q,w) ∈ {(11,6), (13,5), (17,9), (31,7), (2003,2)}, the exact average over translates equals w³/q, and the maximum is at least w³/q.

**Holds.**

**Lemma 5.2.**
- *Union bound.* 3Hw ≤ 3q/(1000H) < q/2, so for each m ≤ 3H < q the bad set {t : ‖t‖_q ≤ 3Hw} has exactly 6Hw + 1 residues. That gives Pr ≤ 3H(6Hw+1)/q ≤ 18/1000 + 3/(2000H) < 1/2. Correct.
- *Short relation, m ≠ 0.* With |x| ≤ H Euclidean, |m| ≤ ‖x‖₁ ≤ √3 H ≤ 3H. The representatives 0 ≤ v₁⁽ⁱ⁾ < w give an integer representative of m·a₁ of absolute value ≤ √3 H(w−1) < 3Hw, which contradicts (5.3) via ‖ma₁‖ = ‖|m|a₁‖.
- This branch needs no distinctness of the u⁽ⁱ⁾, which is exactly what the statement "for any u⁽¹⁾, u⁽²⁾, u⁽³⁾ ∈ V" claims.
- *Short relation, m = 0.* x ≢ 0 mod q because |xᵢ| ≤ H < q. Substituting x₃ = −x₁ − x₂ gives a nontrivial relation between u⁽¹⁾−u⁽³⁾ and u⁽²⁾−u⁽³⁾. Correct.
- *0 ∉ V.* This is the m = 1 condition. Correct.
- *Checks (`s52_shift.py`).*
  - Exact allowed-a₁ fraction, real constants, H ∈ {1,2,3,5,8}, three q each from 2003 to 7.7·10⁶: 0.9865 to 0.9889 in every case. The union bound gives about 0.018.
  - Exclusion logic over all x with |x| ≤ H and all ordered triples (repeats allowed) of shifted no-three-collinear sets, at (q,H,w) = (1009,2,20), (2003,2,15), (8009,2,2) and (40009,3,50): 7.2M relations checked, **0** violations, 0 ∉ V every time.
  - Negative control: a disallowed shift admits a relation, so the check can fail.

**Holds.**

**Prop 5.3.**
- *Uniform affine map.* For fixed G_q, G_q·a is uniform. So (G_q, G_q a) is uniform on GL₃ × F_q³ = AGL₃(F_q). Correct.
- *Transitivity and count.* (0, e₁, e₂) maps to any affinely independent (p₁,p₂,p₃) via v ↦ Mv + p₁ with Me₁ = p₂−p₁ and Me₂ = p₃−p₁. The count is q³(q³−1)(q³−q). Correct.
- *Triples in S.* Ordered affinely independent triples in S number exactly s(s−1)(s−2), because no three points are collinear.
- *Conditioning on a ∈ 𝒜.* Pr(E | 𝒜) ≤ Pr(E)/Pr(𝒜) ≤ 2Pr(E).
- *Rank ≥ 2 bound.* G_q⁻¹ is uniform on ordered linearly independent pairs, at most s² of which lie in S_a². Gives W ≤ q⁹/(s(q³−1)(q³−q)).
- *General bound.* One nonzero column, uniform among the q³ − 1 nonzero vectors, s of which lie in S_a. Gives W ≤ q⁹/(s²(q³−1)).
- *Support.* W > 0 means all three columns lie in some V. Distinct points of V are affinely independent, otherwise two columns are equal, and 0 ∉ V.
- *Check (`s53_weights_b.py`): exhaustive over all of AGL₃(F₃)* (11232 × 27 maps), S = Γ (9 points), all 27³ target triples.
  - With unrestricted shifts, W on every affinely independent triple equals the transitivity prediction 0.807692… exactly (one distinct value).
  - With shifts restricted so that 0 ∉ a + S (density 2/3, the toy analogue of 𝒜), the ratio of W to the explicit bound is: affine 0.75, rank ≥ 2 0.84, general 1.00 (≤ 1), and there are **0** support violations.
  - Control: with unrestricted shifts, 0 can lie in V, and the "no zero column" support claim fails 2029 times. So the support check can fail, and the 0 ∉ V consequence of Lemma 5.2 is what makes it pass.

**Holds.**

**(5.8), the normalization.** Given V, Pr(residues = (t₁,t₂,t₃)) = ∏1{tᵢ ∈ V}/s. Taking the expectation gives Pr(all tᵢ ∈ V)/s³ = W/q⁹, including repeated tᵢ. Independence from main-modulus data holds by construction (§5 last paragraph, §6). **Holds.** (The brief's "(5.6)" is the printed definition of W; the normalization identity is (5.8). Both checked.)

- **EXPOSITION (Prop 5.3 proof, line 2).** "Conditioning back on a ∈ 𝒜 increases the probability of any event by at most two." This should read "by at most a factor of two", since the bound is multiplicative.

---

## §6: the t = 0 hand-off in Prop 6.3

> "For t = 0, Proposition 7.1 below proves the stronger bound O(log(2N)N⁶/I²) for all matrices with rows in Λ and pairwise distinct projected columns. The orbit restriction only reduces this set."

Take A ∈ 𝒜₀. Then A mod h ∈ 𝒪, and Lemma 4.2 says every orbit element has the row span of C. So every row of A reduces into rowspan(C), i.e. lies in Λ_C. Together with columns in ℬ, det A = 0 and distinct projections, this gives 𝒜₀ ⊆ 𝒵. W is the same function in both places, and log(2N) ≤ (log 2N)². **Holds.**

- **EXPOSITION.** The inference "A mod h ∈ 𝒪 ⇒ rows in Λ" is spelled out only in the t ≠ 0 paragraph ("Every row of A belongs to Λ"). One clause repeating it for t = 0 would close the reader's loop.

---

## §7: Prop 7.1, Lemmas 7.2 and 7.3, and the three-case proof

**Lemma 7.2.**
- *g | E.* Primitivity gives x·ℤ³ = ℤ, and Eℤ³ ⊆ Λ.
- *J_x.* This is Lemma 2.3, general form.
- *g³/I ≤ h².* g³/I ≤ E³/(DE) = E²/D ≤ h².
- *Surjectivity.* v − qa·z (with x·z = 1) lifts any point of Π_x into ℤ³ ∩ x^⊥. Multiplying by E keeps it in Λ_x and stays surjective because q ∤ E: E is a power of the prime B < q.
- *(7.3).* A triple of independent vectors of length ≤ 4N forces λ₂(Γ) ≤ 4N, so Lemma 2.2 applies with det Γ = mJ_x.
- *Check (`s72_plane.py`).* 200 matrices C over B ∈ {2,3,5,7}, k ≤ 5, every (b,e), 2000 random primitive x. Compared J_x computed from an explicit integer basis of Λ ∩ x^⊥ against I|x|/g: **0** failures. g³ ≤ Ih²: 0 failures. Image of Λ_x mod q ∈ {11, 13, 101} has rank 2 inside Π_x: 0 failures.

**Holds.**

**Lemma 7.3.**
- *The equivalence.* x·Λ = ⟨(C̃x)₁, (C̃x)₂, (C̃x)₃, h·gcd(x)⟩. So for j ≤ k, B^j | g ⟺ B^j | (C̃x)ᵢ for all i ⟺ Cx ≡ 0 mod B^j. This is true for every x, primitive or not.
- *Density for j ≤ e.* Under y = Qx: y₁ ≡ 0 mod B^j, y₂ ≡ 0 mod B^{max(j−b,0)}, and y₃ is free because B^e ≡ 0 mod B^j. Fraction B^{−j−max(j−b,0)}.
- *The sum.* B^{3a} ≤ Σ_{j≤a} B^{3j} turns Σg³ into Σⱼ B^{3j}·#{Cx ≡ 0 mod B^j}. Each residue class has O((R/B^j)³) points because B^j ≤ h ≤ R; this is exactly where R ≥ h is used.
- The exponents 2j − max(j−b,0) increase strictly to b + e. So the sum is at most 2B^{b+e}, uniformly in B.
- *Check (`s7_lattice.py`).* 53 matrices with B ∈ {2,3,5}, k ∈ {2,3,4}, every (b,e) pattern including the singular cases e = k.
  - Exact density counts mod B^j, j ≤ e: **0** mismatches.
  - The B^j | g ⟺ Cx ≡ 0 equivalence over the full box for all j ≤ k: **0** mismatches.
  - g | E over primitive x: 0 failures. My first run checked all x; the 53 "failures" then were non-primitive multiples. That is my bug, and the lemma's primitivity hypothesis is genuinely used.
  - Σ_{prim, R≤|x|<2R} g³/(R³I) lies in [24.2, 24.8] for every B, b, e and R ∈ {h, 2h, 3h}. This is flat and equals the density of primitive vectors in the shell, (4π/3)·7/ζ(3) ≈ 24.4.

**Holds.**

**Proof of Prop 7.1.**
- *Rank and null vector.* Columns are nonzero (u₃ ≥ N) and pairwise non-proportional, so the rank is exactly 2. If some xᵢ = 0, two columns would be proportional. The cross product of two rows of length < 2√3N has norm ≤ 16N², so there are O(log 2N) dyadic shells.
- *(7.6).* (7.3) with det = mJ_x and J_x ≥ IR/g.
- *Exhaustive split.* By the support statement of Prop 5.3, W > 0 means either (1) residues affinely independent, or (2) some pair i < j of equal columns. Case (2) splits into x̄ ∉ F_qδ, and x̄ ∈ F_qδ with rank ≥ 2 or rank ≤ 1 mod q. That partition is complete. Summing over the three pairs only over-counts.
- *Case 1.* The last clause of Prop 5.3 gives |x| > H, so R > H/2 ≥ h and Lemma 7.3 applies. Contribution N⁶/(I³R³)·R³I = N⁶/I² per shell.
- *Case 2a (index-q claim).* The functional v ↦ v·δ vanishes on Π_x = x̄^⊥ iff δ ∈ F_q x̄, i.e. iff x̄ ∈ F_qδ. So it is nonzero here, and composing with the surjection Λ_x → Π_x gives index q. Power count: R³ · N⁶Ih²/(q³I³R³) · (q³/s)² ≪ N⁶/I² · h²q⁻³ · q²h²⁴ = N⁶/I² · h²⁶/q.
- *Case 2b.* The third coordinate of x is ≡ 0 mod q and nonzero, so |x| ≥ q and R > q/2. That gives q − 1 classes, each with (1 + R/q)³ ≪ (R/q)³ points, so R³/q² normals.
  - Rank ≥ 2: R³/q² · N⁶h²/(I²R³) · qh¹² = N⁶/I² · h¹⁴/q.
  - Rank ≤ 1: the rows lie in one of q+1 lines of Π_x, and the preimage of a line has index q in Λ_x (by surjectivity). That gives (q+1)·N⁶/(qJ_x)³, so R³/q² · N⁶h²/(q²I²R³) · q²h²⁴ = N⁶/I² · h²⁶/q².
- All three are ≪ N⁶/I² because q > h¹⁰⁰. Every shell contributes O(N⁶/I²) (Case 1 only for R > H/2), and there are O(log 2N) shells. The constants are absolute: they involve 2000³, Lemma 2.2's C, and Lemma 7.3's constant, with no dependence on C, h, q or N.

**Holds.**

- **EXPOSITION (Case 1).** "Lemma 5.2 excludes the relation Ax = 0 when |x| ≤ H." The citation that applies directly is the last sentence of Prop 5.3 (affinely independent and W(A) > 0 ⇒ no short relation). Lemma 5.2 needs a specific allowed (a, G_q), and W > 0 supplies one.

---

## §8: deletion, area identity, (8.1)–(8.8), interpolation

All of the following was recomputed symbolically in k (`s8_arith.py`) and by exact integer arithmetic (`s8_bounds.py`).

- **(8.2).** C(2n_r,2)/n_r ≍ n_r and C(2n_r,3)/n_r ≍ n_r², by linearity of expectation over 2n_r samples with shared (G_h, V). Correct.
- **First term.** n_r(hq)⁶N⁻³ ≤ rτ^{−1/2}(hq)⁶N^{−3/2} = rτ^{−1/2}(hq)⁻⁹. log_r exponent = 16 − 27285k < 0. Correct.
- **Second term.** At most (log 2N)²·(h/τ)·r^{2−d}. Here τ ≥ B^{k−1}/3 because ⌊y/2⌋ ≥ y/3 for y ≥ 3, so h/τ ≤ 3B ≤ 600k²r³⁰. log 2N = O_k(log r). Net exponent 32 − d, which is −9 at d = 41.
  - **d > 32 is exactly what is needed**, and d must also be odd for alternation (Lemma 3.1). Correct.
- **Deletion.** Z < n_r, at most Z indices marked, so more than n_r remain. Retained points are distinct, and every retained triple has |det| > τ. Correct.
- **(8.3)/(8.4).** Dividing column j by A₃ⱼ > 0 gives an exact identity. ∏A₃ⱼ < 8N³, so area > τ/(16N³). Correct.
- **a_r > rh^{29/2}.** a_r > r√(N³/h) ≥ r√(h³⁰/h). The actual margin in log_r is 45000k + 15. Correct.
- **(8.5).** n_r² Δ ≥ (a_r/2)²·τ/(16N³) = r²/64. Correct.
- **β, α, η.** 1515k − (k−1)/2 = (3029k+1)/2. α = 1 + 30β = 45435k + 16, which is also log_r a_r exactly. η = 2/α. sympy identities all True.
  - Two-sided bound √2·rB^β < a_r ≤ 2¹⁵√3·rB^β, checked squared in exact integers (2B^{3029k+1} < N³/τ ≤ 3·2³⁰·B^{3029k+1}): 540 cases, k ∈ {2,3,4}, B up to 10007, q at both ends of (h¹⁰⁰, 2h¹⁰⁰]. **0** failures.
  - For the actual k: k has 232 digits and η ≈ 10⁻²³⁶.
- **(8.6) constants.** A_k = (√2/2)(100k²)^β and D_k = 2¹⁵√3(200k²)^β depend on k only.
- **The "sufficiently large r" conditions are compatible.** Each is of the form r ≥ r₀(k), so all can hold together:
  - r is an odd prime.
  - Bertrand for B at 100k²r³⁰, and for q at h¹⁰⁰.
  - θ ≤ 200k²r⁻⁶ < 1/2.
  - EZ < n_r.
  - a_r ≥ 2.
- **(8.8).** r^α ≥ n_r/D_k gives r² ≥ D_k^{−η}n_r^η. Correct.
- **Interpolation (not covered by the Lean).**
  - m = ⌈(n/A_k)^{1/α}⌉, and Bertrand gives a prime r ∈ (m, 2m]. Since r > m → ∞, r is eventually beyond r₀(k).
  - n_r ≥ A_k r^α > A_k m^α ≥ n.
  - n_r ≤ D_k(2m)^α ≤ D_k 4^α n/A_k, using ⌈y⌉ ≤ 2y for y ≥ 1.
  - Restricting to n points can only raise the minimum, and −2 + η < 0, so Δ(n) ≥ c_*(C_k n)^{−2+η}.
  - The constants c₁ = c_* C_k^{−2+η} and n₀ depend only on k, which is fixed. Nothing depends on r or n.

**The every-n Theorem 1.1 follows from (8.6) as written.** This needs (8.6) to hold for every sufficiently large prime r, not just along a subsequence. It does: nothing in §§3–8 restricts r beyond r ≥ r₀(k).

---

## Appendix A

- **P(x) < 4^x.** The induction is right. For x = 2m+1, primes in (m+1, 2m+1] divide C(2m+1, m) < 4^m. Real x reduces to ⌊x⌋.
- **Bertrand argument.** C(2n,n) ≥ 4ⁿ/(2n+1). For each p, p^{v_p} ≤ 2n. Primes ≤ √(2n) contribute ≤ (2n)^{√(2n)}. Primes in (2n/3, n] have exponent 0 (both floors give 2 − 2·1, and p² > 2n). The rest is bounded by P(2n/3) < 4^{2n/3}.
- *Check (`sA_bertrand.py`).*
  - max over x ≤ 2·10⁵ of log P(x) − x log 4 is −1.386.
  - Every exponent claim holds for C(2n,n), 3 ≤ n ≤ 400 (0 violations).
  - The closing inequality holds for every n ≥ 468, which is what "sufficiently large" covers.

**Holds.**

---

## Interface dependencies (outside my sections, not re-refereed here)

§8 consumes three inputs from other sections:
- Lemma 3.3's obstruction (distinct labels ⇒ no representative in [−τ, τ]).
- Lemma 4.2's orbit bound (4.2), |𝒪| ≥ c₀h⁸/(D³E²).
- (4.7), the uniform moment E[D | labels] ≤ 2 for r ≥ r₀(k).

I checked only that the shapes match. Cor 6.4's h⁹/(N⁹|𝒪|)·N⁶/I² ≤ hD/(c₀N³) composes correctly, and the r-dependence of θ is 200k²r⁻⁶. R1's report covers §§2–4 and §6 with no FATAL or GAP, so the inputs §8 consumes are not contested.

---

VERDICT: HOLDS AS READ (§5 Lemmas 5.1, 5.2, Prop 5.3, (5.6)/(5.8); the Prop 6.3 t = 0 hand-off; §7 Prop 7.1, Lemmas 7.2, 7.3, all three cases and both subcases; §8 including the every-n interpolation; Appendix A. Three EXPOSITION notes, no GAP, no FATAL.)

**The three places I was most suspicious of, and what settled each:**

1. **Prop 5.3: uniform affine map, factor-2 conditioning, support statement.** I suspected the restricted shift might break the AGL-uniformity count, or that the support claim was asserted rather than derived.
   - Settled by the hand proof ((G_q, G_q a) is uniform on AGL₃; conditioning costs a factor ≤ 1/Pr(𝒜) ≤ 2).
   - And by the exhaustive AGL₃(F₃) computation: all three bounds hold with explicit constants (max ratios 0.75 / 0.84 / 1.00), and the support statement has 0 violations once 0 ∉ V. The control without that restriction does fail, which shows the check can see a violation.

2. **Lemma 7.3 and Case 1 of Prop 7.1: B^j | g(x) ⟺ Cx ≡ 0 mod B^j, the density, R ≥ h, uniformity in B.** These carry the only non-pointwise g-bound in the paper.
   - Settled by x·Λ = ⟨C̃x, h·gcd(x)⟩, and by exact checks over 53 matrices covering every (b,e) including singular ones: 0 equivalence mismatches, 0 density mismatches.
   - The normalized moment sits at a constant ≈ 24.4 independent of B, b and e. Case 1 uses the lemma only at R > H/2 ≥ h, where it applies.

3. **§8 bookkeeping and the every-n interpolation, which the Lean does not cover.** I suspected an r-dependent constant or incompatible "sufficiently large" conditions.
   - Settled by the symbolic recomputation: α = log_r a_r = 45435k + 16 exactly, the error terms have exponents 16 − 27285k and 32 − d = −9, and the a_r two-sided bound was checked in exact integers.
   - A_k, D_k and C_k are explicit in k. Every largeness condition is r ≥ r₀(k), and Bertrand on r with m = ⌈(n/A_k)^{1/α}⌉ gives n ≤ n_r ≤ C_k n.
