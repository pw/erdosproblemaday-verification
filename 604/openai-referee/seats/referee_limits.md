# Referee report — seat `limits` — §7 (pp. 22–26) of "The weak pinned planar distance theorem" (OpenAI, 23 Sep 2026)

Scope: §7 in full (7.1–7.4 plus the closing paragraph), brief items (viii) and (ix), and the §7 slice of (i).
Every displayed formula below was read off the **rendered PDF** (Read tool, pages 22–26), not paper.txt.
Upstream inputs I used without re-verifying (other seats own them): (2.2), (2.3)/(5.8), Lemma 3.1 / (3.4) (only "E|Δ| is a finite absolute constant"), Lemma 3.2 / (3.5), the definitions (3.7) of W₂, A, W, Lemma 5.1 / (5.1)–(5.2) for both families, injectivity of Z_j under every embedding (§3.1).
Lean consulted as text only (no lean/lake run): MobiusObstruction.lean, BoundedContradiction.lean, LimitObstruction.lean, LogBounds.lean, WeightedSelection.lean.

## Verdict for this scope

**HOLDS AS READ.** I found no FATAL and no GAP in §7. Every step checks line by line, given the upstream inputs listed above. Nine numbered items follow. Items 6 and 9 are verification notes, not objections. The other seven are COSMETIC or wording-level UNCLEAR, and none needs new mathematics. The one point the brief flagged hardest is settled by the PDF. (7.1) is **E_π |log|U_j(x) − U_j(y)|| ≤ C₁**, with the absolute value outside the log. paper.txt drops the outer bars. The absolute value is not just a typographic detail. Because m_j = E_π i_j, the signed mean E_π log|U_j(x) − U_j(y)| is **identically 0**. So the signed reading would be vacuous, and with it (7.2) and (7.3) would both fail; my control in Check 2 shows this. With the absolute value, (7.2) uses the positive part, (7.3) uses the negative part, and each part equals exactly C₁/2.

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

## Finite checks (all run with ~/.venv/bin/python -I; each < 2 s, < 100 MB RSS)

### Check 1 — Lemma 7.1 mechanism, (7.7), (7.8); β₁ = Unif(unit disk), N = 400,000 samples; J computed EXACTLY for the empirical law
What it shows:
- (A) The algebra identity holds to 7.5e−14. CONTROL: the product kernel log(|z−a|·|z−a′|) is off by 13.25.
- (B) (7.8) is an identity of J-values: diff 8.9e−16. CONTROL: the product kernel differs by 0.034. This is far above the 1e−15 level of the exact identity, though small, because J_w is invariant under translation and, for symmetric w, under negation; a sign-flip control would NOT fail, which is why I used the product kernel.
- (C) With a′ ∈ supp β₁ and β₁ nonatomic, the left side of (7.8) decays to 0 roughly linearly in |a_k − a′| (1.32 → 4.5e−4). The right side for a nonatomic β₂ with b′ in its support is 1.48 > 0.
- CONTROL 1 (D): an atom of mass 0.3 at a′ makes X_k = +∞ on the atom. The truncated J grows like U (10 → 100 → 1000), so J = ∞ and the LHS does NOT tend to 0.
- CONTROL 2 (E): a near-atom (mass 0.3 on a disk of radius 1e−9) keeps J ≥ 4 down to |a_k − a′| ≈ 3e−8, decaying only like log(|a_k−a′|/ρ).
- CONTROL 3 (F): a′ outside supp β₁ gives inf_a J ≥ 0.757.
So nonatomicity and the support condition are both load-bearing, as the proof says.

