# Referee report — seat `palettes` — §5 (Circle palettes and their cardinality) and §6 (Transitions and local finiteness of cyclic centres)

Paper: OpenAI, "The Euclidean plane is not five-colorable" (23 Sep 2026), /tmp/oaimath/158/paper/paper.pdf.
Scope read from the rendered PDF, pp. 26–42 (PDF page = printed page), plus §1.1 pp. 3–4 and Lemma 4.3 (p. 25), which §5–6 invoke constantly.
All quotations below are transcribed from the PDF renderings, not from the mangled text files.

## Verdict for this scope

**HOLDS AS READ.** Every lemma, proposition, corollary, remark and theorem in §5 and §6 was checked step by step and no FATAL or GAP
objection was found. The four objections below are COSMETIC or UNCLEAR (exposition only). Four finite checks were run (scripts and outputs
verbatim at the end), each with a control that fails as intended. Lemma 5.5's asymptotic expansions, the sixty-degree identity, the
circle-measure Fourier decay and estimate (6.3), the Lemma 6.4 constants, the four-cycle velocity formula and the five-cycle support-list
combinatorics all reproduce. Each control fails in the direction it should.

The architecture of §5–6 is careful about quantifiers. The deliberate devices are:
- countable generating trace families (p. 27);
- statements made at one or two FIXED centres at a time (Remark 5.3);
- closed essential supports, which are canonical sets with no null-set ambiguity, in place of a.e. statements wherever a sequence of
  centres is involved (§6.3);
- a final reduction to a finite combinatorial contradiction at two fixed directions (§6.3.4).

I found no place where an uncountable union of null sets is taken, and no limit that ignores a subsequence fixed earlier.

## Objections (numbered)

**O1 — COSMETIC (exposition). Lemma 5.5, pp. 30 and 32.**
"Their angular difference is twice an angle strictly between zero and π/2, and stays away from both parallel cases for sufficiently small d."
And: "Choose once and for all 0 < L ≤ min{c0/C0, π/4}".
- The first claim holds for every d < 1/2, not only for small d. Since |d+e^{it}| ∈ (1/2, 3/2), the difference 2 arccos(|d+e^{it}|/2) lies in
  (1.445, 2.636). Numerically, the minimum of |sin(α₊−α₋)| is 0.656 at d = 0.3 (check 2).
- The constraint L ≤ π/4 is never used. The enlarging step needs C0·L ≤ c0, and the extension step needs C0·d < L.
- Both points are harmless. Fix: delete "for sufficiently small d" and "π/4".

**O2 — COSMETIC (statement vs formalization). Lemma 5.5, p. 30.**
"There is an absolute constant δ* > 0 such that, for every fixed pair of labels, any two distinct centers binary for that pair are at distance at least δ*."
- The proof does deliver an absolute constant. c0, C0 and d1 come from colouring-free Taylor expansions of explicit maps. Numerically, for
  d ≤ 0.08 one may take c0 = 0.99 and C0 = 1.3 (check 2), which gives δ* = 0.08 under the paper's formula.
- The Lean counterpart `binary_centers_separated` (BinaryPalettes.lean l.123) states `∃ δ > 0, ∀ x z i j, …` with the colouring c already
  fixed. That is weaker, although its proof draws δ from the colouring-free lemmas `binary_dynamics_controls` and
  `binary_alternating_invariant_false`.
- No consequence follows. Downstream, Prop 5.6 and the triangle case of Theorem 6.5 use only separation for one fixed colouring.

**O3 — UNCLEAR (exposition, not proof). Lemma 6.4, p. 37.**
"At a fixed center, there is no measurable state function with only the two values X, D, representing respectively a singleton {X} and a
fixed disjoint pair D, and changing state under R almost everywhere."
- §6.2 (p. 36) defines only a *state*: "a measurable angular set together with a specified nonempty group of labels contained in P_x(e)
  almost everywhere on that set". "State function" is never defined.
- The intended meaning, and the only one the proof uses, is a measurable w : S → {X, D} such that:
  - X ∈ P_x(e) a.e. on {w = X};
  - D ⊂ P_x(e) a.e. on {w = D};
  - w(Re) ≠ w(e) a.e.
- With that reading the proof is correct. It needs only that 2κ preserves the state and 3κ = π flips it, together with the γ-equality set.
- The application on p. 38 ("If either were null, the other and X would give the impossible alternation of Lemma 6.4") supplies exactly
  these hypotheses through the canonical w_x and (5.7).
- Fix: one defining sentence.

**O4 — COSMETIC (notation). Throughout pp. 26–42.**
Symbols are heavily overloaded:
- L is the constant of Lemma 5.5 (p. 32) and also the four-cycle locus (p. 38: "Let L be its closed locus"). That locus is not the cyclic
  locus ℒ of (6.4).
- D is used for D_{x,i} (p. 27), D_ij(B,h) (p. 34), the pair D of Lemma 6.4, the diagonals D_i (p. 40) and D_dist (p. 33).
- H is used for H_i (p. 26), H = α₊∘α₋⁻¹ (p. 30) and the limit direction H ∈ S (p. 39).
- S is used for the circle, the operator 𝒮 (p. 35), the supports S_i, the lists S(a) and S_{U,x}.

Each use is locally unambiguous. However, statements such as Lemma 6.6, "continuous from L into L¹(S)", force the reader to resolve L
from context (here L is the four-cycle locus). Fix: rename.

