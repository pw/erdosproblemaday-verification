**VERDICT: HOLDS WITH FIXES** — Theorems 1 and 2 are correct as proved (no gap in Lemmas 1–5, 2/2′, 3/3′, the shield, Theorem 3/3′ or the aperiodicity step; my own greedy = closed form at every integer to 10^7 under both rules — 1,224,510 and 1,224,509 elements, first offending integer: none; negative controls fail at t = 126). Fixes still OPEN in the reviewed version: (F1) "Y0' has runs of 2·8^k members and 4·8^k non-members" — the non-member runs are 12·8^k long; (F4′) the new census caveat names the wrong quotient — "16,385, the start of J_4" should be 16,384 (the last quotient of K_4; J_4 starts there too); (F5′) "Queneau 1972 and Finch 1992 concern two-term bases as described by van Berkel–Bosma (§2) and Green's references [119]" — vBB §2 never mentions Finch 1992, and the Green excerpt does not say what [119] is or that it concerns two-term bases; (F6′) entry/COMMIT_MSG.txt says "F1–F6 applied" and the headline tag says "HOLDS WITH FIXES, APPLIED", but F1 is not applied in PROOF.md.

Version reviewed: PROOF.md sha256 472964812d82cb6495d6fea4dbed572a51313dafe5259f5e28448b10b453df13, mtime 12:57:10Z (copy: PROOF_reviewed_snapshot.md). PROOF.md changed twice while I worked (12:39:51Z: the Theorem 1 aperiodicity paragraph; 12:57:10Z: Lemma 5 added, "What the computer checked" items 1/2/4 and "What is new" rewritten, apparently from my draft of this report). All my code and outputs are in this directory (/home/exedev/MathDyad/erdos341q/referee/); I edited nothing else. Status of every finding against that version:

| # | finding | status in reviewed version |
|---|---|---|
| — | Proof of Theorem 1: old "49h would be an ultimate period of the indicator of Y0" | FIXED IN SOURCE (12:39Z); corrected text checked, HOLDS (§5) |
| F1 | Theorem 2 run length "4·8^k non-members" (true: 12·8^k) | OPEN |
| F2 | "FAIL when any one block endpoint is moved by one" overclaimed its log | FIXED IN SOURCE (now "three mutations" + my run) |
| F3 | rule-D positive control unlogged | FIXED IN SOURCE (runs/control_li.log = my their_gates_control.log, same output) |
| F4 | census window criterion fragile | ACKNOWLEDGED IN SOURCE; but the quotient is misnamed (F4′, OPEN) |
| F5 | provenance: erdosproblems read; #342 "unrelated"; Queneau/Finch | erdosproblems + #342 FIXED (live/341.html, live/342.html checked); Queneau/Finch sentence still unsupported (F5′, OPEN) |
| — | forced-controller claim had no proof | FIXED IN SOURCE: Lemma 5 added; checked, HOLDS (§9) |
| F6 | entry tag pre-announced "HOSTILE REFEREE HOLDS" | tag now claims fixes applied while F1 is open (F6′, OPEN) |

---

## 1. Definition of rule Q vs Green; the seed — HOLDS

Quoted: "a_{n+1} is the least integer > a_n not of the form a_i + a_j with i < j ≤ n (distinct earlier terms)".
Green, Problem 7 (live/green_problem7_excerpt.txt, PDF text with subscripts flattened): "define un+1 to be the smallest integer greater than un and not of the form ui + uj with i < j ⩽ n", seed "Start with some ‘seed’ set of values u1 < · · · < um". The sequence is strictly increasing, so i < j ⟺ u_i < u_j: distinct indices = distinct values = the X ⊕ X of PROOF.md. Same rule. It is also van Berkel–Bosma's "strict" rule ("not equal to the sum of t different previous elements") for t = 2.

