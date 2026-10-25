#!/bin/bash
# waits for drive.py's BUILD END, then probes, then the bridges; leanchecker --fresh only if both bridges compiled.
L=/tmp/oaimath/025/lean-build; B=/tmp/oaimath/025/bridge
while ! grep -q '^build ' $L/steps.tsv 2>/dev/null; do sleep 30; done
grep -q '^build 0 ' $L/steps.tsv || { echo "build failed" >> $L/post.log; exit 1; }
bash $L/post.sh
bash $B/build_bridge.sh > $B/build_bridge.out 2>&1
if grep -q 'Bridge304 rc=0' $B/Bridge304.log && grep -q 'Bridge148_293 rc=0' $B/Bridge148_293.log; then bash $L/leanchecker.sh; else echo "bridge did not compile — leanchecker not started" >> $L/post.log; fi
