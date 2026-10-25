# #986 / OpenAI family 170 — kernel replay, ESTIMATE WRITTEN BEFORE CPU (12:00Z erdos seat, 2026-10-20 ~12:20Z, opus 5.5, Team seat 3/yt3)
Box at 12:15Z: load ~5; #552 cadicals ×2 (2.3 GB, 35 days old — never evict); several interactive claude sessions; MemAvailable ~39 GB;
disk 39 GB → ~32 GB after Mathlib d13f23b7 cache get (7.1 GB, done 12:07Z, 8,529 oleans).
Tree: 858 modules / 123,565 lines (RamseyFive closure 482, SharpRamsey closure 408, 32 shared), every module `import Mathlib` + internal only.
Source audit (this seat, 12:1xZ): 0 axiom / set_option / macro / elab / syntax / Lean.Meta / #eval / IO / extern / implemented_by / unsafe /
native_decide / opaque; sorry only in the two ComparatorChallenges files (expected). 76 kernel `decide`s. ⇒ GO.
Build: DAG-parallel, 3 workers, nice 19 / ionice idle-ish, LEAN_NUM_THREADS=1, launch gate MemAvailable ≥ 26 GB (≈6 GB per lean ⇒ ≥ 20 GB
left after). Per-module 4–15 s typical on #138/#184 (Mathlib import dominates) ⇒ 858 × ~10 s / 3 ≈ 50 min; tail risk: a few heavy files
(several minutes each). Then probes (axioms --trust=0, statement match ×2, wrong-shape ×2, planted-sorry), then leanchecker --fresh on both
Mains (≈ 1 h each on prior trees; sequential, ≤ 16 GB). Disk +~1 GB oleans. Delete Mathlib .lake when banked.