The seed is not closed under either rule (1+2 = 3, 2+3 = 5, 7+56 = 63, 5+22 = 27, … all lie in A). Neither Erdős–Graham (OCR of p. 53: "Given a set of integers A, = { a, < ... < a}, extend it", i.e. A_0 = {a_1 < … < a_k}) nor Green (as quoted) restricts the seed; the rule acts only for n ≥ k. Lemma 1 needs only t ∈ S ⟺ t ∉ S ⊕ S for t > N = 97, so seed-internal sums are irrelevant. Note that this is visible in the gates: (G1) fails at q = 1 (1 ∈ Y1 but 1 = 0+1 ∈ Y0 ⊕ Y0, i.e. 63 = 7 + 56 is in the seed although it is a strict sum) — PROOF.md says so correctly: "(The values at q = 0, 1 are prescribed by the seed and are not governed by the gates.)"

Lemma 1 itself: HOLDS. Positivity of S gives u, v < t for every representation, so the scan sees exactly S ∩ [1, t−1]; the first new term must exceed max A = N, which holds since N ∈ S.

## 2. Lemma 2 (S0)(S1)(S2), by hand for all k — HOLDS

Facts used: for an interval [a,b] with b > a, [a,b] ⊕ [a,b] = [2a+1, 2b−1] (s ↦ (⌊(s−1)/2⌋, ⌈(s+1)/2⌉)); [a,b] + [c,d] = [a+c, b+d].

(S0) Y0 = {0,1} ∪ ⋃ I_k, I_k = [8^k+1, 2·8^k], I_0 = {2}. Sums whose larger summand is in I_k (k ≥ 1): {0,1}+I_k = [8^k+1, 2·8^k+1]; 2+I_k = [8^k+3, 2·8^k+2]; I_j+I_k ⊆ [8^k+8^j+2, 2·8^k+2·8^{k−1}] (1 ≤ j < k); I_k ⊕ I_k = [2·8^k+3, 4·8^k−1]. Union = [8^k+1, 4·8^k−1] exactly; the cross-block sums I_j+I_k stay below 2·8^k + 2·8^{k−1} < 4·8^k, so nothing lands in the gap [4·8^k, 8^{k+1}]. The smallest sum with larger summand in I_{k+1} is 8^{k+1}+1. Small sums {0,1,2}: 1, 2, 3. So (S0) as stated.
 Boundary points: 2·8^k+2 ∈ Y0 ⊕ Y0 always via 2 + 2·8^k (0 + (2·8^k+2) and 1 + (2·8^k+1) need non-members; (8^k+1)+(8^k+1) is a double). For k = 1 that is the ONLY representation of 18, so q = 2 ∈ Y0 (the integer 105 ∈ S) is load-bearing there; for k ≥ 2 there are others (e.g. (2·8^k−14) + 16 ∈ I_k + I_1). q = 2 ∈ Y0 is itself forced by (G3) at q = 2 (q−1 = 1 ∉ Y2 ⊕ Y2). 4·8^k ∉ Y0 ⊕ Y0 (max with larger summand in I_k is 4·8^k−1), 8^{k+1} ∉ Y0 ⊕ Y0.

(S1) Y1 = {1} ∪ ⋃ J_k, J_k = [4·8^k, 8·8^k]. 1+J_k = [4·8^k+1, 8·8^k+1]; J_k ⊕ J_k = [8·8^k+1, 16·8^k−1]; J_j+J_k ⊆ [4·8^k+4, 9·8^k] (j < k). Union [4·8^k+1, 16·8^k−1]; 1⊕1 is a double. Boundary: 4·8^k ∉ Y1 ⊕ Y1 (elements below 4·8^k sum to ≤ 2·8^k − 1, and the partner of anything in J_k would be 0 ∉ Y1); 16·8^k ∉ Y1 ⊕ Y1 — its only representation is 8·8^k + 8·8^k, a double. This is exactly where the strict rule differs from Li's rule.

