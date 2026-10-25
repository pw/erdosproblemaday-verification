#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
public="$root/public"
audit="$root/hostile_audit"

test "$(sha256sum "$public/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "9af6dabf0ffcf8d86ee3176c9bd7d875e18f9b341fda6e1aa126f04cfbd43db5"
test "$(sha256sum "$audit/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "510b1e755c550c9d07d06038591557eb35a5e3b23e4f688ac24d86da2f36eae6"

"$public/reproduce.sh"
"$audit/reproduce.sh"

echo "PROBLEM 132 CONVEX-POSITION REPRODUCTION PASSED"
