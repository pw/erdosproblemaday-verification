#!/bin/bash
# sequential k(x) SAT queries (seat C); each query bounded by 1800 s solver timeout inside kenc.py
cd "$(dirname "$0")"
q() { echo "=== $(date -u +%T) python3 kenc.py $*"; nice -n 19 bash -c "ulimit -v 8000000; exec timeout 2000 python3 kenc.py $* --timeout 1800" 2>&1 | grep -v '^MODULI'; }
q --x 12 --k 5
q --x 12 --k 6
q --x 24 --k 6
q --x 24 --k 7
q --x 30 --k 10
q --x 30 --k 11
q --x 36 --k 14
q --x 36 --k 15
q --x 40 --k 15
q --x 40 --k 16
q --x 48 --k 18
q --x 48 --k 19
echo "=== ALLDONE $(date -u +%T)"
