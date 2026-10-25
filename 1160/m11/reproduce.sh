#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"

echo "[1/2] Reproduce corrected author certificate"
"$root/author/reproduce.sh"

echo "[2/2] Reproduce hostile audit"
tmp="$(mktemp -d)"
trap 'find "$tmp" -type d -exec chmod u+w {} +; find "$tmp" -depth -delete' EXIT
cp -al "$root/author" "$tmp/erdos1160_m11_20260811_v2"
"$root/hostile_audit/reproduce_audit.sh" \
  "$tmp/erdos1160_m11_20260811_v2"

echo "PROBLEM 1160 M=11 REPRODUCTION PASSED"
