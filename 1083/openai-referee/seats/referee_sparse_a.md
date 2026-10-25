# Referee report — sparse_a: §6 preamble, §6.1–6.2 (PDF pp. 42–51), Theorem 6.1

Reviewer tag: sparse_a. Paper: /tmp/oaimath/166/paper.pdf (sha256 37f63553…, "September 23, 2026").
Scope: Theorem 6.1 as stated vs its use on p. 8; the top-level logic of its proof across §4–6; §6.1 (Lemma 6.2, Lemma 6.3, (6.6), (6.7)) line by line; §6.2 (Lemma 6.4 and the endpoint count) line by line.
Displayed formulas were read from the rendered PDF pages 42–51, not from the text extraction. The pdftotext output drops the square in (6.5): the PDF reads H(T_s(b)) ≥ σ(b)² min(1, T_s(b)/(D₁D₂)) exp(−o(s)).

**Verdict for this scope: HOLDS AS READ, conditional on the internal inputs listed at the end. Those inputs belong to the algebra and secants scopes; I read them but did not certify them.** I found no FATAL objection and no GAP inside pp. 42–51. Every objection below is UNCLEAR (exposition) or COSMETIC.

---

## 0. Theorem 6.1 as written vs its use on p. 8

**§6, p. 42 (verbatim):** "Theorem 6.1 (Sparse cones). Along a sequence with M = o(A), there cannot be families C_p, one for each p ∈ P, of irreducible projective curves, each spanning projective dimension at most two, such that deg C_p ≤ E = δN/A, δ → 0, and 1 − o(1) of the unordered pairs {p, q} satisfy π_p(q) ∈ C_p or π_q(p) ∈ C_q."

**p. 8 (verbatim):** "In the regime (2.1), one cannot assign to each p ∈ P a union C_p of irreducible projective curves, each spanning a projective space of dimension at most two, with deg C_p ≤ δN/A, δ → 0, such that all but o(N²) unordered pairs {p, q} satisfy π_p(q) ∈ C_p or π_q(p) ∈ C_q. This is Theorem 6.1. Both the alternative between the two endpoints and the absence of a prescribed rate for δ are important."

Comparison:
- "1 − o(1) of the unordered pairs" and "all but o(N²) unordered pairs" are equivalent, since there are about N²/2 pairs.
- Both versions use the either-endpoint OR, both have no rate on δ, and both require each component to span at most P².
- §6 defines a "directional curve family" as finite, and the greedy procedure on p. 9 produces finitely many curves. The curves are complex, and the directions are real points of complex P^{d−1}.
- The use on p. 9 is the exact negation. A pair that does not survive was either rich-line discarded (O(N²/H) + o(N²) = o(N²) as H → ∞), or removed at p (so π_p(q) lies on a recorded curve at p), or removed at q. The total degree is at most N/(KA), so δ = 1/K → 0.
- **MATCH.** The only difference is in the hypotheses; see Objection 1.

## 1. Top-level logic of the proof of Theorem 6.1 (ten lines)

