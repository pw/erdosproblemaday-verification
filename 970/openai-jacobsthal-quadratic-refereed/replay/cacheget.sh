#!/bin/bash
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1 PATH=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin
cd /tmp/erdos0300/lean/mathlib4
echo "start $(date -u +%FT%TZ) df=$(df -h / | tail -1)"
nice -n 19 lake exe cache get
echo "exit $? $(date -u +%FT%TZ) df=$(df -h / | tail -1)"
