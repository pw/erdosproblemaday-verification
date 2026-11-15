# Hostile referee (Opus instance) — Erdős #338 claims of 2026-11-15
Saved by the 09Z erdos seat from the referee's reply (the seat could not write .md files itself). Its scripts and
outputs are in this directory. Brief: refute. Result: nothing fails; no MUST fix; seven SHOULD fixes (all applied).

| Item | Verdict |
|---|---|
| (1) Theorem A (popular density ≥ δ/4, bound 3⌈8/δ⌉ − 2) | HOLDS WITH FIXES (SHOULD only); now a corollary of A″ |
| (1″) Lemma 1″ + Theorem A″ (popular density ≥ δ, bound 3⌈2/δ⌉ − 2) | HOLDS WITH FIXES (SHOULD only) |
| (2) Kneser's theorem as used in Step 2 | HOLDS — source quote matches the note's form |
| (3) Theorem B (exceptions exactly 2·3^j; ≤ 4 summands except 2, 6, 18) | HOLDS |
| (4) Veljjanoski's Theorem 2 (block model, l*(C,3) ≤ 4) | HOLDS — no gap found |

## (1) Theorem A, Step 1′
- (ii) "r(n) ≤ A(x)" needs 0 ∉ A (witness A = {0,…,20} \ {10}, N = 20: r(20) = 10 > A(10) = 9); harmless for positive integers.
- Other inequalities and off-by-ones check out. Steps 2–4 use only g ≤ s − 1; nothing downstream needed the old density.
- Numerics (`test_thmA.py`): r(n) by FFT and by exact convolution (agree, n ≤ 40,000); seven sets + adversarial hill-climb,
  N ≤ 200,000, R ≤ 1000: 0 violations; hill-climb best lhs − rhs = 0 (reached, never exceeded).
- {n ≡ 0,1 mod m}: restricted order EXACTLY m − 1 (exact DP, m = 2..8: finitely many exceptions to "≤ m − 1", every
  n ≡ −1 mod m is an exception to "≤ m − 2"); density 2/m; residue hypothesis holds for every g.
- T(δ) is well defined. "2/δ − 1 ≤ T(δ) ≤ 24/δ − 2" is right only at δ = 2/m.

## (1″) Lemma 1″ and Theorem A″
- c(n) ≤ r(n): different (i, b) give different unordered pairs because b > a_K ≥ a_i′. Pairs with larger element among the a_j
  are deliberately left out; nothing double-counted. N′ = N + a_K runs over every large integer; N → ∞ then K → ∞ is
  legitimate because d(M_R) does not depend on K. (With 0 ∈ A, |B_N| = A(N) − K + 1: cosmetic.)
- Numerics (`test_lemma1pp.py`): nine sets, K ∈ {1,2,5,50,500}, R ≤ 1000, N ≤ 150,000, c(n) from its definition: 0 violations;
  hill-climb max lhs − rhs = 0. Measured popular density: 7ℕ and 20ℕ exactly 1/7, 1/20 at R = 1; {0,1 mod 7}: 3/7; odd
  numbers 1/2; random 0.3: 0.99. Shortfalls at large R are a constant (finite-N lag), so the density tends to δ.
- Steps 2–4 with s = ⌈2/δ⌉: sδ ≥ 2, g ≤ s − 1, |E_t| ≤ s − 2, total ≤ 3s − 2.
- Numbers: δ = 1/5: Veljjanoski 598, Theorem A 118, A″ 28. δ = 2/m: m − 1 ≤ T ≤ 3m − 2. 3⌈2/δ⌉ − 2 < 6/δ + 1.
  No conflict with Chen–Yu (density > 1/2 ⇒ restricted order 2).

