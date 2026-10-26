import Mathlib

/-! Seat D: a constant-provenance audit command (Mathlib-only module).
`#seatD_audit n` lists the constants directly used by `n`'s type and value, with the module that
declared each, then follows the transitive closure through types, definition bodies, and inductive
constructors (theorem PROOFS are not followed: a proof cannot change what a statement means) and
reports how many reachable constants come from each module root. Any root outside the
Mathlib dependency family is printed as an ERROR line `FOREIGN`. -/

open Lean Elab Command

namespace SeatD003

def reachable (env : Environment) (start : Array Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut stack : List Name := start.toList
  while true do
    match stack with
    | [] => break
    | c :: rest =>
      stack := rest
      if seen.contains c then continue
      seen := seen.insert c
      match env.find? c with
      | none => pure ()
      | some ci =>
        stack := ci.type.getUsedConstants.toList ++ stack
        match ci with
        | .defnInfo d => stack := d.value.getUsedConstants.toList ++ stack
        | .inductInfo i => stack := i.ctors ++ stack
        | _ => pure ()
  return seen

def modOf (env : Environment) (c : Name) : Name :=
  match env.getModuleIdxFor? c with
  | some i => env.header.moduleNames[i.toNat]!
  | none => `«<this file>»

def allowedRoots : List Name :=
  [`Init, `Std, `Lean, `Mathlib, `Batteries, `Aesop, `Qq, `ProofWidgets, `Plausible,
   `ImportGraph, `LeanSearchClient, `Cli, `SeatD003]

elab "#seatD_audit " id:ident : command => do
  let env ← getEnv
  let n := id.getId
  let some ci := env.find? n | throwError "unknown constant {n}"
  let direct := (ci.type.getUsedConstants ++ (match ci with
      | .defnInfo d => d.value.getUsedConstants | _ => #[])).toList.eraseDups
  let lines := direct.map fun c => s!"  {c}  [{modOf env c}]"
  logInfo m!"{n} declared in [{modOf env n}]; {direct.length} constants used directly:\n{String.intercalate "\n" lines}"
  let s := reachable env #[n]
  let mut roots : Std.HashMap Name Nat := {}
  let mut foreign : Array String := #[]
  for c in s.toList do
    let m := modOf env c
    let r := if m == `«<this file>» then `«<this file>» else m.getRoot
    roots := roots.insert r (roots.getD r 0 + 1)
    if !(allowedRoots.contains r) && r != `«<this file>» then
      foreign := foreign.push s!"{c} [{m}]"
  let rl := roots.toList.map fun (r, k) => s!"{r}:{k}"
  logInfo m!"{n}: {s.size} constants reachable (types + def bodies + ctors); by module root: {rl}"
  if foreign.isEmpty then
    logInfo m!"AUDIT CLEAN: no reachable constant outside {allowedRoots}"
  else
    logError m!"FOREIGN ({foreign.size}): {foreign.toList.take 40}"

end SeatD003
