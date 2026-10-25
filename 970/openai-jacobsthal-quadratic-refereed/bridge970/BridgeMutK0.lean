import Mathlib
import OAI.NumberTheory.Jacobsthal.Main

/-!
# Bridge: OpenAI's Lean ⟹ Formal Conjectures' `Erdos970.erdos_970` and `Erdos970.erdos_970.variants.iterated_log`
(erdos cron seat, 2026-10-23)

The two definitions and two statements in `namespace Erdos970` below are verbatim copies of
`FormalConjectures/ErdosProblems/970.lean` at google-deepmind/formal-conjectures@93e94653 (FC attributes and docstrings
removed; `verbatim_check.py` asserts the copies, whitespace-normalised). FC tags both statements "research solved" and links
OpenAI's Lean, but their proof bodies are `sorry`: FC states the bound for `jacobsthalFunction k := sInf {m | IsJacobsthalBound k m}`,
OpenAI's theorems state the existence of SOME admissible `m` below the bound. The proofs below make that one step (an admissible
`m` bounds the infimum). The proofs are ours; the mathematics is OpenAI's.
-/

namespace Erdos970

def IsJacobsthalBound (k m : ℕ) : Prop :=
  ∀ n : ℕ, 0 < n → n.primeFactors.card ≤ k →
    ∀ a : ℤ, ∃ i : ℕ, i < m ∧ (a + i).natAbs.Coprime n

noncomputable def jacobsthalFunction (k : ℕ) : ℕ :=
  sInf {m : ℕ | IsJacobsthalBound k m}

/-- FC's predicate and OpenAI's are the same proposition (both bodies are the identical term). -/
theorem isJacobsthalBound_iff_oai (k m : ℕ) :
    IsJacobsthalBound k m ↔ OAI.Erdos970.NumberTheoryLean.Targets.IsJacobsthalBound k m := Iff.rfl

/-- Any admissible `m` bounds FC's `jacobsthalFunction k` from above. -/
theorem jacobsthalFunction_le_of_oai {k m : ℕ}
    (h : OAI.Erdos970.NumberTheoryLean.Targets.IsJacobsthalBound k m) : jacobsthalFunction k ≤ m :=
  Nat.sInf_le ((isJacobsthalBound_iff_oai k m).2 h)

theorem erdos_970 :
    ∃ C > (0 : ℝ), ∀ k : ℕ, (jacobsthalFunction k : ℝ) ≤ C * k ^ 2 := by
  obtain ⟨C, hC, h⟩ := OAI.Erdos970.Erdos970Final.erdos_970_quadratic
  refine ⟨C, hC, fun k hk => ?_⟩
  obtain ⟨m, hm, hb⟩ := h k hk
  exact le_trans (by exact_mod_cast jacobsthalFunction_le_of_oai hm) hb

theorem erdos_970.variants.iterated_log :
    ∃ C > (0 : ℝ), ∀ k : ℕ, 0 < k →
      (jacobsthalFunction k : ℝ) ≤ C * k ^ 2 / (Real.log (Real.log (3 * k))) ^ 2 := by
  obtain ⟨C, hC, h⟩ := OAI.Erdos970.Erdos970Final.erdos_970_iterated_log
  refine ⟨C, hC, fun k hk => ?_⟩
  obtain ⟨m, hm, hb⟩ := h k hk
  exact le_trans (by exact_mod_cast jacobsthalFunction_le_of_oai hm) hb

end Erdos970
