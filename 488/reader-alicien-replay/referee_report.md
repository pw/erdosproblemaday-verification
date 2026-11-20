# #488 reader submission dv8gfk (Alicien B.) — hostile referee report

Seat: separately briefed AI referee (Claude Opus 5.5, tools, no Lean builds), 20 Nov 2026. Brief: refute; quote the
sentence objected to; grade FATAL / GAP / FIX / EXPOSITION. erdosproblems.com not read (site excludes AI agents).
Scratch scripts: `ref_*.py` (copied beside this file).

Recommendation: publish as **correct, not novel**.

## Verdicts
- **Theorem 1 (counterexample): HOLDS AS READ.** No mathematical error. As a claim of a new proof it fails: it is Gessel's
  proof, uncited.
- **Theorem 2 (|A| ≤ 2): HOLDS AS READ.** Not new: earlier proofs and a Lean proof of the two-element case exist, all uncited.
- **Lean statements: correct.** `not_erdos_488` is token for token "¬(FC body)". `erdos_488_card_le_two` is the FC body
  with `A.card ≤ 2 →` inserted; its hypotheses can be met (A = {2}), so it is not vacuous. Separate build at 96b5360 exited
  0; `#print axioms` lists only propext, Classical.choice, Quot.sound for both theorems.

## Objections
1. **FATAL (novelty and priority, not correctness).** Paper: "A counterexample was recently reported by Jiang et al." and
   "What we add is a different proof, which is short and elementary". Gessel's proof note and gist (5 Sep 2026,
   Jig-verified) already contain this argument: the same 54 primes / 53 odd primes with Q their product; the same box
   bound on odd smooth counts, (8j+1)^53; the same finite pigeonhole over 256-fold scales (k < 4096, factor 3/2,
   2^4096·32769^53 < 3^4096); the same dyadic lift c_d ∈ (T, 2T]; the same injection d, r ↦ c_d·r with r coprime to Q;
   the same kind of exact constant comparison (3Q < 16φ(Q)); a Lean adapter whose proposition is token-identical to
   today's FC body. Gessel's argument is just as elementary. Lemmas 5–6 also copy the structure of Jiang's write-up
   Lemmas 1 and 3 (same O(y), a_w, T_w notation). So "different proof" is false, and "a public Lean 4 formalization …
   against an independently maintained formal statement" is not a first either.
2. **GAP (novelty of Theorem 2).** "What we add is … a positive result for |A| ≤ 2." Uncited: Chojecki (ulam.ai,
   20 Mar 2026; primitive sets up to three elements — the world seat read the PDF: Cor. 4.7); xccElephant's Lean
   `erdos_488_pair`; candidate proofs up to four (dicnunz), up to seven (Luew2), pairwise-coprime four (Asaria, July 2026).
3. **EXPOSITION.** "Moreover A is primitive" adds nothing: replacing any A by its divisibility-minimal elements leaves B
   unchanged and does not raise max A. Jiang's set is already an antichain, and his write-up says so.
4. **EXPOSITION.** "no real analysis or Mertens-type estimate is needed" is framed as a contrast with Jiang. Jiang's
   Mertens-type lemma (c > 1/768) is an elementary telescoping product, and Gessel had already avoided both. README and
   formalization.yaml call Jiang's bounds "analytic Mertens", which is wrong.
5. **EXPOSITION.** "Our counterexample has a ratio only slightly above 2." The paper's own constants certify > 2.3787;
   Gessel's certify > 2.141.
