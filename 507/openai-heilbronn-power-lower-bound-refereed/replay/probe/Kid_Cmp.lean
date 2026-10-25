import ComparatorChallenges.HeilbronnTriangle
open Lean Meta in
#eval show MetaM Unit from do
  for nm in [``OAI.Problem355.heilbronnK, ``OAI.Problem355.heilbronnT, ``OAI.Problem355.heilbronnM, ``OAI.Problem355.heilbronnExponent] do
    let ci ← getConstInfo nm
    match ci with
    | .defnInfo d =>
      let h := match d.hints with
        | .opaque => "opaque" | .abbrev => "abbrev" | .regular n => s!"regular {n}"
      let st ← getReducibilityStatus nm
      IO.println s!"@@KID {nm} kernel_hints={h} value_hash={d.value.hash} type_hash={d.type.hash} safety={repr d.safety} elab_status={repr st}"
    | _ => IO.println s!"@@KID {nm} NOT A DEF"
