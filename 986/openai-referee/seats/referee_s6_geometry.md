# Referee report — Paper B (s ≥ 6), Sections 1–3 (foundations, geometry, learning) + figures/validation.tex

Seat: PAPER B geometry/learning. Referee: Claude (Opus 5.5), 2026-10-20. Status: COMPLETE.

VERDICT: HOLDS WITH FIXES (expository only: objections 1, 2, 4, 5, 6, 7; cosmetic 3, 8, 9, 10). No FATAL, no GAP in §§1–3. Cross-seat pointer 11 for §§5–6.

## Working notes / objections (appended as found)

### §1 foundations (01-foundations.tex) — first pass
- base:incidence: identity MM^T = q^{j-1}I + Q_{j-2}J checked; the weighted variance identity checked algebraically
  (Q_{j-2}Q_j − Q_{j-1}^2 = −q^{j-1}); mixing bound via Cauchy–Schwarz holds with constant 1; last assertion holds with C = 4.
- base:flag-graph: K_{d+1}-freeness argument checked (a_{r+1} ∉ ker b_r ⊇ span(a_1..a_r); all a_i ∈ ker b_m, dim d). Reversal symmetry checked.
- base:rectangles: |R(U)| = Q_{r-1}Q_{d-r} ≤ 4q^{d-1}, mean ≤ 4σ, union over ≤ (d+2)q^{(d+1)^2} subspaces with tail q^{-A log(A/4e)}: holds.
- base:selection-entropy: union-bound atom estimate checked; log(eN/ℓ) = (d−1)σ − η log σ + O(1) correct for ℓ = Θ(qσ^{1+η}). Holds.
- base:event-transfer: Donsker–Varadhan with f = −1_E; holds.
- base:tails, base:scale-comparisons: checked, hold.

### §2 geometry (02-geometry.tex) — first pass notes
- geom:validation: ideal-row size bound (≤ 4q^{j+1}/|X| low-p_X points), Markov capture bound 5qe(X,T)/(|X||T|) ≤ 5τ/c,
  rejection-sampling acceptance ≥ .9e^{−C_1hP}, index cost O(hP)=O(qP(d_T+1)) — all check. Second test: |U_T'|/|X_T| ≤ Ce^b ≤ e^{CP}
  uses b ≤ C_bK_* = o(P) — checks. Holds.
- geom:produced-test: first-accepted-row law = ν(·|A) ≤ (1/.9)·unif(X_0^h); exclusion bound follows. Holds.
- geom:projection (PRIORITY 1): checked line by line.
  * center properties: variance identity ⇒ P(| |T∩z^⊥| − p_j|T| | > |T|/3q) ≤ 9q^{j+1}/(Q_j|T|) = O(q/|T|) = o(1) since
    |T| ≥ q^{(j+1)/2}e^{−b/2} with b = o(σ). E coll_z(S)/n ≤ n(q+1)/(2Q_j) ≤ Cq^{(3−j)/2} using n² ≤ Cq^{j+1}. E e(S_0,T_0) ≤ p_j e(S,T).
    Markov ×3 + two 1−o(1) events ⇒ positive probability ⇒ a center exists; it is a function of (S,T,A,U_S,U_T) fixed before the call's
    fresh tables. OK.
  * hypotheses transfer: b' = b+O(1) (|S_0||T_0| ≥ c n|T|/q), τ' = Cτ, d_{S_0} ≤ d_S+o(1), d_{T_0} ≤ d_T+O(1). Each call re-uses the
    ORIGINAL S,T (not A∩S), so b,τ do NOT compound across the 8 calls; across the (j−3) induction levels the constants change O(d) times
    — bounded since d is fixed. OK.
  * reorientation: if |T_0| < |S_0| the (j−1)-lemma captures the T_0 side; validation then returns caps on BOTH sides, so the S_0 cap
    (≤ Cq^j/|T_0| ≤ Cq^{j+1}/|T| ≤ ne^b ≤ m_0) exists regardless. OK.
  * lift loss per call ≤ .01|S_0| + (n−|S_0|) + 1 < .02n, losses add over 8 calls (≤ .16n). OK.
  * contraction: |A_new| ≤ m_0 + Σ(k_i−1) ≤ m_0 + sqrt(m_0·2coll_z(A)) ≤ m_0 + ρ|A| with ρ ≤ C sqrt(m_0/q^{j−1}) ≤ q^{(3−j)/4+o(1)}
    ≤ q^{−1/4+o(1)} for j ≥ 4 (P = o(σ) ⇒ e^{O(P)} = q^{o(1)}). qρ^5 → 0 already; 8 calls are generous. |A_8| = O(m_0). OK.
  * VERDICT on priority 1: the repeated-projection reduction HOLDS as written (losses are O(1) per level in b, O(1) in d_S,d_T, constant
    factor in cost; number of levels j−3 ≤ d−3 fixed). The lifted cap has the claimed size O(ne^{C_3P}) and capture ≥ .84n.
