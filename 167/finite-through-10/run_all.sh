#!/bin/sh
set -eu

cxx="${CXX:-g++}"
geng="${GENG:-/bin/nauty-geng}"

"$cxx" -O3 -std=c++20 -Wall -Wextra -Wpedantic verify_167.cpp -o verify_167

max_n="${MAX_N:-10}"
n=1
while [ "$n" -le "$max_n" ]; do
  "$geng" -cq "$n" | ./verify_167
  n=$((n + 1))
done

python3 independent_audit.py --max-n 9
python3 audit_order10_sample.py
