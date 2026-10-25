#!/usr/bin/env bash
set -euo pipefail

root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$root"

sha256sum -c SHA256SUMS
python3 audit_definition.py

tmpdir=$(mktemp -d)
trap 'find "$tmpdir" -type f -delete; rmdir "$tmpdir"' EXIT
g++ -O3 -std=c++20 -Wall -Wextra -pedantic dfs_n71.cpp -o "$tmpdir/dfs_n71"
if ! cmp -s "$tmpdir/dfs_n71" dfs_n71; then
  echo "rebuilt binary differs from frozen binary" >&2
  exit 1
fi

if [[ "${FULL:-0}" == "1" ]]; then
  cp run_cubes.sh dfs_n71 prefix_bounds_through_70.txt "$tmpdir/"
  (
    cd "$tmpdir"
    ./run_cubes.sh > cube_summary.log
    diff -u <(sed -E 's/ seconds=[^ ]+//' "$root/cube_summary.log") \
            <(sed -E 's/ seconds=[^ ]+//' cube_summary.log)
    for cube in 00 010 011 100 101 110 111; do
      diff -u <(sed -E 's/ seconds=[^ ]+//' "$root/cube_${cube}.log") \
              <(sed -E 's/ seconds=[^ ]+//' "cube_${cube}.log")
      diff -u "$root/cube_${cube}.status" "cube_${cube}.status"
    done
  )
fi

echo "REPRODUCTION PASS"
