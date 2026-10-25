# Referee report, seat EXTREMAL: §1 (definitions, Corollary 1.2) + §2 (Θ, s*, (2.1), Lemma 2.1, the laws table, Proposition 2.2) + brief items (ii), (ix), (x)

Paper: OpenAI, "The weak pinned planar distance theorem", 23 Sep 2026, /tmp/oaimath/604/paper.pdf (sha256 6350959d…).
Every displayed formula quoted below was read off the rendered PDF (pages 2, 5–8), not off paper.txt.
Referee: Claude (extremal seat), 2026-10-14.

## Verdict for this scope

**§1 and §2 HOLD AS READ.** I re-derived every inequality in Corollary 1.2's proof and in Proposition 2.2 (transfer, deletion
process, (2.5), (2.2), (2.3), (2.4) in both regimes) and found no FATAL problem and no GAP. All objections below are COSMETIC or
UNCLEAR. Two exact finite checks (scripts verbatim below) agree with the hand computations, and each one has a control that
fails as it should.

Structural fact for the other seats (brief item (i)): **§2 uses no Euclidean or real-field input at all.** It needs only three
things: F_m is a supremum over a class of configurations that is closed under taking subsets; the "same source, same distance"
classes at each pin partition the other points; and the counting is finite. The real-closed transfer is the only step in §2
that touches the field, and it is used only to land the configuration in a number field for §3. The Lean does not use real
transfer at all (remark R3 below).

---

## Objections

**E1. (2.1), p. 5. COSMETIC.**
> "Fix 0 < c < s∗/3, max{c, (1 − c)s∗} < s < s∗, c < γ < s, (2.1)"

The bound c < s*/3 is never used. Every later use of c needs only 0 < c < γ (§5, the factor n^{c−γ}), (1−c)s* < s (which gives
s′ in (2.4)), and c < 1 (so that s/(1−c) is defined). c < 1 already follows from c < s* ≤ 1. A grep of the whole paper finds no
other use of "s*/3". The Lean (`UniformCore.extremal_parameters`) picks c = s*/4 and uses `hc3` only to derive `c<1`
(`ArithmeticSequence.graph_sequence_of_failure`). Harmless. Fix: drop "/3" or say why it is there.

**E2. Prop. 2.2 and its proof, pp. 6–8: indexing. COSMETIC.**
> "Since N/2 < n ≤ N, there is a sequence δn → 0 such that Tn ≥ n^{s−δn}" with "Tn = λn KN = N^s/(log N log n)".

The sequence is indexed by the attaining sizes N. The final size n = n(N) ∈ (N/2, N] need not be injective in N. Even so, T_n,
δ_n, d_n and λ_n are written as functions of n, while t_N, η_N, b_N and K_N carry N. Every o(1) is really "as the sequence index
→ ∞". Because N/2 < n ≤ N the two readings agree, and no estimate depends on the configuration beyond the index (checked: b_N, t_N
and η_N are built from the global quantities F_m, θ and log N only). Fix: index everything by the sequence index, or note that
any o(1) in N is o(1) in n.

**E3. Transfer paragraph, p. 6. COSMETIC (citation precision), with an observation.**
> "These are finitely many polynomial conditions over Q; a disequality can be expressed as (Dij − Dkl)² > 0. Their existential
> sentence holds over R and therefore over the real algebraic numbers, by transfer for real closed fields [9, Theorems 3.1 and 4.1]."

Kuhlmann's Theorem 4.1 is exactly the needed statement once you take R = ℝ_alg ⊆ R₁ = ℝ. Two small points: (a) the fact that
ℝ_alg is real closed is standard but is not among the cited theorems; (b) Kuhlmann's systems allow "≠" directly, so the
(D−D)² > 0 rewriting is unnecessary but harmless.

Observation: the transfer preserves much more than the downstream proof uses. The Lean (`ArithmeticSequence.planar_factor_model`,
`core_arithmetic_model`) does not transfer to real algebraic points. It specialises via the Nullstellensatz to ℚ̄. It keeps the
zero/non-zero pattern of the products D_ab = (Z₁a−Z₁b)(Z₂a−Z₂b) and of D_ab − D_cd, plus ii² = −1. The only data
`sequence_arithmetic_model` then hands to the arithmetic contradiction are: Z₁, Z₂ injective into a number field; t_e ≠ 0; the
fiber equation; and the purely combinatorial `PreparedGraph`. The pattern equivalence itself is discarded (the `_` in
`obtain ⟨…,hfiber,_⟩`). I pass this to the "whole" seat for item (i). It is not a defect of §2.

**E4. Deletion process, p. 7: the final fibers are full distance classes. UNCLEAR (true, stated only implicitly).**
> "Restricting vertices never splits a source-distance fiber, and each initial fiber can be discarded only once"

Correct. A fiber is keyed by (source, squared distance). An edge disappears only when an endpoint is deleted or its whole fiber is
discarded. So each surviving fiber is the full class {y ∈ P_final ∖ {x_e} : ‖y−x_e‖² = r}, and k_e = k_{P_final}(x_e, y). The
paper never states this last identity, though it follows in one line. My simulation asserts it on every surviving fiber of five
runs (invariant "no fiber split"). No fix is needed unless a later section uses k_e = k_P. I did not find such a use in §2.

**E5. Corollary 1.2 proof, p. 2. COSMETIC.**
> "Each such pin therefore contributes at least n − 1 − n^{1−ε/2} pairs counted by Fn(s). If there are b such pins, then, for all
> sufficiently large n, b/n ≤ (n − 1)Fn(ε/2)/(n − 1 − n^{1−ε/2}) −→ 0."

Correct. ("At least" is in fact "more than", and "sufficiently large n" is exactly what makes the denominator positive.) The
Lean's version (`Pins.bad_fraction_bound`) avoids the division: it proves b/n ≤ pairFraction + n^{1−ε/2}/(n−1), then
≤ 2·pairFraction + 2n^{1−ε/2}/n, valid for every n ≥ 2. The factor 2 is pure slack: pairFraction ≥ 0 and n−1 ≥ n/2. This is the
same inequality, MATCH.

**E6. Lemma 2.1, p. 5. COSMETIC.**
> "Given ϵ > 0, continuity permits a fixed δ > 0 such that Θ(s − δ) < θ + ϵ/2."

Only left-continuity of Θ at s is used. Correct as written; the Lean (`extremal_tail`) uses full `ContinuousAt` the same way.

No FATAL and no GAP in this scope, in either the proof or the exposition.

---

## Line-by-line status

