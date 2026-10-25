#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
cd "$root"

python3 verify_faces.py q9_edges_1506.json
python3 verify_cherries.py q9_edges_1506.json --n 9 --expected-edges 1506
python3 compare_public_frontier.py

test "$(wc -l < q9_edges_1506.txt)" -eq 1506
jq -r '.edges[] | "\(.[0]) \(.[1])"' q9_edges_1506.json | cmp - q9_edges_1506.txt

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
g++ -O3 -fopenmp -std=c++20 generator/q9_min_conflicts.cpp -o "$tmpdir/q9_min_conflicts"
"$tmpdir/q9_min_conflicts" \
  q9_upstream/q9_edges_repair_from1503_iter2.json \
  "$tmpdir/reproduced.json" 1 1000000 1
cmp q9_edges_1506.json "$tmpdir/reproduced.json"
echo "PASS deterministic generation: byte-identical witness"

sha256sum -c SHA256SUMS
