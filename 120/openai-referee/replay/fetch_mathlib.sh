#!/bin/bash
set -u
L=/tmp/erdos0300/lean
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
cd $L
if [ ! -d mathlib4/.git ]; then
  mkdir -p mathlib4 && cd mathlib4 && git init -q && git remote add origin https://github.com/leanprover-community/mathlib4 && log "fetching d13f23b7" && git fetch -q --depth 1 origin d13f23b723b8a846827a245b89c10fc7d3f11612 && git checkout -q FETCH_HEAD && log "checked out $(git rev-parse HEAD)"
else cd mathlib4; fi
cat lean-toolchain
log "lake exe cache get"
nice -n 19 lake exe cache get 2>&1 | tail -20
log "cache get rc=${PIPESTATUS[0]}"
log "oleans: $(find .lake/build/lib/lean/Mathlib -name '*.olean' 2>/dev/null | wc -l)  packages: $(ls .lake/packages 2>/dev/null | tr '\n' ' ')"
du -sh .lake 2>/dev/null
log DONE