| Item | Status | Notes |
|---|---|---|
| §1 definitions D_x(P), k_P(x,y) (counts y), F_n(s) | VERIFIED LINE BY LINE | Same as the Lean `Model.lean`: `distances = (P.erase x).image (dist · x)`, `k` = card of `(P.erase x).filter (dist z x = dist y x)`. |
| Theorem 1.1 statement + "uniform over all configurations … no explicit rate" | VERIFIED (statement) | Uniformity is automatic because F_n is a sup. The proof is the rest of the paper; only §2 is in scope. |
| Corollary 1.2 statement and proof (ε ≥ 1 remark, s = ε/2, light-class count, b/n bound, "in particular") | VERIFIED LINE BY LINE | See D1. The finite check confirms the per-pin and total inequalities; the control fails. |
| §1.1, §1.2 | SKIMMED | Background/outline. [2] Conj. 4.7 checked (citation table). |
| Θ, s*, monotonicity, F_n(t) = 0 for t ≥ 1, 0 < s* ≤ 1 | VERIFIED LINE BY LINE | |
| (2.1), the choice of a continuity point s, θ = Θ(s) > 0 | VERIFIED LINE BY LINE | E1 |
| Lemma 2.1 | VERIFIED LINE BY LINE | E6. Quantifiers right: the sup over m ≥ M_N is inside, the limit in N outside. |
| Probability-laws table; "choose e w.p. k_e/\|E\| then y ∼ µ_e"; "y ∼ q_Y then x ∼ ρ_y" | VERIFIED LINE BY LINE | q(x_e,y) = (k_e/\|E\|)(1/k_e) = 1/\|E\|; q_Y(y) = d⁻(y)/\|E\|, ρ_y = 1/d⁻(y). |
| Prop 2.2: attained maximum, choice of N-sequence | VERIFIED LINE BY LINE | |
| Prop 2.2: transfer | VERIFIED LINE BY LINE | E3; citation MATCH |
| Prop 2.2: deletion process, cost accounting, contradiction at m₀ | VERIFIED LINE BY LINE | D2; finite check Parts A–C |
| (2.5) | VERIFIED LINE BY LINE | D3 |
| (2.2) | VERIFIED LINE BY LINE | D4 |
| (2.3) | VERIFIED LINE BY LINE | D4 |
| (2.4), m > n^{1−c} | VERIFIED LINE BY LINE | D5 |
| (2.4), m ≤ n^{1−c} | VERIFIED LINE BY LINE | D5 (brief (ii): k_C, not k_P, as required) |
| "every k_e ≥ n^γ for sufficiently large n" | VERIFIED | K_N ≥ n^s/log(2n) ≥ n^γ eventually, since γ < s |
| Brief (ix): §6 opening, §6 last paragraph, §7 opening, p. 26 closing paragraph (subsequence dichotomy) | VERIFIED (logic only) | D6. The contents of §6/§7 are other seats'. |
| §3–§7 | NOT READ (out of scope) | except the interface reads listed in D6 |

Hedge words in §1–§2: "clearly", "it follows", "similarly", "the same argument", "obvious" and "immediate" occur 0 times. All 14 occurrences of
"therefore/thus/hence" in the Corollary 1.2 proof and §2 (plus one "henceforth") were checked; each is a one-line consequence
verified in D1–D5.

---

## Derivations (what I re-did)

**D1 — Corollary 1.2.** Take a pin x with r := |D_x| < n^{1−ε} classes, and s = ε/2. "Light" neighbours lie in classes of size
< n^s. Their number is ≤ (number of light classes)·max size < n^{1−ε}·n^s = n^{1−ε/2}, or it is 0. So x has more than
n−1−n^{1−ε/2} "rich" neighbours y, each with k_P(x,y) ≥ n^s. Summing over the b bad pins gives
b(n−1−n^{1−ε/2}) ≤ #rich pairs ≤ n(n−1)F_n(ε/2). Hence b/n ≤ (n−1)F_n(ε/2)/(n−1−n^{1−ε/2}) once n−1 > n^{1−ε/2}. This tends to 0
by Theorem 1.1 because (n−1)/(n−1−n^{1−ε/2}) → 1. For ε ≥ 1, n^{1−ε} ≤ 1, and |D_x| ≥ 1 when n ≥ 2, so b = 0. Uniformity in P
holds because the bound involves only F_n. ✓

**D2 — the edge count (PDF p. 7), with the paper's constants.**
- A_N = N(N−1), B_N = m₀(m₀−1), m₀ = ⌈N/2⌉.
- Initial edges = F_N(s)A_N. Every initial fiber is a full class of size ≥ N^s, so there are ≤ A_N/N^s initial fibers.
- Each fiber is discarded at most once, at a cost < K_N, so the total fiber cost is < (A_N/N^s)·N^s/log N = A_N/log N.
- Reaching m₀ takes N−m₀ deletions, at counts m = N, …, m₀+1. Each costs < 2(θ−η_N)(m−1). Summing,
  Σ_{m=m₀+1}^{N} 2(m−1) = A_N − B_N exactly (checked for 2 ≤ N ≤ 3000).
- So at count m₀ (after cleanup), |E| ≥ F_N(s)A_N − (θ−η_N)(A_N−B_N) − A_N/log N.
- Subtracting (θ+b_N)B_N gives (F_N(s)−θ)A_N + η_N(A_N−B_N) − A_N/log N − b_N B_N.
- Using B_N ≤ A_N and t_N = b_N + |F_N(s)−θ| + 1/log N, this is ≥ η_N(A_N−B_N) − t_N A_N = η_N A_N(1 − B_N/A_N − η_N), since t_N = η_N².
- This is > 0 for large N: B_N/A_N → 1/4, η_N → 0, and η_N > 0 because 1/log N > 0. The 1/log N term in t_N does double duty: it
  absorbs the fiber cost and it makes η_N strictly positive. The control in Part B shows the inequality is false without it.
- Upper bound: every remaining edge lies in a fiber of size ≥ K_N = N^{f_N} ≥ m₀^{f_N} (f_N > 0). So k_{P′}(x,y) ≥ m₀^{f_N} on the
  m₀-point remainder P′, and |E| ≤ B_N F_{m₀}(f_N) ≤ (θ+b_N)B_N by the definition of b_N. Contradiction. ✓
- b_N → 0 is Lemma 2.1 with r_N = f_N = s − log log N/log N → s and M_N = m₀ → ∞. The finite max over [m₀, N] is ≤ the lemma's sup. ✓

**D3 — (2.5).** The process therefore stops at some n > m₀ with every degree ≥ 2(θ−η_N)(n−1) > 0, so E ≠ ∅. Summing degrees gives
2|E| ≥ 2n(θ−η_N)(n−1), i.e. d_n ≥ θ−η_N. Every edge has k ≥ K_N ≥ n^{f_N} (since n ≤ N), so d_n ≤ F_n(f_N) ≤ θ+b_N (since
m₀ < n ≤ N). ✓ Moreover K_N = N^s/log N ≥ n^s/log(2n) = n^{s−o(1)}. ✓

**D4 — (2.2), (2.3).**
- q/π = n(n−1)/|E| = 1/d_n ≤ 2/θ = B₀ once d_n ≥ θ/2.
- q_X(x) ≤ B₀Σ_y π(x,y) = B₀/n = B₀α(x).
- (q_X+q_Y)(x) = deg(x)/|E| ≥ 2(θ−η_N)(n−1)/(d_n n(n−1)), which gives (q_X+q_Y)/2 ≥ ((θ−η_N)/d_n)α ≥ ((θ−η_N)/(θ+b_N))α (needs θ−η_N > 0, true eventually).
- q_Y{d⁻ < n^γ} = Σ d⁻(y)/|E| < n·n^γ/(d_n n(n−1)) = O(n^{γ−1}), and γ < s < s* ≤ 1. ✓

**D5 — (2.4).**
- |E|·LHS = Σ_e 1_C(x_e)|F_e∩C|·1{|F_e∩C| ≥ λ_n k_e}. This counts edges (x_e,y) ∈ C² in "heavy" fibers. The counting identity
  is checked exactly in Part C.
- Each counted pair has k_C(x_e,y) ≥ |F_e∩C| ≥ λ_n k_e ≥ λ_n K_N = T_n. Here k_C is the class size inside C (brief (ii)): F_e∩C ⊆ C∖{x_e}, all at the same distance.
- Since |F_e∩C| ≤ m−1, a nonzero count needs m ≥ T_n+1 → ∞.
- T_n ≥ N^s/(log(2n)·log n) ≥ n^{s−δ_n} with δ_n := log(log(2n) log n)/log n → 0.
- Regime m > n^{1−c}: T_n ≥ m^{s−δ_n} since m ≤ n. So count ≤ m(m−1)F_m(s−δ_n) ≤ (θ+o(1))m(m−1), by Lemma 2.1 with r = s−δ_n → s and M = ⌈n^{1−c}⌉ → ∞. Dividing by |E| = d_n n(n−1) gives (θ+o(1))/d_n·π(C²) = (1+o(1))π(C²), using π(C²) = m(m−1)/(n(n−1)). ✓
- Regime m ≤ n^{1−c}: s′ ∈ (s*, s/(1−c)) exists because s > (1−c)s*. Eventually s−δ_n ≥ (1−c)s′, so T_n ≥ n^{(1−c)s′} ≥ m^{s′}. Then count ≤ m(m−1)F_m(s′) with m ≥ T_n+1 → ∞, and Θ(s′) = 0 by the definition of s*, so sup_{m≥T_n+1}F_m(s′) → 0. Applying F_m to a SUBSET C is legitimate because C is itself an m-point planar set and the count uses k_C. ✓
- Uniformity in C: both bounds depend on m only. ✓

