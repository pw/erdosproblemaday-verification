#!/bin/sh
set -eu

cd "$(dirname "$0")"

work="$(mktemp -d "${TMPDIR:-/tmp}/erdos213-reproduce.XXXXXX")"
trap 'rm -rf "$work"' EXIT HUP INT TERM

python3 -m json.tool heptagon_matrix.json >/dev/null
python3 verify_matrix.py >"$work/matrix.txt"

g++ -O3 -std=c++20 -Wall -Wextra -Werror \
  extend_heptagon.cpp -o "$work/extend_heptagon"
go build -trimpath -o "$work/verify_semiperimeter" verify_semiperimeter.go

"$work/extend_heptagon" --emit-candidates "$work/cpp_candidates.tsv" \
  >"$work/cpp.txt"
"$work/verify_semiperimeter" -emit-candidates "$work/go_candidates.tsv" \
  >"$work/go.txt"

cmp "$work/cpp.txt" "$work/go.txt"
cmp "$work/cpp_candidates.tsv" "$work/go_candidates.tsv"
cmp characteristic_candidates.tsv "$work/cpp_candidates.tsv"

cat "$work/cpp.txt"
cat "$work/matrix.txt"

if [ -f MANIFEST.sha256 ]; then
  sha256sum --check MANIFEST.sha256
fi
