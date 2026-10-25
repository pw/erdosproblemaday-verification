#!/bin/bash
# waits for cache get, then drive.py (W=4), then post.sh probes. leanchecker launched by hand after.
L=/tmp/oaimath/020/lean-build
while ! grep -q '^exit ' $L/cacheget.out 2>/dev/null; do sleep 20; done
grep -q '^exit 0 ' $L/cacheget.out || { echo "cache get failed" >> $L/post.log; exit 1; }
cd $L && python3 drive.py 4 > drive.out 2>&1
bash $L/post.sh
