#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
build="$(mktemp -d)"
trap 'find "$build" -depth -delete' EXIT
threads="${OMP_NUM_THREADS:-8}"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/6] Verify frozen manifests"
test "$(sha256sum "$root/author/SHA256SUMS" | cut -d' ' -f1)" = \
  "566ac359a544556f7453a1b02044692488ed91f0ad2eb4cc09ca24a1503ecd89"
test "$(sha256sum "$root/hostile_audit/SHA256SUMS" | cut -d' ' -f1)" = \
  "bf9b305f499150f0918b48165f358442112ed37c8a6b0ac06d5cc5e13bd951fa"
(cd "$root/author" && sha256sum -c SHA256SUMS)
(cd "$root/hostile_audit" && sha256sum -c SHA256SUMS)

echo "[2/6] Rerun the author certificate"
OMP_NUM_THREADS="$threads" "$root/author/reproduce.sh" | tee "$build/author.out"
cmp "$build/author.out" "$root/hostile_audit/target_reproduce.out"

flags=(-std=c++20 -O3 -fopenmp -Wall -Wextra -Wshadow -Wconversion -pedantic)
echo "[3/6] Compile hostile-audit enumerators"
g++ "${flags[@]}" "$root/hostile_audit/independent_k7_byte.cpp" \
  -o "$build/k7"
g++ "${flags[@]}" "$root/hostile_audit/independent_kle6_byte.cpp" \
  -o "$build/kle6"

echo "[4/6] Independently enumerate all seven-mark rulers"
OMP_NUM_THREADS="$threads" "$build/k7" | tee "$build/k7.out"
cmp "$build/k7.out" "$root/hostile_audit/independent_k7.out"

echo "[5/6] Independently enumerate rulers with at most six marks"
OMP_NUM_THREADS="$threads" "$build/kle6" | tee "$build/kle6.out"
cmp "$build/kle6.out" "$root/hostile_audit/independent_kle6.out"

echo "[6/6] Check the reduction and every witness by literal insertion"
python3 "$root/hostile_audit/independent_reduction_witness.py" \
  | tee "$build/reduction_witness.out"
cmp "$build/reduction_witness.out" \
  "$root/hostile_audit/independent_reduction_witness.out"

echo "PROBLEM 156 FRONTIER-136 REPRODUCTION PASSED"
