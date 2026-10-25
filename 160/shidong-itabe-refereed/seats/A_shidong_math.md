# Seat A: Shi–Dong, arXiv:2607.20752v2, §§2–5 (the construction and the Erdős #160 reduction)

Read from: `/tmp/erdos160/papers/shidong.txt`, plus pages 2–6 of the PDF rendered to PNG (`A_render/`) so the formulas could be read exactly. DTZ was read from `/tmp/erdos160/papers/hunter.txt` (Def 3.1, Lemma 3.2, Defs 7.8/7.10, Lemmas 7.9/7.11). All scripts are in `/tmp/erdos160/seats/A_work/`. Every run used `nice -n 19` and took under 40 s on one core.

## VERDICT: HOLDS AS READ

Theorem 1.1, Corollary 1.2, Corollary 4.3 and Corollary 1.3 (h(N) ≤ N^{1/4+o(1)}) all follow from what is written in §§2–5, once the routine steps below are filled in. I found **no FATAL objection**. There are **two minor GAPs**: places where the written proof applies a lemma outside its stated hypotheses, or gives a reason that is false in general. In both, the conclusion is true. Each closes in one line, and I checked each exhaustively on small cases. Everything else is **EXPOSITION**.

---

## Objections

**1. GAP (minor; closes in one line). Lemma 2.2's proof uses Lemma 2.1 outside its hypothesis, and Lemma 2.1's `e_i` is not the true carry.**
> "Iterating Lemma 2.1 from digit 0 to L − 2 shows inductively that the k − 1 carries to the next digit are equal at every digit position"

Write δ_j for the digits of d and c_{j−1} for the incoming carry. At digit j the effective increment is δ_j + c_{j−1} ∈ {0, …, p}. Lemma 2.1 is stated only for s ∈ {0, …, p−1}, and its "carry" is e_i = 1{x_{i+1} < x_i}. When δ_j = p−1 and c_{j−1} = 1, the increment is p. Then the digit stays fixed (step 0 mod p), so Lemma 2.1 would report e_i = 0, while the true carry is 1 at every step. The conclusion still holds, because in that case the true carry is identically 1 and therefore constant. But the proof as written never says this. It also never says that the step at digit j, (δ_j + c_{j−1}) mod p, is constant across i *because* c_{j−1} is constant. That is the actual induction step.

Fix: one sentence ("if δ_j + c_{j−1} = p the digit is constant and every carry is 1; otherwise apply Lemma 2.1 with s = δ_j + c_{j−1}, where e_i is the true carry").

Checked (`edge22.py`, k = 4, p = 13, L = 3, all (a, d)): 8,788 τ-symmetric APs hit this case, and in none of them is the true carry out of digits 0..L−2 non-constant. My first version of this check reported 5,824 "non-constant" cases. Those were all the top-digit carry, which is correctly discarded mod p^L. The paper rightly puts no τ-condition on digit L−1.

**2. GAP (minor; true conclusion, wrong stated reason). Lemma 5.3's carry step at the boundary x = M/2.**
> "A carry in the first or third addition would place the corresponding pair on opposite sides of M/2, so τ(y0) ≠ τ(y1) or τ(y2) ≠ τ(y3)."

Here τ(x) = ⌊log₂(M − x)⌋. Its classes are {0}, [1, M/2], (M/2, 3M/4], …. So x = M/2 shares its τ-value (log₂M − 1) with 1, …, M/2 − 1, which lie on the other side of M/2. "Opposite sides of M/2 ⇒ different τ" is therefore false in general.

The claim survives because of a different fact. If s ≤ M/2 and the first addition carries, then y0 ≥ M − s ≥ M/2 and y1 = y0 + s − M ≤ s − 1. The only cross-boundary pair with equal τ needs y0 = M/2. That forces s = M/2 and y1 = 0, and τ(0) = log₂M ≠ τ(M/2). The proof should say this.

Checked (`lem53.py`): for M = 2, 4, …, 512, every (y0, s) gives 0 carry-consistency violations, and the boundary case (y0 = M/2, s = M/2, carry) occurs exactly once per M. Negative control (`lem53ctl.py`): replacing τ by ⌊2x/M⌋ (just two halves) produces violations (6/22/86 at M = 8/16/32), so the test is able to fail.

