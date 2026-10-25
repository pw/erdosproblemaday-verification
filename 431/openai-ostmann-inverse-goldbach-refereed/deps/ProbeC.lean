import OAI.NumberTheory.Ostmann.Complete
import DepProbe
open Lean
#eval show CoreM Unit from do
  let env ← getEnv
  let ns := [`OAI.Erdos970, `Erdos970, `OAI.LargePrimeGaps]
  -- count constants reachable from route C's two theorems in each namespace
  for start in [`OAI.Ostmann.inverseGoldbach, `OAI.Ostmann.twoInfiniteSummandsImpossible] do
    let mut visited : NameHashSet := {}
    let mut stack : Array Name := #[start]
    while !stack.isEmpty do
      let n := stack.back!
      stack := stack.pop
      if visited.contains n then continue
      visited := visited.insert n
      if let some ci := env.find? n then
        for c in ci.getUsedConstantsAsSet do
          if !visited.contains c then stack := stack.push c
    for p in ns do
      let k := visited.toList.filter (fun m => p.isPrefixOf m) |>.length
      IO.println s!"@@@ C {start}: reachable constants under {p}: {k} (of {visited.size})"
#eval report "C POSITIVE CONTROL inverseGoldbach -> publishedComplexZeroDensity" `OAI.Ostmann.inverseGoldbach `OAI.Ostmann.publishedComplexZeroDensity
