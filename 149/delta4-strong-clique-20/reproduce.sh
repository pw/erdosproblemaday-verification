#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
author="$root/author"
audit="$root/hostile_audit"
work="$(mktemp -d)"
trap 'find "$work" -depth -delete' EXIT
export PYTHONDONTWRITEBYTECODE=1

echo "[1/3] Verify frozen manifests"
test "$(sha256sum "$author/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "075baf1d0121870c1edccf9d98dcafbb2ccba9ed16e9aa23d4f962d379f78595"
test "$(sha256sum "$audit/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "062e81c6e7c80869d703e65daaefdc5fed152476cc2f548a119abaf4b54ded15"
(cd "$author" && sha256sum --quiet -c MANIFEST.sha256)
test "$(grep -Ec ' \./provenance/site_(index|ledger)_20260811\.js\.gz$' "$audit/MANIFEST.sha256")" = 2
grep -Ev ' \./provenance/site_(index|ledger)_20260811\.js\.gz$' \
  "$audit/MANIFEST.sha256" \
  | sed 's# ../problem149_delta4_strong_clique_exact_20260811/# ../author/#' \
  > "$work/audit-public-manifest.sha256"
(cd "$audit" && sha256sum --quiet -c "$work/audit-public-manifest.sha256")

echo "[2/3] Run the author algebra and graph checker"
(cd "$author" && python3 verify_149_delta4.py) \
  | diff -u "$author/author_verification.stdout" -

echo "[3/3] Run the independent hostile-audit checker"
python3 - "$audit/independent_verify.py" "$author" "$audit" <<'PY'
import importlib.util
import sys
from pathlib import Path

source, author, audit = map(Path, sys.argv[1:])
spec = importlib.util.spec_from_file_location("audit149", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

old_sources = module.SOURCES
module.BUNDLE = author
module.SOURCES = author / "sources"
module.PROVENANCE = audit / "provenance"
module.EXPECTED_HASHES = {
    module.SOURCES / path.relative_to(old_sources): digest
    for path, digest in module.EXPECTED_HASHES.items()
}

module.check_sources()
module.check_live_gate()
module.check_exact_algebra()
histogram = module.check_blowup()
assert dict(sorted(histogram.items())) == {1: 60, 2: 130}
print("PUBLIC HOSTILE-AUDIT CHECKS PASSED")
PY

echo "PROBLEM 149 DEGREE-4 STRONG-CLIQUE REPRODUCTION PASSED"
