import Solution
/-! NEGATIVE CONTROL: the same copy with the factor 2 changed to 3. This must FAIL to elaborate. -/
namespace FCbad
def erdos_488_FC : Prop := ∀ (A : Finset ℕ), A.Nonempty →
    -- These are needed for the reasons outlined here: https://github.com/google-deepmind/formal-conjectures/pull/256
    0 ∉ A → 1 ∉ A →
    letI B := {n ≥ 1 | ∃ a ∈ A, a ∣ n}
    ∀ᵉ (n : ℕ) (m > n), A.max ≤ n →
      ((Finset.Icc 1 m).filter (· ∈ B)).card / (m : ℚ) <
        3 * ((Finset.Icc 1 n).filter (· ∈ B)).card / n
theorem not_erdos_488_FC : ¬ erdos_488_FC := Erdos488.not_erdos_488
end FCbad

