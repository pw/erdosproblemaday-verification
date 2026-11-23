## Verdict

The theorem says what Della Pietra claims, and I found nothing in its trust base that could let a false statement compile. The Lean theorem is exactly Erdős #301's lower-bound claim. In plain words: there is a fixed ε > 0 such that for every large N, some set A ⊆ {1..N} has no relation 1/a = 1/b₁ + … + 1/b_k (with k ≥ 2 and all entries distinct) and still has at least (1/2 + ε)N elements. I re-derived that statement in our own words from their theorem, and it compiles with only the three standard axioms. My own controls fail when they should.

## 1. What the theorem literally says (`Erdos301/Defs.lean`, unchanged since the first commit)

- **Reciprocals are exact rationals.** `def reciprocal (n : ℕ) : ℚ := ((n : ℚ))⁻¹`. Nothing lives in ℕ, so 1/a is never silently 0.
- **What counts as a relation.** `structure Relation (k : ℕ)` holds a head, and a tail `Fin k → ℕ`. Its fields require:
  - every number to be positive (`head_pos`, `tail_pos`);
  - the head to differ from every tail entry (`head_ne_tail : ∀ i, head ≠ tail i`);
  - the tail entries to be pairwise distinct (`tail_injective`);
  - at least two tail entries (`at_least_two : 2 ≤ k`);
  - `equation : reciprocal head = ∑ i, reciprocal (tail i)`.
- **Inside and Admissible.** `Inside A` means the head and every tail entry are in A. `Admissible A` means no relation of any length k sits inside A.
- **The conclusion.** `Erdos301Conclusion := ∃ ε : ℝ, 0 < ε ∧ ∃ N₀ : ℕ, ∀ N ≥ N₀, ∃ A, A ⊆ upto N ∧ Admissible A ∧ (1 / 2 + ε) * (N : ℝ) ≤ (A.card : ℝ)`, where `upto N = Finset.Icc 1 N`. The `1 / 2` there is real division; one of my controls confirms it.
- **This equals #301.** Dropping k = 1 loses nothing, since 1/a = 1/b forces a = b. Equality is used, not inequality.
- **Nothing is shadowed.** None of these names is redefined anywhere in the closure. The only other `upto` is `Erdos327.upto`, which lives in a different namespace.
- **The anti-vacuity check is real.** `Validate.not_admissible_upto` uses the actual relation 1/2 = 1/3 + 1/6 plus `mem_upto`/`omega` to show {1..N} is not admissible for N ≥ 6.

## 2. Our bridge: `~/MathDyad/erdos301/dellapietra/ours/Bridge.lean` (log in `Bridge.log`)

- **Our own definition:** `def OursFree (A) := ∀ a B, a ∈ A → B ⊆ A → a ∉ B → 2 ≤ B.card → (1:ℚ)/a ≠ ∑ b ∈ B, (1:ℚ)/b`.
- **`oursFree_of_admissible`:** their admissibility implies ours, for sets of positive integers. The proof builds one of their relations from B.
- **`ours_lower`:** the statement in Mathlib terms only, `∃ ε : ℝ, 0 < ε ∧ ∃ N₀, ∀ N ≥ N₀, ∃ A ⊆ Finset.Icc 1 N, OursFree A ∧ ((1:ℝ)/2 + ε) * N ≤ A.card`, derived from their theorem.
- **`ours_answers_EG_no`:** I added this. It states the negation of the Erdős–Graham guess directly: it is false that for every δ > 0, eventually every #301-free A ⊆ {1..N} has |A| ≤ (1/2 + δ)N.
- **Sanity lemmas:** `¬ OursFree {2,3,6}`, `¬ OursFree {2,4,6,12}` (a length-3 relation), and `¬ OursFree (Icc 1 N)` for N ≥ 6.
- **Result:** it compiled first try (exit 0, no warnings, 17 s, peak 6.7 GB). Every `#print axioms` line, including theirs, reads `[propext, Classical.choice, Quot.sound]`.

## 3. Controls

Each control is a separate file in `ours/`, with its log beside it.

| Control | What changed | Result |
|---|---|---|
| `Control_density.lean` | Same script, target density `1 + ε` | Fails (exit 1): `Type mismatch hcard has type (1 / 2 + ε) * ↑N ≤ ↑A.card but is expected to have type (1 + ε) * ↑N ≤ ↑A.card` |
| `Control_ineq.lean` | Freeness strengthened to forbid `1/a ≤ Σ` (false for any set with 3 or more elements) | Fails (exit 1): `Tactic rewrite failed … heq : 1 / ↑a ≤ ∑ b ∈ B, 1 / ↑b` |
| `Control_EG.lean` | The refuted upper bound becomes `(1 + δ)N`, which is always true | Fails (exit 1): `linarith failed to find a contradiction` |
| `Control_axioms.lean` | Positive control for the axiom printer: one proof by `sorry`, one by a planted axiom | Compiles; printer names `sorryAx` and `EPAD301.cheat` |

## 4. Trust scan

I scanned for `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`, `partial`, `set_option`, `debug.*`, `skipKernelTC`, macro/elab/syntax/notation, `instance` overrides, `irreducible`, `MetaM`/`Lean.Elab`, `run_cmd`, `#eval`, `addDecl`, `prelude`, `import all`, and `outParam`/`optParam`.

