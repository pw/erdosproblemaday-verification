#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
python3 verify_1183_f7.py | tee /tmp/erdos1183_f7_verify.replay
diff -u VERIFY_OUTPUT.txt /tmp/erdos1183_f7_verify.replay
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic audit_lattice_upper.cpp \
  -o /tmp/erdos1183_lattice_upper.replay
/tmp/erdos1183_lattice_upper.replay | tee /tmp/erdos1183_lattice_upper.replay.out
diff -u AUDIT_LATTICE_OUTPUT.txt /tmp/erdos1183_lattice_upper.replay.out
./drat-trim lower_core.cnf lower_core.drat | tee /tmp/erdos1183_f7_drat.replay
tr '\r' '\n' < /tmp/erdos1183_f7_drat.replay | rg -q '^s VERIFIED$'
echo 'ALL BUNDLE CHECKS PASSED'
