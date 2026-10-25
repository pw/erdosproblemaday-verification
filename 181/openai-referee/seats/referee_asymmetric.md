# Hostile referee report, seat `asymmetric`

Paper: "The hypercube Ramsey number has linear order" (OpenAI, 23 Sept 2026, 172 pp).
Scope: §8 (Asymmetric purity and discrepancy, pp. 69-79: Lemma 8.1, Corollary 8.2), §9 (Intermediate powers of bias, pp. 79-88: Definition 9.1, Proposition 9.2), §1.3 and Figure 1 (pp. 3-6), Appendix A Table 1 rows "Asymmetric purity", "Intermediate sublinear bias", "Intermediate linear bias", and the "Exhaustion and boundary conventions" paragraph (pp. 166-169).
Read from the PDF page images (formulas) plus the plain extraction (verbatim quotes). §2, §3 (Def. 3.1, Lemmas 3.2-3.10), §4 (Lemma 4.1), §7 (Lemma 7.1, Corollary 7.2) were read for the statements I depend on. I did not re-referee their proofs; other seats have those.

## 0. Verdict up front

**HOLDS AS READ** for my scope, at the level of the mathematics. I re-derived every inequality I list as verified in §6 and could not find a sentence where the argument fails. I found no rate requirement on C_n, no parameter cycle, no constant secretly depending on n, and no availability/stabilization misuse.

What is open:
- **UNCLEAR (exposition), Objection 1:** the "adapted height construction" in §9.1 (pp. 81-82) runs Lemma 3.8 outside its stated hypotheses (the radius n^σ is not allowed there, paths cross slices, and the crowd tests are swapped out). The paper gives two paragraphs of sketch. I checked every exponent condition it states and found no failure, but the scale induction itself is not written out, so I **could not check** it line by line.
- Objections 2-5 are wording or bookkeeping slips. None is a mathematical gap.

## 1. Objections

### Objection 1 (UNCLEAR, an exposition gap, not a demonstrated mathematical gap): §9.1 "The adapted height construction", pp. 81-82

Verbatim:
> "We adapt Steps 2–4 of the proof of Lemma 3.8, using paths with step bound 2 in the full cube. The position counts in all eligibility balls are at least n^10/2 with high probability. The hole and crowd probabilities, including the bounded level windows, have the same base estimates as in that proof. The following overlap check permits the paths to cross slices."

> "The base bound, the overlap bound and independence on private regions now give the same scale induction as in Lemma 3.8. This argument uses the three displayed crowd tests; it does not require the original lemma's full-cube radius-(r + 2) crowd test. It gives good heights differing by at most one at full-cube distance at most 2. Choose a covered active center at every such height and fix the resulting map."

**What is wrong.** Lemma 3.8 (p. 15) only allows these radii: "r = Θ(d) with r ≤ (1/4+o(1))d" or "r = ⌊n^{1−ρ}⌋, for fixed 0<ρ<1, with b > b_0 + (D+1)ρ".

§9 uses r = ⌊n^σ⌋ with σ < x_s/10 < .01 (p. 81). Two problems:
- In the first form this is not Θ(d).
- In the second form it forces ρ = 1−σ, so the condition reads b > b_0 + 3(1−σ) > 2.97. That is impossible, because Lemma 3.8 needs b < 1.

So Lemma 3.8 does not apply as stated. Three things also change at once:
- The geometry: paths live in the full cube Q_n and move between slices, where Lemma 3.8 works inside a single Q_d.
- The crowd tests: the (r+D)-ball test is replaced by three tests (same slice radius r, threshold n^{χ/2}; adjacent slices radius r−1, threshold n^{χ/2}; same slice radius r+1, threshold n^{1−σ+ε}), each with "degraded thresholds at successive scales".
- The overlap analysis: it now needs the slice/residual dichotomy quoted above.

Step 5 of Lemma 3.8, which proves the Lipschitz and good-site-level conclusion (i) at the top scale, is not in the "Steps 2–4" being adapted, yet its conclusion is used.

**What I checked, and found no failure in:**
- (a) Base scale. The hole probability is ≤ exp(−n^{b_0}/2) with b_0 > a. The crowd tails are exp(−Ω(n^{χ/2})) with χ/2 > a. The point count is exp(O(R_0 log n)).
- (b) Overlap. If starts are KR′-separated and the residual balls of radius r + CR′ intersect, then cKR′ ≤ 2r + 2CR′, so R′ = O(r/K). Otherwise the overlap is empty. For R′ = O(r) the ball radius is O(n^σ), which is sublinear, so the shell and hypergeometric estimate exp(−Ω(s log n)) of Lemma 3.8 Step 3 applies. Enumerating slices within O(R′) special distance costs m^{O(R′)} = e^{O(R′ log n)}.
- (c) Overlap-exception exponent. The weakest threshold is n^{χ/2}, giving exp(−Ω(n^{χ/2}R′/q)). Its ratio to the child exponent n^a R′^θ is n^{χ/2 − a − σ_h}R′^{1−θ} → ∞ because χ/2 > a + 4σ_h.
- (d) Configuration count. The child exponent beats exp(O(qR_i log n)) because a > σ_h + (1−θ).
- (e) Top scale. n^a H^θ ≥ n^{a+(1−ζ)θ} > n^{1+c}, which allows a union over all 2^n sites.

**Why it matters, and why I do not rate it a gap.** The heights are genuinely needed. A one-level random net leaves 2^n sites each uncovered with probability e^{−n^{b_0}}. A covering-code density large enough to cover everything puts about n^{2−σ} codewords in a radius-(r+1) ball, and then T + m would no longer fit under S_d = n^{y_d} with y_d < 1. So the existence of the ID map with T = O(n^{1−σ+ε}), core size ≤ n^χ and read bound r+3 is a real lemma.

