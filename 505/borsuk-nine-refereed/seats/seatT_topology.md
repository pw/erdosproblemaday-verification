# Seat T: the topological reduction (Sections 2, 3, 4; Lemma 5.2; Lemma 6.1; topological inputs to Theorem 6.5)

**VERDICT: HOLDS AS READ.** Nothing FATAL and no GAP in Sections 2–4, Lemma 5.2, Lemma 6.1, or the topological facts that Sections 6.2–6.5 import. Every objection below is EXPOSITION: a step that is correct but compressed. Every citation I could check against the source is correct. The Lee citations were checked from memory only, not against the text.

Referee: Seat T (Claude, hostile reading). Paper: OpenAI, "A nine-dimensional counterexample to Borsuk's covering assertion", 23 Sep 2026. Page numbers below are the printed ones.

## How I checked

- I read pp. 3–16 line by line. I rendered pp. 4, 6, 7, 9, 10 and 11 at 110 dpi and checked every displayed formula in scope against the image, not against pdftotext. The text matched in all cases. The one sentence that looked garbled in pdftotext ("projection from x0⊥ onto u") reads "onto u⊥" in the PDF, which is correct.
- I checked the Hatcher citations against the books, fetched once into `seats/T_refs/`:
  - AT Prop. 2B.6: an odd map Sⁿ→Sⁿ has odd degree.
  - AT Cor. 2B.7: Borsuk–Ulam, every g: Sⁿ→ℝⁿ has some x with g(x)=g(−x).
  - AT Thm. 2.27: Δ-homology equals singular homology.
  - AT Thm. 3.19: H*(ℝPⁿ;ℤ₂) = ℤ₂[α]/(αⁿ⁺¹).
  - VBKT Thm. 3.1(a): naturality of Stiefel–Whitney classes.

  All five are the right statements.
- Lee, *Introduction to Smooth Manifolds*, 2nd ed., checked from memory only: Thm. 2.23 is existence of partitions of unity, Cor. 5.14 is the regular level set theorem, Thm. 6.10 is Sard. These match what the paper uses.
- I ran numerical controls (`seats/T_scripts/`, all under ulimit and timeout). They are described at the end. They are consistency checks, not proofs.

---

## 1. Lemma 2.4, the strict-gap reduction (pp. 4–5): HOLDS

- **Open thickenings.** "εi = (√2 − di)/4 > 0 … Ui = {P ∈ Xk : distF(P, Ai) < εi}" gives relatively open sets that cover X_k. Every P lies in some nonempty A_i, so its distance to that set is 0 < ε_i.
- **Diameter bound.** "∥P − Q∥F < di + 2εi = (di + √2)/2 < √2" is correct. If dist(P, A_i) < ε_i then some a ∈ A_i has ∥P−a∥ < ε_i, so ∥P−Q∥ < 2ε_i + d_i. The argument works whether the A_i are subsets of X_k or of the ambient space.
- **Pull-back.** x ↦ P_x is a homeomorphism (Lemma 2.1), so the V_i form a finite open cover of P(V).
- **Partition of unity.** Lee Thm. 2.23 gives a smooth partition of unity indexed by the same index set with supp f_i ⊂ V_i. Hence f_i(x) > 0 implies x ∈ V_i.
- **Admissibility (2.3).** If i ∈ S(x) ∩ S(y) with x ⊥ y, then P_x, P_y ∈ U_i are at distance √2 by (2.1). That contradicts diam U_i < √2.
- Lemma 2.1 and (2.1) hold: tr P_x² = 1 and tr(P_xP_y) = ⟨u,v⟩². Remark 2.2 (2.2) is an affine isometry onto ℝ⁹; I checked it numerically to 2e-15.

## 2. Lemma 3.1 (pp. 5–6): HOLDS

