import Solution
/-! erdosproblemaday.com, 2026-11-20. FC's `erdos_488` body, copied verbatim from google-deepmind/formal-conjectures main
(FormalConjectures/ErdosProblems/488.lean, last changed by commit 7db2ea3, 14 Oct 2026), placed in a fresh namespace as a
Prop, and the submitter's theorem applied to it. Elaborated with the repo's Mathlib (v4.35.0-rc2), NOT inside an FC checkout. -/
namespace FCnow
def erdos_488_FC : Prop := ∀ (A : Finset ℕ), A.Nonempty →
    -- These are needed for the reasons outlined here: https://github.com/google-deepmind/formal-conjectures/pull/256
    0 ∉ A → 1 ∉ A →
    letI B := {n ≥ 1 | ∃ a ∈ A, a ∣ n}
    ∀ᵉ (n : ℕ) (m > n), A.max ≤ n →
      ((Finset.Icc 1 m).filter (· ∈ B)).card / (m : ℚ) <
        2 * ((Finset.Icc 1 n).filter (· ∈ B)).card / n
theorem planted : ¬ erdos_488_FC := by sorry
end FCnow
#print axioms FCnow.planted