1. Assume families C_p exist: (2.1) holds in the least failing d, E = δN/A, δ → 0 at any rate, and coverage at either endpoint holds for 1 − o(1) of the unordered pairs.
2. **Partition (Prop 5.1).** Choose s* → ∞ with δe^{6s*} → 0. All but o(N) points split into a core (isolated at degree L with EL² = o(N)) and non-core pieces of dyadic width s ∈ [s*, log B]. Each piece has a path of d proper cuts with limiting times b₁ ≤ … ≤ b_d.
3. **Budgets (Prop 5.2).** Σb_i = 0, b₁ < 0 < b_d, b₁ + b₂ < 0. The carrier mass budget is (5.8) and the rank bound is (5.9).
4. **Selection (Prop 5.5).** Every point gets a global terminal curve (its carrier after the (d−1)st cut). Prop 4.3 deletes the o(N²) ordered incidences with π_p(Y_q) ⊆ C_p. A light-line restriction keeps only lines with at most B^{o(1)} points. Binning then gives one of three cases: (1) a positively covered core; (2) two pieces with a common width and profile, or at s = log B one pool of exp(o(s)) pieces with mass ≥ N√δ, covered in one chosen orientation; (3) two pieces whose width ratio → ∞, same profile, covered in one orientation.
5. **Case (1).** For each centre p, the cone over C_p (dimension 2, degree O(E)) meets the core in O(EL²) = o(N) points.
6. **Case (2), §6.1.**
   - Lemma 6.2 gives product images ψ(X×Y) of dimension 2k, with deg U ≤ e_j² e^{o(s)} and the subfamily mass bound (6.3).
   - Lemma 6.3 gives the label-rank lower bound (6.5) for any dense ordered graph.
   - Covered labels satisfy the upper bound (6.6).
   - The ratio (6.7) is at least min(A/(δD_d), A/(δD₁D₂)). This has a strict s-margin except when s = log B and b_d = 1, so this case ends in a contradiction.
7. **Case (2) with s = log B, b_d = 1, §6.2.**
   - Lemma 6.4 gives a smooth 2k-dimensional label system of degree ≤ B^{2−c} containing almost all product images.
   - At each centre, components of C_p not contained in the specialised system carry o(n) targets.
   - Contained components lift to physical curves.
8. **k = 1.** The lift is the target's terminal curve, an incidence already removed by Prop 4.3.
9. **k ≥ 2.** There is at most one lift per γ, of degree ≤ 2 deg γ (Lemma 4.1 local form, the tangent-inequality test, Cor 3.14). So each row carries ≤ CEM + o(n) targets, and CEM/n ≤ C√δ·M/A → 0. Contradiction.
10. **Case (3), §6.3–6.5 (sparse_b scope).**
    - Prop 6.5 (projection depth at actual centres) and Lemma 6.7 (strict target-plateau margin) are compared with (6.27), H ≤ CE(T+1) per centre.
    - The remaining zero-margin case (v/s → 0, final one-dimensional target plateau) is handled in §6.5. There V_p = Env_{T₀}(C_p), Lemma 3.8 is applied, and the projected terminal curve is identified with a member of F_p, which Prop 4.3 has already removed.

The either-endpoint OR is resolved per selected product, not per pair. One orientation keeps at least half the covered pairs and the others are discarded. In case (2) this is harmless: Lemma 6.3 holds for any dense ordered graph, and the two factors have the same width and limiting profile, so their roles can be swapped. For the pool, both factors are the same set.

## 2. §6.1 audited line by line, with recomputations

**(6.6), recomputed.** At a fixed centre p, the covered labels lie in {p} × (C_p ∩ chart). In the affine chart, polynomials of degree ≤ T in (x, z) restrict on {p} × C_p to the homogeneous degree-T restriction on the projective closure of C_p. Lemma 3.6 (3.5) with k = 1 gives H_V(D) ≤ a·C(D+1, 1) = a(D+1). So the rank at p is ≤ E(T+1). Rank is subadditive over the union of centres, so H(T) ≤ n_x E (T+1) ≤ N E (T+1). (6.6) holds with C = 1.
- The span ≤ P² hypothesis plays no role in (6.6).
- The upper bound is per centre. It is therefore indexed by the covering endpoint, which is exactly why an orientation must be selected.

**(6.5) consistency.** I checked numerically (`/tmp/sparse_a_scripts/check65.py`, 1.7M random admissible profiles with d ≤ 7) that σ(b)² min(1, T/(D₁D₂)) never exceeds the trivial ceilings T^{2d−1} (dimension of degree-T polynomials on the (2d−1)-dimensional label space) or N² (number of labels). I also checked that it is ≤ D₁T^{2d−2} on the hypersurface plateau, as p. 46 claims. The factor min(1, T/(D₁D₂)) is exactly what reconciles σ² (scale 2d) with label dimension 2d−1.

