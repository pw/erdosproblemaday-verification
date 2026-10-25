#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
threads="${OMP_NUM_THREADS:-8}"
build="$(mktemp -d)"
trap 'find "$build" -depth -delete' EXIT

echo "[1/7] Verify frozen hashes"
sha256sum -c SHA256SUMS

flags=(-std=c++20 -O3 -fopenmp -Wall -Wextra -Wshadow -Wconversion -pedantic)

echo "[2/7] Compile exact enumerators"
g++ "${flags[@]}" -DVERIFY_156_K7_MAXIMUM=135 \
  verify_size7_sums.cpp -o "$build/size7_sums"
g++ "${flags[@]}" verify_size7_differences_words.cpp \
  -o "$build/size7_differences"
g++ "${flags[@]}" verify_size6_sums_parallel.cpp \
  -o "$build/size6_parallel"

echo "[3/7] Enumerate all normalized seven-mark rulers by pair sums"
OMP_NUM_THREADS="$threads" "$build/size7_sums" | tee "$build/size7_sums.out"
cmp "$build/size7_sums.out" final_size7_sums.out

echo "[4/7] Enumerate all normalized seven-mark rulers by differences"
OMP_NUM_THREADS="$threads" "$build/size7_differences" \
  | tee "$build/size7_differences.out"
cmp "$build/size7_differences.out" final_size7_differences.out

echo "[5/7] Enumerate all normalized rulers of sizes one through six"
OMP_NUM_THREADS="$threads" "$build/size6_parallel" \
  | tee "$build/size6_parallel.out"
cmp "$build/size6_parallel.out" final_size6_parallel.out

echo "[6/7] Check every upper certificate directly"
python3 verify_witness_102_136.py | tee "$build/witnesses.out"
cmp "$build/witnesses.out" final_witnesses.out

echo "[7/7] Cross-check all blocking formulations on small instances"
python3 crosscheck_blocking_small.py | tee "$build/crosscheck.out"
cmp "$build/crosscheck.out" final_crosscheck.out

if [[ "${FULL:-0}" == 1 ]]; then
  echo "[full] Run the original sequential sizes-one-through-six engine"
  g++ -std=c++20 -O3 -Wall -Wextra -Wshadow -Wconversion -pedantic \
    -DVERIFY_156_MAX_N=136 verify_size6_sums.cpp \
    -o "$build/size6_sequential"
  "$build/size6_sequential" | tee "$build/size6_sequential.out"
  cmp "$build/size6_sequential.out" final_size6_sequential.out

  echo "[full] Run ASan/UBSan on the max-110 pair-sum engine"
  g++ -std=c++20 -O1 -g -fopenmp -fsanitize=address,undefined \
    -fno-omit-frame-pointer -Wall -Wextra -Wshadow -Wconversion \
    -DVERIFY_156_K7_MAXIMUM=110 verify_size7_sums.cpp \
    -o "$build/size7_sums_sanitized"
  OMP_NUM_THREADS="$threads" ASAN_OPTIONS=detect_leaks=1 \
    UBSAN_OPTIONS=print_stacktrace=1 "$build/size7_sums_sanitized" \
    | tee "$build/size7_sums_sanitized.out"
  cmp "$build/size7_sums_sanitized.out" final_size7_sums_max110.out
fi

sha256sum -c SHA256SUMS >/dev/null
echo "PROBLEM 156 FRONTIER-136 REPRODUCTION PASSED"
