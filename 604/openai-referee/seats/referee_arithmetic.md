# Hostile referee report — seat `arithmetic` — §3 of "The weak pinned planar distance theorem" (OpenAI, 23 Sep 2026)

Paper: /tmp/oaimath/604/paper.pdf, sha256 6350959db2b8310fdad1792ad04d4f8d64d6c030808cb6d00b29eb66513789f0.
Every displayed formula in scope was read from the rendered PDF (pp. 8–12), not from paper.txt.
Primary source fetched: Milne, *Algebraic Number Theory* v3.08 (July 19, 2020), https://www.jmilne.org/math/CourseNotes/ANTc.pdf,
sha256 de2066ee7a319c0e6e521895a7e9e9567c2804bcafc0c8e67c417e508f2bc26b (saved /tmp/oaimath/604/seats/arith_dl/ANTc.pdf, text ANTc.txt).
Scripts: /tmp/oaimath/604/seats/arith_scripts/ (all runs < 35 s, < 300 MB). No lean/lake was run; Lean sources were read as text only.

Scope: §3 in full — §3.1 (Z₁, Z₂, (3.1), (3.2), (3.3)); §3.2 (nested grids, Lemma 3.1, (3.4)); §3.3 (giant replacement, Figure 1,
Lemma 3.2, (3.5)); §3.4 (⟨·⟩, 𝓘, (3.6), (3.7)) — and brief items (iii), (iv); brief (i) only as it bears on §3.

---------------------------------------------------------------------------------------------------------------------------

## VERDICT FOR MY SCOPE: HOLDS AS READ.

No FATAL, no GAP. Five COSMETIC/UNCLEAR exposition items (objections 1–5) and one structural NOTE (objection 6, relevant to brief (i)).
Every step of Lemma 3.1 and Lemma 3.2 was re-derived by hand, and checked numerically/exactly with controls that fail:
- Lemma 3.1: the law of Δ = d − i is pair-independent (KS p = 0.40–0.82 across pairs with R from 0.0037 to 317 and different
  angles and base points; the A/A calibration rerun gives p = 0.43). Removing any one randomization makes the law depend on the
  pair (KS p ≤ 3e−94). κ = −1.4572 (quadrature) vs −1.4584 ± 0.0017 (Monte Carlo, 400k samples). (3.4) holds with C₀ = 2√2, b₀ = 1;
  the true lower-tail constant is (4/π)/ln 2 ≈ 1.837 < 2√2.
- Lemma 3.2 / (3.5): exact (Fraction/integer) agreement on Figure 1, on 3,000 random hierarchies with ties, on 30,000 realized
  complex-place grid hierarchies and on 20 p-adic (Gaussian-prime) hierarchies. The set-instead-of-multiset control fails exactly on
  the Figure 1 pairs and on 1,042 of the 3,000 random hierarchies.
- (3.2)+(3.5)+Lemma 3.1 ⇒ (3.6) end to end on an explicit 7-point configuration in K = ℚ(i) with all 10 relevant finite places:
  L*(x,y) − S*(x) − S*(y) is constant across all 21 pairs to Monte-Carlo accuracy (spread 0.050 at 15k grids, down from 0.129 at 3k,
  i.e. shrinking like N^{-1/2}). It is not constant under the three wrong normalizations: dropping the finite places gives spread
  3.37, Milne-normalized |·|_𝔭 with the paper's weights gives 2.92, and the complex weight without the factor 2 gives 1.69.
- (3.2) against Milne: MATCH (Theorems 7.14, 7.15 and Lemma 8.6, quoted below).

---------------------------------------------------------------------------------------------------------------------------

## STATUS TABLE (the deliverable)

| Item | Status |
|---|---|
| §3.1 definition of Z₁, Z₂; injectivity; "nonzero under every embedding" | VERIFIED LINE BY LINE |
| (3.1) factorization t(x,y) = (Z₁(y)−Z₁(x))(Z₂(y)−Z₂(x)) | VERIFIED LINE BY LINE |
| "All archimedean places are complex, since i ∈ K"; σ_v definitions | VERIFIED LINE BY LINE |
| (3.2) normalized product formula + Σ_{v∣∞}σ_v = 1, against Milne v3.08 Thm 7.14, 7.15, Lemma 8.6 | VERIFIED LINE BY LINE + source quoted + numeric end-to-end check |
| "only finitely many finite places make any coordinate difference a nonunit" | VERIFIED |
| raw depths i_j; (3.3) i₁+i₂ = h_e on a fiber; h_e finite | VERIFIED LINE BY LINE |
| §3.2 finite-place hierarchy (ultrametric ⇒ equivalence relation) | VERIFIED LINE BY LINE |
| §3.2 random grid construction: per-scale uniformity, nesting (m ≥ 0 and m < 0) | VERIFIED LINE BY LINE + nesting assert (0/30,000 violations; control with non-nested shifts violates 1,866/2,000) |
| Lemma 3.1: a.s. finiteness | VERIFIED LINE BY LINE |
| Lemma 3.1: upper bound Δ ≤ log√2 | VERIFIED LINE BY LINE (max over 400k MC samples 0.291 < 0.347) |
| Lemma 3.1: lower tail Pr(Δ<−u) ≤ 2√2e^{−u}; (3.4) two-sided | VERIFIED LINE BY LINE (the u < log√2 range is implicit, see obj. 4) + MC + quadrature |
| Lemma 3.1: pair/place/configuration independence of the law of Δ | VERIFIED LINE BY LINE (CDF reduction to a single scale via nesting) + MC with 4 failing controls |
| Lemma 3.1: finite mean κ, measurability | VERIFIED (κ ≈ −1.4572) |
| §3.3 giant definition, uniqueness, multiset 𝒞_j(r), α(C) ≤ 1/2 | VERIFIED LINE BY LINE |
| Figure 1 | VERIFIED (exact recomputation: M=3, S(6)=2, L(6,7)=3, d(6,7)=2) |
| Lemma 3.2 "initial ray" claim, M ∈ [d₋,d₊] | VERIFIED LINE BY LINE + exact check (0 non-ray giant sets in 3,000) |
| Lemma 3.2 pointwise identity o−g = t − 1{x∉G} − 1{y∉G} and its integration ⇒ (3.5) | VERIFIED LINE BY LINE + exact checks |
| Lemma 3.2 bounds 0≤S≤d₊−d₋, 0≤L≤2(d₊−d₋), ∣M∣≤max(∣d₋∣,∣d₊∣); integrability; unit-place vanishing | VERIFIED LINE BY LINE |
| §3.4 ⟨·⟩, 𝓘(g) notation; finiteness of S*, L*, ⟨M₁+M₂⟩ | VERIFIED |
| ⟨d₁(x,y)+d₂(x,y)⟩ = 2κ | VERIFIED LINE BY LINE (stronger per-j form holds, obj. 6) + numeric |
| (3.6) additive identity and its "signed law" consequence | VERIFIED LINE BY LINE + end-to-end numeric with 3 failing controls |
| (3.7) W₂ = 𝓘(π(C²)) = E_π L*, A, W; nonnegativity | VERIFIED LINE BY LINE (Tonelli on a nonnegative integrand) |
| first line of §4, W₂ = b* + 2A and the E_q L* formula (consumers of (3.6)) | VERIFIED (algebra only; the rest of §4 is NOT READ, other seat) |

---------------------------------------------------------------------------------------------------------------------------

## OBJECTIONS

**1. §3.2, p. 9 — independence of the two axis shifts is not stated, but the sharing formula needs it. COSMETIC (exposition).**
Quote (p. 9): "Choose a shift uniform modulo l₀ in each oriented axis. To obtain the shift modulo l_{m+1} from that modulo l_m,
for m ≥ 0, add either 0 or l_m with equal probabilities, independently at every step and in each axis."
Quote (p. 10, proof of Lemma 3.1): "At side length l, a uniform shift gives sharing probability (1 − |a|/l)₊(1 − |b|/l)₊."
The product form requires the shift pair to be uniform on the torus (ℝ/lℤ)², i.e. the two initial axis shifts must be independent.
The text states independence for the bits and leaves the initial shifts ambiguous.
Control (mc_delta.py, mode `sameshift`, which uses one common shift for both axes and keeps everything else random): two pairs with
the *same* displacement but different base points get different laws, KS D = 0.046, p = 2.9e−94. The paper's construction on the
same two pairs gives p = 0.82.
So the reading matters, and the natural reading (independent axes) is the correct one. The Lean also uses it:
RandomGrids.lean line 342 has `def squareLaw : Measure GridSample := axisLaw.prod axisLaw`, documented at line 340 as "Both
independent axis constructions". Line 109's lemma `square_shares_integral` reads "Independent uniform shifts in the two axes give a
product of overlap lengths".
Fix: write "independent uniform shifts modulo l₀ in the two oriented axes".

