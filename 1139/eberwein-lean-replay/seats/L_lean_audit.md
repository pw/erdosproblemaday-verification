**Verdict: CLEAN.** I found no MUST-level problems. The statement checked is byte-for-byte the Formal Conjectures statement, and nothing imported can change what it means. The only changes to OpenAI's file are additions. The build here finished, and the axiom check on `Erdos1139.erdos_1139` is clean.

**Build evidence.** The build in `~/MathDyad/subs-1116/1139/build` had already finished when I looked; I only read its log. The copies there are byte-identical to the repo's.
- The log ends: `Build completed successfully (8713 jobs).`
- `info: Erdos1139Official.lean:49:0: 'Erdos1139.erdos_1139' depends on axioms: [propext, Classical.choice, Quot.sound]`
- The two new theorems report the same three axioms.
- The repo's public CI also passed on tag `1139-v2.0` (7b6aa18) and on main (111b67f). The Lean files are identical between that tag and HEAD a3bff10.
- One caveat about our own script: `run_build.sh` prints `rc=${PIPESTATUS[0]}`, which is the exit code of `tail`, not of `lake`. The evidence of success is the "Build completed successfully" line, not that `rc=0`.

## 1. Statement fidelity: holds

- **Text.** I fetched FC's `1139.lean` at the pinned commit 7db2ea3 and at main. Both are identical to `fc1139.lean`. The `theorem … := by` part of `Erdos1139Official.lean:42-44` is byte-identical to FC's, with the same non-ASCII code points, so no lookalike characters. The only differences from FC:
  - the `@[category research open, question, AMS 11]` line is removed (documentation only);
  - `sorry` is replaced by `exact Erdos1139Sketch.erdos_1139`;
  - the header and imports changed.
  
  `Erdos1139Sketch.lean:263-266` is the same statement apart from one line break.
- **Context.** Official has `open Nat Filter`, `open scoped ArithmeticFunction.Omega`, `open scoped Topology` and `namespace Erdos1139`, all as in FC. Nothing in the imported files can shadow a name the statement uses:
  - All 353 declarations sit in the namespaces `LongGapsBetweenPrimes`, `Erdos1139Cover` or `Erdos1139Sketch`. There is no `_root_`, and the only dotted name is `CoefficientEstimates.one_le_constant`, which lands inside `LongGapsBetweenPrimes`.
  - Nothing is declared in `Nat`, `Filter`, `Real`, `ArithmeticFunction`, `EReal` or `Erdos1139`.
  - There are no `notation`, `macro`, `syntax`, `elab`, `export`, `attribute` or `@[...]` lines, and no `scoped` or `local` declarations.
  - The only instance is `Erdos1139Sketch.lean:25` `instance : DecidablePred AlmostPrime2`. It is used only by `Nat.count` inside a lemma and cannot affect the statement.
  - The statement's identifiers are byte-identical to FC's, so anything left undeclared would at worst become an extra universally quantified variable. That only makes the theorem stronger.
- **Mathlib definitions.** In Mathlib db584cd: `scoped[ArithmeticFunction.Omega] notation "Ω" => ArithmeticFunction.cardFactors`, and `cardFactors` is `n.primeFactorsList.length`. `Nat.nth` counts from 0, so `u 0 = 1`. `primorial n` is the product of primes ≤ n, and `primesLE n = primesBelow (n+1)`.
- **Indexing.** With u counted from 0 and `log(↑k+1)`, the FC ratio is the problem's (u_{k+2}−u_{k+1})/log(k+1). Shifting the index does not change whether the limsup is infinite. At k = 0 the division by log 1 = 0 gives 0, which is harmless.

## 2. Hygiene hits (file:line)

| Hit | Matters? |
|---|---|
| `Challenge.lean:13` `  sorry` | No. It is OpenAI's unchanged comparator challenge file: not in `defaultTargets`, not imported by anything. The CI grep rightly skips it. |
| `Erdos1139Sketch.lean:7` "A complete, `sorry`-free proof…" | No, docstring. |
| `Erdos1139Cover.lean:161` "partial sums" | No, docstring. |
| `Erdos1139Cover.lean:22-23` `set_option maxSynthPendingDepth 1` / `set_option linter.mathlibStandardSet false` | No. These only affect elaboration and linting. |
| `Erdos1139Sketch.lean:25` global `DecidablePred AlmostPrime2` instance | No. |
| `LongGapsBetweenPrimes.lean:1746, 3448-3450, 3631` (upstream) and `:3747` (new) `by decide` on small ℕ facts | No. This is ordinary kernel `decide`, not `native_decide`. |
| `LongGapsBetweenPrimes.lean:2565` `open scoped Fin.CommRing in` | No (upstream, scoped to one declaration). |
| `#print axioms` at `LongGapsBetweenPrimes.lean:4680/4684/4685` and `Erdos1139Official.lean:49` | No, read-only. |

There are no matches anywhere for: `admit`, `native_decide`, `axiom`, `implemented_by`, `extern`, `unsafe`, `opaque`, `partial def`, `csimp`, `ofReduceBool`, `run_cmd`/`run_elab`/`#eval`, `debug.*`/trust options, or any `macro`/`syntax`/`elab`. No local folder shadows Mathlib. The manifest pins Mathlib to `db584cd`, which is what the build used.

