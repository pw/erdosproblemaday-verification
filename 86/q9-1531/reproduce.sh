#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
author="$root/author"
audit="$root/hostile_audit"

test "$(sha256sum "$author/SHA256SUMS" | cut -d' ' -f1)" = \
  "520b3c6ae7ced58c696dc8ccb7141e141d0e9db95bec56d1be7865353b88806f"
test "$(sha256sum "$audit/MANIFEST.sha256" | cut -d' ' -f1)" = \
  "70e62fe1c011767a8cd0c92437ba0319a29c56a79b7e12dd87dc9f26987b1000"

(cd "$author" && sha256sum --quiet -c SHA256SUMS)
diff -qr "$author" "$audit/author_bundle"
"$audit/recheck_audit.sh"

echo "PROBLEM 86 Q9-1531 REPRODUCTION PASSED"
