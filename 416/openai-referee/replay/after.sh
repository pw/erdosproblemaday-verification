#!/bin/bash
# waits for drive.py's BUILD END, then probes, then the bridge; leanchecker --fresh only if the bridge compiled.
L=/tmp/oaimath/024/lean-build
while ! grep -q '^build ' $L/steps.tsv; do sleep 30; done
grep -q '^build 0 ' $L/steps.tsv || { echo "build failed" >> $L/post.log; exit 1; }
bash $L/post.sh
bash /tmp/oaimath/024/bridge/build_bridge.sh > /tmp/oaimath/024/bridge/build_bridge.out 2>&1
grep -q 'Bridge416 rc=0' /tmp/oaimath/024/bridge/Bridge416.log && bash $L/leanchecker.sh || echo "bridge did not compile — leanchecker not started" >> $L/post.log
