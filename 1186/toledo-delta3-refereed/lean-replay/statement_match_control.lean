import Erdos.Proofs.P1186ExFinal
/-! Negative control: the same fresh copy with ONE change (k - 1 replaced by k in the progression length bound),
so `exact h` must FAIL. -/
open Filter Asymptotics
namespace FCbad
def monoCount (k n : ℕ) (c : ℕ → Bool) : ℕ :=
  ((Finset.Icc 1 n ×ˢ Finset.Icc 1 n).filter fun p : ℕ × ℕ =>
    p.1 + k * p.2 ≤ n ∧ ∀ i < k, c (p.1 + i * p.2) = c p.1).card
noncomputable def minMonoCount (k n : ℕ) : ℕ :=
  sInf {m : ℕ | ∃ c : ℕ → Bool, monoCount k n c = m}
noncomputable def δ (k : ℕ) : ℝ :=
  atTop.liminf (fun n : ℕ ↦ (minMonoCount k n : ℝ) / (n : ℝ) ^ 2)
theorem prs_conjecture_bad : δ 3 = 117 / 2192 := by
  have h := Erdos1186Day.erdos_1186.variants.prs_conjecture
  exact h
end FCbad
