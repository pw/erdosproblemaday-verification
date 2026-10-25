#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 PATH_TO_ERDOS80_N9_BUNDLE" >&2
  exit 2
fi

here=$(cd "$(dirname "$0")" && pwd)
python3 "$here/hostile_audit.py" "$1"
