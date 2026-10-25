# Referee report, seat "cells": §2 (pp. 8–14), §10 (pp. 76–82), §1.3 (pp. 6–7)
Paper: OpenAI preprint "Quasipolynomial Bounds for Arithmetic Progressions", 23 Sept 2026 (sha256 481eaf77…). Page numbers are printed = PDF page numbers. Every displayed formula quoted below was read off the rendered PDF page, not from pdftotext.

## Scope read (pages)
- **Read line by line:** pp. 6–7 (§1.3), pp. 8–14 (§2 in full: §2.1–2.8, Figs. 1–3, Thm 2.1, Lemma 2.2 and its proof, Def. 2.3), pp. 76–82 (§10 in full: Lemma 10.1, §10.2, Prop. 10.2, §10.3 steps 1–4, Prop. 10.3, §10.4, Prop. 10.4, proof of Thm 1.1 incl. the threshold form and the colouring corollary).
- **Read to test the interfaces §10 relies on (statements, plus the proofs where the dependency order is argued):** p. 23–24 (§3.5, the stopped tree and the sampling order); p. 25–28 (Prop. 4.1, Lemma 4.2 statement, Lemma 4.3 with its full proof); pp. 35–36 (§4.6, "Termination and the order of the budgets"); pp. 42–44 (Prop. 6.2 with proof, Def. 7.2, Lemma 7.1); pp. 69–75 (§9: Prop. 9.1, Lemmas 9.2–9.4, §9.6); p. 118 (Prop. D.3 statement); p. 120 (Lemma D.5 statement); pp. 122–123 (Def. D.6, Prop. D.7, Remark D.8); p. 193 (Thm I.15, opening of its proof, base case); §7.4 text around eq. (7.8)–(7.10) (pp. 51–52); Prop. 7.8 proof opening (p. 57); §8 paragraph "Averaging over the top kernel".

## Method
1. Wrote out Theorem 2.1 with explicit quantifiers (below) and matched each assertion against what Props. 10.2/10.3 and §10.4 actually state and prove.
2. For each place in §10.3 where a width at level j is bounded, recorded which data it is allowed to depend on (warm = p, forecasts, gaps, budgets at levels > j; cold-pre/late = may also use q_j) and checked that nothing cold at j flows back into A_j or A′_j.
3. Checked the choice order of all run-level parameters (D, degree cutoffs, ξ, η_k, T, p, d0, d*, N_c, γ, then per-layer U_j) for cycles.
4. Checked Lemma 2.2's hypotheses against the application in §10.4 (via Prop. 6.2's output) and Lemma 2.2's proof against the statement of Prop. D.7 and Prop. D.3.
5. Redid every elementary computation: block uniqueness, Lemma 10.1's coverage inequalities, Lemma 4.3's coverage inequalities, the dimension and width envelopes, the horizon T, the claim threshold ≥ e^{−p}, and the inversions in the proof of Thm 1.1 at both endpoints and for r-colourings.
6. Coordinator addendum: the two trace concerns ("mesh/truncation circularity" and "same-layer thresholds charged to width resets"). Located the paper's claimed resolutions and tested them; see the dedicated section.

## Theorem 2.1 with explicit quantifiers (as stated, p. 10)
There are D = D_k, η = η_k > 0, C_k, and nondecreasing polynomials P_1..P_D, P′_1..P′_D, R_root, R_cut, with degrees depending only on k, such that: for all p ≥ 2, a ≥ e^{−p}, cells (C_h, l_h, w_h ≤ 1/32) and progression-free inputs 0 ≤ f ≤ 1 on a positive-dimensional root box with E f B^− > a E B^+, if every root side H has log H ≥ R_cut(p, dims, Q_1..Q_D), then either (impossible) or some root slice of log-cost ≤ R_root(p, dims, Q_1..Q_D) carries a certificate at threshold (1+η)a for a new cell that keeps the old determining data under exact integer reparametrisation and adds ≤ d0 = (2+p)^{C_k} fresh slots plus downward copies, with
- (dimension) d′_i − d_i ≤ d0 + P_i(p, d_{i+1},…,d_D);
- (width) Q′_i − Q_i ≤ P′_i(p, dimension forecasts, Q_{i+1},…,Q_D);
- (root cost) slice cost and root-side cutoff polynomial in p, the dimension data, and every Q_i.
All exponents and η are independent of the number of increments.

