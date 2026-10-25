#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

printf '$ python3 --version\n'
python3 --version
printf '\n$ python3 verify_e6626.py\n'
python3 verify_e6626.py
printf '\n$ python3 verify_e6626_independent.py\n'
python3 verify_e6626_independent.py
printf '\n$ python3 verify_general.py\n'
python3 verify_general.py
