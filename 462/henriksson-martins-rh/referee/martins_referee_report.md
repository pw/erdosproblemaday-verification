**Hostile referee report: P. Martins, "Least prime factors in short intervals under the Riemann Hypothesis" (22 Nov 2026), Erdős #462**

I read the whole paper and rechecked every lemma behind Theorems 1.3, 1.5 and 1.6 line by line. I recomputed every constant the paper states, read the cited results in their arXiv versions, and re-ran part of the numerical table. I could not refute any of the three theorems. I found one real but harmless constant error, and some citation points I could not check. The Lean file does not prove any of the main theorems.

## Verdict per theorem

| Theorem | Verdict | Conditional on |
|---|---|---|
| 1.3: S_C(x) ≥ min{C/54, C²/K} | **HOLDS** | RH |
| 1.5: \|S_C(x) − 4C\| ≤ K′C^{1/2} | **HOLDS**, with a constant error in Prop 5.5 (O1) that does not affect it | RH |
| 1.6: S_C(x) = 4C + o(1) | **HOLDS** | Hypothesis PC exactly as stated in (1.3) |

**What this means for the claim.** It is marked "solved", but nothing here is unconditional. The paper proves the composite-only reading (its Problem 1.2) under RH, and Zhang's Conjecture C under Hypothesis PC. The literal reading (1.1) under RH is classical: there is always a prime in [x, x + (22/25)√x log x], so every window has a term equal to 1. The paper's own claim (§1.3) is only a conditional solution: "no solution of Problem 1.2 conditional on the Riemann Hypothesis … has appeared." My recommendation is **PARTIAL**, described as "a correct conditional (RH) resolution of the composite-only reading, not a solution." Use VERIFIED only if the site labels it "conditional on RH".

## Objections

**O1. False inequality in Proposition 5.5, Step 6 (printed p. 18). Real error, cosmetic effect.**
- The paper says (I confirmed this in the rendered PDF): "By (5.4), using δ′ ≤ δ₊ ≤ (9/8)δ = (9/8)C(log x)²x^{−1/2}".
- But §5.3 defines "For 0 < ε ≤ 1/8 put δ₋ := (1 − 2ε)δ, δ₊ := (1 + 3ε)δ". At ε = 1/8 that gives δ₊ = (11/8)δ.
- So "≤ (9/8)δ" holds only for ε ≤ 1/24. The constant 61 in Proposition 5.5 is unproved for ε ∈ (1/24, 1/8]. The corrected constant is (11/8)(2880)^{1/2} ≈ 73.8, so 74 instead of 61.
- The same 9/8 reappears in the proof of Theorem 1.6: "δ′ ≤ (9/8)C(log x)²x^{−1/2}".
- Why it does not matter:
  - Theorem 1.5 takes ε = (log x)^{−1/3}, which is at most 1/24 for large x, so 9/8 is valid there.
  - Theorem 1.6 only needs μ(x) → 0 and δ′ ≪ x^{−1/2}(log x)².
  - Fix: restrict ε ≤ 1/24, or replace 61 by 74 and K′ = 160(K₂K₅)^{1/2} by about 195(K₂K₅)^{1/2}.

**O2. Conditional only.** The abstract says "We prove that the Riemann Hypothesis implies S_C(x) ≥ min{C/54, C²/K}". Remark 1.4(b) confirms that RH enters only through Lemma 2.1 / Hypothesis S (for 1.3) and Lemma 5.1 (for 1.5). So the "solved" marking overstates it (see the verdict above).

**O3. Which reading is "the problem" (§1.1): not checked.**
- The paper says: "As printed, the summation in (1.1) is not restricted to composite n" [EG80, p. 92].
- I cannot check EG80, and erdosproblems.com is off limits.
- Zhang's arXiv:2608.24930v2 §1.1 prints the question *with* "n composite" under the sum, yet also quotes Tao's remark that the convention is ambiguous.
- The two papers' renderings of the original differ. The priority/world seat should settle this.

**O4. Minor citation numbering.** "[CHD24, (1.1)]" and "[CHD24, Theorem 1.1]" are numbered (1) and Theorem 1 in arXiv 2206.00433v2; the journal numbering may differ. The content matches: (1) is stated for all δ ∈ [1/x, 1], which covers what Lemma 5.1 uses. The explicit Theorem 1 holds only for x ≥ 10⁸ and δ ≤ 10⁻⁸; the paper invokes it only in effectivity remarks.

## Checks that passed

