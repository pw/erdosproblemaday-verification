# Seat S — statement and definitions (2026-10-31)
(Saved by the main seat from the seat's final message; the harness blocked the subagent from writing this file.)

**VERDICT: HOLDS WITH NOTES.** The final Lean statements say what paper Theorem 1.2, (4) and (5) say, using the problem's own definitions of u and f. Caveat: they live in ℕ∞, so reading them with f(n) finite needs an outside fact (Note A).

Repo /tmp/e684/lean/repo @ 49ee38c (tag v3-arxiv); Mathlib 905b958 (= v4.32.2); PNT+ a5154676. Read-only, no lake/lean run. Paper numbering: Remark 1.1 shares the counter, so the main result is Theorem 1.2, displays (4) and (5).

## 1. Definitions — OK
- `Defs.lean:31` `def uPart (n k : ℕ) : ℕ := ∏ p ∈ primesLE k, p ^ (n.choose k).factorization p`; `Defs.lean:35` `sInf ((fun k : ℕ => (k : ℕ∞)) '' {k : ℕ | 1 ≤ k ∧ k ≤ n ∧ n ^ 2 < uPart n k})`.
- Mathlib `PrimeCounting.lean:132` `def primesLE (n : ℕ) : Finset ℕ := primesBelow (n + 1)`; `:129` `primesBelow n := {p ∈ Finset.range n | p.Prime}` ⇒ primes p ≤ k incl. p = k.
- `Sanity.lean:26`: u · (part from primes > k) = C(n,k). Identical to FC `smallPrimePart` (FC 684.lean:36–37).
- Edge cases: k=0 ⇒ u=1 (excluding k=0 changes nothing for n ≥ 1); n=0: problem f(0)=0, Lean ⊤ (harmless); k=1, k=n ⇒ u=1 both; empty set ⇒ ⊤ = sInf ∅ = paper's +∞.
- `fcheck.py`: literal Lean definition vs the problem's wording, n ≤ 400 — only disagreement n = 0. `ftop.py`: for 2 ≤ n ≤ 60,000 the defining set is empty only for n ∈ {2–9, 11–15, 17, 19, 20, 23}.
- Could not check: Erdős 1979 original (paper §9 paraphrase agrees).

## 2. Final statements — OK (Note A)
- `MainUnconditional.lean:20-23`, `:28`, `Sanity.lean:145-147` (limsup in ℝ≥0∞).
- `∀ k, k ≤ X → k < fThr n` ⟺ f(n) > X (X ≥ 0: ⌊X⌋ < f; X < 0: vacuous, f ≥ 1 > X anyway).
- log log log n ≤ 0 (Lean x/0 = 0) covers finitely many n; `∃ᶠ` needs witnesses past every N. ε ≥ ½ trivial, as in the paper. ℕ∞→ℝ≥0∞ sends ⊤ to ⊤ (`ENatENNReal.lean:49`); `ofReal` clips finitely many n.
- **Note A.** Every final statement holds automatically at any n with fThr n = ⊤, and the repo never proves f(n) < ⊤ eventually. The witnesses are genuine (`Main.lean:177-192` proves u ≤ n² for every k ≤ K < n_t). Finiteness for large n comes from APSSV / FC `erdos_684.upper_bound` (k ≤ 514 (log n)², proof by AItoBit Solution.lean, HTTP 200 at the pinned SHA vs 404 for a garbage SHA; not built). Recommendation: a ~10-line corollary importing FC's upper bound. [Main seat: done — `erdos684/bridge/Bridge684.lean`.]

## 3. PNT bridge — OK by source scan
- `PNT.lean:19` uses `MediumPNT` (`MediumPNT.lean:3710-3712`): `∃ c > 0, (ψ - id) =O[atTop] fun x ↦ x * Real.exp (-c * (Real.log x) ^ ((1 : ℝ) / 10))`, ψ = Mathlib `Chebyshev.psi`. `pntHyp` follows via `psi_sub_theta_le`, `theta_le_psi`, `theta_le_log4_mul_x`.
- MediumPNT import closure 8,662 files (14 PNT+, 9 LeanArchitect); the 14 PNT+ files contain no sorry/admit/native_decide/sorry_using; the sorried PNT+ files (StrongPNT, Wiener, IEANTN/*) are outside the closure.
- **Note B — WITHDRAWN by the main seat (2026-10-31, after the blind cold read):** the two lines are inside the `/-- … -/` docstring (lines 120–178) of PrimeNumberTheoremAnd's `Tactic/AdditiveCombination.lean`, an example in a code fence; they declare nothing (text-scan false positive). Original note: `Tactic/AdditiveCombination.lean:172-173` declares `axiom qc : ℚ`, `axiom hqc : qc = 2*qc` inside the closure — consistent (qc = 0), used only in an `example`. [Main seat: our `#print axioms` on all five headline theorems shows only propext, Classical.choice, Quot.sound — neither qc nor hqc is used.]
- LeanArchitect sets `debug.skipKernelTC` only in its blueprint-extraction IO runner, not on the compile path; `@[blueprint]` stores metadata only.
- **Note C** (could not check `#print axioms`). [Main seat: checked, `replay/logs/audit.log`.]

## 4. Parameters — OK
`Params` (Defs.lean:48–61) = paper (11)–(12). Final theorems take none: `Main.lean:270` `let P : Params := optParams (ε / 8) (64 / ε) …`; constraints proved in `Main.lean:200-213` (nlinarith/linarith); key margin c − a = 215/2 + 35ε/4 + ε²/2 ≥ 1 by hand. No `Classical.choose`; `noncomputable` only from ℝ and `sInf`.

## 5. Escape hatches — OK
None of sorry/admit/axiom/native_decide/decide/implemented_by/extern/opaque/unsafe/partial/set_option/macro/elab/syntax/notation/instance/attribute in the project's own files. Only command: `#print axioms`. All variables in final statements explicitly bound.

## 6. Formal Conjectures 684.lean (saved `fc/684.lean`, last commit d9f6ffa8, 2026-10-29)
- `erdos_684.upper_bound` (52-54) and `erdos_684.lower_bound` (64-66: `∃ᶠ n, 1 < n ∧ ∀ k, (k:ℝ) ≤ log n / 8 → smallPrimePart n k = 1`), both "research solved"; no open headline.
- Bae's result settles neither (FC's lower bound needs u = 1, Bae shows u ≤ n²). It would be a new variant in FC's vocabulary. FC's `upper_bound` is exactly the finiteness fact Note A needs.

Scripts: closure.py, list_pkg.py, fcheck.py, ftop.py. Outputs: closure_MediumPNT.txt, v3.txt, fc/684.lean.
