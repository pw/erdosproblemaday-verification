# Referee report — seat `secants`: §4 (pp. 27–33) and §5 (pp. 33–42)

Paper: /tmp/oaimath/166/paper.pdf (sha256 37f63553…). Reviewer seat: Claude (Opus 5.5), 2026-10-12.
Pages read in the rendered PDF (27–42) and in the text extractions. Architecture (pp. 1–13) and all §3 statements (pp. 14–26) were read first. I also read referee_sparse_a.md §8, referee_sparse_b.md ("Verdict for my scope") and the algebra seat's Objection 5.

## Verdict for my scope

**HOLDS AS READ.** I found no FATAL objection and no mathematical GAP in Lemma 4.1, Lemma 4.2, Prop 4.3, Props 5.1–5.3, Lemma 5.4 or Prop 5.5.

- No step uses a rate for δ → 0 or for M/A → 0.
- Every constant that must be fixed is fixed before the limit is taken.
- Everything that depends on the sequence (s\*, the limiting profile, the precision diagonal) is chosen legitimately. Theorem 6.1 is a non-existence statement along one sequence, so its proof may depend on that sequence.
- No step pays a factor equal to the number of windows. That number tends to infinity.

All 14 objections below are exposition: UNCLEAR (true, but a step is not written) or COSMETIC.

What the §6 seats lean on, item by item:

| §6 dependency | Status |
|---|---|
| Lemma 4.2 generic list bound (through Thm B.2) | **Verified line by line**, including the hypothesis paragraph for both carrier configurations. Thm B.2 itself is the incidence seat's. |
| Prop 4.3: o(N²), uniform in assignment and curves | **Verified line by line** in all three cases (lines; nonlinear d ≥ 4; nonlinear d = 3). |
| Prop 4.3 deletes exactly what §6.5 / §6.2 (k = 1) produce | **Yes.** It deletes ordered (p,q) with q assigned to its terminal curve Y (carrier after the (d−1)st cut) and $\overline{\pi_pY}\subseteq C_p$. |
| Prop 5.1(3), Prop 5.3: no-capture / individual cuts uniform over all cuts of degree O(T_s(b)) and over sequences of pieces | **Verified.** The bounds are explicit functions of s and of fixed margins: e^{−7s^{1/10}/18}, and N·e^{−(margin)s+o(s)}. |
| Lemma 5.4 | **Verified.** |
| Prop 5.5: exhausts the cases; covered ordered product of fixed density in one orientation | **Verified.** α ≥ 1/2 − o(1), independent of N and δ. |
| Algebra seat Obj. 5: Lemmas 3.8/3.9 need D ≥ C_n L | **Holds at every §5 use.** The only uses are in Prop 5.3, where D/L = e^{(b′−β)s−o(s)} and D/L′ = e^{(b′−b)s}/O(1). The margins are fixed and s ≥ s\* → ∞. Prop 5.2 uses only Lemma 3.6 at the defining degree, which has no such hypothesis. See Obj. 1. |

---

## Answers to the brief's specific questions

### §4.1 (Lemma 4.1)

**What is computed.** The differential of ψ(x,y) = (x, π_x(y)) on X × Y. Its image has dimension k + l at a general pair:
- the first coordinate gives T_xX (k directions);
- injectivity of T_yY modulo C(y − x) gives l vertical directions.

So the vertical kernel of the image tangent space is $\overline{T_yY}$.

A further root z ∈ Y′ on the same line gives a second family of image tangent vectors, (ξ, −ξ̄/b). Subtracting (ξ, −ξ̄/a) leaves the vertical vector (b^{−1} − a^{−1})ξ̄, with a ≠ b because z ≠ y. Hence $\overline{T_xX}\subseteq\overline{T_yY}$ and k ≤ l.

**k = l case.** Project X from the affine tangent flat y + T_yY. The inclusion T_xX ⊆ T_yY + C(x−y) means this projection has zero differential, so in characteristic 0 its image is a point. Hence X ⊂ some (k+1)-flat ⊇ y + T_yY. Interchanging X and Y and comparing spans gives a common (k+1)-flat.

**Where genericity enters:**
- general pair (Zariski-open in X × Y), so the image point is smooth and the differential has full rank;
- general y for the projection.

**Local assertion (4.1.1).** It needs only p smooth on X, so that every ξ ∈ T_pX is realized by an arc, plus full rank at (p,q) and W smooth of dimension k + l. Then T(image) = TW, and the same subtraction applies.

Verified line by line. I also checked by hand that the vertical kernel has dimension exactly (k + l) − k = l.

### §4.2 (Lemma 4.2): "parameter count, Bézout, generic over what"

Lemma 4.2 has **no parameter count and no Bézout**. Its count is an incidence count:
1. discard pairs tangent at either endpoint (proper-flat cap);
2. discard common-(k+1)-flat pairs with a nonlinear member (proper-flat cap);
3. apply Lemma 4.1;
4. slice the surviving flats by a generic real codimension-k subspace, then a generic plane, and apply Theorem B.2's rich-line count.

"Generic" ranges over three things:
- (i) general pairs (x,y) ∈ X × Y, a finite intersection of Zariski-open sets;
- (ii) one general smooth y ∈ Y per target (resp. x ∈ X per source) for the tangent flats;
- (iii) a generic real slicing subspace and planar projection, avoiding finitely many conditions for the finite families.

