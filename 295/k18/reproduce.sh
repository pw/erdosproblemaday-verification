#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

CXX=${CXX:-g++}
THREADS=${THREADS:-8}
PYTHON_PROCS=${PYTHON_PROCS:-12}
FRONTIER_DEPTH=${FRONTIER_DEPTH:-20}
BINARY=verify_k18_gmp.rebuilt
RUN_TMP=$(mktemp -d)
trap 'rm -f "$BINARY"; rm -rf "$RUN_TMP"' EXIT

"$CXX" -O3 -march=native -std=c++17 -pthread \
  verify_k18_gmp.cpp -lgmpxx -lgmp -o "$BINARY"

expect_gmp_unsat() {
  local terms=$1
  local status
  local output="$RUN_TMP/gmp_$terms.out"
  set +e
  "./$BINARY" 18 "$terms" "$THREADS" "$FRONTIER_DEPTH" | tee "$output"
  status=${PIPESTATUS[0]}
  set -e
  if [[ $status -ne 20 ]]; then
    printf 'unexpected GMP verifier exit status: %s\n' "$status" >&2
    return 1
  fi
  grep -Fqx "min=18 terms=$terms found=false" "$output"
  grep -Fqx "factored_states=0 divisor_states=0 divisor_candidates=0" "$output"
}

expect_fraction_unsat() {
  local terms=$1
  local output="$RUN_TMP/fraction_$terms.out"
  python3 verify_k18_fraction.py 18 "$terms" "$PYTHON_PROCS" | tee "$output"
  grep -Fqx "min=18 terms=$terms found=False" "$output"
}

expect_gmp_unsat 31
expect_gmp_unsat 32
expect_fraction_unsat 31
expect_fraction_unsat 32

grep -Fqx 'states=20293 two_states=13139 scan_candidates=69727' \
  "$RUN_TMP/gmp_31.out"
grep -Fqx 'recursive_states=20293 two_term_states=13139 two_term_candidates=69727' \
  "$RUN_TMP/fraction_31.out"
grep -Fqx 'states=14678224 two_states=11753049 scan_candidates=114603091' \
  "$RUN_TMP/gmp_32.out"
grep -Fqx 'recursive_states=14678224 two_term_states=11753049 two_term_candidates=114603091' \
  "$RUN_TMP/fraction_32.out"

python3 check_k18_upper.py | tee "$RUN_TMP/upper.out"
grep -Fqx 'all_checks=PASS' "$RUN_TMP/upper.out"
printf 'reproduction=PASS\n'