## 3. Upstream diff

- **Where the upstream lives.** It is not in github.com/openai/math. I cloned that repo: no file there mentions `LongGapsBetweenPrimes`, `short_translates` or `long_prime_gaps`. Its prime-gap family (026, `lean/OAI/NumberTheory/PrimeGaps`) is a different result. The real upstream is github.com/openai/LongGapsBetweenPrimes, as CHANGES.md and NOTICE say, at commit `03a1190`, which is its current HEAD.
- **The diff is additions only.** Diffing upstream `03a1190` against the repo's `LongGapsBetweenPrimes.lean` gives two hunks (`3674a3675,3813` and `4543a4683,4685`) and zero removed lines. The repo's `short_translates_divisor.diff` matches the real diff exactly.
- **What was added:**
  - `eventually_sieveY_mul_floor_lt_primorial`
  - `short_translates_divisor_with_sieveDelta`
  - `short_translates_divisor`
  - two `#print axioms` lines
- **Other files.** `Challenge.lean`, `comparator.json`, `formalization.yaml`, `lake-manifest.json`, `lean-toolchain` and `LICENSE` are identical to upstream, and the README is only renamed. `lakefile.toml` only adds three `lean_lib`s and `defaultTargets`.
- **Comparator.** `comparator.json` still checks only OpenAI's `LongGapsBetweenPrimes.long_prime_gaps` against the unchanged `Challenge.lean`. It does not cover `erdos_1139` or the two new theorems.
- **Does the proof rely on a changed statement?** No. It relies on the new `short_translates_divisor`, a new statement with a new proof, which Lean's kernel checks during the build. Every upstream lemma it uses is unmodified. Those are `eventually_simultaneous_roots`, `eventually_sieveY_lt_primorial`, `sieveZ_lower`, `exists_linear_roots`, `prime_dvd_auxiliaryProduct`, `mem_auxiliaryPrimes` and `sieveDelta_pos/_lt_half`. The covering file also uses `greedy_residue_classes`, `eventually_cover_parameters`, `eventually_zeroSurvivors_bound`, `eventually_greedy_product_bound`, `coverZ_le_floor`, `coverW_le_coverZ`, `zeroCoverPrimes_subset/_disjoint`, `auxiliaryPrimes_prime` and `smoothScaleConstant_pos`.

## 4. Lemma chain (exact statements; every step means what the paper and README say)

1. `Erdos1139.erdos_1139` is proved by `exact Erdos1139Sketch.erdos_1139`, which has the identical statement.
2. `Erdos1139Sketch.erdos_1139` rewrites u as `Nat.nth AlmostPrime2`, where `def AlmostPrime2 (n : ℕ) : Prop := 0 < n ∧ Ω n ≤ 2`. It then shows that for every real M, `M+1 ≤ limsup` frequently, using `EReal.eq_top_iff_forall_lt` and `le_limsup_of_frequently_le'`. The parameters are C = 2(|M|+1)+2, `log(k+1) ≤ 4x+2` from `N ≤ 2e^{4x}`, and a gap of at least `3Cx−1`.
3. `eventually_long_run (C) (hC : 1 ≤ C) : ∀ᶠ x : ℝ in atTop, ∃ N : ℕ, primorial ⌊x⌋₊ ≤ N ∧ (N : ℝ) ≤ 2 * Real.exp (4 * x) ∧ ∀ j ∈ Finset.Icc 1 (runLength C x), 3 ≤ Ω (N + j)`, with `runLength C x := ⌊3 * C * x⌋₊`. This is "every N+j has Ω ≥ 3".
4. `gap_of_run {N H} (hN : 1 ≤ N) (hrun : ∀ j ∈ Finset.Icc 1 H, 3 ≤ Ω (N + j)) : ∃ k, k + 1 = Nat.count AlmostPrime2 (N + 1) ∧ Nat.nth AlmostPrime2 k ≤ N ∧ N + H < Nat.nth AlmostPrime2 (k + 1)`. Counting from 0 is handled correctly, and `K < k` gives k → ∞.
5. Lemmas used by step 3:
   - `three_le_cardFactors_of_two_primes (hp hq) (hpq : p ≠ q) (hpn : p ∣ n) (hqn : q ∣ n) (hlt : p * q < n) : 3 ≤ Ω n`
   - `exists_crt_shift n a (ha : ∀ p ∈ n.primesLE, a p < p) : ∃ b < primorial n, ∀ p ∈ n.primesLE, p ∣ b + a p`
   - `dvd_shift_of_hit … : q ∣ b + primorial n * t + j`
   - `shift_le`
   - `eventually_floor_mul_floor_lt_primorial : ∀ᶠ x, ⌊x⌋₊ * ⌊x⌋₊ < primorial ⌊x⌋₊`
   - `eventually_runLength_bounds : … x < runLength C x ∧ runLength C x ≤ x * Real.log x ^ 2`
