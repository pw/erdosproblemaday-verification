#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$here"

author_manifest=author/MANIFEST.sha256
audit_manifest=hostile_audit/MANIFEST.sha256
expected_author=4332c124aa51e217254c7071fb346bf666f6bc610fa95dcb72d8d0c69a06ff73
expected_audit=b620564f9aa47a28bee831ef4d65bbbdc8092af6ba00cd69670c98c4e7b5d11c

printf '%s\n' '[1/4] Verify frozen manifest identities and public inventory'
test "$(sha256sum "$author_manifest" | cut -d' ' -f1)" = "$expected_author"
test "$(sha256sum "$audit_manifest" | cut -d' ' -f1)" = "$expected_audit"
grep -Fqx '362fc1f745e3795e734f5f15bbee46f449551fa9d7d1a7a1527cb221fe69e0d2  ./sources/site_index_20260811.js' "$author_manifest"
grep -Fqx '9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052  ./sources/site_ledger_data_20260811.js' "$author_manifest"
filtered=$(mktemp)
trap 'rm -f "$filtered"' EXIT
grep -vE 'sources/site_(index|ledger_data)_20260811\.js$' "$author_manifest" >"$filtered"
test "$(wc -l <"$filtered")" -eq 16
(cd author && sha256sum --quiet -c "$filtered")
(cd hostile_audit && sha256sum --quiet -c MANIFEST.sha256)

printf '%s\n' '[2/4] Run the author polynomial checker'
(cd author && python3 verify_polynomial_frontier.py)

printf '%s\n' '[3/4] Recheck primary-source and live-page quantifiers'
python3 verify_public.py

printf '%s\n' '[4/4] Complete'
printf '%s\n' 'PROBLEM 1117 PUBLIC REPRODUCTION PASSED'
