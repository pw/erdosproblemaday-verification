#!/bin/bash
H=/tmp/oaimath/003/lean/home
export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1 PATH=$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin
cd /tmp/erdos0300/lean/mathlib4
echo "start $(date -u +%FT%TZ) df=$(df -h / | tail -1)"
lean --version; lake --version
nice -n 19 lake exe cache get
echo "exit $? $(date -u +%FT%TZ) df=$(df -h / | tail -1)"
