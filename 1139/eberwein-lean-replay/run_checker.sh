#!/bin/bash
export PATH=/home/exedev/.elan/toolchains/leanprover--lean4---v4.33.0/bin:$HOME/.elan/bin:$PATH
cd ~/MathDyad/subs-1116/1139/build
echo "start $(date -u +%FT%TZ)"
( time nice -n 15 lake env leanchecker --fresh Erdos1139Official ) 2>&1 | tail -30
echo "leanchecker rc=${PIPESTATUS[0]} done $(date -u +%FT%TZ)"