**Lemma 2.1 (the RH mean-square input).**
- GMP17 Proposition 1 (arXiv 1602.02906v2), with n_K = 1 and d_K = 1, reads ∫_X^{2X}|Δ(x,h)|² ≤ cX(h + L²)L², L = log X, for all X ≥ X₀ and 2 ≤ h ≤ X. This is exactly (2.2).
- So it is valid uniformly down to h ≍ (log X)². For h ≥ (log X)² it gives at most 2c·hX(log X)², with the stated log powers.
- GMP17 itself notes the Saffari–Vaughan misprint at (6.20), as the paper says.
- The dyadic patching and the small-X and initial-segment cases are correct, including K₁ = 2c + 98(1 + X₁³) + 900.

**Hypothesis S and Corollary 2.3.** Trivially correct.

**Lemma 2.5 (prime pairs).**
- The odd-d case and the singular-series bound S(d) ≤ c₃d/φ(d) are correct.
- The restriction d ≤ (log X)³ is what keeps HR's error term in log log 3E/log X uniform, with E = d.
- I did not see HR74 Theorem 5.7 itself (it is a book); the bound is standard.

**Lemma 2.6.** The constant ζ(2)ζ(3)/ζ(6) = 1.94359 is correct.

**Lemmas 2.7 and 2.8.** Correct.

**§4 (Theorem 1.3).**
- I re-derived every parameter and checked (A1)–(A7) and (B1)–(B6).
- Lemma 4.2: q > 2P ≥ p, and 1/q ≥ P/(2x).
- Lemma 4.3: the prime-power bound is equivalent to (A7).
- Lemma 4.4: (y, y+δ] ⊂ J_p.
- Lemma 4.5: |y_p − y_p′| ≥ (L²/4)|p − p′|; the off-diagonal count is 2·1.95·2 ≤ 8; N/δ ≤ P/(L²(log x)²) via (A5); 32·9 = 288; K₄ = 288K₂ + 1.
- Lemma 4.6: Hypothesis S is applied with δ ≥ A₀(log X)², and (K₄η₀/8)^{1/2} = 1/8.
- §4.7: C/4 − C/8 − C/72 = C/9, which gives C/(18L). Then L = max{3, 32K₁K₄/C} gives min{C/54, C²/(576K₁K₄)}.
- No o(1) that depends on C is used uniformly: x₀ is chosen after C.
- The Cauchy–Schwarz step is sound. ‖W‖₂² is within K₄ of what random points would give, so any correlation between the points x/p and the exceptional set of Selberg's estimate is controlled.

**§5 (Theorems 1.5 and 1.6).**
- Lemma 5.1: the θ→ψ prime-power correction is correct.
- Lemma 5.3 (PC ⇒ S⁺): I checked the sandwich bound, the disjointness of the shifted intervals, the PC ranges with ε = 1/12, and the final 48(log 3Y + 1)/(c(log Y)²) + 3/m² (6 + 24 + 18 = 48).
- Lemma 5.4: the main term T = 4C(1 + O(log⁻²x)) is correct.
- Steps 1–7:
  - Step 1: the upper-bound case split (R₁, R₂, R₃) is complete.
  - Step 2: Brun–Titchmarsh gives R₄ = 100Cx^{−1/10}.
  - Step 3: R₅ is correct.
  - Step 4: both smoothing containments hold.
  - (5.4): both terms re-derived exactly.
  - The claim that R_C does not depend on ε is true.
- Proof of Theorem 1.5: μ_j ≤ 8K₅/(3C2^j); Σ2^{−3j/2} = 1.547; (8/3)^{1/2} = 1.633; 61·2.6 = 158.6.
- Proof of Theorem 1.6: (3/8)C(log x)²2^j ≥ (C/4)(log Y)², δ′Y ≤ Y^{1/3}, and every Y ≥ x^{1/2}/2.

**Classical facts.**
- The composite sum's main term 8x^{1/2}/(log x)² comes out from the s-integral: 2x^{1/2}/ℓ² with ℓ = ½log x.
- The window main term 4C follows from H·(d/dx) of that, and independently from Lemma 5.4.
- Composites with p(n) ≤ x^{1/3} contribute O(Cx^{−1/6}(log x)²) = o(1).
- The density e^{−s}ds puts the bulk of the sum on n = pq with p ≍ x^{1/2}; the shares 1 − 1/L match the table.

**Numerics re-run** (script `/tmp/e1122/seatM/scripts/s1.py`):
- S₁ = 4.2537, 4.2587, 4.2148, 4.1642 at x = 10⁶, 2·10⁶, 10⁷, 10⁸.
- B₃ = 2.4930 and B₁₀ = 3.3381 at x = 10⁶, and 13,785 primes in that window.
- S_{1/4}(10⁹) = 1.0349, inside the stated range [1.0292, 1.0358].
- All match Table 1 exactly.

