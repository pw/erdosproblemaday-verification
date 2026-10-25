#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 audit_local_absence.py
python3 verify_149_delta4.py
sha256sum -c MANIFEST.sha256
