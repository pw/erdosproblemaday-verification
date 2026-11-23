#!/bin/bash
cd $HOME/MathDyad/erdos301/dellapietra/negctl; export PATH="$HOME/.elan/bin:$PATH"
st(){ echo "$(date -u +%FT%TZ) $*" >> steps.tsv; }
( lake build NegCtl.Bad NegCtl.Good ) > build.log 2>&1; st "build exit=$?"
( time nice -n 15 lake env leanchecker NegCtl.Bad ) > ctl_bad_nonfresh.log 2>&1; st "bad_nonfresh exit=$?"
( time nice -n 15 lake env leanchecker NegCtl.Good ) > ctl_good_nonfresh.log 2>&1; st "good_nonfresh exit=$?"
( time nice -n 15 lake env leanchecker --fresh NegCtl.Bad ) > ctl_bad_fresh.log 2>&1; st "bad_fresh exit=$?"
st done