The same digit-increment-equals-M issue as Objection 1 is also present here, unremarked: δ_j + c = M means constant digit and every carry 1.

**3. EXPOSITION. §5 promises a proof but gives none for Lemmas 5.1 and 5.2, and the cited statements are not the stated lemmas.**
> "Hunter [Hun25] observed that the remaining patterns can be eliminated … We give a proof of this observation."

Lemma 5.1 and Lemma 5.2 are only citations.

- **DTZ Lemma 3.2** colours Z/NZ and forbids monochromatic *k-patterns*: triples (n1, n2, n3), not all equal, with a·n1 + b·n2 = (a+b)·n3, where a, b ≥ 1 and a + b ≤ k − 1 (DTZ Def 3.1, hunter.txt l.305–306). I did the translation the paper omits. Take k = 4, so a + b ≤ 3, and a 4-AP x, x+d, x+2d, x+3d:
  - {0,1,2}: (x, x+2d, x+d), with (a, b) = (1, 1). Covers AAAB and AAAA.
  - {0,1,3}: (x, x+3d, x+d), with (a, b) = (2, 1), since 2x + (x+3d) = 3(x+d). Covers AABA.
  - {0,2,3}: (x, x+3d, x+2d), with (a, b) = (1, 2), since x + 2(x+3d) = 3(x+2d). Covers ABAA.
  - {1,2,3}: (x+d, x+3d, x+2d), with (a, b) = (1, 1). Covers BAAA.

  Integer relations hold mod N, and distinct elements of [N] stay distinct mod N, so the Z/NZ colouring restricts to [N]. The colour count is e^{C√log N} = N^{o(1)}. **Lemma 5.1 holds.**
- **DTZ Lemma 7.11** colours Z/N_r Z only for one special N_r = Θ(r^{C log r}) per r, not every N. Take a = (1,2,3,4). An a-ABAB pattern is φ(n+d) = φ(n+3d) and φ(n+2d) = φ(n+4d), which is exactly our ABAB, including AAAA. Given N, pick the least r with N_r ≥ N. Then r = e^{O(√log N)} = N^{o(1)}. Restrict to [N]: a nontrivial 4-AP in [N] has 0 < d < N ≤ N_r, so it stays nontrivial mod N_r. **Lemma 5.2 holds.**

  I also re-checked DTZ's proof for this a: Lemma 7.9 with sequence length a4 − a1 + 1 = 4 ≤ a and M coprime to 24, then the axis-of-symmetry step.

None of this is hard, but the paper should write it, since it says it gives a proof.

**4. EXPOSITION. The proof of Corollary 1.3 omits the case analysis.**
> "Taking the product of the coloring from Corollary 4.3 with k = 4 and the colorings in Lemmas 5.1, 5.2, and 5.3 uses N^{1/4+o(1)} colors."

This sentence only counts colours. What is missing is why the product works. If a 4-AP gets ≤ 2 product colours, its colour partition P is one of the 8 partitions of {0,1,2,3} into at most 2 blocks: AAAA, AAAB, AABA, ABAA, BAAA, AABB, ABAB, ABBA. Every factor's pattern on that AP is a *coarsening* of P, so each factor inherits P's equalities. The four factors forbid these equality sets, *including* their degenerate coarsenings:

| Factor | Forbidden equalities | Kills |
|---|---|---|
| Cor 4.3 | 0~3 and 1~2 | ABBA |
| Lemma 5.1 | a monochromatic 3-subset | AAAA and the four 3+1 patterns |
| Lemma 5.2 | 0~2 and 1~3 | ABAB |
| Lemma 5.3 | 0~1 and 2~3 | AABB |

All 8 are killed. I checked that each lemma's proof really excludes the degenerate coarsening too. Theorem 1.1 forbids "symmetrically coloured", which includes AAAA. Lemma 5.3's proof uses only the two equalities. DTZ 7.11's ABAB definition is equality-based. So the argument is complete once stated.

