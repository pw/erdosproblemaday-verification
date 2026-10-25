#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

manifest_normal="$(python3 "$root/check_manifest.py")"
manifest_o="$(python3 -O "$root/check_manifest.py")"
manifest_oo="$(python3 -OO "$root/check_manifest.py")"
[[ "$manifest_normal" == "$manifest_o" ]]
[[ "$manifest_normal" == "$manifest_oo" ]]
printf '%s\n' "$manifest_normal"

proof_normal="$(python3 "$root/verify_convex_proof.py")"
proof_o="$(python3 -O "$root/verify_convex_proof.py")"
proof_oo="$(python3 -OO "$root/verify_convex_proof.py")"
[[ "$proof_normal" == "$proof_o" ]]
[[ "$proof_normal" == "$proof_oo" ]]
printf '%s\n' "$proof_normal"

tamper_normal="$(python3 "$root/tamper_tests.py")"
tamper_o="$(python3 -O "$root/tamper_tests.py")"
tamper_oo="$(python3 -OO "$root/tamper_tests.py")"
[[ "$tamper_normal" == "$tamper_o" ]]
[[ "$tamper_normal" == "$tamper_oo" ]]
printf '%s\n' "$tamper_normal"

echo "PROBLEM 132 CONVEX-POSITION PACKAGE PASSED"
