import FormalConjectures.ErdosProblems.«184»
import EGCheck.Final
open Filter
-- POSITIVE twin of WrongShape2: identical text except the bound is FC's (∃ f =O n, ≤ f (card V)); must elaborate.
open scoped Classical in
theorem right : ∃ f : ℕ → ℝ, (f =O[atTop] fun n : ℕ ↦ (n : ℝ)) ∧ ∀ {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V),
    ∃ (D : Finset G.Subgraph), (∀ H ∈ D, Erdos184.IsCycleOrEdge H.coe) ∧ SimpleGraph.IsDecomposition G D ∧ (D.card : ℝ) ≤ f (Fintype.card V) :=
  EGCheck.erdos_184
#print axioms right