(S2) Y2 = {0} ∪ ⋃ K_k, K_k = [2·8^k, 4·8^k]. 0+K_k = K_k; K_k ⊕ K_k = [4·8^k+1, 8·8^k−1]; K_j+K_k ⊆ [2·8^k+2, 4·8^k+4·8^{k−1}]. Union [2·8^k, 8·8^k−1]; 0⊕0 is a double. Boundary: 8·8^k ∉ Y2 ⊕ Y2 (only 4·8^k + 4·8^k, a double, or 0 + 8·8^k with 8·8^k ∉ Y2).

k = 0, 1 explicitly (by hand, then confirmed by brute force):
 Y0 = {0,1,2} ∪ [9,16] ∪ [65,128]: Y0⊕Y0 = {1,2,3} ∪ [9,31] ∪ [65,255]; complement ∩ [2,∞) = [4,8] ∪ [32,64] ∪ [256,512] = J_0 ∪ J_1 ∪ J_2.
 Y1 = {1} ∪ [4,8] ∪ [32,64]: Y1⊕Y1 = [5,15] ∪ [33,127] ∪ …; complement ∩ [2,∞) = [2,4] ∪ [16,32] ∪ [128,256] = K_0 ∪ K_1 ∪ K_2.
 Y2 = {0} ∪ [2,4] ∪ [16,32]: Y2⊕Y2 = [2,7] ∪ [16,63] ∪ …; complement = {0,1} ∪ [8,15] ∪ [64,127] ∪ …

Every line of the written proof checks, including the stated bounds "[8^k+8^j+2, 2·8^k+2·8^j]", "[4·8^k+4, 8·8^k+8·8^{k−1}]", "[2·8^k+2, 4·8^k+4·8^{k−1}]" and the three disjointness inequalities.

