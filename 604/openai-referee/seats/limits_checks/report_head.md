# Referee report — seat `limits` — §7 (pp. 22–26) of "The weak pinned planar distance theorem" (OpenAI, 23 Sep 2026)

Scope: §7 in full (7.1–7.4 plus the closing paragraph), brief items (viii) and (ix), and the §7 slice of (i).
Every displayed formula below was read off the **rendered PDF** (Read tool, pages 22–26), not paper.txt.
Upstream inputs I used without re-verifying (other seats own them): (2.2), (2.3)/(5.8), Lemma 3.1 / (3.4) (only "E|Δ| is a finite absolute constant"), Lemma 3.2 / (3.5), the definitions (3.7) of W₂, A, W, Lemma 5.1 / (5.1)–(5.2) for both families, injectivity of Z_j under every embedding (§3.1).
Lean consulted as text only (no lean/lake run): MobiusObstruction.lean, BoundedContradiction.lean, LimitObstruction.lean, LogBounds.lean, WeightedSelection.lean.

## Verdict for this scope

**HOLDS AS READ.** I found no FATAL and no GAP in §7. Every step checks line by line, given the upstream inputs listed above. Nine objections follow. All are COSMETIC or wording-level UNCLEAR, and none needs new mathematics. The one point the brief flagged hardest is settled by the PDF. (7.1) is **E_π |log|U_j(x) − U_j(y)|| ≤ C₁**, with the absolute value outside the log. paper.txt drops the outer bars. The absolute value is not just a typographic detail. Because m_j = E_π i_j, the signed mean E_π log|U_j(x) − U_j(y)| is **identically 0**. So the signed reading would be vacuous, and with it (7.2) and (7.3) would both fail; my control in Check 2 shows this. With the absolute value, (7.2) uses the positive part, (7.3) uses the negative part, and each part equals exactly C₁/2.

## Objections

**1. (7.1), p. 23. Absolute value: an extraction artifact, plus a remark the paper does not make.** COSMETIC. This concerns the text file, not the paper.
PDF: "We have  E_π|log|U_j(x) − U_j(y)|| ≤ C₁.  (7.1)  Only distinct pairs occur here." paper.txt line 1216 reads "Eπ log |Uj (x) − Uj (y)| ≤ C1", which loses the outer bars.
What the paper proves is E_π|i_j − m_j| = O(1). Since log|U_j(x)−U_j(y)| = m_j − i_j(x,y), this is exactly (7.1) with the absolute value. Because m_j := E_π i_j, we have E_π log|U_j(x)−U_j(y)| = 0 exactly. Hence E_π(log)_+ = E_π(log)_− = C₁/2. Check 2 shows this numerically to 1e−16 on three configurations. (7.2) is Markov on (log)_+ and (7.3) is Markov on (log)_−. Both are correct as written.
Fix: none needed in the paper. Anyone working from paper.txt must use the PDF line.

**2. §7.1, p. 22. Attribution of the two archimedean sums.** COSMETIC (exposition).
"Since W is bounded, Lemma 5.1 gives  Σ_{v|∞} σ_v T_v ≤ C,  Σ_{v|∞} σ_v V_v = η_n → 0."
The first inequality does not come from Lemma 5.1. It comes from (3.7): W = W₂ + A = Σ_v σ_v E_grids Σ_j (E_π L_j + E_α S_j) = Σ_v σ_v T_v over **all** places, together with T_v ≥ 0 at the finite places (L, S ≥ 0). The second statement defines η_n as the archimedean part of the left side of (5.1) for both families. That part is ≤ o(W+1) = o(1), because the integrands are nonnegative at finite places.
Fix: cite (3.7) for the first sum.

**3. §7.1, p. 22. "the local integrals on the left of (5.2)".** COSMETIC.
The label (5.2) sits on the second line, "= o(W + 1)", of a chained display. The literal left side of that line is C_M n^{c−γ}W₂ + W_{2,sm}. The intended object is the integrand inside I[…] on the left of (5.1): E_F(p−a)²1{m>n^{1−c}} + p²1{m ≤ n^{1−c}, p ≥ 2/k}, at place v, summed over j and both families, with E_grids and without σ_v. My reading of the rest of §7 uses this, and (7.5) uses only its large-cell term.

