#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/3] Verify frozen hashes"
(cd "$root" && sha256sum --quiet -c MANIFEST.sha256)

echo "[2/3] Verify under normal, -O, and -OO modes"
python3 "$root/verify_public_bundle.py" | diff -u "$root/logs/verify.log" -
python3 -O "$root/verify_public_bundle.py" | diff -u "$root/logs/verify.log" -
python3 -OO "$root/verify_public_bundle.py" | diff -u "$root/logs/verify.log" -

echo "[3/3] Run tracked-file and structural tamper matrices"
python3 "$root/audit_tamper_matrix.py" | diff -u "$root/logs/tamper_matrix.log" -

echo "PROBLEM 174 PUBLIC PACKAGE REPRODUCTION PASSED"