```python
# Finite illustration of Lemma 7.1 / (7.7) / (7.8) of the OpenAI #604 preprint.
# J_w(X) = \int w(Pr(X >= u)) du, computed EXACTLY for the empirical law of a sample:
# for u in (X_(i), X_(i+1)], Pr(X>=u) = (N-i)/N  (0-indexed sorted, i = 1..N-1 gaps).
import numpy as np
rng = np.random.default_rng(604)

def w_l(t, l):
    # continuous, compactly supported in (0,1), =1 on [1/l, 1-1/l]
    lo, hi = 1.0/(2*l), 1.0/l
    t = np.asarray(t, float)
    out = np.zeros_like(t)
    up = (t > lo) & (t < hi); out[up] = (t[up]-lo)/(hi-lo)
    mid = (t >= hi) & (t <= 1-hi); out[mid] = 1.0
    dn = (t > 1-hi) & (t < 1-lo); out[dn] = ((1-lo)-t[dn])/(hi-lo)
    return out

def J(x, l, U=None):
    """exact J_{w_l} of the empirical law of finite sample x; +inf entries allowed,
    then the u-integral is truncated to [-U, U] (needs U)."""
    x = np.sort(np.asarray(x, float)); N = len(x)
    fin = np.isfinite(x)
    if not fin.all():
        assert U is not None
        x = np.where(np.isposinf(x), U, x); x = np.clip(x, -U, U)
    gaps = np.diff(x)                         # length of (x_(i), x_(i+1)]
    tail = (N - np.arange(1, N)) / N          # Pr(X >= u) on that gap
    return float(np.sum(w_l(tail, l) * gaps))

def unif_disk(N, c=0j, rad=1.0):
    r = rad*np.sqrt(rng.random(N)); th = 2*np.pi*rng.random(N)
    return c + r*np.exp(1j*th)

N = 400_000; l = 10
Z = unif_disk(N)                                   # beta_1 = uniform on unit disk (nonatomic)
ap = 0.3+0.2j                                      # a' in supp beta_1

print("== (A) algebra: -log|Phi(z)-b'| = log(|z-a|/|z-a'|) - log|b'-b| ==")
a, b, bp = -0.4+0.1j, 2.0-1.0j, 1.5+0.5j
t = (ap-a)*(bp-b)
Phi = lambda z: b + t/(z-a)
lhs = -np.log(np.abs(Phi(Z)-bp))
rhs = np.log(np.abs(Z-a)/np.abs(Z-ap)) - np.log(abs(bp-b))
print("  max |lhs-rhs| =", np.max(np.abs(lhs-rhs)))
wrong = np.log(np.abs(Z-a)*np.abs(Z-ap)) - np.log(abs(bp-b))   # CONTROL: product instead of ratio
print("  CONTROL (product kernel) max |lhs-wrong| =", np.max(np.abs(lhs-wrong)))

print("== (B) (7.8) as an identity of J-values for one Mobius map (beta_2 := Phi_* beta_1) ==")
W = Phi(Z)
J_left = J(np.log(np.abs(Z-a)/np.abs(Z-ap)), l)
J_right = J(-np.log(np.abs(W-bp)), l)
print("  J_left =", J_left, " J_right =", J_right, " diff =", J_left-J_right)
J_ctrl = J(np.log(np.abs(Z-a)*np.abs(Z-ap)), l)
print("  CONTROL J(product kernel) =", J_ctrl, " (differs from J_right by", J_ctrl-J_right, ")")

print("== (C) Lemma 7.1 mechanism: LHS of (7.8) -> 0 as a_k -> a' (beta_1 nonatomic, a' in supp) ==")
for k in range(0, 13, 2):
    ak = ap + 0.5*2.0**(-k)*np.exp(1j*0.7*k)
    X = np.log(np.abs(Z-ak)/np.abs(Z-ap))
    print(f"  k={k:2d} |a_k-a'|={abs(ak-ap):.2e}  J_l(X_k)={J(X,l):.5f}")
beta2 = unif_disk(N, c=1.0+0j, rad=2.0)            # some nonatomic beta_2, b' in its support
bp2 = 1.5+0.5j
print("  RHS of (7.8) for beta_2=Unif(disk(1,2)), b'=1.5+0.5i: J_l(-log|W-b'|) =", J(-np.log(np.abs(beta2-bp2)), l))

print("== (D) CONTROL 1: beta_1 with an ATOM at a' (mass 0.3): X_k = +inf on the atom ==")
Za = Z.copy(); Za[:int(0.3*N)] = ap               # atom at a'
with np.errstate(divide='ignore'):
    for k in (0, 6, 12):
        ak = ap + 0.5*2.0**(-k)*np.exp(1j*0.7*k)
        X = np.log(np.abs(Za-ak)) - np.log(np.abs(Za-ap))   # +inf on the atom
        print(f"  k={k:2d}  J truncated to |u|<=U:", {U: round(J(X, l, U=U),3) for U in (10, 100, 1000)})
print("  (grows linearly in U: J = +inf, does NOT tend to 0)")

print("== (E) CONTROL 2: near-atom (mass 0.3 uniform on disk radius 1e-9 about a') ==")
Zn = Z.copy(); Zn[:int(0.3*N)] = unif_disk(int(0.3*N), c=ap, rad=1e-9)
for k in range(0, 25, 4):
    ak = ap + 0.5*2.0**(-k)*np.exp(1j*0.7*k)
    X = np.log(np.abs(Zn-ak)/np.abs(Zn-ap))
    print(f"  k={k:2d} |a_k-a'|={abs(ak-ap):.2e}  J_l(X_k)={J(X,l):.4f}")

print("== (F) CONTROL 3: a' NOT in supp beta_1 (a'=2.0, beta_1=Unif(unit disk)) ==")
ap_out = 2.0+0j
grid = [x+1j*y for x in np.linspace(-1,1,21) for y in np.linspace(-1,1,21) if x*x+y*y<=1]
vals = [J(np.log(np.abs(Z[:100000]-g)/np.abs(Z[:100000]-ap_out)), l) for g in grid]
print("  min over a in supp of J_l(log|Z-a|/|Z-a'|) =", min(vals), " (bounded away from 0: no a_k -> a')")
```
Output:
```
== (A) algebra: -log|Phi(z)-b'| = log(|z-a|/|z-a'|) - log|b'-b| ==
  max |lhs-rhs| = 7.549516567451064e-14
  CONTROL (product kernel) max |lhs-wrong| = 13.252726418973628
== (B) (7.8) as an identity of J-values for one Mobius map (beta_2 := Phi_* beta_1) ==
  J_left = 2.1674384786822207  J_right = 2.16743847868222  diff = 8.881784197001252e-16
  CONTROL J(product kernel) = 2.201410900563607  (differs from J_right by 0.03397242188138705 )
== (C) Lemma 7.1 mechanism: LHS of (7.8) -> 0 as a_k -> a' (beta_1 nonatomic, a' in supp) ==
  k= 0 |a_k-a'|=5.00e-01  J_l(X_k)=1.32097
  k= 2 |a_k-a'|=1.25e-01  J_l(X_k)=0.45825
  k= 4 |a_k-a'|=3.13e-02  J_l(X_k)=0.11588
  k= 6 |a_k-a'|=7.81e-03  J_l(X_k)=0.02899
  k= 8 |a_k-a'|=1.95e-03  J_l(X_k)=0.00724
  k=10 |a_k-a'|=4.88e-04  J_l(X_k)=0.00182
  k=12 |a_k-a'|=1.22e-04  J_l(X_k)=0.00045
  RHS of (7.8) for beta_2=Unif(disk(1,2)), b'=1.5+0.5i: J_l(-log|W-b'|) = 1.475962026342176
== (D) CONTROL 1: beta_1 with an ATOM at a' (mass 0.3): X_k = +inf on the atom ==
  k= 0  J truncated to |u|<=U: {10: 10.266, 100: 100.266, 1000: 1000.266}
  k= 6  J truncated to |u|<=U: {10: 10.012, 100: 100.012, 1000: 1000.012}
  k=12  J truncated to |u|<=U: {10: 10.0, 100: 100.0, 1000: 1000.0}
  (grows linearly in U: J = +inf, does NOT tend to 0)
== (E) CONTROL 2: near-atom (mass 0.3 uniform on disk radius 1e-9 about a') ==
  k= 0 |a_k-a'|=5.00e-01  J_l(X_k)=20.9932
  k= 4 |a_k-a'|=3.13e-02  J_l(X_k)=18.0029
  k= 8 |a_k-a'|=1.95e-03  J_l(X_k)=15.1851
  k=12 |a_k-a'|=1.22e-04  J_l(X_k)=12.4097
  k=16 |a_k-a'|=7.63e-06  J_l(X_k)=9.6369
  k=20 |a_k-a'|=4.77e-07  J_l(X_k)=6.8643
  k=24 |a_k-a'|=2.98e-08  J_l(X_k)=4.0920
== (F) CONTROL 3: a' NOT in supp beta_1 (a'=2.0, beta_1=Unif(unit disk)) ==
  min over a in supp of J_l(log|Z-a|/|Z-a'|) = 0.7565517885919112  (bounded away from 0: no a_k -> a')
MAXRSS_KB=94024 ELAPSED=1.75
```

