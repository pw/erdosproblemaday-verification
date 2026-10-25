# Family 28 (Gaussian moat; Erdős #952) — replay estimate, 00:00Z erdos seat 2026-10-22
- Closure: 41 OAI modules (OAI/NumberTheory/GaussianMoat), 12,703 lines, external = Mathlib only (rev d13f23b, toolchain v4.34.1 — same as #174/#304/#416/#968).
- Mathlib: /tmp/erdos0300/lean/mathlib4 (.lake deleted after #174) -> `lake exe cache get` ~7 GB disk, ~5–10 min. Disk at start 37 GB free (rule: >= 30).
- Build: drive.py (DAG-parallel, lake-free), W=4, gate MemAvailable >= 18 GB. Expect 10–40 min, peak RSS <= 4 x 8 GB.
- Box at start: load ~6, MemAvailable 40 GB, two #552 cadicals (37 d old, ~1.2 GB each) — not touched.
- leanchecker --fresh over the closure afterwards: ~1 h single process, ~9 GB.
- After everything is banked: delete Mathlib .lake again.
