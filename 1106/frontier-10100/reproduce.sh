#!/bin/sh
set -eu

cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
/usr/bin/time -f 'TIME %e sec MAXRSS %M KB' \
  python3 verify_erdos1106_frontier.py
