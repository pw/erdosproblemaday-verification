import OAI.NumberTheory.JointDickman.PaperMain
-- Kernel dependency walk from OpenAI's comparator theorems: which non-Mathlib modules and which "published input"
-- propositions the PROOF TERMS actually reach (types + values, opaque included). Stops at Mathlib/Lean/Batteries.
open Lean Meta in
#eval show MetaM Unit from do
  let env ← getEnv
  let ours : Name → Bool := fun m => (`OAI).isPrefixOf m || (`PrimeNumberTheoremAnd).isPrefixOf m ||
    (`StrongPNT).isPrefixOf m || (`Architect).isPrefixOf m
  let roots : List Name := [`OAI.JointDickmanPaper.joint_law, `OAI.JointDickmanPaper.increasing_order,
    `OAI.JointDickmanPaper.decreasing_order]
  for r in roots do
    let mut seen : NameSet := {}
    let mut stack : Array Name := #[r]
    let mut mods : NameSet := {}
    let mut inputs : NameSet := {}
    let mut nconst : Nat := 0
    while h : stack.size > 0 do
      let c := stack.back
      stack := stack.pop
      if seen.contains c then continue
      seen := seen.insert c
      match env.getModuleIdxFor? c with
      | some idx =>
        let m := env.header.moduleNames[idx.toNat]!
        if !(ours m) then continue
        mods := mods.insert m
      | none => pure ()
      nconst := nconst + 1
      let s := c.toString
      if (s.splitOn "Input").length > 1 || (s.splitOn "Published").length > 1 then inputs := inputs.insert c
      match env.find? c with
      | some ci =>
        for d in ci.type.getUsedConstants do stack := stack.push d
        match ci.value? (allowOpaque := true) with
        | some v => for d in v.getUsedConstants do stack := stack.push d
        | none => pure ()
      | none => pure ()
    IO.println s!"@@ROOT {r} nonMathlibConstants={nconst} modules={mods.size} inputNamed={inputs.size}"
    for m in mods.toList do IO.println s!"@@MOD {r} {m}"
    for c in inputs.toList do
      let mut ty := "?"
      if let some ci := env.find? c then
        ty := toString (← ppExpr ci.type)
      IO.println s!"@@INPUT {r} {c} : {(ty.replace "\n" " ").take 300}"
