#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

(cd "$root/author" && ./reproduce.sh)

python3 -B "$root/hostile_audit/independent_audit.py" \
  --bundle "$root/author" \
  --online-sources "$root/hostile_audit/sources" \
  --summary "$tmp/verification_summary.json" >/dev/null
cmp "$tmp/verification_summary.json" \
  "$root/hostile_audit/verification_summary.json"

python3 -B "$root/hostile_audit/summarize_solver_runs.py" \
  --runs "$root/hostile_audit/solver_runs" \
  --out "$tmp/solver_summary.json" >/dev/null
cmp "$tmp/solver_summary.json" "$root/hostile_audit/solver_summary.json"

(cd "$root/hostile_audit" && sha256sum -c AUDIT_SHA256SUMS)
echo "PASS: Problem 168 author bundle and hostile audit verified"