- **Continuity on the whole PSD cone, singular boundary included.** Q ↦ Q^{1/2} is continuous on the PSD cone (the uniform polynomial approximation argument is valid). H is continuous at 0 because ∥H(v)∥₁ = ∥v∥². So the integrand is jointly continuous on (bounded set of Q) × compact sphere, and the integral is continuous.
- **Σ_i E_V(Q)_i = tr Q.** Σ H_i = ∥v∥² and ∫uuᵀ dμ = k⁻¹I, so k∫⟨Qu,u⟩ dμ = tr Q.
- **Support identity (3.2), both directions.**
  - ⊆: a positive coordinate needs some u with Q^{1/2}u ≠ 0 and f_i([Q^{1/2}u]) > 0, and Q^{1/2}u lies in ran Q.
  - ⊇: Q^{1/2} is invertible on ran Q, so every line in ran Q equals [Q^{1/2}u₀]. The i-th integrand is positive on a neighbourhood of u₀, and μ_V gives positive mass to nonempty open sets. For dim V = 1, S(V) is two atoms of mass ½ each, so this still holds.
- **E_V(P_x) = f(x).** P_x^{1/2}u = ⟨u,e⟩e and k∫⟨u,e⟩² dμ = 1.
- **Subspace identity.** I checked the measure computation. ν(B) = ∫∥π_W u∥² 1{…} dμ_V is O(W)-invariant: extend g ∈ O(W) by the identity on W⊥; μ_V is invariant and π_W commutes with this extension. Its total mass is ∫∥π_W u∥² dμ_V = tr(π_W)/k = r/k. Uniqueness of the invariant probability measure on S(W) gives ν = (r/k)μ_W, including r = 1. Then Q^{1/2}u = (Q|_W)^{1/2}π_W u and degree-2 homogeneity give k·(r/k)∫_{S(W)} = r∫_{S(W)}, which is the stated identity with factor dim W.
  - Numerically, total mass is 0.2503 / 0.5005 / 0.7500 against r/k = ¼, ½, ¾.
  - Numerically, E_V(Q) − E_W(Q|_W) agrees to Monte Carlo error for r = 1, 2, 3 in k = 4 (1.5e-4, 1.2e-3, 4.5e-3 on coordinates of size 0.7–4). A wrong dimension factor would be off by a factor k/r.
- **Local smoothness, item (3).** In a local smooth orthonormal frame T, (Q|_W)^{1/2} becomes TC^{1/2}Tᵀ, and the integral over the frame sphere is r∫H(TC^{1/2}w). TC^{1/2}w ≠ 0, H is smooth off 0 (f is smooth and v ↦ [v] is a submersion), and the domain is compact, so differentiation under the integral is legitimate.

## 3. Lemma 3.2 and the paragraph on smooth structures (pp. 6–7): HOLDS

- **Oddness.** (−A)₊ = A₋.
- **(3.4) and (3.5), "no cancellation".** The ranges of A₊ and A₋ are orthogonal. Admissibility plus (3.2) make the positive label sets of E(A₊) and E(A₋) disjoint. So F(A)_i > 0 exactly when E(A₊)_i > 0, and F(A)_i < 0 exactly when E(A₋)_i > 0. Summing gives ∥F(A)∥₁ = tr A₊ + tr A₋ = tr|A| and Σ_i F(A)_i = tr A.
- **Nonsingularity.** A kernel line x is orthogonal to both spectral ranges. A label i ∈ S(x), which exists because Σ f = 1, therefore appears in neither union, so F(A)_i = 0.
- **All coordinates negative implies negative definite.** E(A₊) has no positive coordinate, so E(A₊) = 0, so tr A₊ = 0, so A₊ = 0. Nonsingularity then gives A < 0.
- **Smoothness on nonsingular operators.** Π± = ½(I ± A(A²)^{−1/2}) = ½(I ± sign A) is smooth where A² > 0. Local frames come from Gram–Schmidt, and Lemma 3.1(3) finishes it.
- **Smooth structures and mod-2 degree** ("Consequently ordinary sphere degree applies to (3.6) when m = Nk, and local differential arguments are valid at every preimage of a full-support value"). This is legitimate.
  - Degree is a homological invariant of continuous maps. The radial maps A ↦ A/∥A∥_F and y ↦ y/∥y∥₂ are equivariant homeomorphisms, so F becomes an odd continuous self-map of S^{N_k−1}.
  - Near nonsingular A, tr|A| = tr(AΠ₊) − tr(AΠ₋) is smooth with radial derivative tr|A| ≠ 0. So {tr|·| = 1} is a smooth hypersurface there, and the radial map is a local diffeomorphism.
  - In an open sign orthant the ℓ¹ norm is linear.
  - Full-support preimages are nonsingular by the lemma, so the local smoothness is available exactly where Lemma 4.2 needs it.