**D6 — brief (ix): quantifiers and the subsequence logic.**
- Θ(t) = limsup F_n(t) and s* = sup{t : Θ(t) > 0} depend on nothing else. c, s, γ depend on s*; θ = Θ(s); the Prop 2.2 sequence
  depends on (c, s, γ, θ). Nothing is circular.
- The minimal-criminal step (Θ(s′) = 0 for s′ > s*) is used only in (2.4)'s small regime.
- Every property in Prop 2.2 and (4.5) is an "o(1) along the sequence" statement, so it passes to subsequences. The paper says so
  for (4.5): "This estimate holds before passing to either a bounded or an unbounded subsequence of W."
- §6 opens with "Every counterexample sequence therefore has a bounded-W subsequence or a subsequence on which W → ∞" and ends
  with "This excludes every subsequence on which W → ∞". §7 excludes bounded-W subsequences. The closing paragraph (p. 26) says
  "Every sequence of nonnegative real numbers has a bounded subsequence or a subsequence tending to infinity." That dichotomy is
  correct, and further sub-subsequences (weak limits in §7) are harmless.
- RATE: the argument is ineffective by construction (limsup, a continuity point of Θ, weak compactness), and the paper claims no
  rate. n/√log n: not claimed; the paper explicitly separates it ("The sharper pinned conjecture asks for order n/√log n").
- No prove-too-much inside §2: §2 is field-agnostic (see the verdict), so it cannot be what separates ℝ² from F_q². That burden
  lies entirely in §3–§7.
