# Seat P — the paper as written (arXiv 2604.23784v3, Bae), 2026-10-31
(Saved by the main seat from the seat's final message; the harness blocked the subagent from writing this file. Printed numbering from v3.pdf, eqs (1)–(69).)

**VERDICT: HOLDS AS READ.** Every lemma checks and the constant 1/2 follows from the paper's own parameters. Required changes are non-mathematical: (i) §9 overclaims; (ii) the statement of Lemma 4.1 leaves out "for all sufficiently large M".

Files here (all numerics small-case evidence only): structure_check.py/.out (Kummer, fold, ranges I–IV; n up to ~10^135) · tail_check.py/.out (Lemma 4.1; exhaustive over t ≤ 2·10^7 + Monte Carlo) · params_check.py/.out (constraints, constant, finite-M size of the o(1) terms) · e2e_small.py/.out (f(n) at constructed n, illustration only) · dl/ (APSSV v2 source, abstracts, the #684 page and proof-claim entry).

## 1. Lemma by lemma
- **Lemma 2.1 (Kummer), (6)–(7): HOLDS.** Legendre summand = 1{[n]_q<[k]_q}; p^a > n terms vanish; (7) needs K ≤ n (stated). Kummer = Legendre everywhere tested; log u(n,k) = direct factorisation of C(n,k) for 35 pairs.
- **PNT inputs (8)–(10): HOLD.** (10) is Mertens under A → ∞, log A = o(log M); (8) used only at heights ≥ M/2.
- **Lemma 3.1 (code entropy), (17)–(20): HOLDS.** Ceiling error O(M/log M); partial-summation remainder negligible; denominator swap O(MA log²A/log²M); integral recomputed. Only the upper bound is used (at (42)). Convergence very slow: exact prime sums give log C_M/M = 0.907, 0.918, 0.926, 0.933 at M = 10^4…10^7 for c = 0.8 (≈18 for c = 8); correction ~1/log log M.
- **Lemma 3.2 (equal-cell difference), (21): HOLDS** (h < p/2 since 2h < M < p).
- **Lemma 4.1 (high-power tail), (22)–(38): HOLDS.** Step 1 nesting and (26) Z(t) = Σ ℓ_p(t) log p: exhaustive, 0 violations. Step 2: g_p | h+1+s, ≤ 2K/g_p values, L/g_p a unit mod p — enumerated, no prime exceeds 2K/g_p classes. Step 3: prefix weight < βM + log K; for p > M, a_p = 2, b_p = 0 (needs K < M²); (33) exact (4.499810 = 4.499810 at M = 8, K = 30); log Q ≤ 2W + O(√K) < σM ⇒ Q < J licenses J/Q + 1 ≤ 2J/Q; g_p cancel exactly; every bad t caught by some profile. Exhaustive over all 426 profiles with W ≤ 7: 0 violations of (30) or (36), max true/bound ratio 0.267. Step 4: weighting valid, geometric series exact, split at √K gives O_λ(K^{(1+λ)/2}) = o(M). Monte Carlo at M = 30, K = 150 far below bound (vacuous at this size; rules out sign errors only). **Presentational:** (24) says "For every fixed parameter tuple satisfying (11)" but the proof needs "for all sufficiently large M". Cosmetic: "K = M log^{1+o(1)} M" true only because the o(1) is negative; K = M(log M)^{1−o(1)} clearer.
- **Lemma 5.1 (anchored fibres), (39)–(40), selection (41)–(43): HOLD.** Pigeonhole gives a fibre of ≥ |F|+2 points; differences from its least point are distinct. Forbidden set is a condition on t itself (no independence). All three exponent gaps in (42) positive under (11)–(12).
- **Fold (44)–(45): HOLDS** ([n]_p = p−1−d_p, 1 ≤ d_p ≤ 2h−1, both signs of z_p).
- **Lemma 6.1, (48)–(50): HOLDS.** For q ≤ M, [n]_q = q−1−[h]_q ⇒ range (I) is a sub-sum of the carries of C(h+k,h); (e(h+k)/h)^h ⇒ (1/20+o(1))M. Sub-sum identity exact at every k ≤ K tested; ratio to log C(h+k,h) reaches 1.000 (tight).
- **Lemma 6.2, (51)–(57): HOLDS.** Carry at p ⇒ 1 ≤ mp−k < 2h ⇒ p ∈ I_m(k), 2 ≤ m ≤ A+1; active intervals have left end > M−h so (8) applies with absolute error, o(M) over ≤ A+1 values of m; overlaps only over-count; total 2h·H = (1/10+o(1))M. 0 failures; range (II) never exceeded the exact Σ_m θ(I_m(k)).
- **Ranges (III), (58) and (IV), (59): HOLD.** (III) exact identity O(√K); (IV) a ≥ 2, [k]_q = k ⇒ ≤ Z(t). The four ranges summed to log u(n,k) within 10^−9.
- **Proposition 7.1 (60)–(66), main proof (67)–(69): HOLD.** Margins (68) correct; grid δ ∈ (0,½), β ∈ [10^−3, 10^6]: 0 violations. limsup ≥ each fixed-tuple value ⇒ ≥ supremum; no uniformity in λ↑1, β→∞ needed. Diagonal condition log β_j/log M_j < 1/j keeps (66) uniform.

## 2. The constant
limsup ≥ c/(1+σ); admissible tuples have c < λβ < β and σ > 2β, so c/(1+σ) < β/(1+2β) < 1/2; supremum exactly 1/2 (λ→1, c→β, σ→2β, β→∞). τ and 3/20 constraints slack. Under (67): (1−2δ)β/(1+(2+δ)β) — δ=0.01: 0.464 (β=10), 0.48756 (β=10^8); δ=0.001: 0.475, 0.49875.
Where 1/2 comes from: the **2** = CRT overhead (a carry of weight log p costs modulus p², Q ≤ e^{2W}); **c < β** = tail saving e^{−λβM} must beat code size e^{cM}; the **1 in 1+σ** = log L ≈ M, washes out as β → ∞. A limit of the method; the paper does not claim optimality.
**Finite sizes:** (39) fails at every computable M. β = 1, δ = 0.1, excess exponent/M: +0.60 (10^4), +0.47 (10^5), +0.38 (10^6), +0.31 (10^7); β = 10: ~+11 to +14. Decays ~1/log log M (entropy) and M^{−δ/2} (tail). Fine for a limsup; no computation can confirm the constant.

## 3. The shift, numerically (small-case evidence)
Fraction of residues k mod p carrying at level p: shifted n = tL−h−1, z_p ≤ 0: max 0.12–0.23, always ≤ (2h−1)/p; shifted, z_p > 0: max 0.06–0.09, ≤ (2h−1)/p; unshifted n′ = tL−1, z_p > 0: 0.954–0.982; unshifted z_p ≤ 0: ~0.02. Levels ≤ M = exact sub-sum of carries of C(h+k,h) across 72 constructed n. End-to-end (illustration): M ≤ 60, max log u(n,k) over k ≤ K is 28–58 vs 2 log n = 300–714; f(n)/log n ≈ 4.7–5.5.

## 4. Citations and hand-waves
Only PNT with classical remainder (heights ≥ M/2), Chebyshev, CRT (distinct prime bases), Kummer. Every "standard"/"elementary" (tex lines 226, 451, 497, 702, 759) routine and re-derived. Remark 1.1's "no Timofeev, Burgess or Fourier-sieve input" confirmed. APSSV (1/2+o(1)) log n via n = M_K − 1 matches the APSSV v2 source; Li cited accurately; neither used in the proof.

## 5. Framing
Improvement = exactly log log n/log log log n. Intro/abstract accurate, more restrained than v2; Remark 1.1 "stronger" true (v3 implies v2's claim). **§9 overstates:** "Theorem 1.2 gives a direct quantitative answer on the worst-case side of that question … this answers Erdős's original question by giving explicit bounds for his threshold." Erdős's "we do not know how fast" A(n) → ∞ asks for a lower bound valid for every n; a subsequence lower bound does not address it and that bound remains ineffective (Mahler). The forum proof claim ("fully answers 'Give bounds for f(n)'") repeats this. Lean not assessed (per brief).

## 6. Fixes
1. Lemma 4.1 (24): add "for all sufficiently large M" (optionally K = M(log M)^{1−o(1)}).
2. §9: withdraw "answers Erdős's original question"; say the lower bound holds along a subsequence and the rate of f(n) → ∞ is still open.
3. Optional: drop the unused "≍ M/log M" in (55).
None affects the proof of Theorem 1.2.
