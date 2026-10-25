#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")" && pwd)
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT
cxx=${CXX:-g++}
threads=${OMP_NUM_THREADS:-$(nproc)}

"$cxx" -std=gnu++20 -O3 -Wall -Wextra -Wconversion \
  -DVERIFY_156_N=102 "$root/verify_size6_differences.cpp" \
  -o "$build/size6_differences"
"$build/size6_differences"

"$cxx" -std=c++20 -O3 -Wall -Wextra -Wconversion -pedantic \
  -DVERIFY_156_MAX_N=102 "$root/verify_size6_sums.cpp" \
  -o "$build/size6_sums"
"$build/size6_sums"

"$cxx" -std=c++20 -O3 -Wall -Wextra -Wconversion -pedantic \
  "$root/verify_size6_direct.cpp" -o "$build/size6_direct"
"$build/size6_direct"

"$cxx" -std=gnu++20 -O3 -Wall -Wextra -Wconversion -fopenmp \
  -DVERIFY_156_K7_MAXIMUM=101 "$root/verify_size7_parallel.cpp" \
  -o "$build/size7_parallel"
OMP_NUM_THREADS="$threads" "$build/size7_parallel"

python3 "$root/check_witnesses_96_102.py"