**(6.7), recomputed.** Near the last cut σ(b) → e_j D_d^k = ΠD_i = N, using Σb_i = 0. Then:

ratio = N² min(1, D_d/(D₁D₂)) / (N·δN/A·D_d) = min(A/(δD_d), A/(δD₁D₂)), which matches (6.7).

Margins:
- A/(D₁D₂) = e^{−(b₁+b₂)s}.
- A/D_d = B e^{−b_d s}. For s ≤ ½ log B this is ≥ e^{s}. For s = log B it is B^{1−b_d}.
- δ enters only through 1/δ ≥ 1, the favourable direction.

Numeric check (`/tmp/sparse_a_scripts/check67.py`, 200k random profiles, 0 failures): the log-ratio equals the prediction, and the margin is > 0 except when s = log B and b_d = 1. The sentence "No comparison between δ and an uncontrolled exp(o(s)) factor has been made" is **TRUE**.

**Lemma 6.2, checked step by step.**
- Lemma 4.2 lists and deletion of tangent pairs give dim Z = 2k.
- deg Z ≤ 4^k deg X deg Y: the pulled-back linear forms have cleared numerators of degree 2, and refined Bézout counts the isolated points. Then (6.2) follows from (6.4).
- (6.4) follows from (5.8) and ΠD_i = N, with exp(o(s)) pooled pieces.
- Generic fibre of Ẑ over X: the four Stacks tags were checked; see the citation table.
- The point-projection formula (Lemma 3.12(i)) gives deg Y − mult_x Y = t_x(Y)d_Z, and deg Y ≤ 2t_x d_Z. For X = Y nonflat this uses deg Y ≥ 2; coincident flats were deleted as tangential.
- The mixed section gives deg X·d_Z ≤ deg Z.
- Summing with Σ t_x ≤ exp(εs) and multiplying by (6.4) gives (6.3). The bound Σ deg X deg Y ≤ C_d e^{εs} deg(∪J) carries no o(s), so (6.3) is uniform in the subfamily J, including J chosen later. This is used in Lemma 6.3 (group carrying Γ′) and in Lemma 6.4 (the exceptional subfamily E).

**Lemma 6.3, checked step by step.**
- Initial interval: by product testing the envelope is all of label space, so the rank is ≍ T^{2d−1} ≥ T^{2d}·T/(D₁D₂).
- Case h ≥ 2k+1: combine H(T) ≳ aT^h with H_{ψ(Γ′)}(T′) ≲ a(T′+1)^h. The required right side grows with exponent ≤ 2k+1, and σ and the min factor are continuous at cut times.
- Case h = 2k, k = d−1: the image is X × P^{d−1} and a ≳ e₁e^{−o(s)}. The inequality D₁²T^{2d−2}min(1, T/(D₁D₂)) ≤ D₁T^{2d−2} holds for T ≤ D₂ (checked).
- Case h = 2k, k < d−1: a ≥ deg(∪J) ≳ e_j² e^{−εs−o(s)} by (6.3), because the represented product mass is ≥ |Γ′|.
- Rank-one boundary convention: checked at b₁ = −1.
- The lemma is never applied to the covered graph through any coverage property. It is used for the covered graph (in §6.1) and for the uncovered auxiliary graph Λ_h (in §6.2). This matches the statement "its pairs need not be covered".

**Bookkeeping for the positive fraction of pairs.**
- Γ_cov ⊂ S_x × S_y has density ≥ ½·(1 − o(1)) relative to the chosen orientation.
- Lemma 6.3 needs density only. Its exp(−o(s)) is uniform for fixed density, by the sequence formulation.
- The light-line and terminal deletions are not used in §6.1.

## 3. §6.2 audited line by line: the outermost endpoint

