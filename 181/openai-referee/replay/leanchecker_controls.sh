#!/bin/bash
# Controls for reading leanchecker's silence as success: (neg) a module that does not exist must fail loudly;
# (pos) a small real module, non-fresh, should exit 0 silently.
cd /tmp/oaimath/171/lean-build/repo
export HOME=/tmp/oaimath/171/lean-build/home ELAN_HOME=/tmp/oaimath/171/lean-build/home/.elan PATH=/tmp/oaimath/171/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/bin:/bin
O=/tmp/oaimath/171/lean-build/leanchecker_controls.log
: > $O
echo "== NEG: leanchecker HypercubeRamsey.DoesNotExist ==" >> $O
timeout 600 lake env leanchecker HypercubeRamsey.DoesNotExist >> $O 2>&1; echo "neg rc=$?" >> $O
echo "== POS: leanchecker HypercubeRamsey.Basic (non-fresh) ==" >> $O
timeout 1200 lake env leanchecker $(ls HypercubeRamsey/*.lean | head -1 | sed 's#/#.#; s#\.lean$##') >> $O 2>&1; echo "pos rc=$?" >> $O
echo DONE >> $O