## 4. Proposition 4.1 (p. 8): HOLDS

- **Citations.** "An odd map Sⁿ → S^d requires n ≤ d, and an odd self-map of Sⁿ has odd degree; see [8, Proposition 2B.6 and Corollary 2B.7]." Both facts are right.
  - The second fact is Prop. 2B.6 verbatim.
  - The first fact is not stated verbatim. It is the one-line consequence of Cor. 2B.7: if d < n, compose with S^d ⊂ ℝ^{d+1} ⊆ ℝⁿ; Borsuk–Ulam gives g(x) = g(−x) = −g(x), so g(x) = 0 ∉ S^d.
  - EXPOSITION: the citation pairs the two facts with 2B.6 and 2B.7 in reverse order, and the derivation of the first fact is left implicit.
- **Surjectivity.** A map of nonzero mod-2 degree cannot miss a point.
- **Edge assertion** ("That subspace cannot have dimension at least two: restriction to a two-dimensional subspace would contradict the bound N₂ = 3 just proved").
  - The positive spectral subspace is nonzero because y has positive coordinates.
  - All of its lines use only labels {i, j}, by (3.5).
  - On a 2-plane inside it, f restricts to an admissible map with 2 < 3 labels, using the "coordinates that vanish identically may be omitted" remark on p. 4.
  - So it is a line x, and (3.5) gives S(x) = {i, j}.
  - The bound for k = 2 is proved before it is used, so the argument is not circular, and it also covers k = 2 itself.

## 5. Lemma 4.2, local counting (p. 8): HOLDS, and every application meets its hypotheses

- **Proof.** {y} is closed (Y Hausdorff), the fibre is closed in compact M, the inverse function theorem isolates its points, so it is finite. Excision splits H_n(M, M∖fibre). The fundamental class has coordinate 1 in each summand (F₂ coefficients, any component). Each local homeomorphism sends generator to generator. Only smoothness near the fibre is used.
- **Use 1: F at y = (λr, (1−λ)g).** F is continuous globally and smooth near the fibre, because preimages are nonsingular and the coordinates are compatible with the transported structure (item 3).
- **Use 2: Ḡ at [g].** Smooth near preimages via local sections of the double cover.
- **Use 3: each G_x at g, in the a = h case.** At preimages B is negative definite, so G_x is smooth there.
- **Use 4: f: P(V) → |K| at r̃.** Y = |K| is not a manifold, but the lemma needs only a Euclidean neighbourhood of y. Here that neighbourhood is {p ∈ |K| : p_i > 0 ∀ i ∈ I}, which is open in |K| and equal to relint|I| (see item 6.10). Only the local-homology form of the conclusion is used here, not "degree".

## 6. Theorem 4.3, the core (pp. 9–11): HOLDS

1. **Witness line.** "Since I is a maximal support face, there is a line x0 with S(x0) = I." I ⊆ S(x₀) for some x₀, S(x₀) ∈ K, and maximality forces equality.
2. **(4.1).** Lines in x₀⊥ use only J labels, and dim x₀⊥ = k−1 ≥ 2 (this is where k ≥ 3 is needed). Prop. 4.1, after dropping the identically-zero I coordinates, gives a ≥ h, so s ≤ N_k − N_{k−1} = k.
3. **U_I sits in the affine chart.** Lines orthogonal to x₀ carry no I label, so they are not in U_I. Maximality gives S = I on U_I, so f_I maps U_I into the open simplex.
4. **Sard and compactness.** Sard (Lee 6.10) applies to f_I: U_I → Δ̊_I, a smooth map between manifolds of dimensions k−1 ≥ s−1. L = f_I⁻¹(r) = f⁻¹(r̃) is closed in P(V), hence compact. It is a regular level set of dimension (k−1) − (s−1) = k − s.
5. **Dimension count (4.2).** k − s = a − h because N_k − k = N_{k−1}.
6. **G_x and continuity as a bundle map.** "The subspace-restriction and continuity properties of the extension make these maps a continuous map on the corresponding sphere bundle." True. By Lemma 3.1(2), G(x,B) is the J-block of F_V(B̂), where B̂ is B extended by 0 on x, and (x,B) ↦ B̂ is continuous.
   - EXPOSITION: this one-line reason is not written out.
