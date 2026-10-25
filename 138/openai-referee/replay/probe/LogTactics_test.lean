import Mathlib.Data.Nat.Log
import Mathlib.Tactic.NormNum
example : Nat.log 2 2 = 1 := by decide
example : Nat.log 2 2 = 1 := by norm_num
example : Nat.log 2 2 = 1 := by simp
example : Nat.log 2 2 = 1 := by simpa using Nat.log_pow (b := 2) (x := 1) (by norm_num)
example : Nat.log 2 2 = 1 := Nat.log_self (by norm_num)
