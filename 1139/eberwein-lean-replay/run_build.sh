#!/bin/bash
export PATH=$HOME/.elan/bin:$PATH
cd ~/MathDyad/subs-1116/1139/build
echo "start $(date -u +%FT%TZ)"
elan toolchain install leanprover/lean4:v4.33.0 2>&1 | tail -2
lake --version
( time lake exe cache get ) 2>&1 | tail -5
echo "cache done $(date -u +%FT%TZ)"; df -h / | tail -1
( time nice -n 10 lake build 2>&1 | tail -40 ) 2>&1
echo "build rc=${PIPESTATUS[0]} done $(date -u +%FT%TZ)"