7. **Trivialisation (4.3).** Projection x₀⊥ → u⊥ has kernel x₀⊥ ∩ ℝu = 0 because ⟨u,u₀⟩ ≠ 0, so it is invertible and smooth in x. Gram–Schmidt gives an orthonormal frame. Conjugation by it preserves tr|·| and commutes with B ↦ −B, and so does the radial change. So the antipodal map is fibrewise. Smooth structure: the trace-norm parametrisation is smooth near definite B (tr|B| = ∓tr B there).
   - Also checked: dim M = (a−h) + (h−1) = a − 1.
8. **"Odd parity on the bundle".**
   - A negative-orthant value forces B₊ = 0 by (3.5). A kernel line would carry a J label absent from both unions, so B is negative definite. This is the nonsingularity clause of Lemma 3.2 applied in x⊥.
   - G is smooth there by Lemma 3.1(3), with W = x⊥ varying smoothly and −B positive definite.
   - Sard applies on the open set G⁻¹(orthant).
   - "Its preimage is finite by compactness": finiteness also uses that preimages of a regular value in equal dimensions are isolated. EXPOSITION.
9. **Bijection F⁻¹(y) ↔ G⁻¹(g).**
   - A ∈ F⁻¹(y) is nonsingular.
   - A positive spectral subspace of dimension ≥ 2 would meet the hyperplane x₀⊥, giving a line with labels in both I and J, which is impossible. So it is a line x, and (3.5) gives S(x) = I.
   - The positive mass is tr A₊ = λ, and tr|A| = 1 forces tr|B| = 1 for B = −A₋/(1−λ).
   - The subspace formula gives F(A) = (λ f_I(x), (1−λ) G_x(B)), using G_x(B) = −E_{x⊥}(−B) for B < 0.
   - Converse: λP_x + (1−λ)B̂ is already a spectral decomposition with orthogonal ranges.
   - The map is injective, because x and B are recovered from A.
10. **Regularity (4.6): is the derivative really block-triangular?** Yes.
    - Source coordinates: (λ′, x′, z′), with x′ near x in the open set U_I (not only in L) and z′ in the trivialised fibre.
    - Target coordinates: (μ, y_I/μ, y_J/(1−μ)), a diffeomorphism of the sign orthant onto (0,1) × Δ̊_I × (open (a−1)-simplex).
    - In these coordinates the map is exactly (λ′, f_I(x′), G_{x′}(z′)). The Jacobian is [[1,0,0],[0,Df_I,0],[0,∂ₓG,∂_zG]].
    - ker of the first two rows = 0 ⊕ T_xL ⊕ T(fibre) = T_{(x,B)}M. On it the third row is d(G|_M), which is surjective since g is regular. Surjectivity of the whole follows by the usual two-step solve.
    - Dimensions: 1 + (k−1) + (h−1) = N_k − 1 = m − 1 = 1 + (s−1) + (a−1).
    - EXPOSITION: the paper does not say that M sits inside the bundle over U_I as π⁻¹(L) with the same chart-trivialised smooth structure. That fact is what "on the kernel … is the derivative of G|M" uses. It is true.
11. **(4.7).** F has odd degree (Hatcher 2B.6). Lemma 4.2 applies by use 1 in item 5. So |F⁻¹(y)| is odd, and therefore L ≠ ∅.
12. **Stiefel–Whitney step (4.8) and degree zero when a > h.**
    - The map (x,z) ↦ ((x,[z]), G(x,z)) is a continuous, equivariant bijection of double covers over the same base, hence an isomorphism.
    - w₁ is natural (VBKT 3.1(a)). The source cover is pulled back from ℝP^{h−1} because the bundle is globally trivial over the chart. This is the essential point: a nontrivial x⊥-bundle would add w_i(E)-terms in H*(L).
    - Then Ḡ*(w^{a−1}) = pr₂*(u^{a−1}) = 0 because a−1 ≥ h, and H*(ℝP^{h−1}) is truncated at degree h−1 (AT 3.19).
    - Disconnected L: handled, since the paper evaluates on the total fundamental class with F₂ coefficients.
    - Empty L: excluded by (4.7). Even if L were empty, the argument would still give 0 ≠ 1, so emptiness creates no loophole.