**Balance (6.9).** With b_{j+1} = … = b_d = 1, Π_{i>j}D_i = B^{2k}, so e_j = B^{d−2k} and N/e_j = A^k. Also j ≥ 2: if j ≤ 1 then b₂ = 1 and b₁ + b₂ < 0 would force b₁ < −1. Hence 1 ≤ k ≤ d−2 (and 2k ≤ d, because every D_i ≥ 1). **Checked.**

**Times (6.10).** t₀ > max{β, 1+b₁+b₂} exists because 1+b₁+b₂ < 1. All of ε, ξ, τ, t_i are fixed after the limiting profile is fixed. **Checked.**

**Low-span deletion (k ≥ 2).**
- There are ≤ e_j e^{o(s)} carriers.
- Each lies in a complex flat of dimension k+1 ≤ d−1. Its real points lie in a real flat of the same or lower dimension, which Lemma 2.1 caps at C M^{(k+1)/2} ≤ C B^{k+1} points.
- Total ≤ B^{d−k+1+o(1)}, and B^{d−k+1+o(1)}/n₀ = B^{1−k+o(1)} → 0. **Checked.**

**Lemma 6.4.**
- **Step 1 (images in components of dimension ≥ 2k+1 carry o(n²)).**
  - Λ_h is dense in S × S.
  - (3.7) gives H_V(T₀) ≳ a_h T₀^h, and (3.5) gives H_{ψ(Λ_h)}(T′) ≲ a_h(T′+1)^h.
  - Lemma 6.3 just before β gives e_j²T′^{2k}min(1, T′/(D₁D₂)).
  - Propagating with h ≥ 2k+1 gives e_j²T₀^{2k}min(T₀/T_s(β), T₀/(D₁D₂)). This has the strict normalized margins t₀−β and t₀−(1+b₁+b₂).
  - On the other side, H_V(T₀) = H_U(T₀) ≤ C deg U·T₀^{2k} = C e_j² T₀^{2k} e^{o(s)}. **Contradiction verified.**
- **Step 2.** Lemma 3.8 at D = T₁ with L = T₀ gives exceptional degree ≤ C deg(I)·T₀/T₁ = e_j² e^{−(t₁−t₀)s+o(s)}. By (6.3) its mass is ≤ e^{−(t₁−t₀−ε)s+o(s)} = o(1), since ε < (t₁−t₀)/4. **Checked.**
- **Tests.**
  - g∘ψ has degree O(T₁); the tangent tests ∇f_a(r)·v have degree O(T_s(τ)).
  - The annihilator-row identity holds: if a₁·v ≠ 0, then Σc_i a_i with (Σc_i a_i)·v = 0 equals Σ(c_i/(a₁·v))[(a₁·v)a_i − (a_i·v)a₁].
  - Generic nonvanishing of the tangent-inequality test follows from the last assertion of Lemma 4.1, together with the span ≥ k+2 deletion.
  - All degrees are ≤ B^{1+t₂+o(1)} ≤ B^{2−c}. **Checked.**

**Endpoint count.**
- **(a) Components γ not contained in the specialised equations.**
  - Each has ≤ deg γ·B^{2−c} directions (Bézout in the chart).
  - Each direction carries ≤ B^{o(1)} targets (light-line restriction).
  - Per row this gives E B^{2−c+o(1)}/n ≤ √δ B^{−c+o(1)} → 0, uniformly in p. **Checked.**
- **(b) Lifting a contained γ.**
  - W is smooth of dimension 2k at the label, and ψ|X×Y → W has full rank, so the inverse function theorem applies.
  - Since {p}×γ ⊂ zero locus = W near the label, the germ of Y ∩ π_p^{−1}(γ) at q is biholomorphic to the germ of γ.
  - The algebraic component through the branch is a curve C with π_p(C) closure = γ.
  - Consistency check: a {p}×P^{d−1} germ inside W is impossible, because W ∩ {x = p} ≅ (Y, q) has dimension k < d−1. **Checked.**