On the other side, the map is deterministic and coloring-independent ("Randomness is used here only to prove existence of this map"), it is only needed to exist, and every exponent comparison the induction needs is stated and correct.

**Fix.** State and prove a version of Lemma 3.8 for the full-cube metric with slice-crossing paths and the three tabulated crowd tests. Include the top-scale Lipschitz step (Step 5).

### Objection 2 (COSMETIC/UNCLEAR, exposition): §8 Step 2 and Step 4, what "base gates" covers, pp. 70-72

Verbatim (p. 70-71):
> "At a fixed key their combined exception probability is at most e^{−n^{c′}}, for some fixed c′ > 0: η_g ≤ e^{hn^β+n^{τ/2}}Λ, .8A_g ≤ Z_g ≤ 1.2A_g. We also require each of ∫d_i^− dη_g(i) and ∫d_i^− dΛ(i) to be within a factor 1.1 of A_g. With any one cross key omitted, the analogous requirement is within a factor 1.1 of 2^h A_g. We call these the base gates."

And Step 4 (p. 72):
> "Retain the base gates at g and its grid neighbors; these gates depend on the candidate but not on the hypothetical tag and anchor outcomes. ... The density of S_g against this reference is at most exp(hn^β + n^{τ/2} + O(1))."

**What is wrong.** Read grammatically, "these" may mean only the factor-1.1 requirements. But the density bound in Step 4 holds for a candidate ξ only if the candidate's gate also contains the posterior bound η_g^{(ξ)} ≤ e^{hn^β+n^{τ/2}}Λ (equivalently R′(ξ) ≥ N^{−h}e^{−n^{τ/2}}) and Z_g(ξ) ≥ .8A_g.

Without those two conditions:
- A candidate with tiny R′(ξ) has η_g(i)/Λ(i) as large as 1/Λ(i).
- That ratio is unbounded, because the menu is finite but Λ(i) has no lower bound.
- The posterior log-density bound 1.5δhs log n on p. 72 then fails, and with it the atom cap Np_{g,a} ≤ e^{.02 s log n}.

The inclusive reading is clearly the intended one: Step 4's cross-pair bound is stated "On the base gate" using Z_u ≥ .8A_u; Step 5 imposes "the base gates" with the "combined exception probability"; Step 9 writes "On the base gate the tag and anchor laws satisfy ... /((1 − Δ)Z_g)". Under the inclusive reading everything checks. **Fix:** say that the base gates are all the bounds listed in Step 2.

### Objection 3 (COSMETIC): §9.3, the Lemma 3.5 charge constant reuses the letter c, pp. 83 and 88

Verbatim (p. 83):
> "If E_z(w) denotes failure of the displayed sum, choose a small fixed c > 0 and put B_z = {μ_{i_z}(E_z) > e^{−cn^u}}."

Verbatim (p. 88):
> "Since σ < u, charges e^{−cn^u}, with small fixed c > 0, meet Lemma 3.5 for the star and predictive events."

**What is wrong.** On tags that avoid every B_z, the linear-case special-neighbour condition can still fail on μ_{i_z}-mass up to e^{−cn^u}. That mass feeds into the star-event failure probability. Lemma 3.5 needs p_i ≤ x_i Π(1−x_j), so if the charge x_i = e^{−cn^u} uses the same c, the inequality can fail by a constant factor.

**Fix:** use charges e^{−c′n^u} with c′ < c. With degree e^{O(n^σ log n)} and σ < u the conclusion is unchanged.

### Objection 4 (COSMETIC): §9.3, Lemma 3.10 applied without a value of B, p. 88

Verbatim:
> "At such a prehistory apply Lemma 3.10 to the odd rows, with the predictive failures as predicates."

The later even-load step ("using the clock comparison on their disjoint odd neighbor sets", for up to n separated rows times n neighbours) needs the joint bound on n² queried rows, so B ≥ 2. §8 Step 12 says B = 3; §9 should too. With B = 3 every hypothesis holds (§5 table).

### Objection 5 (COSMETIC): reused symbols ρ and σ

In §8 Step 3 (p. 71), "radius r = ⌊ρn⌋ ... ρ = .01" uses ρ, which in Lemma 3.8 is the exponent of the *sublinear* radius option. Here the linear option is the one in force, so nothing goes wrong.

In the same step, "the height parameters ζ, σ, 1−θ" reuse σ, which §9 uses for the radius exponent. §9.1 notices the clash and renames to σ_h; §8 does not, but there is no interaction.

### Things I checked and do NOT object to (so nobody re-raises them)

- **§8 Step 10, p. 77.** "F_z ≤ .98^{−n}(e^{.02s log n})^m Q_v ≤ e^{.03n}Q_v, ms log n = o(n)" is correct: sm = n^{2τ+.2+o(1)} with τ ≤ .01. (The page image is easy to misread as "m log n".)
- **"No relation p > τ is required" (Appendix, p. 167; Step 2, p. 71: "This calculation uses no ordering between p and τ").** Correct. p enters through ε = e^{−n^p} and Δ = e^{−n^{p/2}} in four places:
  - the cutoff exception exp(−n^p + n^{p/2} + O_h(1)) inside the hidden-tuple local lemma, whose dependency degree is O(s^4) = n^{O(τ)};
  - the hit-test probability O(nΔ) inside the anchor local lemma, whose degree is O(n^4);
  - the factors (1−Δ)^{−1};
  - Markov at threshold .02.

  Each needs only e^{−n^{p/2}}·poly(n) → 0, so any fixed p > 0 works.
