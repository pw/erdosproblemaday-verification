#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/6] Verify frozen hashes"
(cd "$root" && sha256sum --quiet -c SHA256SUMS)

echo "[2/6] Verify the canonical witness in every Python optimization mode"
for optimization in normal O OO; do
  case "$optimization" in
    normal) command=(python3) ;;
    O) command=(python3 -O) ;;
    OO) command=(python3 -OO) ;;
  esac
  "${command[@]}" "$root/verify_q9_witness.py" "$root/q9_edges_1531.json" 1531 \
    | diff -u "$root/logs/verify_q9_witness.log" -
done

echo "[3/6] Verify the preserved raw generator output"
python3 "$root/verify_q9_witness.py" "$root/provenance/q9_edges_1531_raw.json" 1531 \
  | diff -u "$root/logs/verify_q9_raw.log" -

echo "[4/6] Run verifier negative controls in every optimization mode"
python3 "$root/audit_negative_controls.py"
python3 -O "$root/audit_negative_controls.py"
python3 -OO "$root/audit_negative_controls.py"

echo "[5/6] Check canonical/raw identity and predecessor comparisons"
python3 "$root/check_canonical_identity.py"
python3 "$root/compare_frontiers.py" \
  | diff -u "$root/logs/compare_frontiers.log" -

echo "[6/6] Rebuild the heuristic and reproduce its known 1505-to-1506 control"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -std=c++20 -O3 -Wall -Wextra -Wshadow -Wconversion -pedantic -fopenmp \
  "$root/generator/q9_min_conflicts.cpp" -o "$tmp/q9_min_conflicts"
OMP_NUM_THREADS=1 "$tmp/q9_min_conflicts" \
  "$root/provenance/q9_public_1505.json" "$tmp/q9_1506.json" 1 1000000 1
python3 "$root/verify_q9_witness.py" "$tmp/q9_1506.json" 1506 >/dev/null
python3 "$root/compare_edge_sets.py" \
  "$tmp/q9_1506.json" "$root/provenance/q9_edges_1506.json"

echo "PROBLEM 86 Q9=1531 REPRODUCTION PASSED"
