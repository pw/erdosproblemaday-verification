#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 audit_site_gate.py
python3 verify_order_slice.py --max-n 40
python3 audit_permutation_collision.py
python3 audit_asymptotics.py
sha256sum -c SHA256SUMS
