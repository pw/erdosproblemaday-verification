#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 independent_full_check.py
python3 inputs/erdos708_c11_full_audit.py