- **Re-deriving the Appendix row for asymmetric purity, "N max p_b ≤ e^{.02s log n} and N max p_v ≤ e^{.1n}" (p. 167).** Both bounds hold:
  - Np^0 ≤ (2+o(1))e^{.01s log n}, and p ≤ p^0/.98.
  - Nw_v ≤ NU_v · e^{.03n}/e^{−.04n} = e^{.07n+o(n)}, using NU_v ≤ e^{n^γ + n^{2τ} + O(1)}.

## 2. Exact quantifiers

### (b) Corollary 8.2 (p. 79)

**Statement as I reconstruct it.** Start from a bad sequence on which (7.2) holds with η_0, and set τ = min(η_0/2, .04)/4. Pass to one further subsequence and make o(N) further discards. Then for every orientation o ∈ {XY, YX} and every rational β ∈ (0, τ/4) and rational γ ∈ (0,1), there exist h_{β,γ} > 0 and n_0(β,γ,o) such that for every n ≥ n_0 in the subsequence:
- for every color G,
- for every law σ on the retained first side with width(σ) ≤ n^β,
- and every law π on the retained second side with width(π) ≤ n^γ,

we have |d_G(σ,π) − 1/2| ≤ n^{−h_{β,γ}}.

Note the order: n_0 and h depend on the pair. There is no uniformity over pairs, and the paper says so ("no uniform exponent over all rational pairs is asserted").

**How it follows.**
1. Set γ′ = max(β,γ) and h_* = h(β,γ′) from Lemma 4.1. That is a function of (β,γ), so the list of properties stays countable.
2. Choose rational β⁺ ∈ (β, τ/4) and γ⁺ ∈ (γ′, 1).
3. The countable list stabilized by Lemma 3.2 is, for every rational pair and both orientations: B(β,γ′,h_*), "bias ≥ n^{−h_*} at widths ≤ n^β, n^{γ′}", and P(β,γ′,h_*), "a pair at widths ≤ 2n^β, 2n^{γ′} with defect ≤ e^{−n^{h_*}} in some color". Both are intrinsic to supports: width is measured against the original N and d_G does not change under removals.
4. If P is available:
   - Lemma 3.2 ("available finite union has an available member") fixes one color.
   - Trimming the narrow side by Markov to degree ≥ 1 − e^{−n^{h_*/2}} costs o(1) width.
   - Lemmas 3.2 and 3.3 give a balanced finite mixture with K = 4/κ.
   - That mixture satisfies Lemma 8.1 with sides reversed: Lemma 8.1's first law is ν, of width 2n^{γ′} ≤ n^{γ⁺}; its second law is the trimmed μ, of width ≤ 2n^β + O(1) ≤ n^{β⁺} < n^{τ/4}; and p = h_*/2.
   - Lemma 8.1 then gives a cube for all large n, which is a contradiction. So P is eventually absent.
5. With P absent, (ii) of Lemma 4.1 holds eventually, so B cannot be available, so B is eventually absent. That gives the bound with h_{β,γ} = h_*.

The list is countable because the pairs are rational and h_* is a function of the pair. Lemma 3.2 applies.

### (c) Definition 9.1 (p. 79)

**The properties.** Fix the sequence after the §7–§8 stabilizations. For an orientation o, rational x, y ∈ (0,1) and rational h > 0, let B^o(x,y,h) be:

> ∃ σ on the first side and π on the second side with width σ ≤ n^x, width π ≤ n^y and |d(σ,π) − 1/2| ≥ n^{−h}.

The absolute bias does not depend on the color. Let B_L^o(x,α,h) be the same property with the second budget αn, α rational and positive. Stabilize this countable list.

**The functions.**
- H^o(x,y) := inf{h ∈ ℚ_{>0} : B^o(x,y,h) available}, taking values in [0,+∞].
- H_L^o(x,α) is defined the same way.

**Monotonicity.** Availability is upward closed in h (a smaller threshold n^{−h′} is a weaker requirement) and upward closed in each budget (the same witness still qualifies). So H is nonincreasing in x and in y.

**Absence below the infimum.** For rational h < H(x,y), B(x,y,h) is not available. Stabilization then makes it eventually absent. This is the only way absence is ever concluded, so no conclusion is drawn *at* the infimum.

**The limiting exponents.**
- H†^o = lim_{x↓0} lim_{y↑1} H^o(x,y) = sup_x inf_y H^o(x,y), with rational arguments. The inner limit is the infimum of a function nonincreasing in y, and that infimum is nonincreasing in x. Both monotone limits exist in [0,∞].
- H_L†^o = lim_{x,α↓0} H_L^o(x,α) = sup_{x,α} H_L^o. This is a monotone net limit and exists in [0,∞].

**They do not move later.** Later passes to subsequences and o(N) removals do not change any H value. Absence persists, and availability persists with κ/2 (Lemma 3.2).

**The case analysis is exhaustive.** For each orientation H† ∈ [0,∞]:
- Either some H† < 1. That is the first bullet of Proposition 9.2.
- Or both H† ≥ 1. Then each H_L† ∈ [0,∞] = {0} ∪ (0,1) ∪ [1,∞]:
  - some H_L† ∈ (0,1): second bullet of Proposition 9.2;
  - some H_L† = 0: Proposition 11.1;
  - both H_L† ∈ [1,∞]: Corollary 11.4, then Corollary 12.1.

**Boundary cases.**
- **H† = 1 exactly.** This falls under "both H† ≥ 1".
  - The linear case of Proposition 9.2 uses H† ≥ 1 only to find x_0 with inf_y H(x_0,y) > h_broad for some rational h_broad < 1. Since sup_x inf_y H = 1 > h_broad, such x_0 exists.
  - Proposition 11.1 needs H†_rev > .95 (p. 97, "H_rev(x_0, 1 − υ/4) > .95"), which also holds.
