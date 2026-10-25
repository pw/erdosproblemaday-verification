#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")" && pwd)
AUTHOR="$ROOT/author"
AUDIT="$ROOT/hostile_audit"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/4] Verify frozen manifest identities"
printf '%s  %s\n' \
  bf38c14f6d43985c6b1cc36607b8ed625e9c4cfe5213bb94e57f1759bf00245c \
  "$AUTHOR/SHA256SUMS" | sha256sum -c -
printf '%s  %s\n' \
  fee79692aa8ea284263f9fba222efaaa2a6e04e9c5b870c8ae839f5c2d586072 \
  "$AUDIT/SHA256SUMS" | sha256sum -c -

echo "[2/4] Verify every published frozen artifact"
omitted=$(awk '$2 == "parallel_sn_19.tar.xz" { count++ } END { print count + 0 }' "$AUTHOR/SHA256SUMS")
test "$omitted" -eq 1
test ! -e "$AUTHOR/parallel_sn_19.tar.xz"
awk '$2 != "parallel_sn_19.tar.xz"' "$AUTHOR/SHA256SUMS" |
  (cd "$AUTHOR" && sha256sum -c -)
(cd "$AUDIT" && sha256sum -c SHA256SUMS)

echo "[3/4] Run the corrected author theorem checks"
(cd "$AUTHOR" && python3 verify_order_slice.py --max-n 40)
(cd "$AUTHOR" && python3 audit_permutation_collision.py)
(cd "$AUTHOR" && python3 audit_asymptotics.py)

echo "[4/4] Run the independent hostile verifier"
(cd "$AUDIT" && ./reproduce.sh)

echo "PROBLEM 1162 ORDER-SLICE REPRODUCTION PASSED"
