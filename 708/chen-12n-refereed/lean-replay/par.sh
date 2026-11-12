#!/bin/bash
export PATH=$HOME/.elan/bin:$PATH
cd /tmp/e708/lean
for m in "$@"; do t0=$(date +%s); lake build "Erdos708.H97.Proofs.$m" > /tmp/e708/run/par_$m.log 2>&1; echo -e "par_$m\t$?\t$(( $(date +%s)-t0 ))\t$(date -u +%FT%TZ)" >> /tmp/e708/run/steps.tsv; done
