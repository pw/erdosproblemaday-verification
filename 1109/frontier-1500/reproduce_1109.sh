#!/usr/bin/env bash
set -euo pipefail

mode=${1:-quick}
case "$mode" in
  quick|primary|pmc|cliquer|sanitizer|all) ;;
  *) printf 'usage: %s [quick|primary|pmc|cliquer|sanitizer|all]\n' "$0" >&2; exit 2 ;;
esac

cd "$(dirname "$0")"
manifest=erdos1109_manifest_2026-08-11.sha256
cliquer_digest=6583a40e338f7bddbfe7eb666b3e1996c1c55bf7e325ce4ca9070a4baa856b84
pmc_digest=cce1073c81456eb675be5adea58cf4fd2caa08f84bfa344465b38eadd5596dc3
witness_digest=e0dbdd09d85666c5cc57534b7905e8f4d3ad2e9fbb7e0925b7fde9367c363911

sha256sum -c "$manifest"
python3 check_1109_witnesses.py | tee /tmp/erdos1109_witness_replay.txt
grep -Fqx "witness_sha256=$witness_digest" /tmp/erdos1109_witness_replay.txt
python3 check_1109_external_audits.py | tee /tmp/erdos1109_external_replay.txt
grep -Fqx "cliquer_audit_sha256=$cliquer_digest" /tmp/erdos1109_external_replay.txt
grep -Fqx "pmc_audit_sha256=$pmc_digest" /tmp/erdos1109_external_replay.txt

if [[ "$mode" == primary || "$mode" == all ]]; then
  primary_bin=$(mktemp /tmp/verify_1109_frontier.XXXXXX)
  primary_out=$(mktemp /tmp/verify_1109_frontier_output.XXXXXX)
  g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
    verify_1109_frontier.cpp -o "$primary_bin"
  "$primary_bin" 1500 >"$primary_out"
  diff -u <(grep '^f=' erdos1109_frontier_run_2026-08-11.log) \
    <(grep '^f=' "$primary_out")
fi

if [[ "$mode" == pmc || "$mode" == all ]]; then
  pmc_out=$(mktemp /tmp/erdos1109_pmc_output.XXXXXX)
  python3 audit_1109_incremental_pmc.py --jobs 2 >"$pmc_out"
  grep -Fqx "audit_sha256=$pmc_digest" "$pmc_out"
fi

if [[ "$mode" == cliquer || "$mode" == all ]]; then
  test "$(sha256sum /usr/bin/cliquer | cut -d' ' -f1)" = \
    d482f5756fff600b4ec646bedeaa9e685b859fc3810be2c7faf078b18ea51d93
  cliquer_out=$(mktemp /tmp/erdos1109_cliquer_output.XXXXXX)
  python3 audit_1109_incremental_parallel_cliquer.py --jobs 6 >"$cliquer_out"
  grep -Fqx "audit_sha256=$cliquer_digest" "$cliquer_out"
fi

if [[ "$mode" == sanitizer || "$mode" == all ]]; then
  sanitizer_bin=$(mktemp /tmp/verify_1109_frontier_sanitize.XXXXXX)
  sanitizer_out=$(mktemp /tmp/verify_1109_frontier_sanitize_output.XXXXXX)
  g++ -std=c++20 -O1 -g -fsanitize=address,undefined \
    -fno-omit-frame-pointer -Wall -Wextra -Wpedantic \
    verify_1109_frontier.cpp -o "$sanitizer_bin"
  "$sanitizer_bin" 1500 >"$sanitizer_out"
  diff -u <(grep '^f=' erdos1109_frontier_run_2026-08-11.log) \
    <(grep '^f=' "$sanitizer_out")
fi

printf 'PASS mode=%s\n' "$mode"