**4. §7.1, p. 23. The selection step.** COSMETIC.
"The places with T_v ≤ 2C+1 have total weight at least 1/2, so one of them satisfies V_v ≤ 2η_n."
The step is correct. The inference is: minimum over the set G = {T_v ≤ 2C+1} ≤ (Σ_{v∈G} σ_v V_v)/σ(G) ≤ η_n/(1/2). It is not "Markov on V over all places", which would need weight strictly above 1/2 on both sides. In fact σ(G) ≥ 1 − C/(2C+1) = (C+1)/(2C+1) > 1/2. The step uses V_v ≥ 0 off G. "No lower bound on an individual place weight" is correct. The Lean `weighted_select` proves the same conclusion by a different combination, Σ w (T + (C+1)V/ε) ≤ 2C+1.

**5. §7.2, p. 24. Oscillation constant.** COSMETIC.
"Its oscillation is at most ω_φ(√2ε), where ω_φ is a uniform modulus of continuity in the spherical metric."
The squares have Euclidean diameter ≤ √2ε. The chordal distance satisfies χ(z,w) ≤ |z−w| only for the diameter-1 sphere. On the unit sphere, χ = 2|z−w|/√((1+|z|²)(1+|w|²)) ≤ 2|z−w|, which gives ω_φ(2√2ε). This does not matter, since ε ↓ 0.

**6. §7.2, p. 24. "(7.4) on … Cauchy–Schwarz … at most √(N V_v)".** No objection: checked; the step is correct. I record the measure it uses, because the step is compressed. The measure is P_grids × Leb(I_ε) × (family weights, total ω ≤ 1) × counting over a grid- and level-dependent index set of at most N occurrences. Its total mass is ≤ N. So ∫ E_F|ν(C)−α(C)| ≤ √N · (∫ E_F(ν(C)−α(C))²)^{1/2}. The integral on the right is over a subset of what V_v integrates: a unit level window (shifted by m_j) and a subset of occurrences with |C| > n^{1−c}. Hence it is ≤ V_v.

**7. §7.3, p. 24. "Passing to Q proves the assertion."** COSMETIC (compressed).
The full step: µ ↦ d(µ, β_j) is bounded and continuous on P(S). So E_Q d(µ_j, β_j) = lim E_q d((U_j)_*µ_e, β_j) = lim E_e d(ν_n^j, β_j) = 0. This holds because under q the fiber e has law k_e/|E|. Therefore µ_j = β_j Q-a.s.

