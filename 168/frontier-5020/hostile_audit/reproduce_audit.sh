#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
bundle=/home/exedev/erdos_scratch/frozen_erdos168_20260811

python3 -B "$root/independent_audit.py" \
  --bundle "$bundle" \
  --online-sources "$root/sources" \
  --summary "$root/verification_summary.json" >/dev/null

python3 -B "$root/summarize_solver_runs.py" \
  --runs "$root/solver_runs" \
  --out "$root/solver_summary.json" >/dev/null

(cd "$root" && sha256sum -c AUDIT_SHA256SUMS)
echo "PASS: independent Problem 168 audit artifacts verified"