Every step checks:
- t_H ≤ e·e^{ηw+o(w)}·B^{−c₀} ≤ e·B^{−c₀/2} (η < c₀/4, w ≤ log B).
- Per dyadic t, the pair weight is ≤ t²e^{−2}e^{o(w)}.
- Σ_{t≥e^{εw}} [e²/t³ + e/t]·t²e^{−2}·e^{o(w)} = e^{−εw+o(w)} + O(B^{−c₀/2}e^{o(w)}) = o(1).

The case k > l is handled by Lemma 4.1 alone: there is no further root at all, so the count is 1 (Obj. 8).

Hypothesis check:
- **Common window:** w = s, e = e_j. Flat count ≤ e_j·e^{o(s)} and weight ≤ (N/e_j)e^{o(s)}/(N e^{−o(s)}) by (5.8) and Π D_i = N.
- **Separated subpower windows:** w = log B, e = B^{d−l}, since every e^{O(s)} = B^{o(1)} when s = o(log B).

Both hold. The flat cap consumed is any c₀ > 0, not the planar B^{2+o(1)}.

### §4.3 (Prop 4.3)

**Cost, case by case:**

| Case | Cost |
|---|---|
| Lines: centres on the line | 2M·Σn_i ≤ 2MN = o(N²) |
| Lines: planes with S_H < A | ≤ N·E·A = **δN²** (the only use of δ → 0 in §4) |
| Lines: planes with S_H ≥ A, N/s term | ≤ N·h_max·log²N = o(N²) |
| Lines: planes with S_H ≥ A, T³/s³ term | ≤ C·M²N²/A² = o(N²) |
| Nonlinear, d ≥ 4: centres in a 3-span or own plane | ≤ N²B^{−c₀} |
| Nonlinear, d ≥ 4: light groups | KNME = Kδ·N²·M/A |
| Nonlinear, d ≥ 4: surviving mass | < εN², because E = o(N) |
| Nonlinear, d = 3: high-multiplicity centres | ≤ 7N |
| Nonlinear, d = 3: line projections | N²B^{−c₀} |
| Nonlinear, d = 3: light groups | KNME |
| Nonlinear, d = 3: surviving mass | < εN², because N⁴/E² = N^{10/3}/δ² ≫ N³ |

None of these needs a rate.

**What is removed.** Ordered incidences (p,q), p ∈ P any sample point (core or not), q a non-core point assigned to its carrier curve Y_q after the (d−1)st cut, with $\overline{\pi_pY_q}\subseteq C_p$. They are removed from the coverage relation, not as points. An unordered pair stays covered if its other orientation survives, so unoriented coverage drops by at most the o(N²) removed.

**Why global and once.** Prop 4.3 bounds the incidences only globally, by o(N²). The selected products have mass only N²e^{−o(s)}, and the outer pool may have mass as small as δN². So a per-product application would not be negligible. The paper therefore deletes once, on the fixed global terminal assignment, before any selection (Prop 5.5, p. 41). The selection then runs on post-deletion coverage. This order is necessary, and it is the order used. Pooling later does not change assignments ("Assignments retain their original meaning if pieces are later pooled").

**Before or after Prop 2.2's greedy removal; does order matter?**
- Prop 4.3 runs **after**. It lives inside the proof of Theorem 6.1 (via Prop 5.5), and Theorem 6.1 is invoked only in the contradiction branch of Prop 2.2, on the curves recorded by the greedy removal (total degree ≤ N/(KA), K → ∞, so δ = 1/K).
- Prop 4.3 and all of §4–5 use only Theorem 6.1's hypotheses: irreducible curves, each spanning ≤ P², total degree ≤ δN/A, δ → 0. They never use the greedy "> KA·deg partners" property. The order therefore carries no hidden dependence.
- Prop 2.3's symmetric selection is in the other branch of Prop 2.2 and never meets Prop 4.3.

### §5.1 (Prop 5.1): windows, widths, core, chain of cuts, profile

- **Widths:** s = 2^{−a} log B for a = 0, 1, …, stopping at the first width in [s\*, 2s\*]. That is ⌊log₂(log B/s\*)⌋ + O(1) widths, a number that tends to infinity.
- **Windows:** at width s, degrees [Be^{−s}, Be^{(1+o(1))s}], i.e. normalized times [−1, 1+o(1)].
- **Dependence on the sequence:** the widths are not independent of it. s\* depends on δ and B ("s∗ ≤ ¼ log B, δ exp(6s∗) → 0"; e.g. s\* = min(¼ log B, (1/12)·log(1/δ)) works with no rate).
- **The number of widths is never paid as a factor:**
  - discards are summed in (5.5) by a geometric series;
  - the selection bins dyadic indices modulo m(h), so the number of bins depends only on the precision h.
- **Core:** the unresolved set at the final width. It is exactly the zero set of product equations of degree ≤ B·e^{s_f+√(2s_f)+C} ≤ B·e^{3s\*}, so EL² ≤ δe^{6s\*}N = o(N).
- **Chain:** each retained batch gets one tree path of exactly d proper cuts.
- **Profile:** limits of the recorded cut times (grid times, mesh → 0).

