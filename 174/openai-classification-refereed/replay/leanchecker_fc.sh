#!/bin/bash
# Family 172: leanchecker --fresh over Bridge174Main (imports Bridge174FC + OpenAI Main ⇒ SphericalRamsey + EuclideanRamsey closures + Mathlib + both FC bridges). Replaced a Bridge174FC-only run (killed after ~15 min, superset).
L=/tmp/oaimath/172/lean-build; B=/tmp/oaimath/172/bridge; source $B/lean_env.sh
export LEAN_PATH=$B/out:$LEAN_PATH
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
cd $B
step leanchecker_fresh_fc bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh Bridge174Main > $L/logs/leanchecker_fresh_fc.log 2>&1"
log "LEANCHECKER FC DONE"; touch $L/LC_FC_DONE
