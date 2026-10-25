theorem t : True := by sorry
example : True := by admit
axiom foo : False
example : 2=2 := by native_decide
@[implemented_by x] def y := 1
@[extern "c"] def z : Nat := 1
unsafe def u := 1
opaque o : Nat
partial def p : Nat := p
set_option debug.skipKernelTC true
syntax "x" : term
attribute [-instance] foo in
-- sorry in a comment must NOT count
/- axiom in a block comment must not count -/
example := Lean.ofReduceBool
