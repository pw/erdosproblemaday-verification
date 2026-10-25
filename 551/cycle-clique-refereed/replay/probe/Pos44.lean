import OAI.Combinatorics.Ramsey.CycleClique.MainTheorem
-- POSITIVE control for TypeCtl: the same term at the right value must elaborate
theorem right44 : (OAI.CycleClique.cycleCliqueRamsey (4:ℤ).toNat (4:ℤ).toNat : ℤ) = (4 - 1) * (4 - 1) + 1 :=
  OAI.CycleClique.thm_main.1 4 4 (by norm_num) (by norm_num) (by decide)
