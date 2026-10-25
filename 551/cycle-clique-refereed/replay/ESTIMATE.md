# #551 / OpenAI family 189 (cycle–clique Ramsey) — kernel replay ESTIMATE, written BEFORE CPU (21:00Z erdos seat, 2026-10-20 ~21:10Z, opus 5.5, Team seat 3/yt3)
Box 21:0xZ: load ~10 (two fresh claude -p seats + #552 cadicals x2, 35 d old — never evict); MemAvailable ~38 GB; disk 30 GB free after cache get.
Repo openai/math @ 1581d4cb, toolchain v4.34.1, Mathlib d13f23b7 (same as #505; .lake re-fetched by `lake exe cache get` 21:04–21:05Z).
Tree OAI/Combinatorics/Ramsey/CycleClique = 443 modules / 222.6 MB / 2.80 M lines. TWO routes:
  (A) comparator theorem OAI.CycleClique.thm_main (MainTheorem.lean) — import closure 182 modules / 28.3 MB / 43,320 `decide`, DAG depth 32;
  (B) Construction.* (261 modules / 194.3 MB, certificates per k = 5..17) behind Main.lean's cycle_clique_main_unconditional — NOT in (A)'s closure.
Source audit (whole tree): 0 axiom decl (1 hit is a docstring) / 0 sorry / 0 native_decide / 0 set_option / macro / elab / syntax / unsafe /
implemented_by / extern / opaque / #eval / ofReduceBool / maxHeartbeats / Lean.Meta / IO. 443,867 `decide` = kernel-evaluated certificates.
Plan: replay (A) only (B would be ~7x more source). DAG-parallel lean, W=3, nice 19, LEAN_NUM_THREADS=1, gate MemAvailable >= 27 GB (20 GB floor + ~7 GB/lean)
→ probes (#print axioms thm_main; pp.all statement match vs ComparatorChallenges/CycleCliqueRamsey.lean; sorry/mutated-statement controls)
→ leanchecker --fresh on OAI.Combinatorics.Ramsey.CycleClique.MainTheorem.
Extrapolation: #505 = 3.5 MB → 4,137 CPU-s ⇒ (A) 28.3 MB ≈ 33,000 CPU-s ≈ 9 CPU-h IF linear (decide cost may be worse) ⇒ ~3–5 h wall at 2–3 workers.
Abort/rethink if any single module > 10 GB RSS or > 1 h. Delete Mathlib .lake when banked.
