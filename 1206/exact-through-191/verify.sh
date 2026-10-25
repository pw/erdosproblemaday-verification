#!/usr/bin/env bash
set -euo pipefail

bundle_dir="$(cd "$(dirname "$0")" && pwd)"
python3 "$bundle_dir/audit_definition.py"

build_dir="$(mktemp -d)"
cleanup() {
  rm -rf -- "$build_dir"
}
trap cleanup EXIT

g++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  "$bundle_dir/verify_exact.cpp" -o "$build_dir/verify_exact"
"$build_dir/verify_exact"