**5. EXPOSITION. §3 defines P_t by a formula of the wrong formal degree, and the citation does not state the property used.**
> "N(z) := z^{1+p+…+p^{t−1}} … the fact that P_t : F_p^t → F_p is a homogeneous polynomial of degree t with no nontrivial zero, is standard … see [LN96, Corollary 2.11; Theorem 2.28]."

Read formally in x_0, …, x_{t−1}, the expression z^{(p^t−1)/(p−1)} has degree (p^t−1)/(p−1). The degree-t homogeneous form that Lemma 4.1 needs is the product of conjugates, ∏_{m<t} (Σ_j x_j α^{j p^m}). Lemma 4.1 uses two facts about it: P_r(u + t v) has degree ≤ r in t, and its t^r coefficient is P_r(v). These agree with the paper's formula as functions on F_p^t because x_j^{p^m} = x_j. Since every degree involved is < p, function-level and formal-level reasoning coincide.

The definition should still be the product of conjugate linear forms. From memory (the book is not on disk, so this is unchecked): LN96 Corollary 2.11 is the existence of irreducible polynomials of every degree, and Theorem 2.28 lists multiplicativity, surjectivity and N(a) = a^m. Homogeneity of degree t follows from those, but the *polynomial* structure comes from Definition 2.27 (product of conjugates). Still a citation-precision point only.

Checked (`norms.py`) for (p, t) ∈ {7, 11, 13} × {3, 5} and (7, 4): no nontrivial zero (exhaustive), homogeneity P(cx) = c^t P(x) (exhaustive), and, on 3,000 random lines u + s v, that s ↦ P(u + s v) interpolates to degree ≤ t with s^t coefficient P(v): 0 failures. Control: the norm composed with coordinatewise x^5 fails this test 292/300 times, so the test can fail.

**6. EXPOSITION. Lemma 2.1: three unproved one-liners.** All three are true; I checked them exhaustively (`lem21.py`).
- (a) > "If s < (k−2)p/(k−1), then, since τ(x_{k/2−1}) = τ(x_{k/2}), necessarily s < p/(k−1)."

  Unproved. The reason: an interval has diameter < p/(k−1), so s ∈ [0, p/(k−1)) ∪ (p − p/(k−1), p).
- (b) > "with s′ = p − s < p/(k−1)"

  The strict inequality needs s ≠ (k−2)p/(k−1). That holds because gcd(k−1, (k−2)p) = 1 for p > k, so the boundary value is never an integer. (Or argue as in (a) that s > (k−2)p/(k−1) strictly.) The edge s = 0 lands in the first branch and is harmless: all carries are 0.
- (c) > "By simple induction we have that all of these points lie in the same interval i, and e0 = … = 0."

  The step from "same interval" to "no carry" needs: a wrap would mean |x_{j+1} − x_j| = p − s > (k−2)p/(k−1) ≥ p/(k−1) > diameter.

On the referee's specific question: the "interval i or i−1 / i or i+1, indices mod k−1" step needs i−1 ≢ i+1 mod (k−1), i.e. k−1 ≥ 3. This holds since k is even and ≥ 4. It is exactly what fails for an odd k = 3 or a 2-interval τ. My control with τ replaced by 2 intervals (k = 4, p = 11 and k = 6, p = 31) produces carry violations (20 and 144). The wrap from interval k−2 to interval 0 is handled correctly by the mod-(k−1) reading.

**7. EXPOSITION. Corollary 4.3: injectivity of [N] → Z/p^{k²/4}Z is left implicit.**
> "Restricting the coloring from Theorem 1.1 to [N] ⊆ Z/p^{k²/4}Z gives the result."

This needs p^{k²/4} > N, which follows from p ≥ ⌊N^{4/k²}⌋ + 1 > N^{4/k²}. That one fact gives injectivity, and also that a nontrivial integer AP in [N] (0 < |d| < N) stays nontrivial mod p^{k²/4}. Bertrand applies because N ≥ k^{k²/4} ⇒ ⌊N^{4/k²}⌋ ≥ k ≥ 2. Then p > ⌊N^{4/k²}⌋ ≥ k, so p > k. For N < k^{k²/4}, N colours (O_k(1)) suffice, so "O_k(N^{4/k²}) for every N" holds. All correct, just not written down.