- **(c) k = 1.** C = Y is the global terminal curve (uniqueness of the carrier at a retained point; nonreal lines were removed). Then π_pY = γ ⊆ C_p, which is exactly a Prop 4.3 incidence. The deletion is on ordered pairs, so it is orientation-free. **Checked.**
- **(d) k ≥ 2, (6.12).**
  - At a general z ∈ γ, the roots are general points of the lifts. The tests (g∘ψ, g_ph, both injectivities, tangent inequality) are polynomials in q that are nonzero at the marked point, hence generically nonzero on the lift.
  - Two distinct roots q′, z′ on the line through p, with carriers Y and Y′, satisfy the hypotheses of the local assertion of Lemma 4.1.
  - I re-derived that tangent calculation. Varying the source along ξ ∈ T_pX with the root fixed gives (ξ, −ξ̄/a) and (ξ, −ξ̄/b) in TW. Their difference is vertical, so ξ̄ ∈ T_{q′}Y mod v.
  - Both projected spaces have dimension k, so they are equal, contradicting the tangent-inequality test. Hence at most one lift, of map degree 1. **Checked.**
- **(e) Degree loss.** If p ∈ C ⊂ Y then Y = X. Cor 3.14 gives mult_p C ≤ deg C/2; I checked its proof: ℓ ∈ m²_{X,p}, so length(R/ℓ) ≥ 2 mult_p C ≤ deg C. Then (3.15) gives deg γ·deg(C→γ) ≥ ½ deg C, so the lift has degree ≤ 2 deg γ. Lemma 3.1 (3.2) with u = 1 gives |P ∩ C| ≤ C·deg C·M, so the row has ≤ 2CEM targets. **Checked.**

**The inequality that must survive an arbitrarily slow δ → 0.**
- The per-row count CEM + C E B^{2−c+o(1)} = o(n) reduces, through n ≥ (1−o(1))N√δ from (6.11), to √δ·M/A → 0 and √δ·B^{−c+o(1)} → 0.
- Each holds with **no rate**: either factor tends to 0 while the other is ≤ 1.
- Every other margin in §6.2 is a fixed positive number set by the profile, independent of δ: t₀−β, t₀−1−b₁−b₂, t₁−t₀−ε, 1−t₂, and k−1.
- The √δ device is essential. With only n = N e^{−o(s)} the ratio would be δ(M/A)B^{o(1)}, which need not tend to 0. This is the "zero margin" the paper names.
- Its own justification is the diagonal choice on p. 42; see Objection 3.

---

## 4. Objections

**1. Theorem 6.1 is stated without its real hypotheses.** (p. 42) — **COSMETIC** (exposition).
- Verbatim: "Along a sequence with M = o(A), there cannot be families C_p …"
- As stated alone, M = o(A) does not supply what the proof consumes: the least-failing-dimension bounds (Lemma 2.1). These enter the flat cap in Lemma 4.2, h_max = o(N) for the light-line restriction, the B^{k+1+o(1)} flat cap in §6.2, and Prop 4.3.
- The preamble sentence "We retain the contradiction hypotheses, including the lower-dimensional induction bounds" carries them. The application on p. 8 is "In the regime (2.1)", so the use is correct.
- Fix: state Theorem 6.1 "in the regime (2.1) in the least failing dimension d".

**2. Prop 5.5 says the outermost pool "may" be used, but §6.2 needs it.** (p. 41 Prop 5.5 / p. 47 §6.2) — **UNCLEAR** (exposition).
- Prop 5.5, verbatim: "In the common outermost window s = log B, the two factors may instead be the same pool of pieces in a shrinking profile bin. That pool has size n ≥ N√δ …"
- §6.2, verbatim: "Assume now s = log B and b_d = 1. Use the common pool supplied by Proposition 5.5".
- If alternative 2 returned two distinct width-log B pieces with b_d = 1, §6.2 would lack n₀ ≥ N√δ, and the final inequality EM/n → 0 is exactly where that bound is used.
- The case is in fact excluded by the "refinement" on p. 42: "If its total mass tends to zero, discard it before the selection. If its mass is bounded below on a subsequence, work only there." So every s = log B selection is the pool.
- Fix: "may instead" should read "are"; §6.2 should cite the p. 42 refinement. Mathematically fine as read.