### Check 2 — the Markov steps (7.1) → (7.2), (7.3), with the paper's normalization m = E_π i, on three explicit n = 1200 configurations
What it shows:
- The signed mean E_π log|U−U′| is 0 to 1e−16 in every configuration, and E(log)₊ = E(log)₋ = C₁/2.
- With the true C₁ = E_π|log|, the pair tail, (7.2) and (7.3) hold at every tested R, z₀ and r.
- CONTROL (fails, as it should): using the bound the mangled paper.txt line would license (C₁ := max(E_π log, 0) = 0) violates the pair tail, (7.2) and (7.3). Clustered config: α(B(z₀, 0.49))² = 0.25 > 1/n. Spread config: 0.918 > 0.00083.
- This is the concrete reason the PDF's absolute value matters.

```python
# Finite check of the Markov steps (7.1) -> (7.2), (7.3) of the #604 preprint, on explicit
# n-point configurations, with the paper's normalization U = e^m Z + b, m = E_pi i = -E_pi log|Z(x)-Z(y)|.
import numpy as np
rng = np.random.default_rng(1604)

def pairlogs(U):
    D = np.abs(U[:, None] - U[None, :])
    iu = ~np.eye(len(U), dtype=bool)
    return np.log(D[iu])                      # all n(n-1) ordered distinct pairs (pi-uniform)

def run(name, Z, signed_control=False):
    n = len(Z)
    m = -pairlogs(Z).mean()                   # m_j = E_pi i_j
    U = np.exp(m) * Z
    L = pairlogs(U)
    C1 = np.abs(L).mean()                     # (7.1): E_pi |log|U(x)-U(y)||
    print(f"[{name}] n={n}  E_pi log|U-U'| = {L.mean():+.2e} (=0 by the choice of m)  "
          f"C1=E|log|={C1:.4f}  E(log)_+={np.maximum(L,0).mean():.4f}  E(log)_-={np.maximum(-L,0).mean():.4f}")
    if signed_control:
        C1 = max(L.mean(), 0.0)              # what the mangled paper.txt line 'E_pi log|U-U'| <= C1' would allow
        print(f"   CONTROL: using signed C1 := max(E log, 0) = {C1:.3g}")
    # (alpha x alpha){|z-z'|>R} <= C1/log R
    D = np.abs(U[:, None] - U[None, :])
    ok_pair = all((D > R).mean() <= C1/np.log(R) + 1e-12 for R in (1.5, 3, 10, 1e3, 1e6))
    R0 = np.exp(2*C1) * 1.0001 if C1 > 0 else 1.0001
    far = (D > R0).mean(axis=1)               # alpha{|z' - z| > R0} for each empirical center z
    zc = U[np.argmin(far)]
    V = U - zc                                # b chosen to move the center to 0
    ok72 = True; worst72 = 0
    for R in 2*R0*np.array([1.01, 2, 10, 1e2, 1e4, 1e8]):
        lhs = (np.abs(V) > R).mean(); rhs = 2*C1/np.log(R/2)
        worst72 = max(worst72, lhs - rhs); ok72 &= lhs <= rhs + 1e-12
    ok73 = True; worst73 = -1; arg = None
    centers = np.concatenate([V[rng.integers(0, n, 200)], (rng.standard_normal(50)+1j*rng.standard_normal(50))])
    for r in (0.49, 0.1, 1e-2, 1e-4, 1e-8, 1e-12):
        for z0 in centers:
            lhs = ((np.abs(V - z0) < r).mean())**2
            rhs = 1.0/n + (C1/np.log(1/(2*r)))
            if lhs - rhs > worst73: worst73, arg = lhs - rhs, (r, lhs, rhs)
            ok73 &= lhs <= rhs + 1e-12
    print(f"   pair tail ok={ok_pair}  (7.2) ok={ok72} (max lhs-rhs={worst72:+.3g})  "
          f"(7.3) ok={ok73} (max lhs-rhs={worst73:+.3g} at r,lhs,rhs={arg})")

n = 1200
# config 1: multi-scale mixture
Z1 = np.concatenate([rng.standard_normal(400)+1j*rng.standard_normal(400),
                     5+0.01*(rng.standard_normal(400)+1j*rng.standard_normal(400)),
                     30*np.exp(2j*np.pi*rng.random(400))])
run("multiscale", Z1)
# config 2: clustered -- half the points inside a disk of radius 1e-9 (all distinct)
Z2 = np.concatenate([1e-9*(rng.random(600)+1j*rng.random(600)), rng.random(600)*2-1+1j*(rng.random(600)*2-1)])
run("clustered", Z2)
run("clustered", Z2, signed_control=True)
# config 3: spread -- 1150 points in unit disk, 50 at radius 1e12
Z3 = np.concatenate([np.sqrt(rng.random(1150))*np.exp(2j*np.pi*rng.random(1150)), 1e12*np.exp(2j*np.pi*rng.random(50))])
run("spread", Z3)
run("spread", Z3, signed_control=True)
```
Output:
```
[multiscale] n=1200  E_pi log|U-U'| = -8.09e-17 (=0 by the choice of m)  C1=E|log|=1.7692  E(log)_+=0.8846  E(log)_-=0.8846
   pair tail ok=True  (7.2) ok=True (max lhs-rhs=+0)  (7.3) ok=True (max lhs-rhs=-0.0665 at r,lhs,rhs=(1e-12, np.float64(6.944444444444446e-07), np.float64(0.06651157847974767)))
[clustered] n=1200  E_pi log|U-U'| = -3.24e-16 (=0 by the choice of m)  C1=E|log|=7.9594  E(log)_+=3.9797  E(log)_-=3.9797
   pair tail ok=True  (7.2) ok=True (max lhs-rhs=+0)  (7.3) ok=True (max lhs-rhs=-0.296 at r,lhs,rhs=(1e-12, np.float64(6.944444444444446e-07), np.float64(0.29630435451153314)))
[clustered] n=1200  E_pi log|U-U'| = -3.24e-16 (=0 by the choice of m)  C1=E|log|=7.9594  E(log)_+=3.9797  E(log)_-=3.9797
   CONTROL: using signed C1 := max(E log, 0) = 0
   pair tail ok=False  (7.2) ok=False (max lhs-rhs=+0.5)  (7.3) ok=False (max lhs-rhs=+0.249 at r,lhs,rhs=(0.49, np.float64(0.25), np.float64(0.0008333333333333334)))
[spread] n=1200  E_pi log|U-U'| = +8.09e-17 (=0 by the choice of m)  C1=E|log|=4.1796  E(log)_+=2.0898  E(log)_-=2.0898
   pair tail ok=True  (7.2) ok=True (max lhs-rhs=+0)  (7.3) ok=True (max lhs-rhs=-0.156 at r,lhs,rhs=(1e-12, np.float64(6.944444444444446e-07), np.float64(0.15599112629186437)))
[spread] n=1200  E_pi log|U-U'| = +8.09e-17 (=0 by the choice of m)  C1=E|log|=4.1796  E(log)_+=2.0898  E(log)_-=2.0898
   CONTROL: using signed C1 := max(E log, 0) = 8.09e-17
   pair tail ok=False  (7.2) ok=False (max lhs-rhs=+0.0417)  (7.3) ok=False (max lhs-rhs=+0.918 at r,lhs,rhs=(0.49, np.float64(0.9184027777777779), np.float64(0.0008333333333373383)))
MAXRSS_KB=92100 ELAPSED=1.05
```