- **H† = ∞.** Covered trivially.
- **H_L† = 1 exactly.** Corollary 11.4 needs, for each ε, some H_L(x,α) > h_0 ∈ (1−ε,1). That holds because sup H_L = 1 > h_0, and Corollary 12.1 needs only h_0 = .96.
- **H_L† = ∞.** Fine.
- **H† = 0.** Handled by the first bullet. The rectangle's positive lower bound comes from Corollary 8.2 at the deep corner (x_2 < τ/4, y_2 < 1), not from H†.

**Each hypothesis is what its consumer uses.** Proposition 9.2 bullet 2 uses H† ≥ 1 in the same orientation as 0 < H_L† < 1. That is true, since both orientations have H† ≥ 1.

## 3. Proposition 9.2: dependency graphs, one per case (p. 80)

The common requirements from "Parameter selection" are:
- 0 < x_s < x_d < .1, u = x_s/2;
- 0 < h_− < h_+ < 1, x_d < (1−h_+)/10;
- σ < x_s/10;
- χ < min(x_s, h_−, 1−h_+)/100;
- h_+ − h_− < χ/10.

Sublinear adds χ < σ/10 and y_s < y_m < 1−σ < y_d. Linear adds σ < χ/10 and 100α_s < α_d < .01.

### Sublinear case (some H† < 1), in order

1. Margin: c := (1+H†)/2 < 1. Depends on H† only.
2. x_2 rational with x_2 < min(τ/4, .1, (1−c)/20); then x_1 ∈ (0,x_2) rational.
3. y_1 rational with H(x_1,y_1) < c (exists because inf_y H(x_1,y) ≤ H† < c) and 1−y_1 < x_1/10. Then y_2 ∈ (y_1,1). Now H ≤ c on the rectangle, by monotonicity.
4. H_min := H(x_2,y_2) ≥ h_{x_2,y_2} > 0, from Corollary 8.2.
5. χ < min(x_1, H_min, 1−c)/101 and χ < (1−y_2)/10.
6. K > 20c/χ diagonal points. Pick an adjacent pair (x_s,y_s) < (x_d,y_d) with H-drop < χ/20. These are rational.
7. Rational h_−, h_+ within χ/40 below H(x_d,y_d) and above H(x_s,y_s). Then h_+ − h_− < χ/10, h_− > 100χ, and 1−h_+ > (1−c)/2 > 10x_d.
8. σ ∈ (1−y_d, 1−y_s). Then σ > 1−y_2 > 10χ, and σ < 1−y_1 < x_1/10 ≤ x_s/10.
9. y_m ∈ (y_s, 1−σ); u = x_s/2.
10. ε with 0 < ε < min(σ, y_d − (1−σ)).
11. b_0 < min(ε, χ/2).
12. Height constants σ_h, ζ, a, θ with σ_h < ζ, b_0 > a > ζ + σ_h + (1−θ), χ/2 > a + 4σ_h.
13. c_4 is absolute. K = 4/κ comes from the shallow availability tolerance.

There is no cycle and every constant is independent of n. Here is where each derived condition is used:
- n^{x_s} = o(na_*) needs x_s < 1−h_+. Used for the even cap L_X, p. 88.
- σ < u: local-lemma degree, p. 88.
- χ < u: 2^k e^{−Ω(n^u)}, p. 84.
- 8χ < 2h_−: tb_*² = o(1), p. 86.
- u + 8χ < x_s: p. 86.
- mb_* = o(na_*) needs y_m − h_− < 1 − h_+. True because y_m < 1−σ and h_+ − h_− < σ/100.
- T + m and S_s + O(n^u) below S_d need 1−σ+ε < y_d, y_m < y_d, u < y_d.
- 1 − σ − 2(h_+−h_−) > u: the concentration exponent, p. 87.
- kb_*² = o(a_*) needs χ < h_− − (h_+−h_−). Holds.

### Linear case (both H† ≥ 1, some 0 < H_L† < 1), in order

1. Margins 0 < ℓ_1 < H_L† < ℓ_2 < 1.
2. h_broad ∈ (ℓ_2, 1) rational.
3. x_0 with:
   - inf_y H(x_0,y) > h_broad (uses H† ≥ 1 > h_broad);
   - φ(x) := sup_α H_L(x,α) > ℓ_1 for x ≤ x_0 (φ ↑ H_L† as x ↓ 0);
   - x_0 < min(.1, (1−ℓ_2)/20).

   Then x_1 ∈ (0,x_0) rational.
4. χ < min(x_1, ℓ_1, 1−ℓ_2)/101.
5. Subdivide [x_1,x_0] so that adjacent x_s < x_d have φ(x_s) − φ(x_d) < χ/30.
6. α_d < .01 rational with H_L(x_d,α_d) > φ(x_d) − χ/30.
7. α_s < α_d/100.
8. Rational h_± around H_L(x_d,α_d) ≤ H_L(x_s,α_s) ≤ φ(x_s). The spread is < χ/15 plus margins, which is < χ/10. Also h_+ < ℓ_2 < h_broad.
9. σ < min(χ/10, x_s/10).
10. u = x_s/2; ε < σ; b_0 < ε with b_0 + σ < χ/2.
11. Height constants as before. m = ⌊α_d n/10⌋.

There is no cycle and every constant is independent of n. The opposite orders of σ and χ in the two cases are imposed only within each case, as the paper says. Budget check: S_s + O(n^u) + log(1/.49)(T+m) ≤ (.01 + .0713)α_d n + o(n) < α_d n.

## 4. Parameter-dependency tables

### Lemma 8.1 (pp. 69-79)

