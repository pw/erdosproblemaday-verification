#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
author="/home/exedev/erdos_scratch/erdos86_q9_1506_20260811"
cd "$root"

python3 verify_q9_independent.py
python3 check_bundle_consistency.py
python3 negative_mutation_test.py
python3 check_site_gate.py

cmp candidate_q9_1506.json "$author/q9_edges_1506.json"
cmp public_q9_1505.json \
  "$author/q9_upstream/q9_edges_repair_from1503_iter2.json"
cmp q9_min_conflicts_author.cpp "$author/generator/q9_min_conflicts.cpp"
cmp reproduced_q9_1506_exact_path.json candidate_q9_1506.json
cmp oeis_A245762_current_20260811.txt \
  "$author/provenance/oeis_A245762_bfile_20260811.txt"
cmp minamoto_2603.29127v4_current.pdf \
  "$author/provenance/minamoto_arxiv_2603.29127v4.pdf"

test "$(git -C public_upstream_current rev-parse HEAD)" = \
  "74e84382cbbc20b32a2ac679bff977cad3ac5d24"
test "$(sha256sum public_upstream_current/q9_edges_repair_from1503_iter2.json | cut -d' ' -f1)" = \
  "0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338"

(cd "$author" && sha256sum -c SHA256SUMS)

echo "COLD_AUDIT_RECHECK_PASS"