### §5.2 (Prop 5.2)

**Bézout products, recomputed:**
- carrier degree ≤ Π_{i≤j}D_i·e^{o(s)} = e_j·e^{o(s)};
- (5.8): a·Π_{i>j}D_i·e^{o(s)}. The later cuts are proper at every piece point, and refined Bézout counts the piece points on W as 0-dimensional components of W ∩ Z(f_{j+1},…,f_d);
- n ≤ Π_iD_i·e^{o(s)}, which gives Σb_i ≥ 0;
- σ(b) = Π min(T,D_i) = e_j·T^{d−j}.

**Rank growth between cuts.** This is **Lemma 3.6** (the upper bound (3.5) at T′, the lower bound (3.7) at T), applied to one dimension-h group of components of V = Env_T(S):

> H_S(T) = H_V(T) ≥ H_{G_h}(T) ≥ c_d·a·T^h,
> H_{S′}(T′) ≤ H_{G_h}(T′) ≤ a·C(T′+h, h).

The hypothesis of (3.7), "irreducible components of a locus defined by equations of degree ≤ L, L ≥ 1", holds at **every** testing degree T = T_s(b) ≥ 1, because V is cut out in degree T. Below 1, the paper's "rank one" boundary convention applies. No D ≥ C·L hypothesis is involved.

**Propagation:** H_S(T) ≥ (c_d/C_d)·H_{S′}(T′)·(T/(T′+1))^h with h ≥ l. The density drops α → α/(2(d+1)) per plateau, at most d times. All constants depend only on d.

### §5.3 (Prop 5.3, Lemma 5.4)

The D ≥ C_n L margins are discussed in Obj. 1. Exceptional degrees:
- Lemma 3.9: e_j·e^{−(b′−b)s+o(s)};
- Lemma 3.8: e_j·e^{−(b′−β)s+o(s)}.

By (5.8) and Π D_i = N, each costs N·e^{−(margin)s+o(s)} = o(n), uniformly.

For pooled pieces the accounting is per piece:
- a point of piece ν on a foreign carrier W_μ is a rank failure (two components through it);
- so the pooled minor combination vanishes there;
- ν's own no-capture then removes it.

This is what "full rank at a surviving point also excludes intersections with a carrier from another piece" means. Checked.

### §5.4 (Prop 5.5)

**Pigeonhole.** It is over K(h)·m(h) bins (profile cells of diameter 1/h × dyadic index mod m(h)), not over the scales. By Cauchy–Schwarz, two random retained points share a bin with probability ≥ 1/(K(h)m(h)), a constant depending only on h. So at fixed h the conditional uncovered fraction is ≤ u(N)·K(h)m(h) → 0. Averaging over piece pairs weighted by |P_x||P_y| yields one pair; choosing an orientation gives density ≥ 1/2 − o(1); then h(N) → ∞ slowly.

**Density retained.** The covered density α inside the selected product is ≥ 1/2 − o(1), fixed and independent of N and δ.

**Masses.**
- Selected pieces have mass N·e^{−o(s)}, not a fixed fraction of N. §6 is built to exponential accuracy, so this suffices.
- The outermost pool has mass ≥ c(h)N at fixed h and, after the diagonal, ≥ N√δ and ≥ N·e^{−o(log B)}.

**"Common" vs "separated".**
- Equal dyadic indices give a common width (alternative 2; at s = log B, the pool).
- Otherwise the congruence mod m(h(N)) → ∞ forces |a_x − a_y| → ∞, so the width ratio → ∞. Normalized widths within 1/h(N) then force both to be o(log B) (alternative 3).

These are exactly the "common window, k = l, w = s" and "separated subpower windows, w = log B" configurations of Lemma 4.2 and §6.3–6.4. The core alternative is contradicted by O(EL²) = o(N) per centre (Obj. 14).

---

## Objections

**Obj. 1 — Prop 5.3, p. 39: the hypothesis D ≥ C_n·L of Lemmas 3.9/3.8 is used but not checked.** UNCLEAR (exposition; true).
- Quotes: "Lemma 3.9, used at degree Ts(b′), pools proper component cuts of degree O(Ts(b)) into one polynomial." and "Apply Lemma 3.8 at degree Ts(b′). Since the cut-system equations have degree at most B exp((β + o(1))s), …"
- Check:
  - Lemma 3.9 needs T_s(b′) ≥ C_n·max{Be^{(β+o(1))s}, C′Be^{bs}}, i.e. e^{(b′−β−o(1))s} ≥ C_n and e^{(b′−b)s} ≥ C_nC′.
  - Lemma 3.8 needs the first of these.
  - Both hold for all large indices, because β < b < b′ are fixed inside the limiting plateau and s ≥ s\* → ∞.
  - The pooled version has L\* ≤ e^{o(s)}·L, so the same check works.
- The threshold index depends on the margins, hence on the limiting profile, i.e. on the subsequence. That is legitimate.
- These are the **only** §5 invocations of Lemmas 3.8/3.9. This discharges the algebra seat's Objection 5 for §5. (The §6 uses at T₁/T₀ = e^{ηs} are sparse_b's.)
- Fix: one sentence, "for large indices, since b′ − β > 0 and s → ∞".

