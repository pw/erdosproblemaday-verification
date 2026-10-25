VERDICT: HOLDS AS READ (seat P scope: Blinov's patch §3 and §4 hunks (norm decomposition, reserved-tag packing, generalised orb:conditional, Lemma orb:tagged-moment), Chen §2, the Lean statements behind them)

Seat P, hostile referee. I found no MUST-FIX defect in the algebra, the packing or the fresh-digit lemma. Every finite fact in scope was recomputed by my own code (none of the authors' scripts or certificates were imported, copied or run). Each check has a mutated input that it rejected. The findings below are all NIT-level. Two items were checked and found NOT to be defects; I list them so the panel does not re-flag them.

Labels are the printed TeX labels from `patches/reserved-tags.patch` (Blinov, e29a291) and Chen's printed equation and section numbers (PDF dated 18 Oct 2026).

## Findings

1. **NIT. The 18-form table only works if (σ(1),σ(2),σ(3)) is read in one-line notation; neither text says so.** Blinov, proof of Lemma `norm:decomposition`: "For each row permutation $\sigma$, the three listed coefficient vectors $c$ define $h(x,y)=\sum_i c_i x_{\sigma(i)}y_i$". Chen §2.1, before (3), says the same: "$h_{p,c}(x,y)=\sum_{i=1}^3 c_ix_{p(i)}y_i$".
   - With the one-line reading, identity (3) holds exactly over Z[u]/(u²−u+1): 0 residual monomials.
   - With the inverse reading x_{σ⁻¹(i)}, which swaps the rows labelled (3,1,2) and (2,3,1), the identity FAILS: 4 nonzero residual monomials.
   - A cycle-notation reading would list (1 2 3) twice, so it cannot be intended.
   - The formula x_{σ(i)} is stated, so the table is determined. Still, one word ("one-line notation") would remove the only ambiguity in an identity that both papers treat as their key new algebraic input.

2. **NIT. The patch's descent step uses notation it never defines.** Patch, proof of Lemma `norm:decomposition`: "Interpolation at $9$ distinct nodes gives $\ell(xyz)=\sum_s\widehat x(s)\widehat y(s)\ell(c_sz)$. Thus the rows $3^{-2}\widehat F_{1w}(s)$, $\widehat F_{2w}(s)$, $\ell(c_sF_{3w})$ give $9\cdot18^2$ base-field determinants."
   - In the patch, x̂ (the power-basis coordinate polynomial of degree ≤ 4) and c_s = L_s(ϑ) (the Lagrange basis) are undefined. The same goes for "$g_0(Z_i(X))$" (meaning the singleton conjugate applied entrywise).
   - They are defined in `notes/sphere-packing.tex` (lines 806–808 and 823–827) and in Chen (5)–(6).
   - The construction is correct as intended; my literal implementation reproduces the norm (see "What I checked", item 2).
   - Since the patch is the written proof, it should carry the two definitions.

3. **NIT. The slope step overstates what is determined.** Patch, proof of Lemma `orb:tagged-moment`: "the equation $F_{k-1}=0$ determines that digit uniquely". The correct statement is "admits at most one of the $M$ allowed values", because the forced value may not be an allowed digit. The proof then uses only "at most one", which is correct. Chen §2.4 phrases it correctly ("At most one of its M values gives zero").

4. **NIT. Chen cites a checker that is not in his release.** Chen §2.1, after (3): "The packet's checker implements this calculation by (a,b)(c,d)=(ac−bd, ad+bc+bd) … It expands 18·27=486 terms and verifies the thirty-six nonzero coefficients."
   - No checker is in the public release: `problems/bound-191/` contains only `README.md` and `paper.pdf`. So the "finite coefficient verification" in the text is a description of a computation, not a verification a reader can rerun.
   - The identity is true (my symbolic check below), so this is a reproducibility NIT.
   - A complete check must also confirm that the 693 non-permutation coefficients vanish. The text says "gives zero unless both triples are permutations", which covers this in words.

5. **NIT. Leftover text in the transferred files.**
   - The patch does not touch §1, which still says (01-introduction.tex, intro paragraph) "We express that polynomial as a sum of monomial determinants". After the transfer the summands are no longer monomial determinants.
   - Patched §3, eq. `norm:positions` context: "All words have centered squared norm $12$" and "The original encoding radix product is $3^{12}$" are vestigial from earlier checkpoints and play no role.
   - None of this is load-bearing. The old Lemma `norm:decomposition` clause "obtained from three distinct degree-$d$ monomials" was deleted. I grepped §§4–8 of the pinned source: nothing downstream uses it. Its only other mention is the §1 sentence above.

6. **NIT. The review guide's exponent pointer names a theorem for a different k.**
   - `docs/review.md` points "Deletion inequalities and exponent identity" at `FiveScales.lean`.
   - But `FiveScales.exact_exponent : 249 * 1166895 + 5 = 2 * 145278430` is for the previous checkpoint's k = 1,166,895.
   - The identity for the claimed k = 408,781 is `ReservedPacking.exact_exponent : 249*packingSize+5 = 2*50893237`. It is correct: I recomputed 249·408781+5 = 101,786,474 = 2·50,893,237.

**Checked and NOT a defect.**

- **4(b), "are all coefficients of U below B?"** This is not needed. If U_n = 0 for n < a and 0 < |U_a| < B, then U(B) = B^a(U_a + B·W) with W an integer, so v_B(U(B)) = a exactly, whatever the sizes of the higher coefficients. Lean `FiveTags.eval_first_valuation` correctly assumes only `hlo`, `hne` and `|U.coeff a| < B`. In any case all |U_n| ≤ 2k·r² ≪ B.
- **The tight case is real.** In the M=3 toy (below), P(b≥2, F_{k−1}=0) equals M^{−5} = 1/243 exactly. The joint bound M^{−(2j+1)} is sharp, not loose. That is a sign the mechanism is what the authors say it is, not an artefact of a weak test.

## What I checked and how
All code is in `/tmp/oaimath/191b/seats/P_work/`. Each run used `bash -c 'ulimit -v 8000000; exec timeout … nice -n 19 <python> -I <script>'`. The python was `~/.venv/bin/python -I` (sympy 1.14, numpy 2.4.6) or `python3 -I`. No file under `src/` was executed or imported. The patch table was parsed as text.

1. **18-form identity, symbolic** (`t1_eighteen.py`, sympy, all 18 matrix entries indeterminate):
   - Parsed the table out of `reserved-tags.patch` programmatically. Transcribed Chen's table by eye from the 150-dpi render of PDF p.2 (`render/chen-02.png`).
   - The two tables are token-for-token identical.
   - Σ_{t=1}^{18} Π_{j=1}^{3} h_t(A_{·j},C_{·j}) − 3·det A·det C reduces to 0 mod u²−u+1: 0 residual monomials for both tables.
   - Controls, all rejected:
     - multipliers 1, −3, 6 leave 36 residual monomials each;
     - every one of the 54 single-coefficient sign flips breaks the identity (54/54);
     - u→v in one entry: 18 residuals;
     - inverse-permutation reading: 4 residuals (finding 1).
2. **Degree-five norm decomposition end to end, over real finite fields** (`t2_norm.py`, my own F_{r^5} arithmetic):
   - Setup: a random irreducible monic quintic (irreducibility via gcd(T^{r^i}−T, m) = 1 for i = 1, 2) and power basis 1, ϑ, …, ϑ⁴.
   - The construction follows the patch literally:
     - conjugate pairs (σZ, σ²Z) and (σ³Z, σ⁴Z), singleton Z;
     - F_{iw} = Z_i·H_w;
     - rows 3^{−2}·F̂_{1w}(s), F̂_{2w}(s), ℓ(L_s(ϑ)·F_{3w});
     - nodes 0..8;
     - 2,916 determinants per input.
   - Results:
     - r = 37 (roots u = 11, 27): construction = Nm(det) on 60/60 random inputs, all with nonzero norm.
     - r = 43 (u = 7, 37): 60/60.
     - The other root of u²−u+1: 10/10 at both primes.
     - 9 random distinct nodes: 10/10 at both primes.
     - Degree-5 homogeneity in a group: 5/5.
   - Labels: distinct Vandermonde labels give a sum ≠ 0 (20/20). Two equal labels give 0 (20/20).
   - Controls:
     - dropping one node: agreement 1/20 at both primes, which is chance level 1/r;
     - omitting 3^{−2}: 0/20;
     - a non-root u: 0/20 and 2/20 (chance);
     - r = 41 ≡ 2 (mod 3): u²−u+1 has no root, so the construction is impossible.
   - Chen's arbitrary-basis variant (`t2b_chen_basis.py`, Z in a random basis β, ℓ in the power basis): 30/30.
3. **Packing, exhaustive** (`t3_packing.py`):
   - Counts:
     - 4,096 twelve-digit {0,1}-words in base 3;
     - below 10: exactly {0, 1, 3, 4, 9};
     - below 204,391: 2,921 words, max 204,390 (= ternary reading of 2920 = 101101101000₂; the next word is 204,391 itself);
     - norm words: T = 2,916;
     - k = 408,781, with 2·max = 408,780 = k−1;
     - ℓ ranges over [0, 408,760].
   - Midpoint-freeness:
     - all 8,390,656 unordered pairs (equal pairs included) of the full cube: 0 violations;
     - all 4,267,581 pairs of the 2,921-set: 0 violations.
   - Full support matching: row 1 = {0} ∪ norm, row 2 = {0,1,3,4,9} ∪ norm, row 3 = ℓ-positions.
     - Exactly 2,916 position triples sum to k−1. All are matched (a = a′ = a″) and tag-free.
     - This covers one tag in row 1, one tag in row 2, and two tags.
   - Controls:
     - tag set (0,1,3,4,8) creates the spurious triple (12, 8, 408760);
     - ℓ = k−2c gives 0 matched triples;
     - consecutive-integer positions give midpoint violations.
4. **Lemma `orb:tagged-moment` / Chen §2.4.**
   - **Line-by-line reading:**
     - (a) F = U(Z1−Z2), with M_33 = 0 and M_31 = M_32 = U.
     - (b) Row 1 below 10 is 1 then r's. Row 2 is the tag representatives at 0, 1, 3, 4, 9 and r elsewhere. Norm positions are ≥ 10 in rows 1 and 2.
     - (c) A0/(B−1) ≤ 6k²P/(100k²P) = 3/50, and (47B^{k−1}+3)/50 > τ.
     - (d) The Schur congruences touch only positions < j ≤ a < 10 ≤ v. z2_v enters F_{k−1} only through U_{k−1−v} = U_a, with coefficient −U_a.
     - (e) B ≤ 200k²P = 80000k⁴r⁶ and M² = 160000k⁴r⁶, so θ ≤ 1/2 exactly.
     - (f) P(exactly two equal) ≤ 3r^{−5}, P(all equal) = r^{−10}, distinct gives 0, total 6/(Mr⁵) + 2/r¹⁰. With M = 400k²r³ this is O(r^{−8}).
     - The generalised `orb:conditional`: with L2 = r, p* = M^{−2} and θ = B/M².
   - **Real-construction check of 4(b)** (`t4c_realU.py`): real tag layout, r = 37, real digit reps, random residues at the low norm positions. U_n = 0 for n < a and 0 < |U_a| < r in 2000/2000 (λ, μ) pairs. Control: removing the residue-1 tag (A_0 = r) breaks |U_a| < r in 200/200.
   - **Independent exact toy, small base** (`t4_toy.py`), my own model:
     - Setup:
       - label space F_r^m, row-1 residue 1 at position 0, row-2 tags at sparse positions;
       - label-dependent arbitrary residues above the tag span in rows 1–2;
       - row-3 residues in three modes: label-dependent random, all-zero (adversarial) and shared;
       - L1 = L2 = r; row-3 digits with M choices; B prime > L3.
     - b is computed from all nine 2×2 minors mod B^k. F_{k−1} is computed generically from the row-3 cofactor expansion; the factorisation is not assumed, and its shape (W3 = 0, W1 = −W2) is observed rather than imposed.
     - M = 3, r = 7, tags (0,2), k = 5, B = 23, all three row-3 modes:
       - every P(b≥j, F_{k−1}=0) ≤ M^{−(2j+1)}, tight at j = 2 (1/243 = 1/243);
       - b ≤ a always;
       - P(F_{k−1}=0) ≤ 1/M;
       - E[D·1] ≤ M^{−1}(1 + Σθ^j);
       - uniform P(b≥j) ≤ M^{−2j}.
     - k = 8, M = 2, r = 5, tags (0,1,3), so a ∈ {0,1,3}. Exactly 2^24 outcomes per label triple.
       - Bases B = 11 and B = 13, three row-3 modes each, six label triples each. The triples were a = 0, a = 1, two with a = 3 (one with zero label coordinates, represented by r), all-equal, and distinct.
       - All 36 configurations are OK:
         - every P(b≥j, F_{k−1}=0) ≤ M^{−(2j+1)}; in the adversarial zero mode at a = 3 the values are 1/64, 1/128, 1/256 (or 5/256, 5/512, 1/256) against 1/8, 1/32, 1/128;
         - b_max ≤ a;
         - P(F_{k−1}=0) ≤ 1/M;
         - E[D·1_{F=0}] ≤ M^{−1}(1 + Σ_{j≤a}(B/M²)^j);
         - P(b≥j) ≤ M^{−2j} for j = 1..3 on every triple, including all-equal and distinct.
       - A B = 23 run aborted on my own int64-overflow guard (23^8 > 2^31), not on a bound. It was replaced by the B = 13 run. Output is in `t4_main.out` and `t4_main_B13.out`.
   - **Negative controls (must fail, and do):**
     - Fresh position inside the Schur prefix (k = 2, a = 1, v = 0, zero row-3 residues): P(b≥1, F=0) = 1/4 against the bound 1/8 (M = 2), and 1/9 against 1/27 (M = 3). FAIL, as required.
     - a = 3, k = 6 (v = 2 < j = 3): j = 1, 2 pass but j = 3 gives 1/64 against 1/128, FAIL. The same labels with k = 8 (v = 4 ≥ 3) pass all j. So the requirement v ≥ j is exactly where the bound breaks.
     - Omitted distinguishing tag (top rows identical, U ≡ 0): P(F=0) = 1, P(b≥1, F=0) = 1/4 > 1/8, b_max = 6 > a.
   - **Actual event J with a large base** (`t4b_J.py`, B prime > 100k²P: 400009 for M = 2, 600011 for M = 3; r = 5, tags (0,1), k = 4):
     - exact enumeration over all 8³ and 81³ outcomes, 16 label/mode configurations;
     - J ⇒ F_{k−1} = 0: 0 violations;
     - P(J) ≤ 1/M; P(b≥j, J) ≤ M^{−(2j+1)}; b ≤ a; E[D·1_J] ≤ M^{−1}(1 + Σθ^j); all-equal labels give P(J) = 1. All OK.
5. **Distinct labels ⇒ not J, with the tags present** (`t5_obstruction.py`): real k = 408,781 layout, real tags, real f_{ia} values from the construction in item 2 at r = 37.
   - γ_{k−1} mod r was computed by brute force over all supported position pairs for each of the six permutations, with no use of the matching lemma.
   - Distinct labels: γ_{k−1} ≡ Nm(Vandermonde) ≠ 0 in 4/4 (values 2, 13, 24, 27).
   - Labels (λ,λ,μ): γ_{k−1} ≡ 0.
   - Control: tags at (0,1,3,4,8) break the congruence in 3/3 (γ = 2, 18, 21 against N = 31, 10, 35).
6. **Lean, read only, nothing built.**
   - `grep -i 'sorry|admit|axiom|native|implemented|extern|unsafe|reduceBool|trust'` over `lean/`: no hits except `#print axioms` lines and two `set_option maxHeartbeats/maxRecDepth`.
   - Statements read:
     - `FiveTagged.tagged_small_residue_moment`. Hypotheses: a < d; 2d ≤ k; A, A′ agree up to a; A.coeff 0 = 1; Q, Q′ agree below a and differ at a; both values in [1, r]; repeated top/second rows; |coeff| ≤ r for i < k; bottom digits ≤ L; 100k²r²L < base; base/M² ≤ 1/2. Conclusion: smallMoment ≤ 2/M, where smallResidue is ∃t, B^k | det − t ∧ 2|t| ≤ B^{k−1}, which is J, and the exponent is defined from all actual 2×2 integer minors.
     - `FiveFiniteTheorem.total_small_residue_moment`: average over N labels ≤ 6/(MN) + 2/N². Inputs are TaggedData for exactly-two-equal triples after a permutation, plus a distinct-label exclusion interface.
     - `FiveNorm.finite_field_norm`: finrank 5, u²−u+1 = 0, 3 ≠ 0, |F| ≥ 9; the norm is a sum of 2,916 base-field determinants.
     - `ReservedPacking.reserved_packing`: positions u ∈ [10, 408781), v = packingSize−1−2u, injective, matching iff a = b = c, one-tag and two-tag exclusions.
     - `FiveScales`: fresh_position, alteration_constraints, exponent_identity; for exact_exponent see finding 6.
   - All hypotheses match what the written transfer supplies: d = 10, k = 408,781, r = L1 = L2 bounds, L = L3, 100k²P < B, θ ≤ 1/2.
   - The instantiation of the tag data from the norm packing, the distinct-label exclusion, and minor-exponent = Smith b are not in Lean, as the author states. I checked the first two numerically (items 4 and 5). The third is the last assertion of the pinned Lemma `orb:diagonal`, which I re-read and accept.

## What I did NOT check
- The CGLV attribution: I did not read whether arXiv:1909.04785 Theorem 4.1 is exactly this table "with the second coefficient column multiplied by three". The abstract confirms the paper concerns Waring rank bounds for det₃. The identity itself was verified directly, so nothing rests on the citation.
- §§5–8 of the transfer: slab cap, lifting identity, weighted count, zero-determinant count, deletion and exponent choice. Chen §3 onward: the box N = (hq)⁴/B^{s0} and the BMOR primes. These belong to the other seats.
- I did not build or run the Lean project, its scripts or its certificates, and I did not compare my numbers to their JSON artifacts.
- Chen's explicit constants (c, N0).
- Whether the PNT-in-progressions step is correctly applied.
