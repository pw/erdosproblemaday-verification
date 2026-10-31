import Erdos684Lean
-- literal f(n) for n ≤ 60 from the formal uPart (compare with an independent Python table)
#eval (List.range 61).map fun n => (n, (List.range (n+1)).find? fun k => 1 ≤ k ∧ n^2 < Erdos684.uPart n k)
