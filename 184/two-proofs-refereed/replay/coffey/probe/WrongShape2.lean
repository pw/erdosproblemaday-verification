import FormalConjectures.ErdosProblems.«184»
import EGCheck.Final
open Filter
-- must FAIL with a TYPE MISMATCH on the bound (not an instance failure): a CONSTANT bound on the number of parts is false
-- (n/2 disjoint edges need n/2 parts). Same binder shape as FC's erdos_184, with `f (card V)` replaced by a constant c.
open scoped Classical in
theorem wrong : ∃ c : ℝ, ∀ {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V),
    ∃ (D : Finset G.Subgraph), (∀ H ∈ D, Erdos184.IsCycleOrEdge H.coe) ∧ SimpleGraph.IsDecomposition G D ∧ (D.card : ℝ) ≤ c :=
  EGCheck.erdos_184
