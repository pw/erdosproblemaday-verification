theorem x : False := by
  sorry
-- sorry in comment
/- axiom nested /- sorry -/ still -/
axiom foo : False
set_option debug.skipKernelTC true
def s := "sorry axiom"
@[implemented_by bar] def q := 1
unsafe def u := 1
