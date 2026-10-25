#!/bin/bash
# Follow-up to run.sh: the first `lake build ErdosProblems -j2` failed instantly (Lake 5 has no -j), so the three audit
# steps ran against an unbuilt tree. check_release.sh (step their_check_release) does the real `lake build ErdosProblems`.
# This waits for that row, then re-runs the audits; leanchecker is handled by run.sh's own gate afterwards.
set -u
S=/tmp/erdos160/itabe/lean-build; R=/tmp/erdos160/itabe/repo
cd "$S"; log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
while ! grep -q '^their_check_release ' "$S/steps.tsv"; do sleep 60; done
log "check_release row: $(grep '^their_check_release ' $S/steps.tsv)"
cd "$R"; export PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=2 ELAN_TOOLCHAIN_GC_DISABLE=1
log "oleans built: $(find .lake/build/lib/lean/ErdosProblems -name '*.olean' 2>/dev/null | wc -l) of 21"
step build2 nice -n 19 lake build ErdosProblems
step their_audit2 bash -c "nice -n 19 lake env lean --trust=0 AxiomAudit.lean > $S/their_axioms.log 2>&1"
step our_audit2 bash -c "nice -n 19 lake env lean --trust=0 $S/Axioms160.lean > $S/axioms.log 2>&1"
step negcontrol2 bash -c "nice -n 19 lake env lean $S/NegControl.lean > $S/negcontrol.log 2>&1"
log "their_axioms.log:"; cat "$S/their_axioms.log"; log "axioms.log tail:"; tail -8 "$S/axioms.log"; log "negcontrol.log:"; cat "$S/negcontrol.log"
log DONE2
