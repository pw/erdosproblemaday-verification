#!/bin/bash
export PATH=/home/exedev/.elan/toolchains/leanprover--lean4---v4.33.0/bin:$HOME/.elan/bin:$PATH
cd ~/MathDyad/subs-1116/117/lean-build
echo "start $(date -u +%FT%TZ)"
nice -n 10 lake build > build_full.log 2>&1
rc=$?
echo "lake build rc=$rc done $(date -u +%FT%TZ)"
grep -E "Build completed|error|erdos_117' depends" build_full.log | tail -20