**Obj. 2 — Prop 5.1 proof, p. 36: the reduction of the plateau no-capture to (5.4) skips a step.** UNCLEAR (exposition; true).
- Quote: "This proves the required no-capture assertion on any limiting open plateau. To allow a fixed multiplicative factor in the testing degree, choose a slightly later grid time which is still inside that plateau."
- (5.4) controls polynomials only at a grid index (τ, l) where the terminal piece's path took a **residual** step at dimension l. The text does not say why such a step exists. It does, for large index:
  1. the actual cut times converge to b_j < b < b_{j+1};
  2. the mesh tends to 0, so there is a grid time τ ∈ (b, b_{j+1});
  3. at τ the path has exactly j cuts and makes no cut, so it took the residual step at (τ, l);
  4. T_s(τ) ≥ C·T_s(b) for large s.
- Fix: state steps 1–4.

**Obj. 3 — Prop 5.1 statement, p. 34: s\* depends on δ, and the statement does not say so.** COSMETIC.
- Quote (proof, p. 35): "Choose s∗ → ∞ sufficiently slowly that s∗ ≤ ¼ log B, δ exp(6s∗) → 0."
- This is the one place in §4–5 where a scale is tied to δ. The smallest window and the core degree B·e^{3s\*} therefore depend on how fast δ → 0.
- No rate is needed: s\* = min{¼ log B, (1/12) log(1/δ)} gives δe^{6s\*} ≤ √δ.
- Everything else in §5 needs only s\* → ∞. I checked every use:
  - (5.4): e^{−7s^{1/10}/18};
  - (5.5) and the e^{−s^{1/3}} remainders: summable for any s\* → ∞;
  - the inherited boundary: e^{−(√2−1)√s};
  - Prop 5.3 margins: e^{−(b′−b)s};
  - Prop 5.5 nonreal lines: D_d^{−1}e^{o(s)} ≤ B^{−1+o(1)}.
- The text's §5 preamble does introduce δ. Fix: mention it in the statement.

**Obj. 4 — Prop 5.1, p. 36: "Σᵢ aᵢ = s^{1/10+o(1)} = o(s^{1/3})" is asymptotic with an extremely late onset.** COSMETIC.
- With a_K = s^{1/10} and a_i = 10a_{i+1}, Σa_i ≈ (10/9)·10^{K−1}·s^{1/10}. This is s^{1/10+o(1)} only because K = O_d(G) = O(√log s), so 10^K = e^{O(√log s)} = s^{o(1)}.
- That is true, but the text gives no reason for G = O(1+√log s) beyond "mesh tending to zero". Numerically (checks.py): K = 16 at s = 10⁶ gives a₁ ≈ 4·10¹⁵ ≫ s^{1/3} = 100.
- Harmless for a limit argument. Fix: say that G must be o(log s) for exactly this reason.

**Obj. 5 — Prop 5.5, p. 42: the pool-mass sentence names the wrong lower bound as the operative one.** UNCLEAR (exposition; true). Refines sparse_a Obj. 3.
- Quote: "In the diagonal choice increase precision slowly enough that its mass is at least N√δ and N exp(−o(log B)). This is possible because δ → 0."
- The global deletion Prop 4.3 performs before selection contains the term "Planes with S_H < A account for at most NAE = δN² pairs" (p. 30). That is of the same order as n² when n = N√δ.
- So n ≥ N√δ alone would **not** make the deleted incidences negligible inside the pool.
- What does make them negligible is the preceding sentence, "It has a fixed positive mass at that precision, and its relative uncovered fraction tends to zero":
  - at fixed h the pool has mass ≥ c(h)N;
  - the uncovered fraction u(N) (which includes the deletions) satisfies u(N)/c(h)² → 0;
  - the slow diagonal keeps u(N)/c(h(N))² → 0.
- Then n²/N² ≫ u(N), and n ≥ N√δ follows whenever the δN² term is present.
- Fix: state that coverage inside the pool is guaranteed by the fixed-h mass, preserved by the diagonal. The N√δ bound is the extra quantitative input §6.2 needs (C√δ·M/A → 0, per sparse_a), not the coverage guarantee.

**Obj. 6 — Prop 5.5, p. 41 vs Prop 4.3, p. 30: the two descriptions of what is deleted differ slightly.** COSMETIC.
- Prop 5.5: "its projection from the center is not a curve contained in the center's directional family."
- Prop 4.3: "q is assigned to Y_i and $\overline{\pi_pY_i}\subseteq C_p$".
- Prop 4.3 also counts point projections (Y_i a line through p, cost ≤ 2MN), which Prop 5.5's wording omits.
- They agree on curve projections, which is the case §6.2 (k = 1) and §6.5 use ("πp Y = γ ⊂ Cp, exactly an incidence removed by Proposition 5.5", l. 3188). No consequence.

**Obj. 7 — Prop 5.5, p. 41: the omitted nonreal-line points are not said to be removed.** COSMETIC.
- Quote: "Omit assignments to nonreal lines. Such a line contains at most one real point, so the omitted fraction in a piece is at most e_{d−1}exp(o(s))/n = D_d^{−1}exp(o(s)) = o(1)".
- Arithmetic: e_{d−1} = N/D_d, D_d ≥ B. Correct.
- The removal itself is done downstream: §6.3 "omit from Py the points left unassigned by the global terminal assignment", and §6.2 (l. 3060–3064) via the nonreal-flat deletion of Prop 5.3. So nothing is lost. Cross-reference only.

