#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
scratch=$(mktemp -d /tmp/erdos80-n9-reproduce.XXXXXX)
trap 'rm -rf -- "$scratch"' EXIT

nauty-geng -q 9 > "$scratch/all_n9.g6"
test "$(sha256sum "$scratch/all_n9.g6" | cut -d' ' -f1)" = \
  ce9c5d4d27c8e55de5f0c6348ec781a650382e16bdff26b6c3418fa00a9cfcf9

g++ -std=c++20 -O2 -Wall -Wextra -pedantic \
  "$here/independent_scan.cpp" -o "$scratch/independent_scan"
"$scratch/independent_scan" "$scratch/all_n9.g6" > "$scratch/independent_scan.out"
diff -u "$here/independent_scan.out" "$scratch/independent_scan.out"

python3 "$here/producer.py" > "$scratch/producer.out"
grep -q '^claims_sha256=da127236a4419ec178b4c6d72334d6335a8e352ba63b37d0224afc232ae943b5$' \
  "$scratch/producer.out"

python3 "$here/audit.py" \
  --graph6 "$scratch/all_n9.g6" \
  --producer-output "$scratch/producer.out"

echo 'REPRODUCE: PASS'
