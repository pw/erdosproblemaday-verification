# Referee report — seat "common" (Section 6, PDF pp. 28–35, + brief item (v) second half)

Paper: OpenAI, "A power saving for planar unit distances" (23 Sep 2026), local copy /tmp/oaimath/167/paper/paper.pdf.
Read: §6 in full, line by line, in paper.txt AND the rendered PDF pp. 28–35 (every displayed formula checked on the
render; the text extraction agrees with the render on every formula used below). Also read for context: §1.2, §3.1–3.4
(Lemma 3.1, Cor 3.2/3.3, (3.13)–(3.17)), §4.1–4.2 ((4.2)–(4.9)), §4.4 (states, (4.16)–(4.18), Lemma 4.5), all of §5
(rendered p. 25 for the score display), Lemma 2.5/2.6. Those are other seats' scope; I used them only as inputs.

## Verdict for my scope

**HOLDS AS READ.** Every step of §6 — (6.1)–(6.13), Lemma 6.1, Lemma 6.2, the classification, (6.7), Prop 6.3,
Lemma 6.4, Prop 6.5 — checks out line by line, *conditional on* the §5 inputs it imports: Prop 5.5 (upper budget,
including for the templated experiment Pθ and its collision term M/d(p)), Prop 5.6 (rare lower budget), Lemma 5.3,
(5.7) (= Cor 3.3 integrated), Lemma 4.5 (consistency, m = O(1), match implications), Lemma 2.5 and (5.4).
I found **no FATAL and no GAP**. Objections below are COSMETIC/UNCLEAR wording items; one of them (O2) matters in the
sense that a literal reading of the paper's definition of "row" makes Lemma 6.2 false (my Control 3), but the proof
and every application use full rows, so it is a wording fix, not a mathematical gap.

The brief's central question — **is Lemma 6.2 sound when U(q,θ) is selected after seeing θ, which is correlated with p
through q?** — **Yes.** Explicit probability space and the two bad events are in §A below. The correlation through q
is harmless because (i) the only place (q,θ) enters is the identity E[ν_{H(p)}(U(q,θ)^c) | q,θ] = ν̃_q(U(q,θ)^c),
which needs exactly p ⟂ θ | q (true by construction (5.9): the template is built from *other*, independently drawn
neighbours of q), and (ii) the second bad event is a function of p alone, defined per history h with no reference to
U, and it catches *every* admissible support of each type simultaneously, so no selection rule can dodge it. Neither
bad event conditions on the selected support. The genuinely hard thing the lemma handles is not the θ-selection but
the per-centre discrepancy between Law(X(p) | q) and the mixture of predictions ν̃_q (they can be totally different
at a single q); that is paid by the history-indexed exceptional sets, which average correctly because the p-marginal
of the joint law is µ. My exact toy (check (c)) finds the worst case over all (q,θ)-measurable selection rules at
0.78η–0.81η on a structured family (so the O(η) price is real, the lemma is not vacuous), never above 8η, and three
controls that drop a hypothesis each produce P = 1.

## §A. Lemma 6.2 written out (the brief's request)

Fix a level. Ω = {(p,q,θ)} finite, P(p,q,θ) = 1{(p,q)∈E}/|E| · a(q,θ), a(q,θ) = P(θ|q) (template = histories of k
further i.i.d. neighbours of q). Under P: p has marginal µ; p ⟂ θ | q. X(p) = true state of p at this level;
H(p) its history; ν_h = Law_µ(X | H = h); ν̃_q = Σ_p ω(p|q) ν_{H(p)}. U(q,θ) is any (q,θ)-measurable choice of a FULL
row {a}×B, a FULL column A×{b}, or a set of ≤ 2 states; G ⊆ Q×Θ with ν̃_q(U(q,θ)) ≥ 1 − 3η² on G; 0 < η < 1/2.

Bad event 1: N₁ = G ∩ {ν_{H(p)}(U(q,θ)) < 1 − η}.
  P(N₁) = E[1_G · P(ν_{H(p)}(U^c) > η | q,θ)] ≤ E[1_G · η^{-1} E[ν_{H(p)}(U^c) | q,θ]]
        = E[1_G · η^{-1} ν̃_q(U(q,θ)^c)] ≤ 3η²/η = 3η.
  The equality E[ν_{H(p)}(U(q,θ)^c) | q,θ] = Σ_p ω(p|q) ν_{H(p)}(U(q,θ)^c) is where p ⟂ θ | q is used; U is a
  constant once (q,θ) is fixed.
