import OAI.NumberTheory.TotientAsymptotic.UnconditionalMain

/-!
# Bridge (erdosproblemaday.com, 2026-10-21): Formal Conjectures' `Erdos416.erdos_416.parts.i` and
# `Erdos416.erdos_416.variants.regularly_varying` from OpenAI's `OAI.TotientAsymptotic.totient_asymptotic_formula`
# (family 24, `OAI.NumberTheory.TotientAsymptotic.UnconditionalMain` closure).

`Erdos416.V` and the statements of `erdos_416.parts.i` and `erdos_416.variants.regularly_varying` below are copied
VERBATIM (text and binder names) from google-deepmind/formal-conjectures @ 32ac619d83ac8943c968142436f782525d75a49f:
`FormalConjectures/ErdosProblems/416.lean`, namespace `Erdos416`, with its `open` lines. FC's `@[category ...]`
attributes are FC-only and dropped. This proves a verbatim copy of FC's statements in OpenAI's environment
(Lean v4.34.1, Mathlib d13f23b7), not FC's own constants.

FC's `V` counts `n ∈ [1, ⌊x⌋]` with `∃ m, m.totient = n` (any `m`, including `0`); OpenAI's `V` counts `n ∈ [1, ⌊x⌋]`
with `∃ m, 0 < m ∧ m.totient = n`. They agree because `φ 0 = 0 < 1 ≤ n` (`V_eq`).
-/

open Filter
open scoped Topology Real

namespace Erdos416

/-- Let `V(x)` count the number of `n≤x` such that `ϕ(m)=n` is solvable. -/
noncomputable abbrev V (x : ℝ) : ℝ :=
  open scoped Classical in
  (Finset.Icc 1 ⌊x⌋₊ |>.filter (fun n => ∃ (m : ℕ), m.totient = n)).card

/-- FC's counting function equals OpenAI's. -/
theorem V_eq (x : ℝ) : V x = OAI.TotientAsymptotic.V x := by
  unfold V OAI.TotientAsymptotic.V
  congr 1
  congr 1
  ext n
  simp only [Finset.mem_filter, Finset.mem_Icc, OAI.TotientAsymptotic.IsTotient]
  constructor
  · rintro ⟨⟨h1, h2⟩, m, hm⟩
    refine ⟨⟨h1, h2⟩, m, ?_, hm⟩
    rcases Nat.eq_zero_or_pos m with rfl | hpos
    · simp at hm
      omega
    · exact hpos
  · rintro ⟨⟨h1, h2⟩, m, -, hm⟩
    exact ⟨⟨h1, h2⟩, m, hm⟩

theorem erdos_416.variants.regularly_varying (c : ℝ) (hc : 0 < c) :
    Filter.Tendsto (fun x => V (c * x) / V x) Filter.atTop (𝓝 c) := by
  have h := (OAI.TotientAsymptotic.totient_asymptotic_formula).2.2.2 c hc
  have e : (fun x => V (c * x) / V x) =
      (fun x => OAI.TotientAsymptotic.V (c * x) / OAI.TotientAsymptotic.V x) := by
    funext x
    rw [V_eq, V_eq]
  rw [e]
  exact h

theorem erdos_416.parts.i :
    Filter.Tendsto (fun x => (V (2 * x) / V (x))) Filter.atTop (𝓝 3) := by
  exact erdos_416.variants.regularly_varying 2 two_pos

end Erdos416
