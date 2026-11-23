import Erdos301
open Lean

/-- Every constant reachable from `root` through types and values (theorem bodies included). -/
partial def reach (env : Environment) (root : Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut stack : Array Name := #[root]
  while !stack.isEmpty do
    let n := stack.back!
    stack := stack.pop
    if seen.contains n then continue
    seen := seen.insert n
    match env.find? n with
    | none => pure ()
    | some ci =>
      for c in ci.type.getUsedConstants do stack := stack.push c
      if let some v := ci.value? (allowOpaque := true) then
        for c in v.getUsedConstants do stack := stack.push c
  return seen

#eval show CoreM Unit from do
  let env ← getEnv
  let s := reach env ``Erdos301.Analytic.erdos301Conclusion_unconditional
  let all := s.toList
  let mertens := all.filter (fun n => (`Mertens).isPrefixOf n)
  let e327 := all.filter (fun n => (`Erdos327).isPrefixOf n)
  let e301 := all.filter (fun n => (`Erdos301).isPrefixOf n)
  IO.println s!"total reachable constants: {all.length}"
  IO.println s!"Erdos301.*: {e301.length}  Erdos327.*: {e327.length}  Mertens.*: {mertens.length}"
  let ms := (mertens.map toString).toArray.qsort (· < ·)
  IO.println s!"Mertens.* reached: {ms.toList.take 40}"
  -- which module does each Mertens constant come from?
  let mods := (mertens.filterMap fun n => env.getModuleIdxFor? n |>.map fun i => env.header.moduleNames[i.toNat]!).eraseDups
  IO.println s!"modules of Mertens.* constants: {mods}"
  -- any reachable constant that is an axiom?
  let axs := all.filter fun n => match env.find? n with | some (.axiomInfo _) => true | _ => false
  IO.println s!"axioms reachable: {axs}"
  -- any reachable opaque / unsafe / partial?
  let odd := all.filter fun n => match env.find? n with
    | some (.opaqueInfo _) => true
    | some ci => ci.isUnsafe || ci.isPartial
    | none => false
  IO.println s!"opaque/unsafe/partial reachable: {odd.length}"
  let kinds := odd.map fun n => match env.find? n with
    | some (.opaqueInfo _) => "opaque" | some ci => if ci.isUnsafe then "unsafe" else "partial" | none => "?"
  IO.println s!"kinds: {kinds.eraseDups}"
  let omods := (odd.filterMap fun n => env.getModuleIdxFor? n |>.map fun i => env.header.moduleNames[i.toNat]!).eraseDups
  IO.println s!"modules of opaque constants: {omods}"
  let ours := odd.filter fun n => match env.getModuleIdxFor? n with
    | some i => let m := env.header.moduleNames[i.toNat]!; (`Erdos301).isPrefixOf m || (`Erdos327).isPrefixOf m || m == `Mathlib.NumberTheory.Mertens || m == `Mathlib.Analysis.SpecialFunctions.Gamma.Deriv || m == `Mathlib.NumberTheory.Harmonic.GammaDeriv || m == `Mathlib.NumberTheory.SumPrimeReciprocals
    | none => true
  IO.println s!"opaque constants from non-upstream modules: {ours}"
  -- constants reached from the 4 fork-modified upstream files
  let forkmods := [`Mathlib.Analysis.SpecialFunctions.Gamma.Deriv, `Mathlib.NumberTheory.Harmonic.GammaDeriv, `Mathlib.NumberTheory.SumPrimeReciprocals]
  for fm in forkmods do
    let cs := all.filter fun n => match env.getModuleIdxFor? n with
      | some i => env.header.moduleNames[i.toNat]! == fm | none => false
    IO.println s!"{fm}: {cs.length} reached: {cs.take 12}"
