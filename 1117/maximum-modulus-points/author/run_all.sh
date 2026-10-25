#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 verify_gate.py
python3 verify_polynomial_frontier.py
sha256sum -c MANIFEST.sha256
