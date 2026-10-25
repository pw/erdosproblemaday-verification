#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1

python3 independent_verify.py
sha256sum -c SHA256SUMS