### Check 3 — the prelimit Möbius relation of §7.3 at a NON-REAL embedding
Setup: points on the circle of radius c = 2^{1/3} about x = (c, c²), with coordinates in Q(c). Embedding c ↦ cω, i ↦ i.
- Under this embedding Z₂ ≠ conj(Z₁) (gap 4.18).
- The normalized product (U₁(y)−U₁(x))(U₂(y)−U₂(x)) is constant = e^{m₁+m₂}σ(t) on the fiber, and U₂(y) = Φ(U₁(y)) with Φ built from one fiber edge. Error 5e−16 at both embeddings.
- CONTROL: a point off the circle violates the relation by 0.53.

```python
# §7.3 prelimit claim: on a fiber (fixed source x, fixed squared distance t), after the
# normalization U_j = e^{m_j} Z_j + b_j at ANY complex embedding, U_2(z) = Phi(U_1(z)) with
# Phi(w) = b + t'/(w-a), (a,b,a',b') = (U_1(x),U_2(x),U_1(y),U_2(y)) for one fiber edge (x,y).
# Test at a NON-REAL embedding of Q(2^(1/3), i): c=2^(1/3) -> c*omega, i -> i.
from fractions import Fraction as F
import cmath, math, random
random.seed(7)
c_real = 2**(1/3); omega = cmath.exp(2j*math.pi/3)
sig = lambda c0, c1, c2: c0 + c1*(c_real*omega) + c2*(c_real*omega)**2   # sigma(c0 + c1 c + c2 c^2)
ident = lambda c0, c1, c2: c0 + c1*c_real + c2*c_real**2
def circle_pt(s):  # rational point on unit circle
    s = F(s); return ((1-s*s)/(1+s*s), 2*s/(1+s*s))
# source x = (c, c^2); fiber points y = x + c*(p,q): squared distance c^2 for every y
x = ((0,1,0), (0,0,1))
fiber = [((0,1+p,0), (0,q,1)) for (p,q) in (circle_pt(s) for s in (F(1,3),F(2,5),F(-7,4),F(5,11),F(13,2),F(-1,9)))]
nonfiber = ((0,F(3,2),0), (0,F(1,7),1))      # CONTROL: x + c*(1/2,1/7), not on the circle
for emb_name, emb in (("identity (real)", ident), ("c->c*omega (non-real)", sig)):
    Z1 = lambda P: emb(*map(float,P[0])) + 1j*emb(*map(float,P[1]))
    Z2 = lambda P: emb(*map(float,P[0])) - 1j*emb(*map(float,P[1]))
    m1, m2, b1, b2 = 0.37, -1.2, 0.5-0.25j, -2+1j     # arbitrary normalization
    U1 = lambda P: math.exp(m1)*Z1(P) + b1
    U2 = lambda P: math.exp(m2)*Z2(P) + b2
    conj_gap = abs(Z2(fiber[0]) - Z1(fiber[0]).conjugate())
    a, b = U1(x), U2(x); ap, bp = U1(fiber[0]), U2(fiber[0])
    tp = (ap-a)*(bp-b)
    Phi = lambda w: b + tp/(w-a)
    prods = [(U1(y)-a)*(U2(y)-b) for y in fiber]
    target = math.exp(m1+m2)*(emb(0,1,0)**2)          # e^(m1+m2) * sigma(c)^2 = e^(m1+m2) sigma(t), t = c^2
    print(f"[{emb_name}] |Z2 - conj(Z1)| = {conj_gap:.3f}")
    print("   max |(U1(y)-U1(x))(U2(y)-U2(x)) - e^(m1+m2) sigma(t)| over fiber =", max(abs(p-target) for p in prods))
    print("   max |U2(y) - Phi(U1(y))| over fiber =", max(abs(U2(y)-Phi(U1(y))) for y in fiber))
    print("   CONTROL non-fiber point: |U2(z) - Phi(U1(z))| =", abs(U2(nonfiber)-Phi(U1(nonfiber))))
```
Output:
```
[identity (real)] |Z2 - conj(Z1)| = 0.000
   max |(U1(y)-U1(x))(U2(y)-U2(x)) - e^(m1+m2) sigma(t)| over fiber = 4.335559509131367e-16
   max |U2(y) - Phi(U1(y))| over fiber = 3.1401849173675503e-16
   CONTROL non-fiber point: |U2(z) - Phi(U1(z))| = 0.5324269382668261
[c->c*omega (non-real)] |Z2 - conj(Z1)| = 4.184
   max |(U1(y)-U1(x))(U2(y)-U2(x)) - e^(m1+m2) sigma(t)| over fiber = 7.021666937153402e-16
   max |U2(y) - Phi(U1(y))| over fiber = 4.965068306494546e-16
   CONTROL non-fiber point: |U2(z) - Phi(U1(z))| = 0.5324269382668263
```