**2. §3.2 / §3.4 — the joint law of the grid families across coordinates j and across complex places is never specified.
COSMETIC/UNCLEAR (exposition; harmless).**
Quote (p. 9): "Use such a grid family for each coordinate j."
Quote (p. 11): "⟨H⟩ = Σ_v σ_v E_grids H".
Within §3 only per-(place, coordinate) marginal laws are used. ⟨·⟩ is a weighted sum of separate expectations, and (3.5) is
pathwise. So any coupling works. I checked downstream: §4 explicitly disclaims the need for independence (paper.txt line 680, "No
independence of the two errors is required."). Grid–vertex independence is stated ("Independently of all vertex and fiber
sampling"), and §6 uses it (line 1078).
Fix: one sentence, e.g. "all grid families (over places and j) are independent; only their marginals are used."

**3. §3.1 — which of the two conjugate embeddings carries the grids at a complex place is unspecified. COSMETIC.**
Quote (p. 9): "All archimedean places are complex, since i ∈ K; there use ordinary complex modulus and σ_v = 2/[K : ℚ]."
The modulus is the same for σ and σ̄, so i_j is well defined. The grid, however, acts on σ_v(Z_j(x)) ∈ ℂ, which needs a choice. The two
choices differ by a reflection. The grid law is reflection-invariant (uniform orientation, Haar shift), so every expectation is
unchanged. Harmless. Fix: "fix one embedding in each conjugate pair."

**4. Lemma 3.1 proof, p. 10 — two small imprecisions. COSMETIC.**
(a) Quote: "Sharing is impossible if l < R/√2". The correct condition is l ≤ R/√2, because a half-open square of side l has diameter
l√2 and that diameter is not attained. It is harmless either way.
(b) Quote: "This proves (3.4) and a uniform first absolute moment." The argument proves Pr(Δ < −u) ≤ 2√2e^{−u} for u ≥ 0 and Δ ≤ log√2.
Two-sided (3.4) then needs Pr(Δ > u) = 0 for u ≥ log√2, which is given. For 0 ≤ u < log√2 one needs C₀e^{−b₀u} ≥ 1, which holds with
C₀ = 2√2, b₀ = 1 (since 2√2·e^{−log√2} = 2). Correct but unstated.
Numerically, Pr(Δ ≥ 0) = 0.0050, Pr(Δ ≥ 0.3) = 1.4e−6, max MC Δ = 0.291 < log√2 = 0.347.
The lower-tail bound is not tight but valid: e^u·Pr(Δ<−u) → (4/π)/ln2 = 1.8369 < 2√2 = 2.83 (quadrature 1.83687 at u = 10; MC 1.83–1.86).

**5. Citation bookkeeping for [11]. COSMETIC.**
The paper cites Milne three ways:
- p. 3: "[11, Theorem 7.15]";
- p. 9: "[11, Theorems 7.14–7.15 and Lemma 8.6]";
- bibliography: "Version 3.08, Theorem 7.15 and Lemma 8.6".
All three are correct items (see the citation table). One step is not literally in the cited items: Σ_{v∣∞}σ_v = 1 uses
r₁ + 2r₂ = [K:ℚ]. Milne v3.08 states it elsewhere ("Thus n = r + 2s", ANTc.txt line 4080; also "r + 2s = [K:ℚ]", line 4354). Trivial.

**6. NOTE (not an error; bears on brief (i)) — (3.6) is a one-coordinate fact; the Euclidean pairing of Z₁ with Z₂ is NOT used in §3.4.**
Quote (p. 12): "For each distinct pair, the product formula and Lemma 3.1 give ⟨d₁(x,y) + d₂(x,y)⟩ = 2κ."
A stronger statement holds: ⟨d_j(x,y)⟩ = κ for each j separately. The reason is that ⟨i_j(x,y)⟩ = −Σ_v σ_v log|Z_j(x)−Z_j(y)|_v = 0 by
(3.2) applied to the single nonzero element Z_j(x) − Z_j(y). Hence L_j*(x,y) = κ − ⟨M_j⟩ + S_j*(x) + S_j*(y) for each j.
Consequences for the "characteristic-zero input" audit:
- In §3 the factorization (3.1) enters ONLY through the fiber identity (3.3).
- (3.5) and (3.6) hold verbatim for ANY finite set of distinct elements of ANY number field under ANY injective coordinate map.
  K ∋ i is not even needed for pair-independence. With real places and 1-D grids, Σ_{v∣∞}σ_vEΔ would be the pair-independent number
  (r₁κ_ℝ + 2r₂κ_ℂ)/[K:ℚ].
- In a global function field (no archimedean place) (3.6) holds with the κ term absent.
- For a constant set such as F_q² ⊂ F_q(T)², every difference is a unit at every place, so M = S = L = 0 and W = 0. Nothing in §3
  rules this out. The F_q obstruction must be excluded downstream: §7 needs an archimedean place, and §7 is not my scope.
The Euclidean/real/arithmetic inputs actually used in §3 are:
- (a) injectivity of Z₁ and Z₂ on P. Reality of u, b means no two points lie on a common isotropic line u ± ib = const. This also
  gives t(x,y) ≠ 0 and finite h_e.
- (b) the product formula in a number field.
- (c) the existence of archimedean places with Σ_{v∣∞}σ_v = 1, which only fixes the constant 2κ.
Hand to the `whole` seat. Severity: none.

No other objection. In particular I looked for these and found them NOT present:
- a wrong sign of S in (3.5);
- a missing multiplicity;
- a non-initial-ray giant set;
- a configuration-dependent κ or C₀, b₀;
- a two-sided tail claimed but one-sided proved (the other side is deterministic);
- a normalization off by the complex factor 2 or by [K_v:ℚ_p].

---------------------------------------------------------------------------------------------------------------------------

## LINE-BY-LINE DERIVATIONS (what I checked, in order)

**§3.1.**
- x = (u,b) with u, b real algebraic. Z₁ = u+ib, Z₂ = u−ib. Injective: if u+ib = u′+ib′ with u,b,u′,b′ real, then u = u′ and b = b′.
- (3.1): (Δu+iΔb)(Δu−iΔb) = Δu²+Δb², using i² = −1 in K under every embedding.
- Nonzero under every embedding: embeddings are injective ring maps.
- i ∈ K ⇒ no real embedding, since φ(i)² = −1 has no real solution. Hence r₁ = 0. The Lean has the same argument as
  `totallyComplex_of_sq_neg_one`.
- (3.3): i₁(x_e,y) + i₂(x_e,y) = −log|(Z₁(x_e)−Z₁(y))(Z₂(x_e)−Z₂(y))|_v = −log|t(x_e,y)|_v. Here t(x_e,y) = t_e for y ∈ F_e, because a
  fiber is "same source and same squared distance" (p. 5). h_e is finite because t_e ≠ 0. ✓

**(3.2) normalization.**
- Finite place v over p: Milne's normalized ‖a‖_v = (1/N𝔭)^{ord𝔭 a}. By Lemma 8.6 with K = ℚ_p and L = K_v, ‖a‖_v = |a|_v^{[K_v:ℚ_p]},
  where |·|_v is the unique extension of |·|_p (|p|_p = 1/p). So log‖a‖_v = [K_v:ℚ_p] log|a|_v.
- Complex place: ‖a‖_v = |σa|², so log‖a‖_v = 2 log|σa|.
- Theorem 7.15 gives Σ_v log‖a‖_v = 0. Dividing by [K:ℚ] gives Σ_v σ_v log|a|_v = 0, with σ_v = [K_v:ℚ_p]/[K:ℚ] at finite places
  and 2/[K:ℚ] at complex places — exactly the paper's choice.
- Σ_{v∣∞}σ_v = 2r₂/[K:ℚ] = 1 since r₁ = 0.
- "Only finitely many finite places make a coordinate difference a nonunit": each nonzero element has finite support of ord𝔭, and
  there are finitely many differences. ✓
- The Lean takes the equivalent route: Mathlib's norm-normalized FinitePlace with weight 1/[K:ℚ], and `archWeight v = v.mult/[K:ℚ]`
  (ProductFormula.lean, `normalized_log_product_formula`, `sum_archWeight`). At a finite place, rescaling the depth by [K_v:ℚ_p] rescales
  r, M, S, L by the same factor, so every weighted quantity agrees with the paper's.

**§3.2 construction.**
- Uniformity: if s_m ~ U[0,l_m) and an independent fair bit adds 0 or l_m, then s_{m+1} ~ U[0,2l_m) = U[0,l_{m+1}). For m < 0,
  s₀ mod l_m is uniform because l_m divides l₀.
- Nesting: s_{m+1} ≡ s_m (mod l_m) for m ≥ 0. For m ≤ 0, s_{m−1} = s₀ mod l_{m−1} ≡ s_m (mod l_{m−1}) because l_{m−1} | l_m. So
  every cell of side l_m is a union of four cells of side l_{m−1}. ✓
- Finite places: |·|_v is ultrametric and d(x,x) = +∞, so {d ≥ r} is an equivalence relation. ✓

**Lemma 3.1, line by line.**
- Notation: R = |σZ_j(x) − σZ_j(y)| > 0, and (a,b) is the displacement in grid axes, so |a|+|b| ≤ √2R.
- One-axis sharing probability with a uniform shift is (1−|a|/l)₊. Two independent axes give the product (see obj. 1).
- Sharing needs l > R/√2. Separation probability = 1 − (1−x)₊(1−y)₊ ≤ x+y.
- Nesting makes the separation events decreasing in the scale. Their probabilities → 0 as l → ∞, so the pair shares at some scale
  a.s., and a smallest sharing scale l* exists (it is bounded below by R/√2).
- Δ = d − i = −log l* + log R. The bound l* > R/√2 gives Δ < log√2.
- For u ≥ 0 let l be the largest side ≤ Re^u. Then l > Re^u/2, and {Δ<−u} = {l* > Re^u} ⊂ {separated at l}. Its probability is
  ≤ √2R/l < 2√2e^{−u}. ✓
- Pair-independence. {Δ ≥ u} = {l* ≤ Re^{−u}}. By nesting this equals {share at the largest side l ≤ Re^{−u}}: a SINGLE-scale
  event. That is the key point: only one-scale marginals of the shift enter, never the joint shift process.
- Given (θ, ξ), its probability is (1−|cos φ|/ρ)₊(1−|sin φ|/ρ)₊, with ρ = l/R and φ = the displacement angle relative to the axes.
- ρ = e^{−u}2^{−U}, where U = frac((−u−ξ+log R)/log 2) is uniform because ξ is uniform on [0, log 2). φ is uniform because θ is,
  and φ is independent of U.
- So Pr(Δ ≥ u) is a universal function of u: the CDF, hence the whole law, is pair-, place- and configuration-free. ✓
- Measurability: countably many scales and finitely many cell tests. ✓
- κ finite: Δ is bounded above and has an exponential lower tail. ✓

**§3.3.**
- Giant: size > n/2, hence unique. The complement has size < n/2 and every other cell has size ≤ n/2, so α(C) ≤ 1/2. ✓
- Ancestor of a giant is a giant ⇒ the existence set is a ray (−∞, M]. For r < d₋ the only cell is P, which is a giant since n ≥ 2;
  for r > d₊ all cells are singletons, and 1 ≤ n/2, so there is no giant. Hence M ∈ [d₋, d₊]. ✓
- Pointwise identity when G exists: t = Σ_{C≠G} 1_C(x)1_C(y) + 1_{Gᶜ}(x)1_{Gᶜ}(y) = o − 1_G(x)1_G(y) + 1_{Gᶜ}(x)1_{Gᶜ}(y). Expanding
  1_G = 1 − 1_{Gᶜ} gives t = o − 1 + 1_{Gᶜ}(x) + 1_{Gᶜ}(y). This is exactly o − g = t − 1{x∉G} − 1{y∉G}.
- The derivation counts Gᶜ as an occurrence in addition to Π∖{G}, so when Gᶜ coincides with a cell the multiset doubling is REQUIRED.
  Figure 1 is that case. Without the doubling the identity fails, as my control shows.
- When there is no giant, t = o and g = 0. ✓
- ∫(o − g)dr = d − M: the difference of two indicators of rays (−∞,d] and (−∞,M].
- t vanishes off [d₋,d₊] on a distinct pair: for r < d₋, 𝒞 = {∅}. t ≤ 2, since x lies in at most one cell of Π∖{G} plus possibly Gᶜ.
- S(x) is supported in [d₋, M]. The bounds follow; integrability comes from E|d| ≤ |i| + E|Δ| < ∞ over finitely many pairs.
- At an all-unit finite place, d₋ = d₊ = 0 ⇒ M = S = L = 0. ✓

**§3.4.**
- ⟨d_j(x,y)⟩ = Σ_v σ_v i_j + Σ_{v∣∞} σ_v EΔ = 0 + κ. This is a finite sum.
- Taking ⟨·⟩ of (3.5) summed over j gives L* = 2κ − ⟨M₁+M₂⟩ + S*(x) + S*(y). Every term is finite: finitely many contributing places,
  each grid-integrable. ✓
- Signed law ν with ν_X + ν_Y = 0: ∫L*dν = b*·ν(total) + Σ_x S*(x)(ν_X+ν_Y)(x) = 0. The zero-total-mass hypothesis is implied by the
  marginal hypothesis, so it is redundant but harmless. ✓
- (3.7): Σ_{C∈𝒞_j(r)} π(C²) = E_π t_j(r), with π on distinct ordered pairs. By Tonelli, 𝓘(π(C²)) = E_π L*. W₂, A ≥ 0. ✓
- Downstream consumers (algebra only): E_π gives W₂ = b* + 2A, using π-marginals = α. For q on distinct pairs,
  E_q L* = b* + Σ_x(q_X+q_Y)(x)S*(x) = W₂ + Σ_x(q_X+q_Y−2α)(x)S*(x). ✓

**Hand-wave inventory in §3.** 17 "thus/therefore/consequently/it follows"-type steps; each was checked. The only load-bearing one is
p. 10, "The sharing formula therefore makes the entire law of Δ independent of the pair." It is valid, but terse: the reader must
supply that nesting reduces {Δ ≥ u} to one scale, which the paper does say in the previous sentence. The others are routine. None is
wrong.

---------------------------------------------------------------------------------------------------------------------------

## CITATION TABLE (my scope)

| Cited | Paper's claim | Source says (quote, Milne v3.08 ANTc.pdf) | Verdict |
|---|---|---|---|
| [11, Thm 7.14] (p. 9) | places of K = prime ideals + complex places (no real ones since i ∈ K) | p. 111: "THEOREM 7.14 Let K be an algebraic number field. There exists exactly one prime of K (a) for each prime ideal p; (b) for each real embedding; (c) for each conjugate pair of complex embeddings." | MATCH |
| [11, Thm 7.15] (pp. 3, 9) | product formula, in the paper's normalization after division by [K:ℚ] | p. 112: "for a prime ideal p of O_K, \|a\|_p = (1/Np)^{ord_p(a)} … for a nonreal complex embedding σ: K ↪ ℂ, \|a\| = \|σa\|². … THEOREM 7.15 (PRODUCT FORMULA) For each prime v, let \|·\|_v be the normalized absolute value. For every nonzero α ∈ K, ∏ \|α\|_v = 1 (product over all primes of K)." | MATCH |
| [11, Lemma 8.6] (p. 9) | converts the norm-normalized finite absolute value to the one extending \|p\|_p = 1/p | p. 137: "Let L be a finite separable extension of K, and let \|·\| be the unique extension of \|·\| to L. Let ‖·‖ be the normalized absolute value on L corresponding to \|·\|. … LEMMA 8.6 In the above situation, ‖a‖ = \|a\|^n, where n = [L:K]." (with K = ℚ_p, L = K_v: ‖a‖_v = \|a\|_v^{[K_v:ℚ_p]}) | MATCH |
| (implicit) Σ_{v∣∞}σ_v = 1 | r₁ = 0, 2r₂ = [K:ℚ] | ANTc.txt l. 4080: "… 2s complex embedding … Thus n = r + 2s." | MATCH (not in the cited items; standard) |
| [1, Section 2.1] Arora (p. 9) | "Randomly shifted recursive square dissections also appear" | not fetched: Arora's homepage PDF URL returned HTML; JACM is paywalled | COULD NOT FETCH — decorative, not load-bearing (left to the `sources` seat) |

The paper's sentence "The weights convert the norm-based finite absolute values and squared complex moduli in that reference to the
absolute values used here, after division by [K : ℚ]" is exactly right, by the computation in "(3.2) normalization" above.

---------------------------------------------------------------------------------------------------------------------------

## FINITE CHECKS (scripts verbatim, outputs verbatim, failing controls)

All scripts are in /tmp/oaimath/604/seats/arith_scripts/ and were run as `python3 -P <script>` from that directory. They read no
downloaded files.

| Script | md5 |
|---|---|
| mc_delta.py | e30b302216372e02a19130d33eefce15 |
| kappa_quad.py | 1fb0b49aa2e7fe7be5e9edcb329208ec |
| exact_35.py | cba12aefb474679971028318ba89946f |
| endtoend_36.py | d4c57f817fe651043684757295595d22 |
| nest_control.py | 1a4202e793c281042c1de20d6057ea2d |

### Check A — Lemma 3.1 Monte Carlo (mc_delta.py, N = 100,000 per pair)

Paper construction: four pairs, R ∈ {1, 317.3, 0.0037, √2}, different angles and base points.

Controls, which SHOULD make the law pair-dependent:
- `fixed`: deterministic grid. The law is a point mass that depends on the pair, and a pair straddling the line u = 0 never shares at
  all.
- `noxi`: no log-uniform phase. KS for R = 1 vs R = √2 gives D = 0.215.
- `norot`: no random orientation. KS for angle 0 vs angle π/4 gives D = 0.083.
- `sameshift`: one shift for both axes. KS for the same displacement at different base points gives D = 0.046.

All four controls reject at p ≤ 3e−94, while the paper's construction is accepted at p ≥ 0.40.

```python
# Monte Carlo of Lemma 3.1 (paper p.9-10): law of Delta = d - i for the random nested grids of Sec 3.2.
# Faithful construction: uniform orientation theta, xi ~ U[0,log2), l_m = e^xi 2^m, shift s0 uniform mod l0 per axis,
# s_{m+1} = s_m + B_m l_m (B_m fair bit, per axis) for m>=0, s_m = s0 mod l_m for m<0. d = -log(smallest sharing side),
# i = -log R, Delta = d - i = log(R / l*).
# Controls (each removes one randomisation; the law should then DEPEND on the pair):
#   'fixed'   : theta=0, xi=0, shift=0 (deterministic grid)
#   'noxi'    : xi=0 (no log-uniform scale), rest random
#   'norot'   : theta=0 (no random orientation), rest random
import numpy as np, sys
from scipy.stats import ks_2samp
LOG2 = np.log(2.0)

def sample_delta(p, q, N, rng, mode='paper'):
    p = np.asarray(p, float); q = np.asarray(q, float)
    R = np.hypot(*(q - p))
    th = rng.uniform(0, 2*np.pi, N) if mode in ('paper', 'noxi', 'sameshift') else np.zeros(N)
    xi = rng.uniform(0, LOG2, N) if mode in ('paper', 'norot', 'sameshift') else np.zeros(N)
    c, s = np.cos(th), np.sin(th)
    # coordinates along the oriented axes (axis1 = (c,s), axis2 = (-s,c))
    P1 = p[0]*c + p[1]*s; P2 = -p[0]*s + p[1]*c
    Q1 = q[0]*c + q[1]*s; Q2 = -q[0]*s + q[1]*c
    l0 = np.exp(xi)
    if mode == 'fixed':
        s0 = np.zeros((N, 2))
    elif mode == 'sameshift':        # control: ONE shift used for both axes (not uniform on the torus)
        s0 = np.repeat(rng.uniform(0, 1, (N, 1)), 2, axis=1) * l0[:, None]
    else:
        s0 = rng.uniform(0, 1, (N, 2)) * l0[:, None]
    mlo = int(np.floor(np.log2(R/np.sqrt(2)))) - 2
    mhi = mlo + 60
    first = np.full(N, np.nan)
    # shifts for m>0 built incrementally from s0 with fresh fair bits
    sm_pos = s0.copy()          # s_0
    for m in range(mlo, mhi):
        l = l0 * 2.0**m
        if m <= 0:
            sm = np.mod(s0, l[:, None])
        else:
            if mode == 'fixed':
                bits = np.zeros((N, 2))
            else:
                bits = rng.integers(0, 2, (N, 2)).astype(float)
                if mode == 'sameshift': bits[:, 1] = bits[:, 0]
            sm_pos = sm_pos + bits * (l0 * 2.0**(m-1))[:, None]   # s_m = s_{m-1} + B l_{m-1}
            sm = sm_pos
        a1 = np.floor((P1 - sm[:, 0]) / l); b1 = np.floor((Q1 - sm[:, 0]) / l)
        a2 = np.floor((P2 - sm[:, 1]) / l); b2 = np.floor((Q2 - sm[:, 1]) / l)
        share = (a1 == b1) & (a2 == b2) & np.isnan(first)
        first[share] = np.log(l[share])
    if np.isnan(first).any():
        print(f"    [{mode}] {np.isnan(first).mean():.3f} of samples NEVER share a cell up to side 2^{mhi} (Delta=-inf)")
        first[np.isnan(first)] = np.inf
    return np.log(R) - first      # Delta = log(R/l*)

def report(tag, D):
    D = D[np.isfinite(D)] if np.isfinite(D).any() else D
    print(f"  {tag}: mean={D.mean():+.4f} sd={D.std():.4f} max={D.max():.4f} (log sqrt2={0.5*np.log(2):.4f}) "
          f"P(D<-1)={np.mean(D<-1):.4f} P(D<-2)={np.mean(D<-2):.5f} P(D<-3)={np.mean(D<-3):.5f}")

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    rng = np.random.default_rng(20261014)
    pairs = {
        'A: R=1, angle 0, at origin':       ((0.0, 0.0), (1.0, 0.0)),
        'B: R=317.3, angle 1.1, off-origin': ((123.4, -56.7), (123.4 + 317.3*np.cos(1.1), -56.7 + 317.3*np.sin(1.1))),
        'C: R=0.0037, angle pi/4':           ((-7.25, 3.5), (-7.25 + 0.0037*np.cos(np.pi/4), 3.5 + 0.0037*np.sin(np.pi/4))),
        'D: R=sqrt2 (=1.4142), angle 0':     ((0.0, 0.0), (np.sqrt(2), 0.0)),
    }
    print("PAPER CONSTRUCTION")
    S = {}
    for k, (p, q) in pairs.items():
        S[k] = sample_delta(p, q, N, rng, 'paper'); report(k, S[k])
    A2 = sample_delta(*pairs['A: R=1, angle 0, at origin'], N, rng, 'paper')
    ks = lambda x, y: ks_2samp(x, y)
    keys = list(pairs)
    print("  KS A vs A' (independent rerun, calibration):", ks(S[keys[0]], A2))
    for k in keys[1:]:
        print(f"  KS A vs {k[:1]}:", ks(S[keys[0]], S[k]))
    allD = np.concatenate(list(S.values()))
    print("TAILS (pooled, n=%d): empirical P(Delta<-u) vs paper bound 2*sqrt2*e^-u" % allD.size)
    for u in [0, 0.5, 1, 2, 3, 4, 5, 6]:
        print(f"  u={u}: emp={np.mean(allD < -u):.6f}  bound={2*np.sqrt(2)*np.exp(-u):.6f}  emp*e^u={np.mean(allD < -u)*np.exp(u):.4f}")
    print("CONTROLS (law SHOULD depend on pair)")
    print("  fixed grid, pair B (straddles the grid line u=0 forever):")
    sample_delta(*pairs[keys[1]], 1000, rng, "fixed")
    for mode, (k1, k2) in [('fixed', (keys[0], keys[2])), ('noxi', (keys[0], keys[3])), ('norot', (keys[0], keys[2]))]:
        x = sample_delta(*pairs[k1], N, rng, mode); y = sample_delta(*pairs[k2], N, rng, mode)
        report(f"{mode} {k1[:1]}", x); report(f"{mode} {k2[:1]}", y)
        print(f"  KS {mode}: {k1[:1]} vs {k2[:1]}:", ks(x, y))
    # extra norot control on direction only: same R, angles 0 and pi/4
    x = sample_delta((0, 0), (1, 0), N, rng, 'norot'); y = sample_delta((0, 0), (np.cos(np.pi/4), np.sin(np.pi/4)), N, rng, 'norot')
    print("  KS norot: R=1 angle 0 vs R=1 angle pi/4:", ks(x, y), " means", x.mean(), y.mean())
    # sameshift control: identical displacement (R=1, angle 0), two different base points
    x = sample_delta((0, 0), (1, 0), N, rng, 'sameshift'); y = sample_delta((0.5, -0.5), (1.5, -0.5), N, rng, 'sameshift')
    print("  KS sameshift: same displacement, base (0,0) vs (0.5,-0.5):", ks(x, y), " means", x.mean(), y.mean())
    x2 = sample_delta((0.5, -0.5), (1.5, -0.5), N, rng, 'paper')
    print("  KS paper    : same pair (0.5,-0.5)->(1.5,-0.5) vs pair A:", ks(S[keys[0]], x2))
```
Output:
```
PAPER CONSTRUCTION
  A: R=1, angle 0, at origin: mean=-1.4621 sd=1.1026 max=0.2649 (log sqrt2=0.3466) P(D<-1)=0.5828 P(D<-2)=0.23809 P(D<-3)=0.09095
  B: R=317.3, angle 1.1, off-origin: mean=-1.4558 sd=1.0947 max=0.2793 (log sqrt2=0.3466) P(D<-1)=0.5818 P(D<-2)=0.23637 P(D<-3)=0.08942
  C: R=0.0037, angle pi/4: mean=-1.4600 sd=1.0903 max=0.2599 (log sqrt2=0.3466) P(D<-1)=0.5858 P(D<-2)=0.23585 P(D<-3)=0.08981
  D: R=sqrt2 (=1.4142), angle 0: mean=-1.4558 sd=1.0861 max=0.2909 (log sqrt2=0.3466) P(D<-1)=0.5846 P(D<-2)=0.23564 P(D<-3)=0.08850
  KS A vs A' (independent rerun, calibration): KstestResult(statistic=np.float64(0.003910000000000025), pvalue=np.float64(0.42808914538350606), statistic_location=np.float64(-1.425173333737311), statistic_sign=np.int8(-1))
  KS A vs B: KstestResult(statistic=np.float64(0.0032200000000000006), pvalue=np.float64(0.6764598355032652), statistic_location=np.float64(-0.7351255806307476), statistic_sign=np.int8(1))
  KS A vs C: KstestResult(statistic=np.float64(0.003990000000000049), pvalue=np.float64(0.4025582044813488), statistic_location=np.float64(-0.963393414104349), statistic_sign=np.int8(-1))
  KS A vs D: KstestResult(statistic=np.float64(0.0037499999999999895), pvalue=np.float64(0.48176335454522834), statistic_location=np.float64(-2.6994349977492136), statistic_sign=np.int8(1))
TAILS (pooled, n=400000): empirical P(Delta<-u) vs paper bound 2*sqrt2*e^-u
  u=0: emp=0.994890  bound=2.828427  emp*e^u=0.9949
  u=0.5: emp=0.852187  bound=1.715528  emp*e^u=1.4050
  u=1: emp=0.583753  bound=1.040520  emp*e^u=1.5868
  u=2: emp=0.236487  bound=0.382786  emp*e^u=1.7474
  u=3: emp=0.089670  bound=0.140819  emp*e^u=1.8011
  u=4: emp=0.033447  bound=0.051804  emp*e^u=1.8262
  u=5: emp=0.012518  bound=0.019058  emp*e^u=1.8578
  u=6: emp=0.004548  bound=0.007011  emp*e^u=1.8346
CONTROLS (law SHOULD depend on pair)
  fixed grid, pair B (straddles the grid line u=0 forever):
    [fixed] 1.000 of samples NEVER share a cell up to side 2^65 (Delta=-inf)
  fixed A: mean=-0.6931 sd=0.0000 max=-0.6931 (log sqrt2=0.3466) P(D<-1)=0.0000 P(D<-2)=0.00000 P(D<-3)=0.00000
  fixed C: mean=-0.0542 sd=0.0000 max=-0.0542 (log sqrt2=0.3466) P(D<-1)=0.0000 P(D<-2)=0.00000 P(D<-3)=0.00000
  KS fixed: A vs C: KstestResult(statistic=np.float64(1.0), pvalue=np.float64(0.0), statistic_location=np.float64(-0.6931471805599453), statistic_sign=np.int8(1))
  noxi A: mean=-1.4707 sd=1.0753 max=0.0000 (log sqrt2=0.3466) P(D<-1)=0.5573 P(D<-2)=0.29910 P(D<-3)=0.07699
  noxi D: mean=-1.4444 sd=1.0958 max=-0.3466 (log sqrt2=0.3466) P(D<-1)=0.7409 P(D<-2)=0.21510 P(D<-3)=0.10986
  KS noxi: A vs D: KstestResult(statistic=np.float64(0.21536999999999995), pvalue=np.float64(0.0), statistic_location=np.float64(-0.6931471805599453), statistic_sign=np.int8(1))
  norot A: mean=-1.3464 sd=1.0178 max=-0.0015 (log sqrt2=0.3466) P(D<-1)=0.5317 P(D<-2)=0.19541 P(D<-3)=0.07188
  norot C: mean=-1.4992 sd=1.1355 max=0.3338 (log sqrt2=0.3466) P(D<-1)=0.6038 P(D<-2)=0.25478 P(D<-3)=0.09724
  KS norot: A vs C: KstestResult(statistic=np.float64(0.08537000000000006), pvalue=np.float64(1.768586e-317), statistic_location=np.float64(-1.1997144756543374), statistic_sign=np.int8(-1))
  KS norot: R=1 angle 0 vs R=1 angle pi/4: KstestResult(statistic=np.float64(0.08262000000000003), pvalue=np.float64(2.3704736370142198e-297), statistic_location=np.float64(-1.3195959204583658), statistic_sign=np.int8(-1))  means -1.3488526666161738 -1.4994630166251286
  KS sameshift: same displacement, base (0,0) vs (0.5,-0.5): KstestResult(statistic=np.float64(0.04647000000000001), pvalue=np.float64(2.8756180286668244e-94), statistic_location=np.float64(-1.4137357105218988), statistic_sign=np.int8(-1))  means -1.4102224173096753 -1.4656175434244145
  KS paper    : same pair (0.5,-0.5)->(1.5,-0.5) vs pair A: KstestResult(statistic=np.float64(0.002809999999999979), pvalue=np.float64(0.8236027172482262), statistic_location=np.float64(-1.9112880042352043), statistic_sign=np.int8(1))

real	0m7.968s
user	0m8.828s
sys	0m0.809s
```

### Check B — κ and the tails by quadrature (kappa_quad.py; independent of the MC)

This check uses the single-scale CDF Pr(Δ ≥ u) = E_{U,φ}[(1−cos φ/ρ)₊(1−sin φ/ρ)₊] with ρ = e^{−u}2^{−U}.
It gives κ = −1.45718. The MC values are −1.4621 / −1.4558 / −1.4600 / −1.4558, pooled −1.4584 ± 0.0017: agreement within 0.7 SE.
The tail probabilities agree too: Pr(Δ<−1) is 0.5825 by quadrature and 0.5838 by MC.
```python
# Independent (non-Monte-Carlo) computation of kappa = E Delta from the single-scale sharing formula
# Pr(Delta >= u) = E_{U,phi}[(1-|cos phi|/rho)_+ (1-|sin phi|/rho)_+],  rho = e^{-u} 2^{-U}, U~U[0,1), phi~U[0,pi/2)
# (paper p.10: "{Delta >= u} is sharing at the largest side l <= R e^{-u}"; law of l/R log-uniform on (e^{-u}/2, e^{-u}]).
import numpy as np
from scipy import integrate
def G(u, nU=400, nphi=400):
    U = (np.arange(nU) + 0.5) / nU
    phi = (np.arange(nphi) + 0.5) / nphi * (np.pi / 2)
    rho = np.exp(-u) * 2.0 ** (-U)[:, None]
    g = np.clip(1 - np.cos(phi)[None, :] / rho, 0, None) * np.clip(1 - np.sin(phi)[None, :] / rho, 0, None)
    return g.mean()
up = integrate.quad(G, 0, 0.5*np.log(2), limit=200)[0]
lo = integrate.quad(lambda u: 1 - G(-u), 0, 60, limit=400)[0]
print("int_0^inf P(Delta>=u) du =", up, "  int_0^inf P(Delta<-u) du =", lo, "  kappa =", up - lo)
for u in [1, 2, 4, 6, 10]:
    print(f"u={u}: P(Delta<-u)={1-G(-u):.6f}  e^u*P = {(1-G(-u))*np.exp(u):.5f}   (asymptote (4/pi)/ln2 = {4/np.pi/np.log(2):.5f})")
print("P(Delta >= 0) =", G(0.0), "  P(Delta >= 0.3) =", G(0.3), " P(Delta >= log sqrt2 - 1e-9) =", G(0.5*np.log(2) - 1e-9))
```
Output:
```
int_0^inf P(Delta>=u) du = 0.00033111270311328667   int_0^inf P(Delta<-u) du = 1.4575153413632442   kappa = -1.4571842286601309
u=1: P(Delta<-u)=0.582533  e^u*P = 1.58349   (asymptote (4/pi)/ln2 = 1.83690)
u=2: P(Delta<-u)=0.235981  e^u*P = 1.74367   (asymptote (4/pi)/ln2 = 1.83690)
u=4: P(Delta<-u)=0.033413  e^u*P = 1.82428   (asymptote (4/pi)/ln2 = 1.83690)
u=6: P(Delta<-u)=0.004549  e^u*P = 1.83519   (asymptote (4/pi)/ln2 = 1.83690)
u=10: P(Delta<-u)=0.000083  e^u*P = 1.83687   (asymptote (4/pi)/ln2 = 1.83690)
P(Delta >= 0) = 0.0050123562956067135   P(Delta >= 0.3) = 1.4413730359144479e-06  P(Delta >= log sqrt2 - 1e-9) = 0.0

real	0m2.012s
user	0m2.934s
sys	0m0.575s
```

### Check C — Lemma 3.2 / (3.5) exactly (exact_35.py, Fractions)

Cases: Figure 1, and 3,000 random hierarchies (n = 2..11, half of them with ties / multi-way merges).
Controls:
- C1 (multiset → set) fails on the Figure 1 pairs (6,7), (6,8), (7,8), where d = 2 but the right side = 1, and on 1,042 of 3,000
  random hierarchies.
- C2 (sign of S flipped) fails on 2,104 of 3,000. It is invisible whenever S(x) = S(y) = 0.
```python
# Exact check of Lemma 3.2, identity (3.5): d(x,y) = M + L(x,y) - S(x) - S(y), on explicit hierarchies (Fractions / ints).
# Hierarchy given by a sharing-depth function d on unordered pairs; Pi(r) = classes of {d >= r}.
# Giant = the cell of size > n/2; C(r) = Pi(r) with the giant replaced by its complement, AS A MULTISET (paper p.10).
# Controls: (C1) multiset -> set (drop a duplicated complement); (C2) sign of S flipped.
from fractions import Fraction as F
import itertools, random, math

def classes(P, d, r):
    # classes of the relation {d >= r} (assumed an equivalence relation; verified)
    cls = []
    for x in P:
        for c in cls:
            if d[frozenset((x, c[0]))] >= r:
                c.append(x); break
        else:
            cls.append([x])
    # verify it IS an equivalence relation (transitivity)
    for c in cls:
        for a, b in itertools.combinations(c, 2):
            assert d[frozenset((a, b))] >= r, "not transitive"
    for c1, c2 in itertools.combinations(cls, 2):
        for a in c1:
            for b in c2:
                assert d[frozenset((a, b))] < r
    return [frozenset(c) for c in cls]

def hier_quantities(P, d, multiset=True):
    n = len(P)
    vals = sorted(set(d.values()))
    # intervals (v_{i}, v_{i+1}] on which Pi(r) = classes(d >= v_{i+1}); (-inf, v_1] -> {P}; (v_k, inf) -> singletons
    M = vals[0]           # giant (=P) exists on (-inf, v_1]
    S = {x: F(0) for x in P}
    L = {frozenset(p): F(0) for p in itertools.combinations(P, 2)}
    giant_ray_ok = True; seen_no_giant = False
    for lo, hi in zip(vals[:-1], vals[1:]):
        length = F(hi) - F(lo)
        Pi = classes(P, d, hi)
        G = [c for c in Pi if 2 * len(c) > n]
        assert len(G) <= 1
        if G:
            if seen_no_giant: giant_ray_ok = False
            G = G[0]; M = hi
            comp = frozenset(P) - G
            Cs = [c for c in Pi if c != G]
            if multiset or comp not in Cs:
                Cs = Cs + [comp]
            for x in P:
                if x not in G: S[x] += length
        else:
            seen_no_giant = True
            Cs = Pi
        for pr in L:
            a, b = tuple(pr)
            L[pr] += length * sum(1 for c in Cs if a in c and b in c)
    return M, S, L, giant_ray_ok

def check(P, d, multiset=True, sign=+1):
    M, S, L, ray = hier_quantities(P, d, multiset)
    bad = []
    for pr in L:
        a, b = tuple(pr)
        rhs = M + L[pr] - sign * (S[a] + S[b])
        if F(d[pr]) != rhs: bad.append((tuple(sorted(pr)), d[pr], rhs))
    return bad, ray

def ultrametric_from_dendrogram(P, rng, tie=False):
    # random agglomeration: start singletons; merge two clusters at strictly decreasing (or tied) depth
    clusters = [[x] for x in P]; d = {}
    h = F(rng.randint(30, 60), rng.randint(1, 4))
    while len(clusters) > 1:
        i, j = rng.sample(range(len(clusters)), 2)
        for a in clusters[i]:
            for b in clusters[j]:
                d[frozenset((a, b))] = h
        clusters[i] = clusters[i] + clusters[j]; clusters.pop(j)
        if not (tie and rng.random() < 0.4):
            h -= F(rng.randint(1, 9), rng.randint(1, 5))
    return d

if __name__ == '__main__':
    # (a) Figure 1: n=8, Pi = {1..5},{6,7,8} on (1,2]
    P = list(range(1, 9)); d = {}
    for a, b in itertools.combinations(P, 2):
        if a <= 5 and b <= 5: d[frozenset((a, b))] = F(3)
        elif a >= 6 and b >= 6: d[frozenset((a, b))] = F(2)
        else: d[frozenset((a, b))] = F(1)
    M, S, L, ray = hier_quantities(P, d)
    print("Figure 1: M =", M, " S(6) =", S[6], " S(1) =", S[1], " L(6,7) =", L[frozenset((6, 7))], " L(1,2) =", L[frozenset((1, 2))])
    print("  paper identity failures:", check(P, d)[0])
    print("  CONTROL C1 (set, not multiset) failures:", check(P, d, multiset=False)[0])
    print("  CONTROL C2 (sign of S flipped) failures (first 3):", check(P, d, sign=-1)[0][:3])
    # (b) random ultrametrics, with and without ties
    rng = random.Random(604)
    tot = fails = c1 = c2 = rayfail = 0; dup_events = 0
    for trial in range(3000):
        n = rng.randint(2, 11)
        P = list(range(n))
        d = ultrametric_from_dendrogram(P, rng, tie=(trial % 2 == 1))
        bad, ray = check(P, d); tot += 1; fails += bool(bad); rayfail += (not ray)
        c1 += bool(check(P, d, multiset=False)[0]); c2 += bool(check(P, d, sign=-1)[0])
    print(f"random ultrametrics: {tot} hierarchies, identity failures = {fails}, non-initial-ray giant sets = {rayfail}")
    print(f"  CONTROL C1 (set) caught {c1}/{tot}; CONTROL C2 (sign) caught {c2}/{tot}")
```
Output:
```
Figure 1: M = 3  S(6) = 2  S(1) = 0  L(6,7) = 3  L(1,2) = 0
  paper identity failures: []
  CONTROL C1 (set, not multiset) failures: [((6, 7), Fraction(2, 1), Fraction(1, 1)), ((6, 8), Fraction(2, 1), Fraction(1, 1)), ((7, 8), Fraction(2, 1), Fraction(1, 1))]
  CONTROL C2 (sign of S flipped) failures (first 3): [((1, 6), Fraction(1, 1), Fraction(5, 1)), ((1, 7), Fraction(1, 1), Fraction(5, 1)), ((1, 8), Fraction(1, 1), Fraction(5, 1))]
random ultrametrics: 3000 hierarchies, identity failures = 0, non-initial-ray giant sets = 0
  CONTROL C1 (set) caught 1042/3000; CONTROL C2 (sign) caught 2104/3000

real	0m7.017s
user	0m6.991s
sys	0m0.008s
```

### Check D — end-to-end (3.2)+(3.5)+Lemma 3.1 ⇒ (3.6) in K = ℚ(i) (endtoend_36.py, 15,000 grids per coordinate)

Setup:
- 7 integer points. Z₁ = u+ib, Z₂ = u−ib ∈ ℤ[i].
- All finite places with a nonunit difference: 1+i (p = 2, ramified); 3 (inert); the split pairs over 5, 13, 17, 29. These are treated
  exactly (p-adic hierarchies, (3.5) asserted).
- The complex place is handled by the paper's grids, with (3.5) asserted pathwise in exact integers on all 30,000 realized hierarchies
  and grid nesting asserted at every scale.

Prediction of (3.6): D(x,y) := L*(x,y) − S*(x) − S*(y) is the same for all 21 pairs.
- Paper normalization: spread 0.050. It was 0.129 at 3,000 grids; the ratio 2.55 ≈ √5, i.e. Monte Carlo noise. The mean sits at
  b* = 2κ − ⟨M₁+M₂⟩ = −1.421.
- Controls fail: dropping the finite places gives spread 3.37; Milne-normalized |·|_𝔭 with the paper's σ_𝔭 (double conversion) gives
  2.92; complex weight 1/[K:ℚ] (factor 2 forgotten) gives 1.69.
```python
# End-to-end check of (3.2)+(3.5)+Lemma 3.1 => (3.6) on an explicit configuration in K = Q(i), [K:Q]=2.
# Points with integer coordinates (u,b); Z1 = u+ib, Z2 = u-ib in Z[i].  Places of K: one complex place (sigma=2/[K:Q]=1,
# ordinary modulus) and the Gaussian primes P over p (|.|_P extends |p|_p=1/p, sigma_P=[K_P:Q_p]/[K:Q]=ef/2).
# (3.6) predicts D(x,y) := L*(x,y) - S*(x) - S*(y) is the SAME number b* = 2kappa - <M1+M2> for every distinct pair.
# Also verifies pathwise (3.5) on every realized complex-place grid hierarchy (exact integers) and that grid cells nest.
# Controls (should make D(x,y) pair-DEPENDENT): drop finite places; Milne-normalized |.|_P (log||z|| = -v log NP) with the
# paper's weights (double conversion); complex weight 1/[K:Q] (forgetting the factor 2); grid without random orientation/scale
# is NOT used here (that is mc_delta.py's job).
import numpy as np, itertools, math, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_35 import hier_quantities, check
from fractions import Fraction as F

PTS = [(0, 0), (1, 0), (0, 1), (2, 1), (3, 3), (5, 2), (1, 4)]
n = len(PTS)
PAIRS = list(itertools.combinations(range(n), 2))
Z = {1: [complex(u, b) for u, b in PTS], 2: [complex(u, -b) for u, b in PTS]}
KAPPA = -1.4571842286601309   # from kappa_quad.py

def gdiv(z, pi):   # exact division in Z[i] if possible, else None
    a, b = int(z.real), int(z.imag); c, d = int(pi.real), int(pi.imag)
    N = c*c + d*d
    re, im = a*c + b*d, b*c - a*d          # z * conj(pi)
    if re % N or im % N: return None
    return complex(re // N, im // N)
def val(z, pi):
    v = 0
    while True:
        w = gdiv(z, pi)
        if w is None: return v
        z = w; v += 1
def gaussian_primes_over(p):
    if p == 2: return [(complex(1, 1), 2, 1)]          # (pi, e, f)
    if p % 4 == 3: return [(complex(p, 0), 1, 2)]
    for a in range(1, int(p**0.5) + 1):
        b2 = p - a*a; b = int(round(b2**0.5))
        if b*b == b2: return [(complex(a, b), 1, 1), (complex(a, -b), 1, 1)]
def rational_primes(m):
    ps, q = set(), 2
    while m > 1:
        while m % q == 0: ps.add(q); m //= q
        q += 1
    return ps

# ---- finite places (exact) ----
diffs = {j: {pr: Z[j][pr[1]] - Z[j][pr[0]] for pr in PAIRS} for j in (1, 2)}
primes = set()
for j in (1, 2):
    for z in diffs[j].values(): primes |= rational_primes(int(round(abs(z)**2)))
places = [pl for p in sorted(primes) for pl in gaussian_primes_over(p)]
print("finite places with a nonunit difference:", [(p_, int(round(abs(pi)**2)) , e, f) for p_ in sorted(primes) for (pi, e, f) in gaussian_primes_over(p_)])

def finite_contrib(weight_mode):
    # returns per-j dicts: Mfin, Sfin[x], Lfin[pair], ifin[pair]  (already multiplied by sigma_v and scaled to i-units)
    out = {}
    for j in (1, 2):
        Mf = 0.0; Sf = np.zeros(n); Lf = {pr: 0.0 for pr in PAIRS}; If = {pr: 0.0 for pr in PAIRS}
        for (pi, e, f) in places:
            p = int(round(abs(pi)**2)) if f == 1 and e == 1 else (2 if e == 2 else int(round(abs(pi))))
            dv = {frozenset(pr): F(val(diffs[j][pr], pi)) for pr in PAIRS}
            M, S, L, ray = hier_quantities(list(range(n)), dv); assert ray
            assert not check(list(range(n)), dv)[0]
            if weight_mode == 'paper':      # sigma = ef/2, |z|_P = p^{-v/e}  -> sigma * (v log p / e) = v f log p / 2
                scale = (e * f / 2) * (math.log(p) / e)
            elif weight_mode == 'milne_double':   # Milne-normalized: -log||z|| = v f log p, times sigma=ef/2 (double conversion)
                scale = (e * f / 2) * (f * math.log(p))
            elif weight_mode == 'none':
                scale = 0.0
            Mf += scale * float(M)
            for x in range(n): Sf[x] += scale * float(S[x])
            for pr in PAIRS:
                Lf[pr] += scale * float(L[frozenset(pr)]); If[pr] += scale * float(dv[frozenset(pr)])
        out[j] = (Mf, Sf, Lf, If)
    return out

# ---- complex place (Monte Carlo over the paper's random nested grids, common random numbers across pairs) ----
LOG2 = math.log(2)
def grid_first_share(points, rng):
    th = rng.uniform(0, 2*math.pi); xi = rng.uniform(0, LOG2); l0 = math.exp(xi)
    c, s = math.cos(th), math.sin(th)
    X = np.array([[z.real*c + z.imag*s, -z.real*s + z.imag*c] for z in points])
    s0 = rng.uniform(0, 1, 2) * l0
    first = {}
    sm = s0.copy(); prev_cells = None
    for m in range(-6, 40):
        l = l0 * 2.0**m
        if m <= 0: sh = np.mod(s0, l)
        else:
            sm = sm + rng.integers(0, 2, 2) * (l0 * 2.0**(m-1)); sh = sm
        cells = [tuple(np.floor((X[k] - sh) / l).astype(np.int64)) for k in range(n)]
        if prev_cells is not None:     # nesting: same finer cell => same coarser cell
            for a_, b_ in PAIRS:
                if prev_cells[a_] == prev_cells[b_]: assert cells[a_] == cells[b_], "grids not nested"
        for pr in PAIRS:
            if pr not in first and cells[pr[0]] == cells[pr[1]]: first[pr] = m
        prev_cells = cells
        if len(first) == len(PAIRS): break
    assert len(first) == len(PAIRS)
    return xi, first

def complex_contrib(NG, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for j in (1, 2):
        Msum = 0.0; Ssum = np.zeros(n); Lsum = {pr: 0.0 for pr in PAIRS}; Dsum = {pr: 0.0 for pr in PAIRS}
        for g in range(NG):
            xi, first = grid_first_share(Z[j], rng)
            dint = {frozenset(pr): F(-first[pr]) for pr in PAIRS}      # d = -xi + log2 * (-a): affine image
            M, S, L, ray = hier_quantities(list(range(n)), dint); assert ray
            for pr in PAIRS:     # pathwise (3.5), exact in integer units
                a_, b_ = pr
                assert dint[frozenset(pr)] == M + L[frozenset(pr)] - S[a_] - S[b_]
            Msum += -xi + LOG2 * float(M)
            for x in range(n): Ssum[x] += LOG2 * float(S[x])
            for pr in PAIRS:
                Lsum[pr] += LOG2 * float(L[frozenset(pr)]); Dsum[pr] += -xi - LOG2 * first[pr]
        out[j] = (Msum/NG, Ssum/NG, {k: v/NG for k, v in Lsum.items()}, {k: v/NG for k, v in Dsum.items()})
    return out

if __name__ == '__main__':
    NG = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    cx = complex_contrib(NG, 1014)
    # sanity: E d_j(x,y) at the complex place = -log|z| + kappa
    errs = [cx[j][3][pr] - (-math.log(abs(diffs[j][pr])) + KAPPA) for j in (1, 2) for pr in PAIRS]
    print(f"complex place, {NG} grids/coordinate: E d - (-log|z| + kappa): mean {np.mean(errs):+.4f}, max|.| {np.max(np.abs(errs)):.4f}")
    for mode, cw in [('paper', 1.0), ('none', 1.0), ('milne_double', 1.0), ('paper', 0.5)]:
        fin = finite_contrib(mode)
        D = {}; Mtot = 0.0
        for pr in PAIRS:
            x, y = pr; val_ = 0.0
            for j in (1, 2):
                Mf, Sf, Lf, If = fin[j]; Mc, Sc, Lc, Dc = cx[j]
                val_ += (Lf[pr] + cw * Lc[pr]) - (Sf[x] + cw * Sc[x]) - (Sf[y] + cw * Sc[y])
            D[pr] = val_
        Mtot = sum(fin[j][0] + cw * cx[j][0] for j in (1, 2))
        Dv = np.array(list(D.values()))
        label = f"{mode}, complex sigma={cw}"
        print(f"[{label:32s}] D(x,y)=L*-S*(x)-S*(y) over 21 pairs: min {Dv.min():+.4f} max {Dv.max():+.4f} spread {Dv.max()-Dv.min():.4f};"
              f"  2*kappa*{cw} - <M1+M2> = {2*KAPPA*cw - Mtot:+.4f}")
```
Output:
```
finite places with a nonunit difference: [(2, 2, 2, 1), (3, 9, 1, 2), (5, 5, 1, 1), (5, 5, 1, 1), (13, 13, 1, 1), (13, 13, 1, 1), (17, 17, 1, 1), (17, 17, 1, 1), (29, 29, 1, 1), (29, 29, 1, 1)]
complex place, 15000 grids/coordinate: E d - (-log|z| + kappa): mean +0.0044, max|.| 0.0249
[paper, complex sigma=1.0        ] D(x,y)=L*-S*(x)-S*(y) over 21 pairs: min -1.4355 max -1.3850 spread 0.0505;  2*kappa*1.0 - <M1+M2> = -1.4210
[none, complex sigma=1.0         ] D(x,y)=L*-S*(x)-S*(y) over 21 pairs: min -2.4816 max +0.8922 spread 3.3737;  2*kappa*1.0 - <M1+M2> = +0.8816
[milne_double, complex sigma=1.0 ] D(x,y)=L*-S*(x)-S*(y) over 21 pairs: min -2.1287 max +0.7868 spread 2.9154;  2*kappa*1.0 - <M1+M2> = -2.1141
[paper, complex sigma=0.5        ] D(x,y)=L*-S*(x)-S*(y) over 21 pairs: min -1.8690 max -0.1761 spread 1.6930;  2*kappa*0.5 - <M1+M2> = -1.8618

real	0m32.008s
user	0m32.665s
sys	0m0.031s
```

### Check E — failing control for the nesting / ultrametric asserts used in Check D (nest_control.py)

The paper's nested-shift rule gives 0 violations in 2,000 grids. Independent per-scale shifts violate nesting in 1,866 of 2,000 and
break the ultrametric property in 1,598 of 2,000. So the asserts in Check D can fire.
```python
# Control for the nesting assertion used in endtoend_36.py: replace the paper's nested-shift rule
# (s_{m+1} = s_m + B*l_m) by INDEPENDENT uniform shifts at each scale. The nesting check must now fire,
# and the "first sharing scale" must stop being an ultrametric (classes() transitivity assert).
import numpy as np, math, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from exact_35 import hier_quantities
PTS = [complex(u, b) for u, b in [(0, 0), (1, 0), (0, 1), (2, 1), (3, 3), (5, 2), (1, 4)]]
n = len(PTS); PAIRS = list(itertools.combinations(range(n), 2))
def run(nested, rng):
    th = rng.uniform(0, 2*math.pi); xi = rng.uniform(0, math.log(2)); l0 = math.exp(xi)
    c, s = math.cos(th), math.sin(th)
    X = np.array([[z.real*c + z.imag*s, -z.real*s + z.imag*c] for z in PTS])
    s0 = rng.uniform(0, 1, 2) * l0; sm = s0.copy(); prev = None; first = {}; nest_ok = True
    for m in range(-6, 40):
        l = l0 * 2.0**m
        if not nested: sh = rng.uniform(0, 1, 2) * l
        elif m <= 0: sh = np.mod(s0, l)
        else: sm = sm + rng.integers(0, 2, 2) * (l0 * 2.0**(m-1)); sh = sm
        cells = [tuple(np.floor((X[k] - sh) / l).astype(np.int64)) for k in range(n)]
        if prev is not None:
            for a, b in PAIRS:
                if prev[a] == prev[b] and cells[a] != cells[b]: nest_ok = False
        for pr in PAIRS:
            if pr not in first and cells[pr[0]] == cells[pr[1]]: first[pr] = m
        prev = cells
        if len(first) == len(PAIRS) and m > 12: break
    ultra_ok = True
    try:
        hier_quantities(list(range(n)), {frozenset(pr): F(-first[pr]) for pr in PAIRS})
    except AssertionError:
        ultra_ok = False
    return nest_ok, ultra_ok
rng = np.random.default_rng(7)
for nested in (True, False):
    res = [run(nested, rng) for _ in range(2000)]
    print(f"nested={nested}: nesting violated in {sum(not a for a,_ in res)}/2000 grids; "
          f"first-share depth not an ultrametric in {sum(not b for _,b in res)}/2000")
```
Output:
```
nested=True: nesting violated in 0/2000 grids; first-share depth not an ultrametric in 0/2000
nested=False: nesting violated in 1866/2000 grids; first-share depth not an ultrametric in 1598/2000

real	0m4.518s
user	0m5.466s
sys	0m0.074s
```

---------------------------------------------------------------------------------------------------------------------------

## SUMMARY

§3 HOLDS AS READ.
- Z₁, Z₂ and (3.1) are correct identities; injectivity uses only the reality of u and b.
- (3.2) is exactly Milne v3.08 Theorem 7.15 divided by [K:ℚ], converted at finite places by Lemma 8.6 (exponent [K_v:ℚ_p]) and at
  complex places by the factor 2 in |σa|². Σ_{v∣∞}σ_v = 1 because i ∈ K forces r₁ = 0. The cited theorems MATCH.
- (3.3) follows from multiplicativity and the fiber definition.
- The nested grids are nested and uniform at every scale.
- Lemma 3.1 is correct, and its pair-independence argument is sound: nesting turns {Δ ≥ u} into a single-scale event whose
  probability depends only on (log-phase, angle), both uniform. The tails are two-sided with C₀ = 2√2, b₀ = 1. κ ≈ −1.4572.
- Lemma 3.2 / (3.5) is an exact algebraic identity. It needs the multiset doubling of Figure 1, and the paper keeps it.
- (3.6) and (3.7) follow by taking ⟨·⟩.
Monte Carlo, quadrature and exact checks all confirm this, each with a control that fails.

Objections, all COSMETIC:
- The independence of the two axis shifts is unstated, though the product sharing formula needs it.
- The coupling of grids across j and across places is unspecified; it is unused here.
- The choice of σ vs σ̄ at a complex place is unspecified; it is reflection-invariant.
- "l < R/√2" should be "≤", and (3.4) for u < log√2 is implicit.
- The [11] theorem numbers are inconsistent across pp. 3, 9 and the bibliography.

NOTE for brief (i): the additive identity is coordinate-wise. ⟨d_j⟩ = κ holds for each j by the product formula on Z_j(x)−Z_j(y) alone,
so §3's identities hold for any finite set of distinct elements of a number field. The squared-distance factorization enters §3 only
through (3.3), and nothing in §3 excludes constant (F_q-type) sets, for which W = 0. The characteristic-zero obstruction must therefore
be used downstream (§7's archimedean normalization), not in §3.
