#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

python3 "$root/verify_boundary_exchange.py"
python3 "$root/verify_frontier_artifacts.py" \
  --bfile "$root/sources/b004059.txt" \
  --artifacts "$root/frontier"
python3 "$root/audit_density_interval.py" \
  --bfile "$root/sources/b004059.txt" \
  --frontier "$root/frontier/results.json" \
  --out "$tmp" \
  --places 60 >/dev/null
cmp "$tmp" "$root/frontier/density_interval.json"
(cd "$root" && sha256sum -c SHA256SUMS)
echo "PASS: all frozen Problem 168 artifacts verified"
