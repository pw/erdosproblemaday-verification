# Seat T report: sufficiency half (printed §1.3, §5, §6)

**Paper:** OpenAI, "A classification of finite Euclidean Ramsey configurations" (23 Sep 2026), Erdős #174.
**Scope:** printed §1.3; §5 (Prop 5.1, Lemmas 5.2–5.5, §5.1–5.3, eqs (19)–(21), Figure 1); §6 (Lemmas 6.1–6.3, Prop 6.4, the completion paragraph, eqs (22)–(30)).
**Read from:** `05-paths.tex`, `06-groups.tex`, `01-introduction.tex`, and the printed numbering in `paper.txt` (eqs (19)–(30) located by grep). I also read the statement of Lemma 4.1 (`04-pairs.tex`) and Prop 2.1/(alg:tensor) (`02-tensors.tex`), but only where §6 depends on them.
**Stance:** hostile. I went through every step of §§5–6, re-derived each one, and ran exact (sympy) toy instances. Each toy has negative controls that fire.

---

## 0. Bottom line

I found no FATAL problem and no GAP in §§5–6. The sufficiency argument, from "for every n there are equal-endpoint path pairs with weight ratio < 1/n" through to the Ramsey property, is correct as written. So is the construction of those pairs from Lemma 4.1's two-scale permutation data. Everything I object to is EXPOSITION or citation precision (§7).

Two things hold up under scrutiny:

1. **The scale-one problem is solved correctly.** The free-group endpoint is never turned into a point. It is used only to colour Hales–Jewett words, through the homomorphism ψ: K → p(βS)p. The realised distances come from the chosen path, specifically its weight. They do not come from the endpoint.
   - The line's variable count t is unknown before colouring. The paper absorbs this by preparing one endpoint w that admits paths of every weight 1/t, t ≤ n (Lemma 5.3).
   - Inverses (group-theoretic cancellation) occur only in diagonal factors. Those become common ultrafilter columns, and Lemma 5.5 realises them by one identical string in all roles, so they contribute exactly zero to every pairwise distance.
   - No continuity of the colouring is used anywhere. The only uniformity needed (the dimension D) comes from compactness (Lemma 5.2).
2. **The correction machinery of §6 is sound.**
   - Lemma 6.1: pair projections are groups containing N×N.
   - Lemma 6.2: L_i is normal, the cost is subadditive and conjugation-invariant, and N^(s−2) ⊂ L_i, proved by an induction using pair-supported fractions.
   - Lemma 6.3: orbit averaging first reaches derived depth s−2, then the cost/degree ratio contracts by (h−1)/h.
   - Prop 6.4: the arithmetic closes with q < 1/(2n) and δ = 1/(2sn).

The sufficiency direction is therefore **conditional only on Lemma 4.1** (and Prop 2.1, which hands Lemma 4.1 a symmetric tensor). Those are other seats' scope.

---

## 1. Proposition 5.1 and the definitions of §5

Definitions as printed:
- A **path** is a finite sequence of diagonal factors Δg (weight 0) and copy factors X_b = (ξ_{b_1}, …, ξ_{b_s}) with ‖b_i−b_j‖² = u‖a_i−a_j‖² (weight u).
- The **endpoint** is the product in K^s.

Since A has s ≥ 2 distinct points, u is determined by b, so the weight is well defined. Copy factors carry only positive letters, so every inverse in a path lives in a diagonal factor. This is load-bearing (see §4) and it holds by definition.

### Lemma 5.2 (compactness): holds

- The space {1,…,r}^E is compact (Tychonoff for finite discrete factors, which needs only the BPI, so ZFC).
- "Not monochromatic on the ordered copy b" depends on s coordinates and is clopen.
- A finite family of copies lies in some R^D, where an avoiding colouring satisfies the family. Hence the whole family is satisfiable on E.

No regularity of the colouring is used. The quantifier order is right: the conclusion "there is D for this r" is obtained after proving "every colouring of E has a copy". In that inner statement the copy may depend on the colouring freely.

### Lemma 5.3 (synchronisation): holds, arithmetic checked exactly

