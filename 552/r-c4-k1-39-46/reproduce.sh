#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/2] Verify the frozen hostile-audit bundle"
test "$(sha256sum "$root/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "4d23d7b2278335fef1c0399ced2295b7ac8d2ff516f17a8e3ae6d2e4753a4706"
(cd "$root" && sha256sum --quiet -c MANIFEST.sha256)

echo "[2/2] Run the dependency-free exact checker"
python3 "$root/independent_verify_f39.py"

echo "PROBLEM 552 FINITE RAMSEY VALUE REPRODUCTION PASSED"