13. **Counting through the quotient Ḡ.** Exactly one representative of each preimage of [g] maps to g, since g ≠ −g. Near that representative Ḡ = π_a ∘ G ∘ (local section), which is smooth with invertible derivative. So smoothness near preimages of −g is never needed (it also holds by oddness). The count is |G⁻¹(g)|, which is odd, against degree 0. This contradiction gives a = h and s = k.
14. **The a = h case (4.9).**
    - With dim L = 0, M is the disjoint union of fibres S^{h−1}. Regularity of g for G is fibrewise regularity.
    - Each G_x is an odd self-map of S^{h−1} with h − 1 ≥ 2 (connected), so it has odd degree, and by Lemma 4.2 |G_x⁻¹(g)| is odd.
    - So |L| ≡ |G⁻¹(g)| ≡ 1 (mod 2).
15. **Facet coefficients via local homology.**
    - {p ∈ |K| : p_I > 0} is open in |K|. Any p in it has supp p ⊇ I, and supp p is a face (a subset of some face), so supp p = I by maximality. Hence this set equals relint|I| ≅ ℝ^{k−1}.
    - A simplicial top cycle Σc_σσ maps to c_I in H_{k−1}(|K|, |K|∖r̃), since every σ ≠ I lies in |K|∖r̃. Combined with AT 2.27 this is correct.
    - "Top homology classes are exactly top cycles" is correct: with no k-simplices, H_{k−1} = Z_{k−1}. Every (k−1)-simplex is a facet, because no face has more than k vertices.
    - Each facet gets coefficient |L| ≡ 1, so the sum of all facets is the cycle f_*[P(V)].
16. **Purity and positivity.** Every (k−2)-face lies in some maximal face, and all maximal faces have k vertices. Even incidence comes from ∂ = 0.

## 7. Lemma 5.2 (p. 12) and Lemma 6.1 (p. 13): HOLD

**Lemma 5.2.**
- Theorem 4.3 applies with k = 3 ≥ 3 and m = 6 = N₃: the complex is pure of dimension 2, all 15 edges are present, and every edge has positive even multiplicity.
- No two complementary triples are both triangles: in ℝ³ some line is orthogonal to both witness lines, and its support would have to avoid all six labels.
- Counting: at most 10 triangles (one per complementary pair) and 3t ≥ 2·15. Equality holds throughout, which gives exactly Definition 5.1.

**Lemma 6.1.**
- **The restriction is a smooth admissible map using all six labels.** "The restriction of f to P(x⊥) ≅ RP2 uses only labels in C. It uses all six: otherwise the lower bound in Proposition 4.1, applied in dimension three, would be violated."
  - S(x) = S exactly, because S is maximal.
  - Lines in x⊥ avoid S by admissibility, so the S-coordinates vanish identically on P(x⊥).
  - The restriction to the embedded submanifold P(x⊥) is smooth, and orthogonality inside x⊥ is orthogonality in V, so it is admissible into Δ^C.
  - All six labels are used by Prop. 4.1 with N₃ = 6. Lemma 5.2 does not actually need this.
  - The support complex of the restriction is a subcomplex of K.
- **"No additional triangles."** If T ⊆ C were a triangle of K outside T_C, then C∖T ∈ T_C ⊆ K. Witness lines for S, T and C∖T are three lines in ℝ⁴, and some line is orthogonal to all three. Its support would have to avoid all 10 labels, which is impossible. This is correct, and here the k = 4 fact (3 lines in ℝ⁴) is used in a k = 4 statement.
- **No two disjoint tetrahedra.** A tetrahedron disjoint from S would place all four of its triples in T_C, which Lemma 5.3(2) forbids. Lemma 5.3 itself is combinatorial and outside my scope.

**Topological inputs to Section 6.2–6.5, all correctly stated.** Sections 6.2–6.5 use only these:
- K is pure of dimension 3 (used in Lemma 6.4 and Theorem 6.5, "By purity…").
- Every triangle lies in a positive even number of tetrahedra (Lemma 6.2).
- T_C is exactly the set of triangles of K inside C (the "on which both systems are the triangles of K" step in Lemma 6.2, and the step in Lemma 6.3).
- No two tetrahedra are disjoint (end of Lemma 6.4).
- The existence of a tetrahedron S (Theorem 6.5), which follows because K ≠ ∅ and every face lies in a 4-vertex facet.