Bad event 2: N₂ = {X(p) ∈ Exc(H(p))}, Exc(h) = E1_h ∪ E2_h ∪ E3_h where E1_h = complement of the unique full row of
  ν_h-mass ≥ 1−η (∅ if none; unique because 1−η > 1/2), E2_h likewise for columns, E3_h = {x : ν_h(x) ≤ η} if some
  ≤2-set has ν_h-mass ≥ 1−η (∅ otherwise). ν_h(Exc(h)) ≤ η + η + 3η. P(N₂) = Σ_h µ(H=h) ν_h(Exc(h)) ≤ 5η — this uses
  only that p ~ µ, under which Law(X | H=h) is EXACTLY ν_h by definition (the paper's "exactly" is correct here).
Inclusion {G, X(p) ∉ U(q,θ)} ⊆ N₁ ∪ N₂: on G \ N₁, ν_h(U) ≥ 1−η with h = H(p). If U is a full row it is THE row
  of E1_h, so X ∉ E1_h ⇒ X ∈ U; columns likewise; if |U| ≤ 2 then every atom of mass > η lies in U (omitting one
  would give ν_h(U) < 1−η), i.e. M_h ⊆ U, and X ∉ E3_h means X ∈ M_h ⊆ U. Hence P(G, X(p) ∉ U) ≤ 3η + 5η = 8η. ∎
(The same inclusion holds for every admissible U at once, which is why θ-dependent selection cannot exploit anything.)

## §B. Line-by-line notes (what I checked and how)

**(6.1)/(6.2).** y_q ∉ Y_θ ⇔ ∃j: ν_{h_j}(R_{y_q}) < 1 − k^{-2}. Each (p_j, q) has the uniform edge law when q ~ κ.
Union bound: ≤ k·P_E(1 − ν_{H(p)}(R_{y_q}) > k^{-2}); Markov: ≤ k·k²·E_E[1 − ν_{H(p)}(R_{y_q})]. Integrate on C;
(5.7) says k³∫_C E_E[…] = o(S). Correct (strict/non-strict thresholds consistent).

**Lemma 6.1, first assertion.** Selected y* is a function of X_1..X_k; misses among X_{k+1..2k} ~ Bin(k, β), β > α.
N < kα/2 ⇒ |N − kβ| > kβ/2 ⇒ Chebyshev ≤ kβ(1−β)/(kβ/2)² ≤ 4/(kβ) < 4/(kα) ≤ 1/2 (uses kα ≥ 8). So
P(E1) ≤ 2P(E2), E2 = {∃y: first half ⊂ R_y, ≥ kα/2 misses in second half}. Symmetrisation: (X_1..X_{2k}) =ᵈ
(Z_{σ(i)}) with σ a uniform split independent of the pooled Z. For y = (a,b), {i: Z_i ∈ R_y} = {i: u_i = a} Δ
{i: v_i = b}; each of the two sets is determined by which of ≤ 2k observed first (resp. second) labels a (resp. b)
equals, or none ⇒ ≤ (2k+1)² index patterns. **The (2k+1)² count is right** (the "or none" option covers centre labels
not carried by any sample). A pattern with m ≥ kα/2 misses all in the second half: C(2k−m,k)/C(2k,k) =
∏_{i<m}(k−i)/(2k−i) ≤ 2^{-m} ≤ 2^{-kα/2}; 0 if m > k. Union bound ⇒ 2(2k+1)²2^{-kα/2}. Repeated states: indices, fine.
**Second assertion (6.3).** Given q: p_1..p_k i.i.d. ω(·|q), X_j | p_j ~ ν_{H(p_j)} ⇒ (X_j) i.i.d. with law ν̃_q
(sum over p). Given θ, X_j independent ~ ν_{h_j}. On F = {∃y ∈ Y_θ: ν̃_q(R_y) < 1 − k^{-1/4}} pick y*(θ);
P(all X_j ∈ R_{y*} | θ) ≥ 1 − Σ_j ν_{h_j}(R^c_{y*}) ≥ 1 − k·k^{-2}. So (1 − 1/k)P(F|q) ≤ P(∃y: ν̃_q(R_y) < 1−α,
all X_j ∈ R_y | q) with α = k^{-1/4}, kα = k^{3/4} ≥ 8 for k ≥ 16; 2/(1 − 1/k) ≤ 4. Correct.
**Remark.** ∫_C 4(2k+1)²2^{-k^{3/4}/2} = W_c·(…) ≤ k^{1/16}S·4(2k+1)²2^{-k^{3/4}/2} = o(S). Correct (W_c ≤ S/ε, ε = k^{-1/16}).

**Application of Lemma 6.2.** ≤ 3 witnesses, each with ν̃_q(R_y) ≥ 1 − k^{-1/4} off the (6.3) event ⇒ intersection
mass ≥ 1 − 3k^{-1/4} = 1 − 3η² exactly for η = k^{-1/8} (η < 1/2 once k > 256). Cost ∫_C 8η = 8k^{-1/8}W_c ≤
8k^{-1/16}S = o(S). Empty intersection impossible once 3k^{-1/4} < 1. Correct.

**§6.2 geometry.** (6.4), the "third outside the row ⇒ ≤ 1 state", (6.5), "three pairwise-distinct ⇒ ∅", Figure 2's
bit/endpoint determination at a centre base and at a point base, the row ⇒ bit 1 rule, and the singleton rule were all
checked EXHAUSTIVELY on a 5×5 label grid plus unseen labels (check (d)): 0 errors. Figure 2's labels are correct
((a,b')–(a,b) and (a',b)–(a',b') bit 1; the vertical edges bit 0). The classification (∅ / singleton / sharing pair with
all-in-line or third-outside / pairwise-distinct with exactly 2 or ≥ 3) is exhaustive.
**Bad edges and (6.6).** ∫_C P(bad) ≤ ∫m [O(1)] + (6.2) [o(S)] + ∫(6.3)-failure [o(S)] + transfer [8k^{-1/16}S]. Correct.
The transfer is applied with G = complement of the (6.3) event, which is (q,θ)-measurable, and U depends only on
(level, θ). Correct.
**"Never renormalise ρ."** Correct and load-bearing: the lower bounds use E[c(ρ)1{Y1=Y2} − 1{Y1≠Y2} | base] =
c(ρ)(ρ²+(1−ρ)²) − 2ρ(1−ρ) EXACTLY because Y1, Y2 are i.i.d. Bernoulli(ρ) given the base under the full law (Q: given
(q,θ), p,r i.i.d. ω(·|q); Pθ: given (p,θ), q,q' i.i.d.); bad pairs enter only additively via score ≥ c·1{Y1=Y2} −
1{Y1≠Y2} − (1+λ)1{some slot bad}. Renormalising to good edges would move ρ across 1/2 ± δ and flip c(ρ).
**(6.7).** Identity: ρ²+(1−ρ)² − 2ρ(1−ρ) = (2ρ−1)². With x = 2ρ−1, ρ²+(1−ρ)² = (1+x²)/2. Inside: x² + λ(1+x²)/2
≥ λ/2 (equality at ρ = 1/2). Outside (|x| > 2δ): x²(1−λ/2) − λ/2 is increasing in |x|, infimum 4δ²(1−λ/2) − λ/2 =
3.7499·10⁻⁴ ≥ 4δ² − λ = 3.5·10⁻⁴ > λ/2 = 2.5·10⁻⁵. Verified analytically and on 200,010 exact rationals (check (a)).

**Prop 6.3.** Slice by θ (π_θ = P(θ), b_θ = P(bad | θ), same π_θ in both experiments since the attached template at a
Q base has marginal Σ_q κ(q)a(q,θ)). Each slot in either experiment has law ω(p,q|θ) ⇒ P(some slot bad | θ) ≤ 2b_θ.
Branches of (6.10):
 - ∅: b_θ = 1; d_Q + d_Pθ ≥ −V_Q − V_Pθ ≥ −1 ≥ (λ/4)·1 − C. ✓
 - singleton {y}: in Pθ both good slots share θ hence both centres have state y; same base point ⇒ same agreement
   pattern ⇒ same bit, and N holds (same state). d_Pθ ≥ (1−λ)(1−2b_θ) − 2b_θ; d_Q ≥ −V_Q ≥ −1/2; sum
   ≥ 1/2 − λ − O(b_θ) ≥ (λ/4)(V_Q+V_Pθ) − Cb_θ since V_Q+V_Pθ ≤ 1. ✓ (no transfer needed in this branch)
 - sharing pair, all candidates in that row: U = full row a (mixture mass ≥ 1 − 2k^{-1/4}); good ⇒ A_p = a = A_q ⇒
   consistent bit 1; V = P(Y1≠Y2) ≤ 2b_θ in each experiment; d_i ≥ −V_i ⇒ d_Q + d_Pθ ≥ −4b_θ. ✓ (column: bit 0)
 - sharing pair + third outside: intersection {(a,b'')} or ∅ (∅ ⇒ (6.3)-failure for every q ⇒ b_θ = 1); good point
   states all equal x* ⇒ at a centre base equal bits and N; d_Q ≥ 1 − λ − O(b_θ), d_Pθ ≥ −1/2. ✓
 - pairwise distinct: ≥ 3 ⇒ empty common cross ⇒ all bad; exactly 2 ⇒ good point states in the two corners, good
   centre states in {y1,y2}, equal bits ⇒ same opposite state ⇒ N, at BOTH base types; each d ≥ λ/2 − O(b_θ) by
   (6.7). ✓
 Summation: Σ_θ π_θ(d_Q+d_Pθ) = common parts of D_Q + D_Pθ at the level; Σ_θ π_θ V(θ) = E_base 2ρ(1−ρ); error
 C∫_C Σ_θ π_θ b_θ = C∫_C P(bad) = o(S). No 1/π_θ and no count of templates enters — correct, and important since M
 can be t^{o(1)}.
 **Signs of the cancellation.** Prop 5.6: noncommon score ≥ 2E H*_x − 2E H*_y − o(S), x = star vertex. Q: x = q ⇒
 2E_κH_q* − 2E_µH_p*. Pθ: x = p ⇒ 2E_µH_p* − 2E_κH_q* (p ~ µ, q ~ κ by Lemma 5.3). Sum = −o(S). **Signs correct.**
 Sandwich: (λ/4 − 10δ²λ)(C_Q + C_Pθ) ≤ o(S), 10δ² = 10⁻³ < 1/4 ⇒ (6.8). (6.9): common part of D_Q ≥ −C_Q ⇒
 2E_κH_q* − 2E_µH_p* − C_Q − o(S) ≤ D_Q ≤ 10δ²λC_Q + o(S) ⇒ E_κH_q* ≤ E_µH_p* + o(S). Direction correct and is
 the direction Prop 6.5 needs.

**(6.11), Lemma 6.4.** Coupling h ~ µ(H = h), p',p'' i.i.d. µ_h: P(A(p') = A(p'')) = Σ_h µ(H=h)‖(ν_h)_A‖², so E F =
integrand of T. ✓ Per-place bound, derived: put α = −log|Z|_v + log c_v, β = log|W|_v − log c_v (c_v = √2 at ∞, 1
finite; from Lemma 4.5's match implications). (4.7) gives l ≤ −log|Z|_v ≤ α and u ≥ log|W|_v ≥ β. Then
∫_l^u F ≤ [min(u,α) − l] + [u − max(l,β)] − (u−l) = min(u,α) − max(l,β) ≤ α − β = −log|Z|_v − log|W|_v + 2log c_v.
This holds at EVERY place, including zero-width ones, precisely because (4.7) is imposed at every place. Σ* over
places: product formula kills the logs (Z, W ∈ N^×; finitely many nonzero terms), Σ*2 log c_v = log 2 (archimedean
weight 1). So ∫_L F ≤ log 2. ✓ Good rare: F ≥ −1{p' exc} − 1{p'' exc} (F = −1 forces a mismatch in the dominant
coordinate) ⇒ −∫_G F ≤ H*_{p'} + H*_{p''}; damaged: F ≥ −1 ⇒ −∫_B F ≤ W_b. ✓ Diagonal: F ≡ 1, ∫_C F = W_c;
P(diag) = Σ_p µ(p)²/µ(H^{-1}H(p)) ≤ |H(P)| max µ ≤ L^{2K}·t^{1+o(a)}/t^{2+2a+o(a)} = t^{-1+o(1)}; times
W_c ≤ k^{1/16}S with k = t^{o(1)}: o(S). ✓ Hence T ≤ log 2 + 2E_µH_p* + W_b + o(S) = 2E_µH_p* + o(S). ✓

**Prop 6.5.** Bad ordinary edge: inconsistent or ν_{H(p)}(R_{y_q}) < 1 − k^{-2}; ∫_C P(bad) ≤ O(1) + k²∫_C E_E[…] =
O(1) + o(S)/k. ✓ Y_p = states of good neighbours; each has ν(R_y) ≥ 1 − ζ and X(p) ∈ R_y (consistency, R symmetric).
(6.13) branches: ∅ (b_p = 1, LHS ≥ −3/2); singleton (r+s ≥ ν(R_{(a,b)}) ≥ 1−ζ ⇒ τ ≥ (r+s)²/2 − 1 ≥ −1/2 − ζ;
d_P ≥ 1 − λ − O(b_p)); shared row all-in-row (τ ≥ (1−2ζ)² − 1 ≥ −4ζ; X(p) in row; all good bits 1; 2ρ_p(1−ρ_p) =
P(Y1≠Y2|p) ≤ 2b_p; d_P ≥ −2b_p — and RHS ≤ (λ/4)·2b_p − C(b_p+ζ), so C ≥ 4+λ/2 suffices); third outside (singleton
intersection of mass ≥ 1 − 3ζ, τ ≥ 2(1−3ζ)² − 1 ≥ 1 − 12ζ); two corners (τ ≥ 2·(1−2ζ)²/2 − 1 ≥ −4ζ by Cauchy–Schwarz
on two atoms; X(p) a corner; bit determines neighbour state; d_P ≥ λ/2 − O(b_p) by (6.7)); three pairwise-distinct
impossible (X(p) would lie in an empty intersection). All four τ bounds checked numerically (check (d)), with a false
bound as control. Averaging: E_µ τ(ν_{H(p)}) integrated on C is T; ζW_c ≤ k^{-31/16}S. ✓ Noncommon part of D_P ≥
2E_µH_p* − 2E_κH_q* − o(S) ≥ −o(S) under the standing assumption (and (6.9)). ✓ C_P = o(S). ✓
**Final step (f ≤ C(V_P + V_Q)).** ℓ(x) = conditional majority bit. P_E(Y ≠ ℓ(p)) = E_µ min(ρ_p, 1−ρ_p) ≤ V_P since
min ≤ 2ρ(1−ρ). Label maps ℓ_P: P → {0,1}, ℓ_Q: Q → {0,1} are genuine label maps on the vertex sets, so Lemma 2.5
applies with s = P_E(ℓ_P(p) ≠ ℓ_Q(q)) ≤ V_P + V_Q. If s ≤ s_0: a_0 with µ{ℓ_P ≠ a_0} + κ{ℓ_Q ≠ a_0} ≤ Cs, so
f ≤ P_E(Y ≠ a_0) ≤ V_P + Cs ≤ (C+1)(V_P+V_Q). If s > s_0: f ≤ 1/2 ≤ (V_P+V_Q)/(2s_0). **Direction correct**;
"V_P + V_Q small ⇒ s small" holds since s ≤ V_P + V_Q. Then ∫_C f ≤ C(C_P + C_Q) = o(S); ∫_G f ≤ ∫_G(h_P + h_Q + m)
= E_µH_p* + E_κH_q* + O(1) = o(S) by (5.4) and Tonelli; ∫_B f ≤ W_b/2 = o(S); L = C ⊔ B ⊔ G. S = o(S), contradiction. ✓

Hand-wave phrases in §6 (grep of "clearly|it follows|similarly|the same argument|same estimate|analogous|as before|
symmetric|immediate|obvious|directly|exactly"): 7 hits — "exactly ν_h" (L6.2; exact, by definition), "exactly two
point states" (Fig. 2; exact), "The same estimate as in the singleton case applies" (checked), "exactly two
candidates" (exact), "exactly W_c" (exact, F ≡ 1 on the diagonal), "As before, a pair with a bad slot costs only
O(b_p)" (checked: ≤ (2+λ)·2b_p), "Columns give bit 0 and the same estimates" (checked; symmetric). None hides a step.

Euclidean content in §6 (brief item (i)/(viii)): §6 itself is combinatorial/probabilistic. Its Euclidean input is
inherited entirely through consistency (Lemma 4.5: exactly one of A, B1 agrees, and the bit says which — this is the
reciprocity d·d^{-1} of (4.1)). Under a parabola-type metric (jumps (d, d²), not reciprocal) nothing forces exactly
one label to agree at each threshold, so the strict-cross classification, the "row ⇒ bit 1" rule and Figure 2 would all be unavailable, so §6 would not run;
§6 contains no step that proves too much on its own. Lemma 6.4 uses only (4.7), the match implications and the
product formula (not Euclidean). §6 uses the near-4/3 density only through the parameter facts it imports
(W_c ≤ k^{1/16}S, k³/S → 0, M, |H(P)| ≤ t^{o(1)}, max µ ≤ t^{-1+o(1)}).

## §C. Objections (numbered)

**O1 — Lemma 6.1 statement, p. 29. COSMETIC (exposition).** "Let ν be a probability measure on a finite product set
and let X1, . . . , Xk be independent samples from ν. For 0 < α < 1 and kα ≥ 8, P(∃y : ν(R_y) < 1 − α, X1, . . . ,
Xk ∈ R_y) ≤ 2(2k + 1)² 2^{−kα/2}." The range of y is not stated; in (6.3) y is a CENTRE state whose labels need not
occur in the product set carrying ν. The proof's count already covers this ("or none"), and "select one by a fixed
ordering" needs a countable range (finite here). Fix: "for y ranging over (A∪A')×(B∪B') for any label sets A', B'".

**O2 — definition of row/column, p. 28, used in Lemma 6.2, p. 29. COSMETIC/UNCLEAR (wording; the proof is right for
the intended reading).** "A row means a set with fixed first coordinate; a column has fixed second coordinate."
Read literally ("a set all of whose elements share the first coordinate") Lemma 6.2 is FALSE: my Control 3 (400
points in one row, distinct columns, one history, centres with 2 private neighbours, U = row minus the centre's own
neighbours' states) satisfies ν̃_q(U) = 0.995 ≥ 1 − 3η² (η = 0.05) and gives P(G, X ∉ U) = 1 > 8η = 0.4. The proof
needs FULL rows ("If a row has mass at least 1 − η, it is unique" is false for sub-rows), and both applications use
full rows ("use that row or column as U"; "places every good point in the same row or column"). Fix: "a row is
{a}×B (all states with first coordinate a)".

**O3 — Lemma 6.2 proof, p. 30. COSMETIC (exposition).** "Hence on G, E[ν_{H(p)}(U(q, θ)^c) | q, θ] ≤ 3η². The event
that this support has ν_{H(p)}-mass less than 1 − η therefore has probability at most 3η." The event bounded is
G ∩ {ν_{H(p)}(U) < 1 − η}, and the equality E[ν_{H(p)}(U^c) | q,θ] = ν̃_q(U^c) should be displayed, since it is the
single place where p ⟂ θ | q is used. True as intended (§A).

**O4 — Lemma 6.4 proof, p. 33. UNCLEAR (exposition; I supply the derivation in §B).** "The A-match can hold only for
s ≤ − log |Z|_v + O_v(1), and the B1-match only for s ≥ log |W|_v − O_v(1). … Therefore ∫_l^u F(p′, p′′) ds ≤
− log |Z|_v − log |W|_v + O_v(1)." The inference needs BOTH (4.7) inequalities (l ≤ −log|Z|_v, u ≥ log|W|_v) — the
paper names them one sentence earlier but does not show the step ∫ ≤ min(u,α) − max(l,β) ≤ α − β. It is also what
makes the bound valid at the infinitely many zero-width places, without which the product-formula sum would not be
legitimate. Correct as stated.

**O5 — Prop 6.3 statement, p. 32. COSMETIC (cross-reference).** "For the center-star and point–template-star
experiments of Theorem 5.3" — the experiments are the list (i)–(iii) in §5.2 preceding Lemma 5.3 (which proves their
marginals). Likewise "Theorem 6.2/6.3/6.4/5.5/5.6/2.5/5.2" = Lemma 6.2/Prop 6.3/Lemma 6.4/Prop 5.5/Prop 5.6/Lemma
2.5/Lemma 5.2: every one points where intended.

**O6 — (6.7), p. 31. COSMETIC.** "Outside that interval the expression is at least 4δ² − λ > λ/2." True; the exact
infimum is 4δ²(1 − λ/2) − λ/2 (not attained), and "≥ 4δ² − λ" uses δ² ≤ 1/4 implicitly. No consequence.

**O7 — Prop 6.3, "Two candidates sharing a coordinate, and a third outside", p. 32. COSMETIC.** "If the intersection
is empty, all edges are bad." True, but only via the (6.3)-failure clause of the bad-edge definition and k > 81
(three crosses of mixture mass ≥ 1 − k^{-1/4} each cannot have empty intersection when 3k^{-1/4} < 1); the reason is
given earlier ("An empty intersection cannot have the asserted mixture mass for large k", p. 30) but not here.

**O8 — citation [14, Lemmas 3.4–3.5], p. 28. COULD NOT FETCH.** Not load-bearing: the paper reproduces the full
double-sampling argument for strict crosses, which I verified independently (§B, check (b)).

No FATAL. No GAP.

## §D. Status per result in scope

| item | status |
|---|---|
| §6 preamble, R_y, rows/columns | VERIFIED LINE BY LINE (O2 wording) |
| ν̃_q, (6.1), (6.2) | VERIFIED LINE BY LINE |
| Lemma 6.1 (both assertions), (6.3) | VERIFIED LINE BY LINE (O1) |
| remark W_c ≤ k^{1/16}S ⇒ o(S) | VERIFIED |
| Lemma 6.2 | VERIFIED LINE BY LINE (O2, O3); probability space §A |
| application paragraph (η = k^{-1/8}, 8k^{-1/16}S) | VERIFIED |
| (6.4), (6.5), three-state claims, classification, Figure 2 | VERIFIED LINE BY LINE + exhaustive check |
| bad-edge definition, (6.6), the no-renormalisation remark | VERIFIED LINE BY LINE |
| (6.7) | VERIFIED (analytic + exact grid) (O6) |
| Proposition 6.3 incl. (6.8)–(6.10), every branch, slice weighting, ±2EH* cancellation, sandwich | VERIFIED LINE BY LINE, conditional on Prop 5.5, Prop 5.6, Lemma 5.3, (5.7) (other seats) |
| (6.11), Lemma 6.4 | VERIFIED LINE BY LINE (O4), conditional on (4.7), Lemma 4.5, Lemma 4.1, §2 degree bounds |
| Proposition 6.5 incl. (6.12), (6.13), final f ≤ C(V_P+V_Q) | VERIFIED LINE BY LINE, conditional on Lemma 2.5, (5.4), Prop 5.5, Prop 5.6 |
| Prop 5.5, Prop 5.6, Lemma 5.3, Lemma 5.4, Cor 3.3, Lemma 4.5, Lemma 2.5 (imported) | SKIMMED (read as inputs only; not verified by this seat) |

## §E. Citation table

| cited | paper's claim | source | verdict |
|---|---|---|---|
| [14] Haussler–Welzl, DCG 2 (1987) 127–151, "Lemmas 3.4–3.5" | the ε-net double-sampling argument, specialised here to strict crosses | Springer serves a JavaScript "Client Challenge" page (3,036 B HTML) to curl and to the fetch layer (which mis-reported it as `ok`); Semantic Scholar lists it as bronze OA at the same URL | COULD NOT FETCH (not load-bearing: argument reproduced in full in the paper and verified here) |

## §F. Finite checks (scripts verbatim, outputs, failing controls)

All in /tmp/oaimath/167/checks/common/, run with `nice -n 19 python3 -u`.
(a) check_67.py — (6.7) on 200,010 exact rationals + boundary points; identity asserted pointwise. Controls that
FAIL: c ≡ 1 on the window (min 0 < λ/2), and λ = 4δ² (min 1.9992e-4 < λ/2 = 2e-4).
(b) check_lemma61.py — Lemma 6.1 ingredients: trace count ≤ (2k+1)² (control: unions of ≤ 3 rows exceed it);
hypergeometric ≤ 2^{-m} (control: ≤ 2^{-m-1} fails 747 times); Chebyshev step ≤ 1/2 for kα ≥ 8 (control kα = 0.3:
0.69 > 1/2); Monte Carlo of the first assertion (i.i.d.: 0/2000 vs bound 2.9e-7; CONTROL dependent samples
X_1 = … = X_k: 2000/2000); exact (6.3) toy (i.i.d. templates 2^{1−k}; CONTROL deterministic template: P = 1 > bound).
(c) check_lemma62.py — Lemma 6.2 exact toy: worst case over ALL (q,θ)-measurable selection rules computed from the
joint law; 600 random instances × 5 η: 0 violations (these random instances never produced an admissible-and-failing
support — weak); structured family aimed at the Markov step: 0.779η–0.811η (nonzero, order η, ≤ 8η); 300 random
draws of that family: max 0.811η. CONTROLS that FAIL: (1) hypothesis weakened to ν̃_q(U) ≥ 1/2: P = 1 vs 8η = 0.4;
(2) arbitrary supports allowed: P = 1; (3) "row" = any subset of a row: P = 1 (this is O2). On each control instance
the paper's exact hypotheses give P = 0.
(d) check_classification.py — exhaustive check of (6.4), (6.5), three-state claims, Figure 2 at both base types,
row ⇒ bit 1, singleton rule (0 errors); CONTROL: point states only in R_{y1} ∪ R_{y2} (no transfer) gives 48
violating pairs; τ-bounds of Prop 6.5 (4 bounds, 0 violations in 20,000 random ν) with a false bound (τ ≥ −4ζ in the
singleton case) as CONTROL: 19,901 violations.

### check_67.py (verbatim)
```python
# (6.7): c(rho)(rho^2+(1-rho)^2) - 2 rho(1-rho) >= lambda/2 for all rho in [0,1],
# delta = 1/100, lambda = delta^2/2, c = 1+lambda on |rho-1/2|<=delta else 1-lambda.
from fractions import Fraction as Fr
import sys

def make_c(delta, lam, inside=None, outside=None):
    inside = 1 + lam if inside is None else inside
    outside = 1 - lam if outside is None else outside
    return lambda r: inside if abs(r - Fr(1, 2)) <= delta else outside

def g(r, c):
    return c(r) * (r * r + (1 - r) ** 2) - 2 * r * (1 - r)

def check(delta, lam, c, N=200000, label=""):
    target = lam / 2
    worst = None
    pts = [Fr(i, N) for i in range(N + 1)]
    # exact boundary points and their neighbours
    for b in (Fr(1, 2) - delta, Fr(1, 2) + delta, Fr(1, 2)):
        for eps in (Fr(0), Fr(1, 10**12), -Fr(1, 10**12)):
            if 0 <= b + eps <= 1:
                pts.append(b + eps)
    for r in pts:
        v = g(r, c)
        # identity check
        ident = (2 * r - 1) ** 2 + (c(r) - 1) * (r * r + (1 - r) ** 2)
        assert v == ident, (r, v, ident)
        if worst is None or v < worst[1]:
            worst = (r, v)
    ok = worst[1] >= target
    print(f"{label}: min over {len(pts)} exact rationals = {float(worst[1]):.6e} at rho={float(worst[0]):.12f}; "
          f"lambda/2 = {float(target):.6e}; holds={ok}")
    return ok

delta = Fr(1, 100); lam = delta ** 2 / 2
ok1 = check(delta, lam, make_c(delta, lam), label="PAPER (delta=1/100, lam=delta^2/2)")
# analytic minima: inside, min of (2r-1)^2 + lam*(r^2+(1-r)^2) at r=1/2 -> lam/2 exactly
print("value at rho=1/2 (exact):", g(Fr(1, 2), make_c(delta, lam)), " = lam/2 =", lam / 2)
# just outside: (2delta)^2 - lam*(1/2 + 2 delta^2)
r = Fr(1, 2) + delta + Fr(1, 10**12)
print("just outside interval:", float(g(r, make_c(delta, lam))), " 4delta^2-lam =", float(4 * delta**2 - lam))
print("10 delta^2 < 1/4:", 10 * delta**2 < Fr(1, 4), "  margin lam/4 - 10delta^2 lam =", float(lam / 4 - 10 * delta**2 * lam))
print("Prop 5.5 constant 4d^2 lam/(2(1/4-d^2)) <= 10 d^2 lam:",
      4 * delta**2 * lam / (2 * (Fr(1, 4) - delta**2)) <= 10 * delta**2 * lam)

# CONTROLS that must FAIL:
# (i) reward 1 near balance (no +lambda bonus): value at 1/2 is 0 < lam/2
okc1 = check(delta, lam, make_c(delta, lam, inside=Fr(1)), label="CONTROL c=1 inside")
# (ii) penalty lambda too large outside: lam = 4 delta^2 kills the outside bound
lam2 = 4 * delta ** 2
okc2 = check(delta, lam2, make_c(delta, lam2), label="CONTROL lam=4delta^2")
print("controls rejected:", (not okc1) and (not okc2))
sys.exit(0 if (ok1 and not okc1 and not okc2) else 1)
```

### check_lemma61.py (verbatim)
```python
# Lemma 6.1 (strict-cross sampling): finite checks of each ingredient + a failing control.
import itertools, math, random, sys
random.seed(167)

def in_cross(x, y):
    (u, v), (a, b) = x, y
    return (u == a) != (v == b)          # exactly one coordinate agrees

# (1) trace count: crosses induce <= (2k+1)^2 distinct index subsets of 2k pooled samples
def n_patterns(samples, family):
    pats = set()
    for S in family(samples):
        pats.add(tuple(S(x) for x in samples))
    return len(pats)

def cross_family(samples):
    A = sorted({u for u, _ in samples}) + ['*']    # '*' = a label not among the samples
    B = sorted({v for _, v in samples}) + ['*']
    for a in A:
        for b in B:
            yield (lambda x, y=(a, b): in_cross(x, y))

def three_rows_family(samples):                   # CONTROL family: unions of <= 3 full rows
    A = sorted({u for u, _ in samples})
    for r in range(0, 4):
        for T in itertools.combinations(A, r):
            yield (lambda x, T=set(T): x[0] in T)

worst = 0; ctrl_fail = False
for trial in range(300):
    k = random.randint(1, 14)
    m = random.choice([1, 2, 3, 5, 2 * k, 4 * k])        # label alphabet size
    samples = [(random.randrange(m), random.randrange(m)) for _ in range(2 * k)]
    c = n_patterns(samples, cross_family)
    assert c <= (2 * k + 1) ** 2, (k, c)
    worst = max(worst, c / (2 * k + 1) ** 2)
# extreme: all 2k first labels distinct and all 2k second labels distinct
for k in range(1, 15):
    s = [(i, i + 1000) for i in range(2 * k)]
    c = n_patterns(s, cross_family)
    assert c <= (2 * k + 1) ** 2
    cc = n_patterns(s, three_rows_family)
    if cc > (2 * k + 1) ** 2:
        ctrl_fail = True
    if k in (2, 8, 14):
        print(f"k={k}: distinct cross traces={c} (bound {(2*k+1)**2}); CONTROL <=3-row unions traces={cc}")
print("max ratio traces/(2k+1)^2 over random trials:", round(worst, 3))
print("CONTROL family exceeds (2k+1)^2 for some k:", ctrl_fail)

# (2) hypergeometric: P(all m misses in 2nd half) = C(2k-m,k)/C(2k,k) <= 2^-m
bad = 0
for k in range(1, 81):
    for m in range(0, 2 * k + 1):
        p = math.comb(2 * k - m, k) / math.comb(2 * k, k) if m <= k else 0.0
        prod = 1.0
        for i in range(m):
            prod *= (k - i) / (2 * k - i) if m <= k else 0
        if m <= k:
            assert abs(p - prod) < 1e-12 * max(1, p)
        assert p <= 2.0 ** (-m) + 1e-15, (k, m, p)
        if m >= 1 and m <= k and p > 2.0 ** (-m - 1):
            bad += 1                     # CONTROL: the sharper claim 2^{-m-1} fails
print("hypergeometric <= 2^-m: all k<=80 OK; CONTROL '<= 2^-(m+1)' violated in", bad, "cases")

# (3) Chebyshev step: for k*alpha >= 8 and beta > alpha, P(Bin(k,beta) < k alpha/2) <= 1/2
def binom_cdf_below(k, beta, thr):   # P(N < thr)
    return sum(math.comb(k, j) * beta ** j * (1 - beta) ** (k - j) for j in range(k + 1) if j < thr)
worst_ch = 0
for k in range(8, 161):
    for i in range(1, 41):
        alpha = max(8 / k, i / 41)
        if alpha >= 1: continue
        beta = min(alpha + 1e-9, 1 - 1e-12)
        worst_ch = max(worst_ch, binom_cdf_below(k, beta, k * alpha / 2))
print("max P(Bin(k,beta)<k alpha/2) over k alpha>=8 grid:", f"{worst_ch:.3e}", "(claim <= 1/2)")
ctrl = binom_cdf_below(1, 0.31, 1 * 0.3 / 2)
print("CONTROL k alpha=0.3 (hypothesis violated): P =", ctrl, "> 1/2:", ctrl > 0.5)

# (4) Monte Carlo of the first assertion; independence is load-bearing.
# nu uniform on an n x n grid; every cross has nu-mass 2(n-1)/n^2 < 1-alpha.
n, k, alpha = 10, 200, 0.4
bound = 2 * (2 * k + 1) ** 2 * 2.0 ** (-k * alpha / 2)
states = [(i, j) for i in range(n) for j in range(n)]
ys = [(a, b) for a in range(n) for b in range(n)]   # labels outside the grid give rows/cols: also small
def event(X):
    for y in ys:
        if all(in_cross(x, y) for x in X):
            return True
    # y with an unseen label: cross = a full column (or row); X all in one column?
    if len({x[1] for x in X}) == 1 or len({x[0] for x in X}) == 1:
        return True
    return False
T = 2000
iid_hits = sum(event([random.choice(states) for _ in range(k)]) for _ in range(T))
dep_hits = 0
for _ in range(T):
    x = random.choice(states); dep_hits += event([x] * k)       # CONTROL: X_1=...=X_k
print(f"MC n={n},k={k},alpha={alpha}: bound={bound:.3e}; iid frequency={iid_hits}/{T}; "
      f"CONTROL dependent samples frequency={dep_hits}/{T}")

# (5) second assertion (6.3), exact toy: two histories h1,h2 with nu_h1=delta_x1, nu_h2=delta_x2,
# x1=(0,0), x2=(1,1); q's neighbours have each history with prob 1/2.  nu~_q=(delta_x1+delta_x2)/2.
def fail_prob(k, template_law):
    tot = 0.0
    alpha = k ** -0.25
    for (c1, prob) in template_law(k):           # c1 = number of h1's in template
        present = set()
        if c1 > 0: present.add('h1')
        if c1 < k: present.add('h2')
        nu = {'h1': (0, 0), 'h2': (1, 1)}
        labs = [0, 1, '*']
        bad = False
        for y in itertools.product(labs, labs):
            if all(in_cross(nu[h], y) for h in present):          # y in Y_theta (exact atoms)
                mass = 0.5 * in_cross((0, 0), y) + 0.5 * in_cross((1, 1), y)
                if mass < 1 - alpha: bad = True
        tot += prob * bad
    return tot
iid = lambda k: [(c, math.comb(k, c) * 0.5 ** k) for c in range(k + 1)]
det = lambda k: [(k, 1.0)]                       # CONTROL: template = k copies of one history
for k in (300, 1000):
    b = 4 * (2 * k + 1) ** 2 * 2.0 ** (-(k ** 0.75) / 2)
    print(f"(6.3) toy k={k}: bound={b:.3e}; iid templates P={fail_prob(k, iid):.3e} (=2^(1-k));"
          f" CONTROL deterministic template P={fail_prob(k, det)}")
```

### check_lemma62.py (verbatim)
```python
# Lemma 6.2 toy: exact P(G, X(p) notin U(q,theta)) under the joint law P_E(p,q) P(theta|q),
# maximised over ALL (q,theta)-measurable selection rules U (and events G), vs 8*eta.
# Floats with a 1e-12 tolerance that favours the ADVERSARY (admissibility is loosened).
import itertools, random
random.seed(62)
TOL = 1e-12

def analyse(X, Hh, E, nA, nB, k, eta, mode="paper", c_relax=None):
    nE = len(E)
    P = sorted({p for p, _ in E}); Q = sorted({q for _, q in E})
    nbr = {q: [] for q in Q}
    for p, q in E: nbr[q].append(p)
    dP = {}
    for p, _ in E: dP[p] = dP.get(p, 0) + 1
    mu = {p: dP[p] / nE for p in P}
    kap = {q: len(nbr[q]) / nE for q in Q}
    muH = {}
    for p in P: muH[Hh[p]] = muH.get(Hh[p], 0) + mu[p]
    nu = {h: {} for h in muH}
    for p in P:
        nu[Hh[p]][X[p]] = nu[Hh[p]].get(X[p], 0) + mu[p] / muH[Hh[p]]
    thr = 1 - 3 * eta ** 2 if c_relax is None else 1 - c_relax
    total = 0.0
    for q in Q:
        dq = len(nbr[q])
        nut = {}
        for p in nbr[q]:
            for x, w in nu[Hh[p]].items():
                nut[x] = nut.get(x, 0) + w / dq
        supp = sorted(nut)
        # candidate supports. Adding zero-nu~ states to a <=2-set only helps containment, so the
        # adversary's admissible <=2-sets may be taken inside supp(nu~_q).
        cands = [('row', a) for a in range(nA)] + [('col', b) for b in range(nB)]
        # any member x of an admissible <=2-set has nu~(x) >= thr - max nu~ (its partner is at most
        # the top atom), so only those atoms can occur; this prunes nothing admissible.
        top = max(nut.values())
        supp2 = [x for x in supp if nut[x] >= thr - top - TOL]
        cands += [('set', frozenset(S)) for r in range(3) for S in itertools.combinations(supp2, r)]
        excl = frozenset(X[p] for p in nbr[q])
        if mode == 'any':      # CONTROL: arbitrary subsets allowed
            cands.append(('set', frozenset(supp) - excl))
        if mode == 'rowsub':   # CONTROL: 'row' = any subset of a row
            for a in range(nA):
                cands.append(('set', frozenset(x for x in supp if x[0] == a) - excl))
        def member(x, U):
            t, v = U
            return x[0] == v if t == 'row' else (x[1] == v if t == 'col' else x in v)
        adm = [U for U in cands if sum(w for x, w in nut.items() if member(x, U)) >= thr - TOL]
        if not adm: continue
        hq = {}
        for p in nbr[q]: hq[Hh[p]] = hq.get(Hh[p], 0) + 1 / dq
        for theta in itertools.product(sorted(hq), repeat=k):
            pth = 1.0
            for h in theta: pth *= hq[h]
            # P(X(p) notin U | q, theta) computed from the joint law: the template is drawn from
            # k further iid neighbours, so given (q,theta) p is still uniform on nbr[q]
            best = max(sum(1 for p in nbr[q] if not member(X[p], U)) / dq for U in adm)
            total += kap[q] * pth * best
    return total

def build(nA, nB, nH, nP, nQ, skew):
    X = [(0, 0) if random.random() < skew else (random.randrange(nA), random.randrange(nB)) for _ in range(nP)]
    Hh = [random.randrange(nH) for _ in range(nP)]
    odd = [p for p in range(nP) if X[p] != (0, 0)]
    E = set()
    for q in range(nQ):
        pool = odd if (odd and random.random() < 0.5) else list(range(nP))
        for p in random.sample(pool, min(random.randint(1, 4), len(pool))):
            E.add((p, q))
    return X, Hh, sorted(E)

worst = (0, None); viol = 0
for trial in range(600):
    nH = random.randint(1, 3)
    X, Hh, E = build(3, 3, nH, random.randint(6, 18), random.randint(3, 9), random.choice([0.6, 0.8, 0.9, 0.97]))
    for eta in (0.01, 0.025, 0.05, 1 / 12, 1 / 9):
        v = analyse(X, Hh, E, 3, 3, 2, eta)
        if v > 8 * eta + 1e-12: viol += 1
        if v / eta > worst[0]: worst = (v / eta, (trial, eta, v))
print("PAPER hypothesis, 600 random instances x 5 etas: violations of <= 8 eta:", viol,
      "; max P/eta =", round(worst[0], 3), worst[1])

# Hand-made instance aimed at the Markov step: one history whose nu_h has mass 3eta^2 off the
# heavy state, all of it on the neighbours of a single centre.
for eta in (0.05, 0.1):
    N = 400; n_odd = int(N * 3 * eta ** 2)
    X = [(1, 1)] * n_odd + [(0, 0)] * (N - n_odd); Hh = [0] * N
    E = sorted([(p, 0) for p in range(n_odd)] + [(p, 1 + p) for p in range(n_odd, N)])
    v = analyse(X, Hh, E, 2, 2, 2, eta)
    print(f"hand-made eta={eta}: P(G,X notin U)={v:.4f} (= mu-mass of odd states {n_odd/N:.4f}); 8eta={8*eta:.2f}")

# Structured family aimed at the Markov step of the proof: "q-type" centres see a 3*eta fraction of
# neighbours whose history h1 has nu_h1(U^c) = eta, and ALL those neighbours are outside U={x0}.
def structured(eta, per=20, nq=5, frac_odd=None):
    n_odd = round(per * 3 * eta) if frac_odd is None else frac_odd
    X, Hh, E = [], [], []
    pid = 0
    for q in range(nq):
        for j in range(per):
            if j < n_odd: X.append((1, 1)); Hh.append(1)     # h1-points outside U, at q
            else:         X.append((0, 0)); Hh.append(0)     # h0-points in x0
            E.append((pid, q)); pid += 1
    # h1-points in x0, elsewhere, so that nu_h1(x1) = eta exactly
    n_in = round(nq * n_odd * (1 - eta) / eta)
    for j in range(n_in):
        X.append((0, 0)); Hh.append(1); E.append((pid, nq + j // 19)); pid += 1
    return X, Hh, sorted(E)
best = 0
for eta in (0.05, 0.1):
    for per in (20, 40, 100):
        X, Hh, E = structured(eta, per=per)
        v = analyse(X, Hh, E, 2, 2, 2, eta)
        best = max(best, v / eta)
        print(f"structured eta={eta} per={per}: P(G,X notin U)={v:.4f} = {v/eta:.3f} eta  (lemma: <= 8 eta)")
# random search over the structured family's free parameters (odd count, degrees)
for trial in range(300):
    eta = random.choice([0.02, 0.05, 0.08, 0.1])
    per = random.randint(10, 60)
    odd = random.randint(1, max(1, int(per * 0.5)))
    X, Hh, E = structured(eta, per=per, nq=random.randint(1, 6), frac_odd=odd)
    v = analyse(X, Hh, E, 2, 2, 2, eta)
    assert v <= 8 * eta + 1e-12, (eta, per, odd, v)
    best = max(best, v / eta)
print("max P/eta over structured family + 300 random parameter draws:", round(best, 3), "(lemma: 8)")

eta = 0.05
# CONTROL 1: hypothesis weakened to nu~_q(U) >= 1/2 -> conclusion fails
X = [(0, 0)] * 10 + [(1, 1)] * 10; Hh = [0] * 20
E = sorted([(p, 0) for p in range(10)] + [(p, 1) for p in range(10, 20)])
v1 = analyse(X, Hh, E, 2, 2, 2, eta, c_relax=0.5); v1p = analyse(X, Hh, E, 2, 2, 2, eta)
print(f"CONTROL 1 (mass >= 1/2 only): P={v1} vs 8eta={8*eta} -> conclusion FAILS: {v1 > 8*eta}; "
      f"paper hypothesis on same instance: P={v1p}")
# CONTROL 2: arbitrary supports (type restriction dropped), mass hypothesis kept
X = [(i // 20, i % 20) for i in range(400)]; Hh = [0] * 400
E = sorted((p, p // 2) for p in range(400))
v2 = analyse(X, Hh, E, 20, 20, 1, eta, mode='any'); v2p = analyse(X, Hh, E, 20, 20, 1, eta)
print(f"CONTROL 2 (arbitrary U): P={v2} vs 8eta={8*eta} -> FAILS: {v2 > 8*eta}; restricted types: P={v2p}")
# CONTROL 3: 'row' = any subset of a row
X = [(0, j) for j in range(400)]; Hh = [0] * 400
E = sorted((p, p // 2) for p in range(400))
v3 = analyse(X, Hh, E, 1, 400, 1, eta, mode='rowsub'); v3p = analyse(X, Hh, E, 1, 400, 1, eta)
print(f"CONTROL 3 (row-subsets): P={v3} -> FAILS: {v3 > 8*eta}; full rows: P={v3p}")
```

### check_classification.py (verbatim)
```python
# Exhaustive check of the strict-cross geometry used in Prop 6.3 / 6.5 ((6.4), (6.5), Figure 2,
# the branch claims), over a 5x5 label grid plus one unseen label per coordinate.
import itertools
L = list(range(5)) + ['u']                      # 'u' = a label carried by no point
POINT = [(a, b) for a in range(5) for b in range(5)]
CENTER = [(a, b) for a in L for b in L]
def R(y): return {x for x in POINT if (x[0] == y[0]) != (x[1] == y[1])}
def bit(x, y):                                  # consistent bit, or None if inconsistent
    if x[0] == y[0] and x[1] != y[1]: return 1
    if x[1] == y[1] and x[0] != y[0]: return 0
    return None
def N(o1, o2, b):                               # nonshared-coordinate match of opposite endpoints
    return o1[1] == o2[1] if b == 1 else o1[0] == o2[0]

errs = []
# (6.4): two states in one row
for (a, b, b2) in itertools.product(L, L, L):
    if b == b2: continue
    I = R((a, b)) & R((a, b2))
    if I != {x for x in POINT if x[0] == a and x[1] not in (b, b2)}: errs.append(('6.4', a, b, b2))
    for y3 in CENTER:                            # third state outside the row
        if y3[0] != a and len(I & R(y3)) > 1: errs.append(('third', a, b, b2, y3))
# (6.5) and three pairwise-distinct states
for y1, y2 in itertools.product(CENTER, CENTER):
    if y1[0] == y2[0] or y1[1] == y2[1]: continue
    I = R(y1) & R(y2)
    exp = {x for x in [(y1[0], y2[1]), (y2[0], y1[1])] if x in POINT}
    if I != exp: errs.append(('6.5', y1, y2))
    for y3 in CENTER:
        if len({y1[0], y2[0], y3[0]}) == 3 and len({y1[1], y2[1], y3[1]}) == 3 and I & R(y3):
            errs.append(('three', y1, y2, y3))
    # Figure 2: with point states in I and centre states in {y1,y2}, equal bits force N at either base
    for base in (y1, y2):                        # centre base
        for x1, x2 in itertools.product(I, I):
            b1, b2 = bit(x1, base), bit(x2, base)
            if b1 is not None and b1 == b2 and not N(x1, x2, b1): errs.append(('fig2-centre', y1, y2))
    for base in I:                               # point base
        for c1, c2 in itertools.product((y1, y2), (y1, y2)):
            b1, b2 = bit(base, c1), bit(base, c2)
            if b1 is not None and b1 == b2 and not N(c1, c2, b1): errs.append(('fig2-point', y1, y2))
# row case: point in row a, centre in row a  =>  any consistent edge has bit 1
for a in L:
    for x in POINT:
        for y in CENTER:
            if x[0] == a and y[0] == a and bit(x, y) not in (None, 1): errs.append(('row-bit', x, y))
# singleton case at a point base: same centre state => equal bits and N
for x in POINT:
    for y in CENTER:
        b = bit(x, y)
        if b is not None and not N(y, y, b): errs.append(('singleton', x, y))
print("errors in paper's claims:", len(errs), errs[:3])

# CONTROL: if the point states were only known to lie in R(y1) UNION R(y2) (no intersection /
# no transfer), equal bits at a centre base would NOT force the nonshared-coordinate match.
ctrl = 0
y1, y2 = (0, 0), (1, 1)
U = R(y1) | R(y2)
for base in (y1, y2):
    for x1, x2 in itertools.product(U, U):
        b1, b2 = bit(x1, base), bit(x2, base)
        if b1 is not None and b1 == b2 and not N(x1, x2, b1): ctrl += 1
print("CONTROL (union instead of intersection): violating pairs =", ctrl, "(must be > 0)")

# tau bounds in Prop 6.5 (random measures meeting each case's hypothesis); control = a false bound
import random
random.seed(65)
def tau(nu):
    A, B = {}, {}
    for (a, b), w in nu.items(): A[a] = A.get(a, 0) + w; B[b] = B.get(b, 0) + w
    return sum(v * v for v in A.values()) + sum(v * v for v in B.values()) - 1
def mass(nu, S): return sum(w for x, w in nu.items() if x in S)
def rand_nu(conc_on, z):
    nu = {x: random.random() * z / 25 for x in POINT}
    s = sum(nu.values()); nu = {x: w * z / s for x, w in nu.items()}  # z spread everywhere
    # remaining 1-z spread over conc_on at random proportions
    ws = [random.random() for _ in conc_on]; t = sum(ws)
    for x, w in zip(conc_on, ws): nu[x] = nu.get(x, 0) + (1 - z) * w / t
    return nu
bad = {'single': 0, 'row': 0, 'third': 0, 'corner': 0, 'CTRL single>=-4z': 0}
for _ in range(20000):
    z = random.choice([1e-4, 1e-3, 1e-2, 0.05])
    y = (0, 0)
    nu = rand_nu(sorted(R(y)), z)                  # nu(R_y) >= 1 - z
    if tau(nu) < -0.5 - z - 1e-12: bad['single'] += 1
    if tau(nu) < -4 * z: bad['CTRL single>=-4z'] += 1
    I = R((0, 0)) & R((0, 1)); nu = rand_nu(sorted(I), 2 * z)
    if tau(nu) < -4 * z - 1e-12: bad['row'] += 1
    I3 = I & R((2, 3)); nu = rand_nu(sorted(I3), 3 * z)
    if tau(nu) < 1 - 12 * z - 1e-12: bad['third'] += 1
    Ic = R((0, 0)) & R((1, 1)); nu = rand_nu(sorted(Ic), 2 * z)
    if tau(nu) < -4 * z - 1e-12: bad['corner'] += 1
print("tau-bound violations (paper's four bounds must be 0; CONTROL must be > 0):", bad)
```

### outputs

#### out_67.txt
```
PAPER (delta=1/100, lam=delta^2/2): min over 200010 exact rationals = 2.500000e-05 at rho=0.500000000000; lambda/2 = 2.500000e-05; holds=True
value at rho=1/2 (exact): 1/40000  = lam/2 = 1/40000
just outside interval: 0.000374990000079998  4delta^2-lam = 0.00035
10 delta^2 < 1/4: True   margin lam/4 - 10delta^2 lam = 1.245e-05
Prop 5.5 constant 4d^2 lam/(2(1/4-d^2)) <= 10 d^2 lam: True
CONTROL c=1 inside: min over 200010 exact rationals = 0.000000e+00 at rho=0.500000000000; lambda/2 = 2.500000e-05; holds=False
CONTROL lam=4delta^2: min over 200010 exact rationals = 1.999200e-04 at rho=0.489999999999; lambda/2 = 2.000000e-04; holds=False
controls rejected: True
exit=0
```

#### out_lemma61.txt
```
k=2: distinct cross traces=11 (bound 25); CONTROL <=3-row unions traces=15
k=8: distinct cross traces=137 (bound 289); CONTROL <=3-row unions traces=697
k=14: distinct cross traces=407 (bound 841); CONTROL <=3-row unions traces=3683
max ratio traces/(2k+1)^2 over random trials: 0.595
CONTROL family exceeds (2k+1)^2 for some k: True
hypergeometric <= 2^-m: all k<=80 OK; CONTROL '<= 2^-(m+1)' violated in 747 cases
max P(Bin(k,beta)<k alpha/2) over k alpha>=8 grid: 8.849e-02 (claim <= 1/2)
CONTROL k alpha=0.3 (hypothesis violated): P = 0.69 > 1/2: True
MC n=10,k=200,alpha=0.4: bound=2.925e-07; iid frequency=0/2000; CONTROL dependent samples frequency=2000/2000
(6.3) toy k=300: bound=2.042e-05; iid templates P=9.818e-91 (=2^(1-k)); CONTROL deterministic template P=1.0
(6.3) toy k=1000: bound=2.747e-20; iid templates P=1.867e-301 (=2^(1-k)); CONTROL deterministic template P=1.0
exit=0
```

#### out_lemma62.txt
```
PAPER hypothesis, 600 random instances x 5 etas: violations of <= 8 eta: 0 ; max P/eta = 0 None
hand-made eta=0.05: P(G,X notin U)=0.0075 (= mu-mass of odd states 0.0075); 8eta=0.40
hand-made eta=0.1: P(G,X notin U)=0.0300 (= mu-mass of odd states 0.0300); 8eta=0.80
structured eta=0.05 per=20: P(G,X notin U)=0.0390 = 0.779 eta  (lemma: <= 8 eta)
structured eta=0.05 per=40: P(G,X notin U)=0.0390 = 0.779 eta  (lemma: <= 8 eta)
structured eta=0.05 per=100: P(G,X notin U)=0.0390 = 0.779 eta  (lemma: <= 8 eta)
structured eta=0.1 per=20: P(G,X notin U)=0.0811 = 0.811 eta  (lemma: <= 8 eta)
structured eta=0.1 per=40: P(G,X notin U)=0.0811 = 0.811 eta  (lemma: <= 8 eta)
structured eta=0.1 per=100: P(G,X notin U)=0.0811 = 0.811 eta  (lemma: <= 8 eta)
max P/eta over structured family + 300 random parameter draws: 0.811 (lemma: 8)
CONTROL 1 (mass >= 1/2 only): P=0.9999999999999998 vs 8eta=0.4 -> conclusion FAILS: True; paper hypothesis on same instance: P=0.0
CONTROL 2 (arbitrary U): P=1.0000000000000007 vs 8eta=0.4 -> FAILS: True; restricted types: P=0.0
CONTROL 3 (row-subsets): P=1.0000000000000007 -> FAILS: True; full rows: P=0.0
exit=0
```

#### out_class.txt
```
errors in paper's claims: 0 []
CONTROL (union instead of intersection): violating pairs = 48 (must be > 0)
tau-bound violations (paper's four bounds must be 0; CONTROL must be > 0): {'single': 0, 'row': 0, 'third': 0, 'corner': 0, 'CTRL single>=-4z': 19901}
exit=0
```

## §G. Summary

§6 holds as read. Lemma 6.1 is the Haussler–Welzl ε-net argument with the correct (2k+1)² trace count for strict
crosses and the correct hypergeometric 2^{-m}; its second assertion correctly uses that the synthetic states are
i.i.d. ν̃_q before the template is revealed and ν_{h_j}-distributed after. Lemma 6.2 is sound with U selected after θ:
the only use of (q,θ) is E[ν_{H(p)}(U^c)|q,θ] = ν̃_q(U^c) (p ⟂ θ | q by (5.9)), and the exceptional sets depend on
h alone and capture every admissible support of each type at once. The classification is exhaustive and each branch
of (6.10)/(6.13) is right; (6.7) holds for all ρ; the ±2EH* terms cancel with the right signs; Lemma 6.4's per-place
bound follows from (4.7) + match implications + product formula; Prop 6.5's final step uses Lemma 2.5 in the right
direction. Only wording objections (O1–O8), the sharpest being that "row" must mean a FULL row (literal reading makes
Lemma 6.2 false; proof and applications use full rows). Everything is conditional on §5's Prop 5.5/5.6, Lemma 5.3,
(5.7), Lemma 4.5 and Lemma 2.5, which this seat did not verify.
