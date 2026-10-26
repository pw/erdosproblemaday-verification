#!/bin/bash
H=/tmp/oaimath/003/lean/home
export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1 PATH=$H/.elan/bin:/usr/local/bin:/usr/bin:/bin
echo "start $(date -u +%FT%TZ) df=$(df -h / | tail -1)"
nice -n 19 elan toolchain install leanprover/lean4:v4.34.1
echo "exit $? $(date -u +%FT%TZ) df=$(df -h / | tail -1)"
