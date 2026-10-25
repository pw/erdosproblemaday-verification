#!/bin/bash
# Controls for reading leanchecker's silence as success on the #1083 replay build (same shape as #181's):
# (neg) a module that does not exist must fail loudly; (pos) a small real module, non-fresh, should exit 0 silently.
cd /tmp/oaimath/166/lean-build/repo
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan PATH=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/bin:/bin
O=/tmp/oaimath/166/lean-build/leanchecker_controls.log
: > $O
echo "== NEG: leanchecker DistinctDistances.DoesNotExist ==" >> $O
timeout 600 nice -n 19 lake env leanchecker DistinctDistances.DoesNotExist >> $O 2>&1; echo "neg rc=$?" >> $O
echo "== POS: leanchecker DistinctDistances.Framework (non-fresh) ==" >> $O
timeout 1800 nice -n 19 lake env leanchecker DistinctDistances.Framework >> $O 2>&1; echo "pos rc=$?" >> $O
echo DONE >> $O
