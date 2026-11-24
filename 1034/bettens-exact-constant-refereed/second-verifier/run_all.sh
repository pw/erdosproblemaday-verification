#!/bin/bash
# Decorrelated second instrument for the Erdos #1034 certificate (sub_j8gq7z). Reads only the deposit's
# verification_model.json + certificate.json.gz as data (paths in core.py); never touches its verify.py.
set -e
cd "$(dirname "$0")"
run() { bash -c "ulimit -v 12000000; exec nice -n 19 timeout 7200 /usr/bin/time -v python3 $*"; }
run basis.py                     2>&1 | tee basis.log          # step 1: geng basis, canonical forms, bijection
run counts.py                    2>&1 | tee counts.log         # step 2a: rooted-configuration counts (6 workers)
run evalA.py --controls          2>&1 | tee evalA_controls.log # step 2b: exact + mod-p residuals, mutations
run psd.py                       2>&1 | tee psd.log            # step 3: exact PSD + signs + planted controls
run routeB.py 1044 1             2>&1 | tee routeB_full.log    # step 2c: independent per-term route, all graphs
run routeB.py 24 20261124 --include-beta --variants 2>&1 | tee routeB_sample_variants.log  # convention controls
