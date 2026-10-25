#!/bin/bash
# After the main #431 build ends: build the rest of the Jacobsthal (#970) closure (689 modules) into the same out/ dir,
# so the proof-term dependency probe can ask whether erdos_970_* use dirichlet_real_zero_bound.
L=/tmp/oaimath/013/lean-build
while ! grep -q '^build ' $L/steps.tsv; do sleep 30; done
cd $L && nice -n 19 python3 drive970.py 6 >> drive970.out 2>&1