| constant | fixed where | depends on | used where |
|---|---|---|---|
| η_0 | Cor. 7.2 | stabilized sequence | (7.2) everywhere in §8 |
| η = min(η_0/2,.04), τ = η/4 | §8 head, p. 69 | η_0 | s, bins, T, b |
| γ < 1, β ∈ (0,τ/4), p > 0, K | hypotheses | — | widths, ε, balance |
| s = ⌈n^τ⌉, chunk ⌊n^{.2}⌋, m = s⌊n^{.2}⌋ | Step 1 | τ | grid, E(g), f_grid |
| bin mass ≤ 2n^{−.04} | Step 1 | — | f_grid, key count |
| δ = 10^{−4} | Step 1 | — | ε_0, density caps |
| h (integer) | declared Step 1, fixed Step 5 (δh/4 > 2C) | C, the list-count constant (independent of h) | R′, A_g, ε_0, L_n |
| ε = e^{−n^p}, Δ = e^{−n^{p/2}} | Steps 1-2 | p | cutoffs, hit test |
| D (removed set), cutoff e^{−n^{2τ}} | Steps 1-2 | η, τ | α_x precision, Z_g |
| c′ | Step 2 | τ, η, p | base-gate exception |
| D=2, r=⌊.01n⌋, λ=n^{10}, b=τ/16, b_0=b/4; ζ, σ, θ, a | Step 3 | τ | Lemma 3.8 |
| T = ⌈n^{τ/8}⌉ | Step 3 | τ | lists, density cap |
| ε_0 = e^{−δhs log n} | Step 4 | δ, h, s | Lemma 3.7, q_{g,k}, q_L |
| c_H, x_H = 2q_H | Step 5 | c′, τ | hidden local lemma |
| L_n = exp(C(s+T)log n) | Step 5 | C absolute | bad lists, Step 7 |
| C_1 | Step 9 | Lemma 3.8 constants | B_g |
| c_A, x_A = 2q_A | Step 10 | τ, p | anchor local lemma |
| θ_0, A_*, P_*, B = 3 | Step 12 | Lemma 3.10 | odd injection |

No cycle. h is chosen after C, and C does not involve h ("the list counts below have exponents independent of h", p. 70).

### Corollary 8.2

| constant | fixed where | depends on | used where |
|---|---|---|---|
| γ′ = max(β,γ) | proof | β, γ | Lemma 4.1 needs β ≤ γ |
| h_* = h(β,γ′) | Lemma 4.1 | β, γ′ | bias and purity thresholds |
| β⁺, γ⁺ | proof | β, γ, τ | Lemma 8.1 widths |
| p = h_*/2 | trimming | h_* | Lemma 8.1 |
| κ, K = 4/κ | Lemmas 3.2/3.3 | purity family | Lemma 8.1 balance |

### Proposition 9.2
See §3.

## 5. Every application of the §3 tools in my scope

| tool | where (page) | hypotheses as stated | met? |
|---|---|---|---|
| Lemma 3.2 | Cor 8.2 (p. 79); Def 9.1 (p. 79); Prop 9.2 color fixing (p. 81) | countable list of witness-intrinsic properties | yes. Rational pairs/exponents; width uses original N; the finite union of two colors gives an available member |
| Lemma 3.3 | Cor 8.2 (p. 79, "A balanced mixture"); Prop 9.2 (p. 81) | finite available menu | yes. K = 4/κ |
| Lemma 3.5 | §8 Step 5 (p. 73) | events on independent hidden tuples Θ_g; one event per key reads B_grid(g,2); degree O((1+2s)^4); x_H = 2q_H, q_H ≤ e^{−n^{c_H}} | yes |
| Lemma 3.5 | §8 Step 10 (p. 77) | independent anchors given the history; cell graph degree O(n), radius ≤ 2, degree O(n^4); q_A ≤ e^{−n^{c_A}} | yes |
| Lemma 3.5 (comparison form) | §8 Steps 11-12 (pp. 77-78); §9 tag and star removals (pp. 83, 88) | remove constraints touching the target variables, then integrate them raw | yes. Costs exp(O(sn²x_A)), exp(O((1+2s)²x_H)), poly(n)e^{O(n^σ log n)}e^{−cn^u}, each 1+o(1) even after a factor n |
| Lemma 3.5 | §9 B_z (p. 83) | independent tags i_z; B_z reads B(z,1) in Q_m; degree O(m²) | yes |
| Lemma 3.5 | §9.3 star + predictive (p. 88) | anchors per ID and masks per row independent; degree poly(n)e^{O(r log n)} | yes, with the c′ < c caveat (Objection 3) |
| Lemma 3.6 | §8 Step 9, twice (p. 76) | Z_v = B_{g(v)}(x), L_B = exp(O(hs+hn^β+n^{τ/2})), f_grid = n^{O(1)}(2n^{−.04})^s; then Z_v = NU_v(x), L_U = e^{n^γ+n^{2τ}+O(1)}, f_res = e^{−Ω(n)} | yes. nfL = o(1) in both; separated products factor (disjoint hidden neighborhoods / disjoint center inputs) |
| Lemma 3.6 | §8 Step 11 (p. 78) | Np_b(y) ≤ e^{.02s log n}; grid distance > 8 separation; d_v = O(K) | yes |
| Lemma 3.6 | §8 Step 12 (p. 79) | Nw_v ≤ e^{.1n}; residual distance > 4; f ≤ n^{O(1)}2^{−(n−m)} | yes |
| Lemma 3.6 | §9 tag loads (p. 82), odd loads (p. 88), even loads (p. 88) | caps e^{S_s}, e^{S_d}, 2^n e^{−c_4na_*/2}; near fractions 2^{−m}, 2^{−n}e^{O(r log n)} | yes |
| Lemma 3.7 | §8 Step 4 (p. 72) | Q = product of candidate-independent references (a probability law); F_ξ includes the candidate's gate | yes, given the inclusive "base gate" reading (Objection 2) |
| Lemma 3.7 | §8 Step 5 (p. 72-73), E_{Θ_g} q_{g,k} ≤ ε_0 | reference fixed by the other tuples | yes |
| Lemma 3.7 | §8 Step 10 (p. 77) | Q_v independent of z (p^0 omits ordinary z; uniform at cross); V and p^0 recomputed with z | yes |
| Lemma 3.7 | §9.3 (p. 87) | Q = P^− (deletion kernels, x-independent); V recomputed; no selection | yes |
| Selection recomputed under candidate replacement | §8 Steps 6-7 (p. 74) | a_ξ disintegrates the raw experiment; Σ_L∫F_ξa_ξ dQ_L ≤ 1; the base posterior is used only when M^a < ε_0M, and that costs ≤ ε_0L_n = o(1) | yes. This is exactly what §1.3 "The probability comparisons" demands |
| Lemma 3.8 | §8 Step 3 (p. 71) | linear radius r = .01n ≤ d/4; D=2; λ = n^{10}; 0 < b_0 < b < 1; small ζ, σ, θ, a | yes |
| Lemma 3.8 (i) | §8 Step 5 (p. 73) | eligible sizes ≥ λ/3 (forbidden IDs O(n(n+s)(s+T)) = o(λ)); eligibility independent of activations | yes; union over e^{O(s log n)} slices |
| Lemma 3.8 (3/λ, (ii)) | §8 Step 9 (p. 76) | uniform over legal eligibility; forced present center | yes |
| Lemma 3.8 adapted | §9.1 (pp. 81-82) | outside the stated radius range | NOT a literal application (Objection 1) |
| Lemma 3.10, B=3 | §8 Step 12 (p. 78) | column sums o(1) ≤ θ_0; atoms e^{.02s log n}/N; predicates read n rows; each row in ≤ n predicates; failure ≤ e^{−.02n}; log g = O(n) | yes |
| Lemma 3.10 | §9.3 (p. 88) | as above, atoms e^{S_d}/N, failure ≤ e^{−c_4na_*/8} | yes, if B ≥ 2 (Objection 4) |
| Lemma 3.9 | — | not used in §8–9 | — |
| Hall (via p. 12) | §8 end (p. 79), §9 end (p. 88) | rows are probability laws on common neighbourhoods; column sums ≤ 1 | yes |
| Finner [11] | §9.2 (p. 87) | each outer anchor read ≤ r+3 times, each mask once; Hoeffding's lemma on each factor | yes. See §7 |

