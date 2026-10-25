#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

echo "[1/7] Verify exact hostile-audit manifest coverage, hashes, and metadata"
python3 "$root/check_audit_manifest.py"

echo "[2/7] Verify the frozen author directory and archive"
python3 "$root/check_author_freeze.py"

echo "[3/7] Run the clean-room proof checker in normal, -O, and -OO modes"
independent_normal="$(python3 "$root/independent_q9_audit.py")"
independent_o="$(python3 -O "$root/independent_q9_audit.py")"
independent_oo="$(python3 -OO "$root/independent_q9_audit.py")"
[[ "$independent_normal" == "$independent_o" ]]
[[ "$independent_normal" == "$independent_oo" ]]
printf '%s\n' "$independent_normal"

author_suite() {
  local -a python_command=("$@")
  "${python_command[@]}" "$root/author_bundle/verify_q9_witness.py" \
    "$root/author_bundle/q9_edges_1531.json" 1531
  "${python_command[@]}" "$root/author_bundle/verify_q9_witness.py" \
    "$root/author_bundle/provenance/q9_edges_1531_raw.json" 1531
  "${python_command[@]}" "$root/author_bundle/audit_negative_controls.py"
  "${python_command[@]}" "$root/author_bundle/check_canonical_identity.py"
  "${python_command[@]}" "$root/author_bundle/compare_frontiers.py"
  "${python_command[@]}" "$root/author_bundle/compare_edge_sets.py" \
    "$root/author_bundle/q9_edges_1531.json" \
    "$root/author_bundle/provenance/q9_edges_1531_raw.json"
}

echo "[4/7] Run every author checker in normal, -O, and -OO modes"
author_normal="$(author_suite python3)"
author_o="$(author_suite python3 -O)"
author_oo="$(author_suite python3 -OO)"
[[ "$author_normal" == "$author_o" ]]
[[ "$author_normal" == "$author_oo" ]]
printf '%s\n' "$author_normal"

echo "[5/7] Run hostile author-verifier tamper controls in every mode"
tamper_normal="$(python3 "$root/author_tamper_audit.py")"
tamper_o="$(python3 -O "$root/author_tamper_audit.py")"
tamper_oo="$(python3 -OO "$root/author_tamper_audit.py")"
[[ "$tamper_normal" == "$tamper_o" ]]
[[ "$tamper_normal" == "$tamper_oo" ]]
printf '%s\n' "$tamper_normal"

echo "[6/7] Recheck dated external evidence and the prepublication site capture"
python3 "$root/check_external_evidence.py"

echo "[7/7] Run the complete frozen author reproduction"
"$root/author_bundle/reproduce.sh"

echo "HOSTILE_AUDIT_RECHECK_PASS lower_bound=1531"