**Obj. 8 — Lemma 4.2 proof, p. 29: "a third moving root" undersells what Lemma 4.1 must rule out.** COSMETIC.
- Quote: "Lemma 4.1 now rules out a third moving root except when k = l and the source and first target are flats in a common (k + 1)-flat H."
- The count in the conclusion includes the generic map degree of π_x|Y itself (a second point of Y on the line).
- Lemma 4.1 with Y′ = Y rules this out too (map degree 1), and for k > l it rules out every further root on every listed l-dimensional target. So the count is exactly 1 outside the flat-in-H case.
- Correct, but the phrase "third" suggests otherwise.

**Obj. 9 — Lemma 4.2 proof, p. 29: a one-line inference is compressed.** COSMETIC.
- Quote: "Every further listed target with the same projection must also lie in H: for a general x ∈ X, its affine join with x equals H."
- "its" = the first target Y. A target Z with π_xZ = π_xY satisfies Z ⊆ π_x^{−1}(π_xY) = join(x,Y) = H.
- A nonlinear Z ⊂ H paired with the flat X lies in a common (k+1)-flat with it, so that pair was already discarded, and Z ∉ 𝒴_X. Each surviving flat Z ⊂ H contributes exactly one root. Checked.

**Obj. 10 — Prop 4.3, p. 31 (twice) and p. 32: "the plane cap" is stronger than needed.** COSMETIC. Relevant to brief item (vi).
- Quotes:
  - "The contribution of N/s to ∑hsF is at most CNB^{2+o(1)}(1 + log N)² = o(N²), using the plane cap and d ≥ 3."
  - "For a planar curve, centers in its own plane also cost o(N²)."
  - "these pairs cost o(N²) by the plane cap."
- In each, the proper-flat cap N·B^{−c₀} suffices: N·NB^{−c₀}·log²N = o(N²).
- So §4 consumes only Lemma 2.1's c₀ > 0. For d = 3, that needs only a planar bound |Δ| ≥ n^β with β > 2/3. It does not need Ω(n/log n), and B^{2+o(1)} is never needed in §4. This agrees with the Lean seat: TrackD's only flat hypothesis is `RealFlatCap P c₀`.

**Obj. 11 — Prop 4.3 d = 3, p. 32: (4.3) is Lemma 3.15, applied to a birational plane model, without the cross-reference.** COSMETIC.
- Quote: "A nonlinear irreducible degree-two curve has no point of multiplicity greater than one; for all other degrees this bounds the number with multiplicity greater than half the degree by an absolute constant."
- The constant is ≤ 7: from Σm² ≤ 2D(D−1) with m ≥ ⌊D/2⌋+1, checked for D < 500.
- The transfer from Y_i to its plane model uses Lemma 3.12(ii): (3.16), singleton fibres, degree preserved.

**Obj. 12 — Prop 4.3 d ≥ 4, p. 31: the "at most Ce_γ possible centers" bound is sharp up to C.** COSMETIC. Recorded so nobody tries to "fix" it.
- The coset argument gives #centres ≤ |Stab| ≤ e_γ = d_i, which is independent of p for the fixed ordered pair. The Bézout orbit bound is tight: the Fermat curve xⁿ + yⁿ = 1 has the n homotheties x ↦ ζx.
- So the bound cannot be O(1). The proof correctly weights each centre by e_γ^{−1}: Σ_p e_γ^{−1} ≤ 1.
- I re-derived the stabilizer steps:
  - a projectivity fixing L pointwise is u ↦ λu + b in the chart with L at infinity;
  - no nontrivial translation preserves an irreducible nonlinear curve;
  - so λ is injective, the group is homotheties about one point, and its order is ≤ the degree.

**Obj. 13 — Prop 5.5, p. 41: "retains all the preceding … conclusions" for the pool omits the one-line reason (5.9) passes to pools.** COSMETIC.
- If S has density α in the pool, then some constituent piece ν has |S ∩ P_ν| ≥ (α/2)·n_ν. By monotonicity of H, H_S ≥ H_{S∩P_ν} ≥ σ(b)e^{−o(s)}, because all constituents share the limiting profile.
- (5.8) is not needed for foreign carriers. Prop 5.3's pooled accounting is per piece, and §6 (6.4) uses only assigned masses ("pooling exp(o(s)) pieces changes this by only exp(o(s))"). Checked.