6. `eventually_cover C hC δ hδ : ∀ᶠ x, Nonempty (CoverData x (runLength C x) δ)`. `CoverData` has fields:
   - `a_lt : ∀ p ∈ ⌊x⌋₊.primesLE, a p < p`
   - `hit : ∀ j ∈ Icc 1 H, ∃ p ∈ ⌊x⌋₊.primesLE, j % p = a p`
   - `S₁ = (Icc 1 H).filter (fun j => (primesLE.filter (fun p => j % p = a p)).card = 1)`
   - `S₁_card : (S₁.card : ℝ) ≤ δ * x`
7. `Erdos1139Cover.eventually_cover_residues (C δ) (hC : 1 ≤ C) (hδ : 0 < δ) : ∀ᶠ x, ∀ H, x / 4 ≤ H → (H : ℝ) ≤ 3 * C * x → ∃ a, (…a p < p) ∧ (∀ j ∈ Icc 1 H, ∃ p ∈ ⌊x⌋₊.primesLE, j % p = a p) ∧ (#{j hit exactly once} : ℝ) ≤ δ * x`. It is built from:
   - `exists_few_divisors_small` (a fixed prime set F with second moment `few_divisors_card_mul_le`; divergence via Mathlib's `not_summable_one_div_on_primes`);
   - `combine_greedy_residues_zero`;
   - `eventually_card_top_primes : x / (4 log x) ≤ #(primes in (⌊x/4⌋, ⌊x⌋])`;
   - `eventually_survivors_le_top`;
   - an injection of the survivors into the top primes (`Function.Embedding.nonempty_of_card_le`).
8. `short_translates_divisor : ∃ δ, 0 < δ ∧ δ < 1/2 ∧ ∀ᶠ x, ∀ H, x < H → H ≤ x (log x)^2 → ∀ S ⊆ Icc 1 H, S.card ≤ δ x → ∀ b < primorial ⌊x⌋₊, ∃ t, 1 ≤ t ∧ t ≤ e^x ∧ ∀ s ∈ S, ∃ p, p.Prime ∧ ⌊x⌋₊ < p ∧ p * ⌊x⌋₊ < b + primorial ⌊x⌋₊ * t + s ∧ p ∣ b + primorial ⌊x⌋₊ * t + s`. It follows from the `_with_sieveDelta` version, which adds `x^6 < p ≤ exp(x/(log x)^5)`. This matches the paper's Proposition P word for word, and its hypotheses are the same as OpenAI's `ShortTranslates`.

## 5. Claims, ranked

**MUST:** none.

**SHOULD**
1. **No independent kernel re-check of `erdos_1139`.** Both our build and their CI rely on Lean's own kernel during `lake build` plus `#print axioms`. The cheapest stronger check is a Comparator config with challenge = the FC statement with `sorry`, solution = `Erdos1139Official`, theorem `Erdos1139.erdos_1139`. Comparator and lean4export are already dependencies in the lakefile. Running `leanchecker` would also work. This is extra robustness, not a defect I found.
2. **Credit wording.** The Lean proof uses more of OpenAI's work than Proposition 1.2: it also reuses their Theorem 1.1 covering machinery (zero-cover and greedy residues, the smooth-number survivor bound, the greedy product bound). The paper's formalization notes and README step 2 say so. The README's "Prior work and credits" section and the paper's abstract name only Proposition 1.2. Our page should credit both.

**NOTE (no overclaim found; the prose never states more than the Lean proves)**
- The paper's abstract is out of date and understates: it says "the remaining steps use standard estimates". The written Lemmas 2–5 (Hildebrand, Mertens, PNT, Halberstam–Richert) are not formalized; the Lean proof uses modified versions, which the paper's Section 6 states honestly.
- Paper §3 says "lake build completes with no errors or warnings". The full build has one style warning, at `Erdos1139Sketch.lean:267` (a `show` that should be `change`).
- Several repo documents are out of date:
  - The README's "Building" paragraph says CI greps only `LongGapsBetweenPrimes.lean`; the workflow actually checks all four files and the six axiom reports.
  - NOTICE lists only the `Erdos1139Sketch` target and file. It omits `Erdos1139Cover.lean`, `Erdos1139Official.lean` and their targets.
  - `paper/README.md` still says the PDF "will be added".
- **Version pins differ from FC's.** FC uses Lean v4.33.1 and Mathlib 0df444a; this repo uses Lean v4.33.0 and Mathlib db584cd. The definitions of `Nat.nth`, `cardFactors` and `Ω` are identical in both Mathlib revisions.
- **Reading of the problem.** The proof covers "at most 2 prime factors" counted with multiplicity (Ω), which is FC's reading and the forum's 2-fold-cover framing. erdosproblems.com returned a Cloudflare 403, so I could not re-read the problem page directly.
- The other credit lines check out. OpenAI's PDF says "The proof is due to GPT 6 Astra" and states Proposition 1.2 as the Lean `ShortTranslates`. Price's priority is stated in the paper, and Chojecki, Tao, Woett and gavinsherry are credited in the README.

Upstream and comparison material is in `/tmp/oai1139/` (`lgbp/`, `math/`, `actual.diff`, `decls.txt`, `paper/paper.txt`, `oaipdf/`).