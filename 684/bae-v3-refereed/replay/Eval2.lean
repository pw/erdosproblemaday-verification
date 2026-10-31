import Erdos684Lean
-- literal f(n), one line per n, n ≤ 73 (the whole OEIS A392019 data range)
def fLit (n : Nat) : Nat := ((List.range (n+1)).find? fun k => 1 ≤ k ∧ n^2 < Erdos684.uPart n k).getD 0
#eval show IO Unit from do
  for n in List.range 74 do IO.println s!"{n} {fLit n}"
