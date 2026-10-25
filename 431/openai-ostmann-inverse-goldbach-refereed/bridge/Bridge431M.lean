import Mathlib
import OAI.NumberTheory.Ostmann.Main

/-!
# Bridge: OpenAI's Lean ⟹ Formal Conjectures' `Erdos431.erdos_431` and `Erdos431.erdos_431.variants.ostmann`
(erdos cron seat, 2026-10-23), from route M (`OAI.NumberTheory.Ostmann.Main`, the solution module of OpenAI's comparator challenge `OstmannPrimes`).

The two statements in `namespace Erdos431` below are verbatim copies of `FormalConjectures/ErdosProblems/431.lean` at
google-deepmind/formal-conjectures (commit in FC_SHA.txt; FC attributes and docstrings removed; `verbatim_check.py` asserts
the copies, whitespace-normalised). FC tags both "research solved" and links OpenAI's Lean, but their proof bodies are
`sorry`. FC's `erdos_431` is phrased with `=ᶠ[Filter.cofinite]` on sets and two INFINITE summands; OpenAI's theorem is
phrased with `Set.Infinite (· ∆ ·)` and two NONTRIVIAL summands. The proofs below are that translation. The proofs are
ours; the mathematics is OpenAI's.
-/

namespace Erdos431

open scoped Pointwise

open scoped symmDiff

theorem erdos_431.variants.ostmann :
    ∀ A B : Set ℕ, A.Nontrivial → B.Nontrivial → ((A + B) ∆ {n | n.Prime}).Infinite := by
  intro A B hA hB
  exact OAI.Ostmann.main A B hA hB

theorem erdos_431 :
    ¬ ∃ A B : Set ℕ, A.Infinite ∧ B.Infinite ∧
      (A + B : Set ℕ) =ᶠ[Filter.cofinite] {n | n.Prime} := by
  rintro ⟨A, B, hA, hB, h⟩
  apply erdos_431.variants.ostmann A B hA.nontrivial hB.nontrivial
  have h' : {x | ¬ (x ∈ A + B ↔ x ∈ {n : ℕ | n.Prime})}.Finite :=
    Filter.eventually_cofinite.mp (Filter.eventuallyEqSet_iff.mp h)
  refine h'.subset ?_
  intro n hn
  simp only [Set.mem_symmDiff, Set.mem_setOf_eq] at hn ⊢
  tauto

end Erdos431
