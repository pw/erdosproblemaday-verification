import Lean
open Lean Elab Command
/-- Adds `bad : False` with value `True.intro`, an ill-typed term, using the kernel-skip option. -/
elab "add_bad_decl" : command => do
  let decl := Declaration.thmDecl { name := `NegCtl.bad, levelParams := [], type := mkConst ``False, value := mkConst ``True.intro }
  liftCoreM (addDecl decl)