## Citation table (§7 scope)

| Cited | Paper's claim | Source (van Gaans, "Probability measures on metric spaces", pub.math.leidenuniv.nl/~gaansowvan/jancol1.pdf, fetched 2026-10-14, 29 pp.; byte-identical to refs/src/vangaans.pdf) | Verdict |
|---|---|---|---|
| [14, Prop. 5.3] | "The space of probability measures on a compact metric space is compact and metrizable for weak convergence" | "Proposition 5.3. If (X, d) is a compact metric space, then (P(X), d_P) is a compact metric space." | MATCH (together with Thm 4.2) |
| [14, Thm 4.2] | (same sentence: metrizability) | "Theorem 4.2. If (X, d) is a separable metric space, then for any µ, µ1, µ2, … ∈ P(X) one has µi ⇒ µ if and only if d_P(µi, µ) → 0." | MATCH |
| [14, Thm 3.2] | "the open-set inequality in the Portmanteau theorem" | "Theorem 3.2 … The following statements are equivalent: (a) µi ⇒ µ … (d) lim inf_{i→∞} µi(U) ≥ µ(U) for all open U ⊂ X" | MATCH |

Internal references used by §7 (not re-verified here): (2.2), (2.3)/(5.8), (3.4), (3.5), (3.7), Lemma 5.1. Each is used exactly as stated at its source location.

## Summary
§7 holds as read. I checked T_v, V_v, the place selection, the O(1) bound, the normalization, (7.1)–(7.3), Riemann-sphere compactness and Portmanteau, (7.4)–(7.5) including N(R,ε), the transformed occurrence and the order of limits, the incoming-law extension, the joint limit Q, domination, the a.s. finiteness, separation and support statements, independence of a from the pair (a′,b′), the Möbius identity (7.6) and its closed-graph passage to the limit, Lemma 7.1 with (7.7), (7.8), measurability, Fubini, the choice of l and a_k → a′, and the closing dichotomy. All of it checks line by line given the upstream inputs. (7.1) carries the absolute value in the PDF, and that is essential, because the normalization makes the signed mean identically zero. Seven objections, all COSMETIC or wording-level, plus two verification notes.
