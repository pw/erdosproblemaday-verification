# #505 / OpenAI family 156 (Borsuk dim 9) — kernel replay ESTIMATE, written BEFORE CPU (18:00Z erdos seat, 2026-10-20 ~18:25Z, opus 5.5, Team seat 3/yt3)
Box 18:2xZ: load ~5.7; #552 cadicals x2 (2.3 GB, 35 d old — never evict); MemAvailable ~38 GB; disk 38 GB free.
Repo openai/math @ 1581d4cb (2026-10-12), toolchain v4.34.1, Mathlib d13f23b7 (same as #138/#184/#986; its .lake was deleted 10-20 09:5xZ).
Tree: OAI/Geometry/Borsuk = 269 modules / 78,964 lines, every module `import Mathlib` + internal only (no other OAI dirs).
Source audit: 0 axiom / sorry / native_decide / set_option / macro / elab / syntax / unsafe / implemented_by / extern / opaque / #eval / IO /
Lean.Meta / ofReduceBool / maxHeartbeats. 13,197 lines with `decide` = 19,594 `by decide` calls (19,574 in FiniteCases/, 145 files / 66k lines) [corrected after blind read] = kernel-evaluated
finite case analysis — the cost risk.
Plan: cache get (~7.1 GB → disk ~31 GB, guard ≥30 OK) → DAG-parallel lean, 3 workers, nice 19, LEAN_NUM_THREADS=1, gate MemAvailable ≥ 26 GB
(~6 GB/lean) → probes (#print axioms on main_theorem + euclidean_nine_counterexample; pp.all statement match vs ComparatorChallenges/BorsukNine.lean;
sorry/mutated-statement controls) → leanchecker --fresh on OAI.Geometry.Borsuk.Main (≤16 GB, ~1 h on prior trees).
Expected wall: build 30–90 min (decide-heavy tail unknown), leanchecker ~1 h. Delete Mathlib .lake when banked.
