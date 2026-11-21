#!/bin/bash
cd $HOME/MathDyad/erdos1186/quana/negctl; export PATH="$HOME/.elan/bin:$PATH"
CHK=$HOME/MathDyad/tools/lean4checker-v4.27.0/.lake/build/bin/lean4checker
( time nice -n 10 lake env $CHK --fresh NegCtl.Bad ) > ctl_bad_fresh.log 2>&1; echo "$(date -u +%FT%TZ) bad_fresh exit=$?" >> steps.tsv
( time nice -n 10 lake env $CHK --fresh NegCtl.Good ) > ctl_good_fresh.log 2>&1; echo "$(date -u +%FT%TZ) good_fresh exit=$?" >> steps.tsv