Each of these is exactly what Theorem 4.3 (k = 4) and Lemma 6.1 prove.

## Small-k and k = 4 leakage

I found no case where a k = 4 fact is used in a general-k statement, and no general-k step that fails for small k.
- **k = 2:** Prop. 4.1 is stated for k ≥ 2, and its edge step uses the k = 2 bound, which is proved first.
- **k ≥ 3 in Theorem 4.3:** this restriction is explicit and is used exactly where needed, for Prop. 4.1 on x₀⊥ (dim ≥ 2) and for h − 1 = N_{k−1} − 1 ≥ 2 (connected fibre spheres, ℝP^{h−1} with h−1 ≥ 2).
- **r = 1 in Lemma 3.1:** the invariant measure on S⁰ is still unique, and I confirmed this numerically.
- **Geometric facts:** "A line perpendicular to both exists" (ℝ³, Lemma 5.2) and "In ℝ⁴ there is a line perpendicular to all three" (Lemma 6.1) are both used only in their own dimension.
- **Lemma 2.4** needs k ≥ 2 for the diameter to be √2 (Lemma 2.1), which is stated.

## Numerical controls (`seats/T_scripts/`)

- **`lemma31_check.py`** (k = 4, generic smooth non-admissible f, 2·10⁶ samples):
  - (2.1) and the (2.2) isometry hold to 2e-15.
  - E_V(P_x) = f(x) to 5e-5.
  - Σ E_V(Q)_i = tr Q to Monte Carlo error.
  - The subspace identity holds for r = 1, 2, 3, and the pushed mass equals r/k.
- **`k3_control.py`, `k3_L.py`, `k3_Gx.py`.** I built an explicit admissible map ℝP² → Δ⁵ from smooth bumps on caps of radius 40° around the six icosahedral axes. Two points in one cap are at most 80° < 90° apart, so it is admissible. This is a nonvacuous positive control for Theorem 4.3 at k = 3 and for Lemma 5.2.
  - The support complex is pure of dimension 2, with all 15 edges, every edge in exactly 2 triangles, and exactly one triangle from each complementary pair. This is the 6-vertex ℝP².
  - |L| = |f⁻¹(r̃)| = 1 for all 10 facets × 2 random r, matching (4.9).
  - For x ∈ L, |G_x⁻¹(g)| = 1 for 6 random g in the negative orthant, matching the odd count behind (4.7) at the k = 2 level.
  - The assert that P(x⊥) carries no I label never fired.
  - Caveat: the root counts come from seeded Newton solving, which can undercount but cannot overcount. They corroborate the theorem; they do not prove anything.

## EXPOSITION notes (no fixes required)

1. **Prop. 4.1, p. 8.** The fact "odd map Sⁿ→S^d needs n ≤ d" is the one-line corollary of Hatcher Cor. 2B.7, not a stated result, and the two facts are cited with 2B.6 and 2B.7 in reverse order.
2. **Thm 4.3, p. 9.** Continuity of G on the bundle deserves the one-line reason G(x,B) = F(B̂)|_J.
3. **Thm 4.3, p. 10.** "Its preimage is finite by compactness" also needs regular-value isolation.
4. **Thm 4.3, p. 10, (4.6).** The coordinates range over the bundle above an open subset of U_I. The identification of M = π⁻¹(L) with the chart-trivialised structure is used implicitly.
5. **Thm 4.3, p. 11.** Smoothness of Ḡ near preimages of [g] is via local sections of the cover. This is implicit but immediate.
6. **Lemma 2.4, p. 4.** It does not say whether the A_i are subsets of X_k or of the ambient space. The proof works either way.

## Side note on the Lean formalisation (from file and lemma names only; I did not read the proofs)

The formalisation appears to implement the signed extension (`SphereGeometry/SphereExtension.lean`, `OddSphereMap.lean`) and a regular-facet parity lemma (`LocalParity/MatrixParity.lean: Admissible.regular_facet_level_odd`). However, it seems to replace singular degree theory and Stiefel–Whitney classes with simplicial approximation plus a ℤ/2 "characteristic degree" / Smith-cochain machinery (`Simplicial/*`, `SmithTheory/*`).

So a green kernel replay would certify the theorem, but not the paper's printed differential-topology route line by line. This seat's reading is therefore independent of the replay, not redundant with it.