- **Erdos301 (all 24 files):** one hit, `set_option maxRecDepth 100000` in `Upper/Finite.lean`. It is harmless and that file is not in the main theorem's closure.
- **erdos327 @ a7201442 (80 modules in the closure, the whole library checked):** zero `set_option` and no escapes. The only `instance` hits are six `Decidable` instances `:= Classical.propDecidable _` and one `NeZero` instance with a real proof. Both are harmless.
- **The Mathlib fork's diff against upstream:** the merge base is `7d6261f2`, an upstream master commit (2026-07-16) that current master contains. The fork changes 5 files: `Mathlib.lean` (+1 import), `Gamma/Deriv.lean` (+75 −7: new lemmas plus a refactored proof of the n = 0 case), `Harmonic/GammaDeriv.lean` (+11), `SumPrimeReciprocals.lean` (+30), and the new `Mertens.lean` (1,378 lines). All of it only adds lemmas.
  - `Mertens.lean` contains no escapes; it has `instance instCoefn : CoeFun Weight …` and two `@[reducible]` weight definitions.
  - The fork's `lakefile.lean`, `lean-toolchain` (v4.33.0-rc1) and `lake-manifest.json` are unchanged from upstream.
  - All package revisions in the build match the pins, and the working trees are clean.
- **What the theorem actually reaches** (`ours/Closure.lean`, which walks every constant the theorem depends on: 60,547 of them):
  - The only axioms reached are `Quot.sound`, `Classical.choice` and `propext`.
  - 77 constants come from the unmerged `Mathlib.NumberTheory.Mertens`, so that file really is used.
  - The fork's additions in the other three changed files are reached too, for example `Real.deriv_Gamma_one_eq_integral_log_log` and `Nat.Primes.tsum_eq_tsum_ite`. Their disclosure ("master plus Mertens.lean") understates this slightly.
  - 48 `opaque` constants are reached, all from upstream Mathlib or core (the standard wrappers Mathlib uses for some definitions). None come from non-upstream code.
- **Your replay matches theirs:** `axioms_theirs.log` is byte-identical to their `AXIOMS.txt` (30 lines), and the build log shows `Build completed successfully (8771 jobs)` with no `sorry` warnings.

## 5. Mertens.lean

It defines an abstract "Mertens weight" and proves, with explicit constants:

- **First theorem:** |Σ_{n≤x} f(n) − log x| ≤ C₁.
- **Second theorem (`E₂_bound`):** |Σ_{n≤x} f(n)/log n − log log x − M_f| ≤ C₂/log x, with M_f given by an explicit integral.
- **For primes:** |Σ_{p≤N} 1/p − log log N − M| ≤ (log 4 + 3)/log N for N ≥ 2, plus an O(1) version.
- **Third theorem:** Π_{p≤N}(1 − 1/p) ~ e^{−γ}/log N, with |E₃(x)| ≤ (log 4 + 3)/log x + 1/⌊x⌋.
- **For von Mangoldt:** M = γ.

These are the real classical theorems, with weak but valid constants. It does not matter for soundness that nobody has reviewed the file: the kernel checks it, so even a misstated lemma could only be a true, perhaps weaker, one.

It is not merged. Upstream master has no `Mathlib/NumberTheory/Mertens.lean`. PR #41394 is open and labelled blocked-by-other-PR, and its split-out PRs #44061 and #44062 are open (last updated 10-24).

## 6. Worries, in order

1. **A fresh build from their repo fails today.** The Mathlib pin `da1f94df` is no longer on any teorth/mathlib4 branch (the branch was rewritten: diverged, ahead 1808 / behind 125). It only builds after fetching that commit by its hash (you did this). If GitHub ever garbage-collects that commit, the proof cannot be rebuilt. The author should re-pin to a reachable commit or tag.
2. **The Lean version has known kernel bugs fixed later.** v4.33.0-rc1 predates fixes for proof-of-False bugs #14576 (closed 07-28), #14875 (08-23), #15704 (10-17) and #15908 (10-24). Each needs something this code doesn't have:
   - meta code or `addDecl` (none here);
   - `prelude` or redefining `Nat.add`-style names (none);
   - `import all` with class inductives (none);
   - unusual inductive declarations (the non-upstream code defines only 3 plain structures and 1 class).

   So the remaining risk is ordinary. Your running `leanchecker --fresh` uses the same C++ kernel, so it re-checks the downloaded Mathlib files but cannot rule out bugs in that kernel. Only porting to v4.36 would close that fully.
3. **Small documentation errors.**
   - `FORMALIZATION.md` says 8,769 jobs; `BUILD.txt` and our build say 8771.
   - It cites `controls/audit-lean-formalization.py`, which does not exist at 789c6f0.
   - Its "no `opaque` anywhere in the closure" is true only outside upstream Mathlib.
4. **The scope is narrower than the problem.** The theorem settles only the "is f(N) = (1/2 + o(1))N?" question, answering no. Estimating f(N) stays open, as the author also says.

The compile is not pending. Your `leanchecker --fresh` run had started at 09:33Z with no output yet when I checked at 09:41Z. My files are in `~/MathDyad/erdos301/dellapietra/ours/`; the audit material is in `audit/` (the erdos327 clone, the fork's changed files from both commits, `cmp_master.json`, `e327_closure.txt`, and a small `probe/` checkout).