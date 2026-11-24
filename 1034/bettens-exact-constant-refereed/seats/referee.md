# Hostile referee report (Claude instance, Opus 5.5, briefed to refute), 2026-11-24

Paper: F. Bettens, "The Quantitative Constant in Erdős Problem #1034" (11 pp., 7 October 2026), Zenodo 23223509.

**Verdict: HOLDS WITH FIXES.** No FATAL objection, no GAP and no FALSE STEP. All fixes are wording; none changes
the argument. The reduction from graphs to graphons is correct, and the verifier computes what the paper says it
computes. Every one of its checks was run piecewise against the real certificate and all pass.

The seat did not run verify.py end to end (the orchestrator did, separately: CERTIFICATE VERIFIED in 63 s). It
imported a scratch copy (sha256 equal to the deposit's) under `python3 -I` and ran its parts separately.

## A. What was run (exact unless stated)

Costs: loading ~1 s; one residual 0.01–0.05 s; all 1044 residuals 50 s; exact PSD of the two dimension-48 blocks
(5, 7) 44 s and 34 s; the other blocks ≤ 8 s each; C2 basis check 0.6 s.

1. C4 positive spot checks: residual exactly 0 for the empty graph, K7, K_{3,4}, C7, K_{3,3}+K1 and a mixed graph.
2. C4 full: all 1044 residuals exactly 0 (their own `residual()`).
3. C3: all 82 blocks pass `check_psd`. Block 0 (the localizer) is positive definite (smallest float eigenvalue
   0.0256); the others have exact kernels (float minimum ≈ −3e−15 against a maximum of 81), as a tight certificate
   should. Signs of all 819 multipliers and 1044 slacks redone in 1200-digit Decimal: no negatives; 597 multipliers
   are zero; smallest positive slack 3.77e−3; β = 1.40535…
4. C2 passes. The 816 scalar localizers are exactly the set of all order-6 τ-flags (Burnside count
   (4096+768+32)/6 = 816; the descriptor set equals the enumerated set).
5. Semantic test independent of their expansion: each term of (31) evaluated at step graphons (a) as
   Σ_H coeff_H·p(H;W) with the verifier's per-graph coefficients and (b) directly from the paper's integral
   definitions (½t(K2), ∫r_σ vᵀQv, ∫r_τ(c*−D)vᵀQ₀v, Σλ_j∫r_τ(c*−D)F_j, β∫r_B(X³−11XE+30T+15P)).
   - At the extremal W* (S plus 6 cliques, α₆=(6+√3)/11), exactly: ρ = 1/4, every other term is exactly 0, the
     constant is −1/4. The 1004 positive slacks all sit on graphs with p(H;W*) = 0; the 40 zero slacks are exactly
     W*'s 40-graph support — the signature of a correct, tight certificate.
   - On 9 random 0/1 step graphons with 3–7 parts, (a) = (b) exactly, term by term.
   - Negative control: doubling the off-diagonal Q weights on the direct side breaks equality (2.3314 vs 2.4535).
6. Adversarial searches for a counterexample to the theorem (not using the certificate): minimise max D over
   triangles subject to ρ ≥ 1/4 + 1e−4. S plus unequal cliques: optimum always at the equal-size endpoint (c₆).
   All 256 one-part extensions of W*: best 0.414528 > c* = 0.414239. 1633 random templates of 4–8 parts: best
   0.43686. No counterexample. (A first run that allowed ρ = 1/4 exactly found 0 via the triangle-free bipartite
   graphon — the seat's artefact.)
7. Lemma 3.1 numerically: min of 1 − 11Σx² + 30Σx³ over simplices up to dimension 12 (2400 starts) ≈ 8e−12;
   min of 20 − 34q + 15τ over 20,000 random weighted graphs 0.0089.
8. §2 arithmetic exact in Q(√3): α₆ − (11/12)α₆² = 1/4; c₆ = 1 − (5/6)α₆ = (36−5√3)/66; c₆ < 83/200;
   c₅ > 83/200 (1265² = 1600225 > 1600000); the derivative (x²−4x+2)/(2x²(x−1)²) is correct, zero at m = 3+2√2.

## B. Negative controls on verify.py (each goes red)

| Mutation | Result |
|---|---|
| slack[144] += 1e−6 | C7 residual becomes 1/10⁶ |
| λ₅ += 1/1000 | residual on F₅+isolated vertex nonzero |
| block-5 entry (3,1)/(1,3) += 1/1000, symmetric | residuals nonzero at graphs 7, 13, 14 |
| block-0 (localizer) entry (2,2) += 1/1000 | residuals nonzero at graphs 21, 42, 43 |
| c* += 1e−9·√3 (bypassing the pin) | K7 residual nonzero |
| c* edited in the JSON | rejected: "Unexpected c_star" |
| β += 1e−6 | graph 677 residual = −1/39375000 |
| target bound 26/100; scalars[818] = 26/100 | both rejected |
| D loses its all-three-neighbours flag; Bollobás −11 → −10; ρ coefficient 1/3 | all rejected |
| block-12 [0][0] −= 1e−30 | "Negative LDL pivot" |
| asymmetric edit | "Nonsymmetric matrix" |
| block-3 off-diagonal ×4 | fails |
| block-3 off-diagonal ×3 | passes — the matrix is genuinely still PSD (det ≈ 0.119 − 0.0997 > 0); a weak control |
| basis minus one graph | "incomplete" |
| a graph replaced by a relabelled copy of another | "Duplicate" |

Primitives against independent oracles: `check_psd` agrees with an exact all-principal-minors oracle on 2000/2000
random matrices over Q(√3) (singular and perturbed included) and with numpy on all 2229 matrices whose verdict is
unambiguous in floating point. `Q.sign` agrees with 1200-digit Decimal on 200,000 cases incl. near-cancellations.

## C. Code audit against §6.1 (C1–C4) — none is a fault

- `quadratic_weights`: the factor 2 for i>j followed by halving for a≠b is right, because `flag_quadratics`
  counts both ordered events under the sorted key (also confirmed by the semantic test, which goes red under a
  factor-2 mutation).
- Localizer, c* times terms with fewer vertices: sampling (roots, left, right, extra) uniformly projects to
  uniform (roots, left, right); denominators 210·24 and 210·4 correct.
- Canonical forms keep roots fixed and permute only free vertices; types are labelled masks matched exactly
  (edges and non-edges), matching r_σ with its (1−W) factors.
- Bollobás sampler: subset sizes (1,1,1), (1,2), (3), (3) match X³, XE, T, P3; sector = adjacency to roots 0, 1;
  edges counted within each subset only.
- Objective ½·(edge fraction); constant pinned to −1/4.
- `check_psd` is a correct LDLᵀ test on the lower triangle after the symmetry check, with the zero-pivot/zero-column rule.
- `check_graph_basis`: min over degree-respecting orderings is a valid canonical form; the number of orderings
  attaining it equals |Aut|; completeness by orbit counting.
- No silent pass: `require` (not `assert`), worker exceptions re-raise, "CERTIFICATE VERIFIED" prints last.
- The one check that can only say pass is the provenance-hash string comparison (FIX-1); not load-bearing.

## D. Objections (page numbers as printed)

- **FIX-1 (p.9, §6.3).** "The verifier checks that the provenance hash stored in the portable witness matches the
  fixed identifier above." In code this compares two stored strings to a literal; no hash is computed and the
  Sage pickle is not included, so it cannot detect any change to the witness. Reword.
- **FIX-2 (p.4, §3).** "Applying (12) after normalizing the measure w(x) dx and multiplying by X³ gives". Lemma
  3.1 is stated for graphons on [0,1] with Lebesgue measure; here it is applied on ([0,1], w dx/X). One sentence:
  the G(N,W) proof works verbatim on any probability space. Small X is harmless (homogeneous), X = 0 trivial.
- **FIX-3 (p.4, proof of Lemma 3.1).** "Moving all their weight to one of the two endpoints cannot increase this
  expression." Should say the better of the two endpoints (the expression is affine). The rest checks: merging
  identity ψ(a)+ψ(b) = ψ(s)+(22−90s)ab, threshold s > 11/45, equalisation, (k−5)(k−6)/k² ≥ 0, expectation
  factors; (11)→(12) via independent-triple density 1−3e+p+2t.
- **FIX-4 (p.8, §5).** "every positive-measure rooting of W_G in the three cells corresponding to T satisfies
  D(W_G;T) = |Y+_G(T)|/n". Single rootings have measure zero; it means every x in the product of the three cells;
  "D(W_G;T)" clashes with D(W,x). Content right; the transfer supplies (27) everywhere on the support of r_τ dx.
- **FIX-5 (p.3, §2).** Implicit steps: h(n) ≤ max_T |Y_G(T)| = max_T |Y⁺_G(T)| − 3 ≤ (c*+ε)n; explicit error
  bounds e(G) ≥ (n−b)b + b²/12 − b/2 and |K(T)| ≤ ⌈b/6⌉. Both correct; one line each.
- NOTE-6 (p.2): for m = 2, α₂ = 1 is not in (0,1); the m-comparison is not load-bearing (only m = 6 is used).
- NOTE-7: the attribution of 2−√(5/2) to Ma–Tang and the problem's wording on erdosproblems.com not checked by
  this seat (wall respected); the limit is insensitive to counting T's own vertices (the ±3).
- NOTE-8 (Thm 1.1): |Y⁺| ≥ c*n is in fact strict (c*n irrational). Harmless.
- NOTE-9 (§6): 597 of the 819 scalar coordinates are 0; the 816 F_j are all order-6 τ-flags.
- NOTE-10 (§6.1): "independent standard-library Python verifier" means independent of FlagAlgebraToolbox, not
  of the author. The other seat's re-implementation supplies real independence.

## E. Answers

§2 correct incl. Y⁺ vs Y and the −3. Lemma 3.1, (12)–(14), B5root correct. Normalisations, Lemma 4.1, (20),
(21), (28) correct; localizers need (c*−D) ≥ 0 only r_τ-a.e., the transfer supplies it everywhere on the support.
(26), ρ(W_G) = e(G)/n², h(n) ≥ ⌈c*n⌉ − 3 correct. (31) as evaluated gives 1/4 − ρ(W) = sum of nonnegative terms;
all signs and PSD confirmed exactly. The theorem follows; nothing unproved is assumed.

Residual risk noted by the seat: its C2–C4 runs used the author's functions on the real data; mitigated by the
exact semantic agreement and the term-by-term vanishing at W*, and by the separate clean-room verifier
(second-verifier/).