## 6. Verified line by line vs only skimmed

### Verified line by line (I re-derived each inequality)

**§8, Lemma 8.1**

- **Step 1** (pp. 69-70):
  - grid bookkeeping: binomial atom O(n^{−.1}) vs bin mass 2n^{−.04}; |E(g)| ≤ 2s; every cube edge lies in the padded lists;
  - (7.2) bounds |X_i^±| < Ne^{−n^η} (n^η ≤ n^{η_0/2}, 2n^{−η} > n^{−η_0});
  - Markov for D;
  - balance gives E_Λμ_i(D) ≤ 2Ke^{−n^η/2};
  - tag discard, own-color defect 2ε;
  - α_x = 2^{−h}(1+O(hn^{−η})+O(2^he^{−Ω(n^η)})) = 2^{−h}(1+o(1/s)), using τ = η/4.
- **Step 2** (pp. 70-71):
  - Pr(R′(Θ) < N^{−h}e^{−n^{τ/2}}) ≤ e^{−n^{τ/2}} by counting;
  - η_g/Λ ≤ e^{hn^β+n^{τ/2}};
  - aggregate widths < n^η/2;
  - sequential hit fractions 1/2 ± 2n^{−η} via (7.2) (widths n^β + n^η ≤ n^{η_0});
  - product = A_g(1+O(hs n^{−η}));
  - own-miss 2hε;
  - E[L_g|Θ_g] ≤ O(hεA_g) via α_x^{|E(g)|} = A_g(1+o(1));
  - removed weight ≤ L_g/Δ;
  - Markov;
  - e^{−n^{2τ}} = o(A_g);
  - .8A_g ≤ Z_g ≤ 1.2A_g;
  - no p–τ ordering.
- **Step 3** (p. 71):
  - Lemma 3.8 parameter admissibility;
  - two levels for ordinary neighbours;
  - 2n^b ≤ T.
- **Step 4** (p. 72):
  - internal density ≤ e^{hn^β+n^{τ/2}}·1.1/.8;
  - cross density ≤ 1.1·2^h/(.8(1−Δ)) ≤ 2^{h+2};
  - posterior log density ≤ 1.5δhs log n (Tn^β h = o(hs), Tn^{τ/2} = o(s));
  - support properties: hits every cross anchor; μ_i{hits ξ | hits Θ_{E(g)}} ≥ 1−Δ.
