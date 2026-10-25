import OAI.Combinatorics.Ramsey.CycleClique.MainTheorem

/-!
# Bridge (erdosproblemaday.com, 2026-10-20): Formal Conjectures' `Erdos551.erdos_551` (and its
# `variants.sufficiently_large`) from OpenAI's `OAI.CycleClique.main` (family 189, MainTheorem closure).

The definition `graphRamsey` and both theorem statements below are copied VERBATIM (text and binder names) from
google-deepmind/formal-conjectures @ 90d18f666eb98adec4eee4d12f1d37e30b4eb204 (2026-10-20T20:20:35Z):
`FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Ramsey.lean` (namespace `SimpleGraph`) and
`FormalConjectures/ErdosProblems/551.lean` (namespace `Erdos551`, tagged `research open` / `research solved`).
Only the enclosing namespace differs (`Bridge551`). This proves a verbatim copy of FC's statement in OpenAI's
environment (Lean v4.34.1, Mathlib d13f23b7), not FC's own constant.
-/

namespace Bridge551

namespace SimpleGraph

noncomputable def graphRamsey {α β : Type*} [Fintype α] [Fintype β]
    (G : SimpleGraph α) (H : SimpleGraph β) : ℕ :=
  sInf { n : ℕ | ∀ (C : SimpleGraph (Fin n)), G.IsContained C ∨ H.IsContained Cᶜ }

end SimpleGraph

open Filter

namespace Erdos551

theorem erdos_551 :
    ∀ (k n : ℕ), 3 ≤ n → n ≤ k → ¬(n = 3 ∧ k = 3) →
      SimpleGraph.graphRamsey (SimpleGraph.cycleGraph k)
        (SimpleGraph.completeGraph (Fin n)) = (k - 1) * (n - 1) + 1 := by
  intro k n hn hnk hne
  have hne' : (k, n) ≠ (3, 3) := by
    intro h
    exact hne ⟨(Prod.mk.inj h).2, (Prod.mk.inj h).1⟩
  have h := OAI.CycleClique.main k n hnk hn hne'
  rw [← h]
  rfl

theorem erdos_551.variants.sufficiently_large :
    ∀ᶠ n : ℕ in atTop, ∀ k : ℕ, n ≤ k →
      SimpleGraph.graphRamsey (SimpleGraph.cycleGraph k)
        (SimpleGraph.completeGraph (Fin n)) = (k - 1) * (n - 1) + 1 := by
  refine Filter.eventually_atTop.2 ⟨4, fun n hn k hk => ?_⟩
  exact erdos_551 k n (by omega) hk (by omega)

end Erdos551

end Bridge551

#print axioms Bridge551.Erdos551.erdos_551
#print axioms Bridge551.Erdos551.erdos_551.variants.sufficiently_large
