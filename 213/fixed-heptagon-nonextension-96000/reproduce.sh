#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")" && pwd)
AUTHOR="$ROOT/author"
AUDIT="$ROOT/hostile_audit"
export PYTHONDONTWRITEBYTECODE=1

echo "[1/3] Verify frozen manifests"
printf '%s  %s\n' \
  8dc4ce03a4bc8e6e8873c314e11f2efefb9840bcb38b62f32d9b5ce2d979aa47 \
  "$AUTHOR/MANIFEST.sha256" | sha256sum -c -
printf '%s  %s\n' \
  edbdb1e8e105b8ff38bf34030e29eddb6c078b53cac8e44c88f6a4296b7a7dd4 \
  "$AUDIT/MANIFEST.sha256" | sha256sum -c -
(cd "$AUTHOR" && sha256sum -c MANIFEST.sha256)
(cd "$AUDIT" && sha256sum -c MANIFEST.sha256)

echo "[2/3] Run the two author scanners"
(cd "$AUTHOR" && ./reproduce.sh)

echo "[3/3] Run the independent hostile audit"
(cd "$AUDIT" && ./reproduce.sh "$AUTHOR")

echo "PROBLEM 213 FIXED-HEPTAGON REPRODUCTION PASSED"
