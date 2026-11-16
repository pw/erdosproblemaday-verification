#!/bin/bash
export PATH=/home/exedev/.elan/toolchains/leanprover--lean4---v4.33.0/bin:$HOME/.elan/bin:$PATH
cd ~/MathDyad/subs-1116/117/lean-build
echo "start $(date -u +%FT%TZ)"
nice -n 15 lake env leanchecker --fresh ErdosProblems.Erdos117 > leanchecker117.log 2>&1
echo "leanchecker rc=$? done $(date -u +%FT%TZ)"
tail -5 leanchecker117.log
