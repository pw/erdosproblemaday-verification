#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
author="$root/author"
audit="$root/hostile_audit"
work="$(mktemp -d)"
trap 'find "$work" -depth -delete' EXIT
export PYTHONDONTWRITEBYTECODE=1

echo "[1/5] Verify frozen manifests"
test "$(sha256sum "$author/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "033285315598188a76523d42a53d6a367bf9d3ca08a173276f39c8df7a89bf4d"
test "$(sha256sum "$audit/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "05de61de06ae5297a1c8d9c6cd84838d0b18ceae05e0ac37346e07fd1fdd4d93"
test "$(grep -Ec ' \./provenance/site_(index|ledger_data)_20260811\.js$' "$author/MANIFEST.sha256")" = 2
grep -Ev ' \./provenance/site_(index|ledger_data)_20260811\.js$' \
  "$author/MANIFEST.sha256" > "$work/author-public-manifest.sha256"
(cd "$author" && sha256sum --quiet -c "$work/author-public-manifest.sha256")
(cd "$audit" && sha256sum --quiet -c MANIFEST.sha256)

echo "[2/5] Rebuild the three exact enumerators"
flags=(-std=c++20 -O3 -fopenmp -Wall -Wextra -Wconversion -Wshadow)
g++ "${flags[@]}" "$author/code/count_avoiders.cpp" -o "$work/endpoint"
g++ "${flags[@]}" "$audit/code/automaton_count.cpp" -o "$work/automaton"
g++ "${flags[@]}" "$audit/code/insertion_count.cpp" -o "$work/insertion"

echo "[3/5] Verify frozen logs and the prior exact table"
(cd "$audit" && python3 code/verify_audit_logs.py)
(cd "$audit" && python3 code/check_goh_zhao_prefix.py)

echo "[4/5] Run definition-level exact controls"
(cd "$audit" && python3 code/exhaustive_controls.py)

echo "[5/5] Recompute a fast common prefix"
OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}" "$work/endpoint" 10 10 > "$work/endpoint.log"
OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}" "$work/automaton" 10 > "$work/automaton.log"
OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}" "$work/insertion" 10 > "$work/insertion.log"
index=0
for value in 1 2 6 22 102 564 3336 22266 168864 1307470; do
  index=$((index + 1))
  rg -q "theta4\($index\)=$value([[:space:]]|$)" "$work/endpoint.log"
  rg -q "theta4=$value([[:space:]]|$)" "$work/automaton.log"
  rg -q "theta4=$value([[:space:]]|$)" "$work/insertion.log"
done

if [[ "${FULL:-0}" == 1 ]]; then
  echo "[full] Recompute all three exact searches through n=14"
  OMP_NUM_THREADS="${OMP_NUM_THREADS:-16}" "$work/endpoint" 14 10 > "$work/endpoint14.log"
  OMP_NUM_THREADS="${OMP_NUM_THREADS:-16}" "$work/automaton" 14 > "$work/automaton14.log"
  OMP_NUM_THREADS="${OMP_NUM_THREADS:-16}" "$work/insertion" 14 > "$work/insertion14.log"
  (cd "$audit" && python3 code/verify_audit_logs.py \
    --fresh "$work/automaton14.log" "$work/insertion14.log")
  rg -q 'theta4\(14\)=9471574188' "$work/endpoint14.log"
fi

echo "PROBLEM 196 THETA4 REPRODUCTION PASSED"