**3. The pool-mass condition has a one-sentence justification.** (p. 42, last two paragraphs of the proof of Prop 5.5) — **UNCLEAR** (exposition gap; the statement is true).
- Verbatim: "In the diagonal choice increase precision slowly enough that its mass is at least N√δ and N exp(−o(log B)). This is possible because δ → 0." and later "This is compatible with the outer-pool mass condition."
- §6.2 uses only the lower bound n₀ ≥ N√δ. But the pool must also absorb every global o(N²) loss as o(n₀²): the uncovered pairs, the Prop 4.3 terminal deletion, and the light-line discard O(N²/H).
- A reader who takes n₀ ≈ N√δ literally would need these losses to be o(δN²), which is a rate.
- The argument actually works because the pool is a largest bin at precision h, of mass ≥ c₀N/K(h). Here K(h) is the number of bins, a fixed function of h independent of N. Choose h(N) → ∞ so slowly that c₀/K(h) ≥ √δ, that K(h)²·(each o(1) loss) → 0, and that H(h) ≤ B^{o(1)}. All of these are "slowly enough" conditions and are jointly satisfiable, so no rate is needed.
- Fix: write n₀ ≥ max{N√δ, c(h)N}, with the global losses o(c(h)²N²) at fixed h, then diagonalise. Not FATAL; I verified the diagonal argument.

**4. One-line justifications at three steps.** (pp. 46, 50) — **COSMETIC.**
- (6.6) "obtained by specializing at each actual center": the missing step is Lemma 3.6 (3.5) with k = 1, which gives C = 1.
- The local assertion of Lemma 4.1 at a general root in (6.12): it needs the tests to be generic on the lift, which follows because they are polynomials in q, nonzero at the marked q.
- "Corollary 3.14 therefore gives mult_p C ≤ deg C/2": the marked q is the point z required by Cor 3.14.
- All three were verified above. Recording them because the step to a general root is easy to miss.

**5. Observation, not a defect: span ≤ P² is used only at k = 1.** (§6.1–6.2) — **COSMETIC.**
- Neither (6.6)/(6.7) nor the k ≥ 2 outer-endpoint argument uses the hypothesis that each component spans at most P². In this scope it enters only through Prop 4.3 at k = 1.
- So the k = 1 terminal-curve case of §6.2 rests entirely on Prop 4.3 (secants scope), which is not certified here.

**6. Bibliography date.** ([25], p. 103; outside scope, noticed in passing) — **COSMETIC.**
- Verbatim: "consulted September 23 and October 1, 2026", in a paper dated "September 23, 2026".
- The text was edited after its printed date. This does not affect the mathematics.

---

## 5. Citation table (external results used in pp. 42–51)

The only external citation in §6.1–6.2 is [25] on p. 44. I fetched the tags to `/tmp/oaimath/166/refs/stacks_sparse_a/`.

