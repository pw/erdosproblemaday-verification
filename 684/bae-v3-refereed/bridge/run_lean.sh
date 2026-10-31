#!/bin/bash
# usage: run_lean.sh FILE.lean  (compiles against the replayed erdos684-lean build)
cd /tmp/e684/lean/repo && env -i PATH=$HOME/.elan/toolchains/leanprover--lean4---v4.32.2/bin:/usr/bin:/bin HOME=$HOME/MathDyad/erdos684/replay/home LANG=C.UTF-8 nice -n 19 lake env lean "$1"
