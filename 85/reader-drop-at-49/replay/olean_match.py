#!/usr/bin/env python3
"""Compare our cold-replay .olean sha256 (steps.tsv, rc=0 rows) and source sha256 with the authors' accepted cold build
(attempt2-evidence/RUN.json: object_sha256, source_sha256). Byte-identical oleans = same elaboration output; a mismatch
is not by itself a defect (paths/toolchain can perturb oleans) but must be counted, not hidden. Exit 2 if nothing compared."""
import json, sys
from pathlib import Path
RUN = Path.home() / "MathDyad/subs-1019/85/dl/receipts/research/problems/erdos-85-wip-01/release_cold_build_20261011/attempt2-evidence/RUN.json"
STEPS = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/erdos85-1019/build/steps.tsv")
th = {}
for k, v in json.load(open(RUN))["completed"].items():
    th[k if k.startswith(("Proofs.", "Archive.")) else "Proofs." + k] = v
ours = {}
for line in STEPS.read_text().splitlines()[1:]:
    f = line.split("\t")
    if len(f) >= 6 and f[1] == "0":
        ours[f[0]] = (f[3], f[5])          # last rc=0 row wins
same = srcdiff = objdiff = missing = 0; diffs = []
for m, (src, obj) in ours.items():
    t = th.get(m)
    if t is None: missing += 1; diffs.append(("NOT-IN-THEIRS", m)); continue
    if t.get("source_sha256") != src: srcdiff += 1; diffs.append(("SRC", m)); continue
    if t.get("object_sha256") == obj: same += 1
    else: objdiff += 1; diffs.append(("OLEAN", m))
print(f"compared {len(ours)} completed modules (theirs: {len(th)}): olean identical {same}, olean differs {objdiff}, "
      f"source differs {srcdiff}, absent from their RUN.json {missing}")
for d in diffs[:30]: print(" ", *d)
sys.exit(2 if not ours else 0)