- With ρ = μ/λ < 1/n, the points α_t = (1/t − ρ)/(1 − ρ) satisfy 0 < α_n < … < α_1 = 1. Positivity uses 1/t ≥ 1/n > ρ.
- The map ξ_z ↦ ξ_{cz} with c = √(l/λ) > 0 is an endomorphism of K. It is applied coordinatewise, so both paths keep a common endpoint. It sends X_b to X_{cb}, multiplying the weight by l/λ, and keeps diagonal factors diagonal.
- Taking big pieces on [0, α_t] and small pieces on [α_t, 1] gives weight α_t + ρ(1 − α_t) = 1/t.
- The endpoint is the ordered product of the per-interval common endpoints, so it does not depend on the choices.

In toy (A) I ran this literally, in exact arithmetic with √ scalings. For n = 1…4 every synchronised path has weight exactly 1/t, and all n paths have one identical reduced endpoint word.

### Lemma 5.4 (βS, idempotent, group corner): holds

- (20) is the Hindman–Strauss product. It matches H–S Thm 4.12(b) verbatim (2012 2nd ed., checked).
- I re-derived associativity: both bracketings reduce to {x: {y: {z: xyz ∈ B} ∈ w} ∈ v} ∈ u, using (xy)⁻¹B = y⁻¹(x⁻¹B).
- Right translation u ↦ uv is continuous. δ_ε is a two-sided identity.
- The idempotent proof is the Ellis–Numakura argument, done correctly: H₀x = H₀, then {y: yx = x} = H₀, so x² = x.
- The corner p(βS)p is a group:
  - every y in it lies in L₀, so (βS)y = L₀ by (21) and p = vy;
  - (pvp)y = p gives a left inverse inside the corner;
  - a monoid with left inverses is a group, by the displayed one-line argument, which is correct.
- Small omission: Zorn needs the intersection of a chain to again be a compact left ideal. It is, and the text only says "nonempty" (see E1).

### Lemma 5.5 (simultaneous realisation): holds

- The invariant P_i⁻¹B ∈ q_{i,j}⋯q_{i,M} is preserved column by column. E_i = {x : (P_i x)⁻¹B ∈ v_i} lies in q_{i,j} by (20).
- In a common column, ∩_i E_i is a finite intersection inside one ultrafilter, so it is nonempty and one string serves all roles.
- In a principal column, z_{i,j} ∈ E_i.
- At the end, P_i⁻¹B ∈ δ_ε means P_i ∈ B.

This is the step that keeps common factors identical across roles. It is correct because the right-hand remainder v_i is fixed before column j is chosen.

---

## 2. Proof of Proposition 5.1 (the Hales–Jewett step): holds

Order of choices: r, then n = HJ(s, r) (depending on s and r only), then the hypothesis pair for this n, then w via Lemma 5.3, then p and ψ. None of these depends on the colouring c. The colouring of words is k(word) = the unique k with B_k ∈ ψ(w_{i_1})⋯ψ(w_{i_n}).

On a monochromatic line with variable set I, |I| = t:
- the role-i product is a product of common factors ψ(w_{c_m}) at fixed positions;
- at variable positions, ψ(w_i) is expanded along the weight-1/t path ending at w. Diagonal Δg gives the common column ψ(g). Copy X_b gives three columns: p (common), δ_{(b_i)} (principal, length 1), p (common).

Because ψ is a homomorphism and w = F₁⋯F_L in K^s, the column product equals ψ(word) in every role, so B_k lies in it. Lemma 5.5 then gives strings in B_k:
- common columns get one string in all roles;
- principal columns get the one-letter strings (b_i).

So all lengths agree and positions align. By (19) (disjoint coordinate blocks, so the J_j are orthogonal isometries), the squared distance between roles i and j is

Σ over copy factors in the t expanded paths of ‖b_i − b_j‖² = t · (1/t) · ‖a_i − a_j‖².

### Brief question (i), written out for s = 3

