#!/usr/bin/env bash
set -euo pipefail

audit_dir=$(cd -- "$(dirname -- "$0")" && pwd)
bundle=${1:-/home/exedev/erdos_scratch/erdos1160_m11_20260811_v2}

case "$(basename -- "$bundle")" in
  erdos1160_m11_20260811_v2)
    expected_manifest=8cb5c802c759c3a2dc12fd3e203e00abb991bfaae5376e44ebaa71e48da6dd90
    ;;
  erdos1160_m11_20260811)
    expected_manifest=2289951ca13d7a86e9878ac22b9f9d1d4185589545dca689e5ef1b403221525f
    ;;
  *)
    printf 'unsupported bundle path: %s\n' "$bundle" >&2
    exit 2
    ;;
esac

printf '[1/5] Verify audit artifacts\n'
(cd "$audit_dir" && sha256sum -c AUDIT_SHA256SUMS >/dev/null)

printf '[2/5] Verify bundle manifest identity and coverage\n'
printf '%s  %s\n' "$expected_manifest" "$bundle/SHA256SUMS" | sha256sum -c -
(cd "$bundle" && sha256sum -c SHA256SUMS >/dev/null)
actual=$(find "$bundle" -type f ! -name SHA256SUMS -printf '%P\n' | LC_ALL=C sort)
listed=$(sed 's/^[0-9a-f]\{64\}  //' "$bundle/SHA256SUMS" | LC_ALL=C sort)
test "$actual" = "$listed"

printf '[3/5] Verify bundle remains read-only\n'
test -z "$(find "$bundle" -perm /222 -print -quit)"

printf '[4/5] Run independently written arithmetic/source verifier\n'
python3 "$audit_dir/independent_verifier.py" "$bundle"
python3 "$audit_dir/check_burrell_table.py"

printf '[5/5] Check frozen live b-file against bundle b-file\n'
cmp "$audit_dir/current_b000001.txt" "$bundle/b000001_20260811.txt"

printf 'AUDIT REPRODUCTION PASSED\n'
