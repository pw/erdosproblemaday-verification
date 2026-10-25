#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
author="$root/author"
audit="$root/hostile_audit"
build="$(mktemp -d)"
trap 'find "$build" -depth -delete' EXIT
export PYTHONDONTWRITEBYTECODE=1

echo "[1/6] Verify frozen manifests"
test "$(sha256sum "$author/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "527f91bb0b9388cee3fabd49c0781d7292a8ebda720aba189469bcf158152622"
test "$(sha256sum "$audit/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "d2bcfd35f48d701daec2d3bb057ccb0f81fc132603a1fbc50cadc3338e57ab30"
test "$(grep -c ' \./site_snapshot/' "$author/MANIFEST.sha256")" = 2
grep -v ' \./site_snapshot/' "$author/MANIFEST.sha256" \
  > "$build/author-public-manifest.sha256"
(cd "$author" && sha256sum -c "$build/author-public-manifest.sha256")
(cd "$audit" && sha256sum -c MANIFEST.sha256)

echo "[2/6] Compile both scanners from source"
g++ -std=c++17 -O2 -fopenmp -Wall -Wextra \
  "$author/sum2sq_gap_scan.cpp" -o "$build/primary_audit"
g++ -std=c++17 -O2 -fopenmp -Wall -Wextra \
  "$author/sum2sq_gap_scan_independent.cpp" -o "$build/independent_audit"

echo "[3/6] Cross-check scanners against the factor criterion"
cp "$audit/scanner_harness.py" "$build/scanner_harness.py"
(cd "$build" && python3 scanner_harness.py) | tee "$build/scanner_harness.out"
sed -n '1,5p' "$audit/scanner_harness.log" > "$build/scanner_harness.expected"
cmp "$build/scanner_harness.out" "$build/scanner_harness.expected"

echo "[4/6] Verify every frozen full-range summary"
python3 "$author/verify_frozen_outputs.py"
python3 "$audit/verify_full_scan.py"

echo "[5/6] Verify the explicit 111-integer obstruction"
python3 "$author/verify_gap_certificate.py"
(cd "$author" && gp -q verify_gap_certificate.gp)

echo "[6/6] Regenerate the obstruction independently"
gp -q "$audit/regenerate_certificate.gp" > "$build/regenerated.cert"
cmp "$build/regenerated.cert" \
  "$author/gap_133858454292_133858454404.cert"

if [[ "${FULL:-0}" == 1 ]]; then
  echo "[full] Recompute every sum of two squares through 200 billion"
  OMP_NUM_THREADS="${OMP_NUM_THREADS:-14}" "$build/primary_audit" \
    0 200000000000 73456789 108 > "$build/full.out" 2> "$build/full.err"
  cmp "$build/full.out" "$audit/full_scan_0_200b_width73456789.out"
fi

echo "PROBLEM 222 RECORD-GAP-112 REPRODUCTION PASSED"
