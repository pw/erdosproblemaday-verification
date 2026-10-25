#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
author="$root/author"
audit="$root/hostile_audit"
build="$(mktemp -d)"
trap 'find "$build" -depth -delete' EXIT
export PYTHONDONTWRITEBYTECODE=1

echo "[1/5] Verify frozen manifests"
test "$(sha256sum "$author/SHA256SUMS" | cut -d' ' -f1)" = \
  "2878fa5ec38e7d52e056883f53dfbeb72c72a200ec6eb133402cbf620d890e3c"
test "$(sha256sum "$audit/AUDIT_SHA256SUMS" | cut -d' ' -f1)" = \
  "c149fc744c9eb44cde6db76d62573ebe70beb4c0bb25b65331336704c7696f52"
(cd "$author" && sha256sum -c SHA256SUMS)
test "$(grep -c ' \./public_upstream_current/' "$audit/AUDIT_SHA256SUMS")" = 52
grep -v ' \./public_upstream_current/' "$audit/AUDIT_SHA256SUMS" \
  > "$build/audit-public-manifest.sha256"
(cd "$audit" && sha256sum -c "$build/audit-public-manifest.sha256")

echo "[2/5] Rerun author verification and deterministic generation"
"$author/reproduce.sh"

echo "[3/5] Run the independent strict graph audit"
python3 "$audit/verify_q9_independent.py"

echo "[4/5] Check JSON/text consistency and the public comparison"
python3 "$audit/check_bundle_consistency.py"
cmp "$audit/candidate_q9_1506.json" "$author/q9_edges_1506.json"
cmp "$audit/public_q9_1505.json" \
  "$author/q9_upstream/q9_edges_repair_from1503_iter2.json"

echo "[5/5] Run the controlled C4 negative test"
python3 "$audit/negative_mutation_test.py"

echo "PROBLEM 86 Q9-1506 REPRODUCTION PASSED"
