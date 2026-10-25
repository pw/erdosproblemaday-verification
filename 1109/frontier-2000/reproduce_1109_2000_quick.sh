#!/usr/bin/env bash
set -euo pipefail

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$here"

base_dir=""
if [[ $# -eq 2 && $1 == "--base-dir" ]]; then
  base_dir=$2
elif [[ $# -ne 0 ]]; then
  printf 'usage: %s [--base-dir PATH]\n' "$0" >&2
  exit 2
elif [[ -f ../frontier-1500/erdos1109_manifest_2026-08-11.sha256 ]]; then
  base_dir=../frontier-1500
fi

printf '%s\n' '[1/5] verifying frozen extension manifest'
sha256sum --quiet -c MANIFEST.sha256

printf '%s\n' '[2/5] verifying key source, binary, and transcript identities'
sha256sum --quiet -c KEY_INPUTS.sha256

printf '%s\n' '[3/5] checking completed primary transcript and all 201 decision rows'
python3 check_primary_completion.py

printf '%s\n' '[4/5] cold-regenerating extension graphs, digest, intervals, and witnesses'
python3 cold_check_extension.py
python3 check_positive_witnesses.py

printf '%s\n' '[5/5] checking the public through-1500 dependency when available'
if [[ -n $base_dir ]]; then
  base_manifest=$base_dir/erdos1109_manifest_2026-08-11.sha256
  test -f "$base_manifest"
  expected=cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9
  actual=$(sha256sum "$base_manifest" | cut -d' ' -f1)
  [[ $actual == "$expected" ]]
  (cd "$base_dir" && sha256sum --quiet -c erdos1109_manifest_2026-08-11.sha256)
  printf 'base_dependency=verified path=%s manifest_sha256=%s\n' "$base_dir" "$actual"
else
  printf '%s\n' \
    'base_dependency=not_present expected_manifest_sha256=cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9'
  printf '%s\n' 'Pass --base-dir PATH to reverify the public frontier-1500 bundle.'
fi

printf '%s\n' 'CONCLUSION quick frozen-artifact audit completed successfully'