**8. Lemma 7.1 proof, p. 26. Two wording points; the proof is correct.** UNCLEAR wording / COSMETIC.
(a) "Choose continuous weights w_l : [0,1] → [0,1], for integers l ≥ 3, each supported inside (0,1) and equal to one on [1/l, 1 − 1/l]." Finiteness of J_w and (7.7) need w to vanish outside a **compact** subinterval [δ, 1−δ], as the definition three paragraphs earlier requires. "Supported inside (0,1)" must be read that way. A w with only w(0) = w(1) = 0 can make J infinite. Example: w(t) = t near 0 together with X = log(|Z−a|/|Z−a′|), where β₁ is nonatomic but log-heavy near a, so that E X₊ = ∞. A piecewise-linear w_l supported on [1/(2l), 1 − 1/(2l)] exists, so this is wording only.
(b) "For Z of law β₂, the variable −log|Z − b′| is nonconstant." This does **not** follow from nonatomicity alone. Counterexample: β₂ = the uniform measure on a circle centred at b′ is nonatomic and makes −log|Z−b′| ≡ const. The claim is true because b′ ∈ supp β₂, which was fixed in the previous sentence and is used in the "More explicitly" sentence, so the proof is right. (The Lean's MobiusObstruction uses a cross-ratio energy, min(1, |(z−w)/(w−d)|), whose positivity needs no support condition on d.)

**9. Closing paragraph, p. 26.** No objection: checked; the step is correct. "Every sequence of nonnegative real numbers has a bounded subsequence or a subsequence tending to infinity." This is true. §7 nests its subsequences correctly: W bounded ⊃ α_n^j ⇒ β_j for both j ⊃ Q-convergence. (7.4) is proved along the second and used along the third. No earlier subsequence is forgotten. The o(1)'s from (2.3), (4.5) and (5.2) are along the Prop. 2.2 sequence, so they hold on every subsequence.

## Line-by-line status

| Item | Status | Notes |
|---|---|---|
| T_v (def.), V_v (def.) | VERIFIED LINE BY LINE | W = Σ_v σ_v T_v over all places (3.7); V_v ≥ 0 (Obj. 2, 3) |
| Σ_{v∣∞}σ_vT_v ≤ C, Σσ_vV_v = η_n → 0 | VERIFIED | needs only W bounded + (5.2); finite places nonneg |
| Selected place: T_v ≤ 2C+1, V_v ≤ 2η_n | VERIFIED | min ≤ restricted average (Obj. 4); Lean `weighted_select` |
| E_grids E_π\|i_j − M_j\| ≤ E_grids E_π(L_j + S_j(x) + S_j(y) + \|Δ_j\|) = O(1) | VERIFIED | from (3.5): i_j − M_j = L_j − S_j(x) − S_j(y) − Δ_j; E_π S_j(x) = E_α S_j (π has uniform marginals), so ≤ 2T_v + E\|Δ\| ≤ 2(2C+1) + C₀/b₀ |
| \|m_j − M_j\| ≤ E_π\|i_j − M_j\| per grid ⇒ E_π\|i_j − m_j\| = O(1) | VERIFIED | E_π\|i_j−m_j\| ≤ 2E_π\|i_j−M_j\| per grid; LHS grid-free, so average over grids |
| U_j = e^{m_j}Z_j + b_j, (7.1) | VERIFIED (PDF has \|log\|) | log\|U_j(x)−U_j(y)\| = m_j − i_j; C₁ = 2(4C+2+C₀/b₀) fixed; signed mean ≡ 0 (Obj. 1) |
| (α⊗α){\|z−z′\|>R} ≤ C₁/log R | VERIFIED | Markov on (log)₊; diagonal contributes nothing; off-diagonal α⊗α = ((n−1)/n)π |
| choice of R₀, center, b_j | VERIFIED | average over empirical centers of α{\|z′−z\|>R₀} < 1/2 ⇒ some center has disk mass > 1/2 |
| (7.2) | VERIFIED | R > 2R₀ ⇒ \|z−z′\| > R − R₀ > R/2; (1/2)α{\|z\|>R} ≤ C₁/log(R/2) |
| (7.3) | VERIFIED | diagonal Σα(x)²1_B ≤ 1/n by injectivity of U_j; off-diagonal pairs at distance < 2r, Markov on (log)₋ |
| Riemann sphere, P(S) compact, Portmanteau | VERIFIED | [14] matches (citation table); β_j{∞} ≤ liminf α_n(O_R) ≤ 2C₁/log(R/2) → 0; β_j{z₀} ≤ (C₁/log(1/2r))^{1/2} → 0 |
| §7.2 normalized grids, level shift −m_j | VERIFIED | similarity maps nested square grids to nested square grids; ∫ over all levels is translation invariant |
| sides in (ε/(2e), ε] on I_ε | VERIFIED | level-r cells are the squares of the largest side l_m ≤ e^{−r}, so l ∈ (e^{−r}/2, e^{−r}]; for r ∈ I_ε, e^{−r} ∈ [ε/e, ε] |
| N(R,ε) | VERIFIED | squares of side ≥ ε/(2e) meeting the disk lie in the radius R+√2ε disk ⇒ area count, any orientation |
| transformed-occurrence trick | VERIFIED | \|ν(B′)−α(B′)\| = \|ν(P∖B′)−α(P∖B′)\|; B′ ↦ occurrence is injective into the multiset C_j(r) |
| large-cell CS term √(NV_v) | VERIFIED | Obj. 6 |
| small-cell term (B+1)n^{−c} | VERIFIED | E_Fν(C) ≤ Bα(C), ωα(C) ≤ α(C) ≤ n^{−c} |
| (7.5) | VERIFIED | split per square: φ(z_Q)(ν−α)(Q) + oscillation·(ν+α)(Q) (total ≤ 2ω_φ) + outside-disk squares ≤ (B+1)‖φ‖α{\|z\|>R} |
| order of limits | VERIFIED | n → ∞ (V_v ≤ 2η_n → 0, Nn^{−c} → 0), then R → ∞ using (7.2) uniform in n, then ε ↓ 0; finally α_nφ → β_jφ |
| incoming-law extension | VERIFIED | omitted targets have q_Y-mass O(n^{γ−1}) by (2.3)/(5.8); each costs ≤ 2‖φ‖ |
| §7.3 joint object, Q | VERIFIED | S⁴ × P(S)² is compact metrizable; law of the object is finitely supported |
| countable dense (f_r), metric d | VERIFIED | C(S) separable; standard metrization; Obj. 7 |
| domination 2B₀β_j⊗β_j | VERIFIED | 1/(n(n−1)) ≤ 2/n² for n ≥ 2; α_n⊗α_n ⇒ β⊗β; limit inequality on nonneg C(S²) ⇒ inequality of measures (regularity) |
| a,b,a′,b′ ∈ ℂ, a≠a′, b≠b′, supports | VERIFIED | (β⊗β)({∞}×S) = 0, (β⊗β)(diag) = ∫β{z}dβ = 0, (β⊗β)(S×(supp β)ᶜ) = 0 |
| a ∼ β₁ independent of the PAIR (a′,b′) | VERIFIED | q(x,y) = q_Y(y)ρ_y(x); (7.4) for ρ_y, j = 1; products f⊗g are dense in C(S×S²) (Stone–Weierstrass). WHY THE PAIR: (7.8) depends on (a, a′, b′), and Fubini needs law(a, a′, b′) = β₁ ⊗ law(a′,b′). With a ⊥ a′ alone, the conditional law of a given b′ could differ from β₁, and "for β₁-a.e. a" would fail. b may depend on everything (in the prelimit, b is a function of a) |
| prelimit Möbius relation | VERIFIED + Check 3 | (U₁(z)−U₁(x))(U₂(z)−U₂(x)) = e^{m₁+m₂}σ_v(t_e) for all z ∈ F_e ⇒ U₂(z) = b + t′/(U₁(z) − a), t′ = (a′−a)(b′−b) |
| (7.6) passage to the limit | VERIFIED | D = {finite, a≠a′, b≠b′} is open in S⁴; (p, ν) ↦ Φ_{p*}ν is continuous on D × P(S) (PGL₂ acts jointly continuously on Ĉ, det = −t′ ≠ 0); graph relatively closed; complement open in the ambient space; every prelimit atom lies in D and on the graph ⇒ Q_n(O) = 0 ⇒ Q(O) = 0 (Portmanteau (d)); Q(D) = 1 |
| Lemma 7.1 statement | VERIFIED | |
| J_w finite, translation invariant | VERIFIED | needs compact support (Obj. 8a) |
| (7.7) | VERIFIED | for u ≥ ε the tail is < δ; for u ≤ −ε it is ≥ Pr(\|X_k\| < ε) > 1−δ |
| Φ(z) − b′ = (b′−b)(a′−z)/(z−a); −log\|Φ(z) − b′\| = log(\|z−a\|/\|z−a′\|) − log\|b′−b\| | VERIFIED (by hand + Check 1A, error 7.5e−14) | |
| (7.8) | VERIFIED + Check 1B | β₁{a} = β₁{a′} = 0 ⇒ a.s. finite; W = Φ(Z) ∼ β₂ |
| measurability remark | VERIFIED | Borel kernel ⇒ (a,a′,u) ↦ β₁{…} jointly measurable ⇒ Tonelli |
| Fubini + independence | VERIFIED | countably many l; the equality set depends on (a,a′,b′) only and has Q-mass 1, because b ≠ b′ a.s. |
| choice of l, RHS > 0 | VERIFIED | tail ∈ [q, 1−p] on (−log r₀, −log r); needs b′ ∈ supp β₂ (Obj. 8b) |
| a_k → a′ inside the full-measure set | VERIFIED | B(a′,1/k)∖{a′} has positive β₁-mass and the equality set has full measure ⇒ they meet |
| convergence in probability, contradiction | VERIFIED + Check 1C | pointwise off the countable null set {a′, a₁, …} |
| closing paragraph | VERIFIED | Obj. 9 |

"Similarly / indeed / as is seen" phrasing in §7 appears 6 times: "a similar use of (7.1)" at (7.3), four "Indeed …" sentences, and "as is seen by testing continuous functions …" at (7.6). I expanded and checked every one; all hold.

## Brief (viii) — direct answers
- (7.1) is the absolute version (PDF). (7.2) needs the positive part and (7.3) the negative part; the normalization makes them equal (= C₁/2).
- The selected place: correct (Obj. 4). It needs no lower bound on σ_v. This matters because [K:Q] is unbounded.
- (7.4)–(7.5): N(R,ε) is uniform in grid, level and n. The giant complement is handled by transforming the occurrence, and the giant square at small levels is a genuine side-≤ε square. Order of limits is correct.
- Independence from the PAIR: correct and necessary (see the table).
- (7.6): the equality graph is relatively closed over the open domain; its complement is open in the ambient space; prelimit mass is exactly 0; Portmanteau applies. Correct.
- Lemma 7.1: correct line by line, with the two wording points in Obj. 8. The existence of a_k → a′ inside the full-measure set is correct.

## Brief (ix) — quantifiers and prove-too-much, for §7
- All constants in §7 (C, C₁, R₀, B = B₀) are fixed before n → ∞. N(R,ε) is uniform. Nothing depends on the configuration.
- §7 is pure compactness plus contradiction: weak limits along unspecified subsequences, and Lemma 7.1 is qualitative. It yields **no rate**, and the paper claims none. Nothing in §7 claims n/√log n.
- The limits are taken in the right order relative to every supremum. The only uniform-in-n inputs are (7.2), (7.3) and N(R,ε), and they are uniform.

## Brief (i) — what §7 uses of characteristic 0 / the archimedean place
1. Σ_{v∣∞} σ_v = 1 and W = Σ_v σ_v T_v. The archimedean places carry a fixed fraction of the total weight. This is what makes selecting a single complex embedding possible. Over F_q there is no archimedean place and nothing to select.
2. The complex modulus at the selected embedding, the local compactness of ℂ, and compactness of the Riemann sphere: the limits β_j exist only because of these.
3. Injectivity of U_j at that embedding (Z_j-differences are nonzero elements of K). It gives the 1/n diagonal term in (7.3) and a ≠ a′ in the prelimit.
4. The factorization (3.1) and t ≠ 0, which give the Möbius relation with det = −t′ ≠ 0.

Beyond (3.1), §7 uses nothing Euclidean. Lemma 7.1 holds verbatim for nonatomic laws on ℝ ∪ {∞}. A real-place, null-coordinate (Minkowski u² − b² = (u+b)(u−b)) version of §7 would go through unchanged. Whether §3's grids and Lemma 3.1 transfer to real places is outside this seat; the `whole` seat owns the generalized statement.

## Lean cross-reference (text only; not a substitute for the paper)
`BoundedContradiction.lean` (`arithmetic_no_bounded`) follows the paper's §7 route:
- `bounded_place_selection`, i.e. the T_v/V_v selection;
- `logNormalize`, i.e. the normalization U = e^{E_π i}·z. Its `logCost` is `|Real.log ‖u x − u y‖|`, which confirms the absolute value in (7.1);
- `log_center` / `small_ball_card`, i.e. (7.2)/(7.3);
- `sphere_arch_test_rate`, i.e. (7.4).

Two places differ from the human-readable text:
(a) The limit object is an "expanded" finite law (an edge plus an additional fiber point; `expandedProbability`, `weak_chart_closed` with `zEquation`/`wEquation`). The paper's P(S)²-valued random element is not used.
(b) The obstruction (`MobiusObstruction.lean`, `no_finite_law` / `bounded_mobius`) uses the cross-ratio energy ∫∫ min(1, |(a′−a)(w−z)/((z−a)(a′−w))|) dβ₁dβ₁ against ∫∫ min(1, |(z−w)/(w−b′)|) dβ₂dβ₂, not the paper's J_w. It has the same hypotheses: `IndepFun (q.1) (q.2.2)` is "a ⊥ (a′,b′)", plus a′ ∈ supp β₁ and b ≠ b′.

So the paper's J_w proof of Lemma 7.1 and its P(S)² limit object are **not** the formalized text. I checked both by hand and both hold. If the Lean compiles, it settles the theorem regardless.
