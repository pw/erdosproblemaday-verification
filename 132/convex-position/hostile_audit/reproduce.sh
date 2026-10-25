#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
unset PYTHONOPTIMIZE
export PYTHONDONTWRITEBYTECODE=1
python3 -B code/check_manifest.py
python3 -B code/verify_independent.py
printf '%s\n' 'SECOND HOSTILE AUDIT REPLAY PASSED'
