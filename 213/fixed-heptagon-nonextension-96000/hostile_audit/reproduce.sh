#!/bin/sh
set -eu

cd "$(dirname "$0")"
author_dir="${1:-../fresh7_erdos213_20260811}"
author_dir="$(cd "$author_dir" && pwd)"

work="$(mktemp -d "${TMPDIR:-/tmp}/audit-erdos213.XXXXXX")"
trap 'rm -rf "$work"' EXIT HUP INT TERM

(cd "$author_dir" && sha256sum --check MANIFEST.sha256)
(cd "$author_dir" && ./reproduce.sh)

g++ -O3 -std=c++20 -Wall -Wextra -Werror \
  audit_sum_difference.cpp -o "$work/audit_sum_difference"
"$work/audit_sum_difference" "$work/audit_candidates.tsv" > "$work/sum_difference.log"
cmp "$work/audit_candidates.tsv" "$author_dir/characteristic_candidates.tsv"
cmp "$work/sum_difference.log" sum_difference.log

python3 audit_metric.py \
  "$author_dir/heptagon_matrix.json" \
  "$work/audit_candidates.tsv" \
  "$author_dir/characteristic_candidates.tsv" > "$work/metric.log"
cmp "$work/metric.log" metric.log

tar -xOf arxiv_0804.1303_source.tar.gz rare.tex | cmp - kreisel_kurz_rare.tex
python3 audit_primary_source.py \
  kreisel_kurz_rare.tex "$author_dir/heptagon_matrix.json" > "$work/primary_source.log"
cmp "$work/primary_source.log" primary_source.log

sha256sum --check MANIFEST.sha256
cat "$work/sum_difference.log"
cat "$work/metric.log"
cat "$work/primary_source.log"
echo HOSTILE_AUDIT_PASS
