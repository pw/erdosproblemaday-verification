HOLDS AS READ

Seat R, hostile check of the site's own claims for #416 (2026-10-21). None of the three claims is false. There are 9 findings below: one is a must-fix if the published wording makes a novelty claim (#5), and the rest are citation, wording or reproducibility fixes. Everything was run in /tmp/oaimath/024/seats/R_work/. The 10^9 jobs were not rerun and no Lean was built.

## Claim 1 (label (b)): A(1; s) is not constant, and sup A / inf A ≥ λ/γ

**What I checked**

- I re-derived every step from the printed Theorem 2.1 and from (2.3)–(2.4).
- The jump goes the way the claim says. With x = y_M/√c and x' = c·x:
  - G_M(B')/G_{M−1}(B) = B'^M/(B^{M−1}·M·g_M) exactly, from (2.4).
  - (B'/B)^M → 1, because B' − B ~ log c / log x and M = O(log B).
  - g_M = γρ^{−M}(1+o(1)), from paper (3.5).
  - B ρ^M/(Mγ) → λ/γ. The paper's own (3.2) gives the same: α/α_θ = 1 + O(log m/m), with α_0 = λ.
  - So A(θ(x'))/A(θ(x)) → γ/λ < 1: the coefficient drops by about 1.89 when m increments.
- Independent cross-check from the definition (2.8). Reindexing the tail h → h+1 sends the s→1⁻ thresholds (γρ/λ)ρ^h D to the s=0 thresholds (γ/λ)ρ^{h+1}D. The prefactors then give A_H(1;1⁻)/A_{H+1}(1;0) = λ/γ, up to window and P-cutoff edge effects.
  - The direction agrees with the claim. There is no internal inconsistency with OpenAI's formula.
- Neither measurability nor continuity is used. The argument needs only 0 < c₋ ≤ A ≤ c₊ (printed Thm 2.1, Lean conjunct 2).
- The Lean definitions match the argument exactly:
  - `m x = ⌊psi (B x)⌋₊`, and psi ≥ 1/λ > 0, so Nat.floor equals floor.
  - `theta = psi − m`.
  - `G x j = B^j/(j!·∏_{i∈Icc 1 j} g i)`.
  - `mainTerm` uses `A (fun _ => 1) (theta x)`.
- Constants, recomputed independently with mpmath nsum and findroot (c1/consts.py):
  - ρ = 0.54259858609847102196
  - λ = 0.61138548455047034571
  - γ = 0.32345753419138067657
  - λ/γ = 1.8901568828158160714
  - These reproduce the paper's C0 = 0.8178146 and D0 = 2.1769687, so λ/γ is consistent with the paper's normalisation.
- I confirmed the cited wrap values from wrap.out: 2.018 (m=100), 1.910 (m=1000), 1.901 (m=2000). Direct evaluation at M = 50 gives 2.1084 and at M = 300 gives 1.9442.

**Findings**

1. **Wrong citation for g_M.** Location: the brief's argument, "g_M = γρ^{−M}(1+o(1)) = γe^{λM}(1+o(1)) (Ford's (3.5))". Ford's (3.5) (arXiv v2, p. 13) is the vector definition "v_i = −e_i + Σ a_j e_{i+j}". The estimate is Ford's **Lemma 3.7**: "|g_i − λϱ^{−i}| ⩽ 5", where Ford's λ is our γ. It is also the **paper's** printed (3.5): "g_j = γρ^{−j} + O(1)". Severity: **typo**. Cite "paper (3.5), from Ford Lemma 3.7".

2. **Variable mix-up in one sentence.** "At ψ(B) = M: B = e^{λM}·log B" holds at B(y_M), but the ratio being evaluated uses B = B(x) = B(y_M) + O(1/log x). The effect is harmless (a factor 1+o(1)), but the sentence as written uses two different B's. Severity: **exposition**.

3. **Use "sup/inf" (or "not constant"), never "A(1⁻) ≠ A(0)".** One-sided limits of A are not known to exist. θ(x') → 0⁺ never equals 0, so the argument says nothing about the single point A(0). A sharper statement that is true: take x' = y_M exactly, so θ = 0 exactly. Then (λ/γ)·A(1;0) is a limit point of A(1;s) as s → 1⁻. Severity: **exposition**. This is a strengthening, not an error.

4. **Novelty is thin.** The statement is not in the paper. The paper deliberately leaves the question open:
   - §2.1, after Thm 2.1: "No regularity of s ↦ A(1; s) is asserted or needed."
   - Proof of Cor 6.2 (printed p. 29): "Neither continuity of the phase coefficient nor matching values at the ends of the phase interval is required."
   - As shown above, the ratio λ/γ can also be read off the prefactor (γ/α_s)^H ρ^{H(H−1)/2} in (2.8).

   Present it as "a five-line consequence of Thm 2.1 + Cor 6.2 + (3.5), not stated in the paper", not as a result. It is **not observable numerically**:
   - m(x) = 1 for every x < 10^212.69. ψ(B) = 2 first occurs at B = 6.1939, i.e. log x = 489.7.
   - θ(10^9) = 0.645.
   - So no census number bears on it. Any sentence tying the V(2x)/V(x) table to the phase jump would be unjustified.

   Severity: **exposition / provenance**.

## Claim 2 (label (d)): the census

**What I checked and reproduced**

- I wrote an independent brute force (bf/bf.py). It computes φ by an Eratosthenes-style update in numpy, not the linear sieve, out to M = 6.2N. The bound comes from an elementary primorial argument: n/φ(n) ≤ 223092870/φ(223092870) = 6.1129 for n < 6,469,693,230.
- At N = 10^7 the brute force matches every claim and every analyze.out line in range:
  - V(10^k) and V(m·10^k) for all listed x ≤ 10^7, including V(10^6) = 180,184 and V(10^7) = 1,634,372.
  - All V(2x)/V(x) values for x ≤ 5·10^6.
  - The maximum of ℓ(d)/d for d ≤ 10^7: d = 2037248, ℓ = 4158795, ratio 2.041379.
  - Smallest d with ℓ(d) > 2d: d = 5888, ℓ = 11985. There are 10 such d up to 10^7.
  - No d ≤ 10^7 has ℓ(d) > 3d, and all satisfy ℓ ≤ 2.5d.
  - N_k counts at 10^6 and 10^7: [163861, 16323, 0…] and [1485793, 148579, 0…].
  - #{n: φ(n) ≤ 10^7} = 19,436,914, equal to vdfs's node count.
- I recompiled vdfs.c, vsieve.c, vdfs2.c and vdfs2ctl.c unchanged and ran them at N = 10^7 (c/). Against the brute force:
  - A7.bits, B7.bits, S7.V and C7.V are bit-identical.
  - A7.ell and B7.ell are identical (non-totients stored as UINT64_MAX).
  - All six threshold sets (t = 2.0414, 2.5, 3, 2, 2.04, 2.0414) agree exactly with the **exact-rational** classification ℓ(d) ≤ t·d.
- The banked A9.bits matches Ford 1998 Table 1, an independent computation, at all 7 tabulated points:
  - V(1M) = 180,184; V(5M) = 840,178; V(10M) = 1,634,372; V(25M) = 3,946,809; V(125M) = 18,657,531; V(300M) = 43,525,579; V(500M) = 71,399,658.
  - V(10^9) read from A9.bits is 139,847,905, as claimed.
  - Route B's B8.bits gives V(10^8) = 15,037,909, and A9 = B8 on [0, 10^8].
  - The SHA-256 of the 6 remaining big files matches SHA256_bigfiles.txt.
- I re-derived the k = 2 seeds up to 10^8 by a different route (seeds8.py). By parity, ℓ(d) ≤ 2d forces a preimage that is odd with n ≤ 2φ(n), or a power of 2. So I sieved φ over **odd** n ≤ 2·10^8 only and masked against A9.bits.
  - Result: **133** seeds, smallest 5888, as claimed. The paper's Remark 7.4 seed 2^18·257 is among them.
- I computed independent least preimages for all 133 seeds by increasing-prime memoised recursion, a different order from invphi.py (ellseeds.py):
  - The maximum is 2037248 → 4158795 (2.041379).
  - N_2(10^8) = 2 and N_3 = N_4 = N_5 = 0, matching analyze.out.
  - ℓ(387383296) = 791597265 = 3·5·17·47·257², with d = 2^16·23·257. The ratio is 2.043447 and φ(ℓ) = d is verified.
- Code attack points:
  - **Overflow.** v·(p−1) ≤ 10^9·10^9 < 2^64. n2 = n·p is formed only after φ(n2) ≤ N is ensured, so n2 is about 6.3·10^9 at most. In vsieve, φ·p ≤ M = 6.6·10^8 < 2^32. All fine.
  - **Inner prime-power loop.** The test `v2 > N/p` is exact for integer division.
  - **DFS completeness.** It covers all primes ≤ N+1, φ(1) = 1 via mark(1,1), and φ(2) = 1 via p = 2. The 10^7 brute-force equality confirms completeness.
  - **Endpoints.** The bitset holds bit N, and V(x) is cumulative up to and including x. Both confirmed.
  - **Double-precision thresholds.** t = 2, 2.5 and 3 are exact. double(2.0414) is 1.19e−16 *below* 10207/5000. Any n/v ≠ t lies at least 1/(5000v) ≥ 2e−13 from t for v ≤ 10^9, so rounding can only matter at exact equality n = 2.0414·v. There it can only create a *false seed*, never hide a real one, and the single 10^9 seed has ratio 2.043447, not 2.0414. **No case can flip toward a missed seed.**
  - S9.V XOR S9.S0 contains exactly one bit, 387383296, and S0 ⊆ V.

**Findings**

5. **The census is not new as far as 5·10^8, and reaches past 10^9 in public.**
   - Ford 1998, Table 1 (arXiv v2, p. 3) already lists V(1M), V(5M), V(10M) and V(500M) with identical values.
   - The erdosproblems.com #416 proof-claims tab (live/part1.txt) carries a claim by Rafik Zeraoulia (2026-07-29) stating: "a new reproducible exact segmented computation determining V(x) through x=10^10 and the doubling ratio V(2x)/V(x) through x=5·10^9."
   - Ford's Table 1 should also be cited as independent confirmation of the DFS.
   - Severity: **gap (provenance)**. It is fatal to any "new" or "first" wording.

6. **The ℓ(d) > 2d seeds may already be in OEIS.** A web search lists 11985 as a term of OEIS A118700. Its snippet description is "odd n with 2φ(n) < n and no smaller even number with the same totient", which is very close to "ℓ-values of k = 2 seeds". The OEIS pages are behind Cloudflare and both my fetches were blocked, so this is **unverified**. Severity: **provenance**. Check A118700 and its cross-references before calling "smallest d with ℓ(d) > 2d is 5888" or the 133-seed list new.

7. **Above 10^8 everything rests on one algorithm.** That covers V(2·10^8), V(10^9), V(2x)/V(x) for x ≥ 2·10^8, "max ℓ(d)/d ≤ 10^9 is 2.043447" and "every totient ≤ 10^9 has a preimage ≤ 2.5d".
   - vdfs2.c is a copy of vdfs.c's DFS, so "S9.V == A9.bits" is the same code run twice, not a second route.
   - Mitigation: the DFS is bit-exact against brute force at 10^7, and its V(25M), V(125M), V(300M) and V(500M) match Ford's independent table.
   - Severity: **exposition**. Say "single route above 10^8, spot-checked against Ford to 5·10^8". Do not say "two routes" for the 10^9 numbers.

8. **A comment in vsieve.c is false at three small values.** The comment reads: "n/phi(n) < e^gamma loglog n + 3/loglog n < 6.55 for 3 <= n <= 1e10".
   - The second inequality fails at n = 3, 4, 5, where the bound takes the values 32.07, 9.77 and 7.15. It also fails from about 1.12e10 onward.
   - The code is still correct. The argument only needs the bound for n > M = 6.6·10^8, where it is 6.36. The elementary primorial bound (≤ 6.1129 below 6.47·10^9) makes Rosser–Schoenfeld unnecessary.
   - The runtime guard checks only n ≤ M, which is not what certifies completeness. The certificate is the bound for n > M.
   - Severity: **exposition**. Change the comment to "for n ≥ 6".

9. **Some recorded claims can no longer be re-checked from banked files.**
   - A9.ell and B8.ell have been deleted. "ℓ arrays to 10^8 byte-identical" now rests only on the recorded equal SHA (3454080…) and analyze.out. I reproduced the downstream ℓ claims independently (finding area above), but not the arrays themselves.
   - The vdfs2ctl (t = 2, 2.04, 2.0414) control run on the full range has no banked output.
   - Severity: **exposition / reproducibility**.

## Claim 3: the bridge

**What I checked**

- I fetched FC `FormalConjectures/ErdosProblems/416.lean` at 32ac619d and at `main` from raw.githubusercontent.com.
  - Both are byte-identical to bridge/FC_416.lean (sha256 7cb5e06a…).
  - FC has not changed the statement since 32ac619d.
- verbatim_check.py exits 0, and its `--mutate` negative control exits 1.
- By eye:
  - `noncomputable abbrev V` is kept as abbrev, with `open scoped Classical in` and `Finset.Icc 1 ⌊x⌋₊ |>.filter (fun n => ∃ (m : ℕ), m.totient = n)` identical.
  - Binder names (c, hc, x) are identical.
  - `open Filter` / `open scoped Topology Real` are identical, so `𝓝` comes from the same scope.
  - It sits in namespace `Erdos416`, and `V` resolves to `Erdos416.V`. No root-level `V` exists in the TotientAsymptotic closure, and the other `V`s in the repo are all inside other namespaces.
  - The return-type coercion ℕ→ℝ is the same as FC's.
- `V_eq` targets the right object. `OAI.TotientAsymptotic.V` and `IsTotient` (`∃ n, 0 < n ∧ n.totient = v`) in Basic.lean are textually identical to the comparator file. All definitions from IsTotient through mainTerm, N and fk diff clean.
- The m = 0 branch is correct: φ(0) = 0 < 1 ≤ n.
- `.2.2.2 c hc` picks the 4th conjunct of `totient_asymptotic_formula`, which is the V(cx)/V(x) → c statement.
- Version claims check out:
  - lean-toolchain is v4.34.1.
  - The manifest pins Mathlib d13f23b7 and PNT+ c39a751, matching the bridge header.
  - The OpenAI commit FC links to, adc7f124, is an ancestor of our 1581d4cb.
  - `git diff adc7f124 HEAD` on lean/OAI/NumberTheory/TotientAsymptotic and the comparator is **empty**, so the proof FC links to is the one we use.

**Finding**

- The bridge header says FC's statements are "copied VERBATIM (text and binder names)" and that "@[category …] attributes are … dropped". FC's docstrings on the two theorems, and the `module`/`@[expose] public section` wrapper, are also dropped, and the header does not say so. Meaning is unchanged. Severity: **typo**. Add "docstrings and module/public-section wrappers dropped" to the header.

## Not checked

- The Lean build or kernel replay of Bridge416 and its mutants (done separately).
- Rosser–Schoenfeld Theorem 15 itself; I bypassed it with the primorial bound.
- Zeraoulia's numbers to 10^10, which I could not cross-check against V(10^9).
- OEIS prior art for the census and seed list: A118700, and any V(10^n) sequence. Fetches were blocked by Cloudflare.
- N_1(10^8) = 1,374,128.
- V(2x)/V(x) for 5·10^6 < x outside Ford's table points.
- The 10^9 runs themselves, which were not rerun by rule.
- Whether erdosproblemaday.com's published prose matches the brief. I checked only the claims as stated in R_brief.md.