## (2) Kneser
Source: Hegyvári–Hennecart–Plagne, author preprint of the CPC 2007 paper (hegyvari.web.elte.hu/artEB4.pdf), proof of Theorem 8:
> "We thus have jdB > 1 ≥ djB. By Kneser's theorem on asymptotic densities of sequences of integers (cf. [9, 10], [4] or
> [12]), we obtain that there exist an integer g ≥ 1 and a sequence B1 of integers such that B ⊆ B1, g + B1 ⊂ B1,
> jB1 ∖ jB is finite, and d jB1 ≥ j dB1 − (j−1)/g."
([9] = Kneser, Math. Z. 58 (1953); [4] = Halberstam–Roth; B = hA, no 0 assumed.) Kneser 1953 and Halberstam–Roth were NOT
reached directly. The s-fold version follows from the two-set theorem plus Kneser in a finite group; 0 ∈ M is not needed
(else use M_R ∪ {0}: "at most s" summands, which only helps); "g + M′ ⊆ M′" is all the argument uses; the deduction
"y₀ ∈ sM_R ⇒ every large n ≡ y₀ (mod g) is in sM_R" survives the exact form.

## (3) Theorem B
- Key Lemma survives digit by digit including carries; n ≡ 2 mod 4 forces exactly two odd summands; n ≡ 0 mod 4 handled;
  3^j − 15 = 2…2110₃ for j = 3..60 with the explicit 4-term representation; whether 0 ∈ A does not matter.
- Independent brute force (`ternary_ref.py`: exact pair counts + inclusion–exclusion searches, every witness re-verified),
  largest N = 100,000,000: not a sum of ≤ 3 distinct = {2·3^j : j ≤ 16} (17 numbers, up to 86,093,442); not a sum of ≤ 4
  distinct = {2, 6, 18}; order-2 misses 0. Same at 1e7, 3e7; identical to `ternary_bitset.py` at 300,000; plain itertools at 1,500 agrees.
- Key Lemma by brute force, k ≤ 40,000: unsolvable k = {3^j − 1} exactly.
- Negative controls (N = 1e6): drop 12 → 15 joins the "≤ 3" exceptions and 11 order-2 misses; drop 1 → "≤ 4" exceptions
  {1,2,5,6,8,17,18}; replace 4a by 4a + 4 → "≤ 3" exceptions {2, 6}.
- Lean vs our description: `ternaryBasis` CONTAINS 0; "order 2" = multiset of ≤ 2 elements, proof covers every m ≥ 1; the
  formal statement is only "not restricted order 3" (via n = 2·3^N at the eventual threshold; the argument shows every
  2·3^j fails). Restricted order exactly 4 is NOT in the Lean file — that is Theorem B. The "could not access / may
  differ" remark is in the pull request description, not in 338.lean.

## (4) Veljjanoski's Theorem 2
Proof sound (existence of y; covering argument forcing |S′| ≤ 2; both cases close). `python3 -I block338.py` reproduces
his output byte for byte. Own test (`block_ref.py`, exact Fractions): controls reproduce 4/5, 7/11, 9/16; 20,000 random C
(≤ 7 elements; halves, thirds, denominators to 1e6, near-ties): l* = 3 for 12,352 and 4 for 7,648; hill-climb and an
exhaustive quarter-grid (7,806 sets) top out at 4. Max l* = 4. A statement about the model only.

## SHOULD fixes (all applied on the page / in CLAIMS)
1. Say A ⊆ positive integers (0 ∉ A) in Step 1′(ii) and Lemma 1″.
2. Corollary A: the range holds at δ = 2/m only; in general ⌊2/δ⌋ − 1 ≤ T(δ).
3. Corollary A″: "for δ ∈ (0,1], ⌊2/δ⌋ − 1 ≤ T(δ) ≤ 3⌈2/δ⌉ − 2 < 6/δ + 1".
4. The Lean set contains 0 (immaterial).
5. "could not access his paper / may differ" comes from the PR description, not the Lean file.
6. His README's "Theorem 10 / Theorem 9 / Conjecture 2" are Theorem 8 / Theorem 7 / Conjecture 1 in the author preprint; check the published numbering before quoting.
7. One line: 0 ∈ M_R is not needed for Kneser.

## What a careful reader could still object to
- Novelty of A″: Lemma 1″ is a few lines of counting over K translates; Theorem A″ is the HHP template plus their
  disjoint-representation step. A routine combination; do not oversell.
- The factor 3 between ≈ 2/δ and ≈ 6/δ remains: "linear in 1/δ" is right, "sharp" would oversell.
- Kneser was quoted from HHP, not read in the original.
- Theorem 2 is about the model; the reduction to actual integer sets was not re-derived.