**What §10 proves.** Prop. 10.2 gives d_i^out ≤ d_i + d0 + H_{i+1}², where H_D = d_D and H_i = d_i + H_{i+1}². The H_{i+1} term involves only d_{>i}, so (dimension) holds exactly, with P_i free of p. Prop. 10.3 gives Q_j^out ≤ q_j + P_j(p, d*, q_{>j}), which is (width) with "dimension forecasts" = d*. It also states that the root slice loss and the root-side cutoff are polynomial in p, d* and all q, which is (root cost). §10.4: "The dimension assertion of Theorem 2.1 is Proposition 10.2; its width assertion and root-cost assertion are Proposition 10.3." The correspondence is exact. Iteration independence holds because P_i comes from the fixed H-recursion, and P_j is a depth-D composition of the fixed F_j, G_j of §10.3 (p. 78). Neither depends on t or T. T enters only through d*, and Prop. 10.4 substitutes T = O_k(1+p) as a polynomial in p.

## Findings

### FATAL
None found.

### GAP
None found in scope. The load-bearing "warm" assertions that §10.3 consumes are out of scope here; they are listed under "did not check".

### EXPOSITION
**E1. Thm 2.1 is not self-contained as a one-step statement (p. 10).** It quotes "(2.4) Q′_i − Q_i ≤ P′_i(p, all dimension forecasts, Q_{i+1},…,Q_D)" and "Gap and discount choices can be made in advance from the dimension and cut-count forecasts." Its hypotheses never introduce forecasts or the gap γ, yet the certificate (2.2) depends on γ through B^+ ("For a small γ > 0", p. 9). In §10, d*, N_c (Prop. 10.2) and γ ("a sufficiently small fixed gain-dependent constant divided by a sufficiently large polynomial in 2+p+d*+N_c", p. 78) are objects of the whole run, fixed before round 1. The deduction in Prop. 10.4 is correct because it fixes them once and feeds the same γ through every round (Lemma 10.1's output boxes use (1+γ)ρ). Repair: state Thm 2.1 for given forecasts d̄ ≥ all dimensions and structural counts in the round, and N̄_c, with γ = γ(p, d̄, N̄_c), and make R_cut and R_root depend on d̄. Harmless.

**E2. Root-cutoff wording (p. 10 vs p. 80).** Thm 2.1 says the root cutoff is polynomial in "p, the dimension data, and all Q_h". Prop. 10.3 says "polynomial in p, d* and all incoming width logs". These are the same thing once E1 is fixed.

**E3. Prop. 10.4 (p. 81): "Every temporary threshold is at least a fixed positive multiple of a_0" is asserted, not argued.** It is true: targets are nondecreasing in t, and within a round only a k-dependent number of proportional discounts occur (the preparation discount is split over N_c cuts; D ascent coverings; s flag removals; D localisations; one compression, (1+γ)^m with γm small). It should say so. The follow-up "so it is at least e^{−p} after enlarging C" is correct: with p = C(2+log(1/α)), e^{−p} = e^{−2C}α^C ≤ cα/2 once e^{−2C} ≤ c/2, since α ≤ 1 and C ≥ 1.

**E4. Lemma 10.1, last paragraph (p. 77).** It quotes: "Their maximum is therefore at most Q_i plus an allowed warm loss." The compression also adds log(4 max{1,‖T‖_∞}/γ) to Q_i, from ρ ≍ γ w_min/(4 max{1,‖T‖_∞}). This term is covered by "warm" (log‖T‖ is polynomial in block dimension; γ is a forecast quantity), but it is not written.

**E5. Proof of Thm 1.1 (p. 81): "If α = 0 the density assertion is immediate."** This is a vacuous branch, since r_k(N) ≥ 1 for N ≥ 1. Harmless.

**E6. Lemma 2.2 proof (p. 11): "Choose a small fixed c > 0" precedes "Choose its fixed target discount ε0 and then c" (p. 12).** The order is fine because c is chosen last either way, but the sentence order reads as if c were chosen twice.

## Item-by-item record of the specific checks asked for
- **Cell definition and block uniqueness (p. 9, §2.2).** Given u and b_{<h}, two integer vectors within (1+γ)w_h ≤ (1+γ)/32 of the same real point differ by at most (1+γ)/16 < 1 in each coordinate, so they are equal. The padded boxes used later (radius 2w_i, p. 54; (1+2γ)r, §7.1) also stay below 1/2. Fig. 1's example was recomputed: A_2(1,b_1) = (1+b_1)/2, the unique pair is (1,1), and the weighted degree is ≤ 2. **OK.**
- **Precision convention Q_h = log(2/w_h).** With w_h ≤ 1/32, Q_h ≥ log 64. Empty blocks are padded with fixed width (Lemma 10.1), so Q_h(0) is constant. Used consistently in §10. **OK.**
- **Lemma 2.2 as stated vs as used in §10.4.**
  - Hypotheses: [0,1]-valued, progression-free, mean ≥ a ≥ e^{−p}, positive dimension n, all sides ≥ exp(poly(2+p+n)).
  - Prop. 6.2 (p. 42) supplies "terminal injective paths … The input is pulled back successively and masked … Its support is progression-free. At least a fraction ηa of terminal paths have mean at least (1−2η)a". Its proof adds (p. 44): "an injective integer-affine pullback of a function with progression-free support again has progression-free support; each flag mask only removes points." Injectivity on the box suffices for a nonconstant AP to stay nonconstant.
  - The threshold (1−2η)a is handled by the §2.1 convention (p. 9: "Multiplying a density threshold by a fixed positive constant changes its logarithmic budget by only a fixed additive amount. We absorb such changes … including the fresh rank bound d0").
  - Side lengths: §10.3 step 1 at j = D, "the absolute-return requirement at the last layer". Layers are sampled 1..D and budgets chosen D..1 (§3.5, p. 23), so layer D's sides are chosen first, from warm data p and n ≤ d*.
  - Impossibility clause: "If its hypotheses are impossible, the original certificate cannot exist" is the contrapositive through Prop. 6.2. That is valid, because Prop. 6.2 produces a positive fraction of terminal boxes satisfying the hypotheses.
  - **Match: OK.** I did not verify the omitted short axes against "every side sufficiently large"; see "did not check".
- **Lemma 2.2's proof vs Prop. D.7 / D.3 (statement level).**
  - D.7 (p. 122) concludes "rank B′ ≤ d + d0", where d0 is the rank in the absolute-rule hypothesis. Remark (p. 123): "The exponent is independent of the absolute rule, of d, d0, and of every variable dimension included in p."
  - Enlarging the resource parameter to P = poly(p+n), which D.7 needs because "Q any box of dimension between 1 and p", leaves the hypothesis true with the same d0. D.3 (p. 118) at fixed n0 gives rank, complexity and score bounds (2+p)^{C}, which are ≤ P / ≥ e^{−P}, with slice cost 0 and prime-side cutoff exp((2+p)^C) ≤ e^P.
  - Old test 1 at threshold (1−c)a: score ≥ ca. Target arithmetic: (1−ε0)(1+ξ0)(1−c) > 1+ξ. The Λ ≥ 1 branch is D.7's impossibility alternative.
  - **Consistent.** The claim that the fresh rank is independent of n is exactly D.7's additive form. Whether D.7 is true (Thm I.15) was not checked.
- **§2.7 / §10.3: every place a width at level j is bounded, and what it depends on.**
  1. Step 1: principal scale, lift ratio v/w_j, omission threshold, minimum sides. Depend on p, the structural and gap bounds, and U_{>j}. Warm. Only the ratio v/w_j is chosen; the width loss sees v only through log(w_j/r′_j) = log(w_j/v) + log(1/ℓ) (Lemma 9.4, p. 75).
  2. Step 2: per-cut loss A_j. It charges the higher failure's coefficient and denominator bounds (R_h, h > j), v/w_j, the higher shrink factors and the omission cutoff, all warm. A copy arriving from h > j and the case "lower width absolutely smaller than a higher width" charge Q_h + log(1/γ), with h > j. Cuts at j cost gap and dimension factors only, and cuts below j cost nothing. Preparation width ≤ q_j + N_c A_j.
  3. Step 3: ascent loss A′_j. It charges the inherited score and slice (cold at j+1, hence warm at j), the warm modular-product bound, the pivot geometry, the caps relative to chart mass, and the original stride. It adds Lemma 10.1's log M_i, log‖T‖, log(1/γ), and the fresh absolute widths (poly(p, d*): Lemma 7.1, and §9.6 "The original two absolute cutoffs … have also been kept").
  4. Step 4: cold-pre and late choices (rank R_j, perturbation, range, parent side, rank-stop probability, flag truncations, modulus cover). These may use q_j + N_c A_j. They feed U_j only, hence only the levels below j and the root.
  5. Prop. 10.3: Q_j^out ≤ q_j + N_c A_j + A′_j ≤ q_j + G_j(p, d*, N_c, log(1/γ), U_{>j}). Substituting U_h ≤ F_h(…, q_h, U_{>h}) for h > j gives poly(p, d*, q_{>j}).

  **No occurrence of q_j or q_{<j} on the right-hand side.** This is consistent with §1.3 ("this bound does not use the current Q_h or the lower precisions") and with Fig. 2. I also traced the height of W_j: it is polynomial in log R_j (§4.6, Cramer). The rank-stop probability at j is chosen after R_j, and e_j is used only for that probability and for discards at j, never for A_j or A′_j. No cycle.
- **§10.2: structural choices.** D is chosen from §9's weight recursion (depth s, at most s·L_wt^s). The degree cutoffs, the H-recursion, d0 = (2+p)^{C_k}, d*, and N_c (counted by dimension: each cut lowers dim W_i by one) use no width, rank, scale, or accuracy. I found nothing in §10.2 that depends on a later precision.
- **Run-level choice order:** ξ (Lemma 2.2) → prescribed loss fractions → η_k → (α) p, T → d0, d*, N_c → γ (from d*, N_c, to make (1+γ)^{O(Dd*)} and the per-cut discounts small) → per-round, per-layer U_D,…,U_1. η_k does not depend on γ or d*, because the losses are prescribed fractions and γ is then chosen to meet them. **No cycle.**
- **Prop. 10.4.**
  - Horizon: a_t ≥ (α/2)(1+η)^t gives a_T ≥ (α/2)(2/α)(1+η) > 1 for T = ⌈log(2/α)/log(1+η)⌉+1 = O_k(1+p).
  - Base certificate: with no slots B^± ≡ 1, and E1_A = α > α/2.
  - Threshold ≥ e^{−p}: see E3.
  - Root losses: per round R_root(p, d*, Q(t)), with Q(t) ≤ V and V and d* polynomial in 2+p of k-dependent degree. The sum over T = O(1+p) rounds plus max_t R_cut plus the margins is a fixed polynomial in 2+p. The exponents are independent of t and T.
  - Initial certificate on [N] (n = 1); root re-slices stay injective integer-affine, so progression-freeness is preserved.
  - Final contradiction: f B^− ≤ B^+ pointwise. **OK.**
- **Proof of Thm 1.1 (pp. 81–82).**
  - log N < C(2+log(1/α))^A ⟺ α < e² exp(−C^{−1/A}(log N)^{1/A}). Correct, and valid for all N ≥ 1 because Prop. 10.4 has no hidden N_0.
  - Threshold form: log N ≥ (log(2C̄/α)/c)^{1/ε} ⇒ r_k(N) ≤ C̄ N α/(2C̄) = αN/2 < αN. N ≥ 2 holds automatically since the right-hand side is > 0.
  - Domination by A(2+log(1/α))^A for A ≥ max{1, 1/ε, c^{−1/ε} max(1, log 2C̄)^{1/ε}} holds on all of 0 < α ≤ 1, including α = 1.
  - Colouring: α = 1/r, and W_r(k) ≤ ⌈exp(A(2+log r)^A)⌉ also covers r = 1.
  - **OK.**
- **Lemma 10.1 (compression), recomputed.** ‖T‖_∞(2+γ)ρ ≤ (2+γ)γ w_min/4 ≤ (3/4)γ w_min, which lies inside the margin γ w_min of the old enlarged box. Strict coverage is (2ρ)^m and enlarged coverage ≤ (2(1+γ)ρ)^m, using uniqueness of the old enlarged tuple. The selected centre loses (1+γ)^{−m} with m ≤ D d*. Within one weight, only linear constant-coefficient dependence occurs (weights are positive; §9.6 for absolute slots; C_in depends only on arguments < h−1 in Lemma 4.3). T is real unitriangular with bounded entries, and log‖T^{−1}‖ = O(m). **OK.**

## Coordinator addendum: the two trace concerns
**(II) "Need check thresholds from lower or same layer repeatedly charged as cost of width resetting w_i. Need independent Q_i." (trace l. ~1985)**
- Where the paper claims to resolve it:
  - Lemma 4.3 item 2 (p. 26): "At weight h, the relative width loss uses only dimension and gap factors, independently of R_h, Q_h, and the size of the rational section used in the cut. At weights above h, no width loss is necessary."
  - Its proof (p. 27): "The new h radius can be a fixed dimension/gap fraction of w_h, independently of e or R_h," and (p. 28) "Large section norms are charged only to lower/spatial precision; the own layer width uses only its gap and dimensions."
  - §4.6 (p. 35): "We spell out the absence of a width circularity … A cut at j uses only its own dimension and gap factors … A cut below j causes no shrinkage at j. With N_c the structural cut bound, the preparation width is therefore at most Q_j + N_c A_j"; repeated as §10.3 step 2 (p. 79).
- Test, part 1 (the coverage argument). I redid it from (4.2)–(4.3): b_h^old − C_h^old = r_h^new + r_in − c − E. With ρ_h, ρ_in, ‖E‖ ≤ γw_h/8, an old strict tuple gets full ρ_h-coverage for every new centre within (1+γ/2)w_h of l_h + c − l_in, and a new enlarged tuple lands inside (1+γ)w_h. So the own-layer loss is log(8/γ) + O(1) per cut, with no ‖e‖ and no R_h.
- Test, part 2 (where ‖e‖, R_h and the denominators go). They enter only:
  - the lower residual refinement ("dimension factors, γ^{−1}, w_h^{−1}, ‖e‖, and the coefficient bound … For every lower level these are permitted higher-level costs", p. 27);
  - the lower congruence modulus (log polynomial in the cold budget at h);
  - the spatial slice.
- Test, part 3 (lower cuts and repeats). Lower cuts act on higher polynomials by exact substitution (4.3), so higher widths are untouched. Multiple cuts at one level add N_c·A_j. A_j is fixed before any q_j-dependent choice, which is why the late choices at j are made against the worst-case prepared width q_j + N_c A_j.
- Test, part 4 (the copy). The forced "common decreased width" at h−1 ≪ γw_h charges Q_h + log(1/γ) to level h−1, which is higher data for level h−1.
- **Verdict: resolution holds as written** (Lemma 4.3 proof read in full; Lemma 4.2's bounds taken as stated).

**(I) "a physical mesh depends on a truncated expansion whose bound already depends exponentially on the truncation parameter … circularity concern unresolved." (trace l. ~1310)**
- In §10.2–10.3, no mesh or truncation parameter appears in steps 1–3, the warm part. Flag-truncation accuracies and the modulus-cover cutoff appear only in step 4 (p. 79: "every flag-truncation accuracy required by those requests. Choose the cutoff for the modulus cover after the relevant model and period bounds"), after A_j and A′_j are fixed. Back-flow is excluded by assertion (p. 80): "Auxiliary cold computations that establish a sharpened warm conclusion do not enlarge that conclusion's output budget. In particular their own cold costs do not return to A_j or A′_j."
- That assertion is substantiated where the width is actually produced:
  - Prop. 9.1 (p. 70): the new slice, the congruence and log(w_j/r′_j) are warm, while "The logarithm of the reciprocal returned full-mass score has cold cost at layer j".
  - Lemma 9.3 and §9.3 (pp. 72–73): the full modulus M is never charged: "this step does not charge log M to any budget".
  - §9.1 (p. 70): flag removal costs a proportional discount only.
  - Lemma 9.4: ℓ is warm.
- So any cold truncation or mesh cost at j lands in the score, which is warm data at j−1, not in a width. I found no mesh or truncation parameter of §10.2–10.3 feeding a bound that should be warm.
- Inside §7.4, the paper's own ordering is (pp. 51–52): "choose a large pre threshold T, before choosing Z" (p. 51) … "Subsequent models and menus may charge log T: the truncation just proved used only the unexpanded score and the current cap and accuracy, not those later menu sizes … forecast successively before Z. Then Z is chosen to contain their periods, and only then are the individual witness comparisons and late sampler parameters fixed." The truncated Möbius expansion (7.8) has absolute error ≤ 1+T, on an exceptional event of mass O(T^{−9}). The dependence on T is **linear**, entering budgets as log T, not exponential.
- The exponential-in-truncation risk the trace names (enumerating subsets of retained modes) is explicitly avoided: "pigeonholing bases, rather than arbitrary subsets of frequencies, costs only a warm fraction" (Prop. 7.8 proof, p. 57) and "we do not enumerate all subsets of the truncated modes" (§8, p. 63). Meshes are claimed to have "polynomial logarithmic size" at a specified accuracy, with warm Lipschitz bounds and independence from orbit coefficients (Lemma 7.5-type statement, p. 53).
- The chain score → T → pivot threshold → mesh accuracy → menu size → Theorem 3.4 errors, as written, is a linear order with no back-edge.
- **Verdict: within my scope the resolution holds.** That the §7.4 / §7.8 / §8 estimates themselves deliver these bounds is other seats' scope and was not verified here. I could not pin the trace's phrase "physical mesh" to a specific object in the paper beyond the field and point-value meshes above.

## External inputs checked
None of the paper's external inputs (LSS [35, Thm 1.2]; Schoen–Sisask [43, Thm 5.4]) is invoked in §2 or §10; they enter through Thm C.1 and the appendices. In scope I checked only internal interface statements: Prop. D.7 (p. 122–123), Prop. D.3 (p. 118), Lemma D.5 (p. 120), the statement of Thm I.15 (p. 193), Prop. 6.2, Prop. 9.1, Lemma 4.3. No external PDF was fetched by this seat.

## What I skimmed / did not check
- The truth of every "warm" claim that §10.3 imports: §3 (Lemma 3.2 one-site comparison, Thm 3.4 warm clause), §5 (detection independent of Q_j), §7–§8 (passive and active ascent; that the ascent's returned score and width loss are as claimed; that no new absolute slots appear at active steps), §9 (I read the statements and the localisation logic, not the measure-theoretic details of Lemma 9.2), Lemma 4.2's proof (§4.3–4.5).
- That terminal boxes with omitted (short) axes still meet "every side sufficiently large" in Lemma 2.2. Prop. 6.2 and §3 handle short axes by enumeration; I did not trace this.
- The proofs of Prop. D.3, Lemma D.5, Thm C.1, Thm I.15, and all of Appendices A–I.
- §11 beyond Prop. 11.1 and Cor. 11.2, which I read in passing.
- The Lean artefact, and the separate kernel replay (not run, per brief).

## Verdict
**HOLDS AS READ IN SCOPE.** The formal assembly is correct as written:
- §10 proves exactly the three assertions of Thm 2.1 (dimension = Prop. 10.2, width and root cost = Prop. 10.3), with iteration-independent exponents.
- The width recurrence never puts q_j or lower widths on its right-hand side.
- The run-level choice order (ξ → η_k → p, T → d0, d*, N_c → γ → U_D..U_1) has no cycle.
- Lemma 2.2's hypotheses match its use at terminal boxes.
- The inversion to Thm 1.1, its threshold form and the colouring bound are correct at both endpoints.
- The two trace concerns are addressed in the paper (Lemma 4.3(2)/§4.6 for same-layer charging; the T→Z→late order, log T charging and basis pigeonholing for truncation/mesh), and the addressing is sound as far as my scope reaches.

Only EXPOSITION issues were found (E1–E6, E1 being the substantive one: Thm 2.1 needs forecasts and γ among its inputs). Correctness of the whole is conditional on the out-of-scope warm/cold claims of §§3–9 and on Appendices C/D/I.
## Appendix: working notes (chronological)
## Partial notes (appended as I go)
- started 2026-10-12; scope pp. 6-7, 8-14, 76-82
- read pp.6-14 and 76-82 from PDF render (done first pass).
- checked: block uniqueness (2*(1+gamma)/32 < 1) OK; T formula OK; e^{-p} threshold check OK (alpha^C e^{-2C} <= c alpha/2); Thm 1.1 inversion algebra OK; threshold/colouring endpoints OK.
- Lemma 10.1 compression arithmetic: ||T||(2+gamma)rho <= (3/4)gamma w_min OK; discount (1+gamma)^m OK.
- open: sampling order vs choice order (constant cycle?); Lemma 2.2 hypotheses at terminal box (progression-free pullback? injectivity of path map); Prop D.7 additive d0 independent of resource parameter.
- Lemma 2.2 vs Prop D.7 (p.122-123) statement-level check: additive rank d+d0 with d0 = rank in the absolute-rule HYPOTHESIS, exponent E independent of d,d0 and variable dims; resource enlargement P=poly(p+n) leaves hypothesis satisfied with same d0. Consistent.
- Prop 6.2 (p.42-44) supplies: terminal injective paths, progression-free support (injective pullback + masks), mean >= (1-2eta)a on fraction >= eta*a. Matches Lemma 2.2 hypotheses (modulo the e^{-p} discount convention of §2.1).
- §3.5 (p.23): layers sampled 1..D, budgets chosen D..1; terminal boxes after layer D; "absolute-return requirement at the last layer" = layer D chosen first. Consistent.
- §4.6 (p.35-36): height of W_j poly in log R_j; rank-stop prob chosen after R_j. No cycle found.
- COORDINATOR ADDENDUM (trace concerns): (I) mesh/truncation circularity -> paper's resolution text at §7.4 (p. 52, plain l.3324-3333) "Subsequent models and menus may charge log T: the truncation just proved used only the unexpanded score and the current cap and accuracy..."; Prop 7.8 proof (p.57) "pigeonholing bases, rather than arbitrary subsets of frequencies, costs only a warm fraction"; §8 (plain l.3957) "we do not enumerate all subsets of the truncated modes". §10.3 step 4 places flag-truncation/modulus-cover/Z choices in cold-pre at j AFTER A_j, A'_j. (II) same-layer charging -> §4.6 "We spell out the absence of a width circularity" + §10.3 step 2. Checking §4.2 cut mechanics next.
