#!/bin/bash
# run.sh FILE : compile one of our audit files against the built Erdos301 environment (read-only use of build/.lake).
Q=$HOME/MathDyad/erdos301/dellapietra
export LEAN_PATH=$(cd $Q/build && ~/.elan/bin/lake env printenv LEAN_PATH)
export LEAN_NUM_THREADS=2
cd $Q/ours
bash $Q/rsscap.sh 9000000 1800 ~/.elan/toolchains/leanprover--lean4---v4.33.0-rc1/bin/lean "$1"
