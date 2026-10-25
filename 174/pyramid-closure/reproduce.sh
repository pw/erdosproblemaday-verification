#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
public="$root/public"
audit="$root/hostile_audit"

test "$(sha256sum "$public/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "96d9a06c67206c4a7d22f00b41d21ead41314ecc87848e1990420ab1648ba9cf"
test "$(sha256sum "$audit/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "6d38a4dfef13fd4a366f92fb45b90f440950987b45b1e590d1100288b0d4b6c7"

(cd "$public" && sha256sum --quiet -c MANIFEST.sha256)
(cd "$audit" && sha256sum --quiet -c MANIFEST.sha256)
"$public/reproduce.sh"

echo "PROBLEM 174 PYRAMID-CLOSURE REPRODUCTION PASSED"
