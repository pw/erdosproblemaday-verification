import FormalConjectures.ErdosProblems.«184»
import EGCheck.Final
open Filter in
-- must FAIL: a CONSTANT bound on the number of parts is false (n/2 disjoint edges need n/2 parts)
theorem wrong : ∃ c : ℝ, ∀ {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V),
    ∃ (D : Finset G.Subgraph), (∀ H ∈ D, Erdos184.IsCycleOrEdge H.coe) ∧ SimpleGraph.IsDecomposition G D ∧ (D.card : ℝ) ≤ c :=
  EGCheck.erdos_184
