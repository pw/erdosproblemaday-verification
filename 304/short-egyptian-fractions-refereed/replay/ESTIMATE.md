# Family 25 (Short Egyptian fractions; Erdős #304/#148/#293) — replay estimate, 18:0xZ erdos seat 2026-10-21
- Closure: 348 OAI modules (290 EgyptianFractions + 58 ShortEgyptian), 44,201 lines, external = Mathlib only (rev d13f23b, toolchain v4.34.1 — same as #416/#968).
- Mathlib: /tmp/erdos0300/lean/mathlib4 (source at d13f23b, .lake deleted 13:4xZ) -> `lake exe cache get` ~7 GB disk, ~5–10 min.
- Build: drive.py (DAG-parallel, lake-free), W=4, gate MemAvailable >= 18 GB. #505 (269 modules) took 29 min at W=4, peak 6.7 GiB/process -> expect 30–60 min, peak RSS <= 4 x 8 GB.
- Box at start: load 3.0, MemAvailable 38 GB, disk 37 GB free, two #552 cadicals (1.2 GB each, 37 d old) — not touched.
- leanchecker --fresh over both closures afterwards: ~1 h single process, ~9 GB.
- After everything is banked: delete Mathlib .lake again (LAKE_DELETED.txt).
