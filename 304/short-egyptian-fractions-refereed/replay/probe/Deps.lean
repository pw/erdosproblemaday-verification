import OAI.NumberTheory.EgyptianFractions.Main
import OAI.NumberTheory.ShortEgyptian.Main
open Lean Meta in
#eval show MetaM Unit from do
  let env ← getEnv
  let roots : List Name := [`OAI.ShortEgyptian.main,
    `OAI.Problem337.egyptian_length_is_minimum, `OAI.Problem337.main_double_log_order,
    `OAI.Problem337.one_expansions_finite_and_bounded, `OAI.Problem337.counting_double_log_order,
    `OAI.Problem337.exact_marker_padding, `OAI.Problem337.every_exact_marker_occurs,
    `OAI.Problem337.quantitative_marked_length, `OAI.Problem337.missing_denominator_semantics,
    `OAI.Problem337.prescribed_denominator_corollary]
  for r in roots do
    let mut seen : NameSet := {}
    let mut stack : Array Name := #[r]
    let mut mods : NameSet := {}
    while h : stack.size > 0 do
      let c := stack.back
      stack := stack.pop
      if seen.contains c then continue
      seen := seen.insert c
      match env.getModuleIdxFor? c with
      | some idx =>
        let m := env.header.moduleNames[idx.toNat]!
        if (`OAI).isPrefixOf m then mods := mods.insert m
        if !(`OAI).isPrefixOf m then continue
      | none => pure ()
      match env.find? c with
      | some ci =>
        for d in ci.type.getUsedConstants do stack := stack.push d
        match ci.value? (allowOpaque := true) with
        | some v => for d in v.getUsedConstants do stack := stack.push d
        | none => pure ()
      | none => pure ()
    IO.println s!"@@ROOT {r} usesOAIModules={mods.size}"
    for m in mods.toList do IO.println s!"@@USE {r} {m}"