**8. EXPOSITION. Lemma 5.3 leaves three things implicit.**
- The orientation d < 0 is never mentioned. It is harmless: reversing a 4-AP maps AABB to BBAA, the same equalities.
- That the digit vectors form an *integer* AP u + i v with v ∈ Z^m: once carries are constant, v_j = δ_j + c_{j−1} − M c_j.
- That n_3 ≤ N < M^m, so there is no top carry.

The quadratic step is right as written. f(0) = f(1) and f(2) = f(3) give 2⟨u,v⟩ + ‖v‖² = 0 and 2⟨u,v⟩ + 5‖v‖² = 0, so ‖v‖² = 0. Note τ takes log₂M + 1 values, not log₂M, which does not affect N^{o(1)}.

**9. EXPOSITION (not load-bearing). Remark 4.2 is an unproved heuristic.**
> "In view of the Chevalley–Warning theorem, one should not expect to gain more than O_k(1) dimensions over k²/4 by using another polynomial of degree O_k(1) within the same framework."

No argument is given. There is a precise version for the *layered* design: by Chevalley–Warning, an anisotropic form of degree r over F_p has ≤ r variables. So with odd layer degrees ≤ k−1, Σ_{r odd} r = k²/4 is exactly the maximum. The broader claim about "another polynomial" is unsubstantiated. It is harmless, but should be stated as a heuristic or proved.

---

## What I verified and how

1. **Lemma 2.1, every case, by hand, then exhaustively.** Both branches; the reversal identity e′_i = 1 − e_{k−2−i} (valid because s ≠ 0 there); the k−1 ≥ 3 requirement; the wrap at interval k−2 → 0; the edges s = 0 and s = (k−2)p/(k−1) (the latter impossible). `lem21.py`: k ∈ {4,6,8,10,12}, all primes k < p < 220, all (x0, s). 119,277 τ-symmetric digit APs (97,164 with nonzero step). 0 carry violations, 0 failures of the "s < p/(k−1) or s > (k−2)p/(k−1)" step, 0 failures of "all points in one interval". The 2-interval controls fire.
2. **Lemma 2.2: top digit, constant step, h ≠ 0 ⇔ d ≠ 0.**
   - The top digit needs no τ-condition: its step is (δ_{L−1} + c_{L−2}) mod p, and the carry out is discarded mod p^L. The step at digit j is constant once c_{j−1} is constant. If h = 0, then x(n0) = x(n1), so n0 = n1, so d = 0.
   - `lem22.c` is exhaustive over all (a, d) ∈ (Z/p^L Z)² for (k, p, L) = (4, 11, 3), (4, 13, 3), (6, 29, 2), (8, 53, 2). The parameters were chosen so that some τ-symmetric APs have a nonzero step *below the top digit*; for k = 6 that needs p > 25, since p = 7 would be degenerate. Results: 27,225 / 74,529 / 31,117 / 171,349 τ-symmetric APs, of which 12,584 / 45,968 / 6,728 / 22,472 are non-degenerate. 0 non-AP digit vectors; 0 failures of h = 0 ⇔ d = 0.
   - Control (drop the τ-condition on digit 0): 350,168 and 565,152 violations.
   - Edge case δ_j + c = p: see Objection 1.