- **Step 5** (pp. 72-74):
  - Markov for q_{g,k};
  - hidden local lemma;
  - Pr_tags(q_L > ε_0^{1/4}) ≤ ε_0^{1/4};
  - L_n^n ε_0^{n/4} vs the cell count;
  - maximal-family marking argument (a used eligible list cannot be bad, because the selecting site's ball contains the shared ID);
  - forbidden count o(λ);
  - selection input scopes B_grid(t,2)×B_Q(b, r+4H+2), hidden B_grid(t,3).
- **Step 6** (p. 74): F_ξa_ξ is the valid-presentation subdensity; disjoint-list sum ≤ 1.
- **Step 7** (pp. 74-75):
  - log density < .003hs log n;
  - |H|/N ≤ e^{−.01s log n};
  - Pr(≥ h/2 coords in H) ≤ 2^h e^{−.002hs log n};
  - q(H) ≤ 1/2 + o(1);
  - the raw-mean cancellation E p^0 ≤ O(1)E_Λν_i, including the ε_0L_n term;
  - scopes B_grid(g,3)×B_Q(a, r+4H+3), B_grid(g,4).
- **Step 8** (p. 75): miss ≤ Δ/(1−Δ) under U_{g,i}; failure O(nΔ); N max p ≤ e^{.02s log n}.
- **Step 9** (pp. 76-77):
  - selection weight λO(1/λ) + Hλe^{−n^c};
  - S_gU_{g,i} ≤ η_gμ_i1/((1−Δ)Z_g);
  - E_raw B_g = O(K) via Eη_g = Λ and α_x^{|E(g)|};
  - f_grid L_B n = o(1);
  - f_res = e^{−Ω(n)} with r = .01n, H = o(n);
  - L_U.
- **Step 10** (p. 77):
  - Q_v construction;
  - F_z ≤ e^{.03n}Q_v;
  - predictive e^{−.04n};
  - Markov e^{−.02n};
  - profile count e^{O(s log n)};
  - degree O(n^4);
  - q_A.
- **Step 11** (pp. 77-78): removal costs; integration order; disjoint radius-4 scopes; the C^l bound; nf_grid L = o(1).
- **Step 12** (pp. 78-79):
  - Lemma 3.10 hypotheses;
  - N max w_v ≤ e^{.1n};
  - residual-separated rows have disjoint odd-neighbour and anchor sets;
  - cancellation Σ_y M_v w_v ≤ U_v(x);
  - column sums O(2^n/N);
  - Hall;
  - every cube edge (ordinary via the hit test recomputed with x, cross via posterior support recomputed with x) is in color G.

**Corollary 8.2** (p. 79): fully (§2).

**§9**

- **Definition 9.1** (p. 79): fully (§2).
- **Parameter selection, both cases** (pp. 80-81): fully (§3).
- **Restriction to degree ≥ 1/2 + a_*** (p. 81): retained mass ≥ 2a_*, width cost h_+ log n.
- **§9.1 read bound** (p. 82):
  - same-slice outside-core ID: d_H(c,v′) > r forces both flipped coordinates into Δ(c,v′), so ≤ r+2 stars;
  - adjacent-slice: ≤ (r+1)+1;
  - distance-two slice: 2;
  - total ≤ r+3.

  Also verified: T + m distinct IDs at an odd row; core size ≤ 6n^{χ/2} ≤ n^χ; the crowd means V_{r±1}/V_r and their thresholds; the budget inequality S_s + O(n^u) + log(1/.49)(T+m) < S_d in both cases.
- **Tags and masks** (pp. 82-83):
  - n-th moment with near fraction 2^{−m};
  - the linear-case special-neighbour condition (broad test on ν̄ of width O(1); deep test for individual tags; clipping; Hoeffding tail exp(−Ω(na_*²/b_*²)) with na_*²/b_*² ≥ n^{1−χ/5} ≫ n^u; Markov; local lemma);
  - mask separation: ν{c ≤ (1+ε)c̄} ≥ ε/(1+ε), so R_b ≤ (1+e^{−n^u})ν.
- **§9.2** (pp. 83-87), every display:
  - prefix widths;
  - forward and reverse regularity via deep discrepancy;
  - P_O(J_−) = 2^{1−k}(1+O(kb_*));
  - the weighted-mean step costing O(kb_*²) (the covariance of the relative weight O(kb_*) with the oscillation O(b_*));
  - the identity 2^kE[P_O1_{J_D}] = a_DQ;
  - R_b = (1+θ)a_DQ + e with ‖e‖_1 ≤ (1+2^k)Pr(irregular);
  - Q = (1+ψ)ν + err, including the exceptional Q-set;
  - λ, s, τ = (1+s/(Ckb_*))λ, linearity giving O(kb_*²);
  - the covariance tail (Fubini, E‖S‖² = O(t + t²b_*²), λ_±, deep discrepancy ⇒ |E| ≤ 2Zb_* = O(b_*√t) vs > ta_*n^{−2χ}; ratio n^{2χ−(h_+−h_−)} → ∞);
  - total core shift o(a_*);
  - the surplus count: ordinary (n−m)a_*; special −.06na_* (linear) or −2mb_* = −o(na_*) (sublinear);
  - Finner + Hoeffding's lemma giving exp(−t²/(8ndb_*²)), t = .1na_*, d = r+3;
  - log(1/2+t) expansion with quadratic loss O(nb_*²) = o(na_*) (needs 2h_− > h_+, true).
- **§9.3** (pp. 87-88):
  - F_x ≤ 2^ne^{−c_4na_*}P^− from p_b ≤ p_b^−/q_b;
  - Lemma 3.7 and Markov;
  - local-lemma charges;
  - odd cap e^{S_d}, near fraction, raw means;
  - Lemma 3.10;
  - even cap L_X ≤ 2^ne^{−c_4na_*/2} (n^{x_s} = o(na_*));
  - even cancellation;
  - column sums O(2^n/N);
  - Hall;
  - adjacency on every edge (p_b^{(x)}(y_b) > 0 ⇒ y_b ∼ x).

**§1.3, Figure 1, and the Appendix rows and paragraph** (pp. 3-6, 166-169): checked against the bodies of §8 and §9. They are consistent: every exponent and width in the three rows matches the body.

### Only skimmed, or not checkable from the text

- **§9.1 "The adapted height construction"** (pp. 81-82): I checked only the exponent conditions; the induction is not written (Objection 1).
- **Lemma 3.8, 3.10 and 3.5 proofs (§3), Lemma 4.1 (§4), Lemma 7.1 and Corollary 7.2 (§7)**: I used their statements only.
- **§8 Step 5 locality bookkeeping** (exact radii B_grid(t,2)×B_Q(b,r+2) and r + 4H + 2): checked for plausibility, not exhaustively enumerated.
- **The "fixed local handling of invalidity" and "local fallbacks"** (pp. 74, 84): I checked that they are functions of local inputs only, as the text says, but no fallback is written out.

## 7. Citation table (external results used in §8–9)

| cited | what the paper claims | what the source says | verdict |
|---|---|---|---|
| [11] H. Finner, Ann. Probab. 20 (1992) 1893-1901. Read: the Project Euclid scan, pp. 1893-1898 (refs/finner/finner.pdf) | p. 87: "the product-space Hölder inequality [11] ... bounds the expectation of a product of nonnegative functions by the product of their d-norms when each independent input is read at most d times. We apply it with d = r + 3" | Theorem 2.1 (p. 1894): "Let m ∈ ℕ, M = {1,...,m}, ∅ ≠ S_j ⊆ I_n, p_j ≥ 1 for j ∈ M, M_i = {j ∈ M: S_j ∋ i} for i ∈ I_n such that Σ_{j∈M_i} p_j^{−1} = 1 for all i ∈ I_n ... Then ∫Π_{j∈M}\|f_j\| dμ_{I_n} ≤ Π_{j∈M}(∫\|f_j\|^{p_j} dμ_{S_j})^{1/p_j}." §3 (p. 1898), for probability measures: "(3.1) remains true if the conditions Σ_{j∈M_i} p_j^{−1} = 1, i ∈ I_n, are weakened to Σ_{j∈M_i} p_j^{−1} ≤ 1." | MATCH. With p_j = d and each variable in ≤ d sets, Σ ≤ 1, which is exactly the probability-space form in §3 |
| [20] P. Hall 1935 (through §3, p. 12) | rows supported on allowed sets with column sums ≤ 1 give \|S\| ≤ \|∪ supp\|, hence distinct representatives | standard marriage theorem | COULD NOT FETCH (the DOI link returns a Cloudflare challenge page; the copy in refs/hall1935/hall.pdf is that HTML page). The step itself is checked in the paper on p. 12 |
| Hoeffding's lemma / bounded-summand tail (uncited in §9, p. 83 "Their downward deviation ... exp(−Ω(na_*²/b_*²))"; p. 87 inside "Exponential Markov") | sums of independent [−2b_*,2b_*] terms | standard (cited elsewhere as [23]) | standard, correctly applied |

No other external result is invoked in §8–§9. Lemmas 3.5-3.10 are internal and were refereed by other seats.

## 8. Rate of C_n and the bound N ≤ n2^n

**No rate on C_n is used anywhere in my scope.** C_n → ∞ enters only through "column sums O(2^n/N) = o(1)" at:
- §8 Step 11 (p. 78) and Step 12 (p. 79);
- §9.3 odd and even column sums (p. 88).

**N ≤ n2^n is used, legitimately, in two ways:**
- (i) Markov at a large fixed threshold, followed by a union over all N labels, after every Lemma 3.6 n-th-moment bound: §8 Steps 9, 11, 12; §9 tags, odd and even loads. Here (K·d̄/C′)^n·n2^n → 0.
- (ii) log g = O(n) in Lemma 3.10.

**Every exponential loss is beaten by a fixed power of n or by n itself, never by C_n:**
- f_grid L_B, f_res L_U, nfL in all six Lemma 3.6 applications;
- ε_0L_n;
- the local-lemma degrees.

## 9. Hedge-phrase audit

Each occurrence in §8–§9 and how it was resolved:
1. "The same works with sides reversed." (p. 69). OK: (7.2) is symmetric, and Corollary 8.2 uses this.
2. "as before" (balance, p. 69). OK.
3. "as in the preceding grid construction" (p. 69). OK: binning fully specified.
4. "the analogous requirement" (p. 71). OK, but see Objection 2.
5. "The same calculation omitting one cross key gives 2^hA_g(1+o(1))" (p. 71). OK.
6. "exactly as in Step 6" (p. 78). OK.
7. "The same identity multiplies over the separated rows" (p. 79). OK.
8. "similarly in reversed orientation" (Corollary 8.2). OK.
9. "As above, monotonicity gives" (p. 80). OK.
10. "We adapt Steps 2–4 ... same base estimates as in that proof ... the same scale induction as in Lemma 3.8" (pp. 81-82). **This is the one hedge at a hard step** (Objection 1).
11. "The same near relation" (p. 88). OK.

## 10. Verdict for this scope

- **Lemma 8.1:** HOLDS AS READ.
- **Corollary 8.2:** HOLDS AS READ. The quantifiers are correct, the list is countable, and the derivation from Lemma 4.1, Lemma 8.1, (7.2) and stabilization is complete.
- **Definition 9.1 and the exhaustion paragraph:** HOLDS AS READ. Both H† and H_L† are well defined, the case split is exhaustive, every boundary case is handled, and nothing uses a conclusion at an infimum.
- **Proposition 9.2:**
  - parameter selection: HOLDS AS READ in both cases, with no cycle and no n-dependence;
  - §9.2 and §9.3: HOLDS AS READ;
  - §9.1: **COULD NOT CHECK** the adapted Lemma 3.8 scale induction (pp. 81-82), because the paper sketches it outside the lemma's stated hypotheses. I checked every exponent condition it states and found none failing, so I classify this as a possible exposition gap, not a demonstrated mathematical one.
- **§1.3, Figure 1, Appendix rows:** consistent with the bodies.
