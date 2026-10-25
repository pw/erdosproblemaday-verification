import OAI.NumberTheory.ShortEgyptian.Main
open Lean Meta in
#eval show MetaM Unit from do
  let env ← getEnv
  let ci := (env.find? `OAI.ShortEgyptian.main).get!
  IO.println s!"kind thm? {ci.isThm} hasValue {ci.value?.isSome} {ci.value? (allowOpaque := true) |>.isSome}"
  match ci.value? (allowOpaque := true) with
  | some v => IO.println s!"{v.getUsedConstants.toList.take 30}"
  | none => pure ()
