#!/bin/bash
# Family 012 (#371): leanchecker --fresh over Bridge371 (imports OpenAI's PaperMain closure: 1,834 modules incl. patched PNT+/StrongPNT
# + LeanArchitect, + Mathlib, + our FC/#928 bridge). Missing-module control first (must fail).
L=/tmp/oaimath/012/lean-build; B=/tmp/oaimath/012/bridge
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$B/out:$(cat $L/lean_path.txt)
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
cd $B
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh Bridge371NoSuchModule > $L/logs/leanchecker_missing_control.log 2>&1"
step leanchecker_fresh bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh Bridge371 > $L/logs/leanchecker_fresh.log 2>&1"
log "LEANCHECKER DONE"; touch $L/LC_DONE
