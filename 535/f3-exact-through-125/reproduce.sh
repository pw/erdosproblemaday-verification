#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir"

audit_tmp_dir=$(mktemp -d /tmp/erdos535-public-reproduce.XXXXXX)
trap 'rm -rf "$audit_tmp_dir"' EXIT HUP INT TERM

python3 verify_535_extension.py | tee "$audit_tmp_dir/python.log"
cmp "$audit_tmp_dir/python.log" verify_535_extension.log

g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  independent_verify.cpp -o "$audit_tmp_dir/independent_verify"
"$audit_tmp_dir/independent_verify" | tee "$audit_tmp_dir/cpp.log"
cmp "$audit_tmp_dir/cpp.log" independent_verify.log

python3 hostile_audit_535.py | tee "$audit_tmp_dir/audit.log"
cmp "$audit_tmp_dir/audit.log" hostile_audit_535.log

sha256sum -c SHA256SUMS
