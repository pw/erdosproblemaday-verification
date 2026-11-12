# Lean replay of chy4pro/erdos-708-explicit-upper-bounds (commit dc150fd), on our machine

Status at publication (2026-11-12 ~10:15Z): IN PROGRESS. Mathlib de5ce8a9 oleans from `lake exe cache get`;
every Erdos708 module compiled here from source with Lean v4.34.0-rc1. The 16 H97 numeric certificate modules
(Numeric{4..7}_{256,512}{Rows,}) are built one owner per module (coord2.py), weight-budgeted because each
*_512Rows module peaks at ~20–25 GB RSS (Chen's CI used 24 GB swap and built them one at a time).
Then `lake build Erdos708.FinalCheck` and `lake env lean Erdos708/FinalCheck.lean` (success = no output).
steps.tsv records every module as it lands; this file and the page are updated when the run ends.
memguard.sh kills the build's process group if MemAvailable < 14 GB (protects long-running solvers on the box).