## Lean file (`LeastPrimeFactorRH.lean`)

The header says: "Written … but not yet compiled". Nothing in it, including the parts without `sorry`, has been machine-checked.

**19 `sorry`s:** lemma_2_1 (l.194), lemma_2_6 (255), lemma_2_8 (278), prime_in_short_interval_of_hypothesisZ' (387), proposition_3_1 (408), eventually_large (479), B4 (566), B5 (572), lemma_4_2 (604), lemma_4_3 (615), lemma_4_4 (623), lemma_4_5 (633), lemma_4_6 (645), corollary_4_7 (773), lemma_5_1 (805), lemma_5_3 (830), lemma_5_4 (847), theorem_1_5 (866), theorem_1_6_of_Splus (874). There are no `axiom`, `admit` or `native_decide` declarations.

**Results from the literature passed in as `Prop` hypotheses:** GMPBound, ChebyshevBound, ChebyshevPiBound, PrimePairBound, DyadicPNT, CMSGapBound, PNTErrorTerm, SelbergThetaBound, BrunTitchmarsh.
- GMPBound, CMSGapBound and SelbergThetaBound enter as `RiemannHypothesis → …`.
- Also taken as hypotheses: Mathlib's `RiemannHypothesis`, HypothesisPC, HypothesisSplus, HypothesisZ′ and ZhangTheoremB.
- GMPBound, CMSGapBound, SelbergThetaBound and HypothesisPC faithfully match their sources or the paper.

**Which `sorry`s each main theorem depends on:**
- **Theorem 1.3:** lemma_2_1, eventually_large, lemma_4_2, 4_3, 4_4, 4_6. All the real mathematical content (§§4.2–4.6 and the dyadic part of Lemma 2.1) is `sorry`. Only the assembly arithmetic, Corollary 2.3, (B1)–(B3), (B6) and `min_le_bound` are written without `sorry`.
- **Theorem 1.5:** its own body is `sorry`. Its RH and Selberg hypotheses are never used.
- **Theorem 1.6:** lemma_5_3 and theorem_1_6_of_Splus, both `sorry`.
- Lemma 4.5, B4, B5, Lemmas 5.1 and 5.4, Corollary 4.7 and Proposition 3.1 are never referenced in any proof term; they are standalone statements.
- Without `sorry` (still uncompiled): problem_1_1_of_RH (assuming the CMS19 Theorem 5 hypothesis), hypothesisZ_false, problem_1_2_of_sqrt_bound, and the Problem 1.2 ⇒ 1.1 implications.

**Is the file's Status section accurate?** Its list of `sorry`s is exact. "Proved here, with no `sorry` in their own proofs" is literally true, but it is uncompiled. As the file's own axiom comment says, Theorems 1.3, 1.5 and 1.6 all still depend on `sorryAx`.

## Prior-work claims checked against sources

- **Zhang arXiv:2608.24930v2:**
  - Theorems 1.1, 1.3, 1.4, Hypothesis 1.5 ("for all y ≥ 2"), Remark 1.6, Theorem 1.7 and Conjecture 1.8 match Theorem A, Hypothesis Z, Theorem B and Conjecture C.
  - Zhang's §5 does take "C₀ := 4C (or any fixed C₀ ≤ 4C)".
  - The paper's point that Hypothesis Z forces gaps p_{n+1} − p_n = o((log p_n)²) is right; Zhang himself writes "(C₀ + o(1))(log p_n)²". Also e^{−γ}/2 = 0.2807.
  - The paper uses Zhang only for context: Proposition 3.1 re-proves Theorem A(i), and Theorems A and B are not used in any proof.
- **CMS19 Theorem 5** is indeed the forward interval [x, x + (22/25)√x log x], x ≥ 4. Quoted correctly.
- **BFT23:** the abstract supports the gap-versus-Hardy–Littlewood remark.

## Not checked

- HR74 Theorem 5.7, read in the book itself.
- Selberg 1943, read directly (checked only via CHD24 and GMP17).
- LP00 Theorem 1 / GM87: the equivalence of Hypothesis PC with pair correlation in Remark 1.7(a). This only bears on the remark; Theorem 1.6 assumes PC directly.
- Saffari–Vaughan (SV77) Lemmas 5–6.
- EG80 p. 92 ("as printed").
- Novelty or priority (left to the other seat).
- Compiling the Lean file.

The downloaded sources are in `/tmp/e1122/seatM/src/` (GMP17, CHD24, CMS19, Zhang).