| Cited | Paper claims | Source says (quote) | Verdict |
|---|---|---|---|
| Stacks Tag 052A | "generic flatness" for Ẑ → X after shrinking X | "Proposition 29.28.1 (Generic flatness). Let f: X → S be a morphism of schemes … Assume S is integral, f is of finite type, and F is a finite type O_X-module. Then there exists an open dense subscheme U ⊂ S such that X_U → U is flat and of finite presentation …" | MATCH |
| Stacks Tag 0559 | "geometric integrality after shrinking" (irreducible half) | "Lemma 37.27.5. … Assume Y is irreducible with generic point η, X_η is geometrically irreducible, and f is of finite type. Then there exists a nonempty open subscheme V ⊂ Y such that X_V → V has geometrically irreducible fibres." | MATCH (the generic fibre is geometrically integral, as argued on p. 44) |
| Stacks Tag 0C0E | the reduced half of geometric integrality | "Lemma 37.26.7. Let f: X → Y be a flat proper morphism of finite presentation. Then the set {y ∈ Y : X_y is geometrically reduced} is open in Y." | MATCH (applied after generic flatness; Ẑ is projective over X) |
| Stacks Tag 0B9T | "constancy of the Hilbert polynomial in a flat projective family" | "Lemma 36.32.2. Let f: X → S be a proper morphism of finite presentation. Let F be an O_X-module of finite presentation, flat over S. The function s ↦ χ(X_s, F_s) is locally constant on S." | MATCH (apply to O(m) for every m) |

Internal results consumed in this scope (statement vs use):

| Result | Used where | Statement vs use | Status |
|---|---|---|---|
| Lemma 3.1 (3.2): \|P∩V\| ≤ C_n a M^u for complex pure u-dim V | §6.2 row count, u = 1 | MATCH; the proof read in full is valid for complex V | verified |
| Lemma 3.6 (3.5)/(3.7) | (6.6); Lemma 6.3; Lemma 6.4 | MATCH (envelope groups at their defining degree; the (3.8) monomial-division step was checked). The interpolation degree q ≤ C_nL comes from Lemma 3.3 and was not checked | conditional |
| Lemma 3.8: exceptional degree ≤ C_n aL/D | Lemma 6.4 at D = T₁, L = T₀ | MATCH at statement level; proof not checked | conditional |
| Lemma 3.12(i), point-projection formula | Lemma 6.2; §6.2 | MATCH; proof skimmed | verified (standard) |
| Cor 3.14 | §6.2 | MATCH; proof checked | verified |
| Lemma 4.1 (generic and local) | Lemma 6.4; (6.12) | MATCH; tangent calculation re-derived | verified |
| Lemma 4.2 (lists, Σ t_x ≤ e^{εw}) | Lemma 6.2 | MATCH (hypotheses supplied by (6.4) with w = s, e = e_j); the Theorem B.2 step was not checked | conditional |
| Prop 4.3 (terminal deletion o(N²)) | §6.2, k = 1 | MATCH ("π_pY_i ⊆ C_p", real lines) | not checked (secants scope) |
| Props 5.1–5.3, 5.5; Lemma 5.4 | throughout | read; statements match the uses | not certified (secants scope) |

## 6. Constant-dependency table (this scope)

| Constant | Fixed where | Depends on | Used where | Claimed independent of |
|---|---|---|---|---|
| δ, E = δN/A | hypothesis of Thm 6.1 | the sequence; any rate | (6.6), (6.7), §6.2 counts | no rate used: (6.7) uses only 1/δ ≥ 1; §6.2 uses √δ·M/A and √δB^{−c} → 0. **Holds** |
| s* | Prop 5.1 | δ (δe^{6s*} → 0) | window widths | only "s* → ∞"; any slow growth is fine |
| s (width) | Prop 5.5 selection | the sequence; s = log B in §6.2 | every o(s) | — |
| b₁…b_d, β, j, k | limits along a subsequence | the subsequence only | (6.7), (6.9), (6.10) | N, δ (after passing to the limit) |
| D_i, e_j, σ | (5.6) | b, s, B | (6.5)–(6.7), (6.9) | — |
| ε (Lemma 6.2) | §6.1: arbitrary fixed; §6.2: < (t₁−t₀)/4 | profile | (6.3) | N; it is fixed before U, so E cannot influence it ("no new generic-depth deletion depends on E") |
| τ_eq < τ_test < τ < t₀ < t₁ < t₂ < 1 | (6.10) | β, b₁+b₂ | degrees of equations and tests | N, δ |
| ξ, endpoint tolerances | after (6.10) | the gaps t₀−β, t₀−1−b₁−b₂ | Lemma 6.4 | N, δ |
| c in B^{2−c} | end of Lemma 6.4 | t₂ and the O(·) constants | §6.2 Bézout count | N, δ |
| α (density of Γ₀) | Prop 5.5 (≈ ½) | — | \|Γ\| ≳ n² | N |
| C_d = 4^k (deg Z ≤ C_d deg X deg Y); C, C_n (Lemmas 3.1, 3.6, 3.8) | Lemmas 3.x, 6.2 | d only | (6.2), (6.6), the row count | the sequence |
| H (light-line threshold) | Prop 5.5 | precision h; H ≤ B^{o(1)} | §6.2 per-direction count | δ (chosen per precision, not per δ) |
| pool precision h(N), mass n₀ | Prop 5.5, p. 42 | δ and the o(1) losses (slow diagonal) | (6.8), (6.11) | rates: none needed (Objection 3) |
| number of pooled pieces | Prop 5.5 | exp(o(s)) = B^{o(1)} | Prop 5.3 pooled version, (6.4) | — |