6. **FIX (optional).** m = (2n)!·Q is needlessly enormous; u over [1, Q] coprime to Q with m = 2xQ gives |T_w| ≥ φ(Q) and
   the same bound (Gessel's choice m = 2TQ).
7. **EXPOSITION.** Remark 8: "In the pair case … B(n)/n exceeds … half of the larger quantity 1/a+1/b." False for
   non-primitive pairs: A = {4,8}, n = 11 gives 2/11 < 3/16; A = {3,6}, n = 8 gives equality. True for primitive pairs
   (checked up to 400). Should say "primitive pair".
8. **EXPOSITION.** "against the statement … in … formal-conjectures": README says "definitionally identical (rfl)", yaml
   "Verified … (by rfl) against upstream". The repo never imports Formal Conjectures; it compiles a pasted copy under four
   Mathlib imports, and no rfl artifact exists. The copy is token-identical; possible elaboration differences
   (decidability instance for `filter (· ∈ B)`, ℕ → WithBot ℕ coercion) do not change meaning.
9. **EXPOSITION (minor).** README "sorry-0" badge beside the two intended sorrys in Challenge.lean; yaml gives the 1961
   Erdős article the id erdosproblems.com/488; yaml lists Jiang as the source adapted and omits Gessel's adapter; Toledo's
   Palomar repo for Gessel's proof (14 Nov) has the same repo name `erdos-488-lean`.

## Theorem 1 steps checked
Lemma 3 holds. Lemma 4: chained inequalities plus 1 ∈ O(2^8) give 6^3500 ≤ 5^3500·28009^53, a contradiction. x = 2^(8j) ≥
256 is in A, max A < 2x ≤ n, A ⊂ [x,2x) excludes 0, 1. Lemma 5: t = aq with q ≤ 256, t smooth in [x, 256x]; for each odd
core w, e in an interval of length 8, so ≤ 9 values. Lemma 6: a_w unique, a_w < 2n so a_w·Q | m, |T_w| exact as
Q | m/a_w, T_w disjoint because w is the largest odd smooth divisor of a_w·u. Strictness: Lemma 6 already strict
(1 ∈ O(x)); final step needs only 216Q ≤ 1280φ(Q), which holds strictly. The Lean follows the paper lemma by lemma
(`oddSmooth_pow_two_le`, `exists_good_scale`, `upper_bound_at_n`, `lower_bound_at_m`, `not_erdos_488_proof`).

## Theorem 2 steps checked
(2), single generator, a | b reduction, u ≥ 2, v ≥ 3, w ≥ 4, B(y+L) = B(y)+w; cases (i), (ii) (r < a and a ≤ r < b),
(iii) all hold; CardLeTwo.lean follows the same case split.

## Numbers computed (integer arithmetic)
| Check | Result |
|---|---|
| Primes ≤ 256 | 54 (53 odd, largest 251); Lean's `oddPrimes256` is that list; Q has 101 digits |
| 5^3500·28009^53 < 6^3500 | True; log margin 95.39 nats (638.13 vs 542.74); smallest number of scales that works: 2925 |
| 216Q vs 1280φ(Q) | strictly smaller; φ(Q)/Q = 0.2007066 vs 0.16875; certified ratio ≥ 2.37874 |
| Gessel's constants | 3Q < 16φ and 2^4096·32769^53 < 3^4096 true; certified ratio ≥ 2.1409 |
| Bound on n | 8·3501 = 28008, n ≤ 2^28008 |

Small analogues (`ref_small_analogue.py`, smoothness bound 2^h, block length h): h = 2, j = 1..5 and h = 3, j = 1 exact —
Lemma 5 bound, T_w disjointness, exact |T_w|, Lemma 6, Σ|T_w| ≤ B(m) all hold; ratios ~0.94–1.07 as expected.
Theorem 2 brute force (`ref_thm2_brute.py`): all 79,800 sets {a}, {a,b}, 2 ≤ a < b ≤ 400, n ∈ [max A, max A + 3·lcm],
sup over m > n exact by periodicity: largest ratio 799/400 = 1.9975 at A = {400}, n = 799; none reaches 2. Remark 8 for
primitive pairs: no failures; tightest 1.0025 at {399,400}, n = 797. Pair extremal formula (2M−3)²/(2(M−1)²) at
{M−1, M} for 4 ≤ M ≤ 35; {2,3} gives 49/40 at n = 7; triples 9 ≤ M ≤ 18 maximal at {M−2, M−1, M}.
Statement diff (`ref_stmt_diff.py`): comments stripped, 92 tokens, identical. Kernel-bypass scan: none of axiom, admit,
native_decide, implemented_by, extern, unsafe, opaque, macro/elab/syntax, #eval/run_cmd, ofReduceBool, skipKernelTC.
Present: kernel `decide`, `set_option maxRecDepth 20000`, `irreducible_def`, two intended sorrys in Challenge.lean
(Solution does not import it). Build warnings: deprecated `dif_pos` only.

## Gessel vs Alicien
| | Gessel (5 Sep 2026) | Alicien (19 Nov 2026) |
|---|---|---|
| Set A | smooth in (T, 256T]; not primitive | smooth in [x, 2x); primitive |
| n | 256T | 256x |
| m | 2TQ | (2n)!·Q |
| Upper count | ≤ 8·H(k+1) | ≤ 9·|O(n)| |
| Scale step | 3/2 over 4096 scales | 6/5 over 3500 scales |
| Constant | 3Q < 16φ(Q) | 216Q < 1280φ(Q) |
| Certified ratio | > 2.14 | > 2.38 |
