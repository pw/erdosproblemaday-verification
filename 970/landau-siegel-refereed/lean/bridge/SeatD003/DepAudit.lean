import SeatD003.ConstAudit

/-! Seat D: two more audit commands (Mathlib-only module).
* `#seatD_deps n`: walk the constants reachable from `n` through types AND values (incl. theorem
  proofs), expanding only constants declared in OAI.* / PrimeNumberTheoremAnd.* modules (Mathlib's own
  closure is trusted). Reports the foreign modules reached and every PrimeNumberTheoremAnd constant used.
* `#seatD_same n term`: elaborate `term` in the CURRENT environment and test whether it is
  syntactically (alpha-)equal to the stored value of definition `n`. -/

open Lean Elab Command Term Meta

namespace SeatD003

def foreignRoots : List Name := [`OAI, `PrimeNumberTheoremAnd, `ComparatorChallenges, `StrongPNT]

elab "#seatD_deps " id:ident : command => do
  let env ← getEnv
  let n := id.getId
  let some _ := env.find? n | throwError "unknown constant {n}"
  let mut seen : NameSet := {}
  let mut stack : List Name := [n]
  let mut mods : Std.HashMap Name Nat := {}
  let mut pnt : Array Name := #[]
  let mut nForeign : Nat := 0
  while true do
    match stack with
    | [] => break
    | c :: rest =>
      stack := rest
      if seen.contains c then continue
      seen := seen.insert c
      let m := modOf env c
      if foreignRoots.contains m.getRoot || c == n then
        nForeign := nForeign + 1
        mods := mods.insert m (mods.getD m 0 + 1)
        if m.getRoot == `PrimeNumberTheoremAnd then pnt := pnt.push c
        match env.find? c with
        | none => pure ()
        | some ci =>
          stack := ci.type.getUsedConstants.toList ++ stack
          match ci with
          | .defnInfo d => stack := d.value.getUsedConstants.toList ++ stack
          | .thmInfo t => stack := t.value.getUsedConstants.toList ++ stack
          | .opaqueInfo o => stack := o.value.getUsedConstants.toList ++ stack
          | .inductInfo i => stack := i.ctors ++ stack
          | .axiomInfo _ => logError m!"AXIOM reached: {c} [{m}]"
          | _ => pure ()
  let ml := (mods.toList.map fun (m, k) => s!"{m}:{k}").toArray.qsort (· < ·)
  logInfo m!"{n}: {nForeign} foreign-module constants reached (types+values incl. proofs) in {mods.size} modules:\n{String.intercalate "\n" ml.toList}"
  let pl := (pnt.map toString).qsort (· < ·)
  logInfo m!"PrimeNumberTheoremAnd constants used ({pnt.size}):\n{String.intercalate "\n" pl.toList}"

elab "#seatD_same " id:ident t:term : command => do
  let env ← getEnv
  let n := id.getId
  let some (.defnInfo d) := env.find? n | throwError "{n} is not a definition"
  let e ← liftTermElabM do
    let e ← elabTerm t (some (mkSort levelZero))
    synthesizeSyntheticMVarsNoPostponing
    instantiateMVars e
  if e.hasMVar then throwError "elaborated term still has metavariables"
  if e == d.value then
    logInfo m!"SAME: the text elaborates in this environment to an Expr identical to the stored value of {n}"
  else
    logError m!"DIFFERENT: the text elaborates to a different Expr than {n}'s stored value"

end SeatD003