Take the path F = (Δg₁, X_b [weight u₁], Δg₂, X_{b'} [weight u₂]). Its endpoint is the free-group triple

w = (g₁ξ_{b₁}g₂ξ_{b'₁}, g₁ξ_{b₂}g₂ξ_{b'₂}, g₁ξ_{b₃}g₂ξ_{b'₃}).

This is **not** a point, and the paper never treats it as one. The role-i ultrafilter is

ψ(w_i) = ψ(g₁)·p·δ_{(b_i)}·p·ψ(g₂)·p·δ_{(b'_i)}·p.

Lemma 5.5 realises it as S₁ S₂ (b_i) S₃ S₄ S₅ (b'_i) S₆, with each S_k identical in all roles. So

‖Φ(z^{(i)}) − Φ(z^{(j)})‖² = ‖b_i−b_j‖² + ‖b'_i−b'_j‖² = (u₁+u₂)‖a_i−a_j‖².

That is the *path weight*, not a function of the endpoint. Now take a line (c, ∗, ∗) with t = 2. Each role is ψ(w_c)ψ(w_i)ψ(w_i), both ψ(w_i) are expanded by the weight-½ path, and the squared distances are 2·½·‖a_i−a_j‖². The group elements g₁, g₂, inverses included, never enter a distance.

### Brief question (ii), quantifier order

No choice depends on the colouring in a way that matters:
- n depends on (s, r);
- the paths, w, p and ψ depend on n;
- the realised copy may depend on c, and is allowed to;
- D comes from Lemma 5.2 afterwards, uniformly in c.

The Lean statement `paths_monochromatic` (ColoringCompactness.lean) has exactly this shape: `∀ c, ∃ b, congruent ∧ mono`, followed by `finite_coloring_compactness`.

### Brief question (iv), Hales–Jewett parameters

The alphabet is the label set {1,…,s}, the length is n = HJ(s, r), and a line has a nonempty variable set I with |I| = t ≤ n. Lemma 5.3 supplies exactly the weights 1/1, …, 1/n. This is the correct application. (Lean pads to n = |β|+1, which is harmless.)

### Why this does not run into Leader–Russell–Walters' Conjecture C

I fetched LRW (arXiv 1012.1350) and checked the paper's remark against it. LRW's Conjecture C fixes the active-set size before colouring ("there exist … n and d … |I| = d"), and they state that "without the restriction '|I| = d', Conjecture C would be an easy consequence of the Hales–Jewett theorem". The paper's remark in §5.3 is therefore an accurate citation.

The paper sidesteps the restriction by making the colour of a word depend only on the endpoint while the distances depend only on the chosen path. I tried to break this decoupling and could not: ψ(w_i) is path-independent because ψ is a homomorphism, and the realisation counts only principal columns.

---

## 3. §6: from coordinate permutations to equal endpoints

### Lemma 6.1: holds

- Any ordered pair at distance r = ‖a_i − a_j‖ extends to an ordered unit copy of A (choose an orthonormal frame inside finitely many coordinates of E).
- (x,y)⁻¹ = (x⁻¹,x⁻¹)(y,x)(y⁻¹,y⁻¹) holds (checked on random words). So M_ij is a monoid generated by elements whose inverses it contains, hence a group.
- It contains (xy⁻¹, 1) and (1, yx⁻¹) and their diagonal conjugates.
- The distance-r graph on E is connected: split a displacement into pieces of length ≤ 2r and use a perpendicular apex of height √(r² − d²/4).
- Edge differences telescope to every ξ_zξ_{z'}⁻¹, and the normal closure of those is N. So N×1 and 1×N lie in M_ij.

### Lemma 6.2: holds

- Inversion swaps numerator and denominator. Diagonal conjugation gives (du)(dv)⁻¹ with the same degree.
- (23): with h = v_i⁻¹gv_i one has v⁻¹g^{[i]}v = h^{[i]}, hence uv⁻¹g^{[i]} = (ua)(vb)⁻¹. Checked on 200 random instances.
- From these: L_i is a subgroup, it is normal, c_i is subadditive, and the tuple cost bound Σ_i c_i(g_i) holds.
- (24): b with b|_J = v|_J⁻¹ exists because M_J is a group, and t = vb then commutes with z because their supports are disjoint. Checked on 200 random instances.
- Induction for (22):
  - The hypotheses (contains the diagonal; pair projections are groups containing N×N) pass to every coordinate projection.
  - Lifting a fraction from the projection away from j gives z_a supported on {i,j} with value a at i.
  - The commutator z_a z_b z_a⁻¹ z_b⁻¹ has value [a,b] at i and is trivial at j and at k.
  - Repeated (24) makes it a right fraction, so [N^(s−3), N^(s−3)] ⊂ L_i.
  - The base case s = 2 is correct.

**Toy (D), s = 3, equilateral triangle.** I built the commutator correction literally following (24). Here a = ξ_zξ_{z'}⁻¹ and b = ξ_wξ_{w'}⁻¹ are edge differences in two orthogonal planes. The result is u = X_a·Δ·X_b·Δ·X_aux·Δ and v = X_a·Δ·X_aux·Δ·X_b·Δ, where every X is asserted to be a genuine unit equilateral triangle in E. Then uv⁻¹ = ([a,b], 1, 1) exactly, with |[a,b]| = 8 and cost 6. This is a concrete instance of N^(1) ⊂ L₁ realised by unit-scale copies.

### Lemma 6.3 (averaging): holds

**Membership part.**
- After right-normalising at x₀, the values on the orbit O lie in N^(r).
- In (27), each point of O is visited |H|/|O| times, so the image in the abelian group N^(r)/N^(r+1) is the same for every x ∈ O.
- Other orbits keep any condition modulo a normal subgroup G ⊲ K (the factors agree mod G term by term). The N^(r) are characteristic in N, hence normal in K.

**Toy (E), H = S₃ on R³, four orbits (sizes 6, 3, 1, 3), depth 0 → 1.** I tested membership in [N,N] *exactly*, using projected Fox derivatives into Z[t^{±1}]. The map N/[N,N] → ⊕_z Z[K/N] is injective; this is the relation-module embedding.
- Before averaging: differences are NOT in [N,N] (the instrument fires).
- After (27): every within-orbit difference is in [N,N] (words up to 15,540 letters, degree 1296).
- Control "product over H minus one element": orbits fail, as they should.
- A third "control" (skip one orbit) did **not** discriminate. Explanation: after the first diagonal normalisation every value already lies in N, so a single averaging round pushes *all* orbits to depth 1 at once. The paper's orbit-by-orbit processing is harmless overkill at this depth. I note this so that nobody reads that control as a pass.

**Cost part.**
- After normalisation every value on O lies in L.
- In (28) one factor of ∏_g w_{gx} is a = w_{x₀} (x₀ is in the orbit). Writing the product as PaQ gives w'_x = P(aQa⁻¹), so c(w'_x) ≤ c(P) + c(Q) ≤ (h−1)B, using conjugation invariance under all of K, which Lemma 6.2 gives.
- The degree multiplies by exactly h, so (29) contracts by ((h−1)/h)^k.
- (30) is a correct telescoping identity (checked on random words). It shows that other orbits' cost/degree ratios cannot increase.
- Values stay in L throughout, because P, Q, a ∈ L.

### Proposition 6.4: holds

H = S_ℓ, and Z is the union of the orbits of the f_i and g_i. Each g_i is *some* permutation σ_i of f_i, and σ_i may depend on i. This is fine because the restriction to (g₁,…,g_s) applies the *same* h to every g_i, so each factor is a q-scaled copy, while the per-i discrepancy r_i = w_{f_i}w_{g_i}⁻¹ is a within-orbit difference.

The weights are m and qm. The i-th component of D₊⁻¹D₋ is w_{f_i}⁻¹ r_i⁻¹ w_{f_i}, which lies in L with cost ≤ δm (identity checked). The tuple bound gives deg u + deg v ≤ sδm. Then

μ/λ = (qm + b)/(m + a) ≤ q + sδ.

### Completion paragraph, brief question (iii): closes

Lemma 4.1 gives q = η/(1+η) for any η > 0, so 0 < q < 1/(2n) is available. With δ = 1/(2sn), μ/λ ≤ q + 1/(2n) < 1/n, which is strict, and λ = m + a > 0. Prop 5.1 applies.

The interface types also match. Prop 2.1 delivers a flip-symmetric T with (e_i⊗e_i)(T) = 0 and G(T) = I_d, which is exactly Lemma 4.1's hypothesis. Lemma 4.1 delivers f_i, g_i ∈ R^ℓ with the exact distances and per-i coordinate permutations, which is exactly Prop 6.4's hypothesis.

---

## 4. §1.3 (overview) against the body

Every §1.3 sentence about §§5–6 matches the body:
- "endpoint is the coordinatewise product";
- "weight is the sum of the squared copy scales";
- "prepare one endpoint at weights 1, 1/2, …, 1/n before coloring";
- "realizes the products by finite strings, keeping common factors identical";
- "t(1/t) = 1";
- "compactness supplies a finite ambient dimension";
- "permutation averaging puts the discrepancies … in a subgroup … corrected by appending paths of unit-scale copies";
- "further averaging makes the total correction weight small".

The §1.3 sentences about §4 (Gaussian construction, discretisation, the convolution image) are outside my scope and were not checked.

---

## 5. Computations (all exact sympy; scripts in `seats/T_work/`)

| Check | What it tests | Result | Negative control |
|---|---|---|---|
| (A) `toy_paths.py` | A = {0,1}: a **genuine** equal-endpoint pair, P₁ = X_{(0,e)} (weight 1) and P₂ = Δ(ξ_e)·∏_{m<k} Δ(ξ_{y_m}⁻¹)X_{(y_{m+1},y_m)} (weight 1/k), with y_m = (1−m/k)e. Both have endpoint (ξ₀, ξ_e). Then Lemma 5.3 literally, then the HJ realisation with random lines and arbitrary strings in common columns (simulating Lemma 5.5's output) | n = 1…4, 30 line realisations, all distances exactly ‖a_i−a_j‖²; every column expansion multiplies back to the word in K | — |
| (B) `toy_paths.py` | Equilateral triangle, synthetic weight-1/t paths with diagonal words containing inverses, rational rotations, √u scales | 27 realisations exact, seeds 1–3 | — |
| (C) `toy_paths.py` | Can the bookkeeping fail? | — | role-dependent string in a common column: 6/6 caught; weight-1/t' path with t' ≠ t: 6/6 caught; unequal-endpoint pair fed to Lemma 5.3: caught |
| (D) `toy_groups.py` | Lemma 6.2 commutator correction built from real unit triangles | uv⁻¹ = ([a,b],1,1) exactly | copy factors asserted unit-congruent |
| (E) `toy_groups.py` | Lemma 6.3 derived step, exact Fox-derivative membership in [N,N] | all orbits pass after (27) | pre-averaging fails; non-uniform product fails; skip-orbit control does **not** discriminate (explained in §3) |
| (F) `toy_groups.py` | The identities in Lemma 6.1, (23), (24), (30) and Prop 6.4 | 200 random instances each, all pass | — |
| (G) `toy_invariant.py` | Sanity: is Prop 5.1's hypothesis consistent with "Ramsey ⇒ spherical"? | The homomorphism ξ_z ↦ ‖z‖² paired with an affine dependency λ gives φ(endpoint) = weight·Σλ_i‖a_i‖² for every path (40/40 random paths, collinear triple and square). So equal endpoints force equal weights for a non-spherical A: the criterion cannot fire on a non-spherical set, consistent with EGMRSS. For the square it gives 0 = 0, so no constraint. | λ = (1,−1,0), not an affine dependency: the identity fails 19/20 |

**Not checked computationally:** the ultrafilter choices themselves (non-constructive), and depth ≥ 2 of Lemma 6.3. Those are covered by proof-reading only.

---

## 6. Cited results (brief question (v))

| Citation | Used for | Says what is used? |
|---|---|---|
| Hales–Jewett [8] | existence of n = HJ(s, r) with a monochromatic combinatorial line with nonempty active set | Yes, the standard statement. |
| Shelah [22, p. 686, §1] | "We use only existence of the length" | Existence is all that is used. Page locator not verified; non-load-bearing. |
| Hindman–Strauss [9, Thm 2.5, Cor 2.6, Thm 1.42] | "fixes the multiplication convention" for (20) | Checked against the **2012 2nd ed.** (the paper cites the 1998 1st ed.; I could not check 1st-ed numbering). Thm 2.5 = Ellis–Numakura idempotent; Cor 2.6 = minimal left ideals are closed and contain idempotents; Thm 1.42 = eSe is a group for an idempotent in a minimal left ideal. These are exactly the facts Lemma 5.4 proves. The convention (20) itself is H–S **Thm 4.12(b)**, which is not cited (E2). Lemma 5.4 is fully proved in-text, so this is not load-bearing. |
| Ellis [3, Lemma 1] | "classical idempotent argument … taking the opposite semigroup matches the one-sided continuity" | Checked (msp.org PDF). Ellis assumes s ↦ ts continuous (left translations); the paper uses right translations. The "opposite semigroup" hedge is correct. |
| EGMRSS [4, Prop. 4] | "compare" for compactness | Not verified (EGMRSS I not fetched). Lemma 5.2's proof is self-contained, so non-load-bearing. |
| LRW [16, Conj. C and the following discussion] | remark that LRW prescribe the number of varying positions | Checked (arXiv 1012.1350): accurate, including LRW's own sentence that without |I| = d it follows from Hales–Jewett. |

---

## 7. Objections (all non-fatal)

**E1 (EXPOSITION), Lemma 5.4.** "Such an ideal exists because every chain of nonempty compact left ideals has a nonempty intersection." Zorn also needs the intersection to be a compact left ideal. It is (closed, and an intersection of left ideals), but the text does not say so. The same applies to "Choose a minimal nonempty compact subsemigroup H₀".

**E2 (EXPOSITION / citation), §5.2.** "The following standard construction fixes the multiplication convention; see [9, Theorem 2.5, Corollary 2.6, and Theorem 1.42]." Those results are the abstract semigroup facts. The convention (20) is H–S Thm 4.12(b) (2nd-ed. numbering). This is harmless because everything is reproved.

**E3 (EXPOSITION), Lemma 6.3, (27).** "Replace the resulting tuple by w'_x = ∏_{h∈H} w_{hx} … For x ∈ O, …" The operation must be, and implicitly is, applied at every x ∈ Z: a represented tuple is a product of factors indexed by all of Z, and the next sentence ("preserves any normal-subgroup condition already obtained on another orbit") presupposes it. Should say "for every x ∈ Z". Related, as my Fox-derivative check shows: at the first derived step all orbits are handled by one round.

**E4 (EXPOSITION), Lemma 6.3, (28).** w_{x₀} means the *current* value at x₀. It equals 1 only in the first iteration after normalisation. Correct as used, but worth a word.

**E5 (EXPOSITION), Lemma 6.1.** "Differences of letters along graph edges consequently generate, after taking their normal closure in K, all differences ξ_zξ_{z'}⁻¹." The differences are generated without any normal closure, by telescoping along a graph path. The normal closure is what turns them into N. The sentence conflates the two, but the conclusion N×N ⊂ M_ij is right.

None of these affects any statement.

---

## 8. What remains outside this seat

The sufficiency direction of Theorem 1.1 holds **if** Lemma 4.1 (the exact two-scale coordinate-permutation configurations, §3–§4) and Prop 2.1 hold. I checked only their statements and that their interfaces with §6 match.

The Lean development has files for §§5–6: PathWords, PathSynchronization, UltrafilterStrings, CornerGroup, ColoringCompactness, PathFractions, DerivedFractions, NormalCost, OrbitAveraging, CorrectionPaths. `grep` finds no `sorry`/`axiom`/`admit` in the EuclideanRamsey directory. Its `Path` inductive and `Ramsey` comparator definition match the paper's: `dist` equality (scale one), arbitrary `c`, `1 ≤ D`. Its `synchronize_paths` uses a slightly different chain from the paper's interval partition, with the same conclusion. I did not compile; the coordinator's kernel replay is the authority there.

VERDICT: HOLDS AS READ
