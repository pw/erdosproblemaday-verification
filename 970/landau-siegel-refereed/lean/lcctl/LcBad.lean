import Lean
/-! Seat D: NEGATIVE control for leanchecker. Adds `SeatD003.bad : False := True.intro` with the kernel
type checker switched off, so the .olean carries an ill-typed theorem. leanchecker MUST reject it. -/
open Lean Elab Command
set_option debug.skipKernelTC true in
run_cmd liftCoreM do
  addDecl (.thmDecl { name := `SeatD003.bad, levelParams := [], type := mkConst ``False,
                      value := mkConst ``True.intro })
