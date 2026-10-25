import Erdos128
/-- Negative control: a sorry'd theorem of the endpoint's shape must show `sorryAx` in `#print axioms`. -/
theorem host_neg_control (hBCL : Erdos128.ModuloBCL.BCLEventual)
    (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (htri : G.CliqueFree 3) :
    Erdos128.HasSparseHalf G ((1 / 50 : ℚ) * (Fintype.card V : ℚ) ^ 2) := by
  sorry
#print axioms host_neg_control
