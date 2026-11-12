# Lean replay of chy4pro/erdos-708-explicit-upper-bounds (commit dc150fd), on our machine — DONE, CLEAN

2026-11-12, 09:13Z → 12:08Z wall (with a restructure mid-run). Lean v4.34.0-rc1; Mathlib de5ce8a9 oleans from
`lake exe cache get`. All 180 Erdos708 modules compiled here from source (kernel-checked here). The 16 H97 numeric
certificate modules (Numeric{4..7}_{256,512}{Rows,}) were built one owner per module (build.sh / par.sh / coord.py,
then coord2.py, weight-budgeted: each *_512Rows module peaks at ~20–25 GB RSS). Then `lake build Erdos708.FinalCheck`
(8886 jobs, "Build completed successfully", 2150 s) and `lake env lean Erdos708/FinalCheck.lean`.

Results
- finalcheck.log is EMPTY (0 bytes) = every #guard_msgs axiom guard held (g_le_81n, g_le_33n, g_le_19n, g_le_12n,
  hinge97, reference_g_le_12/19, and the three H883 reduction steps).
- No "declaration uses 'sorry'" in any build log; axioms_printed.txt (every `#print axioms` emitted during the build)
  contains no sorryAx and no Lean.ofReduceBool; every listed declaration depends only on propext, Classical.choice,
  Quot.sound.
- Negative control: a copy of FinalCheck.lean with g_le_12n's expected list changed to [propext, Quot.sound] fails
  with rc 1 ("Docstring on `#guard_msgs` does not match", finalcheck_negative.log).
- steps.tsv records each module's completion (lane_/pre_/coord_/coord2_ rows; times in seconds where known).
Not done: `leanchecker --fresh` (Mathlib's own oleans are trusted from the cache, as in our other replays).
memguard.sh killed nothing (no memguard.log). One module (Numeric5_512Rows) was deliberately killed and rebuilt to
keep two 512-Rows modules from running at once.