- Sanity context (my remark, not the paper's): F_n(s) → 0 is classical for s > 2/9. Rich pairs are incidences between P and the
  ≤ (#rich pairs)/k circles centred at points of P that carry ≥ k points. The point–circle incidence bound
  I(n,m) ≪ n^{2/3}m^{2/3} + n^{6/11}m^{9/11}κ + n + m (Agarwal–Nevo–Pach–Pinchasi–Sharir–Smorodinsky 2004; Marcus–Tardos 2006; I
  quote it from memory and did not re-fetch it, and nothing below depends on it) gives #rich/n² ≪ k^{−2} + n^{1+o(1)}k^{−9/2} + 1/n.
  This is o(1) when k = n^s with s > 2/9. So under the paper's supposition s* ≤ 2/9; this is consistent with §2 and with
  Katz–Tardos, and is not a contradiction. Theorem 1.1's content is the range of small s.

---

## Finite checks

Both scripts live in /tmp/oaimath/604/seats/extremal_checks/ and were run with `python3` (each run < 25 s wall, < 30 MB RSS; no
lean/lake). Outputs are reproduced verbatim from the `.out` files.

### Check 1: exact pair ratios, exact F_3/F_4, Corollary counting (`check_F_and_cor.py`)

What it establishes:
- 3×3 grid, by hand and confirmed exactly. Corner pins have classes {1:2, 2:1, 4:2, 5:2, 8:1}, edge pins {1:3, 2:2, 5:2, 4:1},
  the centre {1:4, 2:4}. So #{k ≥ 1, 2, 3, 4, 5} = 72, 60, 20, 8, 0 out of 72. The pair ratio is 1, 5/6, 5/18, 1/9, 0 on the
  ranges 9^s ≤ 1, ≤ 2, ≤ 3, ≤ 4, > 4.
- Regular N-gon + centre (n = N+1). An exact chord-index model agrees with 60-digit numerics for N = 5, 6, 7, 8, 12, 13, 18. The
  hand formula for #{k ≥ 2} is N + N[(N−1) − 1{N even} + 1{6 | N}] (the centre joins chord N/6 when 6 | N). The centre has exactly
  one distance: this is the paper's "an exceptional set is necessary".
- **Exact small-n values of F_n** (a proof for each, plus a lattice search that is consistent with it):
  - F_3(s) = 1 for 3^s ≤ 2 (the equilateral triangle; k ≤ 2 always), and 0 for 3^s > 2.
  - F_4(s) = 5/6 for 0 < s ≤ 1/2, and 1/2 for 1/2 < s ≤ log₄3.
  - Proof for F_4: with 3 other points, each pin's class sizes partition 3 as {3}, {2,1} or {1,1,1}, so a pin contributes 3, 2 or
    0 pairs. Twelve or eleven pairs would need three pins each equidistant from the other three, which forces all six distances
    equal: impossible in ℝ². So the maximum is ≤ 10. The rhombus of two equilateral triangles attains 10 (two "centre" pins
    contribute 3 each, the two others 2 each), and gives 6 at threshold 3.
  - The search over 4-subsets of a 25-point Eisenstein patch (exact integer norms) finds max 10 and max 6 and returns the rhombus.
  - The square-lattice patch only reaches 8 (no equilateral triangles). This is a consistency check of the bound, not a proof.
- Corollary 1.2 counting: 70 (configuration, ε) cases (grids, polygons + centre, lattice circles, random grid subsets, generic
  concentric circles), with ε ∈ {0.2, 0.4, 0.6, 0.8, 0.95}. Checked: the per-pin "light < n^{1−ε+s}", the paper's total
  b(n−1−n^{1−ε/2}) ≤ #rich, and the Lean form b/n ≤ R + n^{1−ε/2}/(n−1). 0 violations.

Controls (all must FAIL, and all do):
1. A wrong claimed value 61/72 for the 3×3 grid at k ≥ 2 is rejected.
2. Moving one corner of the grid changes the k ≥ 3 count, so "still 20/72" is rejected.
3. A k that forgets to count y itself does not reproduce 60.
4. The deliberately wrong per-pin lemma "light < n^{1−ε}" (the class-size factor n^s dropped) is VIOLATED on the configuration
   "centre + 10 two-point + 5 sixteen-point generic concentric circles", n = 101, ε = 0.4. There the centre has 15 < 15.9 classes
   but 20 light neighbours. The paper's bound n^{0.8} = 40.2 holds.

### Check 2: deletion-process arithmetic and mechanics (`check_deletion.py`)

What it establishes:
- **Part A.** Σ_{m=m₀+1}^N 2(m−1) = A_N − B_N exactly for 2 ≤ N ≤ 3000. Control: the sum started at m₀ is rejected.
- **Part B.** The excess inequality holds on 200,000 exact rational random instances. Algebraically, LHS − RHS =
  (F−θ+|F−θ|)A + b(A−B) ≥ 0. Control: drop 1/log N from t_N while keeping the fiber cost in the count; with F_N(s) = θ and b_N = 0
  the claimed inequality becomes FALSE, so the 1/log N term is load-bearing.
- **Part C.** The actual process (discard fibers < K; delete vertices with degree < 2a(m−1); clean up after every deletion) runs
  on five concrete planar sets with exact integer squared distances: a 12×12 grid + 56 random points, a 14×14 grid at two
  thresholds, and two disjoint grids. Two runs stop above m₀ and two collapse. Asserted on every run:
  - the number of initial fibers is ≤ E₀/threshold;
  - the fiber cost is ≤ (#fibers)·K, and each fiber is discarded at most once;
  - each deletion at count m costs < 2a(m−1);
  - the edge count is ≥ E₀ − a(A−n(n−1)) − cost, and at the first moment the count equals m₀ it is ≥ E₀ − a(A_N−B_N) − cost;
  - every edge has k_{P′} ≥ K at count m₀;
  - **no fiber is split** (every surviving fiber equals the full class in the final set; E4);
  - all surviving fibers have ≥ K edges, and the degree bounds hold at the stop;
  - d_n ≥ a (the left half of (2.5));
  - (q_X+q_Y)/2 ≥ (a/d_n)α pointwise;
  - the finite form of (2.3);
  - the (2.4) counting identity and k_C(x_e,y) ≥ |F_e∩C| ≥ λK on 60 random subsets per run.
- Control: a mutated process that skips the post-deletion cleanup is REJECTED. It leaves fibers below K and edges with k < K,
  and the (2.4) bound fails.
- Caveat: Part C exercises the finite mechanics only. The contradiction itself is asymptotic, and in these runs the parameter
  "a" plays the role of θ−η_N by fiat.

Both outputs end with `OVERALL: ALL CHECKS PASS, ALL CONTROLS FAIL`.

---

## Citation table (scope §1–§2)

| Cited | Paper's claim | Source says | Verdict |
|---|---|---|---|
| [9] Kuhlmann, RAG lecture notes 09 (17/11/09), Thms 3.1, 4.1 (fetched from math.uni-konstanz.de, 5 pp.) | The existential sentence true over ℝ is true over the real algebraic numbers | Thm 4.1: "Suppose that R ⊆ R1 are real closed fields. Then a system of polynomial equations and inequalities with coefficients in R … where ∀ i ⋄i ∈ {⩾, >, =, ≠} … has a solution x ∈ R1ⁿ ⟺ it has a solution x ∈ Rⁿ." Thm 3.1 is the version for two real closed extensions of an ordered field K. | MATCH (needs ℝ_alg real closed, which is standard but not in [9]; ≠ is allowed directly) |
| [2] Dewar–Frankl–Mansfield–Nixon–Passant–Warren, arXiv:2505.06590v1, Conj. 4.7 (local copy refs/dewar.txt) | "the modern terminology appears, for example, in [2, Conjecture 4.7]" | "Conjecture 4.7 (Weak pinned distance conjecture). For any ε > 0, there exists a constant Cε > 0 such that … For any finite point set P ⊆ R2, there exists a point q ∈ P, which determines at least Cε\|P\|^{1−ε} distances to the other points of P" | MATCH. Corollary 1.2 implies it with C_ε = n₀(ε)^{−(1−ε)} for \|P\| ≥ 2 (for \|P\| = 1 the conjecture is vacuously false, a pedantic point). |
| [4] Erdős 1957 Problem 16, [3], [7], [8], [10], [12], [13] (§1.1) | background | not fetched; outside this seat (the "sources" seat covers them) | COULD NOT FETCH (out of scope) |

---

## Lean cross-reference (read as text only)

- R1. `Pins.lean`: `bad_fraction_bound`, `B_bound`, `pins` (B n ε → 0) and `exists_pin_eventually` (for all large n, every P with
  |P| = n has x with n^{1−ε} ≤ |distances P x|). This is the same argument as the paper's Corollary 1.2 proof, with the division
  replaced by the factor-2 slack (E5). `distances` counts nonzero distances only (`P.erase x`), and `k` includes y. Both match the
  paper.
- R2. The Lean does **not** formalise the paper's greedy deletion process. `ExtremalCore.exists_core` maximises
  score − (θ−η)|C|(|C|−1) over subsets of size ≥ m₀, where score = Σ_e max(|F_e∩C| − K, 0) is a soft fiber cutoff. It reaches
  the same list of outputs (`PreparedCore`/`PreparedGraph`: lower/upper density, the degree bound, fiber > n^γ, the `subset` and
  `small` heavy-count bounds, which are (2.4) multiplied by |E|). `extremal_tail` is Lemma 2.1. `heavySubset_uniform` and
  `heavySubset_count` are (2.4); they use `richPairs (planeSubset P D) r`, i.e. k_C as in the paper. So the paper's §2 route is
  certified here by hand only. The Lean independently certifies that a graph sequence with Prop 2.2's properties exists.
- R3. The Lean's transfer goes to ℚ̄ via the Nullstellensatz, with complex Z₁ and Z₂ that need not be conjugate. It is not real
  transfer (see E3). The subset estimates are proved on the ORIGINAL real configuration before specialising, so the Lean never
  needs subsets of the specialised configuration to be planar.

---

## Summary (≤400 words)

Scope: §1 (definitions, Corollary 1.2), §2 in full (Θ, s*, (2.1), Lemma 2.1, the laws table, Proposition 2.2: transfer, deletion
process, (2.5), (2.2), (2.3), (2.4)), and brief items (ii), (ix), (x). Everything was read off the PDF.

**Verdict: HOLDS AS READ.** There is no FATAL problem and no GAP. Every line of Corollary 1.2's proof and of Proposition 2.2 was
re-derived:
- The edge count closes with the paper's constants: excess ≥ η_N A_N(1 − B_N/A_N − η_N) > 0. The 1/log N term in t_N is
  load-bearing.
- "Restricting vertices never splits a fiber" is right, because the key is (source, squared distance).
- Lemma 2.1 is applied twice with the right quantifiers: sup over m ≥ M_N inside, limit outside.
- (2.4)'s small regime legitimately applies F_m(s′), Θ(s′) = 0, to subsets C, because the count uses k_C.

Objections, all COSMETIC/UNCLEAR:
- c < s*/3 is unused (only c < 1 is needed).
- Indices n and N are mixed along the sequence.
- [9] Thm 4.1 needs ℝ_alg real closed, which is standard but not in [9].
- k_e = k_P(x_e, y) for surviving fibers holds but is never stated.
- The Corollary's "sufficiently large n" division is handled more cleanly in the Lean.

Finite checks, scripts verbatim in the report:
- (1) Exact pair ratios for the 3×3 grid (1, 5/6, 5/18, 1/9, 0) and for regular N-gons + centre (exact model vs 60-digit numerics).
- (2) Exact small values with proofs: F_3 = 1 at threshold 2; F_4 = 5/6 at threshold 2 and 1/2 at threshold 3 (the rhombus is the
  maximiser, confirmed by an exhaustive Eisenstein-patch search).
- (3) Corollary counting on 70 cases, 0 violations.
- (4) Deletion-process arithmetic (exact identities, 200k exact random instances) and the actual process run on five planar sets
  with every invariant asserted.
- Each check has a control that fails: wrong values; k without y; the per-pin lemma without the n^s factor (violated at n = 101);
  the sum from m₀; t_N without 1/log N; the process without cleanup.

Structural findings for other seats:
- §2 is field-agnostic. It needs only a subset-closed class of configurations with partitioned pin classes. So it cannot be what
  separates ℝ² from F_q²; that burden sits entirely in §3–§7.
- The Lean replaces the paper's real-closed transfer with a ℚ̄ Nullstellensatz specialisation. The arithmetic contradiction
  receives only Z₁ and Z₂ injective, t_e ≠ 0, the fiber equation and the combinatorial `PreparedGraph`, and drops the pattern
  equivalence. This bears directly on brief item (i), the generalised "two injective coordinates" statement.
- The Lean also replaces the paper's greedy deletion with a penalised-score maximiser. The human-readable §2 route is therefore
  certified only by this hand check.

Sanity context (from memory): point–circle incidence bounds already give F_n(s) → 0 for s > 2/9. So under the supposition
s* ≤ 2/9, which is consistent with no prove-too-much.

---

## Appendix A: `check_F_and_cor.py` (verbatim)
```python
# Exact pair-ratio R_P(s) = #{(x,y): x!=y, k_P(x,y) >= n^s} / (n(n-1)) for explicit configurations,
# the exact value of F_4, and the Corollary 1.2 per-pin counting inequality, each with a control that must FAIL.
# Exactness: integer / Eisenstein-integer coordinates => integer squared distances; regular polygon via
# chord index (exact combinatorics) cross-checked against 60-digit numerics.
import itertools, math, random
from fractions import Fraction as Fr
import mpmath
mpmath.mp.dps = 60

def classes_sq(P, d2):
    """For each pin x: dict squared-distance -> list of targets. d2 exact (ints)."""
    out = {}
    for x in P:
        c = {}
        for y in P:
            if y != x:
                c.setdefault(d2(x, y), []).append(y)
        out[x] = c
    return out

def kfun(P, d2):
    cl = classes_sq(P, d2)
    return {(x, y): len(cl[x][d2(x, y)]) for x in P for y in P if x != y}, cl

def ratio_threshold(P, d2, T):
    """#{(x,y): x!=y, k >= T} / (n(n-1)) with integer threshold T (k is an integer)."""
    k, _ = kfun(P, d2); n = len(P)
    return Fr(sum(1 for v in k.values() if v >= T), n*(n-1))

sq = lambda a, b: (a[0]-b[0])**2 + (a[1]-b[1])**2
eis = lambda a, b: (a[0]-b[0])**2 - (a[0]-b[0])*(a[1]-b[1]) + (a[1]-b[1])**2   # |(a-b) in Z[w]|^2

fails = []
def expect(name, got, want):
    ok = (got == want)
    show = (lambda v: f"multiset of {len(v)} values, histogram {dict(sorted(__import__('collections').Counter(v).items()))}") if isinstance(got, list) else (lambda v: v)
    print(f"{'PASS' if ok else 'FAIL'} {name}: got {show(got)} want {show(want)}")
    if not ok: fails.append(name)
    return ok

# ---- 1. 3x3 grid, hand-computed values (see report) ----
G = [(i, j) for i in range(3) for j in range(3)]
for T, want in [(1, Fr(1)), (2, Fr(60, 72)), (3, Fr(20, 72)), (4, Fr(8, 72)), (5, Fr(0))]:
    expect(f"3x3 grid ratio k>={T}", ratio_threshold(G, sq, T), want)
_, cl = kfun(G, sq)
expect("3x3 grid distinct distances corner/edge/centre",
       (len(cl[(0, 0)]), len(cl[(1, 0)]), len(cl[(1, 1)])), (5, 4, 2))

# ---- 2. regular N-gon + centre: exact chord-index model vs 60-digit numerics ----
def polygon_centre_exact(N):
    """Points 0..N-1 vertices, 'c' centre; squared distance labels exact: chord min(k,N-k), radius 'R'.
       chord j has squared length 2-2cos(2*pi*j/N) = 1 iff j/N = 1/6."""
    pts = list(range(N)) + ['c']
    def lab(a, b):
        if a == 'c' or b == 'c':
            return 'R'
        j = (a-b) % N; j = min(j, N-j)
        return 'R' if 6*j == N else ('ch', j)
    return pts, lab

def polygon_centre_numeric(N):
    pts = [(mpmath.cos(2*mpmath.pi*i/N), mpmath.sin(2*mpmath.pi*i/N)) for i in range(N)] + [(mpmath.mpf(0), mpmath.mpf(0))]
    idx = list(range(N+1))
    def lab(a, b):
        v = (pts[a][0]-pts[b][0])**2 + (pts[a][1]-pts[b][1])**2
        return mpmath.nstr(v, 40)          # equal algebraic numbers agree to 40 digits; unequal ones differ far above 1e-40 here
    return idx, lab

for N in [5, 6, 7, 8, 12, 13, 18]:
    Pe, le = polygon_centre_exact(N); Pn, ln = polygon_centre_numeric(N)
    ke, _ = kfun(Pe, le); kn, _ = kfun(Pn, ln)
    se = sorted(ke[(x, y)] for (x, y) in ke); sn = sorted(kn.values())
    expect(f"N={N} polygon+centre k-multiset exact==numeric", se, sn)
    n = N + 1
    # hand prediction of the pair count with k>=2: centre->vertices N pairs (k=N>=2);
    # vertex pins: all N-1 other vertices are in classes of size>=2 except the diameter (N even, size 1);
    # the centre is in a class of size 1 unless 6|N (then it joins chord N/6, size 3).
    rich_vertex = (N-1) - (1 if N % 2 == 0 else 0) + (1 if N % 6 == 0 else 0)
    want = Fr(N + N*rich_vertex, n*(n-1))
    expect(f"N={N} polygon+centre ratio k>=2 (hand formula)", ratio_threshold(Pe, le, 2), want)
    _, cle = kfun(Pe, le)
    expect(f"N={N} centre has exactly one distance", len(cle['c']), 1)

# ---- 3. exact F_4 : 5/6 at threshold 2, 1/2 at threshold 3 (proof in report); lattice searches ----
def best4(patch, d2, T):
    best = 0; arg = None
    for Q in itertools.combinations(patch, 4):
        k, _ = kfun(list(Q), d2)
        c = sum(1 for v in k.values() if v >= T)
        if c > best: best, arg = c, Q
    return best, arg
tri = [(a, b) for a in range(-2, 3) for b in range(-2, 3)]          # Eisenstein patch, 25 points
sqp = [(a, b) for a in range(0, 5) for b in range(0, 5)]            # square patch, 25 points
bt2, at2 = best4(tri, eis, 2); bt3, _ = best4(tri, eis, 3)
expect("F_4 threshold 2: Eisenstein-patch max pair count (= 10 = 5/6*12, rhombus)", bt2, 10)
expect("F_4 threshold 3: Eisenstein-patch max pair count (= 6 = 1/2*12)", bt3, 6)
print("   maximiser at threshold 2:", at2)
bs2, as2 = best4(sqp, sq, 2)
print(f"   square-lattice patch max at threshold 2: {bs2} (no equilateral triangles, so must be < 10)")
if not bs2 < 10: fails.append("square patch should not reach 10")

# ---- 4. Corollary 1.2 counting, per pin and in total, paper form and Lean form ----
def cor_check(P, d2, eps, variant="paper"):
    n = len(P); k, cl = kfun(P, d2)
    s = eps/2
    bad = [x for x in P if len(cl[x]) < n**(1-eps)]
    rich = {x: sum(1 for y in P if y != x and k[(x, y)] >= n**s) for x in P}
    ok = True
    for x in bad:
        light = (n-1) - rich[x]
        bound = n**(1-eps+s) if variant == "paper" else n**(1-eps)   # control drops the class-size factor n^s
        if not light < bound and not (light == 0):
            ok = False
    pairs = sum(rich.values())
    b = len(bad)
    if variant == "paper":
        # b*(n-1-n^{1-eps/2}) <= pairs  (paper),   b/n <= pairs/(n(n-1)) + n^{1-eps/2}/(n-1)  (Lean, before the factor 2)
        if b*(n-1-n**(1-eps/2)) > pairs + 1e-9: ok = False
        if b/n > pairs/(n*(n-1)) + n**(1-eps/2)/(n-1) + 1e-12: ok = False
    return ok, b
random.seed(604)
configs = [("3x3 grid", G, sq), ("6x6 grid", [(i, j) for i in range(6) for j in range(6)], sq),
           ("Eisenstein hexagon r=3", [(a, b) for a in range(-3, 4) for b in range(-3, 4) if abs(a-b) <= 3], eis)]
for N in [12, 30, 60]:
    Pe, le = polygon_centre_exact(N); configs.append((f"{N}-gon+centre", Pe, le))
# concentric squares-of-circles style: integer points on circles x^2+y^2=r^2 (r=5,25,65) plus origin
circ = {(0, 0)}
for r2 in [25, 625, 4225]:
    r = int(math.isqrt(r2))
    for x in range(-r, r+1):
        y2 = r2 - x*x; y = math.isqrt(y2)
        if y*y == y2: circ |= {(x, y), (x, -y)}
configs.append(("origin + lattice points on 3 circles", sorted(circ), sq))
# generic concentric circles about a centre: 10 circles x 2 points + 5 circles x 16 points, n = 101.
# Radii and angles are random (60-digit), so all non-centre distances are distinct; the centre is a bad pin
# for eps=0.4 (15 classes < 101^0.6 = 15.9) with 20 neighbours in light classes (size 2 < 101^0.2 = 2.52).
rnd = random.Random(1957)
cc = [(mpmath.mpf(0), mpmath.mpf(0))]
for size in [2]*10 + [16]*5:
    r = mpmath.mpf(1) + rnd.random()*10
    for _ in range(size):
        a = 2*mpmath.pi*rnd.random(); cc.append((r*mpmath.cos(a), r*mpmath.sin(a)))
ccidx = list(range(len(cc)))
ccd = lambda a, b: mpmath.nstr((cc[a][0]-cc[b][0])**2 + (cc[a][1]-cc[b][1])**2, 40)
configs.append(("centre + 10x2 + 5x16 generic concentric circles", ccidx, ccd))
for t in range(6):
    configs.append((f"random 30 pts of 7x7 grid #{t}", random.sample([(i, j) for i in range(7) for j in range(7)], 30), sq))
n_viol_paper = 0; n_viol_control = 0
for name, P, d2 in configs:
    for eps in [0.2, 0.4, 0.6, 0.8, 0.95]:
        okp, b = cor_check(P, d2, eps, "paper"); okc, _ = cor_check(P, d2, eps, "control")
        n_viol_paper += (not okp); n_viol_control += (not okc)
print(f"Corollary counting: {len(configs)*5} (config,eps) cases; paper-form violations = {n_viol_paper}; "
      f"CONTROL (light < n^(1-eps), class-size factor dropped) violations = {n_viol_control}")
if n_viol_paper: fails.append("corollary paper form violated")
if n_viol_control == 0: fails.append("control failed to fail")

# ---- 5. controls on the exact ratio checker itself ----
print("CONTROLS (must FAIL):")
c1 = ratio_threshold(G, sq, 2) == Fr(61, 72)                       # wrong claimed value
G2 = [p if p != (2, 2) else (3, 3) for p in G]                     # perturbed grid: moving a corner must change the count
c2 = ratio_threshold(G2, sq, 3) == Fr(20, 72)
def kfun_wrong(P, d2):   # forgets that k counts y itself (counts z != x,y)
    k, cl = kfun(P, d2); return {key: v-1 for key, v in k.items()}
c3 = sum(1 for v in kfun_wrong(G, sq).values() if v >= 2) == 60
for nm, c in [("claimed 61/72 for 3x3 grid at k>=2", c1), ("perturbed grid keeps 20/72 at k>=3", c2), ("k without y itself reproduces 60", c3)]:
    print(f"  control '{nm}': {'ACCEPTED (BAD)' if c else 'rejected (good)'}")
    if c: fails.append("control " + nm)
print("OVERALL:", "ALL CHECKS PASS, ALL CONTROLS FAIL" if not fails else f"PROBLEMS: {fails}")
```

Output (verbatim):
```
PASS 3x3 grid ratio k>=1: got 1 want 1
PASS 3x3 grid ratio k>=2: got 5/6 want 5/6
PASS 3x3 grid ratio k>=3: got 5/18 want 5/18
PASS 3x3 grid ratio k>=4: got 1/9 want 1/9
PASS 3x3 grid ratio k>=5: got 0 want 0
PASS 3x3 grid distinct distances corner/edge/centre: got (5, 4, 2) want (5, 4, 2)
PASS N=5 polygon+centre k-multiset exact==numeric: got multiset of 30 values, histogram {1: 5, 2: 20, 5: 5} want multiset of 30 values, histogram {1: 5, 2: 20, 5: 5}
PASS N=5 polygon+centre ratio k>=2 (hand formula): got 5/6 want 5/6
PASS N=5 centre has exactly one distance: got 1 want 1
PASS N=6 polygon+centre k-multiset exact==numeric: got multiset of 42 values, histogram {1: 6, 2: 12, 3: 18, 6: 6} want multiset of 42 values, histogram {1: 6, 2: 12, 3: 18, 6: 6}
PASS N=6 polygon+centre ratio k>=2 (hand formula): got 6/7 want 6/7
PASS N=6 centre has exactly one distance: got 1 want 1
PASS N=7 polygon+centre k-multiset exact==numeric: got multiset of 56 values, histogram {1: 7, 2: 42, 7: 7} want multiset of 56 values, histogram {1: 7, 2: 42, 7: 7}
PASS N=7 polygon+centre ratio k>=2 (hand formula): got 7/8 want 7/8
PASS N=7 centre has exactly one distance: got 1 want 1
PASS N=8 polygon+centre k-multiset exact==numeric: got multiset of 72 values, histogram {1: 16, 2: 48, 8: 8} want multiset of 72 values, histogram {1: 16, 2: 48, 8: 8}
PASS N=8 polygon+centre ratio k>=2 (hand formula): got 7/9 want 7/9
PASS N=8 centre has exactly one distance: got 1 want 1
PASS N=12 polygon+centre k-multiset exact==numeric: got multiset of 156 values, histogram {1: 12, 2: 96, 3: 36, 12: 12} want multiset of 156 values, histogram {1: 12, 2: 96, 3: 36, 12: 12}
PASS N=12 polygon+centre ratio k>=2 (hand formula): got 12/13 want 12/13
PASS N=12 centre has exactly one distance: got 1 want 1
PASS N=13 polygon+centre k-multiset exact==numeric: got multiset of 182 values, histogram {1: 13, 2: 156, 13: 13} want multiset of 182 values, histogram {1: 13, 2: 156, 13: 13}
PASS N=13 polygon+centre ratio k>=2 (hand formula): got 13/14 want 13/14
PASS N=13 centre has exactly one distance: got 1 want 1
PASS N=18 polygon+centre k-multiset exact==numeric: got multiset of 342 values, histogram {1: 18, 2: 252, 3: 54, 18: 18} want multiset of 342 values, histogram {1: 18, 2: 252, 3: 54, 18: 18}
PASS N=18 polygon+centre ratio k>=2 (hand formula): got 18/19 want 18/19
PASS N=18 centre has exactly one distance: got 1 want 1
PASS F_4 threshold 2: Eisenstein-patch max pair count (= 10 = 5/6*12, rhombus): got 10 want 10
PASS F_4 threshold 3: Eisenstein-patch max pair count (= 6 = 1/2*12): got 6 want 6
   maximiser at threshold 2: ((-2, -2), (-2, -1), (-1, -2), (-1, -1))
   square-lattice patch max at threshold 2: 8 (no equilateral triangles, so must be < 10)
Corollary counting: 70 (config,eps) cases; paper-form violations = 0; CONTROL (light < n^(1-eps), class-size factor dropped) violations = 1
CONTROLS (must FAIL):
  control 'claimed 61/72 for 3x3 grid at k>=2': rejected (good)
  control 'perturbed grid keeps 20/72 at k>=3': rejected (good)
  control 'k without y itself reproduces 60': rejected (good)
OVERALL: ALL CHECKS PASS, ALL CONTROLS FAIL
wall 4.02 s, maxRSS 19900 KB
```

## Appendix B: `check_deletion.py` (verbatim)
```python
# Sanity checks of the Prop 2.2 deletion-process arithmetic (PDF p.7) and of the finite mechanics it relies on.
# Part A: exact identities used in the edge count, for all N up to 3000, with Fractions.  Control: off-by-one sum.
# Part B: the "excess" inequality as an algebraic implication, checked on random exact rational instances.
#         Control: drop the 1/log N term from t_N (then eta_N can be 0 and strict positivity fails).
# Part C: run the actual process on concrete planar point sets (exact integer squared distances) and assert
#         every invariant the proof uses.  Control: a mutated process that skips the post-deletion fiber cleanup.
import math, random
from fractions import Fraction as Fr
fails = []
def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: fails.append(name)

# ---------- Part A ----------
okA = True; okA_ctrl_rejected = True
for N in range(2, 3001):
    m0 = -(-N // 2); A = N*(N-1); B = m0*(m0-1)
    S = sum(2*(m-1) for m in range(m0+1, N+1))
    if S != A - B: okA = False
    S_bad = sum(2*(m-1) for m in range(m0, N+1))      # control: sum starting at m0
    if S_bad == A - B and N > 1 and m0 > 1: okA_ctrl_rejected = okA_ctrl_rejected and False
check("A: sum_{m=m0+1}^N 2(m-1) == A_N - B_N for 2<=N<=3000", okA)
check("A control: sum from m0 is NOT A_N-B_N (control rejected)", okA_ctrl_rejected)
# B_N/A_N -> 1/4 and the first N with 1 - B/A - eta > 0 for small eta (illustrative)
for N in [10, 100, 1000, 10**6]:
    m0 = -(-N//2); print(f"   N={N}: B_N/A_N = {m0*(m0-1)/(N*(N-1)):.6f}")

# ---------- Part B ----------
# Claim: with t = b + |F-th| + ell (ell = 1/log N > 0), eta = sqrt(t), and 0 <= B <= A, b >= 0,
#   F*A - (th-eta)(A-B) - ell*A - (th+b)*B  >=  eta*(A-B) - t*A  = eta*A*(1 - B/A - eta).
rng = random.Random(2)
viol = 0; ctrl_viol = 0
for _ in range(200000):
    A = Fr(rng.randint(2, 10**6)); B = Fr(rng.randint(0, int(A)))
    th = Fr(rng.randint(1, 1000), 1000); F = Fr(rng.randint(0, 1000), 1000)
    b = Fr(rng.randint(0, 50), 1000); ell = Fr(rng.randint(1, 50), 1000)
    t = b + abs(F-th) + ell
    # exact eta not needed for the identity: the inequality LHS-RHS = (F-th+|F-th|)A + b(A-B) + ... >= 0 ;
    # test it with eta = any number (take a rational eta and set t = eta^2 consistently)
    eta = Fr(rng.randint(0, 1000), 1000)
    lhs = F*A - (th-eta)*(A-B) - ell*A - (th+b)*B
    rhs = eta*(A-B) - t*A
    if lhs < rhs: viol += 1
    if not (eta*(A-B) - eta*eta*A == eta*A*(1 - B/A - eta)): viol += 1
check("B: excess >= eta(A-B) - t*A on 200000 exact random instances (and the factorisation identity)", viol == 0)
# Control: t WITHOUT the 1/log N term (fiber cost -A/log N still subtracted in the edge count).
# Then the claimed "excess >= eta(A-B) - t*A" must FAIL on some instance (F_N(s)=theta, b_N=0).
A, B = Fr(100*99), Fr(50*49); F = th = Fr(1, 3); b = Fr(0); ell = Fr(1, 5)
eta = Fr(1, 10); t_bad = b + abs(F-th)                      # missing ell
lhs = F*A - (th-eta)*(A-B) - ell*A - (th+b)*B
check("B control: with 1/log N dropped from t_N the excess inequality is FALSE (lhs < eta(A-B)-t*A)",
      lhs < eta*(A-B) - t_bad*A)

# ---------- Part C ----------
def run_process(P, s_thr, K, a, mutate_skip_cleanup=False):
    """P: list of integer points.  Initial edges: all (x,y), x!=y, with k_P(x,y) >= s_thr (exact).
       Fibers keyed by (source, squared distance). Discard fibers with < K edges; delete a vertex whose
       in+out degree < 2a(m-1); clean fibers after each deletion.  Returns trace for invariant checks."""
    N = len(P)
    d2 = lambda x, y: (x[0]-y[0])**2 + (x[1]-y[1])**2
    cls = {}
    for x in P:
        for y in P:
            if y != x: cls.setdefault((x, d2(x, y)), set()).add(y)
    fibers = {key: set(T) for key, T in cls.items() if len(T) >= s_thr}      # initial fibers = whole classes
    n_initial_fibers = len(fibers); E0 = sum(len(T) for T in fibers.values())
    V = set(P); fiber_cost = 0; vertex_cost = 0; deletion_log = []
    discarded = set(); ok_split = True; ok_once = True; snap = None
    def cleanup():
        nonlocal fiber_cost, ok_once
        for key in list(fibers):
            if 0 < len(fibers[key]) < K:
                if key in discarded: ok_once = False
                fiber_cost += len(fibers[key]); discarded.add(key); fibers[key] = set()
                if len(fibers[key]) >= K: pass
    cleanup()
    while True:
        m = len(V)
        deg = {v: 0 for v in V}
        for (x, r), T in fibers.items():
            for y in T: deg[x] += 1; deg[y] += 1
        low = [v for v in V if deg[v] < 2*a*(m-1)]
        if not low: break
        v = min(low)                       # any order; the argument is order-free
        cost = deg[v]; vertex_cost += cost; deletion_log.append((m, cost, 2*a*(m-1)))
        V.discard(v)
        for key in list(fibers):
            if key[0] == v: fibers[key] = set()
            else: fibers[key].discard(v)
        if not mutate_skip_cleanup: cleanup()
        if len(V) == -(-N//2) and snap is None:
            Es = sum(len(T) for T in fibers.values())
            kmin = min([sum(1 for z in V if z != x and d2(x, z) == r) for (x, r), T in fibers.items() if T], default=10**9)
            snap = dict(E=Es, fiber_cost=fiber_cost, kmin=kmin)
    # invariants
    E = [(x, y) for (x, r), T in fibers.items() for y in T]
    # (i) no fiber split: every surviving fiber equals the FULL class of its source in the final set
    for (x, r), T in fibers.items():
        if T and T != {y for y in V if y != x and d2(x, y) == r}: ok_split = False
    return dict(N=N, n=len(V), V=V, E=E, fibers=fibers, E0=E0, nfib0=n_initial_fibers, fiber_cost=fiber_cost,
                vertex_cost=vertex_cost, log=deletion_log, ok_split=ok_split, ok_once=ok_once, d2=d2, snap=snap)

def invariants(R, K, a, s_thr, label):
    N, n, E = R['N'], R['n'], R['E']; d2 = R['d2']; V = R['V']
    oks = []
    oks.append(("initial fibers <= E0/s_thr", R['nfib0'] <= R['E0']/s_thr))
    oks.append(("fiber cleanup cost <= (#initial fibers)*K", R['fiber_cost'] <= R['nfib0']*K))
    oks.append(("each deletion at count m costs < 2a(m-1)", all(c < bnd for (m, c, bnd) in R['log'])))
    m0 = -(-N//2)
    # edge accounting at the end: E_final >= E0 - a*(A - n(n-1)) - fiber_cost  (paper's count with m0 replaced by n)
    oks.append(("|E_final| >= E0 - a(N(N-1)-n(n-1)) - fiber_cost",
                len(E) >= R['E0'] - a*(N*(N-1) - n*(n-1)) - R['fiber_cost'] - 1e-9))
    oks.append(("no fiber split (surviving fiber == full class in final set)", R['ok_split']))
    oks.append(("each initial fiber discarded at most once", R['ok_once']))
    if R['snap'] is not None:
        S = R['snap']; A = N*(N-1); B = m0*(m0-1)
        oks.append(("at count m0: |E| >= E0 - a(A_N-B_N) - fiber_cost (paper's count)", S['E'] >= R['E0'] - a*(A-B) - S['fiber_cost'] - 1e-9))
        oks.append(("at count m0: every edge has k_{P'} >= K (so |E| <= B_N * ratio_{P'}(K))", S['kmin'] >= K))
        print(f"     [{label}] m0-snapshot (first time vertex count = m0, after cleanup): |E|={S['E']} >= E0 - a(A-B) - cost = {R['E0'] - a*(A-B) - S['fiber_cost']:.1f}")
    sizes = [len(T) for T in R['fibers'].values() if T]
    oks.append(("all surviving fibers have >= K edges", all(z >= K for z in sizes)))
    if n >= 2 and E:
        dn = len(E)/(n*(n-1))
        deg = {v: 0 for v in V}; indeg = {v: 0 for v in V}
        for x, y in E: deg[x] += 1; deg[y] += 1; indeg[y] += 1
        oks.append(("degree lower bounds hold at stop", all(deg[v] >= 2*a*(n-1) for v in V)))
        oks.append(("d_n >= a  (left half of (2.5))", dn >= a - 1e-12))
        # every edge has k_final(x,y) >= K, so d_n <= R_final(K)  (right half of (2.5) with F replaced by the actual ratio)
        kf = lambda x, y: sum(1 for z in V if z != x and d2(x, z) == d2(x, y))
        oks.append(("every final edge has k_P'(x,y) >= K", all(kf(x, y) >= K for x, y in E)))
        # (2.2): (qX+qY)/2 >= (a/d_n) alpha ; q <= pi/d_n is an identity
        oks.append(("(qX+qY)/2 >= (a/d_n) alpha pointwise", all(deg[v]/(2*len(E)) >= (a/dn)/n - 1e-15 for v in V)))
        gam = 0.5
        mass = sum(indeg[v] for v in V if indeg[v] < n**gam)/len(E)
        oks.append(("(2.3) finite form: qY{d^- < n^g} <= n*n^g/|E|", mass <= n*n**gam/len(E) + 1e-15))
        # (2.4) finite form: |E| * E_e 1_C(x_e) p_e 1{p_e>=lam} == #{(x_e,y) in C^2 : |F_e∩C| >= lam k_e}, and each
        # counted pair has k_C(x_e,y) >= |F_e ∩ C| >= lam*K
        lam = 0.3; rng = random.Random(7); ok24 = True
        Vl = sorted(V)
        for _ in range(60):
            C = set(rng.sample(Vl, rng.randint(2, len(Vl))))
            lhs = sum((len(T)/len(E)) * (1 if x in C else 0) * (len(T & C)/len(T)) * (1 if len(T & C)/len(T) >= lam else 0)
                      for (x, r), T in R['fibers'].items() if T)
            cnt = 0
            for (x, r), T in R['fibers'].items():
                if T and x in C and len(T & C) >= lam*len(T):
                    for y in T & C:
                        cnt += 1
                        kC = sum(1 for z in C if z != x and d2(x, z) == r)
                        if not (kC >= len(T & C) >= lam*K): ok24 = False
            if abs(lhs*len(E) - cnt) > 1e-9: ok24 = False
        oks.append(("(2.4) counting identity + k_C >= |F_e∩C| >= lam*K on 60 random subsets", ok24))
    allok = all(o for _, o in oks)
    print(f"  [{label}] N={N} stop n={n} (m0={m0}) E0={R['E0']} |E|={len(E)} deletions={len(R['log'])} "
          f"fiber_cost={R['fiber_cost']} vertex_cost={R['vertex_cost']}: {'all invariants hold' if allok else 'VIOLATIONS: '+str([nm for nm, o in oks if not o])}")
    return allok

rng = random.Random(604)
grid = [(i, j) for i in range(12) for j in range(12)]
noise = set()
while len(noise) < 56:
    p = (rng.randint(100, 10**6), rng.randint(100, 10**6))
    noise.add(p)
P1 = grid + sorted(noise)                                            # N = 200
P2 = [(i, j) for i in range(14) for j in range(14)]                  # N = 196
P3 = [(i, j) for i in range(10) for j in range(10)] + [(i, j) for i in range(30, 36) for j in range(30, 36)]  # two grids, N=136
okC = True
for P, s_thr, K, a, lab in [(P1, 4, 3, 0.25, "grid12+56 random"), (P1, 4, 4, 0.20, "grid12+56 random b"),
                           (P2, 8, 6, 0.05, "grid14 hi"), (P2, 4, 6, 0.12, "grid14 collapsing"),
                           (P3, 3, 5, 0.08, "two grids collapsing")]:
    R = run_process(P, s_thr, K, a)
    okC &= invariants(R, K, a, s_thr, lab)
check("C: all invariants on 5 concrete runs", okC)
# Control: skip the cleanup after vertex deletions -> some surviving fiber drops below K (the check must see it)
R = run_process(P2, 8, 6, 0.05, mutate_skip_cleanup=True)
ctrl = invariants(R, 6, 0.05, 8, "CONTROL skip-cleanup")
check("C control: skip-cleanup run is REJECTED by the invariant checker", not ctrl)
print("OVERALL:", "ALL CHECKS PASS, ALL CONTROLS FAIL" if not fails else f"PROBLEMS: {fails}")
```

Output (verbatim):
```
PASS A: sum_{m=m0+1}^N 2(m-1) == A_N - B_N for 2<=N<=3000
PASS A control: sum from m0 is NOT A_N-B_N (control rejected)
   N=10: B_N/A_N = 0.222222
   N=100: B_N/A_N = 0.247475
   N=1000: B_N/A_N = 0.249750
   N=1000000: B_N/A_N = 0.250000
PASS B: excess >= eta(A-B) - t*A on 200000 exact random instances (and the factorisation identity)
PASS B control: with 1/log N dropped from t_N the excess inequality is FALSE (lhs < eta(A-B)-t*A)
  [grid12+56 random] N=200 stop n=114 (m0=100) E0=10424 |E|=7634 deletions=86 fiber_cost=422 vertex_cost=2368: all invariants hold
  [grid12+56 random b] N=200 stop n=144 (m0=100) E0=10424 |E|=10424 deletions=56 fiber_cost=0 vertex_cost=0: all invariants hold
  [grid14 hi] N=196 stop n=136 (m0=98) E0=3944 |E|=2824 deletions=60 fiber_cost=420 vertex_cost=700: all invariants hold
     [grid14 collapsing] m0-snapshot (first time vertex count = m0, after cleanup): |E|=1344 >= E0 - a(A-B) - cost = 360.3
  [grid14 collapsing] N=196 stop n=1 (m0=98) E0=20448 |E|=0 deletions=195 fiber_cost=17622 vertex_cost=2826: all invariants hold
     [two grids collapsing] m0-snapshot (first time vertex count = m0, after cleanup): |E|=95 >= E0 - a(A-B) - cost = -232.3
  [two grids collapsing] N=136 stop n=1 (m0=68) E0=7036 |E|=0 deletions=135 fiber_cost=6224 vertex_cost=812: all invariants hold
PASS C: all invariants on 5 concrete runs
  [CONTROL skip-cleanup] N=196 stop n=156 (m0=98) E0=3944 |E|=3468 deletions=40 fiber_cost=0 vertex_cost=476: VIOLATIONS: ['all surviving fibers have >= K edges', "every final edge has k_P'(x,y) >= K", '(2.4) counting identity + k_C >= |F_e∩C| >= lam*K on 60 random subsets']
PASS C control: skip-cleanup run is REJECTED by the invariant checker
OVERALL: ALL CHECKS PASS, ALL CONTROLS FAIL
```
