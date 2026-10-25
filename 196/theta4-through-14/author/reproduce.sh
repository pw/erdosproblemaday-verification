#!/usr/bin/env bash
set -euo pipefail

bundle_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
max_n=14
crosscheck_n=10
threads=16

if [ "$#" -ge 1 ]; then max_n=$1; fi
if [ "$#" -ge 2 ]; then crosscheck_n=$2; fi
if [ "$#" -ge 3 ]; then threads=$3; fi

if [ "$max_n" -lt 1 ] || [ "$max_n" -gt 14 ]; then
  echo "max_n must be in [1,14]" >&2
  exit 2
fi
if [ "$crosscheck_n" -lt 0 ] || [ "$crosscheck_n" -gt "$max_n" ]; then
  echo "crosscheck_n must be in [0,max_n]" >&2
  exit 2
fi
if [ "$threads" -lt 1 ]; then
  echo "threads must be positive" >&2
  exit 2
fi

cd "$bundle_dir"
sha256sum --quiet -c MANIFEST.sha256
echo "manifest_discrepancies=0"

work_dir=$(mktemp -d -t erdos196-repro.XXXXXX)
echo "reproduction_directory=$work_dir"

python3 code/audit_site_collision.py | tee "$work_dir/site_collision.log"

g++ -O3 -march=native -fopenmp -std=c++20 -Wall -Wextra \
  code/count_avoiders.cpp -o "$work_dir/count_avoiders" \
  2>&1 | tee "$work_dir/compile.log"

/usr/bin/time -f "wall_seconds=%e max_rss_kb=%M exit_status=%x" \
  env OMP_NUM_THREADS="$threads" \
  "$work_dir/count_avoiders" "$max_n" "$crosscheck_n" \
  2>&1 | tee "$work_dir/optimized.log"

/usr/bin/time -f "wall_seconds=%e max_rss_kb=%M exit_status=%x" \
  python3 code/independent_verify.py \
  2>&1 | tee "$work_dir/independent.log"

python3 code/verify_count_log.py \
  "$work_dir/optimized.log" expected_counts.tsv "$max_n" \
  | tee "$work_dir/count_comparison.log"

sha256sum "$work_dir/count_avoiders" > "$work_dir/rebuilt_binary.sha256"
echo "reproduction_discrepancies=0"
