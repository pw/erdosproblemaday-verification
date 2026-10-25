#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 independent_verify.py | diff -u independent_verify.stdout -
sha256sum -c MANIFEST.sha256
