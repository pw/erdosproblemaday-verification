#!/bin/bash
set -u
D=$HOME/MathDyad/erdos488/alicien; L=$D/logs; cd $D/src/repo
export PATH="$HOME/.elan/bin:$PATH"; export LEAN_NUM_THREADS=4
stamp(){ echo "$(date -u +%FT%TZ) $*" >> $L/steps.tsv; }
stamp start; git rev-parse HEAD >> $L/steps.tsv
( time lake exe cache get ) > $L/cache_get.log 2>&1; stamp "cache_get exit=$?"
lean --version > $L/env.txt; lake --version >> $L/env.txt; git -C .lake/packages/mathlib rev-parse HEAD >> $L/env.txt
( time nice -n 10 lake build ) > $L/build.log 2>&1; rc=$?; stamp "build exit=$rc"
[ $rc -ne 0 ] && exit $rc
( time lake env lean CheckAxioms.lean ) > $L/check_axioms.log 2>&1; stamp "check_axioms exit=$?"
stamp done
