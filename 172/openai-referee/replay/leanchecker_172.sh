#!/bin/bash
# Re-run of the #181 driver's last step (died rc=127: copied .elan has no bin/ proxies) — toolchain bin dir on PATH directly.
P=/tmp/oai-math/lean-build
TC=$P/home/.elan/toolchains/leanprover--lean4---v4.34.1
cd $P/repo || exit 2
export HOME=$P/home ELAN_HOME=$P/home/.elan PATH=$TC/bin:/usr/local/bin:/usr/bin:/bin
t0=$(date +%s)
echo "start $(date -u +%FT%TZ)" > $P/leanchecker_fresh.rc
lake env leanchecker --fresh HindmanSumsProducts.Main > $P/leanchecker_fresh.log 2>&1
rc=$?
echo "leanchecker_fresh_172 $rc $(( $(date +%s) - t0 ))" >> $P/leanchecker_fresh.rc
echo "end $(date -u +%FT%TZ)" >> $P/leanchecker_fresh.rc
