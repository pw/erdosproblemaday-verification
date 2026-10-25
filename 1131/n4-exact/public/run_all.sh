#!/usr/bin/env bash
set -euo pipefail

fail() {
    printf 'RUN_ALL=FAIL reason=%s\n' "$1" >&2
    exit 1
}

if [[ -v PYTHONOPTIMIZE ]]; then
    fail "PYTHONOPTIMIZE_must_be_unset"
fi

mode="exact"
if (( $# > 1 )); then
    fail "usage_./run_all.sh_[--with-numeric]"
elif (( $# == 1 )); then
    [[ "$1" == "--with-numeric" ]] || fail "unknown_argument"
    mode="numeric"
fi

cd -- "$(dirname -- "$0")"
export LC_ALL=C
export TZ=UTC
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

command -v sha256sum >/dev/null 2>&1 || fail "sha256sum_not_found"
python_bin="${PYTHON:-python3}"
[[ "$python_bin" != *[[:space:]]* ]] || fail "PYTHON_must_be_one_executable_path"
command -v "$python_bin" >/dev/null 2>&1 || fail "python_not_found"

manifest="MANIFEST.sha256"
pin_file="MANIFEST.sha256.pin"
[[ -f "$manifest" && ! -L "$manifest" ]] || fail "manifest_missing_or_symlinked"
[[ -f "$pin_file" && ! -L "$pin_file" ]] || fail "pin_missing_or_symlinked"

IFS= read -r pinned_digest < "$pin_file" || fail "cannot_read_pin"
[[ "$pinned_digest" =~ ^[0-9a-f]{64}$ ]] || fail "invalid_pin"
[[ "$(wc -l < "$pin_file")" == "1" ]] || fail "pin_must_be_one_line"

actual_digest="$(sha256sum -- "$manifest")"
actual_digest="${actual_digest%% *}"
[[ "$actual_digest" == "$pinned_digest" ]] || fail "manifest_digest_mismatch"

verifier_digest=""
while IFS= read -r line; do
    [[ "$line" =~ ^[0-9a-f]{64}\ \ [A-Za-z0-9][A-Za-z0-9_.-]*$ ]] || fail "invalid_manifest_line"
    name="${line:66}"
    [[ -f "$name" && ! -L "$name" ]] || fail "nonregular_payload_$name"
    if [[ "$name" == "verify_manifest.py" ]]; then
        verifier_digest="${line:0:64}"
    fi
done < "$manifest"
[[ -n "$verifier_digest" ]] || fail "manifest_verifier_not_listed"

actual_verifier_digest="$(sha256sum -- verify_manifest.py)"
actual_verifier_digest="${actual_verifier_digest%% *}"
[[ "$actual_verifier_digest" == "$verifier_digest" ]] || fail "manifest_verifier_digest_mismatch"
printf 'BOOTSTRAP_MANIFEST=PASS\n'

"$python_bin" -I -P verify_manifest.py
"$python_bin" -I -P verify_exact.py
if [[ "$mode" == "numeric" ]]; then
    "$python_bin" -I -P verify_numeric.py
fi
