#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
threads="${OMP_NUM_THREADS:-8}"
target="/home/exedev/erdos_scratch/erdos156_A382397_exact_103_136_2026-08-11"
prior="/home/exedev/ErdosProblemADay/verification/156/extension_96_102"
build="$(mktemp -d)"
trap 'find "$build" -depth -delete' EXIT

echo "[1/7] Verify this audit and the immutable target"
sha256sum -c SHA256SUMS
test "$(sha256sum "$target/SHA256SUMS" | cut -d' ' -f1)" = \
  "566ac359a544556f7453a1b02044692488ed91f0ad2eb4cc09ca24a1503ecd89"
test "$(sha256sum "$target/REPORT.md" | cut -d' ' -f1)" = \
  "d9576cc509c93b0330486960f806b2acb1d4c1f5d08e873e014e544a7a14a864"
(cd "$target" && sha256sum -c SHA256SUMS >/dev/null)

flags=(-std=c++20 -O3 -fopenmp -Wall -Wextra -Wshadow -Wconversion -pedantic)
echo "[2/7] Compile the independent byte-array enumerators"
g++ "${flags[@]}" independent_k7_byte.cpp -o "$build/k7"
g++ "${flags[@]}" independent_kle6_byte.cpp -o "$build/kle6"

echo "[3/7] Independently enumerate all seven-mark rulers"
OMP_NUM_THREADS="$threads" "$build/k7" | tee "$build/k7.out"
cmp "$build/k7.out" independent_k7.out

echo "[4/7] Independently enumerate all rulers with at most six marks"
OMP_NUM_THREADS="$threads" "$build/kle6" | tee "$build/kle6.out"
cmp "$build/kle6.out" independent_kle6.out

echo "[5/7] Check the reduction and all witnesses by literal insertion"
python3 independent_reduction_witness.py | tee "$build/reduction_witness.out"
cmp "$build/reduction_witness.out" independent_reduction_witness.out

echo "[6/7] Rerun both target k=7 engines and its remaining default checks"
OMP_NUM_THREADS="$threads" "$target/reproduce.sh" | tee "$build/target.out"
cmp "$build/target.out" target_reproduce.out

echo "[7/7] Verify the prior-through-102 dependency"
(cd "$prior" && sha256sum -c SHA256SUMS >/dev/null)
(cd "$prior/hostile_audit" && sha256sum -c MANIFEST.sha256 >/dev/null)

sha256sum -c SHA256SUMS >/dev/null
echo "HOSTILE AUDIT REPRODUCTION PASSED"