No other objections. In particular I looked for, and did not find:
- a "conditional expectation preserves positivity" step or an ergodicity assumption anywhere in §5–6 (neither occurs);
- a weak-* limit multiplied by another weak-* limit (p. 28 explicitly avoids this: "this passage used a strongly convergent factor
  against a weak-* limit, not a product of two weak-* limits");
- a compactness claim on a non-compact space. W_x sits in the norm-closed unit ball of L^∞ = (L¹)*, which is weak-* compact and
  metrizable because L¹(S) is separable. Essential supports are closed subsets of S.

## Line-by-line status

| Item (page) | Status | Notes |
|---|---|---|
| §5.1 set-up: typical points, H_i, typical circle samplings (p. 26) | VERIFIED LINE BY LINE | "For each fixed r … for almost every y by Fubini and translation invariance; for each fixed y … for almost every r > 0 by polar coordinates" — correct. |
| Definition 5.1, compactness/countability paragraph, closure (5.1) (pp. 26–27) | VERIFIED LINE BY LINE | Diagonal choice in the metrizable bounded-ball weak-* topology is correct. The countable generating family (sup M_i of finite unions) is correct. "Every individual trace has its positive coordinates in the palette almost everywhere" and nonemptiness of P_x(e) a.e. are correct. |
| Lemma 5.2(1), (5.4), (5.5) (pp. 27–28) | VERIFIED LINE BY LINE | Jacobian r_n·\|sin(arg v − arg e)\|. Multiplicity ≤ 2 (two circles meet in ≤ 2 points; coincidence only at y_n = z, r_n = 1, v = −e, which is discarded). Pushforward density ≤ C/δ uniformly in n. The L¹ continuity argument is correct. The weak-*/strong pairing gives ∫ b_i(e)·a_i(x+e+v) = 0. Countable family plus symmetry e ↔ v gives (5.2). |
| Lemma 5.2(2) (p. 28) | VERIFIED LINE BY LINE | Holds for EVERY nonparallel v (no exceptional v). The local inverse branch maps B(x+e+v,h) into an O(h)×O(h) box. (5.2) puts A_i, mod null sets, inside the image of ([e±Ch]∖D_{x,i}) × [v±Ch], so the area is o(h)·O(h) = o(h²). |
| Lemma 5.2(3), (5.6) (p. 29) | VERIFIED LINE BY LINE | The inverse branch applied to z_n + r_n·f − x gives s_n → s, t_n → t in C¹. (5.6) holds by continuous approximation plus bounded inverse derivatives. Density-one points of D_i pull back to conull sets. Assertion 2 at x + s_n(f) + t_n(f) = z_n + r_n·f, typicality and Lemma 4.3 give a_i(z_n + r_n f)·1_{D_i}(s_n f) = 0. Then strong(5.6)/weak-* gives b_i(f)·1_{D_i}(s(f)) = 0. |
| Remark 5.3 (p. 29) | VERIFIED | t may be constant. (x+a)+f = x+f+a is admissible off f = ±a (inverse branch near (f, a)). |
| Corollary 5.4 (p. 29) | VERIFIED + numerics | Rf + R⁻¹f = 2cos(π/3)·f = f. Endpoints are 120° apart. x+f and x+Rf are a unit pair (check 1). |
| §5.3 binary centres, (5.8) (p. 30) | VERIFIED | (5.7) forces two disjoint nonempty subsets of a 2-set, i.e. the two singletons. Translation by κ swaps {s=1} and {s=−1}, so each has measure π. |
| Lemma 5.5 representation, α±, H-invariance, F, F_j (pp. 30–31) | VERIFIED LINE BY LINE + numerics | e^{iα₊} + e^{iα₋} = 2cos(arccos(\|w\|/2))·e^{iΘ} = w (residual 2e−15, check 2). s_x(α₊) = s_x(α₋) = −s_y. s_x(F_j) = (−1)^{2j}·s_x. |
| (5.9) expansion (p. 31) | VERIFIED to first order by hand; C⁰ remainder numerically | arccos′(1/2) = −2/√3 gives α± = t ± κ − d·sin t ∓ (d/√3)·cos t. The composition gives t − (2d/√3)·cos(t+κ) = t + (2d/√3)·sin(t − π/6). Numerically, max\|F − t − (2d/√3)·sin(t−π/6)\|/d² = 0.70–0.72 for d = 0.08…0.005 (bounded). The control (cos instead of sin) grows like 1.63/d. The C² part of the O_{C²}(d²) claim was checked only numerically (\|F_j″\|/d ≤ 1.30). |
| (5.10) six-map bounds (p. 31) | VERIFIED + numerics | Six phases spaced π/3 give max sine and max cosine ≥ √3/2. Numerically min_t max_j (F_j − t)/d = 1.000 and min_t max_j (F_j′ − 1)/d ≥ 1.0017. |
| Enlarging with bounded distortion, (5.11) (pp. 32–33) | VERIFIED LINE BY LINE | F′ ≥ 1 + c0·d − ½·C0·d·ℓ_r ≥ 1 + c0·d/2 since C0·L ≤ c0. The geometric-sum bound Σℓ_r ≤ ℓ_N/(λ−1) gives osc log G′ ≤ 4C0(1+C0·d)L/c0 ≤ 6C0·L/c0. The ratio inequality and the limit interval J = [a,b] are correct. |
| Extending a conull interval (p. 33) | VERIFIED | F_j(a) ≤ a + C0·d < a + L ≤ b, so the union is [a, F_j(b)]. The right endpoint advances by ≥ c0·d, and periodicity contradicts measure π. |
| Proposition 5.6 (pp. 33–34) | VERIFIED LINE BY LINE | Triple 𝒜 on a positive-measure B. (5.2) plus Fubini: each circle about x+e uses only the complementary PAIR. (x+e, 1) is typical for a.e. e. The constant-sequence trace makes x+e binary for that fixed pair. Infinitely many binary centres on a compact circle contradict Lemma 5.5. Each centre x+e is treated separately, so no uncountable union of null sets is needed. |
| §6 intro, D_ij, Definition 6.1, closedness of edge loci, ij ∈ Γ_x ⇒ x ∈ H_i ∩ H_j (p. 34–35) | VERIFIED | A positive-area transition set T₁ ∪ T₂ gives positive area of both colours: T₁ ⊂ A_i and T₁ + h ⊂ A_j. |
| Lemma 6.2, (6.3), circle Fourier decay (pp. 35–36) | VERIFIED LINE BY LINE + numerics | \|σ̂(ξ)\| = \|J0(\|ξ\|)\| ≤ C(1+\|ξ\|)^{−1/2}. The integration-by-parts sketch is correct. The multiplier min(h²ξ²,4)/((1+ξ)h) ≤ 2. Dominated convergence gives o(\|h\|). The transition-mass identity S(a_t − a_t(·+h))(q) = mass of t on the first circle is correct. Cauchy–Schwarz gives average o(1). Choice order B_m, then h_m, then q_m. |
| §6.2 states, essential support (p. 36) | VERIFIED | — |
| Lemma 6.3 (three assertions) (pp. 36–37) | VERIFIED LINE BY LINE | Four labels at density zero (Lemma 5.2(2) both ways) give X at density one. IFT: d/dθ\|w + a − c\|² at c = a equals −2w·Ja ≠ 0 off w ∥ a. 1_{A_n}∘c_n → 1_A gives a positive-measure set of good a. Two density-one points of X at distance \|w_n + a − c_n(a)\| = 1 contradict Lemma 4.3. |
| Lemma 6.4 (p. 37) | VERIFIED LINE BY LINE + exact constants | cos γ = 5/6. 2cos γ = 5/3 is not an integer, so γ/π is irrational. 2γ-invariance plus ergodicity of the irrational rotation contradicts the κ-flip. z_j = x + e^{i(t+2jκ)}(1 − e^{iγ}) form a unit equilateral triangle. The remaining two labels cannot colour it (O3 is about wording only). |
| Theorem 6.5: closedness, finitely many cycles, triangle case (pp. 37–38) | VERIFIED | Any palette of size ≤ 2 inside a triangle lies in a triangle edge, which is forbidden by (6.2). So the palette meets the outside pair, x is binary for that pair, and Lemma 5.5 applies (check 4a). |
| §6.3.1 four-cycle canonical state, w_x(e) ≠ w_x(Re), both diagonals positive (p. 38) | VERIFIED + check 4a | — |
| Lemma 6.6 and (6.5) (p. 38) | VERIFIED LINE BY LINE | The case analysis for the dominating trace is correct. The closed-graph property (5.1) puts limit traces in W_x. Prop 5.6 forbids two positive f_s. Weak-* convergence of indicators to an indicator implies L¹ convergence. |
| Supports N_x, strict margins, lower semicontinuity of supports, N_x ≠ S, gap length ≤ κ (p. 39) | VERIFIED | Uniform margins use Lemma 6.3(iii) with 1_{A_n} = 1_{w_{y_n} = U} → 1_{w_x = U}, which has positive measure. |
| §6.3.2 support transport rule and accumulation contradiction (pp. 39–40) | VERIFIED LINE BY LINE + numerics | V_H(a;b) = −H·b/(a×b) = −H·Ja − (H·a)·cot(β − α) (finite-difference error 5e−9; sign-flipped control 9.66). The reverse transport gives arg a + δ_n(V_H(a;b) − V_H(a;b′)) + o(δ_n), inside the gap. The τ-expansion justifies o(δ_n) without a rate for b′_n. Forcing c_n ∈ S_{V,y_n} and Ra ∈ S_{V,x} contradicts the uniform margin. Every gap endpoint then has H·a = 0, and two antipodal points cannot bound a gap of length ≤ κ < π. |
| §6.3.3 five-cycle diagonals, (6.6), S(a) ∩ S(Ra) = ∅, adjacency in S(R^{±1}a) (pp. 40–41) | VERIFIED + check 4a | — |
| Lemma 6.7 (p. 41) | VERIFIED LINE BY LINE | Traces at z = x + a avoid D_i and D_{i+1}. (5.3) via Remark 5.3 gives P_z(f) ∩ P_x(f) = ∅. The unique outside label X = i+4 is forced into P_z(f) and P_z(Rf), contradicting (5.7) at z. |
| §6.3.4 accumulation for five-cycles (pp. 41–42) | VERIFIED LINE BY LINE + brute force | a_n^± are unit vectors summing to h_n. The no-common-label claim plus (5.2) gives A_k null near y_n, contradicting y_n ∈ H_k. Upper semicontinuity of the lists passes this to ±a. The C5 combinatorics (2, 4 forced; j ∈ {1,4}; Lemma 6.7 bans null the shared state) give no solution over all 31⁶ assignments. Without the bans, 40 (S⁰, S³) pairs extend (check 4b). |
| Lemma 4.3 (p. 25; out of scope, used throughout) | READ, proof correct | The density of x′ + u′ is ≤ 1/(πh²) on B(y, 2h), so P(miss) ≤ 4\|B(y,2h)∖A_i\|/\|B(y,2h)\| = o(1). |

## Test (B) — where FIVE enters in §5–6, and what breaks at SIX

k-independent parts (they hold verbatim for any k):
- Definition 5.1, Lemma 5.2, Remark 5.3, Corollary 5.4, §5.3, Lemma 5.5, Definition 6.1, Lemma 6.2.
- The Lean agrees: `palette_sixty_disjoint`, `binary_centers_separated` and `transition_avoiding_trace` are stated for `Fin k`.
- "for all five labels" in Def 5.1 and the proof of Lemma 5.2 is notational only.

Load-bearing uses of five:
1. **Prop 5.6, p. 34: 5 − 3 = 2.** A palette triple leaves the complementary PAIR, which makes x+e binary so that Lemma 5.5 applies.
   - With k labels the same argument proves |P_x(e)| ≤ k − 3 (a (k−2)-subset leaves a pair). That is ≤ 2 exactly when k ≤ 5.
   - At **six** it gives only |P_x(e)| ≤ 3. A triple in the palette leaves a complementary triple, and "ternary centres" have no analogue of
     (5.8): disjoint nonempty subsets of a 3-set need not be singletons. Lean: `palette_triple_null` is stated for `Fin 5` with
     `(univ \ S).card = 2`.
2. **Lemma 6.3, p. 36: union of the two state groups = I ∖ {X}.** Only then do the four excluded labels force a SINGLE colour to density one,
   so that properness of density-one points (Lemma 4.3) bites. With six labels, two disjoint diagonals leave two labels and no contradiction
   follows.
3. **Lemma 6.4, p. 37: 5 − |{X} ∪ D| = 2 remaining labels** cannot colour a unit equilateral triangle. With six labels three remain, and they
   can.
4. **Theorem 6.5, triangle (p. 38): 5 − 3 = 2 outside labels, hence binary.** At six the outside set is a triple. Check 4d confirms that the
   admissible palettes of size ≤ 2 do not all meet any one fixed pair.
5. **Four-cycle (p. 38): exactly one "fifth label X".** The classification "contains X or is exactly a diagonal" needs both |P| ≤ 2 and a
   single outside label.
6. **Five-cycle (pp. 40–42):** every label lies on the cycle, so palettes are exactly the 5 diagonals. D_i ∩ D_j = ∅ ⇔ j = i ± 1. Lemma 6.7's
   unique outside label is 5 − 4 = 1. The C5 index combinatorics hold (check 4a/4b).
7. "There are only finitely many simple cycles on five labels" (p. 37): lengths 3, 4, 5 only.

Conclusion for (B): the arithmetic is tight at five. The first step to fail at six is Proposition 5.6, and Lemmas 6.3 and 6.4 and the
triangle/four-cycle classifications fail with it. Nothing here suggests a bigger theorem has been left on the table.

At four labels, the same Prop 5.6 argument gives |P| ≤ 1, and (5.7) then makes §6 vacuous. That is consistent with Falconer.

## Test (F) — quantifier audit in scope

- **Exceptional sets.**
  - Def 5.1: depend on x (stated, p. 27).
  - Lemma 5.2: "Each assertion permits an exceptional angular set depending on the fixed centers and on the specified maps" (p. 28). There
    is NO exceptional set in assertion 2: it holds for every nonparallel v once e is a density-one point.
  - Cor 5.4 and Prop 5.6: depend on x (stated). Prop 5.6 uses uncountably many centres x+e, but only through the per-centre property
    "binary", then Lemma 5.5 pairwise. No common null set over uncountably many centres is ever needed (Remark 5.3, p. 29: "never needs a
    common exceptional angular set over an uncountable family of centers"). I confirmed this holds in every use.
- **Limits.**
  - Every trace is a weak-* limit along a sequence chosen first. Subsequences are taken only in compact metrizable spaces: the weak-* ball,
    S, and the support sets.
  - Lemma 6.2's order (B_m, then c_{B_m}, then h_m, then q_m) is correct.
  - Lemma 6.3's order (failing subsequence, then b, d, w, then I, then IFT, then n large, then a) is correct.
  - Lemma 6.6's "every subsequence has a further subsequence with the same limit" is correct.
  - §6.3.2 fixes H by a subsequence before choosing a, b, b′, and the τ-expansion handles b′_n → b′ with no rate.
- **"Connected"** is used once, for the circle (p. 39), which is connected.
- **"Compact"** is used for W_x (closed in the weak-* compact ball) and for essential supports (closed in S).
- **"Closed locally finite" (Thm 6.5):** closed as a finite union of finite intersections of closed edge loci, and each specified-cycle
  locus has no accumulation point in itself. Hence it has finite intersection with compact sets.
- **Lemma 7.2 hypotheses:** not in scope (§7 seat).

## Test (A) — cross-seat note (not in this scope)

The decay of the Fourier transform of circle measure appears in the paper only in §1.1 (p. 4) and in Lemma 6.2 (p. 35). A grep for
`decay`, `(1+|ξ|)^{-1/2}`, `circle measure` and `Bessel` finds nothing else. That use is POST-transfer. So the Fourier decay of circle measure
**cannot** be the ingredient that distinguishes F(i) from Payne's ℚ(i) graph in §2–4. The (A) seats should look elsewhere: divisibility of
K, or the algebraic-radius density in Lemmas 3.4–3.5.

Nothing in §5–6 uses any arithmetic of F(i). These sections work only with the weak measurable condition, which already integrates over all
unit directions.

## Citation table (scope)

| Cited result | Paper's claim | Source (fetched arXiv:0806.1974v1, the only version, PDF → pdftotext) | Verdict |
|---|---|---|---|
| Deroin–Kleptsyn–Navas [6, Section 2.1], cited at p. 32 | "This is an adaptation of Sullivan's expanding-action and bounded-distortion strategy; see Deroin–Kleptsyn–Navas [6, Section 2.1]. The argument below replaces the usual minimality step by explicit small-displacement overlap propagation when extending the conull interval." | §2.1 "Minimality, ergodicity, and exceptional minimal sets", p. 12: "To show the ergodicity one then would like to apply the exponential expansion strategy. This classical procedure consists on expanding very small intervals which concentrate a good proportion of some invariant set, in such a way that the distortion … of the compositions remains controlled. … If one can expand this interval keeping a uniform bound for the distortion, then each one of the 'expanded' intervals also has a proportion of points in A very close to 1. … If the action is minimal, this implies that A is a subset of full measure in the circle." The introduction (l.105) attributes the strategy as "largely going back to D. Sullivan". | **MATCH.** Attribution only, not load-bearing: the paper's argument (pp. 32–33) is self-contained, and it correctly replaces the minimality step. |

No other citation occurs in pp. 26–42. Lemma 4.3 (cites Falconer [8], Payne [22]) is outside this scope.

## Finite checks

Box etiquette:
- Scripts are in /tmp/oaimath/158/seats/palettes_checks/; the fetched source is in /tmp/oaimath/158/seats/palettes_src/.
- Each run used `nice -n 10` and `ulimit -v 3000000` (an earlier run under 1.5 GB virtual failed with an OpenBLAS virtual reservation), with
  OPENBLAS_NUM_THREADS=1.
- Maximum RSS was 190 MB. Wall times were 13.1 s, 4.4 s, 30.1 s and 0.5 s.
- No lean or lake was run.

What each check tests and how its control fails:
- **Check 1** — sixty-degree identity and empirical palettes of the Hadwiger hexagon colouring (r = 2/5), plus the Lemma 6.4 constants.
  - Proper colouring: P(f) ∩ P(Rf) ≠ ∅ on 0 of 163,840 angles at both ε.
  - **CONTROL** (improper hexagons, r = 0.6): 4.19% and 2.85% of angles. These do not shrink to 0 as ε → 0.
  - **CONTROL** κ = 50°: the identity fails (0.29) and the unit distance fails (0.155).
- **Check 2** — Lemma 5.5 representation and expansions.
  - **CONTROL** arcsin in place of arccos breaks the representation (residual 0.89–1.17).
  - **CONTROL** a cos-phase leading term: residual/d² grows like 1/d.
- **Check 3** — circle Fourier decay and (6.3).
  - **CONTROL** decay exponent 1: unbounded (8 → 357).
  - **CONTROL** no circle decay in the multiplier: unbounded (4/h).
  - **CONTROL** no circle average: ‖g − g(·+h)‖/√h → √(4ρ0) = 2.449, not 0.
  - Positive controls: the Fourier formula reproduces the exact lens symmetric-difference area to 2e−5, and a real-space grid reproduces
    the S-version at h = 0.1 (0.025284 vs 0.025283).
- **Check 4** — palette classifications, five-cycle support-list brute force, V_H formula, six-label arithmetic.
  - **CONTROL** removing the Lemma 6.7 bans gives 40 solutions.
  - **CONTROL** the sign-flipped V_H is off by 9.66.


### check1_sixty_hex.py (md5 1aecd67471592ef4d686a55238eda3a8)

```python
# Check 1: sixty-degree exclusion (Cor 5.4) geometry + empirical palettes of hexagonal colourings,
# and the constants of Lemma 6.4.  Control: a non-60-degree rotation and an IMPROPER hexagon colouring.
import numpy as np, sys
from fractions import Fraction
rng = np.random.default_rng(1)

def rot(th): return np.exp(1j*th)
# (a) identity used in Cor 5.4:  f = R f + R^{-1} f, |Rf - f| = 1, endpoints nonparallel
for name, th in [("kappa=pi/3 (paper)", np.pi/3), ("CONTROL kappa=50deg", np.deg2rad(50))]:
    f = rot(rng.uniform(0, 2*np.pi, 1000))
    res = np.max(np.abs(rot(th)*f + rot(-th)*f - f))
    unit = np.max(np.abs(np.abs(rot(th)*f - f) - 1))
    nonpar = abs(np.sin(2*th))          # sin of angle between Rf and R^{-1}f
    print(f"{name}: max|Rf+R^-1f-f|={res:.2e}  max||Rf-f|-1|={unit:.2e}  |sin(angle(Rf,R^-1f))|={nonpar:.3f}")

# (b) empirical palettes for the Hadwiger hexagon colouring: Voronoi cells of the triangular lattice
#     with spacing sqrt(3) r, colour = (m + 2n) mod 7  (Z[w]/(2-w) = Z/7, w = e^{2 pi i/3}).
w = np.exp(2j*np.pi/3)
def colour(z, r):
    a = np.sqrt(3)*r
    # lattice coordinates z = a(m + n w)
    n = (z.imag/a)/np.sin(2*np.pi/3); m = z.real/a - n*np.cos(2*np.pi/3)
    m0, n0 = np.floor(m), np.floor(n)
    best = None; bestd = None
    for dm in (-1, 0, 1, 2):
        for dn in (-1, 0, 1, 2):
            mm, nn = m0+dm, n0+dn
            d = np.abs(z - a*(mm + nn*w))
            if best is None:
                best = (mm + 2*nn) % 7; bestd = d
            else:
                upd = d < bestd
                best = np.where(upd, (mm + 2*nn) % 7, best); bestd = np.where(upd, d, bestd)
    return best.astype(int)

def palettes(x, angles, r, eps, K=12):
    # colours of points within eps of x+e^{i t}: sample centre + K points on circles eps, eps/2
    pts = [x + rot(angles)]
    for rad in (eps, eps/2):
        for k in range(K):
            pts.append(x + rot(angles) + rad*rot(2*np.pi*k/K + 0.1))
    cols = np.stack([colour(p, r) for p in pts])          # (samples, angles)
    M = np.zeros((7, len(angles)), bool)
    for c in range(7): M[c] = (cols == c).any(axis=0)
    return M

T = 4096
ang = 2*np.pi*np.arange(T)/T
shift = T//6                       # R = rotation by 60 deg = T/6 grid steps
for r, label in [(0.4, "proper  r=2/5"), (0.6, "CONTROL r=0.6 (hexagon diameter 1.2>1, improper)")]:
    for eps in (1e-2, 1e-3):
        viol = 0; big = 0; tot = 0
        for _ in range(40):
            x = complex(*rng.uniform(-5, 5, 2))
            M = palettes(x, ang, r, eps)
            MR = np.roll(M, -shift, axis=1)             # palette at R f
            viol += (M & MR).any(axis=0).sum()
            big  += (M.sum(axis=0) >= 3).sum()
            tot += T
        print(f"{label} eps={eps:g}: frac f with P(f)∩P(Rf)≠∅ = {viol/tot:.5f};  frac |P(f)|>=3 = {big/tot:.5f}")

# (c) Lemma 6.4 constants, exact
cosg = Fraction(5, 6)
print("Lemma 6.4: 1-2*sin^2(g/2) with sin(g/2)=1/(2sqrt3):", 1 - 2*Fraction(1, 12), "== 5/6:", 1-2*Fraction(1,12) == cosg)
print("|1-e^{ig}|^2 = 2-2cos g =", 2-2*cosg, "(need 1/3);  triangle side^2 = 3*(1/3) =", 3*(2-2*cosg))
print("2cos g =", 2*cosg, "not an integer -> g/pi irrational (Niven-type argument)")
g = np.arccos(5/6)
for t in rng.uniform(0, 2*np.pi, 3):
    z = [rot(t + 2*j*np.pi/3)*(1 - rot(g)) for j in range(3)]
    print("  side lengths:", [round(abs(z[i]-z[(i+1)%3]), 12) for i in range(3)], " |sin(pi+g)|=", round(abs(np.sin(np.pi+g)), 4))
```

Output:

```
kappa=pi/3 (paper): max|Rf+R^-1f-f|=3.46e-16  max||Rf-f|-1|=3.33e-16  |sin(angle(Rf,R^-1f))|=0.866
CONTROL kappa=50deg: max|Rf+R^-1f-f|=2.86e-01  max||Rf-f|-1|=1.55e-01  |sin(angle(Rf,R^-1f))|=0.985
proper  r=2/5 eps=0.01: frac f with P(f)∩P(Rf)≠∅ = 0.00000;  frac |P(f)|>=3 = 0.00146
proper  r=2/5 eps=0.001: frac f with P(f)∩P(Rf)≠∅ = 0.00000;  frac |P(f)|>=3 = 0.00001
CONTROL r=0.6 (hexagon diameter 1.2>1, improper) eps=0.01: frac f with P(f)∩P(Rf)≠∅ = 0.04190;  frac |P(f)|>=3 = 0.00078
CONTROL r=0.6 (hexagon diameter 1.2>1, improper) eps=0.001: frac f with P(f)∩P(Rf)≠∅ = 0.02849;  frac |P(f)|>=3 = 0.00000
Lemma 6.4: 1-2*sin^2(g/2) with sin(g/2)=1/(2sqrt3): 5/6 == 5/6: True
|1-e^{ig}|^2 = 2-2cos g = 1/3 (need 1/3);  triangle side^2 = 3*(1/3) = 1
2cos g = 5/3 not an integer -> g/pi irrational (Niven-type argument)
  side lengths: [np.float64(1.0), np.float64(1.0), np.float64(1.0)]  |sin(pi+g)|= 0.5528
  side lengths: [np.float64(1.0), np.float64(1.0), np.float64(1.0)]  |sin(pi+g)|= 0.5528
  side lengths: [np.float64(1.0), np.float64(1.0), np.float64(1.0)]  |sin(pi+g)|= 0.5528
[wall 13.06 s, maxRSS 38028 kB]
```

### check2_binary_expansion.py (md5 5113534b405b127b27045c983bbf16b8)

```python
# Check 2: Lemma 5.5 (binary-centre separation) -- exact representation y+e^{it} = x+e^{i a+}+e^{i a-},
# the expansion (5.9) of F = a+ o a-^{-1} - 2kappa, and the six-map bounds (5.10).
# Controls: (i) flip the sign of the arccos in a+- (representation must fail);
#           (ii) a WRONG leading term t+(2d/sqrt3)cos(t-pi/6) (residual/d^2 must blow up).
import numpy as np
kap = np.pi/3
N = 200001
t = np.linspace(-4*np.pi, 4*np.pi, 4*N)          # wide range so every F(u - j*kappa) is evaluated by genuine interpolation
def lifts(d, t, sgn=1.0):
    w = d + np.exp(1j*t)
    Th = t + np.imag(np.log(1 + d*np.exp(-1j*t)))
    ac = np.arccos(np.abs(w)/2)
    return Th + sgn*ac, Th - sgn*ac, w
for d in (0.3, 0.1):
    ap, am, w = lifts(d, t)
    res = np.max(np.abs(np.exp(1j*ap) + np.exp(1j*am) - w))
    apb, amb, _ = lifts(d, t, sgn=-1.0); wrongsum = np.exp(1j*apb) + np.exp(1j*amb) - w   # same pair swapped: still fine
    # real control: use arcsin instead of arccos
    Th = t + np.imag(np.log(1 + d*np.exp(-1j*t))); acw = np.arcsin(np.abs(w)/2)
    resc = np.max(np.abs(np.exp(1j*(Th+acw)) + np.exp(1j*(Th-acw)) - w))
    nonpar = np.min(np.abs(np.sin(ap-am)))
    print(f"d={d}: max|e^ia+ + e^ia- - (d+e^it)| = {res:.1e}; CONTROL(arcsin) = {resc:.2f}; min|sin(a+ - a-)| = {nonpar:.3f}; "
          f"min/max a+' = {np.min(np.gradient(ap,t)):.3f}/{np.max(np.gradient(ap,t)):.3f}")

def sixmaps(d):
    ap, am, _ = lifts(d, t)
    # invert a- by monotone interpolation; evaluate F on s in [0, 2pi]
    s = np.linspace(0, 2*np.pi, 20001)
    am_inv = lambda u: np.interp(u, am, t)
    ap_f = lambda u: np.interp(u, t, ap)
    F = lambda u: ap_f(am_inv(u)) - 2*kap
    Fj = [ (lambda u, j=j: j*kap + F(u - j*kap)) for j in range(6) ]
    return s, F, Fj
print("\n d      max|F-t-(2d/v3)sin(t-pi/6)|/d^2   CONTROL cos-version/d^2   min_t max_j (Fj-t)/d   min_t max_j (Fj'-1)/d   max_j|Fj-t|/d  max_j|Fj'-1|/d  max_j|Fj''|/d")
for d in (0.08, 0.04, 0.02, 0.01, 0.005):
    s, F, Fj = sixmaps(d)
    lead = s + 2*d/np.sqrt(3)*np.sin(s - np.pi/6)
    r1 = np.max(np.abs(F(s) - lead))/d**2
    r2 = np.max(np.abs(F(s) - (s + 2*d/np.sqrt(3)*np.cos(s - np.pi/6))))/d**2
    V = np.stack([Fj[j](s) for j in range(6)])
    D1 = np.gradient(V, s, axis=1); D2 = np.gradient(D1, s, axis=1)
    disp = np.min(np.max(V - s, axis=0))/d
    der  = np.min(np.max(D1 - 1, axis=0))/d
    print(f"{d:<6} {r1:>14.4f} {r2:>30.2f} {disp:>22.4f} {der:>22.4f} {np.max(np.abs(V-s))/d:>16.4f} {np.max(np.abs(D1-1))/d:>14.4f} {np.max(np.abs(D2[:,5:-5]))/d:>14.4f}")
print("theory: leading coefficient 2/sqrt3 =", 2/np.sqrt(3), "; six-phase max of sine >= sqrt3/2 gives max_j(Fj-t)/d -> 1, max_j(Fj'-1)/d -> 1")
```

Output:

```
d=0.3: max|e^ia+ + e^ia- - (d+e^it)| = 2.2e-15; CONTROL(arcsin) = 1.17; min|sin(a+ - a-)| = 0.656; min/max a+' = 0.689/1.451
d=0.1: max|e^ia+ + e^ia- - (d+e^it)| = 2.1e-15; CONTROL(arcsin) = 0.89; min|sin(a+ - a-)| = 0.804; min/max a+' = 0.890/1.123

 d      max|F-t-(2d/v3)sin(t-pi/6)|/d^2   CONTROL cos-version/d^2   min_t max_j (Fj-t)/d   min_t max_j (Fj'-1)/d   max_j|Fj-t|/d  max_j|Fj'-1|/d  max_j|Fj''|/d
0.08           0.7197                          20.59                 1.0003                 1.0278           1.1710         1.2165         1.2953
0.04           0.7105                          40.98                 1.0001                 1.0137           1.1626         1.1834         1.2208
0.02           0.7060                          81.80                 1.0000                 1.0068           1.1586         1.1685         1.1872
0.01           0.7038                         163.44                 1.0000                 1.0034           1.1566         1.1615         1.1708
0.005          0.7027                         326.74                 1.0000                 1.0017           1.1557         1.1581         1.1627
theory: leading coefficient 2/sqrt3 = 1.1547005383792517 ; six-phase max of sine >= sqrt3/2 gives max_j(Fj-t)/d -> 1, max_j(Fj'-1)/d -> 1
[wall 4.44 s, maxRSS 190352 kB]
```

### check3_fourier.py (md5 43544500a1ce6298863e0ef947309db8)

```python
# Check 3: the circle-measure Fourier decay used in Lemma 6.2 and the o(sqrt|h|) estimate (6.3).
#  (a) sigma^(r) = (1/2pi) int exp(i r cos t) dt = J0(r); sup_r |J0(r)|(1+r)^{1/2} bounded.  CONTROL: exponent 1 (unbounded).
#  (b) multiplier m_h(xi) = min(h^2 xi^2,4)/((1+xi) h) is uniformly bounded.  CONTROL: no circle decay -> min(h^2xi^2,4)/h.
#  (c) (6.3) for g = indicator of the disk of radius rho0: ||S(g-g(.+h))||_L2/sqrt(h) -> 0;
#      CONTROL without the circle average S: ||g-g(.+h)||_L2/sqrt(h) -> sqrt(4 rho0) (does NOT go to 0).
#      Positive control on the Fourier formula: the no-S value is checked against the exact lens-area formula,
#      and the S-value at h=0.1 is checked against a direct real-space grid computation.
import numpy as np
from scipy.special import j0, j1
# (a)
for r in (0.0, 5.0, 50.0, 500.0):
    tt = np.linspace(0, 2*np.pi, 200001)[:-1]
    q = np.mean(np.exp(1j*r*np.cos(tt))).real
    print(f"quadrature sigma^({r}) = {q:+.10f}   J0 = {j0(r):+.10f}")
r = np.linspace(0, 2e5, 4_000_001)
A = np.abs(j0(r))
print("sup |J0(r)|(1+r)^0.5 on [0,2e5] = %.4f" % np.max(A*np.sqrt(1+r)), "(asymptotic sqrt(2/pi)=%.4f)" % np.sqrt(2/np.pi))
for R in (1e2, 1e3, 1e4, 2e5):
    m = r <= R
    print(f"  CONTROL sup_(r<={R:g}) |J0(r)|(1+r)^1 = {np.max(A[m]*(1+r[m])):.1f}")
del r, A
# (b)
xi = np.logspace(-6, 10, 200001)
for h in (1e-1, 1e-3, 1e-6):
    m = np.minimum(h*h*xi*xi, 4)/((1+xi)*h)
    mc = np.minimum(h*h*xi*xi, 4)/h
    print(f"h={h:g}: sup multiplier = {m.max():.3f};  CONTROL (no decay) sup = {mc.max():.3g}")
# (c)
rho0 = 1.5
def fourier_norm2(h, with_S, K=3e5, dk=0.02):   # neglected tail <= 1/(pi*rho0*K) ~ 7e-7
    tot = 0.0; start = dk/2; block = 1_000_000          # chunked: keeps RSS ~ 50 MB
    while start < K:
        k = start + dk*np.arange(block); k = k[k < K]
        base = (j1(rho0*k))**2 * (1 - j0(h*k)) / k
        if with_S: base = base * j0(k)**2
        tot += base.sum()*dk; start = k[-1] + dk
    return 4*np.pi*rho0**2 * tot
def lens_sym_diff(h):
    lens = 2*rho0**2*np.arccos(h/(2*rho0)) - (h/2)*np.sqrt(4*rho0**2 - h*h)
    return 2*(np.pi*rho0**2 - lens)
print("\n  h       ||g-g(.+h)||^2 Fourier   exact |D Δ (D-h)|   CONTROL ratio ||g-g(.+h)||/sqrt h    ||S(g-g(.+h))||/sqrt h")
for h in (0.1, 0.03, 0.01, 0.003, 0.001):
    n0 = fourier_norm2(h, False); nS = fourier_norm2(h, True)
    print(f"{h:<7} {n0:>16.6f} {lens_sym_diff(h):>20.6f} {np.sqrt(n0/h):>28.4f} {np.sqrt(nS/h):>28.5f}")
print("sqrt(4*rho0) =", np.sqrt(4*rho0))
# real-space cross-check of the S-version at h = 0.1: S g is radial, Sg(q) = 1 - arccos(c)/pi, c = (rho0^2-|q|^2-1)/(2|q|)
def Sg(z):
    rr = np.abs(z); c = np.clip((rho0**2 - rr**2 - 1)/(2*np.maximum(rr, 1e-12)), -1, 1)
    return 1 - np.arccos(c)/np.pi
h = 0.1; dx = 0.0025; tot = 0.0
xs = np.arange(-2.7, 2.7 + dx/2, dx)
for x0 in np.array_split(xs, 20):
    X, Y = np.meshgrid(x0, xs, indexing="ij"); Z = X + 1j*Y
    tot += np.sum((Sg(Z) - Sg(Z + h))**2)*dx*dx
print(f"real-space grid ||S(g-g(.+0.1))||^2 = {tot:.6f}   vs Fourier formula {fourier_norm2(0.1, True):.6f}")
```

Output:

```
quadrature sigma^(0.0) = +1.0000000000   J0 = +1.0000000000
quadrature sigma^(5.0) = -0.1775967713   J0 = -0.1775967713
quadrature sigma^(50.0) = +0.0558123277   J0 = +0.0558123277
quadrature sigma^(500.0) = -0.0341005569   J0 = -0.0341005569
sup |J0(r)|(1+r)^0.5 on [0,2e5] = 1.1536 (asymptotic sqrt(2/pi)=0.7979)
  CONTROL sup_(r<=100) |J0(r)|(1+r)^1 = 8.0
  CONTROL sup_(r<=1000) |J0(r)|(1+r)^1 = 25.3
  CONTROL sup_(r<=10000) |J0(r)|(1+r)^1 = 79.8
  CONTROL sup_(r<=200000) |J0(r)|(1+r)^1 = 356.8
h=0.1: sup multiplier = 1.905;  CONTROL (no decay) sup = 40
h=0.001: sup multiplier = 1.999;  CONTROL (no decay) sup = 4e+03
h=1e-06: sup multiplier = 2.000;  CONTROL (no decay) sup = 4e+06

  h       ||g-g(.+h)||^2 Fourier   exact |D Δ (D-h)|   CONTROL ratio ||g-g(.+h)||/sqrt h    ||S(g-g(.+h))||/sqrt h
0.1             0.599869             0.599889                       2.4492                      0.50283
0.03            0.179977             0.179997                       2.4493                      0.30513
0.01            0.059980             0.060000                       2.4491                      0.19048
0.003           0.017980             0.018000                       2.4481                      0.11229
0.001           0.005980             0.006000                       2.4454                      0.06876
sqrt(4*rho0) = 2.449489742783178
real-space grid ||S(g-g(.+0.1))||^2 = 0.025284   vs Fourier formula 0.025283
[wall 30.09 s, maxRSS 185368 kB]
```

### check4_combinatorics.py (md5 da8a6245b98ec2ef7498aa1db1a0a12d)

```python
# Check 4: the finite combinatorics of Section 6 (Theorem 6.5) and the four-cycle velocity formula.
#  (a) palette classifications used for triangles / four-cycles / five-cycles (all palettes of size 1..2 on 5 labels);
#  (b) five-cycle support-list contradiction (Sec 6.3.4) by brute force over all 31^6 list assignments
#      (via a compatibility-graph search).  CONTROL: drop the Lemma 6.7 step bans -> solutions must appear.
#  (c) V_H(a;b) = -H.Ja - (H.a) cot(arg b - arg a) for the first output angle of T_h (finite differences).
#      CONTROL: the sign-flipped formula.
#  (d) test (B): the same palette arithmetic with SIX labels (what breaks).
import itertools, numpy as np
L = range(5)
pal = [frozenset(p) for k in (1, 2) for p in itertools.combinations(L, k)]
def edges_of_cycle(cyc): return [frozenset((cyc[i], cyc[(i+1) % len(cyc)])) for i in range(len(cyc))]
def admissible(P, cyc): return not any(P <= e for e in edges_of_cycle(cyc))     # (6.2) for each cycle edge
ok = True
for cyc in itertools.permutations(L, 3):
    out = frozenset(L) - set(cyc)
    ok &= all(P & out for P in pal if admissible(P, cyc))
print("(a) triangle: every admissible palette (|P|<=2) meets the outside pair:", ok)
ok = True
for cyc in itertools.permutations(L, 4):
    X = (set(L) - set(cyc)).pop(); U = frozenset((cyc[0], cyc[2])); V = frozenset((cyc[1], cyc[3]))
    ok &= all((X in P) or P == U or P == V for P in pal if admissible(P, cyc))
print("    four-cycle: admissible palette contains X or is exactly a diagonal:", ok)
cyc = (0, 1, 2, 3, 4); D = [frozenset((i, (i+2) % 5)) for i in L]
print("    five-cycle: admissible palettes == the five diagonals:", set(P for P in pal if admissible(P, cyc)) == set(D))
print("    D_i ∩ D_j = ∅  <=>  j = i±1:", all((not (D[i] & D[j])) == ((j-i) % 5 in (1, 4)) for i in L for j in L if i != j))
print("    label outside D_i ∪ D_{i+1} is unique (= i+4):", all(set(L) - D[i] - D[(i+1) % 5] == {(i+4) % 5} for i in L))

# (b) five-cycle support lists.  Lists S^(r), r in Z/6, nonempty subsets of Z/5 (bitmasks 1..31).
subsets = list(range(1, 32))
mem = lambda m: [i for i in L if m >> i & 1]
def nbr_ok(A, B):            # every i in A has an adjacent index in B
    return all((B >> ((i+1) % 5) & 1) or (B >> ((i-1) % 5) & 1) for i in mem(A))
compat = {(A, B): (A & B) == 0 and nbr_ok(A, B) and nbr_ok(B, A) for A in subsets for B in subsets}
def diag_meet_empty(A):
    inter = set(L)
    for i in mem(A): inter &= D[i]
    return len(inter) == 0
def bans(A):                 # Lemma 6.7: i,i+1 both in the list => steps i<->i+1 banned everywhere
    return {frozenset((i, (i+1) % 5)) for i in L if (A >> i & 1) and (A >> ((i+1) % 5) & 1)}
def step_ok(j, banned):      # state j must have an unbanned step j -> j±1 (R maps state j into states j±1)
    return frozenset((j, (j+1) % 5)) not in banned or frozenset((j, (j-1) % 5)) not in banned
def solve(use_bans, bans_on="S0"):
    sols = []
    S0S3 = [(a, b) for a in subsets for b in subsets if diag_meet_empty(a) and diag_meet_empty(b)]
    for S0, S3 in S0S3:
        banned = bans(S0) | bans(S3) if use_bans else set()
        chk = [S0] if bans_on == "S0" else None
        if use_bans and not all(step_ok(j, banned) for j in mem(S0)): continue
        mids1 = [(S1, S2) for S1 in subsets for S2 in subsets if compat[S0, S1] and compat[S1, S2] and compat[S2, S3]]
        mids2 = [(S4, S5) for S4 in subsets for S5 in subsets if compat[S3, S4] and compat[S4, S5] and compat[S5, S0]]
        if mids1 and mids2: sols.append((mem(S0), mem(mids1[0][0]), mem(mids1[0][1]), mem(S3), mem(mids2[0][0]), mem(mids2[0][1])))
    return sols
s_paper = solve(True)
s_ctrl = solve(False)
print("(b) five-cycle lists with constraints of Sec 6.3.4 + Lemma 6.7 bans: #(S0,S3) admitting a full assignment =", len(s_paper))
print("    CONTROL without Lemma 6.7 bans: #(S0,S3) admitting a full assignment =", len(s_ctrl), "; example (S0..S5):", s_ctrl[0] if s_ctrl else None)

# (c) velocity of the first output angle of T_h(a,b): c+d = a+b-h
def first_output(alpha, beta, h):
    w = np.exp(1j*alpha) + np.exp(1j*beta) - h
    Th = np.angle(w); ac = np.arccos(np.abs(w)/2)
    c1, c2 = Th + ac, Th - ac           # pick the branch whose first output is near alpha
    cand = np.array([c1, c2]); k = np.argmin(np.abs(np.angle(np.exp(1j*(cand - alpha)))))
    return alpha + np.angle(np.exp(1j*(cand[k] - alpha)))
rng = np.random.default_rng(7); worst = 0; worst_c = 0
for _ in range(2000):
    al, be, ph = rng.uniform(0, 2*np.pi, 3)
    if abs(np.sin(be - al)) < 0.2: continue
    H = np.exp(1j*ph); a = np.exp(1j*al); b = np.exp(1j*be); Ja = 1j*a
    dot = lambda u, v: (u*np.conj(v)).real
    VH = -dot(H, Ja) - dot(H, a)/np.tan(be - al)
    eps = 1e-6
    num = (first_output(al, be, eps*H) - first_output(al, be, -eps*H))/(2*eps)
    worst = max(worst, abs(num - VH)); worst_c = max(worst_c, abs(num - (dot(H, Ja) + dot(H, a)/np.tan(be - al))))
print(f"(c) max |finite-difference velocity - V_H formula| = {worst:.2e};  CONTROL sign-flipped formula: {worst_c:.2f}")

# (d) test (B): six labels
L6 = range(6)
pal6 = [frozenset(p) for k in (1, 2, 3) for p in itertools.combinations(L6, k)]
tri = (0, 1, 2); out6 = frozenset(L6) - set(tri)
adm = [P for P in pal6 if not any(P <= e for e in edges_of_cycle(tri)) and len(P) <= 2]
print("(d) SIX labels: complement of a palette triple has size", 6-3, "(Prop 5.6 needs 2); triangle outside set has size", len(out6),
      "; admissible |P|<=2 palettes all meet ONE fixed pair?", any(all(P & frozenset(pr) for P in adm) for pr in itertools.combinations(out6, 2)))
```

Output:

```
(a) triangle: every admissible palette (|P|<=2) meets the outside pair: True
    four-cycle: admissible palette contains X or is exactly a diagonal: True
    five-cycle: admissible palettes == the five diagonals: True
    D_i ∩ D_j = ∅  <=>  j = i±1: True
    label outside D_i ∪ D_{i+1} is unique (= i+4): True
(b) five-cycle lists with constraints of Sec 6.3.4 + Lemma 6.7 bans: #(S0,S3) admitting a full assignment = 0
    CONTROL without Lemma 6.7 bans: #(S0,S3) admitting a full assignment = 40 ; example (S0..S5): ([0, 1], [2, 4], [0, 3], [1, 2], [0, 3], [2, 4])
(c) max |finite-difference velocity - V_H formula| = 4.78e-09;  CONTROL sign-flipped formula: 9.66
(d) SIX labels: complement of a palette triple has size 3 (Prop 5.6 needs 2); triangle outside set has size 3 ; admissible |P|<=2 palettes all meet ONE fixed pair? False
[wall 0.50 s, maxRSS 34612 kB]
```

Notes on reading the outputs:
- **Check 1.** The fraction |P(f)| ≥ 3 in the proper colouring (0.00146 → 0.00001 as ε shrinks) comes from hexagon triple points within
  ε of the circle. It is O(ε), as expected. It is not evidence about Prop 5.6, which concerns 5-colourings; the 7-colouring is used only as
  a positive control for the k-independent Corollary 5.4.
- **Check 2.** The columns max_j|F_j − t|/d, max_j|F_j′ − 1|/d and max_j|F_j″|/d tend to 2/√3 ≈ 1.155, as the expansion predicts. So
  C0 ≈ 1.3 suffices for d ≤ 0.08.
- **Check 3.** The S-averaged ratio decays like (h·log(1/h))^{1/2}: 0.503, 0.305, 0.190, 0.112, 0.069. That is the gain the circle
  average buys. Without it the ratio sits at √(4ρ0).
- **Check 4.** In (b), the paper's argument applies the Lemma 6.7 bans only to S⁰ and S³ and requires an unbanned step from each index of
  S⁰. That reproduces the contradiction exactly as written (the paper's j = 1 / j = 4 cases). The control example S⁰ = {0,1}, S³ = {1,2}
  is precisely the paper's j = 1 case, which only the bans kill.

## Summary

§5 and §6 hold as read. I found no FATAL or GAP objection: four COSMETIC/UNCLEAR exposition items (O1–O4), one MATCH citation, and four
finite checks whose controls fail as they should. The arithmetic that makes "five" work is concentrated in Proposition 5.6 (5 − 3 = 2) and
in Lemmas 6.3 and 6.4 and the triangle/four-cycle classifications (one or two leftover labels). It fails at six, so §5–6 leave no larger
theorem unclaimed. The only analytic input that is not elementary geometry is the J0 decay of circle measure in Lemma 6.2, and it is
post-transfer.
