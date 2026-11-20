import Erdos.Proofs.P1186ExFinal
/-! Statement match (erdosproblemaday.com, 2026-11-19): the three definitions below are copied verbatim from
google-deepmind/formal-conjectures main, FormalConjectures/ErdosProblems/1186.lean (commit 4beab72, the only commit
touching that file as of 2026-11-19), into a fresh namespace, and Quana's theorem is applied to the FRESH δ. -/
open Filter Asymptotics
namespace FCnow
def monoCount (k n : ℕ) (c : ℕ → Bool) : ℕ :=
  ((Finset.Icc 1 n ×ˢ Finset.Icc 1 n).filter fun p : ℕ × ℕ =>
    p.1 + (k - 1) * p.2 ≤ n ∧ ∀ i < k, c (p.1 + i * p.2) = c p.1).card
noncomputable def minMonoCount (k n : ℕ) : ℕ :=
  sInf {m : ℕ | ∃ c : ℕ → Bool, monoCount k n c = m}
noncomputable def δ (k : ℕ) : ℝ :=
  atTop.liminf (fun n : ℕ ↦ (minMonoCount k n : ℝ) / (n : ℝ) ^ 2)
theorem prs_conjecture_fresh : δ 3 = 117 / 2192 := by
  have h := Erdos1186Day.erdos_1186.variants.prs_conjecture
  exact h
end FCnow
#print axioms FCnow.prs_conjecture_fresh
