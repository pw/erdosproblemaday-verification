# #138 / OpenAI family 160 — kernel replay estimate, WRITTEN BEFORE CPU (06:00Z erdos seat, 2026-10-15 06:1xZ)
Solution: lean/OAI/Combinatorics/ProgressionColoring/ — 115 modules, 14,837 lines, imports Mathlib only (+ Lean.Elab.Tactic.Omega, core).
Comparator: ComparatorChallenges/QuantitativeVanDerWaerden.lean (theorem OAI.QuantitativeVanDerWaerden.uniform_lower_bound; .json: solution_module Main, permitted axioms propext/Quot.sound/Classical.choice, enable_nanoda false).
Repo rev 1581d4c (sparse clone reused from /tmp/oaimath/604); the ProgressionColoring path is unchanged since adc7f12 (the commit Formal Conjectures cites). Mathlib d13f23b7 = v4.34.1 at /tmp/erdos0300/lean/mathlib4 (.lake deleted 10-14; cache get relaunched 06:08:42Z).
Reference points: #604 48 modules / 14,207 lines → build 508 s; #508 70 modules → 1,263 s; #90 40 modules / 28k lines → 1,275 s.
ESTIMATE: cache get 2–4 min / ~7 GB disk (54 GB free after pruning /tmp/claude-1000); build of 115 modules at ONE thread nice 19 ≈ 15–40 min wall, ≤ 8 GB RSS; probes minutes; leanchecker --fresh over the Mathlib closure ≈ 1–1.5 h (#604: 3,462 s; #508: 3,765 s).
Memory guard: every lean waits for MemAvailable ≥ 28 GB (box: 37 GB available at 06:00Z with #789 (15,6) at 11 GB, #552 cadicals, #757). Disk guard: ≥ 30 GB before cache get (54 GB). Delete /tmp/erdos0300/lean/mathlib4/.lake when the replay is banked.
Nothing else of mine runs on the box this tick (no SAT campaign: #1159 q=13 finer cubes deferred while #552 runs).
build launched 2026-10-15T06:15:53Z
relaunch after smoke-import fix 2026-10-15T06:19:38Z