3. **§3 norm forms.** `norms.py`, see Objection 5. Does the construction need odd t? Yes. Lemma 4.1 kills the t^r coefficient only for odd r, because g(t+a) is even. Control (`lem41.c`, k = 6, p = 7): replace the top degree-5 layer by the (anisotropic) degree-4 norm of F_{7^4}. Then 5,762,400 of the 5,764,800 nonzero h admit a Q-symmetric 6-AP. Oddness is load-bearing, not cosmetic.
4. **Lemma 4.1 by hand.**
   - deg g ≤ k−1.
   - The k roots {j − a : 0 ≤ j ≤ k−1} of g(a+t) − g(a−t) are exactly the pairs (i−1, k−i), since 2a = k−1. They are distinct because p > k−1, and 2 is invertible because p is odd.
   - In the descending induction, layers s > r contribute P_s(u^{(s)}) (constant; the shift by a is harmless). Layers s < r have t-degree ≤ s < r. So the t^r coefficient of g(t+a) is P_r(v^{(r)}).

   **Exhaustively**, via additive per-layer histograms of (G(0) − G(k−1), …):
   - `lem41.c`: **k = 6, p = 7, all 7^18 pairs (y0, h) ∈ F_7^9 × F_7^9.** h = 0 gives 7^9 solutions, as it must. **Nonzero h with a Q-symmetric 6-AP: 0.**
   - `lem41k4.py`: **k = 4, p ∈ {5, 7, 11, 13}, all (y0, h) ∈ (F_p^4)².** 0 nonzero h. The norm here is computed decorrelated, as the determinant of multiplication-by-z.
   - Controls fire: even-degree top layer (above); isotropic degree-5 form w0·P4(w1..w4), with 5,762,442 bad h; isotropic x1³ for k = 4, with 48 bad h.
5. **Proof of Theorem 1.1, the colour count, Corollaries 1.2 and 4.3.**
   - The colour symmetry gives exactly the hypotheses of Lemma 2.2 (τ on digits 0..L−2) and of Lemma 4.1 (Q on all L digits). The palette is (k−1)^{L−1}·p; for k = 4 that is 27p.
   - Corollary 4.3: see Objection 7.
   - Our earlier brute-force checks (`~/MathDyad/erdos160/check_shidong_k4.{py,c}`; log `c_p13.log`) cover the full k = 4 colouring of Z/p^4Z for p = 5, 7, 11, 13: 0 symmetric 4-APs, palette exactly 27p at p = 13, three controls fire. I did not re-run them.
6. **§5.**
   - Lemma 5.1: the (a, b) table is in Objection 3.
   - Lemma 5.2: from DTZ 7.11 to [N] (Objection 3). Numerically (`dtz711.c`), DTZ's ψ = (Σ digit², digits mod 24) on Z/M^m Z with gcd(M, 24) = 1 has 0 ABAB 4-APs for (M, m) = (5,4), (7,3), (7,4), (11,3), (25,2), (25,3), (29,2), (31,2). Control: dropping χ, i.e. Ψ alone, gives 82 / 12 / 14 ABAB at (7,3) / (25,2) / (29,2). The opposite control (χ alone) never fired at these sizes because χ is near-injective, so it carries no evidence.
   - Lemma 5.3: carries (Objection 2); full colouring ψ_N on [N] for N = 300, 1000, 2500 (palettes 202, 718, 1303) has 0 AABB-type 4-APs (AABB including AAAA). Controls fire: drop τ, or drop Ψ.
   - Corollary 1.3: case analysis in Objection 4.

## Not checked / instrument caveats

- **The end-to-end product test (`cor13.py`) is VACUOUS and is not counted as evidence.** At N = 1500 the product colouring is injective (palette = 1500 = N), so "0 bad 4-APs" and "0 after dropping any factor" carry no information. The N^{o(1)} factors only compress at N far beyond brute force. Evidence for Corollary 1.3 is the per-factor tests above plus the 8-partition case analysis.
- I did not re-prove DTZ Lemma 3.2. DTZ only sketches it via Ruzsa [9, Thm 2.3] and random translates. The [N] form needed here (Behrend-type sets for a·x + b·y = (a+b)·z with a + b ≤ 3, then translates) is classical.
- LN96 numbering is from memory; the book is not on disk.
- Hunter's forum comment [Hun25] was not fetched. It is attribution only and not load-bearing.
- Corollaries 1.4 and 1.5 are outside this seat. I only confirmed the Corollary 1.5 limit algebraically: k − 1 + k²/(4(k−1)) = k + (k−2)²/(4(k−1)).
- No exhaustive test exists for k ≥ 8 (P_7 histograms are out of reach), or for the full k = 6 colouring at non-degenerate p (≥ 29, so Z/29^9Z). For k = 6 the evidence is Lemma 2.2 exhaustive at p = 29 (L = 2) plus Lemma 4.1 exhaustive at p = 7. Both lemmas are p-uniform, and the theorem is their composition.