---
# Addendum (same referee instance, resumed 09:40Z): Theorem C (the bound 4⌈1/δ⌉ − 4 from Erdős–Nathanson–Sárközy 1988)
Verdict: HOLDS WITH FIXES — one MUST (the "factor 2" sentence), five SHOULDs. ENS checked against the page images
(pp. 161–162), not only the OCR. Scripts/outputs: `c_checks.py`, `c_checks_m8.out`, `c_checks_m13.out`.

(a) The ENS proof gives ALL large integers of a class. Their Kneser form (p. 161): "either (i) d_L(hA) ≥ h d_L(A) or (ii)
there exists a minimal integer g ≥ 1 such that hA ∼ hA^(g) and d_L(hA) ≥ h d_L(A) − (h−1)/g". Case (i) impossible for
every s ≥ 1. d_L ≤ 1 − 1/g when g > 1 is minimal (a missed class). (k+s)w − (k+s−1)/g ≤ 1 − 1/g ⇒
g ≤ (k+s−2)/((k+s)w − 1) ≤ k + (k²−2k)/s since w ≥ 1/k. Using k = ⌈1/δ⌉ with δ only a lower bound for d_L(A) is valid.
(b) Lemma 1 (Szemerédi) and Lemma 2 are sound for general h: an admissible i always exists (each u ∈ F other than v forbids
at most one i; at most h − 2 forbidden out of h − 1); after the swap every summand outside G is still an original element
of A′; 0 ∉ A not needed. ENS's own application has two slips at k = 2 that do not affect Theorem C (it takes t = k + s):
Theorem 1(i) with k = 2 uses t = k² − k = 2 for 3 summands (Lemma 2 needs t ≥ h); Theorem 1(ii) with k = 2 has s = 0
while the proof assumes s ≥ 1.
(c) The derivation is legitimate: G = 2k − 2 is fixed before E; the g returned for A₀ = A \ E satisfies
g ≤ 2k − 1 − 1/(k−1) < 2k − 1; "≤ g − 1 elements realise every class" by Step 3; disjointness automatic (summands from
A \ E); count (2k − 1) + (g − 1) ≤ 4k − 4; g = 1 fine. The residue hypothesis is only used for g ≤ 2k − 2.
(d) δ ≤ 1/2 is not needed: any δ < 1 gives 4⌈1/δ⌉ − 4 (δ = 1 gives 2); above 1/2 Chen–Yu's 2 is stronger anyway.
(e) Numbers right (4, 16, 36, 196 vs lower bounds 3, 9, 19, 99). "Factor 2" is NOT right: over δ ∈ [1/200, 1/2] the ratio
upper/lower reaches 8/3 just below 1/2 (δ = 0.49: 8 vs 3); it is (4k−4)/(2k−1) < 2 at δ = 1/k, below 2/(1−δ) always,
and tends to 2 as δ → 0. No choice of s beats s = k − 1 (k = 2..60: the minimum over s equals 4k − 4, unique minimiser).
(f) Numerical check: every periodic set {n : n mod m ∈ S}, m ≤ 13, density ≤ 1/2, satisfying the residue hypothesis
(8,667 sets), true restricted order by exact distinct-summand DP on [1, 40m²]: 0 violations of 4⌈1/δ⌉ − 4; largest
true/bound ratio 3/4 (m = 4, S = {0,1}); no periodic set beat ⌊2/δ⌋ − 1. Eight non-periodic sets: orders 2–6 vs bounds 4–20.

MUST: replace "known up to a factor 2 for δ ≤ 1/2". (Applied: the page says the ratio is at most 8/3 and tends to 2.)
SHOULD: (1) δ ≤ 1/2 unnecessary; (2) hypothesis only needed for g ≤ 2k − 2; (3) note ENS's two k = 2 slips if citing
Theorem 1 as stated; (4) "the residue class of y₀ mod the minimal g"; (5) s = k − 1 is optimal in this method.
Still open to objection: Theorem C rests on Szemerédi's theorem and on ENS's form of Kneser (checked against the scan,
not against Kneser 1953). Crediting the linear dependence to the ENS method is right.
