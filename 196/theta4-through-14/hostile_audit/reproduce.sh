#!/usr/bin/env bash
set -euo pipefail

base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
author=/home/exedev/erdos_scratch/fresh9_erdos196_20260811/bundle_ro
mode=${1:-check}

if [ "$mode" != check ] && [ "$mode" != full ]; then
  echo "usage: $0 [check|full]" >&2
  exit 2
fi

cd "$base"
sha256sum --quiet -c MANIFEST.sha256
echo "audit_manifest_discrepancies=0"

(cd "$author" && sha256sum --quiet -c MANIFEST.sha256)
echo "author_manifest_discrepancies=0"
test "$(find "$author" -type l | wc -l)" -eq 0
test "$(find "$author" -type f | wc -l)" -eq 38
echo "author_file_set_discrepancies=0"

python3 code/verify_audit_logs.py

work=$(mktemp -d -t audit196-repro.XXXXXX)
cleanup() {
  chmod -R u+w "$work" 2>/dev/null || true
  find "$work" -depth -delete 2>/dev/null || true
}
trap cleanup EXIT

common=(-O3 -march=native -fopenmp -std=c++20 -Wall -Wextra -Wconversion -Wshadow -Werror)
g++ "${common[@]}" code/automaton_count.cpp -o "$work/automaton_count"
g++ "${common[@]}" code/insertion_count.cpp -o "$work/insertion_count"
g++ "${common[@]}" "$author/code/count_avoiders.cpp" -o "$work/author_count"

cmp "$work/automaton_count" bin/automaton_count
cmp "$work/insertion_count" bin/insertion_count
cmp "$work/author_count" bin/author_rebuilt_strict
cmp "$work/author_count" "$author/reference/count_avoiders_ubuntu24_x86_64"
sha256sum "$work/automaton_count" "$work/insertion_count" "$work/author_count"
echo "strict_rebuild_discrepancies=0"

if [ "$mode" = full ]; then
  /usr/bin/time -f "wall_seconds=%e user_seconds=%U max_rss_kb=%M exit_status=%x" \
    env OMP_NUM_THREADS=16 "$work/automaton_count" 14 \
    >"$work/automaton.log" 2>&1
  /usr/bin/time -f "wall_seconds=%e user_seconds=%U max_rss_kb=%M exit_status=%x" \
    env OMP_NUM_THREADS=16 "$work/insertion_count" 14 \
    >"$work/insertion.log" 2>&1
  python3 code/verify_audit_logs.py --fresh "$work/automaton.log" "$work/insertion.log"
  "$author/reproduce.sh" 14 10 16
  echo "full_recomputation_discrepancies=0"
fi

echo "audit_reproduction_discrepancies=0"