**Obj. 14 — Prop 5.5, p. 41: the core Bézout count needs the two-generic-combinations form.** UNCLEAR (exposition; true).
- Quote: "The core's isolation equations, restricted to its components, and Bézout bound its intersections with the core by O(EL²) per center."
- The core is cut out by many equations of degree ≤ L. Plain refined Bézout with all of them gives only E·L^{#eqs}.
- The needed form (p. 14, "isolated components … at most the Bézout product") is elementary for **points**, without the "perturb and specialize" sketch the algebra seat flagged:
  1. a generic combination g₁ is nonzero on every 2-dimensional component of the cone K_p through a core point, since the core is finite;
  2. a generic g₂ is nonzero on every curve component of K_p ∩ Z(g₁) through a core point;
  3. so every core point on K_p is isolated in K_p ∩ Z(g₁,g₂), and their number is ≤ deg K_p·L² ≤ E·L².
- Then EL² = δe^{6s\*}N = o(N), and covered core pairs number ≤ 2|core|·o(N).
- Fix: cite p. 14's form explicitly, or add steps 1–3.

### Considered and dismissed (each checked; recorded so others need not re-check)

**§4.3 line case:**
- (4.1): the lift (x₁, x₁²+x₂²); the circle about (a,0) becomes the line v − 2au = r² − a² (numerically verified); ≤ bM distinct lines; ≥ bh_H/2 incidences, since the lift is ≤ 2-to-1.
- ST gives bh_H ≤ C((bh_HM)^{2/3} + h_H + bM). The three branches all give ≤ CM²: b large with h_H = O(M); b large with h_H ≫ M; and bounded b, via h_H ≤ 2M² by two-circle intersection.
- (4.2) from Fs ≤ CF^{2/3}T + CN + CLF: L/s ≤ CM²/A² absorbs the last term; then F ≤ max(2CN/s, 8C³T³/s³).
- Hölder T³ ≤ L(Σ(b/L)^{1/2}N_b²)(Σ(b/L)^{1/4})²: 0 violations on 2,000 random cases. The negative control (dropping the second factor) failed 2,000/2,000.
- hT³/s² ≤ CM²s^{−2}Σ(b/L)^{1/2}N_b²; then dyadic sums over L ≥ b and s ≳ A give O(M²N²/A²).

**§4.3 nonlinear cases:**
- d ≥ 4: span ≤ 3 ⇔ π_pY spans ≤ P²; a 3-span forces p ∈ span; centres in the own plane are cheap; from outside the plane the projection is an isomorphism, so d_i = e_γ.
- Two curves in one group have distinct planes in a common P³, meeting in a line L. The perspective from p fixes L and maps Y_i → Y_j. Σ_{i≠j}n_in_j ≥ W²/2 once K ≥ 2C. Cauchy–Schwarz gives ε²N³/(2E) ≤ CN², which contradicts E = o(N).
- d = 3, (4.4): from Lemma 3.12(i). I checked it on a nodal cubic (3 − 2 = 1·1) and a twisted cubic projected from one of its points (3 − 1 = 2·1).
- d = 3, (4.5):
  - Lemma 4.1 non-tangency for curves holds (otherwise a nonlinear curve lies in a tangent line);
  - birationality and distinct images from v, otherwise there is a coplanarity contradiction at any contributing centre;
  - r_j ≥ t_j/2 ≥ d_j/(4e_γ);
  - Bézout Σr_jr_k ≤ d_jd_k gives Σe_γ^{−2} ≤ 16; in the equal-image branch, (4.3) gives ≤ 32.
- d = 3, invalid triples: weight ≤ 12CMe_γW². Hölder gives ε³N⁴/(2E²) ≤ CN³, which contradicts E = δN^{1/3}.

**§5:**
- (5.2) propagation. The degree is B·e^{s/2+√s+C} at width s/2. It is fresh at each step (no compounding), because second-type batches use any system of degree ≤ Be^{s/2}.
- The inherited lower boundary at s/2 equals the first greedy's stopping rule.
- (5.4): −1/2 + 1/9 = −7/18.
- (5.5) summability with t = u^{1/10}.
- Imbalance:
  - first-type batches have b₁ ≤ −1/2, since the batch polynomial would otherwise capture the whole piece;
  - remainder pieces have b_d ≥ 1/2, since they would otherwise be a second-type batch, being ≥ Ne^{−s^{1/3}−o(s^{1/3})} > Ne^{−√s} points isolated in degree < Be^{s/2}.
- (5.7):
  - Σb ≥ 0 by Bézout on the whole path;
  - Σb ≤ 0 by (5.9) just before b_d with rank ≤ N;
  - b₁ < 0 < b_d by the imbalance;
  - b₁ + b₂ < 0 since d > 2.

---

## Citation table (my scope)

| Cited result | What the paper claims it says | What the source says | Verdict |
|---|---|---|---|
| Kaminski–Kanel-Belov–Teicher [19, §3.2] (arXiv 0712.3878v1, refs/0712.3878v1/KKT.txt) | p. 27: "The generic conclusion is a form of generalized trisecant geometry; compare [19, Section 3.2]. We give the tangent calculation" | KKT.txt l. 460–464: "Theorem 2 First Generalization of The Trisecant Lemma. Let Z be a possibly singular equidimensional variety … of dimension n, other than a linear space, embedded into Pr, r ≥ n + 1. The variety of trisecant lines of Z, that is V1,3(Z), has dimension strictly less than 2n, unless Z is included in a (n + 1)−dimensional linear space and has degree at least 3" | **MATCH** ("compare"; not used as input. Lemma 4.1 is proved in full in the paper and I verified that proof) |
| Fulton [14, Prop. 4.4] | p. 32: "The point-projection formula, obtained from the linear-system degree formula with its base-point contribution [14, Proposition 4.4]" giving (4.4) | refs/Fulton/fulton.pdf is a course syllabus, not the book | **COULD NOT FETCH.** The paper proves the formula itself as Lemma 3.12(i), p. 24 (blow-up computation; checked by the algebra seat). I checked it on two examples (above) |
| Fulton [14, Thm 12.3, Ex. 12.3.1] (cited p. 14, consumed in §5 Bézout counts) | componentwise refined Bézout | — | **COULD NOT FETCH.** The multiplicity-free form used in (5.8), the carrier degree, and n ≤ ΠD_i is Walsh [27, Lemma 2.1], verified at source by the algebra seat. The isolated-points form for Prop 5.5's core is proved elementarily in Obj. 14 |
| Tidor–Yu–Zakharov [26, §§10.2–10.3] (arXiv 2608.14454v1) | p. 32: "closely related to the curve–cone estimates of Tidor, Yu, and Zakharov [26, Sections 10.2–10.3]" | TYZ.txt l. 62–63 (ToC): "10.2. Curves and cones in C3", "10.3. Curve-cone incidences via trisecants" | **MATCH** (attribution only; not used as input) |
| Thm B.2 (internal; Szemerédi–Trotter) | p. 29 "rich-line form"; p. 8, 30–31, 42 | p. 91: "the number of lines containing at least k ≥ 2 points of an n-point set is at most C(n²/k³ + n/k). The same assertions apply to finite point–line configurations in Rs and in real projective space." | MATCH at statement level. Proof is the incidence seat's |
| Lemma 2.1 (internal) | proper-flat cap N·B^{−c₀} incl. complex flats counting real points; line ≤ 2M; plane B^{2+o(1)} | p. 7 statement | MATCH. Only c₀ > 0 and the line row are needed in §4 (Obj. 10) |
| Lemmas 3.1, 3.3, 3.5, 3.6, 3.8, 3.9, 3.12, 3.15 (internal) | as quoted in my answers above | pp. 15–26 statements | MATCH at statement level. Proofs are the algebra seat's. Hypotheses checked at every use in §4–5 (Obj. 1; §5.2 answer) |

## Constant-dependency table (my scope)

| Constant | Fixed where | Depends on | Used where | Claimed independent of | Checked |
|---|---|---|---|---|---|
| c₀ (flat cap) | Lemma 2.1 | d (1/2 claimed; only > 0 needed) | Lemma 4.2 (tangency, common flats, t_H); Prop 4.3 flat/plane caps | N, δ, window | yes |
| η | Lemma 4.2 proof | c₀ (η < c₀/4) | low-weight flat deletion, t_H ≤ eB^{−c₀/2} | N, δ, w | yes |
| ε (Lemma 4.2) | input (§6 "the fixed ε") | — | root count e^{εw}; discarded weight e^{−εw+o(w)} | N, δ | yes |
| e, w | Lemma 4.2 hypotheses | window/profile (e_j or B^{d−l}; s or log B) | flat counts/weights | (parameters, not constants) | hypotheses verified for both configurations |
| C (ST) | Thm B.2 | absolute | Lemma 4.2, Prop 4.3 (4.1)/(4.2), Prop 5.5 light lines | everything | — |
| C (n_i ≤ CMd_i) | Lemma 3.1 | d | Prop 4.3 | assignment | yes |
| threshold A for S_H | Prop 4.3 | A | splits δN² vs M²N²/A² | — | yes |
| K (group threshold) | Prop 4.3 | d (K ≥ 2C for d ≥ 4; K ≥ 24C for d = 3) | light-group discard KNME | N, δ, assignment | yes |
| 7 (high-mult centres per curve) | Prop 4.3, d = 3 | absolute | deletion O(N) | — | yes (numerically) |
| 16 / 32 in (4.5) | Prop 4.3, d = 3 | absolute | Σ_p e_γ^{−2} | — | yes |
| E = δN/A | hypothesis | δ (no rate) | Prop 4.3 (δN² needs δ → 0; E = o(N), N⁴/E² ≫ N³ hold for δ = O(1)); core EL² | — | yes |
| s\* | Prop 5.1 proof | δ, B | smallest width; core degree Be^{3s\*} | — (sequence-dependent, legitimately; Obj. 3) | yes, no rate |
| widths s = 2^{−a}log B; their number ~ log₂(log B/s\*) | Prop 5.1 | B, s\* | every window | never used as a multiplicative factor | yes |
| batch thresholds Ne^{−√s}, Be^{±s/2}, Ne^{−s^{1/3}} | Prop 5.1 | s | greedy windows, imbalance | N/A | yes |
| G = O(1+√log s), K = O_d(G), λ_i = e^{−a_i}, a_K = s^{1/10}, a_i = 10a_{i+1} | Prop 5.1 | s, d; same for all trees of a width | (5.3)–(5.5) | node, piece, δ | yes (Obj. 4) |
| limiting profile b_i | Prop 5.1 (subsequence) | the chosen sequence of pieces | D_i, e_j, σ everywhere | — (legitimate) | yes |
| α in (5.9) | arbitrary fixed | — (shrinks by 2(d+1) per plateau, ≤ d times) | rank propagation | N, δ, S | yes |
| c_d, C_d (Lemma 3.6) | §3 | d | (5.9) propagation | a, L, components | yes (statement level) |
| C_n in Lemmas 3.8/3.9 | §3 | d | Prop 5.3; needs D/L ≥ C_n | — | yes, holds for large index (Obj. 1) |
| β < b < b′ < b″ | Prop 5.3 | profile (fixed points of the plateau) | margins (b′−β)s, (b′−b)s | N, δ | yes |
| precision h; K(h) bins; m(h) | Prop 5.5 | h only | agreement probability ≥ 1/(K(h)m(h)) | number of windows, N, δ | yes |
| h(N) → ∞ (diagonal) | Prop 5.5 | δ and all o(1) losses (slow enough) | profile convergence, pool mass | — (no rate) | yes |
| H (light lines) | Prop 5.5 | precision h; H ≤ B^{o(1)} | §6 per-direction counts | δ | yes |
| α (covered density in product) | Prop 5.5 | — (≥ 1/2 − o(1)) | §6 | N, δ | yes |
| pool mass n | Prop 5.5 | ≥ c(h)N at fixed h; ≥ N√δ, ≥ Ne^{−o(log B)} after diagonal | §6.2 | — | yes (Obj. 5) |

No constant claimed independent of N, δ or the window depends on them. No constant in §4–5 is circular: s\* → partition → terminal assignment → Prop 4.3 deletion → (h, H, h(N)) selection, and nothing feeds back.

## Verified line by line vs skimmed

**Verified line by line:**
- Lemma 4.1: generic part, including the k = l projection-from-the-tangent-flat argument and the span case analysis; local assertion (4.1.1).
- Lemma 4.2: tangency discards at both endpoints; common-(k+1)-flat discard with a nonlinear member (properness needs l < d−1); flat-in-H reduction; merging of the two families; low-weight deletion; slicing; t_H bound; dyadic ST sum; the final hypothesis paragraph for common and subpower windows.
- Prop 4.3: all three cases, including (4.1), (4.2), Hölder, the dyadic sums, the stabilizer argument, Cauchy–Schwarz, (4.3)–(4.5), the invalid-triple bound and the d = 3 Hölder contradiction.
- Prop 5.1: (5.2) and its propagation; batch counts; Lemma 3.3 isolation and the product trick; inherited lower boundary; core degree and EL²; tree construction, index ordering, path monotonicity; (5.3)–(5.5); summability over windows; terminal sizes; imbalance (b₁ ≤ −1/2 and b_d ≥ 1/2).
- Prop 5.2: carrier degree; (5.8); Σb ≥ 0; (5.9) envelope argument including the no-capture reduction; group selection; elimination of a; plateau-to-plateau growth with simultaneous cuts; boundary convention; Σb ≤ 0; (5.7).
- Prop 5.3: single-piece and pooled versions, including D ≥ C·L margins, exceptional mass via (5.8), the minor-combination step, foreign-carrier exclusion, and nonreal flats.
- Lemma 5.4: both cases of the polynomial test, systems, rank tests.
- Prop 5.5: nonreal-line omission; the Prop 4.3 application and what it deletes; core alternative; binning/Cauchy–Schwarz; averaging; orientation; diagonal; dyadic congruence; outermost refinement and pool; light-line restriction; exhaustion of cases.

**Skimmed or statement-level only (outside my scope):**
- Proofs of Lemma 3.3, 3.5, 3.6, 3.8, 3.9, 3.12, 3.15 (algebra seat). I used their statements and checked their hypotheses at each use.
- Proof of Theorem B.2 (incidence seat).
- Fulton's text (COULD NOT FETCH).
- The §6 consumption of my outputs (sparse_a / sparse_b), beyond confirming the interfaces at paper l. 2825–2845, 2914–2925, 3055–3064, 3188, 3240–3252, 3505–3520.

## Numerics (python, nice 19; script /tmp/secants_scripts/checks.py)

- Hölder inequality for T(L) (p. 31): 0 violations in 2,000 random dyadic instances. Negative control (dropping the (Σ(b/L)^{1/4})² factor): 2,000/2,000 failures, so the check can fail.
- Parabolic lift identity behind (4.1): 1,000 random instances exact.
- High-multiplicity centres per curve, from Σm² ≤ 2D(D−1) with m > D/2, D ∈ [3,500): maximum 7.
- (5.4) exponent −1/2 + 1/9 = −7/18; the tail bound Σ_{r>i}a_r < a_i/9 is exact as a rational identity. Floating-point failures at K − i ≥ 17 are rounding only.
- Onset of Σa_i = o(s^{1/3}) (Obj. 4): K = 16 at s = 10⁶ gives a₁ ≈ 4·10¹⁵. True only asymptotically, as stated.

## Verdict

**HOLDS AS READ** for §4 (Lemma 4.1, Lemma 4.2, Prop 4.3) and §5 (Props 5.1, 5.2, 5.3, Lemma 5.4, Prop 5.5). All 14 objections are UNCLEAR or COSMETIC exposition; none is a mathematical gap.

**COULD NOT CHECK:** Fulton [14] at source (book). Every use in my scope is either proved in the paper (Lemma 3.12(i)) or is the multiplicity-free refined Bézout (Walsh [27, Lemma 2.1], verified by the algebra seat). The isolated-points form for the core count is proved elementarily in Obj. 14.

**Conditional on other seats:** Lemmas 3.3/3.6/3.8/3.9/3.12/3.15 (algebra) and Theorem B.2 (incidence).
