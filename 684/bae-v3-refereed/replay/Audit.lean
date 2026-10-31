import Erdos684Lean
-- erdos cron seat 2026-10-31: our own audit of jidodat/erdos684-lean @ v3-arxiv
#print axioms Erdos684.main_theorem_unconditional
#print axioms Erdos684.unbounded_unconditional
#print axioms Erdos684.main_theorem_limsup
#print axioms Erdos684.main_theorem
#print axioms Erdos684.pntHyp
#check @Erdos684.main_theorem_unconditional
#check @Erdos684.unbounded_unconditional
#check @Erdos684.main_theorem_limsup
#check @Erdos684.fThr_eq_top_iff
#check @Erdos684.lt_fThr_iff
#check @Erdos684.uPart_mul_eq_choose
#print Erdos684.fThr
#print Erdos684.uPart
#print Nat.primesLE
#print Erdos684.PNTHyp
-- negative control: the instrument must be able to print sorryAx
theorem audit_ctl_sorry : (1 : Nat) = 2 := by sorry
#print axioms audit_ctl_sorry
