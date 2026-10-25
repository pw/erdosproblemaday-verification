#!/usr/bin/env bash
set -euo pipefail

fail() {
    printf 'ERDOS1131_REPRODUCTION=FAIL reason=%s\n' "$1" >&2
    exit 1
}

if [[ -v PYTHONOPTIMIZE ]]; then
    fail "PYTHONOPTIMIZE_must_be_unset"
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

sha256sum --strict -c SHA256SUMS

(
    cd public
    PYTHON="$python_bin" ./run_all.sh --with-numeric
)
(
    cd hostile_audit
    sha256sum --strict -c MANIFEST.sha256
)
(
    cd literature_audit
    sha256sum --strict -c MANIFEST.sha256
)

printf 'ERDOS1131_REPRODUCTION=PASS\n'
