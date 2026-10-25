import OAI.Combinatorics.Ramsey.CycleClique.MainTheorem
-- must FAIL: thm_main gives R(C_4,K_4) = 10, so it cannot prove 9
theorem wrong44 : (OAI.CycleClique.cycleCliqueRamsey (4:ℤ).toNat (4:ℤ).toNat : ℤ) = 9 :=
  OAI.CycleClique.thm_main.1 4 4 (by norm_num) (by norm_num) (by decide)