Brute force (ref_sumsets.py: Python big-int bitsets, element-by-element shift-OR, no FFT, no interval algebra): Lemma 2 exact and 0 gate violations on [0, 8^6) and on [0, 8^7) (§7). Under the WRONG rule (equal sums) the same sets give 4,4,3 / 5,5,4 / 6,6,5 violations at L = 8^4 / 8^5 / 8^6 (one per scale; consistent with PROOF.md's "7, 7, 6" at 8^7).

## 3. Lemma 3 and the "+1" in (G3) — HOLDS

Complements as stated: ℕ_0∖(Y0⊕Y0) = {0} ∪ ⋃_{k≥0} J_k; ℕ_0∖(Y1⊕Y1) = [0,4] ∪ ⋃_{k≥1} K_k; ℕ_0∖(Y2⊕Y2) = {0,1} ∪ ⋃_{k≥1} [8^k, 2·8^k−1], and q−1 in the last iff q ∈ {2} ∪ ⋃_{k≥1}[8^k+1, 2·8^k] = Y0 ∩ [2,∞).
 q = 2: 2 ∉ Y1, 2 ∈ Y0⊕Y0 ✓; 2 ∈ Y2, 2 ∉ Y1⊕Y1 ✓; 2 ∈ Y0, 1 ∉ Y2⊕Y2 ✓.
 q = 3: 3 ∉ Y1, 3 ∈ Y0⊕Y0 ✓; 3 ∈ Y2, 3 ∉ Y1⊕Y1 ✓; 3 ∉ Y0, 2 ∈ Y2⊕Y2 (0+2) ✓.
 q = 4: 4 ∈ Y1, 4 ∉ Y0⊕Y0 ✓; 4 ∈ Y2, 4 ∉ Y1⊕Y1 ✓; 4 ∉ Y0, 3 ∈ Y2⊕Y2 ✓.
 Also q = 8, 9, 16, 17 for (G3): 8 ∉ Y0 / 7 ∈ Y2⊕Y2; 9 ∈ Y0 / 8 ∉; 16 ∈ Y0 / 15 ∉; 17 ∉ Y0 / 16 ∈. All ✓.
The "+1" is right: (49u+28)+(49v+28) = 49(u+v+1)+7.

## 4. The shield and Theorem 3 — HOLDS

Own code (ref_shield.py, pure set arithmetic in ℤ/49, equal summands included; log ref_shield.log): P, B, D pairwise disjoint; (cover) (B+B) ∪ (P+B) ∪ (D+B) = ℤ/49 ∖ Q; (avoid) holds, and in particular {2b : b ∈ B} ∩ Q = ∅, so (avoid) excludes EQUAL summands too — answering the brief's question; (PP) (P+P) ∩ Q = P, ordered pairs into Q exactly (7,7), (14,14), (28,28); mixed P+P residues are 21, 35, 42 ∉ Q. max D+D = 94 (83 for distinct), < 98.

Case r ∈ Q. The six types exhaust S (every element of S is in D, a B-rail or a P-rail; D's residues are D). A sum of two DIFFERENT P-rails has residue 21, 35 or 42 ∉ Q, so cannot hit a P residue (or a B residue); B+B (any two rails, equal or not), P+B, D+B, D+P are excluded by (avoid). Hence only same-rail diagonal pairs reach P residues, and on one rail distinct elements are exactly distinct q. The three equivalences follow; with Lemma 3 (q ≥ 2) the P-rails satisfy the recurrence; B-rail integers are in S and unrepresented. The quoted sentence "two distinct elements of one rail have distinct q" is sufficient because cross-rail sums were already excluded by (PP)/(avoid).

Case r ∉ Q. Every one of the 41 residues has a cover pair; I enumerated EVERY (x, b) pair, computed u_x and c, and checked q − u_x − c ≥ 0, positivity, residue b, and other-summand ≠ e_x at q = 2, 3, 10 (table: shield_cover_pairs.txt). u_x = 1 only for x = 14 (e_14 = 63); c ∈ {0,1} always (x + b ≤ 96). No residue needs u_x + c = 2. Two residues are reachable ONLY through e_14 = 63: r = 17 (14+3) and r = 36 (14+22). So 63 ∈ A (q = 1 on the 14-rail) is load-bearing, and the proof's handling of u_x = 1 is needed, not decorative; it is correct. The distinctness argument ("equality forces x = b ∈ B, e_x = x ≤ 48, while the other summand is ≥ 49 + b") is right: when x = b, u_x = 0 and q − c ≥ 1.

## 5. Aperiodicity (Proof of Theorem 1) — HOLDS (the old sentence is FIXED IN SOURCE)

The superseded text (saved as proof_old_theorem1_paragraph.txt) said "49h would be an ultimate period of the indicator of Y0; a run of ≥ 49h consecutive non-members". That was true but unjustified as written (the derivation gives h, and 49h is then a multiple). The corrected text — "then 49h is also an ultimate period of it, and since 49(q+h)+7 = (49q+7) + 49h, h is an ultimate period of the indicator of Y0; a run of ≥ h consecutive non-members inside the periodic tail forces that tail to be identically 0" — is correct and complete: the gaps [2·8^k+1, 8^{k+1}] (6·8^k long, checked) occur arbitrarily late, a full residue system of zeros inside a periodic tail kills the tail, and I_k ⊂ Y0 for every k contradicts that. Lemma 4 is Li's Lemma 4.1 (proof read; correct).

Nit (no fix needed): "8^k consecutive members" is the I_k count; the actual first run of Y0 is {0,1,2} (3 members). Irrelevant to the argument.

## 6. Theorem 2 (rule D) — HOLDS, with F1

Lemma 2′ by hand (same interval facts with + instead of ⊕): (S0′) {0,1}+{0,1} = [0,2]; {0,1}+I′_k = [2·8^k, 4·8^k]; I′_k+I′_k = [4·8^k, 8·8^k−2]; I′_j+I′_k ⊆ [2·8^k+2, 4·8^k+4·8^{k−1}−2] (PROOF.md's upper bound "4·8^k−1+4·8^{k−1}" is one too generous, still a valid ⊆); k = 0 pieces give [0,6]. (S1′) 1+1 = 2; 1+J′_k = [8^k, 2·8^k]; J′_k+J′_k = [2·8^k−2, 4·8^k−2]; cross sums inside. (S2′) 0; K′_k ∪ [8·8^k−2, 16·8^k−2] = [4·8^k−1, 16·8^k−2]; cross sums inside. Disjointness inequalities all true.
 Small k: Y0′ = {0,…,3} ∪ [16,31] ∪ [128,255] → Y0′+Y0′ = [0,6] ∪ [16,62] ∪ [128,510], complement [7,15] ∪ [63,127] ∪ [511,1023] = J′_1 ∪ J′_2 ∪ J′_3. Y1′ = {1} ∪ [7,15] ∪ [63,127] → Y1′+Y1′ = {2} ∪ [8,30] ∪ [64,254], complement ∩ [2,∞) = [3,7] ∪ [31,63] ∪ [255,511]. Y2′ = {0} ∪ [3,7] ∪ [31,63] → Y2′+Y2′ = {0} ∪ [3,14] ∪ [31,126] ∪ …, complement {1,2} ∪ [15,30] ∪ [127,254], +1 gives {2,3} ∪ [16,31] ∪ [128,255] = Y0′ ∩ [2,∞).
Lemma 3′: all three complements as stated. Theorem 3′: Li's proof applies verbatim — it uses only e_7 = 7, e_14 = 63, e_28 = 28, all in A (0 ∈ Y0′, 1 ∈ Y1′, 0 ∈ Y2′), and Lemma 3′ for q ≥ 2.

**F1 (wrong number).** Quoted: "Theorem 2 follows as Theorem 1 did (Y0' has runs of 2·8^k members and 4·8^k non-members)." The non-member runs of Y0′ are [4·8^k, 16·8^k − 1], of length 12·8^k (k = 0: [4,15]; k = 1: [32,127]); the first member run is [0,3], length 4. The argument needs only unboundedness, so the conclusion stands; fix the number.

## 7. Independent instrument (own greedy, own closed forms) — HOLDS

ref_greedy.c, written from the problem statement before I opened any project code: for each t > max(seed), scan selected u ascending with 2u ≤ t and test t−u ∈ S; rule Q skips u = t−u. This is a direct representation search, not a bitset sieve (unlike greedy341.c). ref_closed_form.py types S and S′ in from PROOF.md's formulas (and Li's S from his paper).
External positive controls (sources not ours): rule Q from (3,7) and (2,8) reproduces van Berkel–Bosma's printed S_{3,7} (26 terms) and S_{2,8} (14 terms) exactly; rule D from {1,4,9,16,25} gives a_87…a_92 = 440,443,445,448,453,471 and a_311…a_316 = 1616,…,1647, matching the erdosproblems #341 thread comment.

Results (ref_compare.py, exit 0 = match):
 - A, rule Q vs S: MATCH on [1, 10^6] (122,468 elements); MATCH on [1, 10^7] (1,224,510 elements, last 9,999,991; ref_compare_1e7.log)
 - A, rule D vs S′: MATCH on [1, 10^6] (122,467 elements); MATCH on [1, 10^7] (1,224,509 elements, last 9,999,997); same counts as runs/gvc_{strict,equal}_1e7.log from the independent greedy341.c
 - Positive control: Li's seed, rule D vs Li's S: MATCH on [1, 10^6].
 - Negative controls (the comparison can fail): A rule Q vs S′, A rule D vs S, Li's seed rule Q vs Li's S — all MISMATCH at 10^6, first offending integer t = 126 = 49·2 + 28 in each case; A rule Q vs S′ also at 10^7 (408,127 differing integers, first 126). All 10^6 comparisons: ref_compare_1e6.log.
 - PROOF.md's "Li's seed under rule Q is eventually periodic (membership period 5,733 = 49·117": my greedy output has membership period 5,733 on [3364, 10^6] and no smaller period ≤ 20,000 there (ref_li_ruleQ_period.log); I also read ../erdos341/certify.py and its distinct-rule cutoff argument (X0 = 2N + 2q − 2) and find it sound. HOLDS.
 - Sumset/gate brute force at 8^7 = 2,097,152 (ref_sumsets_L8e7.log, own bitset code): Lemma 2 and Lemma 2′ exact on [0, 8^7), 0 gate violations for 2 ≤ q < 8^7 under each controller's own rule; under the other rule [7, 7, 6] violations for both controllers (first offending q = 4, 2, 9 for the strict controller; 6, 2, 15 for the equal one) — the same "7, 7, 6" PROOF.md reports from its FFT code.

## 8. Novelty / scope — HOLDS for every mathematical scope claim; UNSURE for one provenance sentence (F5′, §9)

 - Li (Erdos341.tex): "Equal summands are allowed in every sumset." Rule D only; no mention of a distinct-summand rule; his seed is periodic under rule Q, so Theorem 1 is not a corollary of his theorems or of his family A_p (his gate identities are false under ⊕: for his Y0 = {0} ∪ ⋃[4·8^k, 8·8^k−1], 8 = 4+4 is in Y0+Y0 but not in Y0 ⊕ Y0, yet 8 ∉ his Y1 = [1,3] ∪ ⋃[16·8^k−1, 32·8^k−1]; and his seed is periodic under rule Q — my greedy, §7). HOLDS.
 - Green: "For both variants, the following question appears to be open". No counterexample. HOLDS. "(Problem 7, Jan 2026)": the supplied excerpt carries no date — UNSURE.
 - van Berkel–Bosma. 2609.16843 §1: "initialize the first t ≥ 1 values s1 < s2 < · · · < st" and "these are greedy, strict t-sumfree sequences"; Conjecture 2 "For every g > f ≥ 1 the 2-sumfree sequence Sf,g is ultimately periodic"; Conjecture 4 (folklore) for S_{f,g,h}; the "very general conjecture that all t-sumfree sequences are ‘eventually periodic’" is under the same t-term-start definition. 2609.18522 Conjecture 1 "Every 2-sumfree sequence is eventually periodic" with the definition "initialize the first two values s0 = f ≥ 1 and s1 = g > f". So PROOF.md's sentence "conjecture periodicity for strict 2-sumfree sequences with TWO-term starts S_{f,g} (and t-term starts for t-sumfree)" is accurate to their definitions, and neither paper contains an arbitrary-seed strict counterexample (16843 §3 even notes "a similar criterion for deciding non-periodicity based on a finite initial segment is lacking"). "Theorem 1 does not touch those conjectures" — accurate in the sense that it neither proves nor refutes them (the reason given, "our seed has 21 terms", is the right one: A is not an initial segment of any S_{f,g}, since 3 = 1 + 2 ∈ A).
 - Provenance sentences: see F5′ in §9 (two of three fixed in source; the Queneau/Finch sentence still unsupported).

## 9. Anything else

**Lemma 5 (new at 12:57Z) — HOLDS.** Quoted: "Let R ⊆ {7, 56, 14, 63, 28, 77} contain at least one element of each rail". Checked step by step. r ∉ Q: (cover) gives x, b; for x ∈ P the hypothesis supplies e_x on the x-rail with u_x ≤ 1, so q − u_x − c ≥ 0 at q ≥ 2; the b-rail is full below t by the induction (B ∪ (49+B) ⊂ A_R, later B-rail integers are added); distinctness by residues as in Theorem 3. r ∈ B: only (avoid)/(PP)-excluded types or D+D ≤ 94. r ∈ P: only same-rail diagonal pairs. One presentational point: the recursion "Y1[q] = [q ∉ Y0 ⊕ Y0]" uses Y0[q] itself (the pair 0 + q when 0 ∈ Y0, i.e. 7 + (49q+7)), and "Y2[q] = [q ∉ Y1 ⊕ Y1]" likewise uses Y1[q] (14 + (49q+14) when 14 ∈ R), while "Y0[q] = [q−1 ∉ Y2 ⊕ Y2]" uses only Y2 ∩ [0, q−1]; it is well-founded because inside block q the integers are processed in the order 49q+7 < 49q+14 < 49q+28 — worth one clause. Independent integer-level evidence: for all 27 admissible R and BOTH rules, my own greedy (not a rail model) obeys B-rails-full / non-Q-residues-empty / the three rail recurrences at every 2 ≤ q < 20,408 (ref_census_classify.log). So the rule-D half that PROOF.md calls unchecked ("(no such cross-check was run under rule D)") has in fact been run, by me.

**F2 — FIXED IN SOURCE.** Old: "FAIL when any one block endpoint is moved by one" (log: three mutations). Now: "FAIL when the start of the third block on any one rail is moved down by one (three mutations; the referee's own run moved every endpoint of every block k ≤ 3 by ±1 on both controllers — every non-vacuous mutation breaks a gate on [0, 8^5))". That is what ref_sumsets_L8e5_mut.log shows (48 + 44 mutations; the one survivor, I_0 / I′_0 lower end 2 → 1, is vacuous because 1 ∈ Y0 already). At L = 8^4 three k = 3 upper-end mutations (two under rule Q, one under rule D) survive purely because their effect lies beyond L.

**F3 — FIXED IN SOURCE.** runs/control_li.log (12:55Z) has the same four lines as my their_gates_control.log (rule D: "[0, 0, 0] -> PASS"; rule Q: "(69, 117)"). Independently, my integer greedy on Li's seed under rule D equals Li's closed form to 10^6. "periodic with period 117 from q = 69" is a finite-window rail statement (classify on [69, 32768)); the all-future statement is the integer certificate (5,733 from N = 3364, ../erdos341/certify_runs.log), which I re-read and find sound.

**F4 — acknowledged in source; F4′ OPEN (wrong quotient).** The census verdict "no period ≤ 8,192 on the quotient window [16,384, 32,768)" on the PROVED seed: under rule Q the rail pattern is (Y1, Y2) = (1, 1) at q = 16,384 (the last quotient of K_4 = [8192, 16384] and the first of J_4 = [16384, 32768]) and (1, 0) at every q ∈ [16,385, 32,767]; under rule D it is Y2′ only on [16,384, 32,766] and Y1′ = Y2′ = 1 at q = 32,767 (start of J′_5, end of K′_4). The reason is structural: the controllers switch at powers of two (±1) and the census window [Q/2, Q) with Q = 2^15 has its edges ON powers of two, so each verdict rests on one edge quotient; started at 16,385 the same criterion reports period 1 under rule Q (ref_census_window.log). The reviewed text says "on A itself the verdict hinges on a single quotient (16,385, the start of J_4, under rule Q; 32,767 under rule D)" — the rule-D number is right; the rule-Q hinge is 16,384, and J_4 starts at 16,384, not 16,385 (16,385 is the first quotient where the pattern has already changed). My reproduction used q ∈ [10,204, 20,408), whose edges are NOT at powers of two (the switch at 16,384 is deep inside), and gives the same 18 / 25 and the same per-seed periods (11, 3, 27, 21, 28, 9, 53, 126, 117 under Q; 4, 2 under D) as runs/legit27_table.txt — so the counts survive a non-aligned window; the criterion is still only a (d) observation.

**F5′ — OPEN (one sentence).** Fixed: the erdosproblems read is now backed by live/341.html and live/341-claims.html (both "accessed 2026-10-14"; "Proof claims (1)", Li's only) and #342 is now described correctly (live/342.html: Ulam, "uniquely as $a_i+a_j$ for $i<j\leq n$"). Still unsupported: "Queneau 1972 and Finch 1992 concern two-term bases as described by van Berkel–Bosma (§2) and Green's references [119]". vBB §2 describes Queneau only ("He considered many explicit cases Sf,g"); Finch 1992 appears in neither vBB bibliography; the Green excerpt cites "[119, 164]" only as "references and computations showing that periodicity (if present) can be very slow to appear" and does not identify [119]. Either read the primaries or write «Queneau 1972, as described by van Berkel–Bosma §2, concerns two-term starts; Finch 1992 was not read».

**F6′ — OPEN (entry/, outside PROOF.md).** entry/headline.json tag (12:57Z): "HOSTILE REFEREE: HOLDS WITH FIXES, APPLIED"; entry/COMMIT_MSG.txt: "F1–F6 applied". F1 is not applied in the reviewed PROOF.md (line 114 still reads "Theorem 2 follows as Theorem 1 did (Y0' has runs of 2·8^k members and 4·8^k non-members)."), although entry/body.html (12:57Z) tells readers it was ("HOLDS WITH FIXES, all applied — the fixes were a wrong run length") and points them to "the bundle's PROOF.md" for the rule-D identities; body.html also repeats F4′ ("16,385, where J 4 starts" — rendered from J<sub>4</sub>). F4′ and F5′ are new. COMMIT_MSG also says "its own greedy matches to 10^6" — true when written; it is now 10^7 (§7). History: the 12:38Z tag already said "HOSTILE REFEREE HOLDS" before any report existed, and the 12:38Z census wording ("18 of the 27 seeds of this shape never settle", "18 show no period at all"; excerpts in entry_old_excerpts_1238Z.txt) overstated a (d) observation; both were changed at 12:55Z.

**Numbers in the reviewed PROOF.md checked against logs.** 5,733 = 49·117 and CERTIFIED (../erdos341/certify_runs.log); 7, 7, 6 and 2378 = 41 × 58 cover checks (runs/verify_closed_form.log); 2^17 both rules (same log) and 2^20 rule Q (runs/ic27_runs_Q1048576.txt; its run lists equal my closed-form runs exactly, ref_check_ic27_runs.log); 10^7 element-by-element (runs/gvc_*_1e7.log); 27 / 18 / 25 / 117 / 10^6 (runs/legit27*.{log,txt}); "0 mismatches to 32,768" and "(69, 117)" (runs/control_li.log); "7p − 20 ≥ 106" (Li Thm 5.1, p ≥ 18). The census caveat's "[10,204, 20,408), P ≤ 2,550" and "same 18 and 25" are mine (ref_census_classify.log). No number without a source remains except F4′'s wrong quotient.

## Files (all in this directory)
 - ref_greedy.c / ref_greedy — own greedy (direct representation search, not a sieve), both rules; written before reading any project code.
 - ref_closed_form.py — S, S′ and Li's S typed in from the printed formulas; closed_{Q,D,LI}_1e6.txt, closed_{Q,D}_1e7.txt.
 - greedy_A_rule{Q,D}_1e6.{txt,log}, greedy_A_rule{Q,D}_1e7.{txt,log}, greedy_Li_rule{Q,D}_1e6.{txt,log}.
 - ref_compare.py (first offending integer; exit 0 match / 1 mismatch / 2 cannot see), ref_compare_1e6.log, ref_compare_1e7.log.
 - ref_shield.py, ref_shield.log, shield_cover_pairs.txt — shield + every cover pair with u_x, c.
 - ref_sumsets.py, ref_sumsets_L8e4_mut.log, ref_sumsets_L8e5_mut.log, ref_sumsets_L8e6.log, ref_sumsets_L8e7.log — brute-force Lemma 2/2′, gates, wrong-rule and endpoint-mutation controls.
 - ref_check_ic27_runs.log — project's 2^20 rail runs vs my closed form.
 - ref_li_ruleQ_period.py/.log — Li's seed under rule Q, membership period 5,733.
 - ref_census_run.sh, ref_census_classify.py/.log — independent 27-seed census, both rules (greedy outputs left in /tmp/ref341/census/, 54 × ~1 MB).
 - ref_census_window.py/.log — census window criterion on the proved seed.
 - their_gates_control.log — output of the project's gates.py --control (run read-only before runs/control_li.log existed).
 - PROOF_reviewed_snapshot.md (the version reviewed), proof_old_theorem1_paragraph.txt, proof_old_excerpts_v0.txt, entry_old_excerpts_1238Z.txt — superseded text I quote.
 - ref_quote_check.py, ref_quote_check.log — every double-quoted string in this report found verbatim in its source (missing: 0); «guillemets» mark my suggested wording.
