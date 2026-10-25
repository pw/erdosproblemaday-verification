# #970 (OpenAI family 21) kernel replay — estimate written BEFORE launch (00:1xZ 2026-10-23, 00:00Z erdos seat)
- Closure: 850 modules (OAI 819 = all of OAI/NumberTheory/Jacobsthal, PNT+ Erdos970 19, StrongPNT Erdos970 7, AbsorptionCutoff 5) + 2 comparator modules built after.
- Reference run: #416 (family 24, 829 modules, PNT+) took 31 min wall at W=5, sum of per-module wall 7,562 s, max RSS 7.39 GB.
- Plan: W=3, GATE=20 GB MemAvailable before each launch, nice 19 / ionice idle-ish. Worst case 3 × 7.4 = 22 GB on top of the #552 cadicals (2.3 GB, 38 days old) — box had 38 GB available at launch ⇒ ≥ 16 GB left, above earlyoom's 10% floor.
- Expected: 45–90 min wall, ~2–3 CPU-h. Outputs: oleans ~1–2 GB in out/ (disk 25 GB free after cache get).
- Then post.sh: comparator modules (Jacobsthal, JacobsthalImproved), pp.all probes, --trust=0 axioms, sorry negative control, statement match; then leanchecker --fresh on Main (1 process, ~1 h, ~8 GB).
- After everything is banked: rm -rf /tmp/erdos0300/lean/mathlib4/.lake (7 GB) per the disk guard.
