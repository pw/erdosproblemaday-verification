#!/bin/bash
# Our cold replay of Ryan Coffey's Lean proof of FC's Erdos184.erdos_184 (github.com/steelwheel01/erdos-gallai-lean @ a11bb45 = the
# commit their public release run 36795612102 checked; Lean sources unchanged at HEAD 660ae11). Toolchain v4.33.1 (archive sha256
# verified vs their pin 890afd18…), Mathlib v4.33.1 cache, packages fetched depth-1 at the manifest SHAs (all 10 verified).
# GATES: #85 t1_rep0 exit; OpenAI replay build finished (no overlap); GO file; MemAvailable ≥ 28 GB. LEAN_NUM_THREADS=2 (≤ 2 lean jobs).
set -u
L=/tmp/oaimath/181/coffey; W=$L/ws/formal; G=/tmp/oaimath/181/lean-build
export HOME=$L/home ELAN_HOME=$L/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1 LEAN_NUM_THREADS=2
export PATH="$L/home/.elan/toolchains/leanprover--lean4---v4.33.1/bin:/usr/local/bin:/usr/bin:/bin"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return $rc; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
waitmem(){ local need=$1; while [ "$(memavail_gb)" -lt "$need" ]; do log "waiting(mem ≥ ${need}G): memavail=$(memavail_gb)G"; sleep 120; done; }
T1PID=$(cat $G/T1PID 2>/dev/null)
while [ -n "$T1PID" ] && kill -0 "$T1PID" 2>/dev/null; do log "waiting(#85 t1_rep0 pid $T1PID)"; sleep 120; done
while [ ! -e $G/BUILD_DONE ] || [ ! -e $G/GO ]; do log "waiting(OpenAI build done + GO)"; sleep 120; done
echo "launch $(date -u +%FT%TZ) 0 0" >> "$L/steps.tsv"; lean --version; log "repo HEAD: $(git -C $L/ws rev-parse HEAD)"
waitmem 28
step build bash -c "cd $W && nice -n 19 ionice -c2 -n7 lake build EG EGTest EGCheck EGCheck.Final > $L/logs/build.log 2>&1"
[ "$(tail -1 $L/steps.tsv | cut -d' ' -f2)" = 0 ] || { log "BUILD FAILED — no downstream steps (see logs/build.log)"; exit 1; }
waitmem 20
step ourcheck bash -c "cd $W && nice -n 19 lake env lean --trust=0 $L/probe/OurCheck.lean > $L/logs/ourcheck.log 2>&1"
step wrongshape bash -c "cd $W && nice -n 19 lake env lean $L/probe/WrongShape.lean > $L/logs/wrongshape.log 2>&1"
step negcontrol bash -c "cd $W && nice -n 19 lake env lean $L/probe/NegControl.lean > $L/logs/negcontrol.log 2>&1"
log "wrongshape rc must be NONZERO: $(grep '^wrongshape ' $L/steps.tsv | tail -1); ours axioms: $(grep -o "'ours184' depends on axioms: \[[^]]*\]" $L/logs/ourcheck.log)"
touch $L/CHECKS_DONE
while pgrep -x leanchecker >/dev/null 2>&1; do log "waiting(other leanchecker)"; sleep 120; done
waitmem 24
step leanchecker_fresh bash -c "cd $W && nice -n 19 lake env leanchecker --fresh EGCheck.Final > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "cd $W && nice -n 19 lake env leanchecker --fresh EGCheck.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "DONE — bank into verification/184/; then rm -rf $W/.lake + $L/home per the disk guard"
