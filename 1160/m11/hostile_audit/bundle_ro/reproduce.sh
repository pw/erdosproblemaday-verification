#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/5] Verify frozen-file hashes"
sha256sum -c SHA256SUMS

echo "[2/5] Compile Python in memory"
python3 - <<'PY'
from pathlib import Path

for name in ("verify_erdos1160_m11.py", "audit_independent.py"):
    compile(Path(name).read_text(), name, "exec")
    print(f"compiled {name}")
PY

echo "[3/5] Run main exact verifier"
python3 verify_erdos1160_m11.py

echo "[4/5] Run independent reconstruction"
python3 audit_independent.py

echo "[5/5] Regenerate the GAP audit from pinned Ubuntu packages"
runtime="$(mktemp -d)"
trap 'rm -rf "$runtime"' EXIT
for package in debs/*.deb; do
    dpkg-deb -x "$package" "$runtime"
done
"$runtime/usr/lib/x86_64-linux-gnu/gap/gap" \
    -q -l "$runtime/usr/share/gap" enumerate_gap.g > "$runtime/gap_counts.txt"
cmp gap_available_counts_1_2047.txt "$runtime/gap_counts.txt"

sha256sum -c SHA256SUMS >/dev/null
echo "REPRODUCTION PASSED"
