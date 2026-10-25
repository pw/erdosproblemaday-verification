#!/bin/bash
# waits for drive.py's BUILD END line, then post.sh probes.
L=/tmp/oaimath/021/lean-build
while ! grep -q '^build ' $L/steps.tsv 2>/dev/null; do sleep 30; done
bash $L/post.sh
