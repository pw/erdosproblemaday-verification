# Family 172 (Euclidean Ramsey classification; Erdős #174) — replay estimate, 21:00Z erdos seat 2026-10-21
- Closure: 65 OAI modules (47 EuclideanRamsey + 18 SphericalRamsey), 9,589 lines, external = Mathlib only (rev d13f23b, toolchain v4.34.1 — same as #304/#416/#968).
- Mathlib: /tmp/erdos0300/lean/mathlib4 (.lake deleted 19:3xZ) -> `lake exe cache get` ~7 GB disk, ~5–10 min.
- Build: drive.py (DAG-parallel, lake-free), W=4, gate MemAvailable >= 18 GB. Expect 10–30 min, peak RSS <= 4 x 8 GB.
- Box at start: load 3.3, MemAvailable 38 GB, disk 37 GB free, two #552 cadicals (37 d old) — not touched.
- leanchecker --fresh over the closure afterwards: ~1 h single process, ~9 GB.
- After everything is banked: delete Mathlib .lake again (LAKE_DELETED.txt).
