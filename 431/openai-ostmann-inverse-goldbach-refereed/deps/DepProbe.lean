import Mathlib
/-!
Proof-term dependency probe (06:00Z erdos seat, 2026-10-23). `reach start target` walks `ConstantInfo.getUsedConstantsAsSet`
(types AND values, transitively — the same graph `#print axioms` walks) from `start` and reports whether `target` is reached,
with one path. A constant can be IMPORTED without being USED; this asks about use.
-/
open Lean

def reach (start target : Name) : CoreM (Option (List Name) × Nat) := do
  let env ← getEnv
  let mut parent : NameMap Name := {}
  let mut visited : NameHashSet := {}
  let mut queue : Array Name := #[start]
  let mut i := 0
  visited := visited.insert start
  let mut found := false
  while i < queue.size do
    let n := queue[i]!
    i := i + 1
    if n == target then
      found := true
      break
    if let some ci := env.find? n then
      for c in ci.getUsedConstantsAsSet do
        if !visited.contains c then
          visited := visited.insert c
          parent := parent.insert c n
          queue := queue.push c
  if !found then return (none, visited.size)
  let mut path : List Name := [target]
  let mut cur := target
  while cur != start do
    match parent.find? cur with
    | some p => path := p :: path; cur := p
    | none => break
  return (some path, visited.size)

def report (tag : String) (start target : Name) : CoreM Unit := do
  let env ← getEnv
  unless env.contains start do
    IO.println s!"@@@ {tag}: START NOT IN ENV {start}"; return
  unless env.contains target do
    IO.println s!"@@@ {tag}: TARGET NOT IN ENV {target}"; return
  let (p, n) ← reach start target
  match p with
  | some path => IO.println (s!"@@@ {tag}: REACHED (visited {n}) path length {path.length}:\n    " ++ String.intercalate "\n    " (path.map toString))
  | none => IO.println s!"@@@ {tag}: NOT REACHED (visited {n} constants)"