No constant in this scope depends on N, on δ, or on the chosen window where independence is claimed. I found no circularity: Lemma 6.3 → Lemma 6.2 (earlier plateaus) → Lemma 4.2, Prop 5.3, Lemma 5.4, which do not call back into §6.

## 7. Verified line by line vs skimmed

**Verified line by line:**
- Theorem 6.1 vs p. 8, and its negation in Prop 2.2 (p. 9).
- §6 preamble; (6.1) charts (chart change costs a constant factor in degree, absorbed by "constant factors in testing degree fit inside a chosen open plateau").
- Lemma 6.2 statement and proof (pp. 43–45), including the four Stacks tags.
- Lemma 6.3 statement and proof (pp. 45–46).
- (6.6) recomputed; (6.7) recomputed with a numeric check.
- §6.2 p. 47: (6.8)–(6.11) and the low-span deletion.
- p. 48: the k = 1 identification with the terminal assignment.
- Lemma 6.4 statement and proof (pp. 48–50).
- Endpoint count pp. 50–51: Bézout and light lines; lifting through the analytic inverse; k = 1; (6.12) via Lemma 4.1 local; Cor 3.14; Lemma 3.1; the final √δ·M/A inequality.
- Supporting proofs read in full: Lemma 3.1, Cor 3.14, Lemma 4.1, and the (3.8) step of Lemma 3.6.

**Skimmed / taken on trust (outside scope):**
- Lemma 3.3/3.5 interpolation degree (q ≤ C_nL); Lemma 3.8 proof.
- Lemma 4.2's Szemerédi–Trotter list step and Theorem B.2.
- Prop 4.3 (all three cases).
- Prop 5.1 (partition, thresholds (5.3)–(5.5)), Prop 5.2, Prop 5.3, Lemma 5.4 (read, not certified).
- Prop 5.5's binning and orientation selection (read; I verified only the pool-mass diagonal).
- §6.3–6.5: structure only.

## 8. Verdict for scope

**HOLDS AS READ.**
- The either-endpoint alternative is handled soundly. In case (2) one orientation is chosen per selected product, and Lemma 6.3 needs only density with symmetric roles. In the pool case both factors coincide. Prop 4.3 acts on ordered incidences, so it is orientation-free.
- The common-window comparison (6.7) has a strict s-margin, and δ enters only favourably.
- The outermost endpoint is defeated without a rate, through the pool bound n ≥ N√δ: CEM/n ≤ C√δ·M/A → 0.

**COULD NOT CHECK, and therefore conditional:**
- Lemma 3.6's lower bound via Lemma 3.3 (algebra scope).
- Lemma 3.8 (algebra scope).
- Lemma 4.2's list bound (secants scope, through Theorem B.2).
- Prop 4.3 (secants scope; it carries the entire k = 1 case of §6.2).
- Props 5.1–5.5 and Lemma 5.4 (secants scope).