- geom:preparation: enumeration branch cost n(d_S+1) ≤ 100qP(d_S+1) in budget; K_p, J ≤ n/K_p = q^{1/2}e^{−2g/15} algebra checks;
  greedy cells nonincreasing; large-cell reduction to PG(2,q): lifts per line exactly q, dyadic class ⇒ |T_1| ≥ c|T|/(hσ), product
  q^3e^{−b−O(log σ)}, domain gap +log σ = o(K_*). Cap ≤ Cq^4σ/|T| ≤ Cnσe^b. OK.
- geom:rich-lines (PRIORITY 2): checked. Sampling rate A·sqrt(n/M^3); interpolation degree ≤ CA^{1/3}sqrt(n/M) < (A/2)sqrt(n/M);
  D_0 ≤ Cq^{41/80} < q. Plane factors: Cauchy–Schwarz with plane cap K_p (valid for K-planes — F_q-points of a K-plane span ≤ 3 dims) gives
  u = o(M'), disjoint unions ⇒ O(n/M + D_0²). Flatness polynomials Q_ij: degree ≤ 3D_0−4; vanish at points on ≥3 lines of Z(F_0)
  (uses char odd for the bilinear form). Non-flatness claim: verified — F_z ≠ 0 needs deg F < q; formal branch h with h_ab = 0
  forces h−h_1 ∈ (x1,x2)^q (monomials of degree < q need u,v ∈ {0,1}, uv ≡ 0), then F_0(x,h_1) of degree < q vanishes to order q ⇒ ≡ 0
  ⇒ plane factor, contradiction. This is exactly the Ellenberg–Hablicsek obstruction being avoided by degree < q. Common-line bound
  2D_1D_2 via slicing + resultant: checked incl. degenerate cases (vanishing leading coefficients still give Res(u_0)=0). HOLDS.
  Degree bookkeeping: all degrees ≤ 3D_0 ≤ Cq^{41/80} < q for q ≥ q_0 — the characteristic hypothesis is genuinely satisfied.
- geom:radial: all exponent arithmetic checked (M/n^{1/3} ≥ e^{(2/3−1/20)g}/2, M²/K_p ≥ e^{23g/30}/4, n/M ≤ 2qe^{g/20} ≤ Cq^{41/40},
  J/M ≤ 2e^{−(1+2/15−1/20)g}); list case "center in an earlier plane, ≤ i−1 centers" argument correct; plane-incidence variance count
  16q|C_i|/M²; Σ i f_i ≤ J ≤ q^v; exceptional set ≤ Cne^{−χ}Σa^{98} = o(n). HOLDS.
- geom:overlap: E_a ≤ (q+1)²·#rich radial lines; Δ_a ≤ 2q/a; strong degree case split at (v−1)σ < −4P checked. HOLDS.

### §3 learning (03-learning.tex) — first pass notes
- Poissonization (independent Poisson(qL/n') point–batch counts) correct; total mean RqL = qP.
- learn:elementary-sizes: q/n' < 1/(50P) from n > 100qP; Q_{j−1} = O(B²) and B ≥ cq^{(j−1)/2} ≥ e^{P}: check for j = 2,3.
- learn:regular-pencils: variance sums Σ(λ_H−1)² ≤ CqB, Σ(λ_{H,C}−f_C)² ≤ CqBf_C (incl. the 1/Q_j mean shift); |𝓔| ≤ CqB; pencil-sum
  second-moment exclusion Cn'f_Ce^{−2ξ}, summed over cells (not multiplied by J ≤ q^{1/2}) — correct; typical bounds .75 ≤ λ' < 2,
  |δ'| ≤ .18 check. Holds.
- learn:empty-exceptional: m ≥ |T|/2 ≥ cqBe^{−b} hyperplanes with λ ≤ 8τ; P(empty) = e^{−Pλ_H}; reverse-Markov P(Y ≥ ma/2) ≥ a/2 valid
  without independence; the λ ≥ 10^{−4} contribution Markov bound Ce^{b+8Pτ−10^{−4}P} = o(e^{−8Pτ}) since b,Pτ = o(P). z_x variance/
  double-counting statements check. Holds. NOTE the good event has probability only ce^{−8Pτ}, and Pτ can be as large as
  ~σ^{1−η/2−91β} (not O(1)); this is harmless only because the proposal search budget is e^{O(qP(d_S+1))} ≫ e^{8Pτ} — it is accounted
  for in learn:implementation (Pτ = o(qP)). OK.
- learn:one-mean / one-covariance / one-bounds: Poisson union-emptiness identity and the three bounds re-derived. Hold.
- learn:second-moment: re-derived: (L²e^{−.75L})^R·2^{R−1}[(CBe^ξ)² + B²e^{2χ}2^R O(σ)] + Q_{j−1}(2e^{−.75L})^R ≤ B²e^{−.6P}. Holds.
- learn:high-moment: component decomposition (strong graph θ > t_*), external-line mass ≤ pt_* = .01 (in PG(3,q) two planes meet in ONE
  line, so ≤ p−1 external lines per plane), conditional independence of internal schedules across components given external
  schedules, nonsimple attenuation (2e^{−.74L})^R ≤ e^{−.7P}, simple-singleton signed bound e^{−.68P}(|δ'|^{R/2}+(pθ_max)^{200}+1_{B_H}),
  certificate/ledger union bound with distinct direction–batch events, anchor cost O(q^{v−1}), pair cost e^{2χ}(2P)^{200},
  residual root/nonroot saving q^{hv−2h+2r} ≤ q^{−.8h+O(h/σ)}: each step checked; I could not break it. Overheads p^{O(p)} =
  exp(O((σ/P)log σ)) = exp(o(pP)) since log σ = o(P). (See objection list for exposition issues.)
- learn:row-success / learn:implementation: thresholds z_min/(10q); high-moment tail e^{−.09pP} ≤ q^{−900}; Markov counts; proposal/true
  likelihood ratio (n'/|U_S|)^m with Poisson size factors cancelling; acceptance ≥ ce^{−8Pτ}e^{−2qP(d_S+log 2)}; index cost O(qP(d_S+1)).
  Hold.

### Finite checks run (capped python; scripts in /tmp/oaimath/170/seats/s6geom_scripts/)
- pg_checks.py: MM^T = q^{j−1}I + Q_{j−2}J and the weighted variance identity (base:weighted-variance) verified exactly/numerically for
  (q,j) ∈ {(3,2),(5,2),(7,2),(3,3),(5,3),(3,4)}; mixing bound (base:mixing) on random sets: no violation. Flag graph (base:edge-rule):
  random streams for (q,d) = (3,2),(2,3),(3,3): max clique = d exactly (bound attained ⇒ the check can see cliques), never d+1.
  Rectangle sizes |R(U)| = Q_{r−1}Q_{d−r} ≤ 4q^{d−1}: verified (q,d) = (5,3),(3,4).
- flat_checks.py (rich-lines non-flatness claim, q = 7): flatness polynomials Q_ij of geom:flatness-polynomials vanish identically
  on the plane and on the degree-q surfaces z − x^7, z − x^7 − y^7 (the Ellenberg–Hablicsek-type obstruction: over F_7 the rational
  points of z = x^7 are those of the plane z = x), and do NOT vanish on z − xy, z − x^3 − y, z − x². So the hypothesis "degree < q"
  is genuinely needed and the paper's D_0 ≤ Cq^{41/80} < q keeps it. Consistent with the proof.

### Lean cross-check (read as text only; no lean run)
Files read: Geometry/{GeometricInduction,GeometricCover,EightIntersections,RichLines,HessianTangent,TotalDegreeCombination,SpanPairLine,Weight,TestRowPencils},
Learning/{PublicDecoderCover,TestActualRow,TestActualMoment(head)}, Validation/ProducedExclusion, Windows/UniformBook, Entropy/SelectedEntropy.
- L1 (FORM DIFFERS, Lean STRONGER). The paper states geom:description as a randomized public-table message with failure probability
  Ce^{−cq} "conditional on any earlier data independent of the tables". The Lean (GeometricInduction.lean `Description`,
  GeometricCover.lean `Validated`) proves a DETERMINISTIC covering family F of decoder-known sets with
  log(|F|+1) ≤ J·q·P·(log(|U|/n)+log(|UT|/t)+P) such that EVERY admissible (S,T) of sizes (n,t) has some W ∈ F capturing n/100
  (resp. 99n/100 for Validated) with |W| ≤ n e^{6P} (resp. ≤ 10^5 q^r/t). The bridge is PublicTables.decoder_cover
  (Learning/PublicDecoderCover.lean): acceptance ≥ e^{−a} for each of ≤ e^H supports with H+1 ≤ e^a ⇒ a common family of
  ⌈e^{2a}⌉ rows covers all supports. So for the DESCRIPTION step the adaptivity/freshness question is moot in the formal proof; only
  the VALIDATION rows use random public tables (Validation/ProducedExclusion.lean `produced_exclusion`, constant 6q, matching
  geom:produced-test with C = 5/0.9 + slack).
- L2 Lean `Uniform r H` carries two hypotheses the paper does not state: exact sizes S.card = n, T.card = t (harmless) and the product
  UPPER bound n·t ≤ 2q^r. The paper derives |S||T| ≤ Cq^{j+1} with C = 4 from sparsity (base:incidence); the Lean's 2q^r is also
  derivable (mixing with density ≤ τ/q, τ→0, gives |S||T| ≤ (1+o(1))q^{j+1}), so this is a statement-form difference, not a gap;
  I did not trace where §5's Lean discharges it (Windows/UniformBook passes it through `Book`).
- L3 Induction shape matches: Lean `uniform_step` : Uniform (i+4) H → Uniform (i+5) (16H+32i+3000), hypothesis constant C' = 400C+4
  per level, b ↦ b + log 4, τ ↦ 400τ — exactly "b' = b+O(1), τ' = Cτ, cost ×O(1) per level" in geom:projection; base case
  Uniform 4 (PG(3,q)) = SpatialPublic.validated_cover. `eight_intersections` (EightIntersections.lean) formalizes the 8-cap
  contraction with per-call loss 3/100, ρ ≤ 1/2, qρ^7 ≤ 1 ⇒ |A| ≤ 3m, capture ≥ |S|/2. Both orientations handled explicitly via
  `bidual` (see objection 2).
- L4 Rich lines: Lean RichFiniteProjective.card_mul_le (SpanPairLine.lean) proves (#lines)·M ≤ 8718|S| for S ⊆ PG(3,q), q prime ≥ 3,
  under 198√(|S|/M) < M, 33√(|S|/M) < q, |S|²e^{−5√(|S|/M)} < 1/2, 8K_p ≤ M² — a more general form than geom:rich-lines (which
  assumes cq ≤ n/M ≤ Cq^{41/40}); the paper's regime implies these. Flatness: HessianTangent.lean `plane_factor_of_flatness`
  / `nonplane_factor_not_flat` carry exactly `G.totalDegree < p`, `CharP K p`, `IsAlgClosed K`, squarefree — same as the paper.
- L5 High moment: Lean `HighPencil` (TestRowPencils.lean) requires |δ'| ≤ 13/100 (paper derives ≤ .18; the typical-hyperplane
  definition actually gives ≤ .1+.02+q/n' < .13, so the Lean bound is the tighter TRUE one), Σδ'² ≤ Be^{LR/100} (paper CBe^{L/100};
  Lean weaker, fine), strong-degree field = learn:strong-degree-input, root-selection fields hSize h ≤ (R/2)/400 and
  p·h·(19/20)^{h−1} < 1/2 = the paper's CRe^{−cR} union over ≤ p lists. Certificates: Entropy/AnchorEventsRealized.lean
  (anchor_step_witnesses, pair_step_witnesses, terminal_paid_certificate). So the sketchy final summation of learn:high-moment
  (objection 4) has a formal counterpart. score_second_tail/score_high_tail give exactly B²e^{−(3/5)LR}/t² and
  B^p e^{−(1/10)pLR}/t^p, matching learn:second-moment / learn:high-moment.
- L6 Selected entropy: Entropy/SelectedEntropy.lean `selected_map_entropy` gives ℓ(d log q + η log σ + log c − 1) − log(2C) ≤ H(F)
  from ℓ ≥ cqσ^{1+η}, N ≤ q^dσ, |alphabet| ≥ q^{2d−1}, pointwise stream domination C/|α|^N, and "F occurs (or reversed F occurs)
  in the stream" — identical content to base:selection-entropy.

## Numbered objections (severity · quoted text · why · fix)

No FATAL and no GAP found in §§1–3 + figures/validation.tex. All objections below are EXPOSITION / UNCLEAR / COSMETIC.

1. EXPOSITION — statement form of the description lemma. 02-geometry.tex, geom:description: "There is a public-table description,
   of length at most CqP(d_S+d_T+P), which, except with probability Ce^{−cq}, produces a decoder-known set W ... The probability
   bound holds conditional on any earlier data independent of the tables used by this invocation."
   Why: the randomized form invites exactly the adaptivity question (tables fixed before/after which selection?), and the figure
   caption has to disclaim "No such comparison is asserted for the description's accepted row". The Lean proves the strictly
   stronger deterministic COVERING form (L1): one family F, log|F| ≤ JqP(d_S+d_T+P), covering every admissible (S,T) at once,
   obtained by union-bounding the acceptance probability over all supports (PublicTables.decoder_cover). That form makes the
   description step adaptivity-free; random tables are then needed only for the validation rows (geom:produced-test).
   Fix: state geom:description (and learn:short-row) in the covering form, keep the public-table form only for geom:validation.
   Also record the product upper bound |S||T| ≤ (1+o(1))q^{j+1} (Lean hypothesis n·t ≤ 2q^r) next to geom:product-upper.

2. EXPOSITION — orientation in the projection. 02-geometry.tex, geom:projection proof: "For a point z represented by a vector line
   ⟨z⟩ ... Write S_0,T_0 for the projected S∖{z} and the cut T∩z^⊥."
   Why: the proof silently assumes the SMALLER side S is the point system. Orientation is load-bearing: the collision bound
   E coll_z(S)/n ≤ Cq^{(3−j)/2} uses n ≤ Cq^{(j+1)/2}; projecting the larger side would give E coll/|T| ≤ C|T|q^{1−j}, which need not
   be o(1). If S is the hyperplane side one must use the dual projection (Lean does this explicitly: `bidual` branch `htn` in
   GeometricInduction.uniform_step). Fix: one sentence "by duality assume S lies in the point system".

3. COSMETIC — constants across levels. geom:projection: "These are the induction hypotheses, with changed fixed constants." and
   "Eight calls multiply the cost and failure bounds by fixed constants."
   Why: correct, but the reader should be told the change is multiplicative per level (Lean: C_b ↦ 400C_b+4, τ ↦ 400τ,
   b ↦ b+log 4, cost constant H ↦ 16H+32i+3000) and that there are ≤ d−3 levels, so all constants are O_d(1) and b, τ do NOT
   compound across the 8 calls of one level (each call re-uses the original S,T). Also "after seven further calls" — five already
   suffice (qρ^5 = q^{−1/4+o(1)}); harmless. Fix: one sentence.

4. UNCLEAR — final summation of the high moment. 03-learning.tex, learn:high-moment, last paragraph: "The weakest per-position saving
   comes from sharing e^{−.68P} between the first two positions of a nonsimple component. It is e^{−.34P} before negligible
   overhead. Summing the expansion proves the asserted B^p e^{−.1pP} bound."
   Why: this is the hardest counting step and it is only sketched — the master inequality combining (a) the 3^{#simple} expansion of
   learn:simple-attenuation, (b) the per-component / per-vertex normalized counts, (c) dictionary multiplicities ≤ (2P+Cp) per
   direction choice, (d) p^{O(p)} labelled structures, is never displayed. I reconstructed it (each position contributes at most
   e^{−.34P+o(P)} after normalization by B; overhead exp(O(p log σ)) = exp(o(pP)) since log σ = o(P); total ≤ B^p e^{−.3pP+o(pP)})
   and found no error; the Lean has explicit budgets (HighPencil.certificateBudget, shiftBudget ≤ e^{2LR/25}) and certificate
   lemmas (AnchorEventsRealized). Fix: display the product bound per structure and the structure count.

5. EXPOSITION — injectivity used silently. learn:high-moment: "The sum of the strengths of the external lines in any fixed tuple
   hyperplane is at most pt_* = .01: assign each such line to one other tuple hyperplane containing it, whose overlap is at most t_*."
   Why: the bound needs the assignment line ↦ other hyperplane to be injective, which holds because two distinct planes through x
   meet in exactly ONE radial line (PG(3,q)); and the "overlap" θ_{HH'} equals that line's strength. Fix: say so.

6. EXPOSITION — the prime hypothesis is essential, say so. 02-geometry.tex intro to geom:rich-lines: "here the argument keeps every
   relevant surface degree below the characteristic."
   Why: D_0 ≤ Cq^{41/80} < q only because q is PRIME (char = q). Over F_{p^2} the characteristic is q^{1/2} < D_0 and the argument
   fails exactly at the Ellenberg–Hablicsek/Hermitian obstruction. My flat_checks.py confirms the threshold is sharp: over char 7,
   z − x^7 has all flatness polynomials Q_ij ≡ 0 (and its F_7-points are those of the plane z = x), while degree-2,3 nonplanar
   surfaces do not. Theorem 1.2 and the §6 transfer use primes only, so nothing breaks; but the dependence should be explicit.

7. EXPOSITION — a non-constant-probability event in the learning step. learn:empty-exceptional: "with probability at least ce^{−8Pτ}".
   Why: Pτ is not O(1) (up to ~σ^{1−η/2−91β} at the top of the D range), so this event is NOT one of the "constant-probability
   restrictions" of §1's remark after base:selection-entropy. It is harmless because it is an event of public-table/auxiliary
   sampling absorbed into the proposal search (learn:implementation: acceptance ≥ ce^{−8Pτ}e^{−2qP(d_S+log 2)} ≥ e^{−C_1qP(d_S+1)},
   using Pτ = o(qP)), never a conditioning of the stream law. Fix: one sentence saying so.

8. COSMETIC — notation collisions that cost the reader time: D_0 = interpolation degree (geom:interpolating-degree) AND the static
   exceptional set (learn:overlap-input), next to the budget D; p = moment order AND p_j (incidence probability); h = row length
   (geom:validation), dyadic multiplicity (geom:preparation), residual-vertex count (learn:high-moment) AND formal branch (rich lines);
   B = q^j/n' AND events 𝓑_H AND the §5 support B; C_0 reused for three different constants; n in geom:rich-lines is an upper bound
   while elsewhere n = |S|.

9. COSMETIC — citation scope. 02-geometry.tex: "The interpolation and tangent-plane method has antecedents in
   \cite{GuthKatz2010,ElekesKaplanSharir2011}." GuthKatz2010 in references.bib is the joints paper (Adv. Math. 225 (2010)), not the
   distinct-distances paper (Ann. Math. 2015) where the plane-capped rich-lines theorem is proved. The paper only claims
   "antecedents" and proves geom:rich-lines itself, so no false attribution; a pointer to GK2015 / Ellenberg–Hablicsek's char-p
   rich-lines theorem would help readers.

10. COSMETIC — units/sizes. geom:description "length" is in bits ("O(1+log(m+1)) bits") while all entropies are in nats; constant
    factor only. learn:typical-bounds' .18 is loose (true bound < .13, as the Lean's HighPencil.deviation uses). "R/2 ≥ 200"
    needs σ^β ≥ 400, i.e. log q ≥ 400^{10^7/η}: "sufficiently large q" is astronomically large (fine for an asymptotic statement).

11. CROSS-SEAT POINTER (not an objection to §§1–3). The description+validation cost CqP(d_S+d_T+P) carries d_S+d_T = Θ(σ) whenever a
    domain is still a full projective space (tree spine). §5 bounds the sum via comp:gap-potential / comp:potential-branch to
    comp:tree-cost = CqP log(w+2)(σ+wP) + Cwσ. With P up to 4σ^{1−η/2+9β} and w ≤ Cσ^{1+η/2}/D, the σ-term qPσ·log w is NOT
    small against the final surplus ηℓ log σ ≍ qσ^{1+η}log σ by itself — so the §5/§6 seat must check that comp:tree-cost is
    compared against the stage budget comp:step-bounds (D-dependent), not against the final surplus, and that the iteration in
    §6 keeps the sum O(k)+o(ηk log σ). I did not audit §§4–6.

## Lemmas checked and holding
base:incidence (identity verified symbolically and numerically, mixing constant 1, C = 4), base:flag-graph (brute-force check, bound
attained), base:rectangles, base:selection-entropy (and Lean SelectedEntropy matches), base:event-transfer, base:tails,
base:scale-comparisons; geom:description (all branches, via the induction closed in learn:completion), geom:validation (both tests,
costs, failure), geom:produced-test (law domination 1/.9, exclusion Cq|X∩N(y)|/|X|), geom:projection (center existence, hypothesis
transfer b+O(1), τ·O(1), gap +O(1); lift loss < .02n per call; contraction ρ ≤ q^{−1/4+o(1)}; |A_8| = O(m_0)),
geom:preparation (enumeration, greedy plane list, large-cell reduction to PG(2,q) with q lifts per line and dyadic class),
geom:rich-lines (sampling, interpolation, plane factors, flatness polynomials, non-flatness below the characteristic, coprime
combination, 2D_1D_2 common-line bound), geom:radial, geom:overlap (incl. strong degree), learn:regular-pencils,
learn:empty-exceptional, learn:one-mean/one-covariance/one-bounds, learn:second-moment, learn:high-moment (component,
singleton, anchor/pair/root certificate arguments; final sum reconstructed), learn:row-success, learn:implementation,
learn:short-row, learn:completion; figure geom:validation-figure consistent with the text.

Priority answers: (1) repeated projection preserves the hypotheses with O(1) loss per level in b, a constant factor in τ, O(1) in the
log-gaps, a constant factor in cost; ≤ d−3 levels; the lifted 8-fold intersection has size O(ne^{CP}) and captures ≥ .84n — HOLDS.
(2) Poisson batches / moment argument / rich lines HOLD; every polynomial degree is ≤ 3D_0 ≤ Cq^{41/80} < q = char (q prime); the
polynomial-method inputs are re-proved, not imported, and the E–H obstruction is genuinely avoided (only because q is prime).
(3) §1 inequalities hold with explicit constants; those reused Θ(k) times (event-transfer, linear in KL; selection entropy, used once
at the end with a constant domination factor) do not compound. (4) Validation: fresh tables, second test conditional on the first cap
with its source fixed, failure e^{−cq} per test, produced-row law ≤ (1/.9)·iid on the hidden source — HOLDS.
